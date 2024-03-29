from datetime import datetime, tzinfo
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Literal, get_args

from pykis.__env__ import TIMEZONE
from pykis.api.base.account_product import KisAccountProductBase
from pykis.api.stock.market import (
    DAYTIME_MARKET_SHORT_TYPE_MAP,
    MARKET_TIMEZONE_OBJECT_MAP,
    MARKET_TYPE,
    MARKET_TYPE_KOR_MAP,
)
from pykis.api.stock.quote import quote
from pykis.client.account import KisAccountNumber
from pykis.responses.dynamic import KisDynamic
from pykis.responses.exception import KisMarketNotOpenedError
from pykis.responses.response import KisAPIResponse, raise_not_found
from pykis.responses.types import KisString

if TYPE_CHECKING:
    from pykis.kis import PyKis

ORDER_TYPE = Literal["buy", "sell"]
"""주문 종류"""

ORDER_PRICE = Decimal | int | float
"""주문 가격"""


def ensure_price(price: ORDER_PRICE, digit: int | None = 4) -> Decimal:
    """
    주문 가격을 Decimal로 변환합니다.

    Args:
        price (ORDER_PRICE): 주문 가격
        digit (int | None, optional): 소수점 자릿수 (내림)
    """
    if not isinstance(price, Decimal):
        price = Decimal(price)

    if digit is not None:
        price = price.quantize(Decimal(f"1e{-digit}"))

    return price


ORDER_EXECUTION_CONDITION = Literal["IOC", "FOK"]
"""체결 조건 (IOC, FOK)"""

DOMESTIC_ORDER_CONDITION = Literal[
    # 조건부지정가
    "condition",
    # 최유리지정가
    "best",
    # 최우선지정가
    "priority",
    # 시간외단일가
    "extended",
    # 장전시간외
    "before",
    # 장후시간외
    "after",
]

OVERSEAS_ORDER_CONDITION = Literal[
    # 장개시지정가
    "LOO",
    # 장마감지정가
    "LOC",
    # 장개시시장가
    "MOO",
    # 장마감시장가
    "MOC",
    # 주간거래
    "extended",
]

ORDER_CONDITION = DOMESTIC_ORDER_CONDITION | OVERSEAS_ORDER_CONDITION
"""주문 조건"""


def to_domestic_order_condition(condition: ORDER_CONDITION) -> DOMESTIC_ORDER_CONDITION:
    if condition in get_args(DOMESTIC_ORDER_CONDITION):
        return condition  # type: ignore

    raise ValueError(f"주문 조건이 국내 주문 조건이 아닙니다. ({condition!r})")


def to_overseas_order_condition(condition: ORDER_CONDITION) -> OVERSEAS_ORDER_CONDITION:
    if condition in get_args(OVERSEAS_ORDER_CONDITION):
        return condition  # type: ignore

    raise ValueError(f"주문 조건이 해외 주문 조건이 아닙니다. ({condition!r})")


DOMESTIC_ORDER_CONDITION_KOR_MAP: dict[DOMESTIC_ORDER_CONDITION, str] = {
    "condition": "조건부지정가",
    "best": "최유리지정가",
    "priority": "최우선지정가",
    "extended": "시간외단일가",
    "before": "장전시간외",
    "after": "장후시간외",
}
"""국내 주문 조건 한글 매핑"""

ORDER_CONDITION_MAP: dict[
    tuple[
        bool | None,
        MARKET_TYPE | None,
        ORDER_TYPE,
        bool,
        ORDER_CONDITION | None,
        ORDER_EXECUTION_CONDITION | None,
    ],
    tuple[str, Literal["lower", "upper"] | None, str],
] = {
    # (실전투자여부, 시장, 주문종류, 단가, 주문조건, 체결조건): (주문구분코드, 지정단가설정, 주문구분한글명)
    # 기본
    (None, None, "buy", True, None, None): ("00", None, "지정가"),
    (None, None, "buy", False, None, None): ("00", "upper", "시장가"),
    (None, None, "sell", True, None, None): ("00", None, "지정가"),
    (None, None, "sell", False, None, None): ("00", "lower", "시장가"),
    # 국내
    (None, "KRX", "buy", True, None, None): ("00", None, "지정가"),
    (None, "KRX", "buy", False, None, None): ("01", None, "시장가"),
    (None, "KRX", "buy", True, "condition", None): ("02", None, "조건부지정가"),
    (None, "KRX", "buy", True, "best", None): ("03", None, "최유리지정가"),
    (None, "KRX", "buy", True, "priority", None): ("04", None, "최우선지정가"),
    (True, "KRX", "buy", True, "extended", None): ("07", None, "시간외단일가"),
    (True, "KRX", "buy", False, "before", None): ("05", None, "장전시간외"),
    (True, "KRX", "buy", False, "after", None): ("06", None, "장후시간외"),
    (True, "KRX", "buy", True, None, "IOC"): ("11", None, "IOC지정가"),
    (True, "KRX", "buy", True, None, "FOK"): ("12", None, "FOK지정가"),
    (True, "KRX", "buy", False, None, "IOC"): ("13", None, "IOC시장가"),
    (True, "KRX", "buy", False, None, "FOK"): ("14", None, "FOK시장가"),
    (True, "KRX", "buy", True, "best", "IOC"): ("15", None, "IOC최유리"),
    (True, "KRX", "buy", True, "best", "FOK"): ("16", None, "FOK최유리"),
    (None, "KRX", "sell", True, None, None): ("00", None, "지정가"),
    (None, "KRX", "sell", False, None, None): ("01", None, "시장가"),
    (None, "KRX", "sell", True, "condition", None): ("02", None, "조건부지정가"),
    (None, "KRX", "sell", True, "best", None): ("03", None, "최유리지정가"),
    (None, "KRX", "sell", True, "priority", None): ("04", None, "최우선지정가"),
    (True, "KRX", "sell", True, "extended", None): ("07", None, "시간외단일가"),
    (True, "KRX", "sell", False, "before", None): ("05", None, "장전시간외"),
    (True, "KRX", "sell", False, "after", None): ("06", None, "장후시간외"),
    (True, "KRX", "sell", True, None, "IOC"): ("11", None, "IOC지정가"),
    (True, "KRX", "sell", True, None, "FOK"): ("12", None, "FOK지정가"),
    (True, "KRX", "sell", False, None, "IOC"): ("13", None, "IOC시장가"),
    (True, "KRX", "sell", False, None, "FOK"): ("14", None, "FOK시장가"),
    (True, "KRX", "sell", True, "best", "IOC"): ("15", None, "IOC최유리"),
    (True, "KRX", "sell", True, "best", "FOK"): ("16", None, "FOK최유리"),
    # 나스닥
    (True, "NASD", "buy", True, "LOO", None): ("32", None, "장개시지정가"),
    (True, "NASD", "buy", True, "LOC", None): ("34", None, "장마감지정가"),
    (True, "NASD", "buy", False, "MOO", None): ("32", "upper", "장개시시장가"),
    (True, "NASD", "buy", False, "MOC", None): ("34", "upper", "장마감시장가"),
    # 뉴욕
    (True, "NYSE", "buy", True, "LOO", None): ("32", None, "장개시지정가"),
    (True, "NYSE", "buy", True, "LOC", None): ("34", None, "장마감지정가"),
    (True, "NYSE", "buy", False, "MOO", None): ("32", "upper", "장개시시장가"),
    (True, "NYSE", "buy", False, "MOC", None): ("34", "upper", "장마감시장가"),
    # 아멕스
    (True, "AMEX", "buy", True, "LOO", None): ("32", None, "장개시지정가"),
    (True, "AMEX", "buy", True, "LOC", None): ("34", None, "장마감지정가"),
    (True, "AMEX", "buy", False, "MOO", None): ("32", "upper", "장개시시장가"),
    (True, "AMEX", "buy", False, "MOC", None): ("34", "upper", "장마감시장가"),
    # 나스닥
    (True, "NASD", "sell", True, "LOO", None): ("32", None, "장개시지정가"),
    (True, "NASD", "sell", True, "LOC", None): ("34", None, "장마감지정가"),
    (True, "NASD", "sell", False, "MOO", None): ("31", None, "장개시시장가"),
    (True, "NASD", "sell", False, "MOC", None): ("33", None, "장마감시장가"),
    # 뉴욕
    (True, "NYSE", "sell", True, "LOO", None): ("32", None, "장개시지정가"),
    (True, "NYSE", "sell", True, "LOC", None): ("34", None, "장마감지정가"),
    (True, "NYSE", "sell", False, "MOO", None): ("31", None, "장개시시장가"),
    (True, "NYSE", "sell", False, "MOC", None): ("33", None, "장마감시장가"),
    # 아멕스
    (True, "AMEX", "sell", True, "LOO", None): ("32", None, "장개시지정가"),
    (True, "AMEX", "sell", True, "LOC", None): ("34", None, "장마감지정가"),
    (True, "AMEX", "sell", False, "MOO", None): ("31", None, "장개시시장가"),
    (True, "AMEX", "sell", False, "MOC", None): ("33", None, "장마감시장가"),
}


def orderable_conditions_repr():
    return "\n".join(
        (
            f"order(market={repr(market) if market else '전체'}, order={order!r}, price={'100' if price else 'None'}, condition={condition!r}, execution={execution!r}) "
            f"# {MARKET_TYPE_KOR_MAP[market]} {label} {'매수' if order == 'buy' else '매도'}{'' if ((False, market, order, price, condition, execution) in ORDER_CONDITION_MAP) or (None, market, order, price, condition, execution) in ORDER_CONDITION_MAP else ' (모의투자 미지원)'}"
        )
        for (real, market, order, price, condition, execution), (
            _,
            _,
            label,
        ) in ORDER_CONDITION_MAP.items()
        if real is not False
    )


def order_condition(
    virtual: bool,
    market: MARKET_TYPE,
    order: ORDER_TYPE,
    price: Decimal | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION_CONDITION | None = None,
):
    if price and price <= 0:
        raise ValueError("가격은 0보다 커야합니다.")

    order_condition = [not virtual, market, order, price is not None, condition, execution]

    if tuple(order_condition) not in ORDER_CONDITION_MAP:
        # 조건을 찾을 수 없을 경우, 투자구분을 기본값으로 변환
        order_condition[0] = None

    if tuple(order_condition) not in ORDER_CONDITION_MAP:
        # 조건을 찾을 수 없을 경우, 시장을 기본값으로 변환
        order_condition[1] = None

    if order_condition[3] and tuple(order_condition) not in ORDER_CONDITION_MAP:
        # 조건을 찾을 수 없을 경우, 단가를 시장가로 변환
        order_condition[3] = False

    if tuple(order_condition) not in ORDER_CONDITION_MAP:
        # 모의투자 미지원 여부 확인
        virtual_not_supported = False

        if virtual:
            order_condition[0] = False

            if tuple(order_condition) in ORDER_CONDITION_MAP:
                virtual_not_supported = True

        raise ValueError(
            (
                "모의투자는 해당 주문조건을 지원하지 않습니다."
                if virtual_not_supported
                else "주문조건이 잘못되었습니다."
            )
            + f" (market={market!r}, order={order!r}, price={price!r}, condition={condition!r}, execution={execution!r})\n"
            "아래 주문 가능 조건을 참고하세요.\n\n" + orderable_conditions_repr()
        )

    return ORDER_CONDITION_MAP[tuple(order_condition)]  # type: ignore


class KisOrderNumber(KisDynamic, KisAccountProductBase):
    """한국투자증권 주문번호"""

    branch: str
    """지점코드"""
    number: str
    """주문번호"""

    def __repr__(self) -> str:
        return f"KisOrderNumber(account_number={self.account_number!r}, code={self.code!r}, market={self.market!r}, branch={self.branch!r}, number={self.number!r})"


class KisOrder(KisOrderNumber):
    """한국투자증권 주문"""

    time: datetime
    """주문시간 (현지시간)"""
    time_kst: datetime
    """주문시간 (한국시간)"""
    timezone: tzinfo
    """시간대"""

    def __init__(self, account_number: KisAccountNumber, code: str, market: MARKET_TYPE):
        self.account_number = account_number
        self.code = code
        self.market = market
        self.timezone = MARKET_TIMEZONE_OBJECT_MAP[self.market]


class KisDomesticOrder(KisAPIResponse, KisOrder):
    """한국투자증권 국내주식 주문"""

    branch: str = KisString["KRX_FWDG_ORD_ORGNO"]
    """지점코드"""
    number: str = KisString["ODNO"]
    """주문번호"""
    time: datetime
    """주문시간 (현지시간)"""
    time_kst: datetime
    """주문시간 (한국시간)"""

    def __pre_init__(self, data: dict[str, Any]):
        if data["msg_cd"] == "APBK0919":
            raise KisMarketNotOpenedError(
                data=data,
                response=data["__response__"],
            )

        if data["msg_cd"] == "APBK0656":
            raise_not_found(
                data,
                code=self.code,
                market=self.market,
            )

        super().__pre_init__(data)

        self.time_kst = self.time = datetime.combine(
            datetime.now(TIMEZONE).date(),
            datetime.strptime(data["output"]["ORD_TMD"], "%H%M%S").time(),
            tzinfo=TIMEZONE,
        )


class KisOverseasOrder(KisAPIResponse, KisOrder):
    """한국투자증권 해외주식 주문"""

    branch: str = KisString["KRX_FWDG_ORD_ORGNO"]
    """지점코드"""
    number: str = KisString["ODNO"]
    """주문번호"""
    time: datetime
    """주문시간 (현지시간)"""
    time_kst: datetime
    """주문시간 (한국시간)"""

    def __pre_init__(self, data: dict[str, Any]):
        if data["msg_cd"] == "APBK1664":
            raise KisMarketNotOpenedError(
                data=data,
                response=data["__response__"],
            )

        if data["msg_cd"] == "APBK0656":
            raise_not_found(
                data,
                code=self.code,
                market=self.market,
            )

        super().__pre_init__(data)

        self.time_kst = datetime.combine(
            datetime.now(TIMEZONE).date(),
            datetime.strptime(data["output"]["ORD_TMD"], "%H%M%S").time(),
            tzinfo=TIMEZONE,
        )
        self.time = self.time_kst.astimezone(self.timezone)


class KisOverseasDaytimeOrder(KisAPIResponse, KisOrder):
    """한국투자증권 해외주식 주문 (주간)"""

    branch: str = KisString["KRX_FWDG_ORD_ORGNO"]
    """지점코드"""
    number: str = KisString["ODNO"]
    """주문번호"""
    time: datetime
    """주문시간 (현지시간)"""
    time_kst: datetime
    """주문시간 (한국시간)"""

    def __pre_init__(self, data: dict[str, Any]):
        if data["msg_cd"] == "APBK1664":
            raise KisMarketNotOpenedError(
                data=data,
                response=data["__response__"],
            )

        if data["msg_cd"] == "APBK0656":
            raise_not_found(
                data,
                code=self.code,
                market=self.market,
            )

        super().__pre_init__(data)

        self.time_kst = datetime.combine(
            datetime.now(TIMEZONE).date(),
            datetime.strptime(data["output"]["ORD_TMD"], "%H%M%S").time(),
            tzinfo=TIMEZONE,
        )
        self.time = self.time_kst.astimezone(self.timezone)


DOMESTIC_ORDER_API_CODES: dict[tuple[bool, ORDER_TYPE], str] = {
    # (실전투자여부, 주문종류): API코드
    (True, "buy"): "TTTC0802U",
    (True, "sell"): "TTTC0801U",
    (False, "buy"): "VTTC0802U",
    (False, "sell"): "VTTC0801U",
}


def domestic_order(
    self: "PyKis",
    account: str | KisAccountNumber,
    code: str,
    order: ORDER_TYPE = "buy",
    price: ORDER_PRICE | None = None,
    qty: Decimal | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION_CONDITION | None = None,
    include_foreign: bool = False,
) -> KisDomesticOrder:
    """
    한국투자증권 국내 주식 주문

    국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
    (업데이트 날짜: 2024/03/24)

    Args:
        account (str | KisAccountNumber): 계좌번호
        code (str): 종목코드
        order (ORDER_TYPE, optional): 주문종류
        price (ORDER_PRICE, optional): 주문가격
        qty (Decimal, optional): 주문수량
        condition (ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
        include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부

    Examples:
        >>> domestic_order(account, code, order='buy', price=100, condition=None, execution=None) # 지정가 매수
        >>> domestic_order(account, code, order='buy', price=None, condition=None, execution=None) # 시장가 매수
        >>> domestic_order(account, code, order='buy', price=100, condition='condition', execution=None) # 조건부지정가 매수
        >>> domestic_order(account, code, order='buy', price=100, condition='best', execution=None) # 최유리지정가 매수
        >>> domestic_order(account, code, order='buy', price=100, condition='priority', execution=None) # 최우선지정가 매수
        >>> domestic_order(account, code, order='buy', price=100, condition='extended', execution=None) # 시간외단일가 매수 (모의투자 미지원)
        >>> domestic_order(account, code, order='buy', price=None, condition='before', execution=None) # 장전시간외 매수 (모의투자 미지원)
        >>> domestic_order(account, code, order='buy', price=None, condition='after', execution=None) # 장후시간외 매수 (모의투자 미지원)
        >>> domestic_order(account, code, order='buy', price=100, condition=None, execution='IOC') # IOC지정가 매수
        >>> domestic_order(account, code, order='buy', price=100, condition=None, execution='FOK') # FOK지정가 매수
        >>> domestic_order(account, code, order='buy', price=None, condition=None, execution='IOC') # IOC시장가 매수
        >>> domestic_order(account, code, order='buy', price=None, condition=None, execution='FOK') # FOK시장가 매수
        >>> domestic_order(account, code, order='buy', price=100, condition='best', execution='IOC') # IOC최유리 매수
        >>> domestic_order(account, code, order='buy', price=100, condition='best', execution='FOK') # FOK최유리 매수
        >>> domestic_order(account, code, order='sell', price=100, condition=None, execution=None) # 지정가 매도
        >>> domestic_order(account, code, order='sell', price=None, condition=None, execution=None) # 시장가 매도
        >>> domestic_order(account, code, order='sell', price=100, condition='condition', execution=None) # 조건부지정가 매도
        >>> domestic_order(account, code, order='sell', price=100, condition='best', execution=None) # 최유리지정가 매도
        >>> domestic_order(account, code, order='sell', price=100, condition='priority', execution=None) # 최우선지정가 매도
        >>> domestic_order(account, code, order='sell', price=100, condition='extended', execution=None) # 시간외단일가 매도 (모의투자 미지원)
        >>> domestic_order(account, code, order='sell', price=None, condition='before', execution=None) # 장전시간외 매도 (모의투자 미지원)
        >>> domestic_order(account, code, order='sell', price=None, condition='after', execution=None) # 장후시간외 매도
        >>> domestic_order(account, code, order='sell', price=100, condition=None, execution='IOC') # IOC지정가 매도 (모의투자 미지원)
        >>> domestic_order(account, code, order='sell', price=100, condition=None, execution='FOK') # FOK지정가 매도 (모의투자 미지원)
        >>> domestic_order(account, code, order='sell', price=None, condition=None, execution='IOC') # IOC시장가 매도 (모의투자 미지원)
        >>> domestic_order(account, code, order='sell', price=None, condition=None, execution='FOK') # FOK시장가 매도 (모의투자 미지원)
        >>> domestic_order(account, code, order='sell', price=100, condition='best', execution='IOC') # IOC최유리 매도 (모의투자 미지원)
        >>> domestic_order(account, code, order='sell', price=100, condition='best', execution='FOK') # FOK최유리 매도 (모의투자 미지원)

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        KisMarketNotOpenedError: 시장이 열리지 않은 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    if not account:
        raise ValueError("계좌번호를 입력해주세요.")

    if not code:
        raise ValueError("종목코드를 입력해주세요.")

    if qty != None and qty <= 0:
        raise ValueError("수량은 0보다 커야합니다.")

    price = None if price is None else ensure_price(price, 0)

    condition_code, price_setting, _ = order_condition(
        virtual=self.virtual,
        market="KRX",
        order=order,
        price=price,
        condition=condition,
        execution=execution,
    )

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    if price_setting:
        quote_data = quote(self, code=code, market="KRX")
        price = quote_data.high_limit if price_setting == "upper" else quote_data.low_limit

    if qty is None:
        from pykis.api.account.orderable_amount import orderable_amount

        amount = orderable_amount(
            self,
            account=account,
            market="KRX",
            code=code,
            price=None if price_setting else price,
            condition=condition,
            execution=execution,
        )

        if include_foreign:
            qty = amount.foreign_qty
        else:
            qty = amount.qty

        if qty <= 0:
            raise ValueError("주문가능수량이 없습니다.")

    return self.fetch(
        "/uapi/domestic-stock/v1/trading/order-cash",
        api=DOMESTIC_ORDER_API_CODES[(not self.virtual, order)],
        body={
            "PDNO": code,
            "ORD_DVSN": condition_code,
            "ORD_QTY": str(int(qty)),
            "ORD_UNPR": str(price or 0),
        },
        form=[account],
        response_type=KisDomesticOrder(
            account_number=account,
            code=code,
            market="KRX",
        ),
        method="POST",
    )


OVERSEAS_ORDER_API_CODES: dict[tuple[bool, MARKET_TYPE, ORDER_TYPE], str] = {
    # (실전투자여부, 시장, 주문종류): API코드
    (True, "NASD", "buy"): "TTTT1002U",  # 미국 매수 주문
    (True, "NYSE", "buy"): "TTTT1002U",  # 미국 매수 주문
    (True, "AMEX", "buy"): "TTTT1002U",  # 미국 매수 주문
    (True, "NASD", "sell"): "TTTT1006U",  # 미국 매도 주문
    (True, "NYSE", "sell"): "TTTT1006U",  # 미국 매도 주문
    (True, "AMEX", "sell"): "TTTT1006U",  # 미국 매도 주문
    (True, "TKSE", "buy"): "TTTS0308U",  # 일본 매수 주문
    (True, "TKSE", "sell"): "TTTS0307U",  # 일본 매도 주문
    (True, "SHAA", "buy"): "TTTS0202U",  # 상해 매수 주문
    (True, "SHAA", "sell"): "TTTS1005U",  # 상해 매도 주문
    (True, "SEHK", "buy"): "TTTS1002U",  # 홍콩 매수 주문
    (True, "SEHK", "sell"): "TTTS1001U",  # 홍콩 매도 주문
    (True, "SZAA", "buy"): "TTTS0305U",  # 심천 매수 주문
    (True, "SZAA", "sell"): "TTTS0304U",  # 심천 매도 주문
    (True, "HASE", "buy"): "TTTS0311U",  # 베트남 매수 주문
    (True, "VNSE", "buy"): "TTTS0311U",  # 베트남 매수 주문
    (True, "HASE", "sell"): "TTTS0310U",  # 베트남 매도 주문
    (True, "VNSE", "sell"): "TTTS0310U",  # 베트남 매도 주문
    (False, "NASD", "buy"): "VTTT1002U",  # 미국 매수 주문
    (False, "NYSE", "buy"): "VTTT1002U",  # 미국 매수 주문
    (False, "AMEX", "buy"): "VTTT1002U",  # 미국 매수 주문
    (False, "NASD", "sell"): "VTTT1001U",  # 미국 매도 주문
    (False, "NYSE", "sell"): "VTTT1001U",  # 미국 매도 주문
    (False, "AMEX", "sell"): "VTTT1001U",  # 미국 매도 주문
    (False, "TKSE", "buy"): "VTTS0308U",  # 일본 매수 주문
    (False, "TKSE", "sell"): "VTTS0307U",  # 일본 매도 주문
    (False, "SHAA", "buy"): "VTTS0202U",  # 상해 매수 주문
    (False, "SHAA", "sell"): "VTTS1005U",  # 상해 매도 주문
    (False, "SEHK", "buy"): "VTTS1002U",  # 홍콩 매수 주문
    (False, "SEHK", "sell"): "VTTS1001U",  # 홍콩 매도 주문
    (False, "SZAA", "buy"): "VTTS0305U",  # 심천 매수 주문
    (False, "SZAA", "sell"): "VTTS0304U",  # 심천 매도 주문
    (False, "HASE", "buy"): "VTTS0311U",  # 베트남 매수 주문
    (False, "VNSE", "buy"): "VTTS0311U",  # 베트남 매수 주문
    (False, "HASE", "sell"): "VTTS0310U",  # 베트남 매도 주문
    (False, "VNSE", "sell"): "VTTS0310U",  # 베트남 매도 주문
}


def overseas_order(
    self: "PyKis",
    account: str | KisAccountNumber,
    market: MARKET_TYPE,
    code: str,
    order: ORDER_TYPE = "buy",
    price: ORDER_PRICE | None = None,
    qty: Decimal | None = None,
    condition: OVERSEAS_ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION_CONDITION | None = None,
    include_foreign: bool = False,
) -> KisOverseasOrder:
    """
    한국투자증권 해외 주식 주문

    해외주식주문 -> 해외주식 주문[v1_해외주식-001]
    (업데이트 날짜: 2024/03/24)

    Args:
        account (str | KisAccountNumber): 계좌번호
        market (MARKET_TYPE): 시장
        code (str): 종목코드
        order (ORDER_TYPE, optional): 주문종류
        price (ORDER_PRICE, optional): 주문가격
        qty (Decimal, optional): 주문수량
        condition (DOMESTIC_ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
        include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부

    Examples:
        >>> overseas_order(account, 전체, code, order='buy', price=100, condition=None, execution=None) # 전체 지정가 매수
        >>> overseas_order(account, 전체, code, order='buy', price=None, condition=None, execution=None) # 전체 시장가 매수
        >>> overseas_order(account, 전체, code, order='sell', price=100, condition=None, execution=None) # 전체 지정가 매도
        >>> overseas_order(account, 전체, code, order='sell', price=None, condition=None, execution=None) # 전체 시장가 매도
        >>> overseas_order(account, 'NASD', code, order='buy', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
        >>> overseas_order(account, 'NASD', code, order='buy', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
        >>> overseas_order(account, 'NASD', code, order='buy', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
        >>> overseas_order(account, 'NASD', code, order='buy', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
        >>> overseas_order(account, 'NYSE', code, order='buy', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
        >>> overseas_order(account, 'NYSE', code, order='buy', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
        >>> overseas_order(account, 'NYSE', code, order='buy', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
        >>> overseas_order(account, 'NYSE', code, order='buy', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
        >>> overseas_order(account, 'AMEX', code, order='buy', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
        >>> overseas_order(account, 'AMEX', code, order='buy', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
        >>> overseas_order(account, 'AMEX', code, order='buy', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
        >>> overseas_order(account, 'AMEX', code, order='buy', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
        >>> overseas_order(account, 'NASD', code, order='sell', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매도 (모의투자 미지원)
        >>> overseas_order(account, 'NASD', code, order='sell', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매도 (모의투자 미지원)
        >>> overseas_order(account, 'NASD', code, order='sell', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매도 (모의투자 미지원)
        >>> overseas_order(account, 'NASD', code, order='sell', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매도 (모의투자 미지원)
        >>> overseas_order(account, 'NYSE', code, order='sell', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매도 (모의투자 미지원)
        >>> overseas_order(account, 'NYSE', code, order='sell', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매도 (모의투자 미지원)
        >>> overseas_order(account, 'NYSE', code, order='sell', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매도 (모의투자 미지원)
        >>> overseas_order(account, 'NYSE', code, order='sell', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매도 (모의투자 미지원)
        >>> overseas_order(account, 'AMEX', code, order='sell', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매도 (모의투자 미지원)
        >>> overseas_order(account, 'AMEX', code, order='sell', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매도 (모의투자 미지원)
        >>> overseas_order(account, 'AMEX', code, order='sell', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매도 (모의투자 미지원)
        >>> overseas_order(account, 'AMEX', code, order='sell', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매도 (모의투자 미지원)

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        KisMarketNotOpenedError: 시장이 열리지 않은 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    if not account:
        raise ValueError("계좌번호를 입력해주세요.")

    if not market:
        raise ValueError("시장을 입력해주세요.")

    if not code:
        raise ValueError("종목코드를 입력해주세요.")

    if qty != None and qty <= 0:
        raise ValueError("수량은 0보다 커야합니다.")

    price = None if price is None else ensure_price(price)

    condition_code, price_setting, _ = order_condition(
        virtual=self.virtual,
        market=market,
        order=order,
        price=price,
        condition=condition,
        execution=execution,
    )

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    if qty is None:
        from pykis.api.account.orderable_amount import orderable_amount

        amount = orderable_amount(
            self,
            account=account,
            market=market,
            code=code,
            price=price,
            condition=condition,
            execution=execution,
        )

        if include_foreign:
            qty = amount.foreign_qty
        else:
            qty = amount.qty

        if qty <= 0:
            raise ValueError("주문가능수량이 없습니다.")

    if price_setting:
        quote_data = quote(self, code=code, market="KRX")
        price = quote_data.high_limit if price_setting == "upper" else quote_data.low_limit

    return self.fetch(
        "/uapi/overseas-stock/v1/trading/order",
        api=OVERSEAS_ORDER_API_CODES[(not self.virtual, market, order)],
        body={
            "OVRS_EXCG_CD": market,
            "PDNO": code,
            "ORD_QTY": str(int(qty)),
            "OVRS_ORD_UNPR": str(price or 0),
            "SLL_TYPE": "00" if order == "sell" else "",
            "ORD_SVR_DVSN_CD": "0",
            "ORD_DVSN": condition_code,
        },
        form=[account],
        response_type=KisOverseasOrder(
            account_number=account,
            code=code,
            market=market,
        ),
        method="POST",
    )


def overseas_daytime_order(
    self: "PyKis",
    account: str | KisAccountNumber,
    market: MARKET_TYPE,
    code: str,
    order: ORDER_TYPE = "buy",
    price: ORDER_PRICE | None = None,
    qty: Decimal | None = None,
    include_foreign: bool = False,
) -> KisOverseasDaytimeOrder:
    """
    한국투자증권 해외주식 주간거래 주문 (주간, 모의투자 미지원)

    해외주식주문 -> 해외주식 미국주간주문[v1_해외주식-026]
    (업데이트 날짜: 2024/03/25)

    Args:
        account (str | KisAccountNumber): 계좌번호
        market (MARKET_TYPE): 시장
        code (str): 종목코드
        order (ORDER_TYPE, optional): 주문종류
        price (ORDER_PRICE, optional): 주문가격
        qty (Decimal, optional): 주문수량
        include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부
    """
    if self.virtual:
        raise NotImplementedError("주간거래 주문은 모의투자를 지원하지 않습니다.")

    if market not in DAYTIME_MARKET_SHORT_TYPE_MAP:
        raise ValueError(f"주간거래가 지원되지 않는 시장입니다. ({market})")

    if not account:
        raise ValueError("계좌번호를 입력해주세요.")

    if not market:
        raise ValueError("시장을 입력해주세요.")

    if not code:
        raise ValueError("종목코드를 입력해주세요.")

    if qty != None and qty <= 0:
        raise ValueError("수량은 0보다 커야합니다.")

    price = None if price is None else ensure_price(price)

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    if qty is None:
        from pykis.api.account.orderable_amount import orderable_amount

        amount = orderable_amount(
            self,
            account=account,
            market=market,
            code=code,
            price=price,
            condition="extended",
        )

        if include_foreign:
            qty = amount.foreign_qty
        else:
            qty = amount.qty

        price = amount.unit_price

        if qty <= 0:
            raise ValueError("주문가능수량이 없습니다.")

    if not price:
        quote_data = quote(self, code=code, market=market, extended=True)
        price = quote_data.high_limit if order == "buy" else quote_data.low_limit

    return self.fetch(
        "/uapi/overseas-stock/v1/trading/daytime-order",
        api="TTTS6036U" if order == "buy" else "TTTS6037U",
        body={
            "OVRS_EXCG_CD": market,
            "PDNO": code,
            "ORD_QTY": str(int(qty)),
            "OVRS_ORD_UNPR": str(price),
            "ORD_SVR_DVSN_CD": "0",
            "ORD_DVSN": "00",
        },
        form=[account],
        response_type=KisOverseasDaytimeOrder(
            account_number=account,
            code=code,
            market=market,
        ),
        method="POST",
        domain="real",
    )


def order(
    self: "PyKis",
    account: str | KisAccountNumber,
    market: MARKET_TYPE,
    code: str,
    order: ORDER_TYPE,
    price: ORDER_PRICE | None = None,
    qty: Decimal | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION_CONDITION | None = None,
    include_foreign: bool = False,
) -> KisOrder:
    """
    한국투자증권 통합주식 주문

    국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
    해외주식주문 -> 해외주식 주문[v1_해외주식-001]

    Args:
        account (str | KisAccountNumber): 계좌번호
        code (str): 종목코드
        order (ORDER_TYPE): 주문종류
        price (ORDER_PRICE, optional): 주문가격
        qty (Decimal, optional): 주문수량
        condition (DOMESTIC_ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
        include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부

    Examples:
        >>> order(account, 전체, code, order='buy', price=100, condition=None, execution=None) # 전체 지정가 매수
        >>> order(account, 전체, code, order='buy', price=None, condition=None, execution=None) # 전체 시장가 매수
        >>> order(account, 전체, code, order='sell', price=100, condition=None, execution=None) # 전체 지정가 매도
        >>> order(account, 전체, code, order='sell', price=None, condition=None, execution=None) # 전체 시장가 매도
        >>> order(account, 'KRX', code, order='buy', price=100, condition=None, execution=None) # 지정가 매수
        >>> order(account, 'KRX', code, order='buy', price=None, condition=None, execution=None) # 시장가 매수
        >>> order(account, 'KRX', code, order='buy', price=100, condition='condition', execution=None) # 조건부지정가 매수
        >>> order(account, 'KRX', code, order='buy', price=100, condition='best', execution=None) # 최유리지정가 매수
        >>> order(account, 'KRX', code, order='buy', price=100, condition='priority', execution=None) # 최우선지정가 매수
        >>> order(account, 'KRX', code, order='buy', price=100, condition='extended', execution=None) # 시간외단일가 매수 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='buy', price=None, condition='before', execution=None) # 장전시간외 매수 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='buy', price=None, condition='after', execution=None) # 장후시간외 매수 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='buy', price=100, condition=None, execution='IOC') # IOC지정가 매수 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='buy', price=100, condition=None, execution='FOK') # FOK지정가 매수 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='buy', price=None, condition=None, execution='IOC') # IOC시장가 매수 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='buy', price=None, condition=None, execution='FOK') # FOK시장가 매수 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='buy', price=100, condition='best', execution='IOC') # IOC최유리 매수 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='buy', price=100, condition='best', execution='FOK') # FOK최유리 매수 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='sell', price=100, condition=None, execution=None) # 지정가 매도
        >>> order(account, 'KRX', code, order='sell', price=None, condition=None, execution=None) # 시장가 매도
        >>> order(account, 'KRX', code, order='sell', price=100, condition='condition', execution=None) # 조건부지정가 매도
        >>> order(account, 'KRX', code, order='sell', price=100, condition='best', execution=None) # 최유리지정가 매도
        >>> order(account, 'KRX', code, order='sell', price=100, condition='priority', execution=None) # 최우선지정가 매도
        >>> order(account, 'KRX', code, order='sell', price=100, condition='extended', execution=None) # 시간외단일가 매도 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='sell', price=None, condition='before', execution=None) # 장전시간외 매도 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='sell', price=None, condition='after', execution=None) # 장후시간외 매도
        >>> order(account, 'KRX', code, order='sell', price=100, condition=None, execution='IOC') # IOC지정가 매도 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='sell', price=100, condition=None, execution='FOK') # FOK지정가 매도 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='sell', price=None, condition=None, execution='IOC') # IOC시장가 매도 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='sell', price=None, condition=None, execution='FOK') # FOK시장가 매도 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='sell', price=100, condition='best', execution='IOC') # IOC최유리 매도 (모의투자 미지원)
        >>> order(account, 'KRX', code, order='sell', price=100, condition='best', execution='FOK') # FOK최유리 매도 (모의투자 미지원)
        >>> order(account, 'NASD', code, order='buy', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
        >>> order(account, 'NASD', code, order='buy', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
        >>> order(account, 'NASD', code, order='buy', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
        >>> order(account, 'NASD', code, order='buy', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='buy', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='buy', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='buy', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='buy', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='buy', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='buy', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='buy', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='buy', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
        >>> order(account, 'NASD', code, order='sell', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매도 (모의투자 미지원)
        >>> order(account, 'NASD', code, order='sell', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매도 (모의투자 미지원)
        >>> order(account, 'NASD', code, order='sell', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매도 (모의투자 미지원)
        >>> order(account, 'NASD', code, order='sell', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매도 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='sell', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매도 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='sell', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매도 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='sell', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매도 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='sell', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매도 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='sell', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매도 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='sell', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매도 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='sell', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매도 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='sell', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매도 (모의투자 미지원)
        >>> order(account, 'NASD', code, order='buy', price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='buy', price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='buy', price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수 (모의투자 미지원)
        >>> order(account, 'NASD', code, order='buy', price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='buy', price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='buy', price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수 (모의투자 미지원)
        >>> order(account, 'NASD', code, order='sell', price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매도 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='sell', price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매도 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='sell', price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매도 (모의투자 미지원)
        >>> order(account, 'NASD', code, order='sell', price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매도 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='sell', price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매도 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='sell', price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매도 (모의투자 미지원)

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        KisMarketNotOpenedError: 시장이 열리지 않은 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    if market == "KRX":
        return domestic_order(
            self,
            account=account,
            code=code,
            order=order,
            price=price,
            qty=qty,
            condition=condition,  # type: ignore
            execution=execution,
            include_foreign=include_foreign,
        )
    else:
        if condition == "extended":
            if execution is not None:
                raise ValueError("주간거래 주문에서는 체결조건을 지정할 수 없습니다.")

            return overseas_daytime_order(
                self,
                account=account,
                market=market,
                code=code,
                order=order,
                price=price,
                qty=qty,
                include_foreign=include_foreign,
            )

        return overseas_order(
            self,
            account=account,
            market=market,
            code=code,
            order=order,
            price=price,
            qty=qty,
            condition=condition,  # type: ignore
            execution=execution,
            include_foreign=include_foreign,
        )


# TODO: 전량 매도 구현
