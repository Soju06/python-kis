from typing import Protocol

from pykis.api.stock.market import MARKET_TYPE, MARKET_TYPE_KOR_MAP
from pykis.client.object import KisObjectBase, KisObjectProtocol
from pykis.utils.repr import kis_repr


class KisMarketProtocol(KisObjectProtocol, Protocol):
    """한국투자증권 시장 프로토콜"""

    @property
    def market(self) -> MARKET_TYPE:
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


@kis_repr(
    "market",
    lines="single",
)
class KisMarketBase(KisObjectBase):
    """한국투자증권 시장 베이스"""

    market: MARKET_TYPE
    """시장유형"""

    @property
    def market_name(self) -> str:
        """실제 상품유형명"""
        return MARKET_TYPE_KOR_MAP[self.market]

    @property
    def foreign(self) -> bool:
        """해외종목 여부"""
        from pykis.api.stock.info import MARKET_TYPE_MAP

        return self.market not in MARKET_TYPE_MAP["KRX"]

    @property
    def domestic(self) -> bool:
        """국내종목 여부"""
        return not self.foreign
