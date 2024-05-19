from typing import Any

from pykis.__env__ import APPKEY_LENGTH, SECRETKEY_LENGTH
from pykis.client.form import KisForm

__all__ = ["KisKey"]


class KisKey(KisForm):
    """
    한국투자증권 Open API 인증키
    https://apiportal.koreainvestment.com/intro 에서 발급 받으십시오.
    """

    appkey: str
    """앱 키"""
    secretkey: str
    """앱 시크릿"""

    def __init__(self, appkey: str, secretkey: str):
        if len(appkey) != APPKEY_LENGTH:
            raise ValueError(f"appkey 길이는 {APPKEY_LENGTH}자여야 합니다.")
        if len(secretkey) != SECRETKEY_LENGTH:
            raise ValueError(f"secretkey 길이는 {SECRETKEY_LENGTH}자여야 합니다.")

        self.appkey = appkey
        self.secretkey = secretkey

    def build(self, dict: dict[str, Any] | None = None) -> dict[str, Any]:
        if dict is None:
            dict = {}

        dict.update(
            {
                "appkey": self.appkey,
                "appsecret": self.secretkey,
            }
        )
        return dict

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(appkey={self.appkey}, secretkey=***)"
