from datetime import datetime, tzinfo
from decimal import Decimal

from pykis.__env__ import TIMEZONE
from pykis.api.account.order import ORDER_CONDITION
from pykis.api.stock.asking_price import KisAskingPrice, KisAskingPriceItem
from pykis.api.stock.market import (
    CURRENCY_TYPE,
    MARKET_TYPE,
    get_market_currency,
    get_market_timezone,
)
from pykis.api.websocket.price import parse_overseas_realtime_symbol
from pykis.responses.types import KisAny, KisInt, KisString
from pykis.responses.websocket import KisWebsocketResponse


class KisRealtimeAskingPrice(KisWebsocketResponse, KisAskingPrice):
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
    currency: CURRENCY_TYPE
    """통화코드"""

    ask: list[KisAskingPriceItem]
    """매도호가"""
    bid: list[KisAskingPriceItem]
    """매수호가"""

    condition: ORDER_CONDITION | None
    """주문 조건"""


DOMESTIC_REALTIME_ASKING_PRICE_ORDER_CONDITION_MAP: dict[str, ORDER_CONDITION | None] = {
    "0": None,
    "A": "after",
    "B": "before",
    "C": None,
    "D": "extended",
}


class KisDomesticRealtimeAskingPrice(KisRealtimeAskingPrice):
    """국내주식 실시간 호가"""

    __fields__ = [
        KisString["symbol"],  # 0 MKSC_SHRN_ISCD 유가증권 단축 종목코드
        None,  # 1 BSOP_HOUR 영업 시간
        KisAny(lambda x: DOMESTIC_REALTIME_ASKING_PRICE_ORDER_CONDITION_MAP.get(x))[
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
    currency: CURRENCY_TYPE = "KRW"
    """통화코드"""

    ask: list[KisAskingPriceItem]  # 매도호가
    """매도호가"""
    bid: list[KisAskingPriceItem]  # 매수호가
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

        self.ask = [
            KisAskingPriceItem(
                price=Decimal(data[3 + i]),
                volume=int(data[23 + i]),
            )
            for i in range(10)
        ]
        self.bid = [
            KisAskingPriceItem(
                price=Decimal(data[13 + i]),
                volume=int(data[33 + i]),
            )
            for i in range(10)
        ]


class KisAsiaRealtimeAskingPrice(KisRealtimeAskingPrice):
    """아시아 주식 실시간 호가"""

    __fields__ = [
        None,  # 0 RSYM	실시간종목코드
        KisString["symbol"],  # 1 SYMB	종목코드
        KisInt["decimal_places"],  # 2 ZDIV	소수점자리수
        None,  # 3 XYMD	현지일자
        None,  # 4 XHMS	현지시간
        None,  # 5 KYMD	한국일자
        None,  # 6 KHMS	한국시간
        None,  # 7 BVOL	매수총잔량
        None,  # 8 AVOL	매도총잔량
        None,  # 9 BDVL	매수총잔량대비
        None,  # 10 ADVL	매도총잔량대비
        None,  # 11 PBID1	매수호가1
        None,  # 12 PASK1	매도호가1
        None,  # 13 VBID1	매수잔량1
        None,  # 14 VASK1	매도잔량1
        None,  # 15 DBID1	매수잔량대비1
        None,  # 16 DASK1	매도잔량대비1
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
    currency: CURRENCY_TYPE  # RSYM 실시간종목코드
    """통화코드"""

    ask: list[KisAskingPriceItem]  # PASK1 매도호가1, VASK1 매도잔량1
    """매도호가"""
    bid: list[KisAskingPriceItem]  # PBID1 매수호가1, VBID1 매수잔량1
    """매수호가"""

    condition: ORDER_CONDITION | None  # RSYM 실시간종목코드
    """주문 조건"""

    def __pre_init__(self, data: list[str]):
        super().__pre_init__(data)

        (
            self.market,
            self.condition,
            _,
        ) = parse_overseas_realtime_symbol(data[0])
        self.timezone = get_market_timezone(self.market)
        self.currency = get_market_currency(self.market)

        self.time = datetime.strptime(data[3] + data[4], "%Y%m%d%H%M%S").replace(tzinfo=self.timezone)
        self.time_kst = self.time.astimezone(TIMEZONE)

        self.ask = [
            KisAskingPriceItem(
                price=Decimal(data[12]),
                volume=int(data[14]),
            )
        ]
        self.bid = [
            KisAskingPriceItem(
                price=Decimal(data[11]),
                volume=int(data[13]),
            )
        ]
