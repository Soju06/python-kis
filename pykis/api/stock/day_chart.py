import math
from datetime import datetime, time, timedelta, tzinfo
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from pykis.__env__ import TIMEZONE
from pykis.api.stock.chart import KisChart, KisChartBar, TChart
from pykis.api.stock.market import MARKET_SHORT_TYPE_MAP, MARKET_TYPE, KisTradingHours
from pykis.api.stock.quote import STOCK_SIGN_TYPE
from pykis.responses.dynamic import KisDynamic, KisList, KisObject, KisTransform
from pykis.responses.response import KisResponse, raise_not_found
from pykis.responses.types import KisDecimal, KisInt, KisTime

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisDayChartBar(KisChartBar):
    """한국투자증권 당일 차트 봉"""

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
    volume: int
    """거래량"""
    amount: Decimal
    """거래대금"""

    change: Decimal
    """전일대비"""
    sign: STOCK_SIGN_TYPE
    """전일대비 부호"""


class KisDayChart(KisChart):
    """한국투자증권 당일 차트"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    timezone: tzinfo
    """시간대"""
    bars: list[KisDayChartBar]
    """차트 (오름차순)"""


class KisDomesticDayChartBar(KisDynamic, KisDayChartBar):
    """한국투자증권 국내 당일 차트 봉"""

    time: datetime = KisTransform[
        lambda x: datetime.strptime(
            x["stck_bsop_date"] + x["stck_cntg_hour"],
            "%Y%m%d%H%M%S",
        ).replace(tzinfo=TIMEZONE)
    ]
    """시간"""
    time_kst: datetime  # __post_init__에서 값 설정
    """시간 (한국시간)"""
    open: Decimal = KisDecimal["stck_oprc"]
    """시가"""
    close: Decimal = KisDecimal["stck_prpr"]
    """종가 (현재가)"""
    high: Decimal = KisDecimal["stck_hgpr"]
    """고가"""
    low: Decimal = KisDecimal["stck_lwpr"]
    """저가"""
    volume: int = KisInt["cntg_vol"]
    """거래량"""
    amount: Decimal = KisDecimal["acml_tr_pbmn"]
    """거래대금"""

    change: Decimal  # KisDomesticDayChart의 __post_init__에서 값 설정
    """전일대비"""

    @property
    def sign(self) -> STOCK_SIGN_TYPE:
        """전일대비 부호"""
        return "steady" if self.change == 0 else "rise" if self.change > 0 else "decline"

    def __post_init__(self):
        super().__post_init__()
        self.time_kst = self.time.astimezone(TIMEZONE)


class KisDomesticDayChart(KisResponse, KisDayChart):
    """한국투자증권 국내 당일 차트"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE = "KRX"
    """상품유형타입"""

    timezone: tzinfo = TIMEZONE
    """시간대"""
    bars: list[KisDomesticDayChartBar] = KisList(KisDomesticDayChartBar)("output2", absolute=True)
    """차트"""

    prev_price: Decimal = KisDecimal["stck_prdy_clpr"]
    """전일종가"""

    def __init__(self, symbol: str):
        self.symbol = symbol

    def __pre_init__(self, data: dict[str, Any]):
        super().__pre_init__(data)

        if data["output1"]["stck_prpr"] == "0":
            raise_not_found(
                data,
                "해당 종목의 차트를 조회할 수 없습니다.",
                code=self.symbol,
                market=self.market,
            )

    def __post_init__(self):
        super().__post_init__()

        for bar in self.bars:
            bar.change = bar.close - self.prev_price


class KisOverseasDayChartBar(KisDynamic, KisDayChartBar):
    """한국투자증권 해외 당일 차트 봉"""

    time: datetime = KisTransform[
        lambda x: datetime.strptime(
            x["xymd"] + x["xhms"],
            "%Y%m%d%H%M%S",
        )
    ]  #  KisOverseasDayChart의 __post_init__에서 timezone 설정
    """시간 (현지시간)"""
    time_kst: datetime = KisTransform[
        lambda x: datetime.strptime(
            x["kymd"] + x["khms"],
            "%Y%m%d%H%M%S",
        ).replace(tzinfo=TIMEZONE)
    ]
    """시간 (한국시간)"""
    open: Decimal = KisDecimal["open"]
    """시가"""
    close: Decimal = KisDecimal["last"]
    """종가 (현재가)"""
    high: Decimal = KisDecimal["high"]
    """고가"""
    low: Decimal = KisDecimal["low"]
    """저가"""
    volume: int = KisInt["evol"]
    """거래량"""
    amount: Decimal = KisDecimal["eamt"]
    """거래대금"""


class KisOverseasTradingHours(KisDynamic, KisTradingHours):
    """한국투자증권 해외 장 운영 시간"""

    market: MARKET_TYPE
    """시장 종류"""
    open: time = KisTime["stim"]
    """장 시작 시간"""
    open_kst: time = KisTime["sktm"]
    """장 시작 시간 (한국시간)"""
    close: time = KisTime["etim"]
    """장 종료 시간"""
    close_kst: time = KisTime["ektm"]
    """장 종료 시간 (한국시간)"""

    def __init__(self, market: MARKET_TYPE):
        self.market = market


class KisOverseasDayChart(KisResponse, KisDayChart):
    """한국투자증권 해외 당일 차트"""

    trading_hours: KisOverseasTradingHours
    """장 운영 시간"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    timezone: tzinfo
    """시간대"""
    bars: list[KisOverseasDayChartBar] = KisList(KisOverseasDayChartBar)["output2"]
    """차트 (오름차순)"""

    def __init__(self, symbol: str, market: MARKET_TYPE):
        self.trading_hours = KisOverseasTradingHours(self.market)
        self.symbol = symbol
        self.market = market

    def __pre_init__(self, data: dict[str, Any]):
        super().__pre_init__(data)

        if not data["output1"]["nrec"]:
            raise_not_found(
                data,
                "해당 종목의 차트를 조회할 수 없습니다.",
                code=self.symbol,
                market=self.market,
            )

        self.timezone = KisObject.transform_(
            data["output1"],
            self.trading_hours,
            ignore_missing=True,
            pre_init=False,
        ).timezone

    def __post_init__(self):
        super().__post_init__()

        for bar in self.bars:
            bar.time = bar.time.replace(tzinfo=self.timezone)


def drop_after(
    chart: TChart,
    start: time | timedelta | None = None,
    end: time | None = None,
    period: int | None = None,
) -> TChart:
    if isinstance(start, timedelta):
        start = (chart.bars[0].time - start).time()

    bars = []

    for i, bar in enumerate(chart.bars):
        if start and bar.time.time() < start:
            break

        if end and bar.time.time() > end:
            continue

        if period and i % period != 0:
            continue

        bars.insert(0, bar)

    chart.bars = bars

    return chart


def domestic_day_chart(
    self: "PyKis",
    symbol: str,
    start: time | timedelta | None = None,
    end: time | None = None,
    period: int = 1,
) -> KisDomesticDayChart:
    """
    한국투자증권 국내 당일 봉 차트 조회

    국내주식시세 -> 주식당일분봉조회[v1_국내주식-022]
    (업데이트 날짜: 2023/09/05)

    Args:
        symbol (str): 종목코드
        start (time | timedelta, optional): 조회 시작 시간. timedelta인 경우 최근 timedelta만큼의 봉을 조회합니다. Defaults to None.
        end (time, optional): 조회 종료 시간. Defaults to None.
        period (int, optional): 조회 간격 (분). Defaults to 1.

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 조회 파라미터가 올바르지 않은 경우
    """
    if not symbol:
        raise ValueError("종목 코드를 입력해주세요.")

    if period < 1:
        raise ValueError("간격은 1분 이상이어야 합니다.")

    if isinstance(start, time) and end and start > end:
        raise ValueError("시작 시간은 종료 시간보다 이전이어야 합니다.")

    cursor = end
    chart = None

    while True:
        result = self.fetch(
            "/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice",
            api="FHKST03010200",
            params={
                "FID_ETC_CLS_CODE": "",
                "FID_COND_MRKT_DIV_CODE": "J",
                "FID_INPUT_ISCD": symbol,
                "FID_INPUT_HOUR_1": time.strftime(cursor or time(0, 0, 0), "%H%M%S"),
                "FID_PW_DATA_INCU_YN": "N",
            },
            response_type=KisDomesticDayChart(
                symbol=symbol,
            ),
            domain="real",
        )

        if not chart:
            chart = result

        if not result.bars:
            break

        last = result.bars[-1].time.time()

        if cursor and cursor < last:
            break

        if chart and result != chart:
            chart.bars.extend(result.bars)

        if isinstance(start, timedelta):
            start = (chart.bars[0].time - start).time()

        if start and last <= start:
            break

        cursor = (
            datetime.combine(
                datetime.min,
                last,
            )
            - timedelta(minutes=1)
        ).time()

    return drop_after(
        chart,
        start=start,
        end=end,
        period=period,
    )


OVERSEAS_MAX_RECORDS = 120
OVERSEAS_MAX_PERIODS = math.ceil(24 * 60 / OVERSEAS_MAX_RECORDS)


# records = 120
# indices = set()

# for i in range(math.ceil(24 * 60 / records)):
#     for j in range(records):
#         indices.add((i + 1) * (j + 1))


def overseas_day_chart(
    self: "PyKis",
    symbol: str,
    market: MARKET_TYPE,
    start: time | timedelta | None = None,
    end: time | None = None,
    period: int = 1,
    once: bool = False,
) -> KisOverseasDayChart:
    """
    한국투자증권 해외 당일 봉 차트 조회

    해당 조회 시스템은 한국투자증권 API의 한계로 인해 (24 * 60 / 최대 레코드 수)번 호출하여 원하는 영역의 근접 값을 채워넣습니다.
    따라서, 누락된 봉이 존재할 수 있으며, n = (최대 레코드 수), I = {x | x = (i + 1) * (j + 1), 0 <= ceil(24 * 60 / n), 0 <= j < n}의 해상도를 가집니다.

    해외주식현재가 -> 해외주식분봉조회[v1_해외주식-030]
    (업데이트 날짜: 2023/09/05)

    Args:
        symbol (str): 종목코드
        market (MARKET_TYPE): 시장 종류
        start (time | timedelta, optional): 조회 시작 시간. timedelta인 경우 최근 timedelta만큼의 봉을 조회합니다. Defaults to None.
        end (time, optional): 조회 종료 시간. Defaults to None.
        period (int, optional): 조회 간격 (분). Defaults to 1.
        once (bool, optional): 한 번만 조회할지 여부. Defaults to False.

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 조회 파라미터가 올바르지 않은 경우
    """
    if not symbol:
        raise ValueError("종목 코드를 입력해주세요.")

    if period < 1:
        raise ValueError("간격은 1분 이상이어야 합니다.")

    if market == "KRX":
        raise ValueError("국내 시장은 domestic_chart()를 사용해주세요.")

    chart = None
    bars = {}

    for i in range(OVERSEAS_MAX_PERIODS):
        result = self.fetch(
            "/uapi/overseas-price/v1/quotations/inquire-time-itemchartprice",
            api="HHDFS76950200",
            params={
                "AUTH": "",
                "EXCD": MARKET_SHORT_TYPE_MAP[market],
                "SYMB": symbol,
                "NMIN": str(i + 1),
                "PINC": "1",
                "NEXT": "",
                "NREC": str(OVERSEAS_MAX_RECORDS),
                "FILL": "",
                "KEYB": "",
            },
            response_type=KisOverseasDayChart(
                symbol=symbol,
                market=market,
            ),
            domain="real",
        )

        if not chart:
            chart = result

        if not result.bars:
            break

        last = result.bars[-1].time.time()

        for bar in result.bars:
            if bar.time.time() not in bars:
                bars[bar.time.time()] = bar

        if isinstance(start, timedelta):
            start = (chart.bars[0].time - start).time()

        if start and last <= start:
            break

        if once:
            break

    bars = list(bars.values())
    bars.sort(key=lambda x: x.time, reverse=True)  # type: ignore
    chart.bars = bars  # type: ignore

    return drop_after(
        chart,  # type: ignore
        start=start,
        end=end,
        period=period,
    )


def day_chart(
    self: "PyKis",
    symbol: str,
    market: MARKET_TYPE,
    start: time | timedelta | None = None,
    end: time | None = None,
    period: int = 1,
) -> KisDayChart:
    """
    한국투자증권 당일 봉 차트 조회

    해외 당일 봉 차트 조회는 한국투자증권 API의 한계로 인해 (24 * 60 / 최대 레코드 수)번 호출하여 원하는 영역의 근접 값을 채워넣습니다.
    따라서, 누락된 봉이 존재할 수 있으며, n = (최대 레코드 수), I = {x | x = (i + 1) * (j + 1), 0 <= ceil(24 * 60 / n), 0 <= j < n}의 해상도를 가집니다.

    국내주식시세 -> 주식당일분봉조회[v1_국내주식-022]
    해외주식현재가 -> 해외주식분봉조회[v1_해외주식-030]

    Args:
        symbol (str): 종목코드
        market (MARKET_TYPE): 시장 종류
        start (time | timedelta, optional): 조회 시작 시간. timedelta인 경우 최근 timedelta만큼의 봉을 조회합니다. Defaults to None.
        end (time, optional): 조회 종료 시간. Defaults to None.
        period (int, optional): 조회 간격 (분). Defaults to 1.

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 조회 파라미터가 올바르지 않은 경우
    """
    if market == "KRX":
        return domestic_day_chart(
            self,
            symbol,
            start=start,
            end=end,
            period=period,
        )
    else:
        return overseas_day_chart(
            self,
            symbol,
            market,
            start=start,
            end=end,
            period=period,
        )
