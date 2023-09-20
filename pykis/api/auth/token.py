from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from pykis.__env__ import TIMEZONE
from pykis.client.form import KisForm
from pykis.responses.types import KisDatetime, KisDynamic, KisInt, KisString

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisAccessToken(KisDynamic, KisForm):
    """한국투자증권 API 접속 토큰"""

    token: str = KisString["access_token"]
    """접속 토큰"""
    type: str = KisString["token_type"]
    """토큰 타입"""
    expired_at: datetime = KisDatetime("%Y-%m-%d %H:%M:%S")["access_token_token_expired"]
    """만료 시각"""
    validity_period: int = KisInt["expires_in"]
    """토큰 유효기간 (초)"""

    @property
    def expired(self) -> bool:
        """토큰이 만료되었는지 여부"""
        return self.expired_at < datetime.now(TIMEZONE)

    @property
    def remaining(self) -> timedelta:
        """토큰의 남은 유효기간"""
        return self.expired_at - datetime.now(TIMEZONE)

    def build(self, dict: dict[str, Any] | None = None) -> dict[str, Any]:
        if dict is None:
            dict = {}

        dict["Authorization"] = f"{self.type} {self.token}"

        return dict

    def __str__(self) -> str:
        return f"{self.type} {self.token}"

    def __repr__(self) -> str:
        return f"<KisAccessToken {self.type} expired_at={self.expired_at}>"


def token_issue(self: "PyKis"):
    """
    API 접속 토큰을 발급합니다.

    OAuth인증 -> 접근토큰발급(P)[인증-001]
    (업데이트 날짜: 2023/09/05)
    """
    return self.fetch(
        "/oauth2/tokenP",
        body={
            "grant_type": "client_credentials",
        },
        appkey_location="body",
        response_type=KisAccessToken,
        method="POST",
        auth=False,
    )


def token_revoke(self: "PyKis", token: str):
    """
    API 접속 토큰을 폐기합니다.

    OAuth인증 -> 접근토큰폐기(P)[인증-002]
    (업데이트 날짜: 2023/09/05)

    Args:
        token (str): 접속 토큰
    """
    res = self.request(
        "/oauth2/revokeP",
        body={
            "token": token,
        },
        appkey_location="body",
        method="POST",
        auth=False,
    )

    if not res.ok:
        raise ValueError(f"토큰 폐기에 실패했습니다. ({res.status_code}, {res.text})")
