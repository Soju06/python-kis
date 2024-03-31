from typing import TYPE_CHECKING

from pykis.api.base.account import KisAccountBase
from pykis.api.base.product import KisProductBase
from pykis.api.stock.market import MARKET_TYPE
from pykis.client.account import KisAccountNumber

if TYPE_CHECKING:
    from pykis.scope.account.account import KisAccount


class KisAccountProductBase(KisAccountBase, KisProductBase):
    """한국투자증권 계좌 상품 기본정보"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(account_number={self.account_number!r}, code={self.symbol!r}, market={self.market!r})"

    @property
    def account(self) -> "KisAccount":
        """
        계좌 Scope

        해당 계좌 Scope는 해당 상품에 해당하는 시장에 대한 정보를 제공합니다.
        """
        return self.kis.account(account=self.account_number)
