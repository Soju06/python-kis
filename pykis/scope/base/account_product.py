from typing import TYPE_CHECKING

from pykis.api.base.account_product import KisAccountProductBase
from pykis.api.stock.market import MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.scope.base.product import KisProductScope
from pykis.utils.repr import kis_repr

if TYPE_CHECKING:
    from pykis.kis import PyKis


__all__ = [
    "KisAccountProductScope",
]


@kis_repr(
    "account_number",
    "market",
    "symbol",
    lines="single",
)
class KisAccountProductScope(KisProductScope, KisAccountProductBase):
    """한국투자증권 상품 기본정보"""

    account_number: KisAccountNumber
    """계좌번호"""

    def __init__(self, kis: "PyKis", market: MARKET_TYPE, symbol: str, account: KisAccountNumber):
        super().__init__(
            kis=kis,
            market=market,
            symbol=symbol,
        )
        self.account_number = account

    from pykis.api.account.order import account_product_order as order  # 주문
    from pykis.api.account.orderable_amount import (
        account_product_orderable_amount as orderable_amount,  # 주문 가능 금액 조회
    )
