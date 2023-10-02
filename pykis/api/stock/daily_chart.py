from datetime import date, datetime, timedelta, tzinfo
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Literal

from pykis.__env__ import TIMEZONE
from pykis.api.stock.chart import KisChart, KisChartBar, TChart
from pykis.api.stock.market import EX_DATE_TYPE_CODE_MAP, MARKET_TYPE, ExDateType
from pykis.responses.dynamic import KisList
from pykis.responses.response import KisResponse, raise_not_found
from pykis.responses.types import KisAny, KisDatetime, KisDecimal

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisDomesticDailyChartBar(KisChartBar):
    """한국투자증권 국내 기간 차트 봉"""

    time: datetime = KisDatetime("%Y%m%d", timezone=TIMEZONE)["stck_bsop_date"]
    """시간 (현지시간)"""
    time_kst: datetime = KisDatetime("%Y%m%d", timezone=TIMEZONE)["stck_bsop_date"]
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


class KisDomesticDailyChart(KisResponse, KisChart):
    """한국투자증권 국내 기간 차트"""

    bars: list[KisDomesticDailyChartBar] = KisList(KisDomesticDailyChartBar)["output2"]
    """차트"""
    timezone: tzinfo = TIMEZONE
    """시간대"""

    def __init__(self, code: str, market: MARKET_TYPE):
        self.code = code
        self.market = market

    def __pre_init__(self, data: dict[str, Any]):
        super().__pre_init__(data)

        if data["output1"]["stck_prpr"] == "0":
            raise_not_found(
                data,
                "해당 종목의 차트를 조회할 수 없습니다.",
                code=self.code,
                market=self.market,
            )

        data["output2"] = [x for x in data["output2"] if x]


def drop_after(
    chart: TChart,
    start: date | None = None,
    end: date | None = None,
) -> TChart:
    bars = []

    for i, bar in enumerate(chart.bars):
        if start and bar.time.date() < start:
            break

        if end and bar.time.date() > end:
            continue

        bar.time.replace(tzinfo=chart.timezone)
        bars.insert(0, bar)

    chart.bars = bars

    return chart


DOMESTIC_MAX_RECORDS = 100


def domestic_daily_chart(
    self: "PyKis",
    code: str,
    start: date | None = None,
    end: date | None = None,
    period: Literal["day", "week", "month", "year"] = "day",
    adjust: bool = False,
):
    """
    한국투자증권 국내 기간 차트 조회

    국내주식시세 -> 국내주식기간별시세(일/주/월/년)[v1_국내주식-016]
    (업데이트 날짜: 2023-10-02)

    Args:
        code (str): 종목 코드
        start (date, optional): 조회 시작 시간. Defaults to None.
        end (date, optional): 조회 종료 시간. Defaults to None.
        period (Literal["day", "week", "month", "year"], optional): 조회 기간. Defaults to "day".
        adjust (bool, optional): 수정 주가 여부. Defaults to False.

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 조회 파라미터가 올바르지 않은 경우
    """
    if not code:
        raise ValueError("종목 코드를 입력해주세요.")

    if start and end and start > end:
        raise ValueError("시작 시간은 종료 시간보다 이전이어야 합니다.")

    if not end:
        end = datetime.now(TIMEZONE).date()

    cursor = end
    chart = None
    period_delta = timedelta(
        days=1 if period == "day" else 7 if period == "week" else 30 if period == "month" else 365
    )

    while True:
        result = self.fetch(
            "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice",
            api="FHKST03010100",
            params={
                "FID_COND_MRKT_DIV_CODE": "J",
                "FID_INPUT_ISCD": code,
                "FID_INPUT_DATE_1": start.strftime("%Y%m%d") if start else "00000101",
                "FID_INPUT_DATE_2": cursor.strftime("%Y%m%d"),
                "FID_PERIOD_DIV_CODE": "D"
                if period == "day"
                else "W"
                if period == "week"
                else "M"
                if period == "month"
                else "Y",
                "FID_ORG_ADJ_PRC": "0" if adjust else "1",
            },
            response_type=KisDomesticDailyChart(
                code=code,
                market="KRX",
            ),
            domain="real",
        )

        if not chart:
            chart = result

        if not result.bars:
            break

        last = result.bars[-1].time.date()

        if cursor and cursor < last:
            break

        if chart and result != chart:
            chart.bars.extend(result.bars)

        if start and last <= start:
            break

        cursor = last - period_delta

    return drop_after(
        chart,
        start=start,
        end=end,
    )
