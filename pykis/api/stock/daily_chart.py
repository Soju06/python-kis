from datetime import datetime, tzinfo
from decimal import Decimal
from typing import TYPE_CHECKING

from pykis.__env__ import TIMEZONE
from pykis.api.stock.chart import KisChart, KisChartBar
from pykis.api.stock.market import EX_DATE_TYPE_CODE_MAP, MARKET_TYPE, ExDateType
from pykis.api.stock.quote import KisQuote
from pykis.responses.dynamic import KisList, KisObject
from pykis.responses.response import KisResponse
from pykis.responses.types import KisAny, KisDatetime, KisDecimal, KisString

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisDomesticDailyChartBar(KisChartBar):
    """한국투자증권 국내 기간 차트 봉"""

    time: datetime = KisDatetime(timezone=TIMEZONE)["stck_bsop_date"]
    """시간 (현지시간)"""
    time_kst: datetime = KisDatetime(timezone=TIMEZONE)["stck_bsop_date"]
    """시간 (한국시간)"""
    open: Decimal = KisDecimal["stck_oprc"]
    """시가"""
    close: Decimal = KisDecimal["stck_clpr"]
    """종가 (현재가)"""
    high: Decimal = KisDecimal["stck_hgpr"]
    """고가"""
    low: Decimal = KisDecimal["stck_lwpr"]
    """저가"""
    volume: Decimal = KisDecimal["acml_vol"]
    """거래량"""
    amount: Decimal = KisDecimal["acml_tr_pbmn"]
    """거래대금"""

    ex_date_type: ExDateType = KisAny(lambda x: EX_DATE_TYPE_CODE_MAP[x])["flng_cls_code"]
    """락 구분"""
    split_ratio: Decimal = KisDecimal["prtt_rate"]
    """분할 비율"""
