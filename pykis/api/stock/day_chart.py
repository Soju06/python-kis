import math
from datetime import datetime, time, timedelta, tzinfo
from typing import TYPE_CHECKING, Any

from pykis.__env__ import TIMEZONE
from pykis.api.stock.chart import KisChart, KisChartBar
from pykis.api.stock.market import MARKET_TYPE, MARKET_TYPE_SHORT_MAP, KisTradingHours
from pykis.client.exception import KisAPIError
from pykis.responses.dynamic import KisList, KisObject, KisTransform
from pykis.responses.response import KisResponse
from pykis.responses.types import KisFloat, KisTime

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisDomesticDayChartBar(KisChartBar):
    """한국투자증권 국내 당일 차트 봉"""

    time: datetime = KisTransform[
        lambda x: datetime.strptime(
            x["stck_bsop_date"] + x["stck_cntg_hour"],
            "%Y%m%d%H%M%S",
        ).replace(tzinfo=TIMEZONE)
    ]
    """시간"""
    time_kst: datetime = KisTransform[
        lambda x: datetime.strptime(
            x["stck_bsop_date"] + x["stck_cntg_hour"],
            "%Y%m%d%H%M%S",
        ).replace(tzinfo=TIMEZONE)
    ]
    """시간 (한국시간)"""
    open: float = KisFloat["stck_oprc"]
    """시가"""
    close: float = KisFloat["stck_prpr"]
    """종가 (현재가)"""
    high: float = KisFloat["stck_hgpr"]
    """고가"""
    low: float = KisFloat["stck_lwpr"]
    """저가"""
    volume: float = KisFloat["cntg_vol"]
    """거래량"""
    amount: float = KisFloat["acml_tr_pbmn"]
    """거래대금"""


class KisDomesticDayChart(KisResponse, KisChart):
    """한국투자증권 국내 당일 차트"""

    bars: list[KisDomesticDayChartBar] = KisList(KisDomesticDayChartBar)["output2"]
    """차트"""
    timezone: tzinfo = TIMEZONE
    """시간대"""

    def __init__(self, code: str, market: MARKET_TYPE):
        self.code = code
        self.market = market


class KisOverseasDayChartBar(KisChartBar):
    """한국투자증권 해외 당일 차트 봉"""

    time: datetime = KisTransform[
        lambda x: datetime.strptime(
            x["xymd"] + x["xhms"],
            "%Y%m%d%H%M%S",
        )
    ]
    """시간 (현지시간)"""
    time_kst: datetime = KisTransform[
        lambda x: datetime.strptime(
            x["kymd"] + x["khms"],
            "%Y%m%d%H%M%S",
        ).replace(tzinfo=TIMEZONE)
    ]
    """시간 (한국시간)"""
    open: float = KisFloat["open"]
    """시가"""
    close: float = KisFloat["last"]
    """종가 (현재가)"""
    high: float = KisFloat["high"]
    """고가"""
    low: float = KisFloat["low"]
    """저가"""
    volume: float = KisFloat["evol"]
    """거래량"""
    amount: float = KisFloat["eamt"]
    """거래대금"""


class KisOverseasTradingHours(KisTradingHours):
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


class KisOverseasDayChart(KisResponse, KisChart):
    """한국투자증권 해외 당일 차트"""

    trading_hours: KisOverseasTradingHours
    """장 운영 시간"""

    bars: list[KisOverseasDayChartBar] = KisList(KisOverseasDayChartBar)["output2"]
    """차트"""

    def __init__(self, code: str, market: MARKET_TYPE):
        self.code = code
        self.market = market
        self.market_time = KisOverseasTradingHours(self.market)

    def __pre_init__(self, data: dict[str, Any]):
        super().__pre_init__(data)

        if not data["output1"]["stim"]:
            raise KisAPIError(
                data={
                    "rt_cd": "7",
                    "msg_cd": "KIER2620",
                    "msg1": "조회할 자료가 없습니다. (이 예외는 한국투자증권 API 오류가 아닌 PyKis에서 처리한 오류입니다.)",
                },
                response=data["__response__"],
            )

        self.timezone = KisObject.transform_(
            data["output1"],
            self.market_time,
            ignore_missing=True,
            pre_init=False,
        ).timezone


def drop_after(
    chart: KisChart,
    start: time | None = None,
    end: time | None = None,
    step: int | None = None,
):
    bars = []

    for i, bar in enumerate(chart.bars):
        if start and bar.time.time() < start:
            break

        if end and bar.time.time() > end:
            continue

        if step and i % step != 0:
            continue

        bar.time.replace(tzinfo=chart.timezone)
        bars.insert(0, bar)

    chart.bars = bars

    return chart


def domestic_day_chart(
    self: "PyKis",
    code: str,
    start: time | None = None,
    end: time | None = None,
    step: int = 1,
):
    """
    한국투자증권 국내 당일 봉 차트 조회

    국내주식시세 -> 주식당일분봉조회[v1_국내주식-022]
    (업데이트 날짜: 2023/09/05)

    Args:
        code (str): 종목코드
        start (time, optional): 조회 시작 시간. Defaults to None.
        end (time, optional): 조회 종료 시간. Defaults to None.
        step (int, optional): 조회 간격 (분). Defaults to 1.
    """
    if not code:
        raise ValueError("종목 코드를 입력해주세요.")

    if step < 1:
        raise ValueError("간격은 1분 이상이어야 합니다.")

    if start and end and start > end:
        raise ValueError("시작 시간은 종료 시간보다 이전이어야 합니다.")

    cursor = end
    chart = None

    while True:
        result = KisDomesticDayChart(
            code=code,
            market="KRX",
        )
        result = self.fetch(
            "/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice",
            api="FHKST03010200",
            params={
                "FID_ETC_CLS_CODE": "",
                "FID_COND_MRKT_DIV_CODE": "J",
                "FID_INPUT_ISCD": code,
                "FID_INPUT_HOUR_1": time.strftime(cursor or time(0, 0, 0), "%H%M%S"),
                "FID_PW_DATA_INCU_YN": "N",
            },
            response_type=result,
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

        if start and cursor and cursor <= start:
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
        step=step,
    )


OVERSEAS_MAX_RECORDS = 120
OVERSEAS_MAX_STEPS = math.ceil(24 * 60 / OVERSEAS_MAX_RECORDS)


records = 120
indices = set()

for i in range(math.ceil(24 * 60 / records)):
    for j in range(records):
        indices.add((i + 1) * (j + 1))


def overseas_day_chart(
    self: "PyKis",
    code: str,
    market: MARKET_TYPE,
    start: time | None = None,
    end: time | None = None,
    step: int = 1,
    once: bool = False,
):
    """
    한국투자증권 해외 당일 봉 차트 조회

    해당 조회 시스템은 한국투자증권 API의 한계로 인해 (24 * 60 / 최대 레코드 수)번 호출하여 원하는 영역의 근접 값을 채워넣습니다.
    따라서, 누락된 봉이 존재할 수 있으며, n = (최대 레코드 수), I = {x | x = (i + 1) * (j + 1), 0 <= ceil(24 * 60 / n), 0 <= j < n}의 해상도를 가집니다.

    해외주식현재가 -> 해외주식분봉조회[v1_해외주식-030]
    (업데이트 날짜: 2023/09/05)

    Args:
        code (str): 종목코드
        market (MARKET_TYPE): 시장 종류
        start (time, optional): 조회 시작 시간. Defaults to None.
        end (time, optional): 조회 종료 시간. Defaults to None.
        step (int, optional): 조회 간격 (분). Defaults to 1.
        once (bool, optional): 한 번만 조회할지 여부. Defaults to False.
    """
    if not code:
        raise ValueError("종목 코드를 입력해주세요.")

    if step < 1:
        raise ValueError("간격은 1분 이상이어야 합니다.")

    if market == "KRX":
        raise ValueError("국내 시장은 domestic_chart()를 사용해주세요.")

    cursor = None
    chart = None
    bars = {}

    for i in range(OVERSEAS_MAX_STEPS):
        result = KisOverseasDayChart(
            code=code,
            market=market,
        )
        result = self.fetch(
            "/uapi/overseas-price/v1/quotations/inquire-time-itemchartprice",
            api="HHDFS76950200",
            params={
                "AUTH": "",
                "EXCD": MARKET_TYPE_SHORT_MAP[market],
                "SYMB": code,
                "NMIN": str(i + 1),
                "PINC": "1",
                "NEXT": "",
                "NREC": str(OVERSEAS_MAX_RECORDS),
                "FILL": "",
                "KEYB": "",
            },
            response_type=result,
            domain="real",
        )

        if not chart:
            chart = result

        if not result.bars:
            break

        last = result.bars[-1].time.time()

        # if cursor and cursor <= last:
        #     break

        for bar in result.bars:
            if bar.time.time() not in bars:
                bars[bar.time.time()] = bar

        if start and cursor and cursor <= start:
            break

        cursor = last

        if once:
            break

    bars = list(bars.values())
    bars.sort(key=lambda x: x.time, reverse=True)  # type: ignore
    chart.bars = bars  # type: ignore

    return drop_after(
        chart,  # type: ignore
        start=start,
        end=end,
        step=step,
    )


def day_chart(
    self: "PyKis",
    code: str,
    market: MARKET_TYPE,
    start: time | None = None,
    end: time | None = None,
    step: int = 1,
) -> KisChart:
    """
    한국투자증권 당일 봉 차트 조회

    해외 당일 봉 차트 조회는 한국투자증권 API의 한계로 인해 (24 * 60 / 최대 레코드 수)번 호출하여 원하는 영역의 근접 값을 채워넣습니다.
    따라서, 누락된 봉이 존재할 수 있으며, n = (최대 레코드 수), I = {x | x = (i + 1) * (j + 1), 0 <= ceil(24 * 60 / n), 0 <= j < n}의 해상도를 가집니다.

    국내주식시세 -> 주식당일분봉조회[v1_국내주식-022]
    해외주식현재가 -> 해외주식분봉조회[v1_해외주식-030]

    Args:
        code (str): 종목코드
        market (MARKET_TYPE): 시장 종류
        start (time, optional): 조회 시작 시간. Defaults to None.
        end (time, optional): 조회 종료 시간. Defaults to None.
        step (int, optional): 조회 간격 (분). Defaults to 1.
    """
    if market == "KRX":
        return domestic_day_chart(
            self,
            code,
            start=start,
            end=end,
            step=step,
        )
    else:
        return overseas_day_chart(
            self,
            code,
            market,
            start=start,
            end=end,
            step=step,
        )
