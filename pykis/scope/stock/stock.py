from typing import TYPE_CHECKING

from pykis.api.stock.info import info as _info
from pykis.api.stock.market import MARKET_TYPE
from pykis.api.stock.quote import quote as _quote
from pykis.client.account import KisAccountNumber
from pykis.scope.account.account import KisAccountScope
from pykis.scope.base.product import KisProductScopeBase
from pykis.utils.cache import cached

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisStock(KisAccountScope, KisProductScopeBase):
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
        return f"{self.__class__.__name__}(code={self.code!r}, name={self.name!r})"
