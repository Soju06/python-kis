from typing import TYPE_CHECKING
from pykis.client.account import KisAccountNumber
from pykis.client.object import KisObjectBase

if TYPE_CHECKING:
    from pykis.scope.account.account import KisAccount


class KisAccountBase(KisObjectBase):
    """한국투자증권 계좌 기본정보"""

    account_number: KisAccountNumber
    """계좌번호"""

    @property
    def account(self) -> "KisAccount":
        """
        계좌 Scope

        해당 `KisAccountBase`의 계좌 Scope는 전체 시장에 대한 정보를 제공합니다.
        Product에 따라 시장 정보를 제공받으려면 `KisAccountProductBase`를 사용하세요.
        """
        return self.kis.account(account=self.account_number)
