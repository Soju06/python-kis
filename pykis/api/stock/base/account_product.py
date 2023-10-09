from typing import TYPE_CHECKING
from pykis.api.stock.base.account import KisAccountBase
from pykis.api.stock.base.product import KisProductBase

if TYPE_CHECKING:
    from pykis.scope.account.account import KisAccount


class KisAccountProductBase(KisAccountBase, KisProductBase):
    """한국투자증권 계좌 상품 기본정보"""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(account_number={self.account_number!r}, code={self.code!r}, market={self.market!r})"

    @property
    def account(self) -> "KisAccount":
        """
        계좌 Scope

        해당 계좌 Scope는 해당 상품에 해당하는 시장에 대한 정보를 제공합니다.
        """
        return self.kis.account(
            account=self.account_number,
            market=self.market,
        )
