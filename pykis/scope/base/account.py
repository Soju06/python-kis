from typing import TYPE_CHECKING

from pykis.api.stock.market import MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.scope.base.market import KisMarketScope

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisAccountScope(KisMarketScope):
    """한국투자증권 계좌 Base Scope"""

    account: KisAccountNumber | None
    """Scope에서 사용할 계좌 정보"""

    def __init__(
        self, kis: "PyKis", market: MARKET_TYPE | None = None, account: KisAccountNumber | None = None
    ):
        super().__init__(
            kis=kis,
            market=market,
        )
        self.account = account

    @property
    def _account(self) -> KisAccountNumber:
        """
        계좌 정보를 반환합니다. 스코프에 계좌 정보가 없는 경우 기본 계좌 정보를 반환합니다.

        Raises:
            ValueError: 스코프에 계좌 정보가 없으며, 기본 계좌 정보가 없을 경우
        """
        if self.account is None:
            return self.kis.primary

        return self.account
