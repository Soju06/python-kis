from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Literal

from pykis.__env__ import TIMEZONE
from pykis.api.stock.base.account_product import KisAccountProductBase
from pykis.api.stock.market import MARKET_TYPE
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

DOMESTIC_ORDER_CONDITION_KOR_MAP = {
    "condition": "조건부지정가",
    "best": "최유리지정가",
    "priority": "최우선지정가",
    "extended": "시간외단일가",
    "before": "장전시간외",
    "after": "장후시간외",
}

DOMESTIC_ORDER_CONDITION_MAP: dict[
    tuple[bool, DOMESTIC_ORDER_CONDITION | None, ORDER_EXECUTION_CONDITION | None], str
] = {
    # 단가, 주문조건, 체결조건
    (True, None, None): "00",  # 지정가
    (False, None, None): "01",  # 시장가
    (True, "condition", None): "02",  # 조건부지정가
    (True, "best", None): "03",  # 최유리지정가
    (True, "priority", None): "04",  # 최우선지정가
    (True, "extended", None): "07",  # 시간외 단일가
    (False, "before", None): "05",  # 장전 시간외
    (False, "after", None): "06",  # 장후 시간외
    (True, None, "IOC"): "11",  # IOC지정가
    (True, None, "FOK"): "12",  # FOK지정가
    (False, None, "IOC"): "13",  # IOC시장가
    (False, None, "FOK"): "14",  # FOK시장가
    (True, "best", "IOC"): "15",  # IOC최유리
    (True, "best", "FOK"): "16",  # FOK최유리
}

DOMESTIC_ORDER_CONDITION_CODE_KOR_MAP = {
    "00": "지정가",
    "01": "시장가",
    "02": "조건부지정가",
    "03": "최유리지정가",
    "04": "최우선지정가",
    "05": "장전시간외",
    "06": "장후시간외",
    "07": "시간외단일가",
    "11": "IOC지정가",
    "12": "FOK지정가",
    "13": "IOC시장가",
    "14": "FOK시장가",
    "15": "IOC최유리",
    "16": "FOK최유리",
}


def _domestic_orderable_conditions_repr():
    return "\n".join(
        (
            f"domestic_order(price={'100' if price else 'None'}, condition={condition!r}, execution={execution!r}) "
            f"# {DOMESTIC_ORDER_CONDITION_CODE_KOR_MAP[code]}"
        )
        for (price, condition, execution), code in DOMESTIC_ORDER_CONDITION_MAP.items()
    )


def _domestic_order_condition(
    price: int | None = None,
    condition: DOMESTIC_ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION_CONDITION | None = None,
):
    if price and price < 0:
        raise ValueError("가격은 0보다 작을 수 없습니다.")

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
    price: int | None = None,
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
