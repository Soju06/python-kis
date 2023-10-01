from pykis.api.stock.market import MARKET_TYPE, MARKET_TYPE_KOR_MAP
from pykis.client.object import KisObjectBase
from pykis.utils.cache import cached


class KisProductBase(KisObjectBase):
    """한국투자증권 상품 기본정보"""

    code: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    @property
    def market_name(self) -> str:
        """시장 종류"""
        return MARKET_TYPE_KOR_MAP[self.market]

    @property
    @cached
    def info(self):
        """종목정보 조회"""
        from pykis.api.stock.info import info as _info

        return _info(
            self.kis,
            code=self.code,
            market=self.market,
        )

    @property
    def stock(self):
        """종목 Scope"""
        from pykis.scope.stock.info_stock import KisInfoStock

        return KisInfoStock(
            kis=self.kis,
            info=self.info,
        )
