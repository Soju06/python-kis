from typing import Any

from requests import Response
from pykis.client.exception import KisAPIError
from pykis.client.object import KisObjectBase
from pykis.responses.dynamic import KisDynamic
from pykis.responses.types import KisAny, KisString


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
