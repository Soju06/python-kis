from typing import TYPE_CHECKING, Callable, Literal, Protocol, runtime_checkable

from pykis.api.base.account import KisAccountProtocol
from pykis.event.handler import KisEventFilter, KisEventTicket, KisMultiEventFilter
from pykis.event.subscription import KisSubscriptionEventArgs

if TYPE_CHECKING:
    from pykis.api.account.order import KisOrder
    from pykis.api.websocket.order_execution import KisRealtimeExecution
    from pykis.client.websocket import KisWebsocketClient

__all__ = [
    "KisRealtimeOrderableAccount",
    "KisRealtimeOrderableAccountMixin",
]


@runtime_checkable
class KisRealtimeOrderableAccount(Protocol):
    """한국투자증권 실시간 주문가능 상품 프로토콜"""

    def on(
        self,
        event: Literal["execution"],
        callback: "Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]], None]",
        where: "KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]] | None" = None,
        once: bool = False,
    ) -> "KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]]":
        """
        웹소켓 이벤트 핸들러 등록

        [국내주식] 실시간시세 -> 국내주식 실시간체결통보[실시간-005]
        [해외주식] 실시간시세 -> 해외주식 실시간체결통보[실시간-009]

        Args:
            callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]], None]): 콜백 함수
            where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]] | None, optional): 이벤트 필터. Defaults to None.
            once (bool, optional): 한번만 실행 여부. Defaults to False.
        """
        ...

    def once(
        self,
        event: Literal["execution"],
        callback: "Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]], None]",
        where: "KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]] | None" = None,
    ) -> "KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]]":
        """
        웹소켓 이벤트 핸들러 등록

        [국내주식] 실시간시세 -> 국내주식 실시간체결통보[실시간-005]
        [해외주식] 실시간시세 -> 해외주식 실시간체결통보[실시간-009]

        Args:
            callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]], None]): 콜백 함수
            where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]] | None, optional): 이벤트 필터. Defaults to None.
        """
        ...


class KisRealtimeOrderableAccountMixin:
    """한국투자증권 실시간 주문가능 상품"""

    def on(
        self: "KisAccountProtocol",
        event: Literal["execution"],
        callback: "Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]], None]",
        where: "KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]] | None" = None,
        once: bool = False,
    ) -> "KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]]":
        """
        웹소켓 이벤트 핸들러 등록

        [국내주식] 실시간시세 -> 국내주식 실시간체결통보[실시간-005]
        [해외주식] 실시간시세 -> 해외주식 실시간체결통보[실시간-009]

        Args:
            callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]], None]): 콜백 함수
            where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]] | None, optional): 이벤트 필터. Defaults to None.
            once (bool, optional): 한번만 실행 여부. Defaults to False.
        """
        from pykis.api.websocket.order_execution import on_account_execution

        if event == "execution":
            return on_account_execution(
                self,
                callback=callback,
                where=where,
                once=once,
            )

        raise ValueError(f"Unknown event: {event}")

    def once(
        self: "KisAccountProtocol",
        event: Literal["execution"],
        callback: "Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]], None]",
        where: "KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]] | None" = None,
    ) -> "KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]]":
        """
        웹소켓 이벤트 핸들러 등록

        [국내주식] 실시간시세 -> 국내주식 실시간체결통보[실시간-005]
        [해외주식] 실시간시세 -> 해외주식 실시간체결통보[실시간-009]

        Args:
            callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]], None]): 콜백 함수
            where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]] | None, optional): 이벤트 필터. Defaults to None.
        """
        from pykis.api.websocket.order_execution import on_account_execution

        if event == "execution":
            return on_account_execution(
                self,
                callback=callback,
                where=where,
                once=True,
            )

        raise ValueError(f"Unknown event: {event}")


class KisRealtimeOrderableOrderMixin:
    """한국투자증권 실시간 주문 가능 주문"""

    def on(
        self: "KisOrder",
        event: Literal["execution"],
        callback: "Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]], None]",
        where: "KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]] | None" = None,
        once: bool = False,
    ) -> "KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]]":
        """
        웹소켓 이벤트 핸들러 등록

        [국내주식] 실시간시세 -> 국내주식 실시간체결통보[실시간-005]
        [해외주식] 실시간시세 -> 해외주식 실시간체결통보[실시간-009]

        Args:
            callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]], None]): 콜백 함수
            where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]] | None, optional): 이벤트 필터. Defaults to None.
            once (bool, optional): 한번만 실행 여부. Defaults to False.
        """
        from pykis.api.websocket.order_execution import on_account_execution

        if event == "execution":
            return on_account_execution(
                self,
                callback=callback,
                where=KisMultiEventFilter(self, where) if where else self,
                once=once,
            )

        raise ValueError(f"Unknown event: {event}")

    def once(
        self: "KisOrder",
        event: Literal["execution"],
        callback: "Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]], None]",
        where: "KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]] | None" = None,
    ) -> "KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]]":
        """
        웹소켓 이벤트 핸들러 등록

        [국내주식] 실시간시세 -> 국내주식 실시간체결통보[실시간-005]
        [해외주식] 실시간시세 -> 해외주식 실시간체결통보[실시간-009]

        Args:
            callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]], None]): 콜백 함수
            where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]] | None, optional): 이벤트 필터. Defaults to None.
        """
        from pykis.api.websocket.order_execution import on_account_execution

        if event == "execution":
            return on_account_execution(
                self,
                callback=callback,
                where=KisMultiEventFilter(self, where) if where else self,
                once=True,
            )

        raise ValueError(f"Unknown event: {event}")
