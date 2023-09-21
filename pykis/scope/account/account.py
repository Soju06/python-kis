from typing import TYPE_CHECKING

from pykis.__env__ import EMPTY, EMPTY_TYPE
from pykis.api.stock.info import info as _info
from pykis.api.stock.market import MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.scope.base.account import KisAccountScope
from pykis.scope.stock.info_stock import KisInfoStock

if TYPE_CHECKING:
    from pykis.kis import PyKis

class KisAccount(KisAccountScope):
    """한국투자증권 계좌 Scope"""

    def __repr__(self) -> str:
        return f"KisAccount({self.account})"
    
    def stock(self, code: str, market: MARKET_TYPE | None | EMPTY_TYPE = EMPTY) -> KisInfoStock:
        """
        종목을 조회하고 종목 Scope를 반환합니다.

        Args:
            code (str): 종목코드
            market (str): 상품유형명 (기본값: 현재 스코프의 상품유형명)
        """
        if market is EMPTY:
            market = self.market

        return KisInfoStock(
            kis=self.kis,
            info=_info(
                self.kis,
                code=code,
                market=market,  # type: ignore
            ),
            account=self.account,
        )

def account(
    self: "PyKis",
    account: str | KisAccountNumber | None = None,
    market: MARKET_TYPE | None = "KRX",
    primary: bool = False,
) -> KisAccount:
    """계좌 정보를 반환합니다.

    Args:
        account: 계좌 번호. None이면 기본 계좌 정보를 사용합니다.
        market: 상품유형. None이면 모든 상품유형을 사용합니다.
        primary: 기본 계좌로 설정할지 여부
    """
    if isinstance(account, str):
        account = KisAccountNumber(account)

    account = account or self._primary_account

    if primary:
        self.primary_account = account

    return KisAccount(
        kis=self,
        account=account,
        market=market,
    )
