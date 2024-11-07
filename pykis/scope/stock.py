from typing import TYPE_CHECKING, Protocol

from pykis.adapter.account_product.order import (
    KisOrderableAccountProduct,
    KisOrderableAccountProductMixin,
)
from pykis.adapter.product.quote import KisQuotableProduct, KisQuotableProductMixin
from pykis.adapter.websocket.price import (
    KisWebsocketQuotableProduct,
    KisWebsocketQuotableProductMixin,
)
from pykis.api.base.account_product import (
    KisAccountProductBase,
    KisAccountProductProtocol,
)
from pykis.api.stock.info import MARKET_INFO_TYPES
from pykis.api.stock.info import info as _info
from pykis.client.account import KisAccountNumber
from pykis.client.websocket import KisWebsocketClient
from pykis.event.filters.product import KisProductEventFilter
from pykis.event.handler import KisEventFilter
from pykis.event.subscription import KisSubscriptionEventArgs
from pykis.scope.base import KisScope, KisScopeBase

if TYPE_CHECKING:
    from pykis.api.stock.market import MARKET_TYPE
    from pykis.kis import PyKis

__all__ = [
    "KisStock",
    "KisStockScope",
]


class KisStock(
    # Base
    KisScope,
    KisAccountProductProtocol,
    # Adapters
    KisOrderableAccountProduct,
    KisWebsocketQuotableProduct,
    KisQuotableProduct,
    # Filters
    KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs],
    Protocol,
):
    """한국투자증권 주식 Base Scope"""


class KisStockScope(
    # Base
    KisScopeBase,
    KisAccountProductBase,
    # Adapters
    KisOrderableAccountProductMixin,
    KisWebsocketQuotableProductMixin,
    KisQuotableProductMixin,
    # Filters
    KisProductEventFilter,
):
    """한국투자증권 주식 Base Scope"""

    symbol: str
    """종목코드"""
    market: "MARKET_TYPE"
    """상품유형타입"""

    account_number: KisAccountNumber
    """Scope에서 사용할 계좌 정보"""

    def __init__(
        self,
        kis: "PyKis",
        market: "MARKET_TYPE",
        symbol: str,
        account: KisAccountNumber,
    ):
        super().__init__(kis=kis)
        KisProductEventFilter.__init__(self, self)  # Register event filter
        self.market = market
        self.symbol = symbol
        self.account_number = account


def stock(
    self: "PyKis",
    symbol: str,
    market: MARKET_INFO_TYPES = None,
    account: KisAccountNumber | None = None,
) -> KisStock:
    """
    종목을 조회하고 종목 Scope를 반환합니다.

    국내주식시세 -> 상품기본조회[v1_국내주식-029]

    Args:
        symbol (str): 종목코드
        market (str): 상품유형명
        account (KisAccountNumber): 계좌번호

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    info = _info(
        self,
        symbol=symbol,
        market=market,
    )

    return KisStockScope(
        kis=self,
        symbol=info.symbol,
        market=info.market,
        account=account or self.primary,
    )
