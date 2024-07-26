from typing import TYPE_CHECKING

from pykis.event.handler import KisEventFilterBase, KisEventHandler
from pykis.event.subscription import KisSubscriptionEventArgs
from pykis.responses.websocket import TWebsocketResponse

if TYPE_CHECKING:
    from pykis.client.websocket import KisWebsocketClient


__all__ = [
    "KisSubscriptionEventFilter",
]


class KisSubscriptionEventFilter(
    KisEventFilterBase["KisWebsocketClient", KisSubscriptionEventArgs[TWebsocketResponse]]
):
    """TR 구독 이벤트 필터"""

    __slots__ = ("id", "key")

    def __init__(self, id: str, key: str | None = None):
        self.id = id
        self.key = key

    def __filter__(
        self,
        handler: KisEventHandler,
        sender: "KisWebsocketClient",
        e: KisSubscriptionEventArgs[TWebsocketResponse],
    ) -> bool:
        return not (e.tr.id == self.id and (self.key is None or e.tr.key == self.key))

    def __hash__(self) -> int:
        return hash((self.__class__, self.id, self.key))
