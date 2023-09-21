from datetime import time
from typing import TYPE_CHECKING
from pykis.api.stock.info import info as _info

from pykis.api.stock.market import MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.scope.account.account import KisAccountScope
from pykis.utils.cache import cached

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisStock(KisAccountScope):
    """한국투자증권 주식 Scope"""

    code: str
    """종목코드"""
    name: str
    """종목명"""

    def __init__(
        self,
        kis: "PyKis",
        code: str,
        name: str,
        market: MARKET_TYPE | None = None,
        account: KisAccountNumber | None = None,
    ):
        super().__init__(
            kis=kis,
            market=market,
            account=account,
        )
        self.code = code
        self.name = name

    def __repr__(self) -> str:
        return f"KisStock(code='{self.code}', name='{self.name}', account={self.account})"

    @property
    @cached
    def info(self):
        """종목정보 조회"""
        return _info(
            self.kis,
            code=self.code,
            market=self.market,
        )
