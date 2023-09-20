from dataclasses import dataclass
from typing import Any
from pykis.__env__ import APPKEY_LENGTH, APPSECRET_LENGTH

from pykis.client.form import KisForm


class KisKey(KisForm):
    """
    한국투자증권 Open API 인증키
    https://apiportal.koreainvestment.com/intro 에서 발급 받으십시오.
    """

    appkey: str
    """앱 키"""
    appsecret: str
    """앱 시크릿"""

    def __init__(self, appkey: str, appsecret: str):
        if len(appkey) != APPKEY_LENGTH:
            raise ValueError(f"AppKey 길이는 {APPKEY_LENGTH}자여야 합니다.")
        if len(appsecret) != APPSECRET_LENGTH:
            raise ValueError(f"AppSecret 길이는 {APPSECRET_LENGTH}자여야 합니다.")

        self.appkey = appkey
        self.appsecret = appsecret

    def build(self, dict: dict[str, Any] | None = None) -> dict[str, Any]:
        if dict is None:
            dict = {}

        dict.update({"appkey": self.appkey, "appsecret": self.appsecret})
        return dict

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(appkey={self.appkey}, appsecret=***)"
