from typing import Callable, Literal, Protocol, overload, runtime_checkable

from pykis.api.base.product import KisProductProtocol
from pykis.api.websocket.order_book import KisRealtimeOrderBook
from pykis.api.websocket.price import KisRealtimePrice
from pykis.client.websocket import KisWebsocketClient
from pykis.event.handler import KisEventFilter, KisEventTicket
from pykis.event.subscription import KisSubscriptionEventArgs

__all__ = [
    "KisWebsocketQuotableProduct",
    "KisWebsocketQuotableProductImpl",
]


@runtime_checkable
class KisWebsocketQuotableProduct(Protocol):
    """한국투자증권 웹소켓 시세조회가능 상품 프로토콜"""

    @overload
    def on(
        self,
        event: Literal["price"],
        callback: Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]], None],
        where: KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]] | None = None,
        once: bool = False,
        extended: bool = False,
    ) -> KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]]:
        """
        웹소켓 이벤트 핸들러 등록

        Args:
            event (Literal["price"]): 이벤트 타입
            callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]], None]): 콜백 함수
            where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]] | None, optional): 이벤트 필터. Defaults to None.
            once (bool, optional): 한번만 실행할지 여부. Defaults to False.
            extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)
        """
        raise NotImplementedError

    @overload
    def on(
        self,
        event: Literal["orderbook"],
        callback: Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]], None],
        where: (
            KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]] | None
        ) = None,
        once: bool = False,
        extended: bool = False,
    ) -> KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]]:
        """
        웹소켓 이벤트 핸들러 등록

        Args:
            event (TEventType): 이벤트 타입
            callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]], None]): 콜백 함수
            where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]] | None, optional): 이벤트 필터. Defaults to None.
            once (bool, optional): 한번만 실행할지 여부. Defaults to False.
            extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)
        """
        raise NotImplementedError

    def on(
        self,
        event: Literal["price", "orderbook"],
        callback: (
            Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]], None]
            | Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]], None]
        ),
        where: (
            KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]]
            | KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]]
            | None
        ) = None,
        once: bool = False,
        extended: bool = False,
    ) -> (
        KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]]
        | KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]]
    ):
        raise NotImplementedError

    @overload
    def once(
        self,
        event: Literal["price"],
        callback: Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]], None],
        where: KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]] | None = None,
        extended: bool = False,
    ) -> KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]]:
        """
        웹소켓 이벤트 핸들러 등록

        Args:
            event (Literal["price"]): 이벤트 타입
            callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]], None]): 콜백 함수
            where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]] | None, optional): 이벤트 필터. Defaults to None.
            extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)
        """
        raise NotImplementedError

    @overload
    def once(
        self,
        event: Literal["orderbook"],
        callback: Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]], None],
        where: (
            KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]] | None
        ) = None,
        extended: bool = False,
    ) -> KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]]:
        """
        웹소켓 이벤트 핸들러 등록

        Args:
            event (Literal["orderbook"]): 이벤트 타입
            callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]], None]): 콜백 함수
            where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]] | None, optional): 이벤트 필터. Defaults to None.
            extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)
        """
        raise NotImplementedError

    def once(
        self,
        event: Literal["price", "orderbook"],
        callback: (
            Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]], None]
            | Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]], None]
        ),
        where: (
            KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]]
            | KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]]
            | None
        ) = None,
        extended: bool = False,
    ) -> (
        KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]]
        | KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]]
    ):
        raise NotImplementedError


class KisWebsocketQuotableProductImpl:
    """한국투자증권 웹소켓 시세조회가능 상품"""

    @overload
    def on(
        self: "KisProductProtocol",
        event: Literal["price"],
        callback: Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]], None],
        where: KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]] | None = None,
        once: bool = False,
        extended: bool = False,
    ) -> KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]]:
        """
        웹소켓 이벤트 핸들러 등록

        Args:
            event (Literal["price"]): 이벤트 타입
            callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]], None]): 콜백 함수
            where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]] | None, optional): 이벤트 필터. Defaults to None.
            once (bool, optional): 한번만 실행할지 여부. Defaults to False.
            extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)
        """

    @overload
    def on(
        self: "KisProductProtocol",
        event: Literal["orderbook"],
        callback: Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]], None],
        where: (
            KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]] | None
        ) = None,
        once: bool = False,
        extended: bool = False,
    ) -> KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]]:
        """
        웹소켓 이벤트 핸들러 등록

        Args:
            event (TEventType): 이벤트 타입
            callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]], None]): 콜백 함수
            where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]] | None, optional): 이벤트 필터. Defaults to None.
            once (bool, optional): 한번만 실행할지 여부. Defaults to False.
            extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)
        """

    def on(
        self: "KisProductProtocol",
        event: Literal["price", "orderbook"],
        callback: (
            Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]], None]
            | Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]], None]
        ),
        where: (
            KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]]
            | KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]]
            | None
        ) = None,
        once: bool = False,
        extended: bool = False,
    ) -> (
        KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]]
        | KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]]
    ):
        if event == "price":
            from pykis.api.websocket.price import on_product_price as on_price

            return on_price(
                self,
                callback,  # type: ignore
                where=where,
                once=once,
                extended=extended,
            )
        elif event == "orderbook":
            from pykis.api.websocket.order_book import (
                on_product_order_book as on_orderbook,
            )

            return on_orderbook(
                self,
                callback,  # type: ignore
                where=where,
                once=once,
                extended=extended,
            )

        raise ValueError(f"Unknown event: {event}")

    @overload
    def once(
        self: "KisProductProtocol",
        event: Literal["price"],
        callback: Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]], None],
        where: KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]] | None = None,
        extended: bool = False,
    ) -> KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]]:
        """
        웹소켓 이벤트 핸들러 등록

        Args:
            event (Literal["price"]): 이벤트 타입
            callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]], None]): 콜백 함수
            where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]] | None, optional): 이벤트 필터. Defaults to None.
            extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)
        """
        raise NotImplementedError

    @overload
    def once(
        self: "KisProductProtocol",
        event: Literal["orderbook"],
        callback: Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]], None],
        where: (
            KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]] | None
        ) = None,
        extended: bool = False,
    ) -> KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]]:
        """
        웹소켓 이벤트 핸들러 등록

        Args:
            event (Literal["orderbook"]): 이벤트 타입
            callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]], None]): 콜백 함수
            where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]] | None, optional): 이벤트 필터. Defaults to None.
            extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)
        """
        raise NotImplementedError

    def once(
        self: "KisProductProtocol",
        event: Literal["price", "orderbook"],
        callback: (
            Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]], None]
            | Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]], None]
        ),
        where: (
            KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]]
            | KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]]
            | None
        ) = None,
        extended: bool = False,
    ) -> (
        KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]]
        | KisEventTicket[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderBook]]
    ):
        """
        웹소켓 이벤트 핸들러 등록

        Args:
            event (Literal["price", "orderbook"]): 이벤트 타입
            callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice | KisRealtimeOrderBook]], None]): 콜백 함수
            where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]] | None, optional): 이벤트 필터. Defaults to None.
            extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)
        """
        if event == "price":
            from pykis.api.websocket.price import on_product_price as on_price

            return on_price(
                self,
                callback,  # type: ignore
                where=where,
                once=True,
                extended=extended,
            )
        elif event == "orderbook":
            from pykis.api.websocket.order_book import (
                on_product_order_book as on_orderbook,
            )

            return on_orderbook(
                self,
                callback,  # type: ignore
                where=where,
                once=True,
                extended=extended,
            )
