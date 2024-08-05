from datetime import datetime, tzinfo
from decimal import Decimal
from typing import TYPE_CHECKING, Callable, Protocol, runtime_checkable

from pykis.api.account.order import ORDER_CONDITION
from pykis.api.base.product import KisProductProtocol
from pykis.api.stock.market import MARKET_TYPE, get_market_timezone
from pykis.api.stock.order_book import (
    KisOrderbook,
    KisOrderbookBase,
    KisOrderbookItem,
    KisOrderbookItemBase,
)
from pykis.api.websocket.price import (
    build_foreign_realtime_symbol,
    parse_foreign_realtime_symbol,
)
from pykis.event.filters.product import KisProductEventFilter
from pykis.event.handler import KisEventFilter, KisEventTicket, KisMultiEventFilter
from pykis.event.subscription import KisSubscriptionEventArgs
from pykis.responses.types import KisAny, KisInt, KisString
from pykis.responses.websocket import KisWebsocketResponse, KisWebsocketResponseProtocol
from pykis.utils.timezone import TIMEZONE
from pykis.utils.typing import Checkable

if TYPE_CHECKING:
    from pykis.client.websocket import KisWebsocketClient


@runtime_checkable
class KisRealtimeOrderbook(KisWebsocketResponseProtocol, KisOrderbook, Protocol):
    """한국투자증권 실시간 호가"""


class KisRealtimeOrderbookBase(KisWebsocketResponse, KisOrderbookBase):
    """한국투자증권 실시간 호가"""

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

    decimal_places: int
    """소수점 자리수"""

    asks: list[KisOrderbookItem]
    """매도호가"""
    bids: list[KisOrderbookItem]
    """매수호가"""

    condition: ORDER_CONDITION | None
    """주문 조건"""


DOMESTIC_REALTIME_ORDER_BOOK_ORDER_CONDITION_MAP: dict[str, ORDER_CONDITION | None] = {
    "0": None,
    "A": "after",
    "B": "before",
    "C": None,
    "D": "extended",
}


class KisDomesticRealtimeOrderbookItem(KisOrderbookItemBase):
    """국내주식 실시간 호가"""


class KisDomesticRealtimeOrderbook(KisRealtimeOrderbookBase):
    """국내주식 실시간 호가"""

    __fields__ = [
        KisString["symbol"],  # 0 MKSC_SHRN_ISCD 유가증권 단축 종목코드
        None,  # 1 BSOP_HOUR 영업 시간
        KisAny(DOMESTIC_REALTIME_ORDER_BOOK_ORDER_CONDITION_MAP.get)[
            "condition"
        ],  # 2 HOUR_CLS_CODE 시간 구분 코드
        None,  # 3 ASKP1 매도호가1
        None,  # 4 ASKP2 매도호가2
        None,  # 5 ASKP3 매도호가3
        None,  # 6 ASKP4 매도호가4
        None,  # 7 ASKP5 매도호가5
        None,  # 8 ASKP6 매도호가6
        None,  # 9 ASKP7 매도호가7
        None,  # 10 ASKP8 매도호가8
        None,  # 11 ASKP9 매도호가9
        None,  # 12 ASKP10 매도호가10
        None,  # 13 BIDP1 매수호가1
        None,  # 14 BIDP2 매수호가2
        None,  # 15 BIDP3 매수호가3
        None,  # 16 BIDP4 매수호가4
        None,  # 17 BIDP5 매수호가5
        None,  # 18 BIDP6 매수호가6
        None,  # 19 BIDP7 매수호가7
        None,  # 20 BIDP8 매수호가8
        None,  # 21 BIDP9 매수호가9
        None,  # 22 BIDP10 매수호가10
        None,  # 23 ASKP_RSQN1 매도호가 잔량1
        None,  # 24 ASKP_RSQN2 매도호가 잔량2
        None,  # 25 ASKP_RSQN3 매도호가 잔량3
        None,  # 26 ASKP_RSQN4 매도호가 잔량4
        None,  # 27 ASKP_RSQN5 매도호가 잔량5
        None,  # 28 ASKP_RSQN6 매도호가 잔량6
        None,  # 29 ASKP_RSQN7 매도호가 잔량7
        None,  # 30 ASKP_RSQN8 매도호가 잔량8
        None,  # 31 ASKP_RSQN9 매도호가 잔량9
        None,  # 32 ASKP_RSQN10 매도호가 잔량10
        None,  # 33 BIDP_RSQN1 매수호가 잔량1
        None,  # 34 BIDP_RSQN2 매수호가 잔량2
        None,  # 35 BIDP_RSQN3 매수호가 잔량3
        None,  # 36 BIDP_RSQN4 매수호가 잔량4
        None,  # 37 BIDP_RSQN5 매수호가 잔량5
        None,  # 38 BIDP_RSQN6 매수호가 잔량6
        None,  # 39 BIDP_RSQN7 매수호가 잔량7
        None,  # 40 BIDP_RSQN8 매수호가 잔량8
        None,  # 41 BIDP_RSQN9 매수호가 잔량9
        None,  # 42 BIDP_RSQN10 매수호가 잔량10
        None,  # 43 TOTAL_ASKP_RSQN 총 매도호가 잔량
        None,  # 44 TOTAL_BIDP_RSQN 총 매수호가 잔량
        None,  # 45 OVTM_TOTAL_ASKP_RSQN 시간외 총 매도호가 잔량
        None,  # 46 OVTM_TOTAL_BIDP_RSQN 시간외 총 매수호가 잔량
        None,  # 47 ANTC_CNPR 예상 체결가
        None,  # 48 ANTC_CNQN 예상 체결량
        None,  # 49 ANTC_VOL 예상 거래량
        None,  # 50 ANTC_CNTG_VRSS 예상 체결 대비
        None,  # 51 ANTC_CNTG_VRSS_SIGN 예상 체결 대비 부호
        None,  # 52 ANTC_CNTG_PRDY_CTRT 예상 체결 전일 대비율
        None,  # 53 ACML_VOL 누적 거래량
        None,  # 54 TOTAL_ASKP_RSQN_ICDC 총 매도호가 잔량 증감
        None,  # 55 TOTAL_BIDP_RSQN_ICDC 총 매수호가 잔량 증감
        None,  # 56 OVTM_TOTAL_ASKP_ICDC 시간외 총 매도호가 증감
        None,  # 57 OVTM_TOTAL_BIDP_ICDC 시간외 총 매수호가 증감
        None,  # 58 STCK_DEAL_CLS_CODE 주식 매매 구분 코드
    ]

    symbol: str  # MKSC_SHRN_ISCD 유가증권 단축 종목코드
    """종목코드"""
    market: MARKET_TYPE = "KRX"
    """상품유형타입"""

    time: datetime  # BSOP_HOUR 영업 시간
    """체결 시간"""
    time_kst: datetime  # BSOP_HOUR 영업 시간
    """체결 시간(KST)"""
    timezone: tzinfo = TIMEZONE
    """시간대"""

    decimal_places: int = 1
    """소수점 자리수"""

    asks: list[KisOrderbookItem]  # 매도호가
    """매도호가"""
    bids: list[KisOrderbookItem]  # 매수호가
    """매수호가"""

    condition: ORDER_CONDITION | None  # HOUR_CLS_CODE 시간 구분 코드
    """주문 조건"""

    def __pre_init__(self, data: list[str]):
        super().__pre_init__(data)

        self.time = datetime.combine(
            datetime.now().date(),
            datetime.strptime(data[1], "%H%M%S").time(),
            tzinfo=TIMEZONE,
        )
        self.time_kst = self.time.astimezone(TIMEZONE)

        self.asks = [
            KisDomesticRealtimeOrderbookItem(
                price=Decimal(data[3 + i]),
                volume=int(data[23 + i]),
            )
            for i in range(10)
        ]
        self.bids = [
            KisDomesticRealtimeOrderbookItem(
                price=Decimal(data[13 + i]),
                volume=int(data[33 + i]),
            )
            for i in range(10)
        ]


class KisAsiaRealtimeOrderbookItem(KisOrderbookItemBase):
    """아시아 주식 실시간 호가"""


class KisAsiaRealtimeOrderbook(KisRealtimeOrderbookBase):
    """아시아 주식 실시간 호가"""

    __fields__ = [
        None,  # 0 RSYM	실시간종목코드
        KisString["symbol"],  # 1 SYMB 종목코드
        KisInt["decimal_places"],  # 2 ZDIV 소수점자리수
        None,  # 3 XYMD 현지일자
        None,  # 4 XHMS 현지시간
        None,  # 5 KYMD 한국일자
        None,  # 6 KHMS 한국시간
        None,  # 7 BVOL 매수총잔량
        None,  # 8 AVOL 매도총잔량
        None,  # 9 BDVL 매수총잔량대비
        None,  # 10 ADVL 매도총잔량대비
        None,  # 11 PBID1 매수호가1
        None,  # 12 PASK1 매도호가1
        None,  # 13 VBID1 매수잔량1
        None,  # 14 VASK1 매도잔량1
        None,  # 15 DBID1 매수잔량대비1
        None,  # 16 DASK1 매도잔량대비1
    ]

    symbol: str  # SYMB 종목코드
    """종목코드"""
    market: MARKET_TYPE  # RSYM 실시간종목코드
    """상품유형타입"""

    time: datetime  # XYMD 현지일자, XHMS 현지시간
    """체결 시간"""
    time_kst: datetime  # XYMD 현지일자, XHMS 현지시간
    """체결 시간(KST)"""
    timezone: tzinfo  # RSYM 실시간종목코드
    """시간대"""

    decimal_places: int  # ZDIV 소수점자리수
    """소수점 자리수"""

    asks: list[KisOrderbookItem]  # PASK1 매도호가1, VASK1 매도잔량1
    """매도호가"""
    bids: list[KisOrderbookItem]  # PBID1 매수호가1, VBID1 매수잔량1
    """매수호가"""

    condition: ORDER_CONDITION | None  # RSYM 실시간종목코드
    """주문 조건"""

    def __pre_init__(self, data: list[str]):
        super().__pre_init__(data)

        (
            self.market,
            self.condition,
            _,
        ) = parse_foreign_realtime_symbol(data[0])
        self.timezone = get_market_timezone(self.market)

        self.time = datetime.strptime(data[3] + data[4], "%Y%m%d%H%M%S").replace(tzinfo=self.timezone)
        self.time_kst = self.time.astimezone(TIMEZONE)

        self.asks = [
            KisAsiaRealtimeOrderbookItem(
                price=Decimal(data[12]),
                volume=int(data[14]),
            )
        ]
        self.bids = [
            KisAsiaRealtimeOrderbookItem(
                price=Decimal(data[11]),
                volume=int(data[13]),
            )
        ]


class KisUSRealtimeOrderbookItem(KisOrderbookItemBase):
    """미국 주식 실시간 호가"""


class KisUSRealtimeOrderbook(KisRealtimeOrderbookBase):
    """미국 주식 실시간 호가"""

    __fields__ = [
        None,  # 0 RSYM 실시간종목코드
        KisString["symbol"],  # 1 SYMB 종목코드
        KisInt["decimal_places"],  # 2 ZDIV 소수점자리수
        None,  # 3 XYMD 현지일자
        None,  # 4 XHMS 현지시간
        None,  # 5 KYMD 한국일자
        None,  # 6 KHMS 한국시간
        None,  # 7 BVOL 매수총잔량
        None,  # 8 AVOL 매도총잔량
        None,  # 9 BDVL 매수총잔량대비
        None,  # 10 ADVL 매도총잔량대비
        None,  # 11 PBID1 매수호가1
        None,  # 12 PASK1 매도호가1
        None,  # 13 VBID1 매수잔량1
        None,  # 14 VASK1 매도잔량1
        None,  # 15 DBID1 매수잔량대비1
        None,  # 16 DASK1 매도잔량대비1
        None,  # 17 PBID2 매수호가2
        None,  # 18 PASK2 매도호가2
        None,  # 19 VBID2 매수잔량2
        None,  # 20 VASK2 매도잔량2
        None,  # 21 DBID2 매수잔량대비2
        None,  # 22 DASK2 매도잔량대비2
        None,  # 23 PBID3 매수호가3
        None,  # 24 PASK3 매도호가3
        None,  # 25 VBID3 매수잔량3
        None,  # 26 VASK3 매도잔량3
        None,  # 27 DBID3 매수잔량대비3
        None,  # 28 DASK3 매도잔량대비3
        None,  # 29 PBID4 매수호가4
        None,  # 30 PASK4 매도호가4
        None,  # 31 VBID4 매수잔량4
        None,  # 32 VASK4 매도잔량4
        None,  # 33 DBID4 매수잔량대비4
        None,  # 34 DASK4 매도잔량대비4
        None,  # 35 PBID5 매수호가5
        None,  # 36 PASK5 매도호가5
        None,  # 37 VBID5 매수잔량5
        None,  # 38 VASK5 매도잔량5
        None,  # 39 DBID5 매수잔량대비5
        None,  # 40 DASK5 매도잔량대비5
        None,  # 41 PBID6 매수호가6
        None,  # 42 PASK6 매도호가6
        None,  # 43 VBID6 매수잔량6
        None,  # 44 VASK6 매도잔량6
        None,  # 45 DBID6 매수잔량대비6
        None,  # 46 DASK6 매도잔량대비6
        None,  # 47 PBID7 매수호가7
        None,  # 48 PASK7 매도호가7
        None,  # 49 VBID7 매수잔량7
        None,  # 50 VASK7 매도잔량7
        None,  # 51 DBID7 매수잔량대비7
        None,  # 52 DASK7 매도잔량대비7
        None,  # 53 PBID8 매수호가8
        None,  # 54 PASK8 매도호가8
        None,  # 55 VBID8 매수잔량8
        None,  # 56 VASK8 매도잔량8
        None,  # 57 DBID8 매수잔량대비8
        None,  # 58 DASK8 매도잔량대비8
        None,  # 59 PBID9 매수호가9
        None,  # 60 PASK9 매도호가9
        None,  # 61 VBID9 매수잔량9
        None,  # 62 VASK9 매도잔량9
        None,  # 63 DBID9 매수잔량대비9
        None,  # 64 DASK9 매도잔량대비9
        None,  # 65 PBID10 매수호가10
        None,  # 66 PASK10 매도호가10
        None,  # 67 VBID10 매수잔량10
        None,  # 68 VASK10 매도잔량10
        None,  # 69 DBID10 매수잔량대비10
        None,  # 70 DASK10 매도잔량대비10
    ]

    symbol: str  # SYMB 종목코드
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    time: datetime
    """체결 시간"""
    time_kst: datetime
    """체결 시간(KST)"""
    timezone: tzinfo
    """시간대"""

    decimal_places: int  # ZDIV 소수점자리수
    """소수점 자리수"""

    asks: list[KisOrderbookItem]
    """매도호가"""
    bids: list[KisOrderbookItem]
    """매수호가"""

    condition: ORDER_CONDITION | None
    """주문 조건"""

    def __pre_init__(self, data: list[str]):
        super().__pre_init__(data)

        (
            self.market,
            self.condition,
            _,
        ) = parse_foreign_realtime_symbol(data[0])
        self.timezone = get_market_timezone(self.market)

        self.time = datetime.strptime(data[3] + data[4], "%Y%m%d%H%M%S").replace(tzinfo=self.timezone)
        self.time_kst = self.time.astimezone(TIMEZONE)

        self.asks = [
            KisUSRealtimeOrderbookItem(
                price=Decimal(data[12 + i * 6]),
                volume=int(data[14 + i * 6]),
            )
            for i in range(10)
        ]
        self.bids = [
            KisUSRealtimeOrderbookItem(
                price=Decimal(data[11 + i * 6]),
                volume=int(data[13 + i * 6]),
            )
            for i in range(10)
        ]


# IDE Type Checker
if TYPE_CHECKING:
    Checkable[KisRealtimeOrderbook](KisDomesticRealtimeOrderbook)
    Checkable[KisRealtimeOrderbook](KisAsiaRealtimeOrderbook)
    Checkable[KisRealtimeOrderbook](KisUSRealtimeOrderbook)


def on_order_book(
    self: "KisWebsocketClient",
    market: MARKET_TYPE,
    symbol: str,
    callback: Callable[["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimeOrderbook]], None],
    where: KisEventFilter["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimeOrderbook]] | None = None,
    once: bool = False,
    extended: bool = False,
) -> KisEventTicket["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimeOrderbook]]:
    """
    웹소켓 이벤트 핸들러 등록

    [국내주식] 실시간시세 -> 국내주식 실시간호가[실시간-004]
    [해외주식] 실시간시세 -> 해외주식 실시간지연호가(아시아)[실시간-008]
    [해외주식] 실시간시세 -> 해외주식 실시간호가(미국)[실시간-021]

    Args:
        market (MARKET_TYPE): 시장유형
        symbol (str): 종목코드
        callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderbook]], None]): 콜백 함수
        where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderbook]] | None, optional): 이벤트 필터. Defaults to None.
        once (bool, optional): 한번만 실행 여부. Defaults to False.
        extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)
    """
    filter = KisProductEventFilter(symbol=symbol, market=market)

    return self.on(
        id=(
            "H0STASP0"
            if market == "KRX"
            else "HDFSASP0" if market in ("NYSE", "NASDAQ", "AMEX") else "HDFSASP1"
        ),
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


def on_product_order_book(
    self: "KisProductProtocol",
    callback: Callable[["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimeOrderbook]], None],
    where: KisEventFilter["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimeOrderbook]] | None = None,
    once: bool = False,
    extended: bool = False,
) -> KisEventTicket["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimeOrderbook]]:
    """
    웹소켓 이벤트 핸들러 등록

    [국내주식] 실시간시세 -> 국내주식 실시간호가[실시간-004]
    [해외주식] 실시간시세 -> 해외주식 실시간지연호가(아시아)[실시간-008]
    [해외주식] 실시간시세 -> 해외주식 실시간호가(미국)[실시간-021]

    Args:
        callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderbook]], None]): 콜백 함수
        where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeOrderbook]] | None, optional): 이벤트 필터. Defaults to None.
        once (bool, optional): 한번만 실행 여부. Defaults to False.
        extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)
    """
    return on_order_book(
        self.kis.websocket,
        market=self.market,
        symbol=self.symbol,
        callback=callback,
        where=where,
        once=once,
        extended=extended,
    )
