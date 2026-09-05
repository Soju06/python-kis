from typing import TYPE_CHECKING, Literal

from vmkis.responses.dynamic import KisDynamic
from vmkis.responses.types import KisString

if TYPE_CHECKING:
    from vmkis.kis import VmKis

__all__ = [
    "KisWebsocketApprovalKey",
    "websocket_approval_key",
]


class KisWebsocketApprovalKey(KisDynamic):
    """한국투자증권 웹소켓 접속 키"""

    approval_key: str = KisString["approval_key"]
    """접속 키"""


def websocket_approval_key(self: "VmKis", domain: Literal["live", "paper"] | None = None) -> KisWebsocketApprovalKey:
    """
    웹소켓 접속 키를 발급합니다.

    OAuth인증 -> 실시간 (웹소켓) 접속키 발급[실시간-000]
    (업데이트 날짜: 2024/04/04)
    """
    appkey = self.appkey if domain == "live" else self.paper_appkey

    if appkey is None:
        raise ValueError("모의도메인 appkey가 없습니다.")

    return self.fetch(
        "/oauth2/Approval",
        body={
            "grant_type": "client_credentials",
            "appkey": appkey.appkey,
            "secretkey": appkey.secretkey,
        },
        response_type=KisWebsocketApprovalKey,
        method="POST",
        auth=False,
        appkey_location=None,
        verbose=False,
    )
