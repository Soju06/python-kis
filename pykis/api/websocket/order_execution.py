from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Callable, Protocol, runtime_checkable
from zoneinfo import ZoneInfo

from pykis.api.account.order import (
    ORDER_CONDITION,
    ORDER_EXECUTION,
    ORDER_QUANTITY,
    ORDER_TYPE,
    KisOrder,
    KisOrderNumber,
    KisSimpleOrder,
    resolve_domestic_order_condition,
)
from pykis.api.base.account import KisAccountProtocol
from pykis.api.base.account_product import KisAccountProductBase
from pykis.api.stock.info import COUNTRY_TYPE, get_market_country
from pykis.api.stock.market import get_market_timezone
from pykis.client.account import KisAccountNumber
from pykis.event.handler import KisEventFilter, KisEventTicket
from pykis.event.subscription import KisSubscriptionEventArgs
from pykis.responses.types import KisAny, KisDecimal, KisString, KisTimeToDatetime
from pykis.responses.websocket import KisWebsocketResponse, KisWebsocketResponseProtocol
from pykis.utils.repr import kis_repr
from pykis.utils.timezone import TIMEZONE
from pykis.utils.typing import Checkable

if TYPE_CHECKING:
    from pykis.api.stock.market import MARKET_TYPE
    from pykis.client.websocket import KisWebsocketClient

__all__ = [
    "KisRealtimeExecution",
]


@runtime_checkable
class KisRealtimeExecution(KisWebsocketResponseProtocol, Protocol):
    """한국투자증권 실시간 체결"""

    @property
    def time(self) -> datetime:
        """주문시각"""
        ...

    @property
    def time_kst(self) -> datetime:
        """주문시각(KST)"""
        ...

    @property
    def timezone(self) -> ZoneInfo:
        """시간대"""
        ...

    @property
    def order_number(self) -> KisOrderNumber:
        """주문번호"""
        ...

    @property
    def type(self) -> ORDER_TYPE:
        """주문유형"""
        ...

    @property
    def price(self) -> Decimal:
        """체결단가"""
        ...

    @property
    def unit_price(self) -> Decimal | None:
        """주문단가"""
        ...

    @property
    def order_price(self) -> Decimal | None:
        """주문단가"""
        ...

    @property
    def quantity(self) -> ORDER_QUANTITY:
        """주문수량"""
        ...

    @property
    def qty(self) -> ORDER_QUANTITY:
        """주문수량"""
        ...

    @property
    def executed_quantity(self) -> ORDER_QUANTITY:
        """체결수량"""
        ...

    @property
    def executed_qty(self) -> ORDER_QUANTITY:
        """체결수량"""
        ...

    @property
    def executed_amount(self) -> Decimal:
        """체결금액"""
        ...

    @property
    def condition(self) -> ORDER_CONDITION | None:
        """주문조건"""
        ...

    @property
    def execution(self) -> ORDER_EXECUTION | None:
        """체결조건"""
        ...

    @property
    def receipt(self) -> bool:
        """접수여부"""
        ...

    @property
    def canceled(self) -> bool:
        """취소여부 (IOC/FOK)"""
        ...

    @property
    def rejected(self) -> bool:
        """거부여부"""
        ...

    @property
    def rejected_reason(self) -> str | None:
        """거부사유"""
        ...


@kis_repr(
    "account_number",
    "market",
    "symbol",
    "time",
    "type",
    "price",
    "executed_qty",
    lines="single",
)
class KisRealtimeExecutionRepr:
    """한국투자증권 실시간 체결"""


class KisRealtimeExecutionBase(KisRealtimeExecutionRepr, KisWebsocketResponse, KisAccountProductBase):
    """한국투자증권 실시간 체결"""

    symbol: str
    """종목코드"""
    market: "MARKET_TYPE"
    """상품유형타입"""

    account_number: KisAccountNumber
    """계좌번호"""

    time: datetime
    """체결시각"""
    time_kst: datetime
    """체결시각(KST)"""
    timezone: ZoneInfo
    """시간대"""

    order_number: KisOrderNumber
    """주문번호"""

    type: ORDER_TYPE
    """주문유형"""

    price: Decimal
    """체결단가"""
    unit_price: Decimal | None
    """주문단가"""

    @property
    def order_price(self) -> Decimal | None:
        """주문단가"""
        return self.unit_price

    quantity: ORDER_QUANTITY
    """주문수량"""

    @property
    def qty(self) -> ORDER_QUANTITY:
        """주문수량"""
        return self.quantity

    executed_quantity: ORDER_QUANTITY
    """체결수량"""

    @property
    def executed_qty(self) -> ORDER_QUANTITY:
        """체결수량"""
        return self.executed_quantity

    executed_amount: Decimal
    """체결금액"""

    condition: ORDER_CONDITION | None
    """주문조건"""
    execution: ORDER_EXECUTION | None
    """체결조건"""

    receipt: bool
    """접수여부"""

    canceled: bool
    """취소여부 (IOC/FOK)"""
    rejected: bool
    """거부여부"""
    rejected_reason: str | None
    """거부사유"""


class KisDomesticRealtimeOrderExecution(KisRealtimeExecutionBase):
    """한국투자증권 국내주식 실시간 체결"""

    __fields__ = [
        None,  # 0 CUST_ID 고객 ID
        KisAny(KisAccountNumber)["account_number"],  # 1 ACNT_NO 계좌번호
        None,  # 2 ODER_NO 주문번호
        None,  # 3 OODER_NO 원주문번호
        KisAny(lambda x: "sell" if x == "01" else "buy")["type"],  # 4 SELN_BYOV_CLS 매도매수구분 01 : 매도 02 : 매수
        None,  # 5 RCTF_CLS 정정구분
        None,  # 6 ODER_KIND 주문종류 00 : 지정가 01 : 시장가 02 : 조건부지정가 03 : 최유리지정가 04 : 최우선지정가 05 : 장전 시간외 06 : 장후 시간외 07 : 시간외 단일가 08 : 자기주식 09 : 자기주식S-Option 10 : 자기주식금전신탁 11 : IOC지정가 (즉시체결,잔량취소) 12 : FOK지정가 (즉시체결,전량취소) 13 : IOC시장가 (즉시체결,잔량취소) 14 : FOK시장가 (즉시체결,전량취소) 15 : IOC최유리 (즉시체결,잔량취소) 16 : FOK최유리 (즉시체결,전량취소)
        None,  # 7 ODER_COND 주문조건
        KisString["symbol"],  # 8 STCK_SHRN_ISCD 주식 단축 종목코드
        KisDecimal["executed_quantity"],  # 9 CNTG_QTY 체결 수량
        KisDecimal["price"],  # 10 CNTG_UNPR 체결단가
        KisTimeToDatetime("%H%M%S", timezone=TIMEZONE)["time"],  # 11 STCK_CNTG_HOUR 주식 체결 시간
        KisAny(lambda x: x == "1")["rejected"],  # 12 RFUS_YN 거부여부 0 : 승인 1 : 거부
        None,  # 13 CNTG_YN 체결여부 1 : 주문,정정,취소,거부 2 : 체결 (★ 체결만 보실경우 2번만 보시면 됩니다)
        None,  # 14 ACPT_YN 접수여부 1 : 주문접수 2 : 확인 3: 취소(FOK/IOC)
        None,  # 15 BRNC_NO 지점번호
        KisDecimal["quantity"],  # 16 ODER_QTY 주문수량
        None,  # 17 ACNT_NAME 계좌명
        None,  # 18 CNTG_ISNM 체결종목명
        None,  # 19 CRDT_CLS 신용구분
        None,  # 20 CRDT_LOAN_DATE 신용대출일자
        None,  # 21 CNTG_ISNM40 체결종목명40
        KisDecimal["unit_price"],  # 22 ODER_PRC 주문가격
    ]

    symbol: str  # 8 STCK_SHRN_ISCD 주식 단축 종목코드
    """종목코드"""
    market: "MARKET_TYPE" = "KRX"
    """상품유형타입"""

    account_number: KisAccountNumber  # 1 ACNT_NO 계좌번호
    """계좌번호"""

    time: datetime  # 11 STCK_CNTG_HOUR 주식 체결 시간
    """체결시각"""
    time_kst: datetime  # 11 STCK_CNTG_HOUR 주식 체결 시간
    """체결시각(KST)"""
    timezone: ZoneInfo = TIMEZONE
    """시간대"""

    order_number: KisOrderNumber  # 2 ODER_NO 주문번호, 15 BRNC_NO 지점번호
    """주문번호"""

    type: ORDER_TYPE  # 4 SELN_BYOV_CLS 매도매수구분
    """주문유형"""

    price: Decimal  # 10 CNTG_UNPR 체결단가
    """체결단가"""
    unit_price: Decimal | None  # 22 ODER_PRC 주문가격
    """주문단가"""

    quantity: ORDER_QUANTITY  # 16 ODER_QTY 주문수량
    """주문수량"""

    executed_quantity: ORDER_QUANTITY  # 9 CNTG_QTY 체결 수량
    """체결수량"""

    @property
    def executed_amount(self) -> Decimal:
        """체결금액"""
        return self.executed_quantity * (self.price or Decimal(0))

    condition: ORDER_CONDITION | None  # 6 ODER_KIND 주문종류
    """주문조건"""
    execution: ORDER_EXECUTION | None  # 6 ODER_KIND 주문종류
    """체결조건"""

    receipt: bool  # 14 ACPT_YN 접수여부
    """접수여부"""
    canceled: bool  # 14 ACPT_YN 접수여부
    """취소여부 (IOC/FOK)"""
    rejected: bool  # 12 RFUS_YN 거부여부
    """거부여부"""
    rejected_reason: str | None = None
    """거부사유"""

    _has_price: bool = True
    """주문단가 유무"""

    def __pre_init__(self, data: list[str]):
        super().__pre_init__(data)
        self._has_price, self.condition, self.execution = resolve_domestic_order_condition(data[6])

        self.canceled = data[14] == "3"
        self.receipt = data[14] == "1"

    def __post_init__(self):
        super().__post_init__()
        self.time_kst = self.time.astimezone(TIMEZONE)

        if not self._has_price:
            self.unit_price = None

        if self.receipt:
            self.quantity = self.executed_quantity
            self.executed_quantity = ORDER_QUANTITY(0)

    def __kis_post_init__(self):
        super().__kis_post_init__()

        self.order_number = KisSimpleOrder.from_order(
            kis=self.kis,
            symbol=self.symbol,
            market=self.market,
            account_number=self.account_number,
            branch=self.__data__[15],  # 지점번호
            number=self.__data__[2],  # 주문번호
            time_kst=self.time_kst,
        )


# 해외종목구분 4:홍콩(HKD) 5:상하이B(USD) 6:NASDAQ 7:NYSE 8:AMEX 9:OTCB C:홍콩(CNY) A:상하이A(CNY) B:심천B(HKD) D:도쿄 E:하노이 F:호치민
FOREIGN_MARKET_CODE_MAP: dict[str, "MARKET_TYPE"] = {
    "4": "HKEX",
    "5": "SSE",
    "6": "NASDAQ",
    "7": "NYSE",
    "8": "AMEX",
    "C": "HKEX",
    "A": "SSE",
    "B": "SZSE",
    "D": "TYO",
    "E": "HNX",
    "F": "HSX",
}

# 미국 4 일본 1 중국 3 홍콩 3 베트남 0
FOREIGN_DECIMAL_PLACES_MAP: dict[COUNTRY_TYPE, int] = {
    "US": 4,
    "JP": 1,
    "CN": 3,
    "HK": 3,
    "VN": 0,
}

# 주문종류2 1:시장가 2:지정자 6:단주시장가 7:단주지정가 A:MOO B:LOO C:MOC D:LOC
FOREIGN_ORDER_CONDITION_MAP: dict[str, tuple[bool, ORDER_CONDITION | None]] = {
    # (지정가여부, 주문조건)
    "1": (False, None),
    "2": (True, None),
    "6": (False, None),
    "7": (True, None),
    "A": (False, "MOO"),
    "B": (True, "LOO"),
    "C": (False, "MOC"),
    "D": (True, "LOC"),
}


class KisForeignRealtimeOrderExecution(KisRealtimeExecutionBase):
    """한국투자증권 해외주식 실시간 체결"""

    __fields__ = [
        None,  # 0 CUST_ID 고객 ID
        KisAny(KisAccountNumber)["account_number"],  # 1 ACNT_NO 계좌번호
        None,  # 2 ODER_NO 주문번호
        None,  # 3 OODER_NO 원주문번호
        KisAny(lambda x: "sell" if x == "01" else "buy")["type"],  # 4 SELN_BYOV_CLS 매도매수구분
        None,  # 5 RCTF_CLS 정정구분 0:정상 1:정정 2:취소
        None,  # 6 ODER_KIND2 주문종류2 1:시장가 2:지정자 6:단주시장가 7:단주지정가 A:MOO B:LOO C:MOC D:LOC
        KisString["symbol"],  # 7 STCK_SHRN_ISCD 주식 단축 종목코드
        KisDecimal["executed_quantity"],  # 8 CNTG_QTY 체결 수량
        KisDecimal[
            "price"
        ],  # 9 CNTG_UNPR 체결단가 ※ 체결단가의 경우, 국가에 따라 소수점 생략 위치가 상이합니다. 미국 4 일본 1 중국 3 홍콩 3 베트남 0 EX) 미국 AAPL(현재가 : 148.0100)의 경우 001480100으로 체결단가가 오는데, 4번째 자리에 소수점을 찍어 148.01로 해석하시면 됩니다.
        None,  # 10 STCK_CNTG_HOUR 주식 체결 시간 특정 거래소의 체결시간 데이터는 수신되지 않습니다. 체결시간 데이터가 필요할 경우, 체결통보 데이터 수신 시 타임스탬프를 찍는 것으로 대체하시길 바랍니다.
        KisAny(lambda x: x == "1")["rejected"],  # 11 RFUS_YN 거부여부 0:정상 1:거부
        None,  # 12 CNTG_YN 체결여부 1:주문,정정,취소,거부 2:체결
        None,  # 13 ACPT_YN 접수여부 1:주문접수 2:확인 3:취소(FOK/IOC)
        None,  # 14 BRNC_NO 지점번호
        KisDecimal[
            "quantity", Decimal(-1)
        ],  # 15 ODER_QTY 주문수량, 주문통보인 경우 해당 위치 미출력 (주문통보의 주문수량은 CNTG_QTY 위치에 출력). 체결통보인 경우 해당 위치에 주문수량이 출력
        None,  # 16 ACNT_NAME 계좌명
        None,  # 17 CNTG_ISNM 체결종목명
        KisAny(FOREIGN_MARKET_CODE_MAP.__getitem__)[
            "market"
        ],  # 18 ODER_COND 해외종목구분 4:홍콩(HKD) 5:상하이B(USD) 6:NASDAQ 7:NYSE 8:AMEX 9:OTCB C:홍콩(CNY) A:상하이A(CNY) B:심천B(HKD) D:도쿄 E:하노이 F:호치민
        None,  # 19 DEBT_GB 담보유형코드 10:현금 15:해외주식담보대출
        None,  # 20 DEBT_DATE 담보대출일자 대출일(YYYYMMDD)
    ]

    symbol: str  # 7 STCK_SHRN_ISCD 주식 단축 종목코드
    """종목코드"""
    market: "MARKET_TYPE"  # 18 ODER_COND 해외종목구분
    """상품유형타입"""

    account_number: KisAccountNumber  # 1 ACNT_NO 계좌번호
    """계좌번호"""

    time: datetime  # __post_init__에서 설정
    """체결시각"""
    time_kst: datetime  # __post_init__에서 설정
    """체결시각(KST)"""
    timezone: ZoneInfo  # __post_init__에서 설정
    """시간대"""

    order_number: KisOrderNumber  # 2 ODER_NO 주문번호, 14 BRNC_NO 지점번호
    """주문번호"""

    type: ORDER_TYPE  # 4 SELN_BYOV_CLS 매도매수구분
    """주문유형"""

    price: Decimal  # 9 CNTG_UNPR 체결단가, __post_init__에서 설정
    """체결단가"""
    unit_price: Decimal | None  # 9 CNTG_UNPR 체결단가, __post_init__에서 설정
    """주문단가"""

    quantity: ORDER_QUANTITY  # 15 ODER_QTY 주문수량
    """주문수량"""

    executed_quantity: ORDER_QUANTITY  # 8 CNTG_QTY 체결 수량
    """체결수량"""

    @property
    def executed_amount(self) -> Decimal:
        """체결금액"""
        return self.executed_quantity * (self.price or Decimal(0))

    condition: ORDER_CONDITION | None  # 6 ODER_KIND2 주문종류2, __post_init__에서 설정
    """주문조건"""
    execution: ORDER_EXECUTION | None = None
    """체결조건"""

    receipt: bool  # 13 ACPT_YN 접수여부
    """접수여부"""

    canceled: bool  # 13 ACPT_YN 접수여부
    """취소여부 (IOC/FOK)"""
    rejected: bool  # 11 RFUS_YN 거부여부
    """거부여부"""
    rejected_reason: str | None = None
    """거부사유"""

    def __pre_init__(self, data: list[str]):
        super().__pre_init__(data)

        self.canceled = data[13] == "3"
        self.receipt = data[13] == "1"

    def __post_init__(self):
        super().__post_init__()
        has_price, self.condition = FOREIGN_ORDER_CONDITION_MAP[self.__data__[6]]
        self.price = self.price * Decimal(f"1e-{FOREIGN_DECIMAL_PLACES_MAP[get_market_country(self.market)]}")
        self.unit_price = self.price if has_price else None
        self.time_kst = datetime.now(TIMEZONE)
        self.timezone = get_market_timezone(self.market)
        self.time = self.time_kst.astimezone(self.timezone)

        if self.quantity < 0:
            self.quantity = self.executed_quantity

        if self.receipt:
            self.quantity = self.executed_quantity
            self.executed_quantity = ORDER_QUANTITY(0)

    def __kis_post_init__(self):
        super().__kis_post_init__()

        self.order_number = KisSimpleOrder.from_order(
            kis=self.kis,
            symbol=self.symbol,
            market=self.market,
            account_number=self.account_number,
            branch=self.__data__[14],  # 지점번호
            number=self.__data__[2],  # 주문번호
            time_kst=self.time_kst,
        )


# IDE Type Checker
if TYPE_CHECKING:
    Checkable[KisRealtimeExecution](KisDomesticRealtimeOrderExecution)
    Checkable[KisRealtimeExecution](KisForeignRealtimeOrderExecution)


def on_execution(
    self: "KisWebsocketClient",
    callback: Callable[["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimeExecution]], None],
    where: KisEventFilter["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimeExecution]] | None = None,
    once: bool = False,
) -> KisEventTicket["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimeExecution]]:
    """
    웹소켓 이벤트 핸들러 등록

    [국내주식] 실시간시세 -> 국내주식 실시간체결통보[실시간-005]
    [해외주식] 실시간시세 -> 해외주식 실시간체결통보[실시간-009]

    Args:
        callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]], None]): 콜백 함수
        where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]] | None, optional): 이벤트 필터. Defaults to None.
        once (bool, optional): 한번만 실행 여부. Defaults to False.
    """
    appkey = self.kis.virtual_appkey if self.kis.virtual else self.kis.appkey

    if appkey is None:
        raise ValueError("모의도메인 appkey가 없습니다.")

    domestic = self.on(
        id="H0STCNI9" if self.kis.virtual else "H0STCNI0",
        key=appkey.id,
        callback=callback,
        where=where,
        once=once,
        primary=True,
    )

    foreign = self.on(
        id="H0GSCNI9" if self.kis.virtual else "H0GSCNI0",
        key=appkey.id,
        callback=callback,
        where=where,
        once=once,
        primary=True,
    )

    domestic.unsubscribed_callbacks.append(lambda _: foreign.unsubscribe())

    return domestic


def on_account_execution(
    self: "KisAccountProtocol",
    callback: Callable[["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimeExecution]], None],
    where: KisEventFilter["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimeExecution]] | None = None,
    once: bool = False,
) -> KisEventTicket["KisWebsocketClient", KisSubscriptionEventArgs[KisRealtimeExecution]]:
    """
    웹소켓 이벤트 핸들러 등록

    [국내주식] 실시간시세 -> 국내주식 실시간체결통보[실시간-005]
    [해외주식] 실시간시세 -> 해외주식 실시간체결통보[실시간-009]

    Args:
        callback (Callable[[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]], None]): 콜백 함수
        where (KisEventFilter[KisWebsocketClient, KisSubscriptionEventArgs[KisRealtimeExecution]] | None, optional): 이벤트 필터. Defaults to None.
        once (bool, optional): 한번만 실행 여부. Defaults to False.
    """
    return on_execution(
        self.kis.websocket,
        callback=callback,
        where=where,
        once=once,
    )
