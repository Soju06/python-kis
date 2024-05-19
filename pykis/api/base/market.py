from pykis.api.stock.market import MARKET_TYPE, MARKET_TYPE_KOR_MAP


class KisMarketBase:
    """한국투자증권 시장 베이스"""

    market: MARKET_TYPE
    """상품유형타입"""

    @property
    def market_name(self) -> str:
        """실제 상품유형명"""
        return MARKET_TYPE_KOR_MAP[self.market]

    @property
    def overseas(self) -> bool:
        """해외종목 여부"""
        from pykis.api.stock.info import MARKET_TYPE_MAP

        return self.market not in MARKET_TYPE_MAP["KRX"]

    @property
    def domestic(self) -> bool:
        """국내종목 여부"""
        return not self.overseas
