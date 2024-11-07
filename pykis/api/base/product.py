from typing import TYPE_CHECKING, Protocol, runtime_checkable

from pykis.api.base.market import KisMarketBase, KisMarketProtocol
from pykis.api.stock.market import MARKET_TYPE
from pykis.utils.repr import kis_repr

if TYPE_CHECKING:
    from pykis.api.stock.info import KisStockInfo
    from pykis.kis import PyKis
    from pykis.scope.stock import KisStock

__all__ = [
    "KisProductProtocol",
    "KisProductBase",
]


@runtime_checkable
class KisProductProtocol(KisMarketProtocol, Protocol):
    """한국투자증권 상품 프로토콜"""

    @property
    def symbol(self) -> str:
        """종목코드"""
        ...

    @property
    def name(self) -> str:
        """상품명"""
        ...

    @property
    def info(self) -> "KisStockInfo":
        """상품기본정보 조회"""
        ...

    @property
    def stock(self) -> "KisStock":
        """종목 Scope"""
        ...


@kis_repr(
    "market",
    "symbol",
    lines="single",
)
class KisProductBase(KisMarketBase):
    """한국투자증권 상품 기본정보"""

    kis: "PyKis"
    """
    한국투자증권 API.
    
    Note:
        기본적으로 __init__ 호출 이후 라이브러리 단위에서 lazy initialization 되며,
        라이브러리 내에서는 해당 속성을 사용할 때 초기화 단계에서 사용하지 않도록 해야합니다.
    """

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    @property
    def name(self) -> str:
        """상품명"""
        return self.info.name

    @property
    def info(self) -> "KisStockInfo":
        """
        상품기본정보 조회.

        국내주식시세 -> 상품기본조회[v1_국내주식-029]

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 종목 코드가 올바르지 않은 경우
        """
        from pykis.api.stock.info import info as _info

        return _info(
            self.kis,
            symbol=self.symbol,
            market=self.market,
        )

    @property
    def stock(self) -> "KisStock":
        """종목 Scope"""
        from pykis.scope.stock import stock

        return stock(
            self.kis,
            symbol=self.symbol,
            market=self.market,
        )
