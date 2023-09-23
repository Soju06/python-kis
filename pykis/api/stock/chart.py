from datetime import datetime, tzinfo
from pykis.api.stock.base.product import KisProductBase
from pykis.api.stock.market import MARKET_TYPE
from pykis.responses.dynamic import KisDynamic


class KisChartBar(KisDynamic):
    """한국투자증권 차트 봉"""

    time: datetime
    """시간 (현지시간)"""
    time_kst: datetime
    """시간 (한국시간)"""
    open: float
    """시가"""
    close: float
    """종가 (현재가)"""
    high: float
    """고가"""
    low: float
    """저가"""
    volume: float
    """거래량"""
    amount: float
    """거래대금"""


class KisChart(KisDynamic, KisProductBase):
    """한국투자증권 차트"""

    timezone: tzinfo
    """시간대"""
    bars: list[KisChartBar]
    """차트"""
