from typing import TYPE_CHECKING
from pykis.api.stock.market import MARKET_TYPE, MARKET_TYPE_KOR_MAP

from pykis.scope.base.scope import KisScope

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisMarketScope(KisScope):
    """한국투자증권 계좌 Base Scope"""

    market: MARKET_TYPE | None
    """시장구분"""

    @property
    def market_name(self) -> str:
        """시장구분 한글"""
        return MARKET_TYPE_KOR_MAP[self.market]

    def __init__(self, kis: "PyKis", market: MARKET_TYPE | None = None):
        super().__init__(kis)
        self.market = market
