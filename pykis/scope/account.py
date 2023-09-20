from typing import TYPE_CHECKING

from pykis.client.account import KisAccountNumber
from pykis.scope.scope import KisScope

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisAccountScope(KisScope):
    """한국투자증권 계좌 Base Scope"""

    account: KisAccountNumber | None
    """Scope에서 사용할 계좌 정보"""

    def __init__(self, kis: "PyKis", account: KisAccountNumber | None = None):
        super().__init__(kis)
        self.account = account

    @property
    def _account(self) -> KisAccountNumber:
        """계좌 정보를 반환합니다."""
        if self.account is None:
            return self.kis._primary_account

        return self.account


class KisAccount(KisAccountScope):
    """한국투자증권 계좌 Scope"""

    def __repr__(self) -> str:
        return f"KisAccount({self.account})"
    
    def stock(self, code: str, name: str) -> "KisStock":
        """주식 Scope를 생성합니다."""
        return KisStock(self.kis, code, name, account=self._account)
