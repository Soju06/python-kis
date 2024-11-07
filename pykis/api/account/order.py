from datetime import datetime, tzinfo
from decimal import Decimal
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Literal,
    Protocol,
    get_args,
    overload,
    runtime_checkable,
)

from typing_extensions import deprecated

from pykis.adapter.account_product.order_modify import (
    KisOrderableOrder,
    KisOrderableOrderMixin,
)
from pykis.adapter.websocket.execution import (
    KisRealtimeOrderableAccount,
    KisRealtimeOrderableOrderMixin,
)
from pykis.api.base.account import KisAccountProtocol
from pykis.api.base.account_product import (
    KisAccountProductBase,
    KisAccountProductProtocol,
)
from pykis.api.stock.info import get_market_country
from pykis.api.stock.market import (
    DAYTIME_MARKET_SHORT_TYPE_MAP,
    MARKET_TYPE,
    get_market_code,
    get_market_name,
    get_market_timezone,
)
from pykis.api.stock.quote import quote
from pykis.client.account import KisAccountNumber
from pykis.event.filters.order import KisOrderNumberEventFilter
from pykis.event.handler import KisEventFilter
from pykis.event.subscription import KisSubscriptionEventArgs
from pykis.responses.exceptions import KisMarketNotOpenedError
from pykis.responses.response import KisAPIResponse, raise_not_found
from pykis.responses.types import KisString
from pykis.utils.timezone import TIMEZONE
from pykis.utils.typing import Checkable

if TYPE_CHECKING:
    from pykis.api.account.pending_order import KisPendingOrder
    from pykis.api.base.account_product import KisAccountProductProtocol
    from pykis.client.websocket import KisWebsocketClient
    from pykis.kis import PyKis

__all__ = [
    "ORDER_TYPE",
    "ORDER_PRICE",
    "ORDER_EXECUTION",
    "ORDER_CONDITION",
    "KisOrderNumber",
    "KisOrder",
    "order",
]

ORDER_TYPE = Literal["buy", "sell"]
"""주문 종류"""

ORDER_PRICE = Decimal | int | float
"""주문 가격"""

ORDER_QUANTITY = Decimal
"""주문 수량"""

IN_ORDER_QUANTITY = Decimal | int | float
"""주문 수량"""


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


def ensure_quantity(quantity: IN_ORDER_QUANTITY, digit: int | None = 0) -> ORDER_QUANTITY:
    """
    주문 수량을 Decimal로 변환합니다.

    Args:
        quantity (IN_ORDER_QUANTITY): 주문 수량
        digit (int | None, optional): 소수점 자릿수 (내림)
    """
    if not isinstance(quantity, ORDER_QUANTITY):
        quantity = ORDER_QUANTITY(quantity)

    if digit is not None:
        quantity = quantity.quantize(Decimal(f"1e{-digit}"))

    return quantity


ORDER_EXECUTION = Literal[
    # 즉시체결 또는 전량취소
    "IOC",
    # 전량체결 또는 전량취소
    "FOK",
]
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

FOREIGN_ORDER_CONDITION = Literal[
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

ORDER_CONDITION = DOMESTIC_ORDER_CONDITION | FOREIGN_ORDER_CONDITION
"""주문 조건"""


def to_domestic_order_condition(condition: ORDER_CONDITION) -> DOMESTIC_ORDER_CONDITION:
    if condition in get_args(DOMESTIC_ORDER_CONDITION):
        return condition  # type: ignore

    raise ValueError(f"주문 조건이 국내 주문 조건이 아닙니다. ({condition!r})")


def to_foreign_order_condition(condition: ORDER_CONDITION) -> FOREIGN_ORDER_CONDITION:
    if condition in get_args(FOREIGN_ORDER_CONDITION):
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
        ORDER_EXECUTION | None,
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
    (True, "NASDAQ", "buy", True, "LOO", None): ("32", None, "장개시지정가"),
    (True, "NASDAQ", "buy", True, "LOC", None): ("34", None, "장마감지정가"),
    (True, "NASDAQ", "buy", False, "MOO", None): ("32", "upper", "장개시시장가"),
    (True, "NASDAQ", "buy", False, "MOC", None): ("34", "upper", "장마감시장가"),
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
    (True, "NASDAQ", "sell", True, "LOO", None): ("32", None, "장개시지정가"),
    (True, "NASDAQ", "sell", True, "LOC", None): ("34", None, "장마감지정가"),
    (True, "NASDAQ", "sell", False, "MOO", None): ("31", None, "장개시시장가"),
    (True, "NASDAQ", "sell", False, "MOC", None): ("33", None, "장마감시장가"),
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
            f"# {get_market_name(market)} {label} {'매수' if order == 'buy' else '매도'}{'' if ((False, market, order, price, condition, execution) in ORDER_CONDITION_MAP) or (None, market, order, price, condition, execution) in ORDER_CONDITION_MAP else ' (모의투자 미지원)'}"
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
    execution: ORDER_EXECUTION | None = None,
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
            ("모의투자는 해당 주문조건을 지원하지 않습니다." if virtual_not_supported else "주문조건이 잘못되었습니다.")
            + f" (market={market!r}, order={order!r}, price={price!r}, condition={condition!r}, execution={execution!r})\n"
            "아래 주문 가능 조건을 참고하세요.\n\n" + orderable_conditions_repr()
        )

    return ORDER_CONDITION_MAP[tuple(order_condition)]  # type: ignore


DOMESTIC_REVERSE_ORDER_CONDITION_MAP: dict[str, tuple[bool, ORDER_CONDITION | None, ORDER_EXECUTION | None]] = {
    # 주문구분코드: (지정가여부, 주문조건, 체결조건)
    "00": (True, None, None),
    "01": (False, None, None),
    "02": (True, "condition", None),
    "03": (True, "best", None),
    "04": (True, "priority", None),
    "05": (False, "before", None),
    "06": (False, "after", None),
    "07": (True, "extended", None),
    "11": (True, None, "IOC"),
    "12": (True, None, "FOK"),
    "13": (False, None, "IOC"),
    "14": (False, None, "FOK"),
    "15": (True, "best", "IOC"),
    "16": (True, "best", "FOK"),
}


def resolve_domestic_order_condition(
    code: str,
) -> tuple[bool, ORDER_CONDITION | None, ORDER_EXECUTION | None]:
    if code not in DOMESTIC_REVERSE_ORDER_CONDITION_MAP:
        return True, None, None

    return DOMESTIC_REVERSE_ORDER_CONDITION_MAP[code]


@runtime_checkable
class KisOrderNumber(KisAccountProductProtocol, KisEventFilter["KisWebsocketClient", KisSubscriptionEventArgs], Protocol):
    """한국투자증권 주문번호"""

    @property
    def branch(self) -> str:
        """지점코드"""
        ...

    @property
    def number(self) -> str:
        """주문번호"""
        ...

    def __eq__(self, value: "object | KisOrderNumber") -> bool:
        ...

    def __hash__(self) -> int:
        ...


@runtime_checkable
class KisOrder(KisOrderNumber, KisOrderableOrder, KisRealtimeOrderableAccount, Protocol):
    """한국투자증권 주문"""

    @property
    def time(self) -> datetime:
        """주문시간 (현지시간)"""
        ...

    @property
    def time_kst(self) -> datetime:
        """주문시간 (한국시간)"""
        ...

    @property
    def timezone(self) -> tzinfo:
        """시간대"""
        ...

    @property
    def pending(self) -> bool:
        """미체결 여부"""
        ...

    @property
    def pending_order(self) -> "KisPendingOrder | None":
        """미체결 주문"""
        ...

    @staticmethod
    def from_number(
        kis: "PyKis",
        symbol: str,
        market: MARKET_TYPE,
        account_number: KisAccountNumber,
        branch: str,
        number: str,
    ) -> "KisOrderNumber":
        """
        주문번호 생성

        Args:
            kis (PyKis): 한국투자증권 API
            symbol (str): 종목코드
            market (MARKET_TYPE): 상품유형
            account_number (KisAccountNumber): 계좌번호
            branch (str): 지점코드
            number (str): 주문번호
        """
        return KisSimpleOrderNumber.from_number(
            kis=kis,
            symbol=symbol,
            market=market,
            account_number=account_number,
            branch=branch,
            number=number,
        )

    @staticmethod
    def from_order(
        kis: "PyKis",
        symbol: str,
        market: MARKET_TYPE,
        account_number: KisAccountNumber,
        branch: str,
        number: str,
        time_kst: datetime,
    ) -> "KisOrder":
        """
        주문 생성

        Args:
            kis (PyKis): 한국투자증권 API
            symbol (str): 종목코드
            market (MARKET_TYPE): 상품유형
            account_number (KisAccountNumber): 계좌번호
            branch (str): 지점코드
            number (str): 주문번호
            time_kst (datetime): 주문시간 (한국시간)
        """
        return KisSimpleOrder.from_order(
            kis=kis,
            symbol=symbol,
            market=market,
            account_number=account_number,
            branch=branch,
            number=number,
            time_kst=time_kst,
        )


class KisOrderNumberBase(KisAccountProductBase, KisOrderNumberEventFilter):
    """한국투자증권 주문번호"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    branch: str
    """지점코드"""
    number: str
    """주문번호"""

    @overload
    def __init__(self): ...

    @overload
    def __init__(self, kis: "PyKis"): ...

    @overload
    def __init__(
        self,
        kis: "PyKis",
        symbol: str,
        market: MARKET_TYPE,
        account_number: KisAccountNumber,
        branch: str,
        number: str,
    ): ...

    def __init__(
        self,
        kis: "PyKis | None" = None,
        symbol: str | None = None,
        market: MARKET_TYPE | None = None,
        account_number: KisAccountNumber | None = None,
        branch: str | None = None,
        number: str | None = None,
    ):
        super().__init__(self)

        if kis is not None:
            self.kis = kis

        if symbol is not None:
            self.symbol = symbol

            if market is None:
                raise ValueError("market이 지정되지 않았습니다.")

            self.market = market

            if account_number is None:
                raise ValueError("account_number가 지정되지 않았습니다.")

            self.account_number = account_number

            if branch is None:
                raise ValueError("branch가 지정되지 않았습니다.")

            self.branch = branch

            if number is None:
                raise ValueError("number가 지정되지 않았습니다.")

            self.number = number

    def __eq__(self, value: object | KisOrderNumber) -> bool:
        try:
            return (
                self.account_number == value.account_number  # type: ignore
                and self.symbol == value.symbol  # type: ignore
                and self.market == value.market  # type: ignore
                and (self.foreign or self.branch == value.branch)  # type: ignore
                and int(self.number) == int(value.number)  # type: ignore
            )
        except AttributeError:
            return False

    def __hash__(self) -> int:
        return hash((self.account_number, self.symbol, self.market, self.branch, int(self.number)))

    def __repr__(self) -> str:
        return f"""{self.__class__.__name__}(
    kis=kis,
    account_number={self.account_number!r},
    code={self.symbol!r},
    market={self.market!r},
    branch={self.branch!r},
    number={self.number!r}
)"""


class KisOrderBase(KisOrderNumberBase, KisOrderableOrderMixin, KisRealtimeOrderableOrderMixin):
    """한국투자증권 주문"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    branch: str
    """지점코드"""
    number: str
    """주문번호"""

    time: datetime
    """주문시간 (현지시간)"""
    time_kst: datetime
    """주문시간 (한국시간)"""
    timezone: tzinfo
    """시간대"""

    @overload
    def __init__(self): ...

    @overload
    def __init__(self, account_number: KisAccountNumber, symbol: str, market: "MARKET_TYPE"): ...

    @overload
    def __init__(
        self,
        account_number: KisAccountNumber,
        symbol: str,
        market: "MARKET_TYPE",
        branch: str,
        number: str,
        time_kst: datetime,
        kis: "PyKis",
    ): ...

    def __init__(
        self,
        account_number: KisAccountNumber | None = None,
        symbol: str | None = None,
        market: "MARKET_TYPE | None" = None,
        branch: str | None = None,
        number: str | None = None,
        time_kst: datetime | None = None,
        kis: "PyKis | None" = None,
    ):
        super().__init__()

        if kis is not None:
            self.kis = kis

        if account_number is not None:
            self.account_number = account_number

            if symbol is None:
                raise ValueError("symbol이 지정되지 않았습니다.")

            self.symbol = symbol

            if market is None:
                raise ValueError("market이 지정되지 않았습니다.")

            self.market = market
            self.timezone = get_market_timezone(self.market)

        if branch is not None:
            if account_number is None:
                raise ValueError("account_number가 지정되지 않았습니다.")

            self.branch = branch

            if number is None:
                raise ValueError("number가 지정되지 않았습니다.")

            self.number = number

            if time_kst is None:
                raise ValueError("time_kst가 지정되지 않았습니다.")

            self.time_kst = time_kst
            self.time = self.time_kst.astimezone(self.timezone)

    @property
    def pending(self) -> bool:
        """미체결 여부"""
        return self.pending_order is not None

    @property
    def pending_order(self) -> "KisPendingOrder | None":
        """미체결 주문"""
        from pykis.api.account.pending_order import pending_orders

        return pending_orders(
            self.kis,
            account=self.account_number,
            country=get_market_country(self.market),
        ).order(self)

    @staticmethod
    @deprecated("Use KisOrder.from_number() instead")
    def from_number(
        kis: "PyKis",
        symbol: str,
        market: MARKET_TYPE,
        account_number: KisAccountNumber,
        branch: str,
        number: str,
    ) -> "KisOrderNumber":
        """
        주문번호 생성

        Args:
            kis (PyKis): 한국투자증권 API
            symbol (str): 종목코드
            market (MARKET_TYPE): 상품유형
            account_number (KisAccountNumber): 계좌번호
            branch (str): 지점코드
            number (str): 주문번호
        """
        return KisSimpleOrderNumber.from_number(
            kis=kis,
            symbol=symbol,
            market=market,
            account_number=account_number,
            branch=branch,
            number=number,
        )

    @staticmethod
    @deprecated("Use KisOrder.from_order() instead")
    def from_order(
        kis: "PyKis",
        symbol: str,
        market: MARKET_TYPE,
        account_number: KisAccountNumber,
        branch: str,
        number: str,
        time_kst: datetime,
    ) -> "KisOrder":
        """
        주문 생성

        Args:
            kis (PyKis): 한국투자증권 API
            symbol (str): 종목코드
            market (MARKET_TYPE): 상품유형
            account_number (KisAccountNumber): 계좌번호
            branch (str): 지점코드
            number (str): 주문번호
            time_kst (datetime): 주문시간 (한국시간)
        """
        return KisSimpleOrder.from_order(
            kis=kis,
            symbol=symbol,
            market=market,
            account_number=account_number,
            branch=branch,
            number=number,
            time_kst=time_kst,
        )


class KisSimpleOrderNumber(KisOrderNumberBase):
    """한국투자증권 주문번호"""

    @staticmethod
    def from_number(
        kis: "PyKis",
        symbol: str,
        market: MARKET_TYPE,
        account_number: KisAccountNumber,
        branch: str,
        number: str,
    ) -> "KisOrderNumber":
        """
        주문번호 생성

        Args:
            kis (PyKis): 한국투자증권 API
            symbol (str): 종목코드
            market (MARKET_TYPE): 상품유형
            account_number (KisAccountNumber): 계좌번호
            branch (str): 지점코드
            number (str): 주문번호
        """
        return KisSimpleOrderNumber(
            kis=kis,
            symbol=symbol,
            market=market,
            account_number=account_number,
            branch=branch,
            number=number,
        )


class KisSimpleOrder(KisOrderBase):
    """한국투자증권 주문번호"""

    @staticmethod
    def from_order(
        kis: "PyKis",
        symbol: str,
        market: MARKET_TYPE,
        account_number: KisAccountNumber,
        branch: str,
        number: str,
        time_kst: datetime,
    ) -> "KisOrder":
        """
        주문 생성

        Args:
            kis (PyKis): 한국투자증권 API
            symbol (str): 종목코드
            market (MARKET_TYPE): 상품유형
            account_number (KisAccountNumber): 계좌번호
            branch (str): 지점코드
            number (str): 주문번호
            time_kst (datetime): 주문시간 (한국시간)
        """
        return KisSimpleOrder(
            account_number=account_number,
            symbol=symbol,
            market=market,  # type: ignore
            branch=branch,
            number=number,
            time_kst=time_kst,
            kis=kis,
        )


if TYPE_CHECKING:
    # IDE Type Checking
    Checkable[KisOrderNumber](KisOrderNumberBase)
    Checkable[KisOrder](KisOrderBase)


class KisDomesticOrder(KisAPIResponse, KisOrderBase):
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
                code=self.symbol,
                market=self.market,
            )

        super().__pre_init__(data)

        self.time_kst = self.time = datetime.combine(
            datetime.now(TIMEZONE).date(),
            datetime.strptime(data["output"]["ORD_TMD"], "%H%M%S").time(),
            tzinfo=TIMEZONE,
        )


class KisForeignOrder(KisAPIResponse, KisOrderBase):
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
                code=self.symbol,
                market=self.market,
            )

        super().__pre_init__(data)

        self.time_kst = datetime.combine(
            datetime.now(TIMEZONE).date(),
            datetime.strptime(data["output"]["ORD_TMD"], "%H%M%S").time(),
            tzinfo=TIMEZONE,
        )
        self.time = self.time_kst.astimezone(self.timezone)


class KisForeignDaytimeOrder(KisAPIResponse, KisOrderBase):
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
                code=self.symbol,
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


def _orderable_quantity(
    self: "PyKis",
    account: str | KisAccountNumber,
    market: MARKET_TYPE,
    symbol: str,
    order: ORDER_TYPE = "buy",
    price: ORDER_PRICE | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
    include_foreign: bool = False,
    throw_no_qty: bool = True,
) -> tuple[ORDER_QUANTITY, Decimal | None]:
    """
    주문 가능 수량 조회

    국내주식주문 -> 매수가능조회[v1_국내주식-007]
    해외주식주문 -> 해외주식 매수가능금액조회[v1_해외주식-014]

    국내주식시세 -> 상품기본조회[v1_국내주식-029]
    국내주식주문 -> 주식잔고조회[v1_국내주식-006]
    해외주식주문 -> 해외주식 체결기준현재잔고[v1_해외주식-008] (실전투자, 모의투자)
    해외주식주문 -> 해외주식 잔고[v1_해외주식-006] (모의투자)

    Args:
        account (str | KisAccountNumber): 계좌번호
        market (MARKET_TYPE): 시장
        symbol (str): 종목코드
        order (ORDER_TYPE, optional): 주문종류
        price (ORDER_PRICE, optional): 주문가격
        condition (ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
        include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부
        throw_no_qty (bool, optional): 주문가능수량이 없을 경우 예외 발생 여부

    Returns:
        tuple[ORDER_QUANTITY, Decimal | None]: 주문가능수량, 주문단가

    Raises:
        ValueError: 주문가능수량이 없는 경우
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
    """
    if order == "buy":
        from pykis.api.account.orderable_amount import orderable_amount

        amount = orderable_amount(
            self,
            account=account,
            market="KRX",
            symbol=symbol,
            price=price,
            condition=condition,
            execution=execution,
        )

        if include_foreign:
            qty = amount.foreign_qty
        else:
            qty = amount.qty

        if throw_no_qty and qty <= 0:
            raise ValueError("주문가능수량이 없습니다.")

        return qty, amount.unit_price
    else:
        from pykis.api.account.balance import orderable_quantity

        qty = orderable_quantity(
            self,
            account=account,
            symbol=symbol,
            country=get_market_country(market),
        )

        if throw_no_qty and (not qty or qty <= 0):
            raise ValueError("주문가능수량이 없습니다.")

        return qty or Decimal(0), None


def _get_order_price(
    self: "PyKis",
    market: MARKET_TYPE,
    symbol: str,
    price_setting: Literal["lower", "upper"],
) -> Decimal:
    quote_data = quote(self, symbol=symbol, market=market)

    if price_setting == "upper":
        return quote_data.high_limit or (quote_data.close * Decimal(1.5))
    else:
        return quote_data.low_limit or (quote_data.close * Decimal(0.5))


def domestic_order(
    self: "PyKis",
    account: str | KisAccountNumber,
    symbol: str,
    order: ORDER_TYPE = "buy",
    price: ORDER_PRICE | None = None,
    qty: IN_ORDER_QUANTITY | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
    include_foreign: bool = False,
) -> KisDomesticOrder:
    """
    한국투자증권 국내 주식 주문

    국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
    (업데이트 날짜: 2024/03/24)

    Args:
        account (str | KisAccountNumber): 계좌번호
        symbol (str): 종목코드
        order (ORDER_TYPE, optional): 주문종류
        price (ORDER_PRICE, optional): 주문가격
        qty (IN_ORDER_QUANTITY, optional): 주문수량
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

    if not symbol:
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
        price = _get_order_price(
            self,
            market="KRX",
            symbol=symbol,
            price_setting=price_setting,
        )

    if qty is None:
        qty, _ = _orderable_quantity(
            self,
            account=account,
            market="KRX",
            symbol=symbol,
            order=order,
            price=None if price_setting else price,
            condition=condition,
            execution=execution,
            include_foreign=include_foreign,
        )

    return self.fetch(
        "/uapi/domestic-stock/v1/trading/order-cash",
        api=DOMESTIC_ORDER_API_CODES[(not self.virtual, order)],
        body={
            "PDNO": symbol,
            "ORD_DVSN": condition_code,
            "ORD_QTY": str(int(qty)),
            "ORD_UNPR": str(price or 0),
        },
        form=[account],
        response_type=KisDomesticOrder(
            account_number=account,
            symbol=symbol,
            market="KRX",
        ),
        method="POST",
    )


FOREIGN_ORDER_API_CODES: dict[tuple[bool, MARKET_TYPE, ORDER_TYPE], str] = {
    # (실전투자여부, 시장, 주문종류): API코드
    (True, "NASDAQ", "buy"): "TTTT1002U",  # 미국 매수 주문
    (True, "NYSE", "buy"): "TTTT1002U",  # 미국 매수 주문
    (True, "AMEX", "buy"): "TTTT1002U",  # 미국 매수 주문
    (True, "NASDAQ", "sell"): "TTTT1006U",  # 미국 매도 주문
    (True, "NYSE", "sell"): "TTTT1006U",  # 미국 매도 주문
    (True, "AMEX", "sell"): "TTTT1006U",  # 미국 매도 주문
    (True, "TYO", "buy"): "TTTS0308U",  # 일본 매수 주문
    (True, "TYO", "sell"): "TTTS0307U",  # 일본 매도 주문
    (True, "SSE", "buy"): "TTTS0202U",  # 상하이 매수 주문
    (True, "SSE", "sell"): "TTTS1005U",  # 상하이 매도 주문
    (True, "HKEX", "buy"): "TTTS1002U",  # 홍콩 매수 주문
    (True, "HKEX", "sell"): "TTTS1001U",  # 홍콩 매도 주문
    (True, "SZSE", "buy"): "TTTS0305U",  # 심천 매수 주문
    (True, "SZSE", "sell"): "TTTS0304U",  # 심천 매도 주문
    (True, "HNX", "buy"): "TTTS0311U",  # 베트남 매수 주문
    (True, "HSX", "buy"): "TTTS0311U",  # 베트남 매수 주문
    (True, "HNX", "sell"): "TTTS0310U",  # 베트남 매도 주문
    (True, "HSX", "sell"): "TTTS0310U",  # 베트남 매도 주문
    (False, "NASDAQ", "buy"): "VTTT1002U",  # 미국 매수 주문
    (False, "NYSE", "buy"): "VTTT1002U",  # 미국 매수 주문
    (False, "AMEX", "buy"): "VTTT1002U",  # 미국 매수 주문
    (False, "NASDAQ", "sell"): "VTTT1001U",  # 미국 매도 주문
    (False, "NYSE", "sell"): "VTTT1001U",  # 미국 매도 주문
    (False, "AMEX", "sell"): "VTTT1001U",  # 미국 매도 주문
    (False, "TYO", "buy"): "VTTS0308U",  # 일본 매수 주문
    (False, "TYO", "sell"): "VTTS0307U",  # 일본 매도 주문
    (False, "SSE", "buy"): "VTTS0202U",  # 상하이 매수 주문
    (False, "SSE", "sell"): "VTTS1005U",  # 상하이 매도 주문
    (False, "HKEX", "buy"): "VTTS1002U",  # 홍콩 매수 주문
    (False, "HKEX", "sell"): "VTTS1001U",  # 홍콩 매도 주문
    (False, "SZSE", "buy"): "VTTS0305U",  # 심천 매수 주문
    (False, "SZSE", "sell"): "VTTS0304U",  # 심천 매도 주문
    (False, "HNX", "buy"): "VTTS0311U",  # 베트남 매수 주문
    (False, "HSX", "buy"): "VTTS0311U",  # 베트남 매수 주문
    (False, "HNX", "sell"): "VTTS0310U",  # 베트남 매도 주문
    (False, "HSX", "sell"): "VTTS0310U",  # 베트남 매도 주문
}


def foreign_order(
    self: "PyKis",
    account: str | KisAccountNumber,
    market: MARKET_TYPE,
    symbol: str,
    order: ORDER_TYPE = "buy",
    price: ORDER_PRICE | None = None,
    qty: IN_ORDER_QUANTITY | None = None,
    condition: FOREIGN_ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
    include_foreign: bool = False,
) -> KisForeignOrder:
    """
    한국투자증권 해외 주식 주문

    해외주식주문 -> 해외주식 주문[v1_해외주식-001]
    (업데이트 날짜: 2024/03/24)

    Args:
        account (str | KisAccountNumber): 계좌번호
        market (MARKET_TYPE): 시장
        symbol (str): 종목코드
        order (ORDER_TYPE, optional): 주문종류
        price (ORDER_PRICE, optional): 주문가격
        qty (IN_ORDER_QUANTITY, optional): 주문수량
        condition (DOMESTIC_ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
        include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부

    Examples:
        >>> foreign_order(account, 전체, code, order='buy', price=100, condition=None, execution=None) # 전체 지정가 매수
        >>> foreign_order(account, 전체, code, order='buy', price=None, condition=None, execution=None) # 전체 시장가 매수
        >>> foreign_order(account, 전체, code, order='sell', price=100, condition=None, execution=None) # 전체 지정가 매도
        >>> foreign_order(account, 전체, code, order='sell', price=None, condition=None, execution=None) # 전체 시장가 매도
        >>> foreign_order(account, 'NASDAQ', code, order='buy', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
        >>> foreign_order(account, 'NASDAQ', code, order='buy', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
        >>> foreign_order(account, 'NASDAQ', code, order='buy', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
        >>> foreign_order(account, 'NASDAQ', code, order='buy', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
        >>> foreign_order(account, 'NYSE', code, order='buy', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
        >>> foreign_order(account, 'NYSE', code, order='buy', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
        >>> foreign_order(account, 'NYSE', code, order='buy', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
        >>> foreign_order(account, 'NYSE', code, order='buy', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
        >>> foreign_order(account, 'AMEX', code, order='buy', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
        >>> foreign_order(account, 'AMEX', code, order='buy', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
        >>> foreign_order(account, 'AMEX', code, order='buy', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
        >>> foreign_order(account, 'AMEX', code, order='buy', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
        >>> foreign_order(account, 'NASDAQ', code, order='sell', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매도 (모의투자 미지원)
        >>> foreign_order(account, 'NASDAQ', code, order='sell', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매도 (모의투자 미지원)
        >>> foreign_order(account, 'NASDAQ', code, order='sell', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매도 (모의투자 미지원)
        >>> foreign_order(account, 'NASDAQ', code, order='sell', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매도 (모의투자 미지원)
        >>> foreign_order(account, 'NYSE', code, order='sell', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매도 (모의투자 미지원)
        >>> foreign_order(account, 'NYSE', code, order='sell', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매도 (모의투자 미지원)
        >>> foreign_order(account, 'NYSE', code, order='sell', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매도 (모의투자 미지원)
        >>> foreign_order(account, 'NYSE', code, order='sell', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매도 (모의투자 미지원)
        >>> foreign_order(account, 'AMEX', code, order='sell', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매도 (모의투자 미지원)
        >>> foreign_order(account, 'AMEX', code, order='sell', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매도 (모의투자 미지원)
        >>> foreign_order(account, 'AMEX', code, order='sell', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매도 (모의투자 미지원)
        >>> foreign_order(account, 'AMEX', code, order='sell', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매도 (모의투자 미지원)

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

    if not symbol:
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

    if price_setting:
        price = _get_order_price(
            self,
            market=market,
            symbol=symbol,
            price_setting=price_setting,
        )

    if qty is None:
        qty, _ = _orderable_quantity(
            self,
            account=account,
            market=market,
            symbol=symbol,
            order=order,
            price=None if price_setting else price,
            condition=condition,
            execution=execution,
            include_foreign=include_foreign,
        )

    return self.fetch(
        "/uapi/overseas-stock/v1/trading/order",
        api=FOREIGN_ORDER_API_CODES[(not self.virtual, market, order)],
        body={
            "OVRS_EXCG_CD": get_market_code(market),
            "PDNO": symbol,
            "ORD_QTY": str(int(qty)),
            "OVRS_ORD_UNPR": str(price or 0),
            "SLL_TYPE": "00" if order == "sell" else "",
            "ORD_SVR_DVSN_CD": "0",
            "ORD_DVSN": condition_code,
        },
        form=[account],
        response_type=KisForeignOrder(
            account_number=account,
            symbol=symbol,
            market=market,
        ),
        method="POST",
    )


def foreign_daytime_order(
    self: "PyKis",
    account: str | KisAccountNumber,
    market: MARKET_TYPE,
    symbol: str,
    order: ORDER_TYPE = "buy",
    price: ORDER_PRICE | None = None,
    qty: IN_ORDER_QUANTITY | None = None,
    include_foreign: bool = False,
) -> KisForeignDaytimeOrder:
    """
    한국투자증권 해외주식 주간거래 주문 (주간, 모의투자 미지원)

    해외주식주문 -> 해외주식 미국주간주문[v1_해외주식-026]
    (업데이트 날짜: 2024/03/25)

    Args:
        account (str | KisAccountNumber): 계좌번호
        market (MARKET_TYPE): 시장
        symbol (str): 종목코드
        order (ORDER_TYPE, optional): 주문종류
        price (ORDER_PRICE, optional): 주문가격
        qty (IN_ORDER_QUANTITY, optional): 주문수량
        include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부
    """
    if self.virtual:
        raise NotImplementedError("주간거래 주문은 모의투자를 지원하지 않습니다.")

    if market not in DAYTIME_MARKET_SHORT_TYPE_MAP:
        raise ValueError(f"주간거래가 지원되지 않는 시장입니다. ({market})")

    if not account:
        raise ValueError("계좌번호를 입력해주세요.")

    if not symbol:
        raise ValueError("종목코드를 입력해주세요.")

    if qty != None and qty <= 0:
        raise ValueError("수량은 0보다 커야합니다.")

    price = None if price is None else ensure_price(price)

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    if qty is None:
        qty, price = _orderable_quantity(
            self,
            account=account,
            market=market,
            symbol=symbol,
            order=order,
            price=price,
            condition="extended",
            include_foreign=include_foreign,
        )

    if not price:
        quote_data = quote(self, symbol=symbol, market=market, extended=True)
        price = quote_data.high_limit if order == "buy" else quote_data.low_limit

    return self.fetch(
        "/uapi/overseas-stock/v1/trading/daytime-order",
        api="TTTS6036U" if order == "buy" else "TTTS6037U",
        body={
            "OVRS_EXCG_CD": get_market_code(market),
            "PDNO": symbol,
            "ORD_QTY": str(int(qty)),
            "OVRS_ORD_UNPR": str(price),
            "ORD_SVR_DVSN_CD": "0",
            "ORD_DVSN": "00",
        },
        form=[account],
        response_type=KisForeignDaytimeOrder(
            account_number=account,
            symbol=symbol,
            market=market,
        ),
        method="POST",
        domain="real",
    )


def order(
    self: "PyKis",
    account: str | KisAccountNumber,
    market: MARKET_TYPE,
    symbol: str,
    order: ORDER_TYPE,
    price: ORDER_PRICE | None = None,
    qty: IN_ORDER_QUANTITY | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
    include_foreign: bool = False,
) -> KisOrder:
    """
    한국투자증권 통합주식 주문

    국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
    해외주식주문 -> 해외주식 주문[v1_해외주식-001]

    Args:
        account (str | KisAccountNumber): 계좌번호
        market (MARKET_TYPE): 시장
        symbol (str): 종목코드
        order (ORDER_TYPE): 주문종류
        price (ORDER_PRICE, optional): 주문가격
        qty (IN_ORDER_QUANTITY, optional): 주문수량
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
        >>> order(account, 'NASDAQ', code, order='buy', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
        >>> order(account, 'NASDAQ', code, order='buy', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
        >>> order(account, 'NASDAQ', code, order='buy', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
        >>> order(account, 'NASDAQ', code, order='buy', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='buy', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='buy', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='buy', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='buy', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='buy', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='buy', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='buy', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='buy', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
        >>> order(account, 'NASDAQ', code, order='sell', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매도 (모의투자 미지원)
        >>> order(account, 'NASDAQ', code, order='sell', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매도 (모의투자 미지원)
        >>> order(account, 'NASDAQ', code, order='sell', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매도 (모의투자 미지원)
        >>> order(account, 'NASDAQ', code, order='sell', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매도 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='sell', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매도 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='sell', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매도 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='sell', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매도 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='sell', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매도 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='sell', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매도 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='sell', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매도 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='sell', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매도 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='sell', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매도 (모의투자 미지원)
        >>> order(account, 'NASDAQ', code, order='buy', price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='buy', price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='buy', price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수 (모의투자 미지원)
        >>> order(account, 'NASDAQ', code, order='buy', price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='buy', price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='buy', price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수 (모의투자 미지원)
        >>> order(account, 'NASDAQ', code, order='sell', price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매도 (모의투자 미지원)
        >>> order(account, 'NYSE', code, order='sell', price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매도 (모의투자 미지원)
        >>> order(account, 'AMEX', code, order='sell', price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매도 (모의투자 미지원)
        >>> order(account, 'NASDAQ', code, order='sell', price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매도 (모의투자 미지원)
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
            symbol=symbol,
            order=order,
            price=price,
            qty=qty,
            condition=condition,
            execution=execution,
            include_foreign=include_foreign,
        )  # type: ignore
    else:
        if condition == "extended":
            if execution is not None:
                raise ValueError("주간거래 주문에서는 체결조건을 지정할 수 없습니다.")

            return foreign_daytime_order(
                self,
                account=account,
                market=market,
                symbol=symbol,
                order=order,
                price=price,
                qty=qty,
                include_foreign=include_foreign,
            )  # type: ignore

        return foreign_order(
            self,
            account=account,
            market=market,
            symbol=symbol,
            order=order,
            price=price,
            qty=qty,
            condition=condition,  # type: ignore
            execution=execution,
            include_foreign=include_foreign,
        )  # type: ignore


order_function = order


def account_order(
    self: "KisAccountProtocol",
    market: MARKET_TYPE,
    symbol: str,
    order: ORDER_TYPE,
    price: ORDER_PRICE | None = None,
    qty: IN_ORDER_QUANTITY | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
    include_foreign: bool = False,
) -> KisOrder:
    """
    한국투자증권 통합주식 주문

    국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
    해외주식주문 -> 해외주식 주문[v1_해외주식-001]

    Args:
        market (MARKET_TYPE): 시장
        symbol (str): 종목코드
        order (ORDER_TYPE): 주문종류
        price (ORDER_PRICE, optional): 주문가격
        qty (IN_ORDER_QUANTITY, optional): 주문수량
        condition (DOMESTIC_ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
        include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부

    Examples:
        >>> order(전체, code, order='buy', price=100, condition=None, execution=None) # 전체 지정가 매수
        >>> order(전체, code, order='buy', price=None, condition=None, execution=None) # 전체 시장가 매수
        >>> order(전체, code, order='sell', price=100, condition=None, execution=None) # 전체 지정가 매도
        >>> order(전체, code, order='sell', price=None, condition=None, execution=None) # 전체 시장가 매도
        >>> order('KRX', code, order='buy', price=100, condition=None, execution=None) # 지정가 매수
        >>> order('KRX', code, order='buy', price=None, condition=None, execution=None) # 시장가 매수
        >>> order('KRX', code, order='buy', price=100, condition='condition', execution=None) # 조건부지정가 매수
        >>> order('KRX', code, order='buy', price=100, condition='best', execution=None) # 최유리지정가 매수
        >>> order('KRX', code, order='buy', price=100, condition='priority', execution=None) # 최우선지정가 매수
        >>> order('KRX', code, order='buy', price=100, condition='extended', execution=None) # 시간외단일가 매수 (모의투자 미지원)
        >>> order('KRX', code, order='buy', price=None, condition='before', execution=None) # 장전시간외 매수 (모의투자 미지원)
        >>> order('KRX', code, order='buy', price=None, condition='after', execution=None) # 장후시간외 매수 (모의투자 미지원)
        >>> order('KRX', code, order='buy', price=100, condition=None, execution='IOC') # IOC지정가 매수 (모의투자 미지원)
        >>> order('KRX', code, order='buy', price=100, condition=None, execution='FOK') # FOK지정가 매수 (모의투자 미지원)
        >>> order('KRX', code, order='buy', price=None, condition=None, execution='IOC') # IOC시장가 매수 (모의투자 미지원)
        >>> order('KRX', code, order='buy', price=None, condition=None, execution='FOK') # FOK시장가 매수 (모의투자 미지원)
        >>> order('KRX', code, order='buy', price=100, condition='best', execution='IOC') # IOC최유리 매수 (모의투자 미지원)
        >>> order('KRX', code, order='buy', price=100, condition='best', execution='FOK') # FOK최유리 매수 (모의투자 미지원)
        >>> order('KRX', code, order='sell', price=100, condition=None, execution=None) # 지정가 매도
        >>> order('KRX', code, order='sell', price=None, condition=None, execution=None) # 시장가 매도
        >>> order('KRX', code, order='sell', price=100, condition='condition', execution=None) # 조건부지정가 매도
        >>> order('KRX', code, order='sell', price=100, condition='best', execution=None) # 최유리지정가 매도
        >>> order('KRX', code, order='sell', price=100, condition='priority', execution=None) # 최우선지정가 매도
        >>> order('KRX', code, order='sell', price=100, condition='extended', execution=None) # 시간외단일가 매도 (모의투자 미지원)
        >>> order('KRX', code, order='sell', price=None, condition='before', execution=None) # 장전시간외 매도 (모의투자 미지원)
        >>> order('KRX', code, order='sell', price=None, condition='after', execution=None) # 장후시간외 매도
        >>> order('KRX', code, order='sell', price=100, condition=None, execution='IOC') # IOC지정가 매도 (모의투자 미지원)
        >>> order('KRX', code, order='sell', price=100, condition=None, execution='FOK') # FOK지정가 매도 (모의투자 미지원)
        >>> order('KRX', code, order='sell', price=None, condition=None, execution='IOC') # IOC시장가 매도 (모의투자 미지원)
        >>> order('KRX', code, order='sell', price=None, condition=None, execution='FOK') # FOK시장가 매도 (모의투자 미지원)
        >>> order('KRX', code, order='sell', price=100, condition='best', execution='IOC') # IOC최유리 매도 (모의투자 미지원)
        >>> order('KRX', code, order='sell', price=100, condition='best', execution='FOK') # FOK최유리 매도 (모의투자 미지원)
        >>> order('NASDAQ', code, order='buy', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
        >>> order('NASDAQ', code, order='buy', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
        >>> order('NASDAQ', code, order='buy', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
        >>> order('NASDAQ', code, order='buy', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
        >>> order('NYSE', code, order='buy', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
        >>> order('NYSE', code, order='buy', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
        >>> order('NYSE', code, order='buy', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
        >>> order('NYSE', code, order='buy', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
        >>> order('AMEX', code, order='buy', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
        >>> order('AMEX', code, order='buy', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
        >>> order('AMEX', code, order='buy', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
        >>> order('AMEX', code, order='buy', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
        >>> order('NASDAQ', code, order='sell', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매도 (모의투자 미지원)
        >>> order('NASDAQ', code, order='sell', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매도 (모의투자 미지원)
        >>> order('NASDAQ', code, order='sell', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매도 (모의투자 미지원)
        >>> order('NASDAQ', code, order='sell', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매도 (모의투자 미지원)
        >>> order('NYSE', code, order='sell', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매도 (모의투자 미지원)
        >>> order('NYSE', code, order='sell', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매도 (모의투자 미지원)
        >>> order('NYSE', code, order='sell', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매도 (모의투자 미지원)
        >>> order('NYSE', code, order='sell', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매도 (모의투자 미지원)
        >>> order('AMEX', code, order='sell', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매도 (모의투자 미지원)
        >>> order('AMEX', code, order='sell', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매도 (모의투자 미지원)
        >>> order('AMEX', code, order='sell', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매도 (모의투자 미지원)
        >>> order('AMEX', code, order='sell', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매도 (모의투자 미지원)
        >>> order('NASDAQ', code, order='buy', price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수 (모의투자 미지원)
        >>> order('NYSE', code, order='buy', price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수 (모의투자 미지원)
        >>> order('AMEX', code, order='buy', price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수 (모의투자 미지원)
        >>> order('NASDAQ', code, order='buy', price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수 (모의투자 미지원)
        >>> order('NYSE', code, order='buy', price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수 (모의투자 미지원)
        >>> order('AMEX', code, order='buy', price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수 (모의투자 미지원)
        >>> order('NASDAQ', code, order='sell', price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매도 (모의투자 미지원)
        >>> order('NYSE', code, order='sell', price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매도 (모의투자 미지원)
        >>> order('AMEX', code, order='sell', price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매도 (모의투자 미지원)
        >>> order('NASDAQ', code, order='sell', price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매도 (모의투자 미지원)
        >>> order('NYSE', code, order='sell', price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매도 (모의투자 미지원)
        >>> order('AMEX', code, order='sell', price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매도 (모의투자 미지원)

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        KisMarketNotOpenedError: 시장이 열리지 않은 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    return order_function(
        self.kis,
        account=self.account_number,
        market=market,
        symbol=symbol,
        order=order,
        price=price,
        qty=qty,
        condition=condition,
        execution=execution,
        include_foreign=include_foreign,
    )


def account_buy(
    self: "KisAccountProtocol",
    market: MARKET_TYPE,
    symbol: str,
    price: ORDER_PRICE | None = None,
    qty: IN_ORDER_QUANTITY | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
    include_foreign: bool = False,
) -> KisOrder:
    """
    한국투자증권 통합주식 매수 주문

    국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
    해외주식주문 -> 해외주식 주문[v1_해외주식-001]

    Args:
        market (MARKET_TYPE): 시장
        symbol (str): 종목코드
        price (ORDER_PRICE, optional): 주문가격
        qty (IN_ORDER_QUANTITY, optional): 주문수량
        condition (DOMESTIC_ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
        include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부

    Examples:
        >>> buy(전체, code, price=100, condition=None, execution=None) # 전체 지정가 매수
        >>> buy(전체, code, price=None, condition=None, execution=None) # 전체 시장가 매수
        >>> buy('KRX', code, price=100, condition=None, execution=None) # 지정가 매수
        >>> buy('KRX', code, price=None, condition=None, execution=None) # 시장가 매수
        >>> buy('KRX', code, price=100, condition='condition', execution=None) # 조건부지정가 매수
        >>> buy('KRX', code, price=100, condition='best', execution=None) # 최유리지정가 매수
        >>> buy('KRX', code, price=100, condition='priority', execution=None) # 최우선지정가 매수
        >>> buy('KRX', code, price=100, condition='extended', execution=None) # 시간외단일가 매수 (모의투자 미지원)
        >>> buy('KRX', code, price=None, condition='before', execution=None) # 장전시간외 매수 (모의투자 미지원)
        >>> buy('KRX', code, price=None, condition='after', execution=None) # 장후시간외 매수 (모의투자 미지원)
        >>> buy('KRX', code, price=100, condition=None, execution='IOC') # IOC지정가 매수 (모의투자 미지원)
        >>> buy('KRX', code, price=100, condition=None, execution='FOK') # FOK지정가 매수 (모의투자 미지원)
        >>> buy('KRX', code, price=None, condition=None, execution='IOC') # IOC시장가 매수 (모의투자 미지원)
        >>> buy('KRX', code, price=None, condition=None, execution='FOK') # FOK시장가 매수 (모의투자 미지원)
        >>> buy('KRX', code, price=100, condition='best', execution='IOC') # IOC최유리 매수 (모의투자 미지원)
        >>> buy('KRX', code, price=100, condition='best', execution='FOK') # FOK최유리 매수 (모의투자 미지원)
        >>> buy('NASDAQ', code, price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
        >>> buy('NASDAQ', code, price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
        >>> buy('NASDAQ', code, price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
        >>> buy('NASDAQ', code, price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
        >>> buy('NYSE', code, price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
        >>> buy('NYSE', code, price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
        >>> buy('NYSE', code, price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
        >>> buy('NYSE', code, price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
        >>> buy('AMEX', code, price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
        >>> buy('AMEX', code, price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
        >>> buy('AMEX', code, price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
        >>> buy('AMEX', code, price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
        >>> buy('NASDAQ', code, price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수 (모의투자 미지원)
        >>> buy('NYSE', code, price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수 (모의투자 미지원)
        >>> buy('AMEX', code, price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수 (모의투자 미지원)
        >>> buy('NASDAQ', code, price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수 (모의투자 미지원)
        >>> buy('NYSE', code, price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수 (모의투자 미지원)
        >>> buy('AMEX', code, price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수 (모의투자 미지원)

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        KisMarketNotOpenedError: 시장이 열리지 않은 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    return account_order(
        self,
        market=market,
        symbol=symbol,
        order="buy",
        price=price,
        qty=qty,
        condition=condition,
        execution=execution,
        include_foreign=include_foreign,
    )


def account_sell(
    self: "KisAccountProtocol",
    market: MARKET_TYPE,
    symbol: str,
    price: ORDER_PRICE | None = None,
    qty: IN_ORDER_QUANTITY | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
    include_foreign: bool = False,
) -> KisOrder:
    """
    한국투자증권 통합주식 매도 주문

    국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
    해외주식주문 -> 해외주식 주문[v1_해외주식-001]

    Args:
        market (MARKET_TYPE): 시장
        symbol (str): 종목코드
        price (ORDER_PRICE, optional): 주문가격
        qty (IN_ORDER_QUANTITY, optional): 주문수량
        condition (DOMESTIC_ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
        include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부

    Examples:
        >>> sell(전체, code, price=100, condition=None, execution=None) # 전체 지정가 매도
        >>> sell(전체, code, price=None, condition=None, execution=None) # 전체 시장가 매도
        >>> sell('KRX', code, price=100, condition=None, execution=None) # 지정가 매도
        >>> sell('KRX', code, price=None, condition=None, execution=None) # 시장가 매도
        >>> sell('KRX', code, price=100, condition='condition', execution=None) # 조건부지정가 매도
        >>> sell('KRX', code, price=100, condition='best', execution=None) # 최유리지정가 매도
        >>> sell('KRX', code, price=100, condition='priority', execution=None) # 최우선지정가 매도
        >>> sell('KRX', code, price=100, condition='extended', execution=None) # 시간외단일가 매도 (모의투자 미지원)
        >>> sell('KRX', code, price=None, condition='before', execution=None) # 장전시간외 매도 (모의투자 미지원)
        >>> sell('KRX', code, price=None, condition='after', execution=None) # 장후시간외 매도
        >>> sell('KRX', code, price=100, condition=None, execution='IOC') # IOC지정가 매도 (모의투자 미지원)
        >>> sell('KRX', code, price=100, condition=None, execution='FOK') # FOK지정가 매도 (모의투자 미지원)
        >>> sell('KRX', code, price=None, condition=None, execution='IOC') # IOC시장가 매도 (모의투자 미지원)
        >>> sell('KRX', code, price=None, condition=None, execution='FOK') # FOK시장가 매도 (모의투자 미지원)
        >>> sell('KRX', code, price=100, condition='best', execution='IOC') # IOC최유리 매도 (모의투자 미지원)
        >>> sell('KRX', code, price=100, condition='best', execution='FOK') # FOK최유리 매도 (모의투자 미지원)
        >>> sell('NASDAQ', code, price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매도 (모의투자 미지원)
        >>> sell('NASDAQ', code, price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매도 (모의투자 미지원)
        >>> sell('NASDAQ', code, price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매도 (모의투자 미지원)
        >>> sell('NASDAQ', code, price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매도 (모의투자 미지원)
        >>> sell('NYSE', code, price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매도 (모의투자 미지원)
        >>> sell('NYSE', code, price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매도 (모의투자 미지원)
        >>> sell('NYSE', code, price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매도 (모의투자 미지원)
        >>> sell('NYSE', code, price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매도 (모의투자 미지원)
        >>> sell('AMEX', code, price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매도 (모의투자 미지원)
        >>> sell('AMEX', code, price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매도 (모의투자 미지원)
        >>> sell('AMEX', code, price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매도 (모의투자 미지원)
        >>> sell('AMEX', code, price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매도 (모의투자 미지원)
        >>> sell('NASDAQ', code, price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매도 (모의투자 미지원)
        >>> sell('NYSE', code, price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매도 (모의투자 미지원)
        >>> sell('AMEX', code, price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매도 (모의투자 미지원)
        >>> sell('NASDAQ', code, price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매도 (모의투자 미지원)
        >>> sell('NYSE', code, price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매도 (모의투자 미지원)
        >>> sell('AMEX', code, price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매도 (모의투자 미지원)

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        KisMarketNotOpenedError: 시장이 열리지 않은 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    return account_order(
        self,
        market=market,
        symbol=symbol,
        order="sell",
        price=price,
        qty=qty,
        condition=condition,
        execution=execution,
        include_foreign=include_foreign,
    )


def account_product_order(
    self: "KisAccountProductProtocol",
    order: ORDER_TYPE,
    price: ORDER_PRICE | None = None,
    qty: IN_ORDER_QUANTITY | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
    include_foreign: bool = False,
) -> KisOrder:
    """
    한국투자증권 통합주식 주문

    국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
    해외주식주문 -> 해외주식 주문[v1_해외주식-001]

    Args:
        order (ORDER_TYPE): 주문종류
        price (ORDER_PRICE, optional): 주문가격
        qty (IN_ORDER_QUANTITY, optional): 주문수량
        condition (DOMESTIC_ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
        include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부

    Examples:
        >>> order('buy', price=100, condition=None, execution=None) # 전체 지정가 매수
        >>> order('buy', price=None, condition=None, execution=None) # 전체 시장가 매수
        >>> order('sell', price=100, condition=None, execution=None) # 전체 지정가 매도
        >>> order('sell', price=None, condition=None, execution=None) # 전체 시장가 매도
        >>> order('buy', price=100, condition=None, execution=None) # 지정가 매수
        >>> order('buy', price=None, condition=None, execution=None) # 시장가 매수
        >>> order('buy', price=100, condition='condition', execution=None) # 조건부지정가 매수
        >>> order('buy', price=100, condition='best', execution=None) # 최유리지정가 매수
        >>> order('buy', price=100, condition='priority', execution=None) # 최우선지정가 매수
        >>> order('buy', price=100, condition='extended', execution=None) # 시간외단일가 매수 (모의투자 미지원)
        >>> order('buy', price=None, condition='before', execution=None) # 장전시간외 매수 (모의투자 미지원)
        >>> order('buy', price=None, condition='after', execution=None) # 장후시간외 매수 (모의투자 미지원)
        >>> order('buy', price=100, condition=None, execution='IOC') # IOC지정가 매수 (모의투자 미지원)
        >>> order('buy', price=100, condition=None, execution='FOK') # FOK지정가 매수 (모의투자 미지원)
        >>> order('buy', price=None, condition=None, execution='IOC') # IOC시장가 매수 (모의투자 미지원)
        >>> order('buy', price=None, condition=None, execution='FOK') # FOK시장가 매수 (모의투자 미지원)
        >>> order('buy', price=100, condition='best', execution='IOC') # IOC최유리 매수 (모의투자 미지원)
        >>> order('buy', price=100, condition='best', execution='FOK') # FOK최유리 매수 (모의투자 미지원)
        >>> order('sell', price=100, condition=None, execution=None) # 지정가 매도
        >>> order('sell', price=None, condition=None, execution=None) # 시장가 매도
        >>> order('sell', price=100, condition='condition', execution=None) # 조건부지정가 매도
        >>> order('sell', price=100, condition='best', execution=None) # 최유리지정가 매도
        >>> order('sell', price=100, condition='priority', execution=None) # 최우선지정가 매도
        >>> order('sell', price=100, condition='extended', execution=None) # 시간외단일가 매도 (모의투자 미지원)
        >>> order('sell', price=None, condition='before', execution=None) # 장전시간외 매도 (모의투자 미지원)
        >>> order('sell', price=None, condition='after', execution=None) # 장후시간외 매도
        >>> order('sell', price=100, condition=None, execution='IOC') # IOC지정가 매도 (모의투자 미지원)
        >>> order('sell', price=100, condition=None, execution='FOK') # FOK지정가 매도 (모의투자 미지원)
        >>> order('sell', price=None, condition=None, execution='IOC') # IOC시장가 매도 (모의투자 미지원)
        >>> order('sell', price=None, condition=None, execution='FOK') # FOK시장가 매도 (모의투자 미지원)
        >>> order('sell', price=100, condition='best', execution='IOC') # IOC최유리 매도 (모의투자 미지원)
        >>> order('sell', price=100, condition='best', execution='FOK') # FOK최유리 매도 (모의투자 미지원)
        >>> order('buy', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
        >>> order('buy', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
        >>> order('buy', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
        >>> order('buy', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
        >>> order('buy', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
        >>> order('buy', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
        >>> order('buy', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
        >>> order('buy', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
        >>> order('buy', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
        >>> order('buy', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
        >>> order('buy', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
        >>> order('buy', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
        >>> order('sell', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매도 (모의투자 미지원)
        >>> order('sell', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매도 (모의투자 미지원)
        >>> order('sell', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매도 (모의투자 미지원)
        >>> order('sell', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매도 (모의투자 미지원)
        >>> order('sell', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매도 (모의투자 미지원)
        >>> order('sell', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매도 (모의투자 미지원)
        >>> order('sell', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매도 (모의투자 미지원)
        >>> order('sell', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매도 (모의투자 미지원)
        >>> order('sell', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매도 (모의투자 미지원)
        >>> order('sell', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매도 (모의투자 미지원)
        >>> order('sell', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매도 (모의투자 미지원)
        >>> order('sell', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매도 (모의투자 미지원)
        >>> order('buy', price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수 (모의투자 미지원)
        >>> order('buy', price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수 (모의투자 미지원)
        >>> order('buy', price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수 (모의투자 미지원)
        >>> order('buy', price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수 (모의투자 미지원)
        >>> order('buy', price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수 (모의투자 미지원)
        >>> order('buy', price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수 (모의투자 미지원)
        >>> order('sell', price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매도 (모의투자 미지원)
        >>> order('sell', price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매도 (모의투자 미지원)
        >>> order('sell', price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매도 (모의투자 미지원)
        >>> order('sell', price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매도 (모의투자 미지원)
        >>> order('sell', price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매도 (모의투자 미지원)
        >>> order('sell', price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매도 (모의투자 미지원)

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        KisMarketNotOpenedError: 시장이 열리지 않은 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    return order_function(
        self.kis,
        account=self.account_number,
        market=self.market,
        symbol=self.symbol,
        order=order,
        price=price,
        qty=qty,
        condition=condition,
        execution=execution,
        include_foreign=include_foreign,
    )


def account_product_buy(
    self: "KisAccountProductProtocol",
    price: ORDER_PRICE | None = None,
    qty: IN_ORDER_QUANTITY | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
    include_foreign: bool = False,
) -> KisOrder:
    """
    한국투자증권 통합주식 매수 주문

    국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
    해외주식주문 -> 해외주식 주문[v1_해외주식-001]

    Args:
        price (ORDER_PRICE, optional): 주문가격
        qty (IN_ORDER_QUANTITY, optional): 주문수량
        condition (DOMESTIC_ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
        include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부

    Examples:
        >>> buy(price=100, condition=None, execution=None) # 전체 지정가 매수
        >>> buy(price=None, condition=None, execution=None) # 전체 시장가 매수
        >>> buy(price=100, condition=None, execution=None) # 지정가 매수
        >>> buy(price=None, condition=None, execution=None) # 시장가 매수
        >>> buy(price=100, condition='condition', execution=None) # 조건부지정가 매수
        >>> buy(price=100, condition='best', execution=None) # 최유리지정가 매수
        >>> buy(price=100, condition='priority', execution=None) # 최우선지정가 매수
        >>> buy(price=100, condition='extended', execution=None) # 시간외단일가 매수 (모의투자 미지원)
        >>> buy(price=None, condition='before', execution=None) # 장전시간외 매수 (모의투자 미지원)
        >>> buy(price=None, condition='after', execution=None) # 장후시간외 매수 (모의투자 미지원)
        >>> buy(price=100, condition=None, execution='IOC') # IOC지정가 매수 (모의투자 미지원)
        >>> buy(price=100, condition=None, execution='FOK') # FOK지정가 매수 (모의투자 미지원)
        >>> buy(price=None, condition=None, execution='IOC') # IOC시장가 매수 (모의투자 미지원)
        >>> buy(price=None, condition=None, execution='FOK') # FOK시장가 매수 (모의투자 미지원)
        >>> buy(price=100, condition='best', execution='IOC') # IOC최유리 매수 (모의투자 미지원)
        >>> buy(price=100, condition='best', execution='FOK') # FOK최유리 매수 (모의투자 미지원)
        >>> buy(price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
        >>> buy(price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
        >>> buy(price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
        >>> buy(price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
        >>> buy(price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
        >>> buy(price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
        >>> buy(price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
        >>> buy(price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
        >>> buy(price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
        >>> buy(price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
        >>> buy(price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
        >>> buy(price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
        >>> buy(price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수 (모의투자 미지원)
        >>> buy(price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수 (모의투자 미지원)
        >>> buy(price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수 (모의투자 미지원)
        >>> buy(price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수 (모의투자 미지원)
        >>> buy(price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수 (모의투자 미지원)
        >>> buy(price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수 (모의투자 미지원)

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        KisMarketNotOpenedError: 시장이 열리지 않은 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    return account_product_order(
        self,
        order="buy",
        price=price,
        qty=qty,
        condition=condition,
        execution=execution,
        include_foreign=include_foreign,
    )


def account_product_sell(
    self: "KisAccountProductProtocol",
    price: ORDER_PRICE | None = None,
    qty: IN_ORDER_QUANTITY | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
    include_foreign: bool = False,
) -> KisOrder:
    """
    한국투자증권 통합주식 매도 주문

    국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
    해외주식주문 -> 해외주식 주문[v1_해외주식-001]

    Args:
        price (ORDER_PRICE, optional): 주문가격
        qty (IN_ORDER_QUANTITY, optional): 주문수량
        condition (DOMESTIC_ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
        include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부

    Examples:
        >>> sell(price=100, condition=None, execution=None) # 전체 지정가 매도
        >>> sell(price=None, condition=None, execution=None) # 전체 시장가 매도
        >>> sell(price=100, condition=None, execution=None) # 지정가 매도
        >>> sell(price=None, condition=None, execution=None) # 시장가 매도
        >>> sell(price=100, condition='condition', execution=None) # 조건부지정가 매도
        >>> sell(price=100, condition='best', execution=None) # 최유리지정가 매도
        >>> sell(price=100, condition='priority', execution=None) # 최우선지정가 매도
        >>> sell(price=100, condition='extended', execution=None) # 시간외단일가 매도 (모의투자 미지원)
        >>> sell(price=None, condition='before', execution=None) # 장전시간외 매도 (모의투자 미지원)
        >>> sell(price=None, condition='after', execution=None) # 장후시간외 매도
        >>> sell(price=100, condition=None, execution='IOC') # IOC지정가 매도 (모의투자 미지원)
        >>> sell(price=100, condition=None, execution='FOK') # FOK지정가 매도 (모의투자 미지원)
        >>> sell(price=None, condition=None, execution='IOC') # IOC시장가 매도 (모의투자 미지원)
        >>> sell(price=None, condition=None, execution='FOK') # FOK시장가 매도 (모의투자 미지원)
        >>> sell(price=100, condition='best', execution='IOC') # IOC최유리 매도 (모의투자 미지원)
        >>> sell(price=100, condition='best', execution='FOK') # FOK최유리 매도 (모의투자 미지원)
        >>> sell(price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매도 (모의투자 미지원)
        >>> sell(price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매도 (모의투자 미지원)
        >>> sell(price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매도 (모의투자 미지원)
        >>> sell(price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매도 (모의투자 미지원)
        >>> sell(price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매도 (모의투자 미지원)
        >>> sell(price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매도 (모의투자 미지원)
        >>> sell(price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매도 (모의투자 미지원)
        >>> sell(price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매도 (모의투자 미지원)
        >>> sell(price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매도 (모의투자 미지원)
        >>> sell(price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매도 (모의투자 미지원)
        >>> sell(price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매도 (모의투자 미지원)
        >>> sell(price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매도 (모의투자 미지원)
        >>> sell(price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매도 (모의투자 미지원)
        >>> sell(price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매도 (모의투자 미지원)
        >>> sell(price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매도 (모의투자 미지원)
        >>> sell(price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매도 (모의투자 미지원)
        >>> sell(price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매도 (모의투자 미지원)
        >>> sell(price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매도 (모의투자 미지원)

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        KisMarketNotOpenedError: 시장이 열리지 않은 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    return account_product_order(
        self,
        order="sell",
        price=price,
        qty=qty,
        condition=condition,
        execution=execution,
        include_foreign=include_foreign,
    )
