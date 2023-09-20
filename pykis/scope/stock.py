from typing import TYPE_CHECKING
from pykis.api.stock.info import info as _info

from pykis.api.stock.market import MARKET_TYPE, MARKET_TYPE_KOR_MAP
from pykis.client.account import KisAccountNumber
from pykis.scope.account import KisAccountScope
from pykis.utils.cache import cached

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisStock(KisAccountScope):
    """한국투자증권 주식 Scope"""

    code: str
    """종목코드"""
    name: str
    """종목명"""
    market: MARKET_TYPE
    """시장구분"""

    @property
    def market_kor(self) -> str:
        """시장구분 한글"""
        return MARKET_TYPE_KOR_MAP[self.market]  # type: ignore

    def __init__(self, kis: "PyKis", code: str, name: str, account: KisAccountNumber | None = None):
        super().__init__(kis, account=account)
        self.code = code
        self.name = name

    def __repr__(self) -> str:
        return f"KisStock(code='{self.code}', name='{self.name}', account={self.account})"

    @cached
    def info(self):
        """종목정보 조회"""
        return _info(self.kis, code=self.code, market=self.market)
    
    