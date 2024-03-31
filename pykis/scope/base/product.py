from typing import TYPE_CHECKING

from pykis.api.base.product import KisProductBase
from pykis.api.stock.market import MARKET_TYPE
from pykis.scope.base.scope import KisScope
from pykis.utils.cache import cached

if TYPE_CHECKING:
    from pykis.api.stock.info import KisStockInfo
    from pykis.kis import PyKis
    from pykis.scope.stock.info_stock import KisInfoStock


class KisProductScope(KisScope, KisProductBase):
    """한국투자증권 상품 기본정보"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """시장구분"""

    def __init__(self, kis: "PyKis", market: MARKET_TYPE):
        super().__init__(kis)
        self.market = market

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self.symbol}, market={self.market})"

    @property
    @cached
    def info(self) -> "KisStockInfo":
        """
        상품기본정보 조회.

        국내주식시세 -> 상품기본조회[v1_국내주식-029]

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 종목 코드가 올바르지 않은 경우
        """
        from pykis.api.stock.info import info

        return info(
            self.kis,
            symbol=self.symbol,
            market=self.market,
        )

    @property
    def stock(self) -> "KisInfoStock":
        """종목 Scope"""
        from pykis.scope.stock.info_stock import KisInfoStock

        return KisInfoStock(
            kis=self.kis,
            info=self.info,
        )
