from typing import TYPE_CHECKING, Protocol, runtime_checkable

from pykis.client.object import KisObjectBase, KisObjectProtocol
from pykis.utils.repr import kis_repr

if TYPE_CHECKING:
    from pykis.api.stock.market import CURRENCY_TYPE, MARKET_TYPE


__all__ = [
    "KisMarketProtocol",
    "KisMarketBase",
]


@runtime_checkable
class KisMarketProtocol(KisObjectProtocol, Protocol):
    """한국투자증권 시장 프로토콜"""

    @property
    def market(self) -> "MARKET_TYPE":
        """시장유형"""
        ...

    @property
    def market_name(self) -> str:
        """실제 상품유형명"""
        ...

    @property
    def foreign(self) -> bool:
        """해외종목 여부"""
        ...

    @property
    def domestic(self) -> bool:
        """국내종목 여부"""
        ...

    @property
    def currency(self) -> "CURRENCY_TYPE":
        """통화"""
        ...


@kis_repr(
    "market",
    lines="single",
)
class KisMarketBase(KisObjectBase):
    """한국투자증권 시장 베이스"""

    market: "MARKET_TYPE"
    """시장유형"""

    @property
    def market_name(self) -> str:
        """실제 상품유형명"""
        from pykis.api.stock.market import get_market_name

        return get_market_name(self.market)

    @property
    def foreign(self) -> bool:
        """해외종목 여부"""
        from pykis.api.stock.info import MARKET_TYPE_MAP

        return self.market not in MARKET_TYPE_MAP["KRX"]

    @property
    def domestic(self) -> bool:
        """국내종목 여부"""
        return not self.foreign

    @property
    def currency(self) -> "CURRENCY_TYPE":
        """통화"""
        from pykis.api.stock.market import get_market_currency

        return get_market_currency(self.market)
