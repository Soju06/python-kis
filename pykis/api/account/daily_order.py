from datetime import date, datetime, timedelta
from decimal import Decimal
from functools import cached_property
from typing import TYPE_CHECKING, Any, Iterable, Protocol, runtime_checkable
from zoneinfo import ZoneInfo

from pykis.api.account.order import (
    ORDER_CONDITION,
    ORDER_EXECUTION,
    ORDER_QUANTITY,
    ORDER_TYPE,
    KisOrder,
    KisSimpleOrder,
)
from pykis.api.base.account import KisAccountBase, KisAccountProtocol
from pykis.api.base.account_product import (
    KisAccountProductBase,
    KisAccountProductProtocol,
)
from pykis.api.stock.info import COUNTRY_TYPE
from pykis.api.stock.market import (
    MARKET_TYPE,
    KisMarketType,
    get_market_code,
    get_market_code_timezone,
    get_market_timezone,
)
from pykis.client.account import KisAccountNumber
from pykis.client.page import KisPage
from pykis.responses.dynamic import KisDynamic, KisList, KisTransform
from pykis.responses.response import KisPaginationAPIResponse
from pykis.responses.types import KisAny, KisDecimal, KisString
from pykis.utils.repr import kis_repr
from pykis.utils.timezone import TIMEZONE

if TYPE_CHECKING:
    from pykis.kis import PyKis

__all__ = [
    "KisDailyOrder",
    "KisDailyOrders",
    "daily_orders",
]


@runtime_checkable
class KisDailyOrder(KisAccountProductProtocol, Protocol):
    """한국투자증권 일별 체결내역"""

    @property
    def time(self) -> datetime:
        """시간 (현지시간)"""
        ...

    @property
    def time_kst(self) -> datetime:
        """시간 (한국시간)"""
        ...

    @property
    def timezone(self) -> ZoneInfo:
        """시간대"""
        ...

    @property
    def account_number(self) -> KisAccountNumber:
        """계좌번호"""
        ...

    @property
    def order_number(self) -> KisOrder:
        """주문번호"""
        ...

    @property
    def type(self) -> ORDER_TYPE:
        """주문유형"""
        ...

    @property
    def price(self) -> Decimal | None:
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
    def pending_quantity(self) -> ORDER_QUANTITY:
        """미체결수량"""
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

    @property
    def canceled(self) -> bool:
        """취소여부"""
        ...


@runtime_checkable
class KisDailyOrders(KisAccountProtocol, Protocol):
    """한국투자증권 일별 체결내역"""

    @property
    def account_number(self) -> KisAccountNumber:
        """계좌번호"""
        ...

    @property
    def orders(self) -> list[KisDailyOrder]:
        """일별 체결내역"""
        ...

    def __getitem__(self, key: int | KisOrder | str) -> KisDailyOrder:
        """인덱스 또는 주문번호로 주문을 조회합니다."""
        ...

    def order(self, key: KisOrder | str) -> KisDailyOrder | None:
        """주문번호 또는 종목코드로 주문을 조회합니다."""
        ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterable[KisDailyOrder]: ...


@kis_repr(
    "order_number",
    "type",
    "price",
    "qty",
    "executed_qty",
    lines="multiple",
)
class KisDailyOrderBase(KisAccountProductBase):
    """한국투자증권 일별 체결내역"""

    time: datetime
    """시간 (현지시간)"""
    time_kst: datetime
    """시간 (한국시간)"""
    timezone: ZoneInfo
    """시간대"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    order_number: KisOrder
    """주문번호"""

    name: str
    """종목명"""

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

    quantity: ORDER_QUANTITY
    """주문수량"""

    @property
    def qty(self) -> ORDER_QUANTITY:
        """주문수량"""
        return self.quantity

    executed_quantity: ORDER_QUANTITY
    """체결수량"""

    pending_quantity: ORDER_QUANTITY
    """미체결수량"""

    @property
    def executed_qty(self) -> ORDER_QUANTITY:
        """체결수량"""
        return self.executed_quantity

    @property
    def executed_amount(self) -> Decimal:
        """체결금액"""
        return (self.executed_quantity * self.price) if self.price else Decimal(0)

    @property
    def pending_qty(self) -> ORDER_QUANTITY:
        """미체결수량"""
        return self.pending_quantity

    condition: ORDER_CONDITION | None
    """주문조건"""
    execution: ORDER_EXECUTION | None
    """체결조건"""

    rejected: bool = False
    """거부여부"""
    rejected_reason: str | None = None
    """거부사유"""

    canceled: bool
    """취소여부"""


@kis_repr(
    "account_number",
    "orders",
    lines="multiple",
    field_lines={"orders": "multiple"},
)
class KisDailyOrdersBase(KisAccountBase):
    """한국투자증권 일별 체결내역"""

    account_number: KisAccountNumber
    """계좌번호"""

    orders: list[KisDailyOrder]
    """일별 체결내역"""

    def __getitem__(self, key: int | KisOrder | str) -> KisDailyOrder:
        """인덱스 또는 주문번호로 주문을 조회합니다."""
        if isinstance(key, int):
            return self.orders[key]
        elif isinstance(key, str):
            for order in self.orders:
                if order.symbol == key:
                    return order
        elif isinstance(key, KisOrder):
            for order in self.orders:
                if order.order_number == key:
                    return order

        raise KeyError(key)

    def order(self, key: KisOrder | str) -> KisDailyOrder | None:
        """주문번호 또는 종목코드로 주문을 조회합니다."""
        if isinstance(key, str):
            for order in self.orders:
                if order.symbol == key:
                    return order
        elif isinstance(key, KisOrder):
            for order in self.orders:
                if order.order_number == key:
                    return order

        return None

    def __len__(self) -> int:
        return len(self.orders)

    def __iter__(self) -> Iterable[KisDailyOrder]:
        return iter(self.orders)


DOMESTIC_EXCHANGE_CODE_MAP: dict[str, tuple[COUNTRY_TYPE, MARKET_TYPE | None, ORDER_CONDITION | None]] = {
    "01": ("KR", "KRX", None),
    "02": ("KR", "KRX", None),
    "03": ("KR", "KRX", None),
    "04": ("KR", "KRX", None),
    "05": ("KR", "KRX", None),
    "06": ("KR", "KRX", None),
    "07": ("KR", "KRX", None),
    "21": ("KR", "KRX", None),
    "51": ("HK", None, None),
    "52": ("CN", "SSE", None),
    "53": ("CN", "SZSE", None),
    "54": ("HK", None, None),
    "55": ("US", None, None),
    "56": ("JP", "TYO", None),
    "57": ("CN", "SSE", None),
    "58": ("CN", "SZSE", None),
    "59": ("VN", None, None),
    "61": ("KR", "KRX", "before"),
    "64": ("KR", "KRX", None),
    "65": ("KR", "KRX", None),
    "81": ("KR", "KRX", "extended"),
}


class KisDomesticDailyOrder(KisDynamic, KisDailyOrderBase):
    """한국투자증권 국내 일별 체결내역"""

    time: datetime
    """시간 (현지시간)"""
    time_kst: datetime = KisTransform(
        lambda x: datetime.strptime(x["ord_dt"] + x["ord_tmd"], "%Y%m%d%H%M%S").replace(tzinfo=TIMEZONE)
    )()
    """시간 (한국시간)"""
    timezone: ZoneInfo = TIMEZONE
    """시간대"""

    symbol: str = KisString["pdno"]
    """종목코드"""

    market: MARKET_TYPE = "KRX"
    """시장"""

    account_number: KisAccountNumber
    """계좌번호"""

    branch: str = KisString["ord_gno_brno"]
    """지점코드"""
    number: str = KisString["odno"]
    """주문번호"""

    @property
    def order_number(self) -> KisOrder:
        """주문번호"""
        return KisSimpleOrder.from_order(
            account_number=self.account_number,
            symbol=self.symbol,
            market=self.market,
            branch=self.branch,
            number=self.number,
            time_kst=self.time_kst,
            kis=self.kis,
        )

    name: str = KisString["prdt_name"]
    """종목명"""

    type: ORDER_TYPE = KisAny(lambda x: "buy" if x == "02" else "sell")["sll_buy_dvsn_cd"]
    """주문유형"""

    price: Decimal | None = KisDecimal["avg_prvs"]
    """체결단가"""
    unit_price: Decimal | None = KisDecimal["ord_unpr"]
    """주문단가"""

    quantity: ORDER_QUANTITY = KisDecimal["ord_qty"]
    """주문수량"""

    @property
    def qty(self) -> ORDER_QUANTITY:
        """주문수량"""
        return self.quantity

    executed_quantity: ORDER_QUANTITY = KisDecimal["tot_ccld_qty"]
    """체결수량"""

    pending_quantity: ORDER_QUANTITY = KisDecimal["rmn_qty"]
    """미체결수량"""

    condition: ORDER_CONDITION | None = None
    """주문조건"""
    execution: ORDER_EXECUTION | None = None
    """체결조건"""

    rejected: bool = KisAny(lambda x: x and x != "0")["rjct_qty"]
    """거부여부"""
    rejected_reason: str | None = None
    """거부사유"""

    canceled: bool = KisTransform(lambda x: x == "Y")["ccld_yn"]
    """취소여부"""

    def __pre_init__(self, data: dict[str, Any]) -> None:
        super().__pre_init__(data)

        country, market, condition = DOMESTIC_EXCHANGE_CODE_MAP[data["excg_dvsn_cd"]]

        self.country = country

        if market:
            self.market = market
            self.timezone = get_market_timezone(market)

        self.condition = condition

    def __post_init__(self) -> None:
        super().__post_init__()

        self.time = self.time_kst.astimezone(self.timezone)


class KisDomesticDailyOrders(KisPaginationAPIResponse, KisDailyOrdersBase):
    """한국투자증권 국내 일별 체결내역"""

    __path__ = None

    account_number: KisAccountNumber
    """계좌번호"""

    orders: list[KisDailyOrder] = KisList(KisDomesticDailyOrder)["output1"]
    """일별 체결내역"""

    def __init__(self, account_number: KisAccountNumber) -> None:
        super().__init__()
        self.account_number = account_number

    def __post_init__(self) -> None:
        super().__post_init__()

        for order in self.orders:
            if isinstance(order, KisDailyOrderBase):
                order.account_number = self.account_number

    def __kis_post_init__(self) -> None:
        super().__kis_post_init__()
        self._kis_spread(self.orders)  # type: ignore


class KisForeignDailyOrder(KisDynamic, KisDailyOrderBase):
    """한국투자증권 해외 일별 체결내역"""

    time: datetime
    """시간 (현지시간)"""
    time_kst: datetime = KisTransform(
        lambda x: datetime.strptime(x["ord_dt"] + x["ord_tmd"], "%Y%m%d%H%M%S").replace(tzinfo=TIMEZONE)
    )()
    """시간 (한국시간)"""
    timezone: ZoneInfo = KisAny(get_market_code_timezone)["ovrs_excg_cd"]
    """시간대"""

    symbol: str = KisString["pdno"]
    """종목코드"""
    market: MARKET_TYPE = KisMarketType["ovrs_excg_cd"]
    """상품유형타입"""

    account_number: KisAccountNumber
    """계좌번호"""

    branch: str = KisString["ord_gno_brno"]
    """지점코드"""
    number: str = KisString["odno"]
    """주문번호"""

    # Pylance bug: cached_property[KisOrder] type inference error.
    @cached_property
    def order_number(self) -> KisOrder:  # type: ignore
        """주문번호"""
        return KisSimpleOrder.from_order(
            account_number=self.account_number,
            symbol=self.symbol,
            market=self.market,
            branch=self.branch,
            number=self.number,
            time_kst=self.time_kst,
            kis=self.kis,
        )

    order_number: KisOrder

    name: str = KisString["prdt_name"]
    """종목명"""

    type: ORDER_TYPE = KisAny(lambda x: "buy" if x == "02" else "sell")["sll_buy_dvsn_cd"]
    """주문유형"""

    price: Decimal | None = KisDecimal["ft_ccld_unpr3"]
    """체결단가"""
    unit_price: Decimal | None = KisDecimal["ft_ord_unpr3"]
    """주문단가"""

    quantity: ORDER_QUANTITY = KisDecimal["ft_ord_qty"]
    """주문수량"""

    executed_quantity: ORDER_QUANTITY = KisDecimal["ft_ccld_qty"]
    """체결수량"""

    pending_quantity: ORDER_QUANTITY = KisDecimal["nccs_qty"]
    """미체결수량"""

    condition: ORDER_CONDITION | None = None
    """주문조건"""
    execution: ORDER_EXECUTION | None = None
    """체결조건"""

    rejected: bool = KisAny(lambda x: bool(x))["rjct_rson"]
    """거부여부"""
    rejected_reason: str | None = KisString["rjct_rson_name"]
    """거부사유"""

    canceled: bool = False
    """취소여부"""

    def __post_init__(self) -> None:
        super().__post_init__()

        self.time = self.time_kst.astimezone(self.timezone)


class KisForeignDailyOrders(KisPaginationAPIResponse, KisDailyOrdersBase):
    """한국투자증권 해외 일별 체결내역"""

    __path__ = None

    account_number: KisAccountNumber
    """계좌번호"""

    orders: list[KisDailyOrder] = KisList(KisForeignDailyOrder)["output"]
    """일별 체결내역"""

    def __init__(self, account_number: KisAccountNumber) -> None:
        super().__init__()
        self.account_number = account_number

    def __post_init__(self) -> None:
        super().__post_init__()

        for order in self.orders:
            if isinstance(order, KisDailyOrderBase):
                order.account_number = self.account_number

    def __kis_post_init__(self) -> None:
        super().__kis_post_init__()
        self._kis_spread(self.orders)  # type: ignore


class KisIntegrationDailyOrders(KisDailyOrdersBase):
    """한국투자증권 체결내역"""

    account_number: KisAccountNumber
    """계좌번호"""
    orders: list[KisDailyOrder]
    """미체결주문"""

    _orders: list[KisDailyOrders]
    """내부구현 체결내역"""

    def __init__(self, kis: "PyKis", account_number: KisAccountNumber, *orders: KisDailyOrders) -> None:
        super().__init__()
        self.kis = kis
        self.account_number = account_number
        self._orders = list(orders)
        self.orders = []

        for order in orders:
            self.orders.extend(order.orders)

        self.orders.sort(key=lambda x: x.time_kst, reverse=True)


DOMESTIC_DAILY_ORDERS_API_CODES: dict[tuple[bool, bool], str] = {
    # (실전투자여부, 최근3개월이내여부) -> API코드
    (True, True): "TTTC8001R",
    (True, False): "CTSC9115R",
    (False, True): "VTTC8001R",
    (False, False): "VTSC9115R",
}


def _domestic_daily_orders(
    self: "PyKis",
    account: str | KisAccountNumber,
    start: date,
    end: date,
    type: ORDER_TYPE | None = None,
    page: KisPage | None = None,
    continuous: bool = True,
) -> KisDomesticDailyOrders:
    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    if start > end:
        start, end = end, start

    now = datetime.now(TIMEZONE).date()

    is_recent = (now.year - start.year) * 12 - now.month <= 3

    if end.month + (now.year - end.year) * 12 - now.month > 3 and is_recent:
        raise ValueError("조회 기간은 최근 3개월 이내거나 3개월 이상이어야 합니다.")

    page = (page or KisPage.first()).to(100)
    first = None

    while True:
        result = self.fetch(
            "/uapi/domestic-stock/v1/trading/inquire-daily-ccld",
            api=DOMESTIC_DAILY_ORDERS_API_CODES[(not self.virtual, is_recent)],
            params={
                "INQR_STRT_DT": start.strftime("%Y%m%d"),
                "INQR_END_DT": end.strftime("%Y%m%d"),
                "SLL_BUY_DVSN_CD": "00" if type is None else ("02" if type == "buy" else "01"),
                "INQR_DVSN": "00",
                "PDNO": "",
                "CCLD_DVSN": "00",
                "ORD_GNO_BRNO": "",
                "ODNO": "",
                "INQR_DVSN_3": "00",
                "INQR_DVSN_1": "",
            },
            form=[
                account,
                page,
            ],
            continuous=not page.is_first,
            response_type=KisDomesticDailyOrders(
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


def domestic_daily_orders(
    self: "PyKis",
    account: str | KisAccountNumber,
    start: date,
    end: date | None = None,
) -> KisDomesticDailyOrders:
    """
    한국투자증권 국내 체결내역 조회

    국내주식주문 -> 주식일별주문체결조회[v1_국내주식-005]
    (업데이트 날짜: 2024/04/02)

    Args:
        account (str | KisAccountNumber): 계좌번호
        page (KisPage, optional): 페이지 정보
        start (date): 조회 시작일
        end (date, optional): 조회 종료일

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    if end is None:
        end = datetime.now(TIMEZONE).date()

    if start > end:
        start, end = end, start

    now = datetime.now(TIMEZONE).date()

    if (now.year - start.year) * 12 - now.month <= 3 and (now.year - end.year) * 12 - now.month <= 3:
        return _domestic_daily_orders(
            self,
            account=account,
            start=start,
            end=end,
        )

    split_start = now - timedelta(days=90)
    split_start = date(split_start.year, split_start.month, 1)

    first = _domestic_daily_orders(
        self,
        account=account,
        start=split_start,
        end=end,
    )

    first.orders.extend(
        _domestic_daily_orders(
            self,
            account=account,
            start=start,
            end=split_start - timedelta(days=1),
        ).orders
    )

    return first


def _internal_foreign_daily_orders(
    self: "PyKis",
    account: str | KisAccountNumber,
    start: date,
    end: date,
    market: MARKET_TYPE | None = None,
    page: KisPage | None = None,
    continuous: bool = True,
) -> KisForeignDailyOrders:
    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    if start > end:
        start, end = end, start

    page = (page or KisPage.first()).to(200)
    first = None

    while True:
        result = self.fetch(
            "/uapi/overseas-stock/v1/trading/inquire-ccnl",
            api="VTTS3035R" if self.virtual else "TTTS3035R",
            params={
                "PDNO": "" if self.virtual else "%",
                "ORD_STRT_DT": start.strftime("%Y%m%d"),
                "ORD_END_DT": end.strftime("%Y%m%d"),
                "SLL_BUY_DVSN": "00",
                "CCLD_NCCS_DVSN": "00",
                "OVRS_EXCG_CD": ("" if self.virtual else "%") if market is None else get_market_code(market),
                "SORT_SQN": "DS",
                "ORD_DT": "",
                "ORD_GNO_BRNO": "",
                "ODNO": "",
            },
            form=[
                account,
                page,
            ],
            continuous=not page.is_first,
            response_type=KisForeignDailyOrders(
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


def foreign_daily_orders(
    self: "PyKis",
    account: str | KisAccountNumber,
    start: date,
    end: date | None = None,
    country: COUNTRY_TYPE | None = None,
) -> KisForeignDailyOrders:
    """
    한국투자증권 해외 체결내역 조회

    국내주식주문 -> 해외주식 주문체결내역[v1_해외주식-007]
    (업데이트 날짜: 2024/04/02)

    Args:
        account (str | KisAccountNumber): 계좌번호
        page (KisPage, optional): 페이지 정보
        start (date): 조회 시작일
        end (date, optional): 조회 종료일
        country (COUNTRY_TYPE, optional): 국가코드

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    if end is None:
        end = datetime.now(TIMEZONE).date()

    markets = FOREIGN_COUNTRY_MARKET_MAP.get(country, FOREIGN_COUNTRY_MARKET_MAP[None])

    first = None

    for market in markets:
        result = _internal_foreign_daily_orders(
            self,
            account=account,
            start=start,
            end=end,
            market=market,
        )

        if first is None:
            first = result
        else:
            first.orders.extend(result.orders)

    if first is None:
        raise ValueError("Invalid country code")

    first.orders.sort(key=lambda x: x.time_kst, reverse=True)

    return first


def daily_orders(
    self: "PyKis",
    account: str | KisAccountNumber,
    start: date,
    end: date | None = None,
    country: COUNTRY_TYPE | None = None,
) -> KisDailyOrders:
    """
    한국투자증권 통합일별 체결내역 조회

    국내주식주문 -> 주식일별주문체결조회[v1_국내주식-005]
    국내주식주문 -> 해외주식 주문체결내역[v1_해외주식-007]

    Args:
        account (str | KisAccountNumber): 계좌번호
        start (date): 조회 시작일
        end (date, optional): 조회 종료
        country (COUNTRY_TYPE, optional): 국가코드

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    if country is None:
        return KisIntegrationDailyOrders(
            self,
            account,
            domestic_daily_orders(
                self,
                account=account,
                start=start,
                end=end,
            ),
            foreign_daily_orders(
                self,
                account=account,
                start=start,
                end=end,
            ),
        )
    elif country == "KR":
        return domestic_daily_orders(
            self,
            account=account,
            start=start,
            end=end,
        )
    else:
        return foreign_daily_orders(
            self,
            account=account,
            start=start,
            end=end,
            country=country,
        )


def account_daily_orders(
    self: "KisAccountProtocol",
    start: date,
    end: date | None = None,
    country: COUNTRY_TYPE | None = None,
) -> KisDailyOrders:
    """
    한국투자증권 통합일별 체결내역 조회

    국내주식주문 -> 주식일별주문체결조회[v1_국내주식-005]
    국내주식주문 -> 해외주식 주문체결내역[v1_해외주식-007]

    Args:
        start (date): 조회 시작일
        end (date): 조회 종료일
        country (COUNTRY_TYPE, optional): 국가코드

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    return daily_orders(
        self.kis,
        account=self.account_number,
        start=start,
        end=end,
        country=country,
    )
