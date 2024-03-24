from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Literal, get_args

from pykis.__env__ import TIMEZONE
from pykis.api.stock.base.account_product import KisAccountProductBase
from pykis.api.stock.market import MARKET_TYPE, MARKET_TYPE_KOR_MAP
from pykis.client.account import KisAccountNumber
from pykis.responses.dynamic import KisDynamic
from pykis.responses.response import KisAPIResponse
from pykis.responses.types import KisString

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisOrderNumber(KisDynamic, KisAccountProductBase):
    """한국투자증권 주문번호"""

    branch: str
    """지점코드"""
    number: str
    """주문번호"""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(account_number={self.account_number!r}, code={self.code!r}, market={self.market!r}, branch={self.branch!r}, number={self.number!r})"


class KisOrder(KisOrderNumber):
    """한국투자증권 주문"""

    time: datetime
    """주문시간 (현지시간)"""
    time_kst: datetime
    """주문시간 (한국시간)"""

    def __init__(self, account_number: KisAccountNumber, code: str, market: MARKET_TYPE):
        self.account_number = account_number
        self.code = code
        self.market = market


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
        super().__pre_init__(data)

        self.time_kst = self.time = datetime.combine(
            datetime.now(TIMEZONE).date(),
            datetime.strptime(data["ORD_TMD"], "%H%M%S").time(),
            tzinfo=TIMEZONE,
        )


ORDER_TYPE = Literal["buy", "sell"]
"""주문 종류"""

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

DOMESTIC_ORDER_CONDITION_MAP: dict[
    tuple[bool, ORDER_TYPE, DOMESTIC_ORDER_CONDITION | None, ORDER_EXECUTION_CONDITION | None],
    tuple[str, str],
] = {
    # (단가, 주문종류, 주문조건, 체결조건): (주문구분코드, 주문구분한글명)
    (True, "buy", None, None): ("00", "지정가"),
    (False, "buy", None, None): ("01", "시장가"),
    (True, "buy", "condition", None): ("02", "조건부지정가"),
    (True, "buy", "best", None): ("03", "최유리지정가"),
    (True, "buy", "priority", None): ("04", "최우선지정가"),
    (True, "buy", "extended", None): ("07", "시간외단일가"),
    (False, "buy", "before", None): ("05", "장전시간외"),
    (False, "buy", "after", None): ("06", "장후시간외"),
    (True, "buy", None, "IOC"): ("11", "IOC지정가"),
    (True, "buy", None, "FOK"): ("12", "FOK지정가"),
    (False, "buy", None, "IOC"): ("13", "IOC시장가"),
    (False, "buy", None, "FOK"): ("14", "FOK시장가"),
    (True, "buy", "best", "IOC"): ("15", "IOC최유리"),
    (True, "buy", "best", "FOK"): ("16", "FOK최유리"),
    (True, "sell", None, None): ("00", "지정가"),
    (False, "sell", None, None): ("01", "시장가"),
    (True, "sell", "condition", None): ("02", "조건부지정가"),
    (True, "sell", "best", None): ("03", "최유리지정가"),
    (True, "sell", "priority", None): ("04", "최우선지정가"),
    (True, "sell", "extended", None): ("07", "시간외단일가"),
    (False, "sell", "before", None): ("05", "장전시간외"),
    (False, "sell", "after", None): ("06", "장후시간외"),
    (True, "sell", None, "IOC"): ("11", "IOC지정가"),
    (True, "sell", None, "FOK"): ("12", "FOK지정가"),
    (False, "sell", None, "IOC"): ("13", "IOC시장가"),
    (False, "sell", None, "FOK"): ("14", "FOK시장가"),
    (True, "sell", "best", "IOC"): ("15", "IOC최유리"),
    (True, "sell", "best", "FOK"): ("16", "FOK최유리"),
}


def _domestic_orderable_conditions_repr():
    return "\n".join(
        (
            f"domestic_order(order={order!r}, price={'100' if price else 'None'}, condition={condition!r}, execution={execution!r}) "
            f"# {label} {'매수' if order == 'buy' else '매도'}"
        )
        for (price, order, condition, execution), (_, label) in DOMESTIC_ORDER_CONDITION_MAP.items()
    )


def _domestic_order_condition(
    order: ORDER_TYPE = "buy",
    price: Decimal | None = None,
    condition: DOMESTIC_ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION_CONDITION | None = None,
):
    if price and price <= 0:
        raise ValueError("가격은 0보다 커야합니다.")

    order_condition = (price is not None, order, condition, execution)

    if order_condition not in DOMESTIC_ORDER_CONDITION_MAP:
        # 조건을 찾을 수 없을 경우, 시장가로 변환
        order_condition = (False, order, condition, execution)

    if order_condition not in DOMESTIC_ORDER_CONDITION_MAP:
        raise ValueError(
            f"주문조건이 잘못되었습니다. (order={order!r} price={price!r}, condition={condition!r}, execution={execution!r})\n"
            "아래 주문 가능 조건을 참고하세요.\n\n" + _domestic_orderable_conditions_repr()
        )

    return DOMESTIC_ORDER_CONDITION_MAP[order_condition]


def domestic_order(
    self: "PyKis",
    account: str | KisAccountNumber,
    code: str,
    order: ORDER_TYPE = "buy",
    price: Decimal | None = None,
    qty: int | None = None,
    condition: DOMESTIC_ORDER_CONDITION | None = None,
):
    if not account:
        raise ValueError("계좌번호를 입력해주세요.")

    if not code:
        raise ValueError("종목코드를 입력해주세요.")

    if qty and qty < 0:
        raise ValueError("수량은 0보다 작을 수 없습니다.")

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)


OVERSEAS_ORDER_CONDITION_MAP: dict[
    tuple[
        bool | None,
        MARKET_TYPE | None,
        ORDER_TYPE,
        bool,
        OVERSEAS_ORDER_CONDITION | None,
        ORDER_EXECUTION_CONDITION | None,
    ],
    tuple[str, Literal["lower", "upper"] | None, str],
] = {
    # (실전투자여부, 시장, 주문종류, 단가, 주문조건, 체결조건): (주문구분코드, 지정단가설정, 주문구분한글명)
    (None, None, "buy", True, None, None): ("00", None, "지정가"),
    (None, None, "buy", False, None, None): ("00", "upper", "시장가"),
    (None, None, "sell", True, None, None): ("00", None, "지정가"),
    (None, None, "sell", False, None, None): ("00", "lower", "시장가"),
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


def _overseas_orderable_conditions_repr():
    return "\n".join(
        (
            f"overseas_order(market={repr(market) if market else '전체'}, order={order!r}, price={'100' if price else 'None'}, condition={condition!r}, execution={execution!r}) "
            f"# {MARKET_TYPE_KOR_MAP[market]} {label} {'매수' if order == 'buy' else '매도'}{'' if ((False, market, order, price, condition, execution) in OVERSEAS_ORDER_CONDITION_MAP) else ' (모의투자 지원안함)'}"
        )
        for (real, market, order, price, condition, execution), (
            _,
            _,
            label,
        ) in OVERSEAS_ORDER_CONDITION_MAP.items()
        if real is not False
    )


def _overseas_order_condition(
    virtual: bool,
    market: MARKET_TYPE,
    order: ORDER_TYPE,
    price: Decimal | None = None,
    condition: OVERSEAS_ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION_CONDITION | None = None,
):
    if price and price <= 0:
        raise ValueError("가격은 0보다 커야합니다.")

    order_condition = [not virtual, market, order, price is not None, condition, execution]

    if tuple(order_condition) not in OVERSEAS_ORDER_CONDITION_MAP:
        # 조건을 찾을 수 없을 경우, 투자구분을 기본값으로 변환
        order_condition[0] = None

    if tuple(order_condition) not in OVERSEAS_ORDER_CONDITION_MAP:
        # 조건을 찾을 수 없을 경우, 시장을 기본값으로 변환
        order_condition[1] = None

    if order_condition[3] and tuple(order_condition) not in OVERSEAS_ORDER_CONDITION_MAP:
        # 조건을 찾을 수 없을 경우, 단가를 시장가로 변환
        order_condition[3] = False

    if tuple(order_condition) not in OVERSEAS_ORDER_CONDITION_MAP:
        # 모의투자 지원 안함 여부 확인
        virtual_not_supported = False

        if virtual:
            order_condition[0] = False

            if tuple(order_condition) in OVERSEAS_ORDER_CONDITION_MAP:
                virtual_not_supported = True

        raise ValueError(
            (
                "모의투자는 해당 주문조건을 지원하지 않습니다."
                if virtual_not_supported
                else "주문조건이 잘못되었습니다."
            )
            + f" (market={market!r}, order={order!r}, price={price!r}, condition={condition!r}, execution={execution!r})\n"
            "아래 주문 가능 조건을 참고하세요.\n\n" + _overseas_orderable_conditions_repr()
        )

    return OVERSEAS_ORDER_CONDITION_MAP[tuple(order_condition)]  # type: ignore
