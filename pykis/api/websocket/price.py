from datetime import date, datetime
from datetime import time as time_type
from datetime import tzinfo
from decimal import Decimal

from pykis.__env__ import TIMEZONE
from pykis.api.account.order import ORDER_CONDITION, ORDER_CONDITION_MAP, ORDER_TYPE
from pykis.api.base.product import KisProductBase
from pykis.api.stock.market import (
    CURRENCY_TYPE,
    MARKET_TYPE,
    REVERSE_DAYTIME_MARKET_SHORT_TYPE_MAP,
    REVERSE_MARKET_SHORT_TYPE_MAP,
)
from pykis.api.stock.quote import (
    STOCK_SIGN_TYPE,
    STOCK_SIGN_TYPE_KOR_MAP,
    STOCK_SIGN_TYPE_MAP,
)
from pykis.responses.types import (
    KisAny,
    KisDate,
    KisDecimal,
    KisInt,
    KisString,
    KisTime,
)
from pykis.responses.websocket import KisWebsocketResponse
from pykis.utils.repr import kis_repr


def parse_overseas_realtime_symbol(raw_symbol: str) -> tuple[MARKET_TYPE, ORDER_CONDITION | None, str]:
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
            raise ValueError(f"Invalid overseas realtime symbol: {raw_symbol!r}")


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
class KisRealtimePrice(KisWebsocketResponse, KisProductBase):
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
        return self.change / self.price * 100

    bid: Decimal
    """매수호가"""
    ask: Decimal
    """매도호가"""
    bid_quantity: Decimal
    """매수호가잔량"""
    ask_quantity: Decimal
    """매도호가잔량"""

    @property
    def spread(self) -> Decimal:
        """매수/매도호가대비"""
        return self.ask - self.bid

    @property
    def spread_rate(self) -> Decimal:
        """매수/매도호가대비율 (-100~100)"""
        return self.spread / self.price * 100

    @property
    def bid_qty(self) -> Decimal:
        """매수호가잔량"""
        return self.bid_quantity

    @property
    def ask_qty(self) -> Decimal:
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
        return self.open_change / self.open * 100

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
        return self.high_change / self.high * 100

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
        return self.low_change / self.low * 100

    volume: int
    """누적거래량"""
    amount: Decimal
    """누적거래대금"""
    prev_volume: int | None
    """전일동일시간거래량"""
    count: int
    """체결건수"""
    buy_quantity: Decimal
    """매수체결량"""
    sell_quantity: Decimal
    """매도체결량"""

    @property
    def intensity(self) -> Decimal:
        """체결강도 (0 ~ 100+)"""
        return (self.buy_quantity / self.sell_quantity * 100) if self.sell_quantity else Decimal(100)

    @property
    def buy_qty(self) -> Decimal:
        """매수체결량"""
        return self.buy_quantity

    @property
    def sell_qty(self) -> Decimal:
        """매도체결량"""
        return self.sell_quantity

    @property
    def volume_rate(self) -> Decimal | None:
        """전일동일시간거래량비율 (-100~100)"""
        return Decimal(self.volume / self.prev_volume * 100) if self.prev_volume else None

    type: ORDER_TYPE
    """주문구분"""
    quantity: Decimal
    """거래량"""
    condition: ORDER_CONDITION | None
    """주문조건"""

    @property
    def qty(self) -> Decimal:
        """거래량"""
        return self.quantity

    decimal_places: int
    """소수점 자리수"""

    currency: CURRENCY_TYPE
    """통화코드"""


DOMESTIC_REALTIME_PRICE_ORDER_CONDITION_MAP: dict[str, ORDER_CONDITION | None] = {
    "1": "before",
    "2": None,
    "3": "after",
    "4": "extended",
}


class KisDomesticRealtimePrice(KisRealtimePrice):
    """국내주식 실시간 체결가"""

    __fields__ = [
        KisString["symbol"],  # 0 MKSC_SHRN_ISCD 유가증권 단축 종목코드
        None,  # 1 STCK_CNTG_HOUR 주식 체결 시간
        KisDecimal["price"],  # 2 STCK_PRPR 주식 현재가
        KisAny(lambda x: STOCK_SIGN_TYPE_MAP[x])["sign"],  # 3 PRDY_VRSS_SIGN 전일 대비 부호
        KisDecimal["change"],  # 4 PRDY_VRSS 전일 대비
        None,  # 5 PRDY_CTRT 전일 대비율
        None,  # 6 WGHN_AVRG_STCK_PRC 가중 평균 주식 가격
        KisDecimal["open"],  # 7 STCK_OPRC 주식 시가
        KisDecimal["high"],  # 8 STCK_HGPR 주식 고가
        KisDecimal["low"],  # 9 STCK_LWPR 주식 저가
        KisDecimal["ask"],  # 10 ASKP1	매도호가1
        KisDecimal["bid"],  # 11 BIDP1	매수호가1
        KisDecimal["quantity"],  # 12 CNTG_VOL 체결 거래량
        KisInt["volume"],  # 13 ACML_VOL 누적 거래량
        KisDecimal["amount"],  # 14 ACML_TR_PBMN 누적 거래 대금
        KisInt["sell_count"],  # 15 SELN_CNTG_CSNU 매도 체결 건수
        KisInt["buy_count"],  # 16 SHNU_CNTG_CSNU 매수 체결 건수
        None,  # 17 NTBY_CNTG_CSNU 순매수 체결 건수
        None,  # 18 CTTR 체결강도
        KisDecimal["sell_quantity"],  # 19 SELN_CNTG_SMTN 총 매도 수량
        KisDecimal["buy_quantity"],  # 20 SHNU_CNTG_SMTN 총 매수 수량
        KisAny(lambda x: "buy" if x == "1" else "sell")["type"],  # 21 CCLD_DVSN 체결구분
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
        KisAny(lambda x: DOMESTIC_REALTIME_PRICE_ORDER_CONDITION_MAP.get(x))[
            "condition"
        ],  # 34 NEW_MKOP_CLS_CODE 신 장운영 구분 코드
        None,  # 35 TRHT_YN 거래정지 여부
        None,  # 36 ASKP_RSQN1 매도호가 잔량1
        None,  # 37 BIDP_RSQN1 매수호가 잔량1
        KisDecimal["ask_quantity"],  # 38 TOTAL_ASKP_RSQN 총 매도호가 잔량
        KisDecimal["bid_quantity"],  # 39 TOTAL_BIDP_RSQN 총 매수호가 잔량
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
    bid_quantity: Decimal  # BIDP_RSQN1 매수호가 잔량1
    """매수호가잔량"""
    ask_quantity: Decimal  # ASKP_RSQN1 매도호가 잔량1
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

    @property
    def count(self) -> int:
        """체결건수"""
        return self.buy_count + self.sell_count

    buy_quantity: Decimal  # SHNU_CNTG_SMTN 총 매수 수량
    """매수체결량"""
    sell_quantity: Decimal  # SELN_CNTG_SMTN 총 매도 수량
    """매도체결량"""

    type: ORDER_TYPE  # CCLD_DVSN 체결구분
    """주문구분"""
    quantity: int  # CNTG_VOL 체결 거래량
    """거래량"""
    condition: ORDER_CONDITION | None  # NEW_MKOP_CLS_CODE 신 장운영 구분 코드
    """주문조건"""

    decimal_places: int = 1
    """소수점 자리수"""

    currency: CURRENCY_TYPE = "KRW"
    """통화코드"""

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