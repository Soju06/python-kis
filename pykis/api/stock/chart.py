from datetime import datetime, tzinfo
from decimal import Decimal
from typing import TypeVar
from pykis.api.stock.base.product import KisProductBase
from pykis.api.stock.quote import STOCK_SIGN_TYPE, STOCK_SIGN_TYPE_KOR_MAP
from pykis.responses.dynamic import KisDynamic


class KisChartBar(KisDynamic):
    """한국투자증권 차트 봉"""

    chart: "KisChart"
    """차트"""

    time: datetime
    """시간 (현지시간)"""
    time_kst: datetime
    """시간 (한국시간)"""
    open: Decimal
    """시가"""
    close: Decimal
    """종가 (현재가)"""
    high: Decimal
    """고가"""
    low: Decimal
    """저가"""
    volume: Decimal
    """거래량"""
    amount: Decimal
    """거래대금"""

    change: Decimal
    """전일대비"""
    sign: STOCK_SIGN_TYPE
    """전일대비 부호"""

    @property
    def price(self) -> Decimal:
        """현재가 (종가)"""
        return self.close

    @property
    def prev_price(self) -> Decimal:
        """전일가"""
        return self.close - self.change

    @property
    def rate(self) -> Decimal:
        """등락률 (-100 ~ 100)"""
        return self.change / self.prev_price * 100

    @property
    def sign_name(self) -> str:
        """대비부호명"""
        return STOCK_SIGN_TYPE_KOR_MAP[self.sign]


class KisChart(KisDynamic, KisProductBase):
    """한국투자증권 차트"""

    timezone: tzinfo
    """시간대"""
    bars: list[KisChartBar]
    """차트"""


TChart = TypeVar("TChart", bound=KisChart)
