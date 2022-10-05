
from base64 import b64decode
from typing import TYPE_CHECKING, Any
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

if TYPE_CHECKING:
    from .messaging import KisRTSysResponse

class KisRTEncrypt:
    key: str
    iv: str

    def __init__(self, res: 'KisRTSysResponse'):
        if not res.key or not res.iv:
            raise Exception('암호화 키가 없습니다.')
        self.key = res.key
        self.iv = res.iv


    def decrypt(self, data: bytes | str) -> str:
        if isinstance(data, str):
            data = b64decode(data)
        data = unpad(AES.new(self.key.encode('utf-8'), AES.MODE_CBC, self.iv.encode('utf-8')).decrypt(data), AES.block_size)
        return bytes.decode(data)
