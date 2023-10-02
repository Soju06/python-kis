from typing import Any

from requests import Response
from pykis.client.exception import KisAPIError
from pykis.client.object import KisObjectBase
from pykis.responses.dynamic import KisDynamic
from pykis.responses.exception import KisNotFoundError
from pykis.responses.types import KisAny, KisString


def raise_not_found(data: dict[str, Any], message: str | None = None, **fields: Any) -> KisNotFoundError:
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


class KisResponse(KisDynamic, KisObjectBase):
    """KIS 응답 결과"""

    __response__: Response | None = KisAny(lambda r: r)("__response__", absolute=True)
    """원본 응답 데이터"""
    __message__: str = KisAny(lambda s: s.strip())("msg1", absolute=True)
    """응답 메시지"""
    __code__: str = KisString()("msg_cd", absolute=True)
    """응답 코드"""

    def __pre_init__(self, data: dict[str, Any]):
        super().__pre_init__(data)

        if int(data["rt_cd"]) != 0:
            raise KisAPIError(
                data=data,
                response=data["__response__"],
            )


class KisAPIResponse(KisResponse):
    """KIS API 응답 결과"""

    __path__ = "output"
