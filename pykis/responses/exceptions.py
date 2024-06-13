from typing import Any

from requests import Response

from pykis.client.exceptions import KisAPIError, KisException

__all__ = [
    "KisNotFoundError",
    "KisMarketNotOpenedError",
]


class KisNotFoundError(KisException):
    """KIS API 요청 결과가 없는 경우"""

    data: dict[str, Any]
    """응답 데이터"""

    def __init__(
        self,
        data: dict,
        response: Response,
        message: str | None = None,
        fields: dict[str, Any] = {},
    ):
        super().__init__(
            (message if message else "KIS API 요청한 자료가 존재하지 않습니다.")
            + f" ({', '.join(f'{k}={v!r}' for k, v in fields.items())})",
            response=response,
        )
        self.data = data


class KisMarketNotOpenedError(KisAPIError):
    """시장이 열리지 않은 경우"""

    def __init__(self, data: dict, response: Response):
        super().__init__(data, response)
