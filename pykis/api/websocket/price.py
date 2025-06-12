from datetime import datetime, tzinfo
from decimal import Decimal
from typing import TYPE_CHECKING, Callable, Protocol, runtime_checkable

from pykis.api.account.order import ORDER_CONDITION
from pykis.api.base.product import KisProductBase, KisProductProtocol
from pykis.api.stock.market import (
    DAYTIME_MARKET_SHORT_TYPE_MAP,
    MARKET_SHORT_TYPE_MAP,
    MARKET_TYPE,
    REVERSE_DAYTIME_MARKET_SHORT_TYPE_MAP,
    REVERSE_MARKET_SHORT_TYPE_MAP,
    get_market_timezone,
)
from pykis.api.stock.quote import (
    STOCK_SIGN_TYPE,
    STOCK_SIGN_TYPE_KOR_MAP,
    STOCK_SIGN_TYPE_MAP,
)
from pykis.event.filters.product import KisProductEventFilter
from pykis.event.handler import KisEventFilter, KisEventTicket, KisMultiEventFilter
from pykis.event.subscription import KisSubscriptionEventArgs
from pykis.responses.types import KisAny, KisDecimal, KisInt, KisString
from pykis.responses.websocket import KisWebsocketResponse, KisWebsocketResponseProtocol
from pykis.utils.math import safe_divide
from pykis.utils.repr import kis_repr
from pykis.utils.timezone import TIMEZONE
from pykis.utils.typing import Checkable

if TYPE_CHECKING:
    from pykis.client.websocket import KisWebsocketClient

__all__ = [
    "KisRealtimePrice",
]


@runtime_checkable
class KisRealtimePrice(KisWebsocketResponseProtocol, KisProductProtocol, Protocol):
    """한국투자증권 실시간 체결가"""

    @property
    def time(self) -> datetime:
        """체결 시간"""
        ...

    @property
    def time_kst(self) -> datetime:
        """체결 시간(KST)"""
        ...

    @property
    def timezone(self) -> tzinfo:
        """시간대"""
        ...

    @property
    def price(self) -> Decimal:
        """현재가"""
        ...

    @property
    def last(self) -> Decimal:
        """현재가"""
        ...

    @property
    def prev_price(self) -> Decimal:
        """전일가"""
        ...

    @property
    def change(self) -> Decimal:
        """전일대비"""
        ...

    @property
    def sign(self) -> STOCK_SIGN_TYPE:
        """대비부호"""
        ...

    @property
    def sign_name(self) -> str:
        """대비부호명"""
        ...

    @property
    def change_rate(self) -> Decimal:
        """전일대비율 (-100~100)"""
        ...

    @property
    def bid(self) -> Decimal:
        """매수호가"""
        ...

    @property
    def ask(self) -> Decimal:
        """매도호가"""
        ...

    @property
    def bid_quantity(self) -> int:
        """매수호가잔량"""
        ...

    @property
    def ask_quantity(self) -> int:
        """매도호가잔량"""
        ...

    @property
    def spread(self) -> Decimal:
        """매수/매도호가대비"""
        ...

    @property
    def spread_rate(self) -> Decimal:
        """매수/매도호가대비율 (-100~100)"""
        ...

    @property
    def bid_qty(self) -> int:
        """매수호가잔량"""
        ...

    @property
    def ask_qty(self) -> int:
        """매도호가잔량"""
        ...

    @property
    def open(self) -> Decimal:
        """당일시가"""
        ...

    @property
    def open_time(self) -> datetime | None:
        """시가시간"""
        ...

    @property
    def open_time_kst(self) -> datetime | None:
        """시가시간(KST)"""
        ...

    @property
    def open_change(self) -> Decimal:
        """시가대비"""
        ...

    @property
    def open_change_rate(self) -> Decimal:
        """시가대비율"""
        ...

    @property
    def high(self) -> Decimal:
        """당일고가"""
        ...

    @property
    def high_time(self) -> datetime | None:
        """고가시간"""
        ...

    @property
    def high_time_kst(self) -> datetime | None:
        """고가시간(KST)"""
        ...

    @property
    def high_change(self) -> Decimal:
        """고가대비"""
        ...

    @property
    def high_change_rate(self) -> Decimal:
        """고가대비율"""
        ...

    @property
    def low(self) -> Decimal:
        """당일저가"""
        ...

    @property
    def low_time(self) -> datetime | None:
        """저가시간"""
        ...

    @property
    def low_time_kst(self) -> datetime | None:
        """저가시간(KST)"""
        ...

    @property
    def low_change(self) -> Decimal:
        """저가대비"""
        ...

    @property
    def low_change_rate(self) -> Decimal:
        """저가대비율"""
        ...

    @property
    def volume(self) -> int:
        """누적거래량"""
        ...

    @property
    def amount(self) -> Decimal:
        """누적거래대금"""
        ...

    @property
    def prev_volume(self) -> int | None:
        """전일동일시간거래량"""
        ...

    @property
    def buy_quantity(self) -> int:
        """매수체결량"""
        ...

    @property
    def sell_quantity(self) -> int:
        """매도체결량"""
        ...

    @property
    def intensity(self) -> float:
        """체결강도 (0 ~ 100+)"""
        ...

    @property
    def buy_qty(self) -> int:
        """매수체결량"""
        ...

    @property
    def sell_qty(self) -> int:
        """매도체결량"""
        ...

    @property
    def volume_rate(self) -> Decimal | None:
        """전일동일시간거래량비율 (-100~100)"""
        ...

    @property
    def condition(self) -> ORDER_CONDITION | None:
        """주문조건"""
        ...

    @property
    def decimal_places(self) -> int:
        """소수점 자리수"""
        ...


@kis_repr(
    "market",
    "symbol",
    "time",
    "price",
    "change",
    "volume",
    "amount",
    lines="single",
)
class KisRealtimePriceRepr:
    """한국투자증권 실시간 체결가"""


class KisRealtimePriceBase(KisRealtimePriceRepr, KisWebsocketResponse, KisProductBase):
    """한국투자증권 실시간 체결가"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    time: datetime
    """체결 시간"""
    time_kst: datetime
    """체결 시간(KST)"""
    timezone: tzinfo
    """시간대"""

    price: Decimal
    """현재가"""

    @property
    def last(self) -> Decimal:
        """현재가"""
        return self.price

    prev_price: Decimal
    """전일가"""
    change: Decimal
    """전일대비"""
    sign: STOCK_SIGN_TYPE
    """대비부호"""

    @property
    def sign_name(self) -> str:
        """대비부호명"""
        return STOCK_SIGN_TYPE_KOR_MAP[self.sign]

    @property
    def change_rate(self) -> Decimal:
        """전일대비율 (-100~100)"""
        return safe_divide(self.change, self.price) * 100

    bid: Decimal
    """매수호가"""
    ask: Decimal
    """매도호가"""
    bid_quantity: int
    """매수호가잔량"""
    ask_quantity: int
    """매도호가잔량"""

    @property
    def spread(self) -> Decimal:
        """매수/매도호가대비"""
        return self.ask - self.bid

    @property
    def spread_rate(self) -> Decimal:
        """매수/매도호가대비율 (-100~100)"""
        return safe_divide(self.spread, self.price) * 100

    @property
    def bid_qty(self) -> int:
        """매수호가잔량"""
        return self.bid_quantity

    @property
    def ask_qty(self) -> int:
        """매도호가잔량"""
        return self.ask_quantity

    open: Decimal
    """당일시가"""
    open_time: datetime | None
    """시가시간"""
    open_time_kst: datetime | None
    """시가시간(KST)"""

    @property
    def open_change(self) -> Decimal:
        """시가대비"""
        return self.open - self.prev_price

    @property
    def open_change_rate(self) -> Decimal:
        """시가대비율"""
        return safe_divide(self.open_change, self.open) * 100

    high: Decimal
    """당일고가"""
    high_time: datetime | None
    """고가시간"""
    high_time_kst: datetime | None
    """고가시간(KST)"""

    @property
    def high_change(self) -> Decimal:
        """고가대비"""
        return self.high - self.prev_price

    @property
    def high_change_rate(self) -> Decimal:
        """고가대비율"""
        return safe_divide(self.high_change, self.high) * 100

    low: Decimal
    """당일저가"""
    low_time: datetime | None
    """저가시간"""
    low_time_kst: datetime | None
    """저가시간(KST)"""

    @property
    def low_change(self) -> Decimal:
        """저가대비"""
        return self.low - self.prev_price

    @property
    def low_change_rate(self) -> Decimal:
        """저가대비율"""
        return safe_divide(self.low_change, self.low) * 100

    volume: int
    """누적거래량"""
    amount: Decimal
    """누적거래대금"""
    prev_volume: int | None
    """전일동일시간거래량"""

    buy_quantity: int
    """매수체결량"""
    sell_quantity: int
    """매도체결량"""

    @property
    def intensity(self) -> float:
        """체결강도 (0 ~ 100+)"""
        return safe_divide(self.buy_quantity, self.sell_quantity) * 100 if self.sell_quantity else 100

    @property
    def buy_qty(self) -> int:
        """매수체결량"""
        return self.buy_quantity

    @property
    def sell_qty(self) -> int:
        """매도체결량"""
        return self.sell_quantity

    @property
    def volume_rate(self) -> Decimal | None:
        """전일동일시간거래량비율 (-100~100)"""
        return Decimal(safe_divide(self.volume, self.prev_volume) * 100) if self.prev_volume else None

    condition: ORDER_CONDITION | None
    """주문조건"""

    decimal_places: int
    """소수점 자리수"""


DOMESTIC_REALTIME_PRICE_ORDER_CONDITION_MAP: dict[str, ORDER_CONDITION | None] = {
    "1": "before",
    "2": None,
    "3": "after",
    "4": "extended",
}


class KisDomesticRealtimePrice(KisRealtimePriceBase):
    """국내주식 실시간 체결가"""

    __fields__ = [
        KisString["symbol"],  # 0 MKSC_SHRN_ISCD 유가증권 단축 종목코드
        None,  # 1 STCK_CNTG_HOUR 주식 체결 시간
        KisDecimal["price"],  # 2 STCK_PRPR 주식 현재가
        KisAny(STOCK_SIGN_TYPE_MAP.__getitem__)["sign"],  # 3 PRDY_VRSS_SIGN 전일 대비 부호
        KisDecimal["change"],  # 4 PRDY_VRSS 전일 대비
        None,  # 5 PRDY_CTRT 전일 대비율
        None,  # 6 WGHN_AVRG_STCK_PRC 가중 평균 주식 가격
        KisDecimal["open"],  # 7 STCK_OPRC 주식 시가
        KisDecimal["high"],  # 8 STCK_HGPR 주식 고가
        KisDecimal["low"],  # 9 STCK_LWPR 주식 저가
        KisDecimal["ask"],  # 10 ASKP1	매도호가1
        KisDecimal["bid"],  # 11 BIDP1	매수호가1
        None,  # 12 CNTG_VOL 체결 거래량
        KisInt["volume"],  # 13 ACML_VOL 누적 거래량
        KisDecimal["amount"],  # 14 ACML_TR_PBMN 누적 거래 대금
        KisInt["sell_count"],  # 15 SELN_CNTG_CSNU 매도 체결 건수
        KisInt["buy_count"],  # 16 SHNU_CNTG_CSNU 매수 체결 건수
        None,  # 17 NTBY_CNTG_CSNU 순매수 체결 건수
        None,  # 18 CTTR 체결강도
        KisInt["sell_quantity"],  # 19 SELN_CNTG_SMTN 총 매도 수량
        KisInt["buy_quantity"],  # 20 SHNU_CNTG_SMTN 총 매수 수량
        None,  # 21 CCLD_DVSN 체결구분
        None,  # 22 SHNU_RATE 매수비율
        None,  # 23 PRDY_VOL_VRSS_ACML_VOL_RATE 전일 거래량 대비 등락율
        None,  # 24 OPRC_HOUR 시가 시간
        None,  # 25 OPRC_VRSS_PRPR_SIGN 시가대비구분
        None,  # 26 OPRC_VRSS_PRPR 시가대비
        None,  # 27 HGPR_HOUR 최고가 시간
        None,  # 28 HGPR_VRSS_PRPR_SIGN 고가대비구분
        None,  # 29 HGPR_VRSS_PRPR 고가대비
        None,  # 30 LWPR_HOUR 최저가 시간
        None,  # 31 LWPR_VRSS_PRPR_SIGN 저가대비구분
        None,  # 32 LWPR_VRSS_PRPR 저가대비
        None,  # 33 BSOP_DATE 영업 일자
        KisAny(lambda x: DOMESTIC_REALTIME_PRICE_ORDER_CONDITION_MAP[x[0]])[
            "condition"
        ],  # 34 NEW_MKOP_CLS_CODE 신 장운영 구분 코드
        None,  # 35 TRHT_YN 거래정지 여부
        None,  # 36 ASKP_RSQN1 매도호가 잔량1
        None,  # 37 BIDP_RSQN1 매수호가 잔량1
        KisInt["ask_quantity"],  # 38 TOTAL_ASKP_RSQN 총 매도호가 잔량
        KisInt["bid_quantity"],  # 39 TOTAL_BIDP_RSQN 총 매수호가 잔량
        None,  # 40 VOL_TNRT 거래량 회전율
        KisInt["prev_volume"],  # 41 PRDY_SMNS_HOUR_ACML_VOL 전일 동시간 누적 거래량
        None,  # 42 PRDY_SMNS_HOUR_ACML_VOL_RATE 전일 동시간 누적 거래량 비율
        None,  # 43 HOUR_CLS_CODE 시간 구분 코드
        None,  # 44 MRKT_TRTM_CLS_CODE 임의종료구분코드
        None,  # 45 VI_STND_PRC 정적VI발동기준가
    ]

    symbol: str  # MKSC_SHRN_ISCD 유가증권 단축 종목코드
    """종목코드"""
    market: MARKET_TYPE = "KRX"
    """상품유형타입"""

    time: datetime
    """체결 시간"""
    time_kst: datetime
    """체결 시간(KST)"""

    timezone: tzinfo = TIMEZONE
    """시간대"""

    price: Decimal  # STCK_PRPR 주식 현재가
    """현재가"""

    @property
    def prev_price(self) -> Decimal:
        """전일가"""
        return self.price - self.change

    change: Decimal  # PRDY_VRSS 전일 대비
    """전일대비"""
    sign: STOCK_SIGN_TYPE  # PRDY_VRSS_SIGN 전일 대비 부호
    """대비부호"""

    bid: Decimal  # BIDP1 매수호가1
    """매수호가"""
    ask: Decimal  # ASKP1 매도호가1
    """매도호가"""
    bid_quantity: int  # BIDP_RSQN1 매수호가 잔량1
    """매수호가잔량"""
    ask_quantity: int  # ASKP_RSQN1 매도호가 잔량1
    """매도호가잔량"""

    open: Decimal  # STCK_OPRC 주식 시가
    """당일시가"""
    open_time: datetime  # OPRC_HOUR 시가 시간
    """시가시간"""
    open_time_kst: datetime  # OPRC_HOUR 시가 시간(KST)
    """시가시간(KST)"""

    high: Decimal  # STCK_HGPR 주식 고가
    """당일고가"""
    high_time: datetime  # HGPR_HOUR 최고가 시간
    """고가시간"""
    high_time_kst: datetime  # HGPR_HOUR 최고가 시간(KST)
    """고가시간(KST)"""

    low: Decimal  # STCK_LWPR 주식 저가
    """당일저가"""
    low_time: datetime  # LWPR_HOUR 최저가 시간
    """저가시간"""
    low_time_kst: datetime  # LWPR_HOUR 최저가 시간(KST)
    """저가시간(KST)"""

    volume: int  # ACML_VOL 누적 거래량
    """누적거래량"""
    amount: Decimal  # ACML_TR_PBMN 누적 거래 대금
    """누적거래대금"""
    prev_volume: int | None
    """전일동일시간거래량"""
    buy_count: int  # SHNU_CNTG_CSNU 매수 체결 건수
    """매수체결건수"""
    sell_count: int  # SELN_CNTG_CSNU 매도 체결 건수
    """매도체결건수"""

    buy_quantity: int  # SHNU_CNTG_SMTN 총 매수 수량
    """매수체결량"""
    sell_quantity: int  # SELN_CNTG_SMTN 총 매도 수량
    """매도체결량"""

    condition: ORDER_CONDITION | None  # NEW_MKOP_CLS_CODE 신 장운영 구분 코드
    """주문조건"""

    decimal_places: int = 1
    """소수점 자리수"""

    def __pre_init__(self, data: list[str]):
        super().__pre_init__(data)

        self.time = datetime.strptime(data[33] + data[1], "%Y%m%d%H%M%S").replace(tzinfo=TIMEZONE)
        self.time_kst = self.time.astimezone(TIMEZONE)
        self.open_time = datetime.strptime(data[33] + data[24], "%Y%m%d%H%M%S").replace(tzinfo=TIMEZONE)
        self.open_time_kst = self.open_time.astimezone(TIMEZONE)
        self.high_time = datetime.strptime(data[33] + data[27], "%Y%m%d%H%M%S").replace(tzinfo=TIMEZONE)
        self.high_time_kst = self.high_time.astimezone(TIMEZONE)
        self.low_time = datetime.strptime(data[33] + data[30], "%Y%m%d%H%M%S").replace(tzinfo=TIMEZONE)
        self.low_time_kst = self.low_time.astimezone(TIMEZONE)


FOREIGN_REALTIME_PRICE_ORDER_CONDITION_MAP: dict[str, ORDER_CONDITION | None] = {
    "1": None,
    "2": None,
    "3": "extended",
}


def parse_foreign_realtime_symbol(raw_symbol: str) -> tuple[MARKET_TYPE, ORDER_CONDITION | None, str]:
    match raw_symbol[0]:
        case "D":
            return REVERSE_MARKET_SHORT_TYPE_MAP[raw_symbol[1:4]], None, raw_symbol[4:]
        case "R":
            return (
                REVERSE_DAYTIME_MARKET_SHORT_TYPE_MAP[raw_symbol[1:4]],
                "extended",
                raw_symbol[4:],
            )
        case _:
            raise ValueError(f"Invalid foreign realtime symbol: {raw_symbol!r}")


def build_foreign_realtime_symbol(market: MARKET_TYPE, symbol: str, extended: bool = False) -> str:
    if extended and market in DAYTIME_MARKET_SHORT_TYPE_MAP:
        return f"R{DAYTIME_MARKET_SHORT_TYPE_MAP[market]}{symbol}"

    return f"D{MARKET_SHORT_TYPE_MAP[market]}{symbol}"


class KisForeignRealtimePrice(KisRealtimePriceBase):
    """해외주식 실시간 체결가"""

    __fields__ = [
        None,  # 0 RSYM 실시간종목코드
        KisString["symbol"],  # 1 SYMB 종목코드
        KisInt["decimal_places"],  # 2 ZDIV 수수점자리수
        None,  # 3 TYMD 현지영업일자
        None,  # 4 XYMD 현지일자
        None,  # 5 XHMS 현지시간
        None,  # 6 KYMD 한국일자
        None,  # 7 KHMS 한국시간
        KisDecimal["open"],  # 8 OPEN 시가
        KisDecimal["high"],  # 9 HIGH 고가
        KisDecimal["low"],  # 10 LOW 저가
        KisDecimal["price"],  # 11 LAST 현재가
        KisAny(STOCK_SIGN_TYPE_MAP.__getitem__)["sign"],  # 12 SIGN 대비구분
        KisDecimal["change"],  # 13 DIFF 전일대비
        None,  # 14 RATE 등락율
        KisDecimal["bid"],  # 15 PBID 매수호가
        KisDecimal["ask"],  # 16 PASK 매도호가
        KisInt["bid_quantity"],  # 17 VBID 매수잔량
        KisInt["ask_quantity"],  # 18 VASK 매도잔량
        None,  # 19 EVOL 체결량
        KisInt["volume"],  # 20 TVOL 거래량
        KisInt["amount"],  # 21 TAMT 거래대금
        KisInt["sell_quantity"],  # 22 BIVL 매도체결량
        KisInt["buy_quantity"],  # 23 ASVL 매수체결량
        None,  # 24 STRN 체결강도
        KisAny(FOREIGN_REALTIME_PRICE_ORDER_CONDITION_MAP.get)["condition"],  # 25 MTYP 시장구분 1:장중,2:장전,3:장후
    ]

    symbol: str  # RSYM 실시간종목코드
    """종목코드"""
    market: MARKET_TYPE  # RSYM 실시간종목코드
    """상품유형타입"""

    time: datetime  # XYMD 현지일자 + XHMS 현지시간
    """체결 시간"""
    time_kst: datetime  # XYMD 현지일자 + XHMS 현지시간
    """체결 시간(KST)"""
    timezone: tzinfo  # RSYM 실시간종목코드
    """시간대"""

    price: Decimal  # LAST 현재가
    """현재가"""

    @property
    def prev_price(self) -> Decimal:
        """전일가"""
        return self.price - self.change

    change: Decimal  # DIFF 전일대비
    """전일대비"""
    sign: STOCK_SIGN_TYPE  # SIGN 대비구분
    """대비부호"""

    bid: Decimal  # PBID 매수호가
    """매수호가"""
    ask: Decimal  # PASK 매도호가
    """매도호가"""
    bid_quantity: int  # VBID 매수잔량
    """매수호가잔량"""
    ask_quantity: int  # VASK 매도잔량
    """매도호가잔량"""

    open: Decimal  # OPEN 시가
    """당일시가"""
    open_time: datetime | None = None
    """시가시간"""
    open_time_kst: datetime | None = None
    """시가시간(KST)"""

    high: Decimal  # HIGH 고가
    """당일고가"""
    high_time: datetime | None = None
    """고가시간"""
    high_time_kst: datetime | None = None
    """고가시간(KST)"""

    low: Decimal  # LOW 저가
    """당일저가"""
    low_time: datetime | None = None
    """저가시간"""
    low_time_kst: datetime | None = None
    """저가시간(KST)"""

    volume: int  # TVOL 거래량
    """누적거래량"""
    amount: Decimal  # TAMT 거래대금
    """누적거래대금"""
    prev_volume: int | None
    """전일동일시간거래량"""

    buy_quantity: int  # ASVL 매수체결량
    """매수체결량"""
    sell_quantity: int  # BIVL 매도체결량
    """매도체결량"""

    condition: ORDER_CONDITION | None  # MTYP 시장구분 1:장중,2:장전,3:장후
    """주문조건"""

    decimal_places: int  # ZDIV 수수점자리수
    """소수점 자리수"""

    def __pre_init__(self, data: list[str]):
        super().__pre_init__(data)

        (
            self.market,
            _,
            _,
        ) = parse_foreign_realtime_symbol(data[0])
        self.timezone = get_market_timezone(self.market)

        self.time = datetime.strptime(data[4] + data[5], "%Y%m%d%H%M%S").replace(tzinfo=self.timezone)
        self.time_kst = self.time.astimezone(TIMEZONE)


# IDE Type Checker
if TYPE_CHECKING:
    Checkable[KisRealtimePrice](KisDomesticRealtimePrice)
    Checkable[KisRealtimePrice](KisForeignRealtimePrice)


def on_price(
    self: "KisWebsocketClient",
    market: MARKET_TYPE,
    symbol: str,
    callback: Callable[["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimePrice]], None],
    where: KisEventFilter["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimePrice]] | None = None,
    once: bool = False,
    extended: bool = False,
) -> KisEventTicket["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimePrice]]:
    """
    웹소켓 이벤트 핸들러 등록

    [국내주식] 실시간시세 -> 국내주식 실시간체결가[실시간-003]
    [해외주식] 실시간시세 -> 해외주식 실시간지연체결가[실시간-007]

    Args:
        market (MARKET_TYPE): 시장유형
        symbol (str): 종목코드
        callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]], None]): 콜백 함수
        where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]] | None, optional): 이벤트 필터. Defaults to None.
        once (bool, optional): 한번만 실행 여부. Defaults to False.
        extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)
    """
    filter = KisProductEventFilter(symbol=symbol, market=market)

    return self.on(
        id="H0STCNT0" if market == "KRX" else "HDFSCNT0",
        key=(
            symbol
            if market == "KRX"
            else build_foreign_realtime_symbol(
                market=market,
                symbol=symbol,
                extended=extended,
            )
        ),
        callback=callback,
        where=KisMultiEventFilter(filter, where) if where else filter,
        once=once,
    )


def on_product_price(
    self: "KisProductProtocol",
    callback: Callable[["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimePrice]], None],
    where: KisEventFilter["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimePrice]] | None = None,
    once: bool = False,
    extended: bool = False,
) -> KisEventTicket["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimePrice]]:
    """
    웹소켓 이벤트 핸들러 등록

    [국내주식] 실시간시세 -> 국내주식 실시간체결가[실시간-003]
    [해외주식] 실시간시세 -> 해외주식 실시간지연체결가[실시간-007]

    Args:
        callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]], None]): 콜백 함수
        where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimePrice]] | None, optional): 이벤트 필터. Defaults to None.
        once (bool, optional): 한번만 실행 여부. Defaults to False.
        extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)
    """
    return on_price(
        self.kis.websocket,
        market=self.market,
        symbol=self.symbol,
        callback=callback,
        where=where,
        once=once,
        extended=extended,
    )
