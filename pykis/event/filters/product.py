from typing import TYPE_CHECKING, Protocol, overload, runtime_checkable

from pykis.api.base.product import KisProductProtocol
from pykis.api.stock.market import MARKET_TYPE
from pykis.event.handler import KisEventFilterBase, KisEventHandler
from pykis.event.subscription import KisSubscriptionEventArgs
from pykis.responses.websocket import TWebsocketResponse

if TYPE_CHECKING:
    from pykis.client.websocket import KisWebsocketClient

__all__ = [
    "KisProductEventFilter",
]


@runtime_checkable
class KisSimpleProductProtocol(Protocol):
    """한국투자증권 상품 프로토콜"""

    @property
    def symbol(self) -> str:
        """종목코드"""
        ...

    @property
    def market(self) -> MARKET_TYPE:
        """시장유형"""
        ...


class KisSimpleProduct:
    """한국투자증권 상품"""

    __slots__ = ("market", "symbol")

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """시장유형"""

    def __init__(self, symbol: str, market: MARKET_TYPE):
        self.symbol = symbol
        self.market = market


class KisProductEventFilter(KisEventFilterBase["KisWebsocketClient", KisSubscriptionEventArgs[TWebsocketResponse]]):

    _product: KisSimpleProductProtocol

    @overload
    def __init__(self, symbol: str, market: MARKET_TYPE): ...

    @overload
    def __init__(self, symbol: KisProductProtocol, /): ...

    def __init__(self, symbol: KisProductProtocol | str, market: MARKET_TYPE | None = None):
        super().__init__()

        if isinstance(symbol, str):
            if market is None:
                raise ValueError("market is required")

            self._product = KisSimpleProduct(symbol=symbol, market=market)
        else:
            self._product = symbol

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
        # runtime_checkable isinstance은 프로퍼티 값의 타입을 비교하므로 의도되지 않은 접근이 발생할 수 있습니다.
        # if isinstance(e.response, KisProductProtocol):
        #     return False

        return not (
            isinstance(e.response, KisSimpleProductProtocol)
            and e.response.symbol == self._product.symbol
            and e.response.market == self._product.market
        )

    def __hash__(self) -> int:
        return hash((self.__class__, self._product))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(symbol={self._product.symbol!r}, market={self._product.market!r})"

    def __str__(self) -> str:
        return repr(self)
