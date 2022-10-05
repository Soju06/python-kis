
from dataclasses import dataclass

APPKEY_LENGTH = 36
APPSECRET_LENGTH = 180

@dataclass
class KisKey:
    appkey: str
    appsecret: str
    virtual_account: bool

    def __init__(self, appkey: str, appsecret: str, virtual_account: bool = False):
        if len(appkey) != APPKEY_LENGTH:
            raise ValueError(f'AppKey 길이는 {APPKEY_LENGTH}자여야 합니다.')
        if len(appsecret) != APPSECRET_LENGTH:
            raise ValueError(f'AppSecret 길이는 {APPSECRET_LENGTH}자여야 합니다.')

        self.appkey = appkey
        self.appsecret = appsecret
        self.virtual_account = virtual_account
