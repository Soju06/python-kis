from typing import TYPE_CHECKING

from pykis.api.base.account import KisAccountBase
from pykis.client.account import KisAccountNumber
from pykis.scope.base.scope import KisScope

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisAccountScope(KisScope, KisAccountBase):
    """한국투자증권 계좌 Base Scope"""

    account_number: KisAccountNumber | None
    """Scope에서 사용할 계좌 정보"""

    def __init__(self, kis: "PyKis", account: KisAccountNumber | None = None):
        super().__init__(kis=kis)
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
