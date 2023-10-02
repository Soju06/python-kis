from typing import TYPE_CHECKING

from pykis.api.stock.market import MARKET_TYPE, MARKET_TYPE_KOR_MAP
from pykis.client.object import KisObjectBase
from pykis.utils.cache import cached

if TYPE_CHECKING:
    from pykis.api.stock.info import KisStockInfo
    from pykis.scope.stock.info_stock import KisInfoStock
    from pykis.api.stock.quote import KisQuote


class KisProductScopeBase(KisObjectBase):
    """한국투자증권 상품 기본정보"""

    code: str
    """종목코드"""
    market: MARKET_TYPE | None
    """상품유형타입"""

    @property
    def primary_market(self) -> MARKET_TYPE:
        """실제 상품유형타입"""
        if self.market is not None:
            return self.market

        return self.info.market

    @property
    def market_name(self) -> str:
        """시장 종류"""
        return MARKET_TYPE_KOR_MAP[self.market]

    @property
    @cached
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
            code=self.code,
            market=self.market,
        )

    @property
    def stock(self) -> "KisInfoStock":
        """종목 Scope"""
        from pykis.scope.stock.info_stock import KisInfoStock

        return KisInfoStock(
            kis=self.kis,
            info=self.info,
        )

    def quote(self) -> "KisQuote":
        """
        한국투자증권 주식 현재가 조회

        국내주식시세 -> 주식현재가 시세[v1_국내주식-008]
        해외주식현재가 -> 해외주식 현재가상세[v1_해외주식-029]

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 종목 코드가 올바르지 않은 경우
        """
        from pykis.api.stock.quote import quote as _quote

        return _quote(
            self.kis,
            code=self.code,
            market=self.primary_market,
        )
