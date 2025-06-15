from datetime import date, datetime, time, timedelta, tzinfo
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from pykis.api.base.exchange import KisExchangeBase, KisExchangeProtocol
from pykis.api.stock.exchange import (
    EXCHANGE_TYPE,
    get_exchange_name,
    get_exchange_timezone,
)
from pykis.api.stock.info import COUNTRY_TYPE
from pykis.responses.exceptions import KisNotFoundError
from pykis.utils.repr import kis_repr
from pykis.utils.timezone import TIMEZONE

if TYPE_CHECKING:
    from pykis import PyKis

__all__ = [
    "KisTradingHours",
    "KisSimpleTradingHours",
    "trading_hours",
]


@runtime_checkable
class KisTradingHours(KisExchangeProtocol, Protocol):
    """한국투자증권 장 운영 시간"""

    @property
    def exchange(self) -> EXCHANGE_TYPE:
        """시장 종류"""
        ...

    @property
    def open(self) -> time:
        """장 시작 시간"""
        ...

    @property
    def open_kst(self) -> time:
        """장 시작 시간 (한국시간)"""
        ...

    @property
    def close(self) -> time:
        """장 종료 시간"""
        ...

    @property
    def close_kst(self) -> time:
        """장 종료 시간 (한국시간)"""
        ...

    @property
    def timezone(self) -> tzinfo:
        """시간대"""
        ...

    @property
    def exchange_name(self) -> str:
        """시장 종류"""
        ...


@kis_repr(
    "exchange",
    "open",
    "open_kst",
    "close",
    "close_kst",
    lines="multiple",
)
class KisTradingHoursRepr:
    """한국투자증권 장 운영 시간"""


class KisTradingHoursBase(KisTradingHoursRepr, KisExchangeBase):
    """한국투자증권 장 운영 시간"""

    exchange: EXCHANGE_TYPE
    """시장 종류"""
    open: time
    """장 시작 시간"""
    open_kst: time
    """장 시작 시간 (한국시간)"""
    close: time
    """장 종료 시간"""
    close_kst: time
    """장 종료 시간 (한국시간)"""

    @property
    def timezone(self) -> tzinfo:
        """시간대"""
        return get_exchange_timezone(self.exchange)

    @property
    def exchange_name(self) -> str:
        """시장 종류"""
        return get_exchange_name(self.exchange)


class KisSimpleTradingHours(KisTradingHoursBase):
    """한국투자증권 장 운영 시간"""

    exchange: EXCHANGE_TYPE
    """시장 종류"""
    open: time
    """장 시작 시간"""
    open_kst: time
    """장 시작 시간 (한국시간)"""
    close: time
    """장 종료 시간"""
    close_kst: time
    """장 종료 시간 (한국시간)"""

    def __init__(self, exchange: EXCHANGE_TYPE, open: time, close: time):
        self.exchange = exchange
        self.open = open
        self.close = close

        day = date(2000, 1, 1)

        self.open_kst = datetime.combine(day, open, tzinfo=self.timezone).astimezone(TIMEZONE).time()
        self.close_kst = datetime.combine(day, close, tzinfo=self.timezone).astimezone(TIMEZONE).time()


EXCHANGE_SAMPLE_STOCK_MAP: dict[EXCHANGE_TYPE, list[str] | EXCHANGE_TYPE] = {
    # 2024/07/29 기준 시총 상위 3개 종목
    "KRX": ["005930", "000660", "373220"],  # 삼성전자, SK하이닉스, LG에너지솔루션
    "NASDAQ": ["MSFT", "AAPL", "NVDA"],  # 마이크로소프트, 애플, 엔비디아
    "NYSE": ["TSM", "BRK-A", "LLY"],  # TSMC, 버크셔해서웨이, 일라이릴리
    "AMEX": ["IMO", "SIM", "BTG"],  # 임페리얼오일, 그루포시멕, B2골드
    "TYO": ["7203", "8306", "6758"],  # 도요타, 미쓰비시, 소니
    "HKEX": ["00700", "00941", "00939"],  # 텐센트, 차이나모바일, 건설은행
    "HNX": "HSX",
    "HSX": ["VCB", "BID", "FPT"],  # 베트남무역은행, 베트남개발은행, FPT
    "SSE": ["600519", "601398", "601288"],  # 귀주모태주, 공상은행, 농업은행
    "SZSE": "SSE",
}


def trading_hours(
    self: "PyKis",
    exchange: EXCHANGE_TYPE | COUNTRY_TYPE,
    use_cache: bool = True,
) -> KisTradingHours:
    """
    한국투자증권 장운영 시간 조회

    해외 당일 봉 차트 조회의 파생 API입니다.

    해외주식현재가 -> 해외주식분봉조회[v1_해외주식-030]
    (업데이트 날짜: 2024/07/29)

    Args:
        exchange (EXCHANGE_TYPE): 시장 종류
        use_cache (bool, optional): 캐시 사용 여부. Defaults to True.

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 조회 파라미터가 올바르지 않은 경우
    """
    match exchange:
        case "KR":
            exchange = "KRX"
        case "US":
            exchange = "NASDAQ"
        case "JP":
            exchange = "TYO"
        case "HK":
            exchange = "HKEX"
        case "VN":
            exchange = "HSX"
        case "CN":
            exchange = "SSE"

    if use_cache:
        cached = self.cache.get(f"trading_hours:{exchange}", KisSimpleTradingHours)

        if cached:
            return cached

    if exchange == "KRX":
        result = KisSimpleTradingHours(
            exchange="KRX",
            open=time(9, 0, tzinfo=TIMEZONE),
            close=time(15, 30, tzinfo=TIMEZONE),
        )
    else:
        from pykis.api.stock.day_chart import foreign_day_chart

        while isinstance(samples := EXCHANGE_SAMPLE_STOCK_MAP[exchange], str):
            exchange = samples

        result = None

        for symbol in samples:
            try:
                chart = foreign_day_chart(
                    self,
                    exchange=exchange,
                    symbol=symbol,
                    once=True,
                )

                result = chart.trading_hours
                break
            except KisNotFoundError:
                pass

        if not result:
            raise ValueError("해외 주식 시장 정보를 찾을 수 없습니다.")

    if use_cache:
        self.cache.set(f"trading_hours:{exchange}", result, expire=timedelta(days=1))

    return result
