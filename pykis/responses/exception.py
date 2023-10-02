from typing import Any

from requests import Response

from pykis.client.exception import KisException


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
