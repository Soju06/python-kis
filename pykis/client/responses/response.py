from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Iterable, TypeVar

import requests

from ..exception import KisAPIError
from ..page import KisPage, KisPageStatus, to_page_status
from .dynamic import STORE_RESPONSE, KisDynamic


@dataclass
class KisResponse:
    def __init__(self, data: dict, response: requests.Response):
        pass


class KisAPIResponse(KisResponse):
    """KIS API 응답 결과"""

    id: str
    """거래 ID"""
    uid: str
    """거래고유번호"""
    message: str
    """응답 메시지"""
    code: str
    """응답 코드"""
    _sf_dbl: bool = False
    """중복 생성 방지"""

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        if self._sf_dbl:
            return

        self._sf_dbl = True
        self.id = response.headers["tr_id"]
        self.uid = response.headers["gt_uid"]
        self.message = data["msg1"].strip()
        self.code = data["msg_cd"]

        if int(data["rt_cd"]) != 0:
            raise KisAPIError(
                data=data,
                response=response,
            )

        del data["rt_cd"], data["msg1"], data["msg_cd"]


class KisPagingAPIResponse(KisAPIResponse):
    """KIS Paging API 응답 결과"""

    page_status: KisPageStatus
    """페이징 상태"""
    next_page: KisPage
    """페이징 정보"""

    @property
    def is_last(self) -> bool:
        """마지막 페이지인지 확인합니다."""
        return self.page_status == "end"

    def __init__(self, data: dict, response: requests.Response, page_size: int = 100):
        super().__init__(data, response)
        self.page_status = to_page_status(response.headers["tr_cont"])
        self.next_page = KisPage(data, page_size)


class KisDynamicAPIResponse(KisAPIResponse, KisDynamic):
    header: dict[str, str] | None = None
    """원본 응답 헤더"""

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        KisDynamic.__init__(self, data)  # type: ignore

        if STORE_RESPONSE:
            self.header = dict(response.headers)


TFPR = TypeVar("TFPR", bound="KisDynamicPagingAPIResponse")


class KisDynamicPagingAPIResponse(KisPagingAPIResponse, KisDynamicAPIResponse):
    def __init__(self, data: dict, response: requests.Response, page_size: int = 100):
        super().__init__(data, response, page_size)
        KisDynamicAPIResponse.__init__(self, data, response)  # type: ignore

    @abstractmethod
    def __add__(self, other: TFPR) -> TFPR:
        raise NotImplementedError

    @staticmethod
    def iterable(
        fetch_func: Callable[..., TFPR | None],
        args: Iterable,
        kwargs: dict[str, Any],
        page: KisPage = KisPage.first(),
        count: int | None = None,
        detect_inf_repet: bool = True,
    ) -> Iterable[TFPR]:
        """페이징 API 응답을 순회할 수 있는 반복자를 반환합니다."""
        i = 0

        while not count or i < count:
            kwargs["page"] = page
            response = fetch_func(*args, **kwargs)

            if response is None:
                return

            yield response

            if response.is_last:
                return

            page = response.next_page
            i += 1

            if detect_inf_repet and page.empty:
                raise ValueError("무한 순회가 감지되었습니다.")

    @staticmethod
    def join(items: Iterable[TFPR]) -> TFPR:
        """페이징 API 응답을 하나의 응답으로 합칩니다."""
        item = None

        for i in items:
            if item is None:
                item = i
            else:
                item += i

        if item is None:
            raise ValueError("조회된 주문이 없습니다.")

        return item


class KisDynamicLongPagingAPIResponse(KisDynamicPagingAPIResponse):
    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response, 200)


class KisDynamicZeroPagingAPIResponse(KisDynamicPagingAPIResponse):
    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response, 0)
