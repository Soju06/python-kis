from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any
from zoneinfo import ZoneInfo

from pykis.__env__ import TIMEZONE
from pykis.api.account.order import (
    ORDER_CONDITION,
    ORDER_EXECUTION,
    ORDER_TYPE,
    KisOrder,
    KisOrderNumber,
    resolve_domestic_order_condition,
)
from pykis.api.base.account import KisAccountBase
from pykis.api.base.account_product import KisAccountProductBase
from pykis.api.stock.info import COUNTRY_TYPE
from pykis.api.stock.market import CURRENCY_TYPE, MARKET_TYPE, get_market_timezone
from pykis.client.account import KisAccountNumber
from pykis.client.page import KisPage
from pykis.responses.dynamic import KisDynamic, KisList
from pykis.responses.response import KisPaginationAPIResponse
from pykis.responses.types import KisAny, KisDecimal, KisString
from pykis.utils.repr import kis_repr

if TYPE_CHECKING:
    from pykis.kis import PyKis


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
class KisPendingOrder(KisDynamic, KisAccountProductBase):
    """한국투자증권 미체결 주식"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    time: datetime
    """주문시각"""
    time_kst: datetime
    """주문시각(KST)"""
    timezone: ZoneInfo
    """시간대"""

    order_number: KisOrder
    """주문번호"""

    @property
    def name(self) -> str:
        """종목명"""
        return self.info.name

    type: ORDER_TYPE
    """주문유형"""

    price: Decimal | None
    """체결단가"""
    unit_price: Decimal | None
    """주문단가"""

    @property
    def order_price(self) -> Decimal | None:
        """주문단가"""
        return self.unit_price

    quantity: Decimal
    """주문수량"""

    @property
    def qty(self) -> Decimal:
        """주문수량"""
        return self.quantity

    executed_quantity: Decimal
    """체결수량"""

    orderable_quantity: Decimal
    """주문가능수량"""

    @property
    def executed_qty(self) -> Decimal:
        """체결수량"""
        return self.executed_quantity

    @property
    def executed_amount(self) -> Decimal:
        """체결금액"""
        return (self.executed_quantity * self.price) if self.price else Decimal(0)

    @property
    def orderable_qty(self) -> Decimal:
        """주문가능수량"""
        return self.orderable_quantity

    @property
    def pending_quantity(self) -> Decimal:
        """미체결수량"""
        return self.quantity - self.executed_quantity

    @property
    def pending_qty(self) -> Decimal:
        """미체결수량"""
        return self.pending_quantity

    condition: ORDER_CONDITION | None
    """주문조건"""
    execution: ORDER_EXECUTION | None
    """체결조건"""

    rejected: bool
    """거부여부"""
    rejected_reason: str | None
    """거부사유"""

    currency: CURRENCY_TYPE
    """통화"""


@kis_repr(
    "account_number",
    "orders",
    lines="multiple",
    field_lines={"orders": "multiple"},
)
class KisPendingOrders(KisDynamic, KisAccountBase):
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

    def __iter__(self):
        return iter(self.orders)


class KisDomesticPendingOrder(KisPendingOrder, KisAccountProductBase):
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

    price: Decimal | None = KisDecimal["ord_unpr"]
    """체결단가"""
    unit_price: Decimal | None = KisDecimal["ord_unpr"]
    """주문단가"""

    quantity: Decimal = KisDecimal["ord_qty"]
    """주문수량"""

    executed_quantity: Decimal = KisDecimal["tot_ccld_qty"]
    """체결수량"""

    orderable_quantity: Decimal = KisDecimal["psbl_qty"]
    """주문가능수량"""

    condition: ORDER_CONDITION | None
    """주문조건"""
    execution: ORDER_EXECUTION | None
    """체결조건"""

    rejected: bool = False
    """거부여부"""
    rejected_reason: str | None = None
    """거부사유"""

    currency: CURRENCY_TYPE = "KRW"
    """통화"""

    def __pre_init__(self, data: dict[str, Any]):
        super().__pre_init__(data)

        self.time_kst = self.time = datetime.combine(
            datetime.now(TIMEZONE).date(),
            datetime.strptime(data["ord_tmd"], "%H%M%S").time(),
            tzinfo=TIMEZONE,
        )

    def __post_init__(self):
        super().__post_init__()

        has_price, self.condition, self.execution = resolve_domestic_order_condition(
            self.__data__["ord_dvsn_cd"]
        )

        if not has_price:
            self.unit_price = None

    def __kis_post_init__(self):
        super().__kis_post_init__()

        self.order_number = KisOrder(
            kis=self.kis,
            symbol=self.symbol,
            market=self.market,
            account_number=self.account_number,
            branch=self.__data__["ord_gno_brno"],
            number=self.__data__["odno"],
            time_kst=self.time_kst,
        )


class KisDomesticPendingOrders(KisPaginationAPIResponse, KisPendingOrders):
    """한국투자증권 국내 미체결 주식"""

    __path__ = None

    account_number: KisAccountNumber
    """계좌번호"""

    orders: list[KisDomesticPendingOrder] = KisList(KisDomesticPendingOrder)["output"]
    """미체결주문"""

    def __init__(self, account_number: KisAccountNumber):
        super().__init__()
        self.account_number = account_number

    def __post_init__(self) -> None:
        super().__post_init__()

        for order in self.orders:
            order.account_number = self.account_number

    def __kis_post_init__(self):
        super().__kis_post_init__()
        self._kis_spread(self.orders)


class KisOverseasPendingOrder(KisPendingOrder, KisAccountProductBase):
    """한국투자증권 해외 미체결 주식"""

    symbol: str = KisString["pdno"]
    """종목코드"""
    market: MARKET_TYPE = KisString["ovrs_excg_cd"]
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    time: datetime
    """주문시각"""
    time_kst: datetime
    """주문시각(KST)"""
    timezone: ZoneInfo = KisAny(get_market_timezone)["ovrs_excg_cd"]
    """시간대"""

    order_number: KisOrder
    """주문번호"""

    type: ORDER_TYPE = KisAny(lambda x: "buy" if x == "02" else "sell")["sll_buy_dvsn_cd"]
    """주문유형"""

    price: Decimal | None = KisDecimal["ft_ccld_unpr3"]
    """체결단가"""
    unit_price: Decimal | None = KisDecimal["ft_ord_unpr3"]
    """주문단가"""

    quantity: Decimal = KisDecimal["ft_ord_qty"]
    """주문수량"""

    executed_quantity: Decimal = KisDecimal["ft_ccld_qty"]
    """체결수량"""

    orderable_quantity: Decimal = KisDecimal["nccs_qty"]
    """주문가능수량"""

    condition: ORDER_CONDITION | None = None
    """주문조건"""
    execution: ORDER_EXECUTION | None = None
    """체결조건"""

    rejected: bool = KisAny(lambda x: bool(x))["rjct_rson"]
    """거부여부"""
    rejected_reason: str | None = KisAny(lambda x: x if x else None)["rjct_rson_name"]
    """거부사유"""

    currency: CURRENCY_TYPE = KisString["tr_crcy_cd"]
    """통화"""

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

        self.order_number = KisOrder(
            kis=self.kis,
            symbol=self.symbol,
            market=self.market,
            account_number=self.account_number,
            branch=self.__data__["ord_gno_brno"],
            number=self.__data__["odno"],
            time_kst=self.time_kst,
        )


class KisOverseasPendingOrders(KisPaginationAPIResponse, KisPendingOrders):
    """한국투자증권 해외 미체결 주식"""

    __path__ = None

    account_number: KisAccountNumber
    """계좌번호"""

    orders: list[KisOverseasPendingOrder] = KisList(KisOverseasPendingOrder)["output"]
    """미체결주문"""

    def __init__(self, account_number: KisAccountNumber):
        super().__init__()
        self.account_number = account_number

    def __post_init__(self) -> None:
        super().__post_init__()

        for order in self.orders:
            order.account_number = self.account_number

    def __kis_post_init__(self):
        super().__kis_post_init__()
        self._kis_spread(self.orders)


class KisIntegrationPendingOrders(KisPendingOrders):
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


def _overseas_pending_orders(
    self: "PyKis",
    account: str | KisAccountNumber,
    market: MARKET_TYPE | None = None,
    page: KisPage | None = None,
    continuous: bool = True,
) -> KisOverseasPendingOrders:
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
                "OVRS_EXCG_CD": market or "",
                "SORT_SQN": "DS" if self.virtual else "",
            },
            form=[
                account,
                page,
            ],
            continuous=not page.is_first,
            response_type=KisOverseasPendingOrders(
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


OVERSEAS_COUNTRY_MARKET_MAP: dict[str | None, list[MARKET_TYPE | None]] = {
    # 국가코드 -> 조회시장코드
    None: [None],
    "US": ["NASD"],
    "HK": ["SEHK"],
    "CN": ["SHAA", "SZAA"],
    "JP": ["TKSE"],
    "VN": ["VNSE", "HASE"],
}


def overseas_pending_orders(
    self: "PyKis",
    account: str | KisAccountNumber,
    country: COUNTRY_TYPE | None = None,
) -> KisOverseasPendingOrders:
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
    markets = OVERSEAS_COUNTRY_MARKET_MAP.get(country, OVERSEAS_COUNTRY_MARKET_MAP[None])

    first = None

    for market in markets:
        result = _overseas_pending_orders(self, account, market)

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

    if country is None:
        return KisIntegrationPendingOrders(
            self,
            account,
            domestic_pending_orders(self, account),
            overseas_pending_orders(self, account),
        )
    elif country == "KR":
        return domestic_pending_orders(self, account)
    else:
        return overseas_pending_orders(self, account, country)