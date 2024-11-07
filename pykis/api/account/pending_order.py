from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Iterable, Protocol, runtime_checkable
from zoneinfo import ZoneInfo

from typing_extensions import deprecated

from pykis.adapter.account_product.order_modify import (
    KisOrderableOrder,
    KisOrderableOrderMixin,
)
from pykis.adapter.websocket.execution import KisRealtimeOrderableOrderMixin
from pykis.api.account.order import (
    ORDER_CONDITION,
    ORDER_EXECUTION,
    ORDER_QUANTITY,
    ORDER_TYPE,
    KisOrder,
    KisOrderNumber,
    KisOrderNumberBase,
    KisSimpleOrder,
    KisSimpleOrderNumber,
    resolve_domestic_order_condition,
)
from pykis.api.base.account import KisAccountBase, KisAccountProtocol
from pykis.api.base.account_product import (
    KisAccountProductBase,
    KisAccountProductProtocol,
)
from pykis.api.stock.info import COUNTRY_TYPE, get_market_country
from pykis.api.stock.market import (
    MARKET_TYPE,
    KisMarketType,
    get_market_code,
    get_market_code_timezone,
)
from pykis.client.account import KisAccountNumber
from pykis.client.page import KisPage
from pykis.event.filters.order import KisOrderNumberEventFilter
from pykis.responses.dynamic import KisDynamic, KisList
from pykis.responses.response import KisPaginationAPIResponse
from pykis.responses.types import KisAny, KisDecimal, KisString
from pykis.utils.repr import kis_repr
from pykis.utils.timezone import TIMEZONE
from pykis.utils.typing import Checkable

if TYPE_CHECKING:
    from pykis.kis import PyKis

__all__ = [
    "KisPendingOrder",
    "KisPendingOrders",
    "pending_orders",
]


@runtime_checkable
class KisPendingOrder(KisOrder, Protocol):
    """한국투자증권 미체결 주식"""

    @property
    def order_number(self) -> KisOrder:
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
    def orderable_quantity(self) -> ORDER_QUANTITY:
        """주문가능수량"""
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
    def orderable_qty(self) -> ORDER_QUANTITY:
        """주문가능수량"""
        ...

    @property
    def pending_quantity(self) -> ORDER_QUANTITY:
        """미체결수량"""
        ...

    @property
    def pending_qty(self) -> ORDER_QUANTITY:
        """미체결수량"""
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
    def rejected(self) -> bool:
        """거부여부"""
        ...

    @property
    def rejected_reason(self) -> str | None:
        """거부사유"""
        ...


@runtime_checkable
class KisPendingOrders(KisAccountProtocol, Protocol):
    """한국투자증권 미체결 주식"""

    @property
    def account_number(self) -> KisAccountNumber:
        """계좌번호"""
        ...

    @property
    def orders(self) -> list[KisPendingOrder]:
        """미체결주문"""
        ...

    def __getitem__(self, key: int | KisOrderNumber | str) -> KisPendingOrder:
        """인덱스 또는 주문번호로 주문을 조회합니다."""
        ...

    def order(self, key: KisOrderNumber | str) -> KisPendingOrder | None:
        """주문번호 또는 종목코드로 주문을 조회합니다."""
        ...

    def __len__(self) -> int:
        ...

    def __iter__(self) -> Iterable[KisPendingOrder]:
        ...


@kis_repr(
    "order_number",
    "type",
    "price",
    "qty",
    "executed_qty",
    "condition",
    "execution",
    lines="multiple",
)
class KisPendingOrderBase(
    KisAccountProductBase, KisOrderNumberEventFilter, KisRealtimeOrderableOrderMixin, KisOrderableOrderMixin
):
    """한국투자증권 미체결 주식"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    @property
    def branch(self) -> str:
        """지점코드"""
        return self.order_number.branch

    @property
    def number(self) -> str:
        """주문번호"""
        return self.order_number.number

    time: datetime
    """주문시각"""
    time_kst: datetime
    """주문시각(KST)"""
    timezone: ZoneInfo
    """시간대"""

    @property
    def pending(self) -> bool:
        """미체결 여부"""
        return True

    @property
    def pending_order(self) -> "KisPendingOrder | None":
        """미체결 주문"""
        return self

    order_number: KisOrder
    """주문번호"""

    type: ORDER_TYPE
    """주문유형"""

    price: Decimal
    """체결단가"""
    unit_price: Decimal | None
    """주문단가"""

    quantity: ORDER_QUANTITY
    """주문수량"""

    executed_quantity: ORDER_QUANTITY
    """체결수량"""

    orderable_quantity: ORDER_QUANTITY
    """주문가능수량"""

    condition: ORDER_CONDITION | None
    """주문조건"""
    execution: ORDER_EXECUTION | None
    """체결조건"""

    rejected: bool
    """거부여부"""
    rejected_reason: str | None
    """거부사유"""

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

    @property
    def executed_qty(self) -> ORDER_QUANTITY:
        """체결수량"""
        return self.executed_quantity

    @property
    def executed_amount(self) -> Decimal:
        """체결금액"""
        return (self.executed_quantity * self.price) if self.price else Decimal(0)

    @property
    def orderable_qty(self) -> ORDER_QUANTITY:
        """주문가능수량"""
        return self.orderable_quantity

    @property
    def pending_quantity(self) -> ORDER_QUANTITY:
        """미체결수량"""
        return self.quantity - self.executed_quantity

    @property
    def pending_qty(self) -> ORDER_QUANTITY:
        """미체결수량"""
        return self.pending_quantity

    def __init__(self) -> None:
        super().__init__(lambda: self)

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

    def __eq__(self, value: object | KisOrderNumber) -> bool:
        return self.order_number == value

    def __hash__(self) -> int:
        return hash(self.order_number)


if TYPE_CHECKING:
    # IDE Type Checking
    Checkable[KisOrderNumber](KisPendingOrderBase)
    Checkable[KisOrder](KisPendingOrderBase)


@kis_repr(
    "account_number",
    "orders",
    lines="multiple",
    field_lines={"orders": "multiple"},
)
class KisPendingOrdersBase(KisAccountBase):
    """한국투자증권 미체결 주식"""

    account_number: KisAccountNumber
    """계좌번호"""

    orders: list[KisPendingOrder]
    """미체결주문"""

    def __getitem__(self, key: int | KisOrderNumber | str) -> KisPendingOrder:
        """인덱스 또는 주문번호로 주문을 조회합니다."""
        if isinstance(key, int):
            return self.orders[key]
        elif isinstance(key, str):
            for order in self.orders:
                if order.symbol == key:
                    return order
        elif isinstance(key, KisOrderNumber):
            for order in self.orders:
                if order.order_number == key:
                    return order

        raise KeyError(key)

    def order(self, key: KisOrderNumber | str) -> KisPendingOrder | None:
        """주문번호 또는 종목코드로 주문을 조회합니다."""
        if isinstance(key, str):
            for order in self.orders:
                if order.symbol == key:
                    return order
        elif isinstance(key, KisOrderNumber):
            for order in self.orders:
                if order.order_number == key:
                    return order

        return None

    def __len__(self) -> int:
        return len(self.orders)

    def __iter__(self) -> Iterable[KisPendingOrder]:
        return iter(self.orders)


class KisDomesticPendingOrder(KisDynamic, KisPendingOrderBase):
    """한국투자증권 국내 미체결 주식"""

    symbol: str = KisString["pdno"]
    """종목코드"""
    market: MARKET_TYPE = "KRX"
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    time: datetime
    """주문시각"""
    time_kst: datetime
    """주문시각(KST)"""
    timezone: ZoneInfo = TIMEZONE
    """시간대"""

    order_number: KisOrder
    """주문번호"""

    type: ORDER_TYPE = KisAny(lambda x: "buy" if x == "02" else "sell")["sll_buy_dvsn_cd"]
    """주문유형"""

    price: Decimal = KisDecimal["ord_unpr"]
    """체결단가"""
    unit_price: Decimal | None = KisDecimal["ord_unpr"]
    """주문단가"""

    quantity: ORDER_QUANTITY = KisDecimal["ord_qty"]
    """주문수량"""

    executed_quantity: ORDER_QUANTITY = KisDecimal["tot_ccld_qty"]
    """체결수량"""

    orderable_quantity: ORDER_QUANTITY = KisDecimal["psbl_qty"]
    """주문가능수량"""

    condition: ORDER_CONDITION | None
    """주문조건"""
    execution: ORDER_EXECUTION | None
    """체결조건"""

    rejected: bool = False
    """거부여부"""
    rejected_reason: str | None = None
    """거부사유"""

    def __pre_init__(self, data: dict[str, Any]):
        super().__pre_init__(data)

        self.time_kst = self.time = datetime.combine(
            datetime.now(TIMEZONE).date(),
            datetime.strptime(data["ord_tmd"], "%H%M%S").time(),
            tzinfo=TIMEZONE,
        )

    def __post_init__(self):
        super().__post_init__()

        has_price, self.condition, self.execution = resolve_domestic_order_condition(self.__data__["ord_dvsn_cd"])

        if not has_price:
            self.unit_price = None

    def __kis_post_init__(self):
        super().__kis_post_init__()

        self.order_number = KisSimpleOrder.from_order(
            kis=self.kis,
            symbol=self.symbol,
            market=self.market,
            account_number=self.account_number,
            branch=self.__data__["ord_gno_brno"],
            number=self.__data__["odno"],
            time_kst=self.time_kst,
        )


class KisDomesticPendingOrders(KisPaginationAPIResponse, KisPendingOrdersBase):
    """한국투자증권 국내 미체결 주식"""

    __path__ = None

    account_number: KisAccountNumber
    """계좌번호"""

    orders: list[KisPendingOrder] = KisList(KisDomesticPendingOrder)["output"]
    """미체결주문"""

    def __init__(self, account_number: KisAccountNumber):
        super().__init__()
        self.account_number = account_number

    def __post_init__(self) -> None:
        super().__post_init__()

        for order in self.orders:
            order.account_number = self.account_number  # type: ignore

    def __kis_post_init__(self):
        super().__kis_post_init__()
        self._kis_spread(self.orders)  # type: ignore


class KisForeignPendingOrder(KisDynamic, KisPendingOrderBase):
    """한국투자증권 해외 미체결 주식"""

    symbol: str = KisString["pdno"]
    """종목코드"""
    market: MARKET_TYPE = KisMarketType["ovrs_excg_cd"]
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    time: datetime
    """주문시각"""
    time_kst: datetime
    """주문시각(KST)"""
    timezone: ZoneInfo = KisAny(get_market_code_timezone)["ovrs_excg_cd"]
    """시간대"""

    order_number: KisOrder
    """주문번호"""

    type: ORDER_TYPE = KisAny(lambda x: "buy" if x == "02" else "sell")["sll_buy_dvsn_cd"]
    """주문유형"""

    price: Decimal = KisDecimal["ft_ccld_unpr3"]
    """체결단가"""
    unit_price: Decimal | None = KisDecimal["ft_ord_unpr3"]
    """주문단가"""

    quantity: ORDER_QUANTITY = KisDecimal["ft_ord_qty"]
    """주문수량"""

    executed_quantity: ORDER_QUANTITY = KisDecimal["ft_ccld_qty"]
    """체결수량"""

    orderable_quantity: ORDER_QUANTITY = KisDecimal["nccs_qty"]
    """주문가능수량"""

    condition: ORDER_CONDITION | None = None
    """주문조건"""
    execution: ORDER_EXECUTION | None = None
    """체결조건"""

    rejected: bool = KisAny(lambda x: bool(x))["rjct_rson"]
    """거부여부"""
    rejected_reason: str | None = KisAny(lambda x: x if x else None)["rjct_rson_name"]
    """거부사유"""

    def __pre_init__(self, data: dict[str, Any]):
        super().__pre_init__(data)

        self.time_kst = datetime.combine(
            datetime.now(TIMEZONE).date(),
            datetime.strptime(data["ord_tmd"], "%H%M%S").time(),
            tzinfo=TIMEZONE,
        )

    def __post_init__(self):
        super().__post_init__()

        self.time = self.time_kst.astimezone(self.timezone)

        if not self.unit_price:
            self.unit_price = None

    def __kis_post_init__(self):
        super().__kis_post_init__()

        self.order_number = KisSimpleOrder.from_order(
            kis=self.kis,
            symbol=self.symbol,
            market=self.market,
            account_number=self.account_number,
            branch=self.__data__["ord_gno_brno"],
            number=self.__data__["odno"],
            time_kst=self.time_kst,
        )


class KisForeignPendingOrders(KisPaginationAPIResponse, KisPendingOrdersBase):
    """한국투자증권 해외 미체결 주식"""

    __path__ = None

    account_number: KisAccountNumber
    """계좌번호"""

    orders: list[KisPendingOrder] = KisList(KisForeignPendingOrder)["output"]
    """미체결주문"""

    def __init__(self, account_number: KisAccountNumber):
        super().__init__()
        self.account_number = account_number

    def __post_init__(self) -> None:
        super().__post_init__()

        for order in self.orders:
            order.account_number = self.account_number  # type: ignore

    def __kis_post_init__(self):
        super().__kis_post_init__()
        self._kis_spread(self.orders)  # type: ignore


class KisIntegrationPendingOrders(KisPendingOrdersBase):
    """한국투자증권 미체결 주식"""

    account_number: KisAccountNumber
    """계좌번호"""
    orders: list[KisPendingOrder]
    """미체결주문"""

    _orders: list[KisPendingOrders]
    """내부구현 미체결주문"""

    def __init__(self, kis: "PyKis", account_number: KisAccountNumber, *orders: KisPendingOrders):
        super().__init__()
        self.kis = kis
        self.account_number = account_number
        self._orders = list(orders)
        self.orders = []

        for order in orders:
            self.orders.extend(order.orders)

        self.orders.sort(key=lambda x: x.time_kst, reverse=True)


class KisSimplePendingOrders(KisPendingOrdersBase):
    """한국투자증권 미체결 주식"""

    account_number: KisAccountNumber
    """계좌번호"""
    orders: list[KisPendingOrder]
    """미체결주문"""

    def __init__(self, account_number: KisAccountNumber, orders: list[KisPendingOrder]):
        self.account_number = account_number
        self.orders = orders

        self.orders.sort(key=lambda x: x.time_kst, reverse=True)


def domestic_pending_orders(
    self: "PyKis",
    account: str | KisAccountNumber,
    page: KisPage | None = None,
    continuous: bool = True,
) -> KisDomesticPendingOrders:
    """
    한국투자증권 국내 주식 미체결 조회 (모의투자 미지원)

    국내주식주문 -> 주식정정취소가능주문조회[v1_국내주식-004]
    (업데이트 날짜: 2024/03/31)

    Args:
        account (str | KisAccountNumber): 계좌번호
        page (KisPage, optional): 페이지 정보
        continuous (bool, optional): 연속조회 여부

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    if self.virtual:
        raise NotImplementedError("모의투자에서는 미체결 주문 조회를 지원하지 않습니다.")

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    page = (page or KisPage.first()).to(100)
    first = None

    while True:
        result = self.fetch(
            "/uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl",
            api="TTTC8036R",
            params={
                "INQR_DVSN_1": "1",
                "INQR_DVSN_2": "0",
            },
            form=[
                account,
                page,
            ],
            continuous=not page.is_first,
            response_type=KisDomesticPendingOrders(
                account_number=account,
            ),
        )

        if first is None:
            first = result
        else:
            first.orders.extend(result.orders)

        if not continuous or result.is_last:
            break

        page = result.next_page

    return first


def _foreign_pending_orders(
    self: "PyKis",
    account: str | KisAccountNumber,
    market: MARKET_TYPE | None = None,
    page: KisPage | None = None,
    continuous: bool = True,
) -> KisForeignPendingOrders:
    """
    한국투자증권 해외 주식 미체결 조회

    국내주식주문 -> 해외주식 미체결내역[v1_해외주식-005]
    (업데이트 날짜: 2024/04/01)

    Args:
        account (str | KisAccountNumber): 계좌번호
        market (MARKET_TYPE, optional): 시장코드
        page (KisPage, optional): 페이지 정보
        continuous (bool, optional): 연속조회 여부

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    page = (page or KisPage.first()).to(200)
    first = None

    while True:
        result = self.fetch(
            "/uapi/overseas-stock/v1/trading/inquire-nccs",
            api="VTTS3018R" if self.virtual else "TTTS3018R",
            params={
                "OVRS_EXCG_CD": get_market_code(market) if market is not None else "",
                "SORT_SQN": "DS" if self.virtual else "",
            },
            form=[
                account,
                page,
            ],
            continuous=not page.is_first,
            response_type=KisForeignPendingOrders(
                account_number=account,
            ),
        )

        if first is None:
            first = result
        else:
            first.orders.extend(result.orders)

        if not continuous or result.is_last:
            break

        page = result.next_page

    return first


FOREIGN_COUNTRY_MARKET_MAP: dict[str | None, list[MARKET_TYPE | None]] = {
    # 국가코드 -> 조회시장코드
    None: [None],
    "US": ["NASDAQ"],
    "HK": ["HKEX"],
    "CN": ["SSE", "SZSE"],
    "JP": ["TYO"],
    "VN": ["HSX", "HNX"],
}


def foreign_pending_orders(
    self: "PyKis",
    account: str | KisAccountNumber,
    country: COUNTRY_TYPE | None = None,
) -> KisForeignPendingOrders:
    """
    한국투자증권 해외 주식 미체결 조회

    국내주식주문 -> 해외주식 미체결내역[v1_해외주식-005]
    (업데이트 날짜: 2024/04/01)

    Args:
        account (str | KisAccountNumber): 계좌번호
        country (COUNTRY_TYPE, optional): 국가코드

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    markets = FOREIGN_COUNTRY_MARKET_MAP.get(country, FOREIGN_COUNTRY_MARKET_MAP[None])

    first = None

    for market in markets:
        result = _foreign_pending_orders(self, account, market)

        if first is None:
            first = result
        else:
            first.orders.extend(result.orders)

    if first is None:
        raise ValueError("Invalid country code")

    return first


def pending_orders(
    self: "PyKis",
    account: str | KisAccountNumber,
    country: COUNTRY_TYPE | None = None,
) -> KisPendingOrders:
    """
    한국투자증권 통합 미체결 조회

    국내주식주문 -> 주식정정취소가능주문조회[v1_국내주식-004] (모의투자 미지원)
    해외주식주문 -> 해외주식 미체결내역[v1_해외주식-005]
    (업데이트 날짜: 2024/04/01)

    Args:
        account (str | KisAccountNumber): 계좌번호
        country (COUNTRY_TYPE, optional): 국가코드

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    if country is None and not self.virtual:
        return KisIntegrationPendingOrders(
            self,
            account,
            domestic_pending_orders(self, account),
            foreign_pending_orders(self, account),
        )
    elif country == "KR":
        return domestic_pending_orders(self, account)
    else:
        return foreign_pending_orders(self, account, country)


def account_pending_orders(
    self: "KisAccountProtocol",
    country: COUNTRY_TYPE | None = None,
) -> KisPendingOrders:
    """
    한국투자증권 통합 미체결 조회

    국내주식주문 -> 주식정정취소가능주문조회[v1_국내주식-004] (모의투자 미지원)
    해외주식주문 -> 해외주식 미체결내역[v1_해외주식-005]
    (업데이트 날짜: 2024/04/01)

    Args:
        country (COUNTRY_TYPE, optional): 국가코드

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """

    return pending_orders(
        self.kis,
        account=self.account_number,
        country=country,
    )


def account_product_pending_orders(
    self: "KisAccountProductProtocol",
) -> KisPendingOrders:
    """
    한국투자증권 통합 미체결 조회

    국내주식주문 -> 주식정정취소가능주문조회[v1_국내주식-004] (모의투자 미지원)
    해외주식주문 -> 해외주식 미체결내역[v1_해외주식-005]
    (업데이트 날짜: 2024/04/01)

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """

    orders = pending_orders(
        self.kis,
        account=self.account_number,
        country=get_market_country(self.market),
    )

    return KisSimplePendingOrders(
        account_number=self.account_number,
        orders=[order for order in orders.orders if order.symbol == self.symbol and order.market == self.market],
    )
