from typing import TYPE_CHECKING, Callable, Protocol, overload, runtime_checkable

from pykis.api.stock.market import MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.event.handler import KisEventFilter, KisEventHandler
from pykis.event.subscription import KisSubscriptionEventArgs
from pykis.responses.websocket import TWebsocketResponse

if TYPE_CHECKING:
    from pykis.api.account.order import KisOrderNumber
    from pykis.client.websocket import KisWebsocketClient

__all__ = [
    "KisOrderNumberEventFilter",
]


@runtime_checkable
class KisSimpleRealtimeExecution(Protocol):
    """한국투자증권 실시간체결 프로토콜"""

    @property
    def order_number(self) -> "KisOrderNumber":
        """주문번호"""
        ...


@runtime_checkable
class KisSimpleOrderNumberProtocol(Protocol):
    """한국투자증권 주문번호 프로토콜"""

    @property
    def symbol(self) -> str:
        """종목코드"""
        ...

    @property
    def market(self) -> MARKET_TYPE:
        """시장유형"""
        ...

    @property
    def branch(self) -> str:
        """지점코드"""
        ...

    @property
    def number(self) -> str:
        """주문번호"""
        ...

    @property
    def account_number(self) -> KisAccountNumber:
        """계좌번호"""
        ...


class KisSimpleOrderNumber:
    """한국투자증권 주문번호"""

    __slots__ = ("market", "symbol", "branch", "number", "account_number")

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """시장유형"""
    branch: str
    """지점코드"""
    number: str
    """주문번호"""
    account_number: KisAccountNumber

    def __init__(self, symbol: str, market: MARKET_TYPE, branch: str, number: str, account: KisAccountNumber):
        self.symbol = symbol
        self.market = market
        self.branch = branch
        self.number = number
        self.account_number = account


class KisOrderNumberEventFilter(KisEventFilter["KisWebsocketClient", KisSubscriptionEventArgs[TWebsocketResponse]]):
    _order: KisSimpleOrderNumberProtocol | Callable[..., KisSimpleOrderNumberProtocol]

    @overload
    def __init__(self, symbol: str, /, market: MARKET_TYPE, branch: str, number: str, account: KisAccountNumber): ...

    @overload
    def __init__(self, symbol: "KisOrderNumber", /): ...

    @overload
    def __init__(self, callable: Callable[..., KisSimpleOrderNumberProtocol], /): ...

    def __init__(
        self,
        symbol_or_callable: "KisOrderNumber | str | Callable[..., KisSimpleOrderNumberProtocol]",
        market: MARKET_TYPE | None = None,
        branch: str | None = None,
        number: str | None = None,
        account: KisAccountNumber | None = None,
    ):
        super().__init__()

        if isinstance(symbol_or_callable, str):
            if market is None:
                raise ValueError("market is required")

            if branch is None:
                raise ValueError("branch is required")

            if number is None:
                raise ValueError("number is required")

            if account is None:
                raise ValueError("account is required")

            self._order = KisSimpleOrderNumber(
                symbol=symbol_or_callable,
                market=market,
                branch=branch,
                number=number,
                account=account,
            )
        else:
            self._order = symbol_or_callable

    def __filter__(
        self,
        handler: KisEventHandler,
        sender: "KisWebsocketClient",
        e: KisSubscriptionEventArgs[TWebsocketResponse],
    ) -> bool:
        """
        이벤트를 필터링합니다.

        Args:
            sender: 이벤트 발생 객체
            e: 이벤트 데이터

        Returns:
            `False`일 경우 이벤트를 전달합니다.
            `True`일 경우 이벤트를 무시합니다.
        """
        if not isinstance(e.response, KisSimpleRealtimeExecution):
            return True

        order = e.response.order_number
        value = self._order() if callable(self._order) else self._order

        return not (
            order.symbol == value.symbol
            and order.market == value.market
            and (order.foreign or order.branch == value.branch)
            and int(order.number) == int(value.number)
            and order.account_number == value.account_number
        )
