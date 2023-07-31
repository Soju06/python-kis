from datetime import datetime, timedelta
from threading import Lock
from typing import TYPE_CHECKING
from .responses import KisAccessTokenResponse
from ..timezone import tz_kst

if TYPE_CHECKING:
    from .client import KisClient


class KisAccessToken:
    """한국투자증권 API 접속 토큰"""

    client: "KisClient"
    """한국투자증권 API 클라이언트"""
    token: str
    """접속 토큰"""
    token_type: str
    """토큰 타입"""
    expires_in: int
    """토큰 만료"""
    timestamp: datetime
    """토큰 발급 시간"""
    expires_at: datetime
    """토큰 만료 시간"""
    empty: bool
    _ensure_lock: Lock

    def __init__(self, client: "KisClient"):
        self.client = client
        self.token = ""
        self.token_type = ""
        self.expires_in = -1
        self.timestamp = datetime.now(tz_kst)
        self.expires_at = datetime.now(tz_kst)
        self.empty = True
        self._ensure_lock = Lock()

    def issue(self):
        """토큰을 발급합니다."""
        self.client.logger.info("ACCESS_TOKEN: issue access token")
        data = self.client.request(
            "post",
            "/oauth2/tokenP",
            body={"grant_type": "client_credentials"},
            auth=False,
            appkey_location="body",
            response=KisAccessTokenResponse,
        )

        self.token = data.access_token
        self.token_type = data.token_type
        self.expires_in = data.expires_in
        self.timestamp = data.timestamp
        self.expires_at = self.timestamp + timedelta(seconds=self.expires_in)
        self.empty = False

    def expired(self):
        """토큰이 만료되었는지 확인합니다."""
        return self.empty or self.expires_at < datetime.now(tz_kst)

    def ensure(self):
        """토큰이 만료되었으면 새로 발급합니다."""
        with self._ensure_lock:
            if self.expired():
                self.issue()

    def discard(self):
        """토큰을 폐기합니다."""
        if self.expired():
            return

        self.client.request(
            "post",
            "/oauth2/revokeP",
            body={"token": self.token},
            auth=False,
            appkey_location="body",
        )

        self.token = ""
        self.token_type = ""
        self.expires_in = -1
        self.timestamp = datetime.now(tz_kst)
        self.expires_at = datetime.now(tz_kst)
        self.empty = True

    def __enter__(self) -> str:
        self.ensure()
        return self.token

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
