from typing import Callable, Literal, Protocol, runtime_checkable

from pykis.api.base.account import KisAccountProtocol
from pykis.api.websocket.order_execution import KisRealtimeOrderExecution
from pykis.client.websocket import KisWebsocketClient
from pykis.event.handler import KisEventFilter, KisEventTicket
from pykis.event.subscription import KisSubscriptionEventArgs

__all__ = [
    "KisRealtimeOrderableAccount",
    "KisRealtimeOrderableAccountImpl",
]


# TODO: 종목 체결 필터


@runtime_checkable
class KisRealtimeOrderableAccount(Protocol):
    """한국투자증권 실시간 주문가능 상품 프로토콜"""

    def on(
        self,
        event: Literal["execution"],
        callback: Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderExecution]], None],
        where: (
            KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderExecution]] | None
        ) = None,
        once: bool = False,
    ) -> KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderExecution]]:
        raise NotImplementedError


class KisRealtimeOrderableAccountImpl:
    """한국투자증권 실시간 주문가능 상품"""

    def on(
        self: "KisAccountProtocol",
        event: Literal["execution"],
        callback: Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderExecution]], None],
        where: (
            KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderExecution]] | None
        ) = None,
        once: bool = False,
    ) -> KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderExecution]]:
        from pykis.api.websocket.order_execution import on_account_execution

        if event == "execution":
            return on_account_execution(
                self,
                callback=callback,
                where=where,
                once=once,
            )

        raise ValueError(f"Unknown event: {event}")
