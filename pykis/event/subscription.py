from typing import Generic

from pykis.client.messaging import KisWebsocketTR
from pykis.event.handler import KisEventArgs
from pykis.responses.websocket import TWebsocketResponse

__all__ = [
    "KisSubscribedEventArgs",
    "KisUnsubscribedEventArgs",
    "KisSubscriptionEventArgs",
]


class KisSubscribedEventArgs(KisEventArgs):
    """실시간 구독 추가 이벤트 데이터"""

    tr: KisWebsocketTR
    """구독된 실시간 TR"""

    def __init__(self, tr: KisWebsocketTR):
        super().__init__()
        self.tr = tr


class KisUnsubscribedEventArgs(KisEventArgs):
    """실시간 구독 해제 이벤트 데이터"""

    tr: KisWebsocketTR
    """해제된 실시간 TR"""

    def __init__(self, tr: KisWebsocketTR):
        super().__init__()
        self.tr = tr


class KisSubscriptionEventArgs(Generic[TWebsocketResponse], KisEventArgs):
    """실시간 구독 이벤트 데이터"""

    tr: KisWebsocketTR
    """구독된 실시간 TR"""
    response: TWebsocketResponse
    """실시간 응답 객체"""

    def __init__(self, tr: KisWebsocketTR, response: TWebsocketResponse):
        super().__init__()
        self.tr = tr
        self.response = response
