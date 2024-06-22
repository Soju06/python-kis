from pykis.client.messaging import KisWebsocketTR
from pykis.event.handler import KisEventArgs
from pykis.responses.websocket import KisWebsocketResponse


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


class KisSubscriptionEventArgs(KisEventArgs):
    """실시간 구독 이벤트 데이터"""

    tr: KisWebsocketTR
    """구독된 실시간 TR"""
    response: KisWebsocketResponse
    """실시간 응답 객체"""

    def __init__(self, tr: KisWebsocketTR, response: KisWebsocketResponse):
        super().__init__()
        self.tr = tr
        self.response = response
