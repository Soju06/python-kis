from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Literal

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
    tuple[bool, DOMESTIC_ORDER_CONDITION | None, ORDER_EXECUTION_CONDITION | None], tuple[str, str]
] = {
    # (단가, 주문조건, 체결조건): (주문구분코드, 주문구분한글명)
    (True, None, None): ("00", "지정가"),
    (False, None, None): ("01", "시장가"),
    (True, "condition", None): ("02", "조건부지정가"),
    (True, "best", None): ("03", "최유리지정가"),
    (True, "priority", None): ("04", "최우선지정가"),
    (True, "extended", None): ("07", "시간외단일가"),
    (False, "before", None): ("05", "장전시간외"),
    (False, "after", None): ("06", "장후시간외"),
    (True, None, "IOC"): ("11", "IOC지정가"),
    (True, None, "FOK"): ("12", "FOK지정가"),
    (False, None, "IOC"): ("13", "IOC시장가"),
    (False, None, "FOK"): ("14", "FOK시장가"),
    (True, "best", "IOC"): ("15", "IOC최유리"),
    (True, "best", "FOK"): ("16", "FOK최유리"),
}


def _domestic_orderable_conditions_repr():
    return "\n".join(
        (
            f"domestic_order(price={'100' if price else 'None'}, condition={condition!r}, execution={execution!r}) "
            f"# {label}"
        )
        for (price, condition, execution), (_, label) in DOMESTIC_ORDER_CONDITION_MAP.items()
    )


def _domestic_order_condition(
    price: Decimal | None = None,
    condition: DOMESTIC_ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION_CONDITION | None = None,
):
    if price and price <= 0:
        raise ValueError("가격은 0보다 커야합니다.")

    order = (price is not None, condition, execution)

    if order not in DOMESTIC_ORDER_CONDITION_MAP:
        # 조건을 찾을 수 없을 경우, 시장가로 변환
        order = (False, condition, execution)

    if order not in DOMESTIC_ORDER_CONDITION_MAP:
        raise ValueError(
            f"주문조건이 잘못되었습니다. (price={price!r}, condition={condition!r}, execution={execution!r})\n"
            "아래 주문 가능 조건을 참고하세요.\n\n" + _domestic_orderable_conditions_repr()
        )

    return DOMESTIC_ORDER_CONDITION_MAP[order]


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
            f"# {MARKET_TYPE_KOR_MAP[market]} {label}{' (모의투자 지원안함)' if ((False, market, order, price, condition, execution) in OVERSEAS_ORDER_CONDITION_MAP) else ''}"
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
            ("모의투자는 해당 주문조건을 지원하지 않습니다." if virtual_not_supported else "주문조건이 잘못되었습니다.")
            + f" (market={market!r}, order={order!r}, price={price!r}, condition={condition!r}, execution={execution!r})\n"
            "아래 주문 가능 조건을 참고하세요.\n\n" + _overseas_orderable_conditions_repr()
        )

    return OVERSEAS_ORDER_CONDITION_MAP[tuple(order_condition)]  # type: ignore
