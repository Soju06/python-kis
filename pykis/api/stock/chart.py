from datetime import datetime, tzinfo
from decimal import Decimal
from pykis.api.stock.base.product import KisProductBase
from pykis.api.stock.market import MARKET_TYPE
from pykis.responses.dynamic import KisDynamic


class KisChartBar(KisDynamic):
    """한국투자증권 차트 봉"""

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


class KisChart(KisDynamic, KisProductBase):
    """한국투자증권 차트"""

    timezone: tzinfo
    """시간대"""
    bars: list[KisChartBar]
    """차트"""
