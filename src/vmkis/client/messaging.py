from typing import TYPE_CHECKING, Any, Literal

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from vmkis.client.form import KisForm
from vmkis.client.object import KisObjectBase
from vmkis.utils.repr import kis_repr

if TYPE_CHECKING:
    from vmkis.kis import VmKis

__all__ = [
    "KisWebsocketForm",
    "KisWebsocketRequest",
    "TR_SUBSCRIBE_TYPE",
    "TR_UNSUBSCRIBE_TYPE",
    "KisWebsocketTR",
    "KisWebsocketEncryptionKey",
]


class KisWebsocketForm(KisForm):
    """한국투자증권 실시간 요청 본문"""


class KisWebsocketRequest(KisForm, KisObjectBase):
    """한국투자증권 실시간 요청"""

    type: str
    """요청 타입"""
    body: KisWebsocketForm | None
    """요청 본문"""
    domain: Literal["live", "paper"] | None = None
    """요청 도메인"""

    def __init__(
        self,
        kis: "VmKis",
        type: str,
        body: KisWebsocketForm | None = None,
        domain: Literal["live", "paper"] | None = None,
    ):
        super().__init__()
        self.kis = kis
        self.type = type
        self.body = body
        self.domain = domain

    def build(self, dict: dict[str, Any] | None = None) -> dict[str, Any]:
        # 순환 회피용 지연 import. 파일 상단으로 올리지 마세요.
        # vmkis.api.auth.websocket 이 다시 client 를 import 하므로, 모듈 레벨로
        # 올리면 패키지가 로드 불능이 됩니다(ARCHITECTURE.md 불변식 3번).
        #
        # client -> api 는 이슈 #17 이 없앤 역방향 간선이고 pyproject.toml 의
        # import-linter 계약 "client 는 api 를 import 하지 않는다" 가 이를 막습니다.
        # 이 한 줄만 그 계약의 ignore_imports 에 면제로 등록되어 있습니다.
        from vmkis.api.auth.websocket import websocket_approval_key

        dict = dict or {}

        dict["header"] = {
            "approval_key": websocket_approval_key(
                self.kis,
                domain=self.domain,
            ).approval_key,
            "custtype": "P",
            "tr_type": self.type,
            "content-type": "utf-8",
        }

        if self.body is not None:
            dict["body"] = {"input": self.body.build()}

        return dict


TR_SUBSCRIBE_TYPE: str = "1"
TR_UNSUBSCRIBE_TYPE: str = "2"


@kis_repr(
    "id",
    "key",
    lines="single",
)
class KisWebsocketTR(KisWebsocketForm):
    """한국투자증권 실시간 TR 요청"""

    __slots__ = [
        "id",
        "key",
    ]

    id: str
    """TR ID"""
    key: str
    """TR Key"""

    def __init__(self, tr_id: str, tr_key: str):
        super().__init__()

        self.id = tr_id
        self.key = tr_key

    def build(self, dict: dict[str, Any] | None = None) -> dict[str, Any]:
        dict = dict or {}

        dict["tr_id"] = self.id
        dict["tr_key"] = self.key

        return dict

    def __str__(self) -> str:
        if self.key:
            return f"{self.id}.{self.key}"

        return self.id

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id and self.key == other.key

    def __hash__(self) -> int:
        return hash((self.id, self.key))

    def __copy__(self) -> "KisWebsocketTR":
        return self.__class__(self.id, self.key)

    def __deepcopy__(self, memo: dict[int, Any]) -> "KisWebsocketTR":
        return self.__copy__()


class KisWebsocketEncryptionKey:
    """한국투자증권 실시간 암호화 키"""

    __slots__ = [
        "iv",
        "key",
    ]

    iv: bytes
    """Initialization Vector"""
    key: bytes
    """Key"""

    def __init__(self, iv: bytes, key: bytes):
        super().__init__()

        self.iv = iv
        self.key = key

    @property
    def cipher(self):
        return Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())

    def decrypt(self, data: bytes) -> bytes:
        decryptor = self.cipher.decryptor()
        decrypted_data = decryptor.update(data) + decryptor.finalize()

        # Unpadding the decrypted data
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()  # type: ignore
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        return unpadded_data

    def text(self, data: bytes) -> str:
        return self.decrypt(data).decode("utf-8")
