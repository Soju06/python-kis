from typing import Any

from requests import Response
from pykis.client.exception import KisAPIError
from pykis.responses.dynamic import KisDynamic, KisObject, TDynamic
from pykis.responses.types import KisAny, KisString


class KisResponse(KisDynamic):
    """KIS 응답 결과"""

    __response__: Response | None = KisAny(lambda r: r)["__response__"]
    """원본 응답 데이터"""

    message: str = KisAny(lambda s: s.strip())["msg1"]
    """응답 메시지"""
    code: str = KisString["msg_cd"]
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

    __ignore_missing__: bool = True

    def __pre_init__(self, data: dict[str, Any], field: str = "output"):
        super().__pre_init__(data)
        KisObject.transform_(
            data[field],
            self,
            ignore_missing=True,
            pre_init=False,
        )
