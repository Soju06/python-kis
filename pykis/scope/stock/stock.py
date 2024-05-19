from decimal import Decimal
from typing import TYPE_CHECKING

from pykis.api.account.order import ORDER_CONDITION, ORDER_EXECUTION
from pykis.api.stock.market import MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.scope.base.product import KisProductScope

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisStock(KisProductScope):
    """한국투자증권 주식 Scope"""

    account_number: KisAccountNumber | None

    def __init__(
        self,
        kis: "PyKis",
        symbol: str,
        market: MARKET_TYPE,
        account: KisAccountNumber | None = None,
    ):
        super().__init__(kis=kis, market=market)
        self.symbol = symbol
        self.account_number = account

    @property
    def account(self) -> KisAccountNumber:
        """
        계좌 정보를 반환합니다. 스코프에 계좌 정보가 없는 경우 기본 계좌 정보를 반환합니다.

        Raises:
            ValueError: 스코프에 계좌 정보가 없으며, 기본 계좌 정보가 없을 경우
        """
        if self.account_number is None:
            return self.kis.primary

        return self.account_number

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(kis=kis, symbol={self.symbol!r}, market={self.market!r}, account={self.account_number!r})"
