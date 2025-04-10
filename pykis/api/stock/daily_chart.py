from datetime import date, datetime, timedelta, tzinfo
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Literal, TypeVar

from pykis.api.stock.chart import KisChart, KisChartBar, KisChartBarRepr, KisChartBase
from pykis.api.stock.market import (
    EX_DATE_TYPE_CODE_MAP,
    MARKET_SHORT_TYPE_MAP,
    MARKET_TYPE,
    ExDateType,
    get_market_timezone,
)
from pykis.api.stock.quote import (
    STOCK_SIGN_TYPE,
    STOCK_SIGN_TYPE_KOR_MAP,
    STOCK_SIGN_TYPE_MAP,
)
from pykis.responses.dynamic import KisDynamic, KisList
from pykis.responses.response import KisResponse, raise_not_found
from pykis.responses.types import KisAny, KisDatetime, KisDecimal, KisInt
from pykis.utils.math import safe_divide
from pykis.utils.timezone import TIMEZONE

if TYPE_CHECKING:
    from pykis.api.base.product import KisProductProtocol
    from pykis.kis import PyKis

__all__ = [
    "daily_chart",
]


class KisDomesticDailyChartBar(KisChartBarRepr, KisDynamic):
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
    volume: int = KisInt["acml_vol"]
    """거래량"""
    amount: Decimal = KisDecimal["acml_tr_pbmn"]
    """거래대금"""

    change: Decimal = KisDecimal["prdy_vrss"]
    """전일대비"""
    sign: STOCK_SIGN_TYPE = KisAny(STOCK_SIGN_TYPE_MAP.__getitem__)["prdy_vrss_sign"]
    """전일대비 부호"""

    ex_date_type: ExDateType = KisAny(lambda x: EX_DATE_TYPE_CODE_MAP.get(x, ExDateType.NONE))["flng_cls_code"]
    """락 구분"""
    split_ratio: Decimal = KisDecimal["prtt_rate"]
    """분할 비율"""

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
        return safe_divide(self.change, self.prev_price) * 100

    @property
    def sign_name(self) -> str:
        """대비부호명"""
        return STOCK_SIGN_TYPE_KOR_MAP[self.sign]


class KisDomesticDailyChart(KisResponse, KisChartBase):
    """한국투자증권 국내 기간 차트"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE = "KRX"
    """상품유형타입"""

    timezone: tzinfo = TIMEZONE
    """시간대"""
    bars: list[KisChartBar] = KisList(KisDomesticDailyChartBar)["output2"]
    """차트"""

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    def __pre_init__(self, data: dict[str, Any]) -> None:
        super().__pre_init__(data)

        if data["output1"]["stck_prpr"] == "0":
            raise_not_found(
                data,
                "해당 종목의 차트를 조회할 수 없습니다.",
                code=self.symbol,
                market=self.market,
            )

        data["output2"] = [x for x in data["output2"] if x]


class KisForeignDailyChartBar(KisChartBarRepr, KisDynamic):
    """한국투자증권 해외 기간 차트 봉"""

    time: datetime = KisDatetime("%Y%m%d")["xymd"]  # KisForeignDailyChart의 __post_init__에서 timezone 설정
    """시간 (현지시간)"""
    time_kst: datetime  # KisForeignDailyChart의 __post_init__에서 값 지정
    """시간 (한국시간)"""

    open: Decimal = KisDecimal["open"]
    """시가"""
    close: Decimal = KisDecimal["clos"]
    """종가 (현재가)"""
    high: Decimal = KisDecimal["high"]
    """고가"""
    low: Decimal = KisDecimal["low"]
    """저가"""
    volume: int = KisInt["tvol"]
    """거래량"""
    amount: Decimal = KisDecimal["tamt"]
    """거래대금"""

    change: Decimal = KisDecimal["diff"]
    """전일대비"""
    sign: STOCK_SIGN_TYPE = KisAny(STOCK_SIGN_TYPE_MAP.__getitem__)["sign"]
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
        return safe_divide(self.change, self.prev_price) * 100

    @property
    def sign_name(self) -> str:
        """대비부호명"""
        return STOCK_SIGN_TYPE_KOR_MAP[self.sign]


class KisForeignDailyChart(KisResponse, KisChartBase):
    """한국투자증권 해외 당일 차트"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    timezone: tzinfo
    """시간대"""
    bars: list[KisChartBar] = KisList(KisForeignDailyChartBar)["output2"]
    """차트"""

    def __init__(self, symbol: str, market: MARKET_TYPE) -> None:
        self.symbol = symbol
        self.market = market

    def __pre_init__(self, data: dict[str, Any]) -> None:
        super().__pre_init__(data)

        record_size = data["output1"]["nrec"]

        if not record_size:
            raise_not_found(
                data,
                "해당 종목의 차트를 조회할 수 없습니다.",
                code=self.symbol,
                market=self.market,
            )

        self.timezone = get_market_timezone(self.market)

        data["output2"] = data["output2"][: int(record_size)]

    def __post_init__(self) -> None:
        for bar in self.bars:
            bar.time.replace(tzinfo=self.timezone)
            bar.time_kst = bar.time.astimezone(TIMEZONE)  # type: ignore


TChartBase = TypeVar("TChartBase", bound=KisChartBase)


def drop_after(
    chart: TChartBase,
    start: date | timedelta | None = None,
    end: date | None = None,
) -> TChartBase:
    if isinstance(start, timedelta):
        start = (chart.bars[0].time - start).date()

    bars: list[KisChartBar] = []

    for bar in chart.bars:
        if start and bar.time.date() < start:
            break

        if end and bar.time.date() > end:
            continue

        bars.insert(0, bar)

    chart.bars = bars

    return chart


def domestic_daily_chart(
    self: "PyKis",
    symbol: str,
    start: date | timedelta | None = None,
    end: date | None = None,
    period: Literal["day", "week", "month", "year"] = "day",
    adjust: bool = False,
) -> KisDomesticDailyChart:
    """
    한국투자증권 국내 기간 차트 조회

    국내주식시세 -> 국내주식기간별시세(일/주/월/년)[v1_국내주식-016]
    (업데이트 날짜: 2023-10-02)

    Args:
        symbol (str): 종목 코드
        start (date, optional): 조회 시작 시간. timedelta인 경우 최근 timedelta만큼의 봉을 조회합니다. Defaults to None.
        end (date, optional): 조회 종료 시간. Defaults to None.
        period (Literal["day", "week", "month", "year"], optional): 조회 기간. Defaults to "day".
        adjust (bool, optional): 수정 주가 여부. Defaults to False.

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 조회 파라미터가 올바르지 않은 경우
    """
    if not symbol:
        raise ValueError("종목 코드를 입력해주세요.")

    if not end:
        end = datetime.now(TIMEZONE).date()

    if isinstance(start, datetime):
        start = start.date()

    if isinstance(end, datetime):
        end = end.date()

    if isinstance(start, date) and end and start > end:
        start, end = end, start

    cursor = end
    chart = None
    period_delta = timedelta(days=1 if period == "day" else 7 if period == "week" else 30 if period == "month" else 365)

    while True:
        result = self.fetch(
            "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice",
            api="FHKST03010100",
            params={
                "FID_COND_MRKT_DIV_CODE": "J",
                "FID_INPUT_ISCD": symbol,
                "FID_INPUT_DATE_1": start.strftime("%Y%m%d") if isinstance(start, date) else "00000101",
                "FID_INPUT_DATE_2": cursor.strftime("%Y%m%d"),
                "FID_PERIOD_DIV_CODE": (
                    "D" if period == "day" else "W" if period == "week" else "M" if period == "month" else "Y"
                ),
                "FID_ORG_ADJ_PRC": "0" if adjust else "1",
            },
            response_type=KisDomesticDailyChart(symbol=symbol),
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

        if isinstance(start, timedelta):
            start = (chart.bars[0].time - start).date()

        if start and last <= start:
            break

        cursor = last - period_delta

    return drop_after(
        chart,
        start=start,
        end=end,
    )


def foreign_daily_chart(
    self: "PyKis",
    symbol: str,
    market: MARKET_TYPE,
    start: date | timedelta | None = None,
    end: date | None = None,
    period: Literal["day", "week", "month", "year"] = "day",
    adjust: bool = False,
) -> KisForeignDailyChart:
    """
    한국투자증권 해외 기간 차트 조회

    해외주식현재가 -> 해외주식 기간별시세[v1_해외주식-010]
    (업데이트 날짜: 2023-10-03)

    Args:
        symbol (str): 종목 코드
        market (MARKET_TYPE): 시장 구분
        start (date, optional): 조회 시작 시간. timedelta인 경우 최근 timedelta만큼의 봉을 조회합니다. Defaults to None.
        end (date, optional): 조회 종료 시간. Defaults to None.
        period (Literal["day", "week", "month", "year"], optional): 조회 기간. Defaults to "day".
        adjust (bool, optional): 수정 주가 여부. Defaults to False.

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 조회 파라미터가 올바르지 않은 경우
    """
    if not symbol:
        raise ValueError("종목 코드를 입력해주세요.")

    if isinstance(start, datetime):
        start = start.date()

    if isinstance(end, datetime):
        end = end.date()

    if isinstance(start, date) and end and start > end:
        start, end = end, start

    cursor = end
    chart = None
    period_delta = timedelta(days=1 if period == "day" else 7 if period == "week" else 30)

    while True:
        result = self.fetch(
            "/uapi/overseas-price/v1/quotations/dailyprice",
            api="HHDFS76240000",
            params={
                "AUTH": "",
                "EXCD": MARKET_SHORT_TYPE_MAP[market],
                "SYMB": symbol,
                "GUBN": "0" if period == "day" else "1" if period == "week" else "2",
                "BYMD": cursor.strftime("%Y%m%d") if cursor else "",
                "MODP": "1" if adjust else "0",
            },
            response_type=KisForeignDailyChart(
                symbol=symbol,
                market=market,
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

        if isinstance(start, timedelta):
            start = (chart.bars[0].time - start).date()

        if start and last <= start:
            break

        cursor = last - period_delta

    if period == "year":
        bars = []
        best_bar = None
        best_diff = 0
        target_time = None

        for bar in chart.bars:
            if not target_time or not best_bar:
                target_time = bar.time
                best_bar = bar
                best_diff = 0
                continue

            if bar.time.year != best_bar.time.year:
                bars.append(best_bar)
                target_time -= period_delta
                best_diff = float("inf")

            diff = abs((bar.time - target_time).days)

            if diff < best_diff:
                best_bar = bar
                best_diff = diff

        if best_bar != bars[-1]:
            bars.append(best_bar)

        chart.bars = bars

    return drop_after(
        chart,
        start=start,
        end=end,
    )


def daily_chart(
    self: "PyKis",
    symbol: str,
    market: MARKET_TYPE,
    start: date | timedelta | None = None,
    end: date | None = None,
    period: Literal["day", "week", "month", "year"] = "day",
    adjust: bool = False,
) -> KisChart:
    """
    한국투자증권 기간 차트 조회

    국내주식시세 -> 국내주식기간별시세(일/주/월/년)[v1_국내주식-016]
    해외주식현재가 -> 해외주식 기간별시세[v1_해외주식-010]

    Args:
        symbol (str): 종목 코드
        market (MARKET_TYPE): 시장 구분
        start (date, optional): 조회 시작 시간. timedelta인 경우 최근 timedelta만큼의 봉을 조회합니다. Defaults to None.
        end (date, optional): 조회 종료 시간. Defaults to None.
        period (Literal["day", "week", "month", "year"], optional): 조회 기간. Defaults to "day".
        adjust (bool, optional): 수정 주가 여부. Defaults to False.

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 조회 파라미터가 올바르지 않은 경우
    """
    if market == "KRX":
        return domestic_daily_chart(
            self,
            symbol,
            start=start,
            end=end,
            period=period,
            adjust=adjust,
        )
    else:
        return foreign_daily_chart(
            self,
            symbol,
            market,
            start=start,
            end=end,
            period=period,
            adjust=adjust,
        )


def product_daily_chart(
    self: "KisProductProtocol",
    start: date | timedelta | None = None,
    end: date | None = None,
    period: Literal["day", "week", "month", "year"] = "day",
    adjust: bool = False,
) -> KisChart:
    """
    한국투자증권 기간 차트 조회

    국내주식시세 -> 국내주식기간별시세(일/주/월/년)[v1_국내주식-016]
    해외주식현재가 -> 해외주식 기간별시세[v1_해외주식-010]

    Args:
        start (date, optional): 조회 시작 시간. timedelta인 경우 최근 timedelta만큼의 봉을 조회합니다. Defaults to None.
        end (date, optional): 조회 종료 시간. Defaults to None.
        period (Literal["day", "week", "month", "year"], optional): 조회 기간. Defaults to "day".
        adjust (bool, optional): 수정 주가 여부. Defaults to False.

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 조회 파라미터가 올바르지 않은 경우
    """
    return daily_chart(
        self.kis,
        self.symbol,
        self.market,
        start=start,
        end=end,
        period=period,
        adjust=adjust,
    )
