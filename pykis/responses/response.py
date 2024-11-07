from typing import Any, Protocol, runtime_checkable

from requests import Response

from pykis.client.exceptions import KisAPIError
from pykis.client.object import KisObjectBase, KisObjectProtocol
from pykis.client.page import KisPage, KisPageStatus, to_page_status
from pykis.responses.dynamic import (
    KisDynamic,
    KisDynamicProtocol,
    KisDynamicScopedPath,
    KisObject,
)
from pykis.responses.exceptions import KisNotFoundError
from pykis.responses.types import KisAny, KisString

__all__ = [
    "raise_not_found",
    "KisResponse",
    "KisAPIResponse",
    "KisPaginationAPIResponse",
]


def raise_not_found(
    data: dict[str, Any],
    message: str | None = None,
    **fields: Any,
) -> KisNotFoundError:
    """
    응답 데이터가 없음 예외를 발생시킵니다.

    Args:
        data (dict[str, Any]): 응답 데이터
        message (str | None, optional): 예외 메시지. Defaults to None.
        fields (dict[str, Any], optional): 요청 조건 필드. Defaults to {}.

    Raises:
        KisNotFoundError: 응답 데이터가 없는 경우
    """
    raise KisNotFoundError(
        data=data,
        response=data["__response__"],
        message=message,
        fields=fields,
    )


@runtime_checkable
class KisResponseProtocol(KisDynamicProtocol, KisObjectProtocol, Protocol):
    """KIS 응답 결과 프로토콜"""

    @property
    def __response__(self) -> Response | None:
        """원본 응답 데이터"""
        ...

    @property
    def __message__(self) -> str:
        """응답 메시지"""
        ...

    @property
    def __code__(self) -> str:
        """응답 코드"""
        ...


class KisResponse(KisDynamic, KisObjectBase):
    """KIS 응답 결과"""

    __response__: Response | None = KisAny(lambda r: r)("__response__", absolute=True)
    """원본 응답 데이터"""
    __message__: str = KisAny(lambda s: s.strip())("msg1", absolute=True)
    """응답 메시지"""
    __code__: str = KisString()("msg_cd", absolute=True)
    """응답 코드"""

    def __pre_init__(self, data: dict[str, Any]) -> None:
        super().__pre_init__(data)

        if int(data["rt_cd"]) != 0:
            raise KisAPIError(
                data=data,
                response=data["__response__"],
            )

    def raw(self) -> dict[str, Any] | None:
        """원본 응답 데이터의 복사본을 반환합니다."""
        if self.__data__ is None:
            return None

        data = self.__data__.copy()
        data.pop("__response__", None)

        return data


class KisAPIResponse(KisResponse):
    """KIS API 응답 결과"""

    __path__: KisDynamicScopedPath | str | None = "output"


@runtime_checkable
class KisPaginationAPIResponseProtocol(KisResponseProtocol, Protocol):
    """KIS Pagination API 응답 결과 프로토콜"""

    @property
    def page_status(self) -> KisPageStatus:
        """페이징 상태"""
        ...

    @property
    def next_page(self) -> KisPage:
        """페이징 정보"""
        ...

    @property
    def is_last(self) -> bool:
        """마지막 페이지인지 확인합니다."""
        ...

    @property
    def has_next(self) -> bool:
        """다음 페이지가 있는지 확인합니다."""
        ...


class KisPaginationAPIResponse(KisAPIResponse):
    """KIS Pagination API 응답 결과"""

    page_status: KisPageStatus
    """페이징 상태"""
    next_page: KisPage
    """페이징 정보"""

    @property
    def is_last(self) -> bool:
        """마지막 페이지인지 확인합니다."""
        return self.page_status == "end"

    @property
    def has_next(self) -> bool:
        """다음 페이지가 있는지 확인합니다."""
        return self.page_status != "end" and not self.next_page.is_empty

    def __pre_init__(self, data: dict[str, Any]) -> None:
        super().__pre_init__(data)

        response: Response = data["__response__"]

        self.page_status = to_page_status(response.headers["tr_cont"])
        self.next_page = KisObject.transform_(
            data=data,
            transform_type=KisPage,
            ignore_missing=True,
        )
