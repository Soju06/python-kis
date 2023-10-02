from pykis.api.stock.market import MARKET_TYPE
from pykis.scope.base.product import KisProductScopeBase


class KisProductBase(KisProductScopeBase):
    """한국투자증권 상품 기본정보"""

    market: MARKET_TYPE
    """상품유형타입"""
