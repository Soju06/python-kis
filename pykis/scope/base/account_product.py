from typing import TYPE_CHECKING

from pykis.api.base.account_product import KisAccountProductBase
from pykis.api.stock.market import MARKET_TYPE
from pykis.scope.base.product import KisProductScope
from pykis.utils.repr import kis_repr

if TYPE_CHECKING:
    from pykis.kis import PyKis


@kis_repr(
    "account_number",
    "market",
    "symbol",
    lines="single",
)
class KisAccountProductScope(KisProductScope, KisAccountProductBase):
    """한국투자증권 상품 기본정보"""

    def __init__(self, kis: "PyKis", market: MARKET_TYPE, symbol: str):
        super().__init__(
            kis,
            market=market,
            symbol=symbol,
        )
