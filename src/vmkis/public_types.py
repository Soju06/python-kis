"""공개 사용자용 타입 별칭 모음.

이 모듈은 사용자에게 노출되는 최소한의 타입 별칭만 제공합니다.
"""

from typing import TypeAlias

from vmkis.api.account.balance import KisIntegrationBalance as _KisIntegrationBalance
from vmkis.api.account.order import KisOrder as _KisOrder
from vmkis.api.stock.chart import KisChart as _KisChart
from vmkis.api.stock.market import KisMarketType as _KisMarketType
from vmkis.api.stock.order_book import KisOrderbook as _KisOrderbook
from vmkis.api.stock.quote import KisQuoteResponse as _KisQuoteResponse
from vmkis.api.stock.trading_hours import KisTradingHours as _KisTradingHours

Quote: TypeAlias = _KisQuoteResponse
Balance: TypeAlias = _KisIntegrationBalance
Order: TypeAlias = _KisOrder
Chart: TypeAlias = _KisChart
Orderbook: TypeAlias = _KisOrderbook
MarketInfo: TypeAlias = _KisMarketType
MarketType: TypeAlias = _KisMarketType
TradingHours: TypeAlias = _KisTradingHours

__all__ = [
    "Quote",
    "Balance",
    "Order",
    "Chart",
    "Orderbook",
    "MarketInfo",
    "MarketType",
    "TradingHours",
]
