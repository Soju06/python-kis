from typing import TYPE_CHECKING

from pykis.api.base.product import KisProductBase
from pykis.api.stock.market import MARKET_TYPE
from pykis.scope.base.scope import KisScope
from pykis.utils.repr import kis_repr

if TYPE_CHECKING:
    from pykis.kis import PyKis


@kis_repr(
    "market",
    "symbol",
    lines="single",
)
class KisProductScope(KisScope, KisProductBase):
    """한국투자증권 상품 기본정보"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """시장구분"""

    def __init__(self, kis: "PyKis", market: MARKET_TYPE):
        super().__init__(kis)
        self.market = market

    from pykis.api.stock.quote import product_quote as quote  # 시세 조회
