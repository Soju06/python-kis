from datetime import date, datetime
from decimal import Decimal
from functools import cached_property
from typing import TYPE_CHECKING, Iterable, Protocol, runtime_checkable
from zoneinfo import ZoneInfo

from pykis.api.account.order import ORDER_QUANTITY
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
)
from pykis.client.account import KisAccountNumber
from pykis.client.page import KisPage
from pykis.responses.dynamic import KisDynamic, KisList, KisTransform
from pykis.responses.response import KisPaginationAPIResponse
from pykis.responses.types import KisAny, KisDecimal, KisString
from pykis.utils.math import safe_divide
from pykis.utils.repr import kis_repr
from pykis.utils.timezone import TIMEZONE

if TYPE_CHECKING:
    from pykis.kis import PyKis

__all__ = [
    "KisOrderProfit",
    "KisOrderProfits",
    "order_profits",
]


@runtime_checkable
class KisOrderProfit(KisAccountProductProtocol, Protocol):
    """한국투자증권 일별 매매손익"""

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
    def symbol(self) -> str:
        """종목코드"""
        ...

    @property
    def market(self) -> MARKET_TYPE:
        """상품유형타입"""
        ...

    @property
    def account_number(self) -> KisAccountNumber:
        """계좌번호"""
        ...

    @property
    def name(self) -> str:
        """종목명"""
        ...

    @property
    def buy_price(self) -> Decimal:
        """매수단가"""
        ...

    @property
    def sell_price(self) -> Decimal:
        """매도단가"""
        ...

    @property
    def buy_amount(self) -> Decimal:
        """매수금액"""
        ...

    @property
    def sell_amount(self) -> Decimal:
        """매도금액"""
        ...

    @property
    def quantity(self) -> ORDER_QUANTITY:
        """매도수량"""
        ...

    @property
    def qty(self) -> ORDER_QUANTITY:
        """매도수량"""
        ...

    @property
    def profit(self) -> Decimal:
        """손익금액"""
        ...

    @property
    def profit_rate(self) -> Decimal:
        """손익률 (-100 ~ 100)"""
        ...

    @property
    def exchange_rate(self) -> Decimal:
        """당일환율"""
        ...


@runtime_checkable
class KisOrderProfits(KisAccountProtocol, Protocol):
    """한국투자증권 일별 매매손익"""

    @property
    def account_number(self) -> KisAccountNumber:
        """계좌번호"""
        ...

    @property
    def orders(self) -> list[KisOrderProfit]:
        """일별 체결내역"""
        ...

    @property
    def fees(self) -> Decimal:
        """수수료"""
        ...

    @property
    def buy_amount(self) -> Decimal:
        """매수금액"""
        ...

    @property
    def sell_amount(self) -> Decimal:
        """매도금액"""
        ...

    @property
    def profit(self) -> Decimal:
        """손익금액"""
        ...

    def __getitem__(self, key: int | str) -> KisOrderProfit:
        """인덱스 또는 주문번호로 주문을 조회합니다."""
        ...

    def order(self, key: str) -> KisOrderProfit | None:
        """주문번호 또는 종목코드로 주문을 조회합니다."""
        ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterable[KisOrderProfit]: ...


@kis_repr(
    "time_kst",
    "market",
    "symbol",
    "name",
    "buy_price",
    "sell_price",
    "qty",
    "profit",
    "profit_rate",
    lines="single",
)
class KisOrderProfitRepr:
    """한국투자증권 일별 매매손익"""


class KisOrderProfitBase(KisOrderProfitRepr, KisAccountProductBase):
    """한국투자증권 일별 매매손익"""

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

    name: str
    """종목명"""

    buy_price: Decimal
    """매수단가"""
    sell_price: Decimal
    """매도단가"""

    buy_amount: Decimal
    """매수금액"""
    sell_amount: Decimal
    """매도금액"""

    quantity: ORDER_QUANTITY
    """매도수량"""

    @property
    def qty(self) -> ORDER_QUANTITY:
        """매도수량"""
        return self.quantity

    @property
    def profit(self) -> Decimal:
        """손익금액"""
        return self.sell_amount - self.buy_amount

    @property
    def profit_rate(self) -> Decimal:
        """손익률 (-100 ~ 100)"""
        return safe_divide(self.profit, self.buy_amount) * 100

    exchange_rate: Decimal
    """당일환율"""


@kis_repr(
    "account_number",
    "buy_amount",
    "sell_amount",
    "profit",
    "orders",
    lines="multiple",
    field_lines={"orders": "multiple"},
)
class KisOrderProfitsRepr:
    """한국투자증권 일별 매매손익"""


class KisOrderProfitsBase(KisOrderProfitsRepr, KisAccountBase):
    """한국투자증권 일별 매매손익"""

    account_number: KisAccountNumber
    """계좌번호"""

    orders: list[KisOrderProfit]
    """일별 체결내역"""

    fees: Decimal
    """수수료"""

    @property
    def buy_amount(self) -> Decimal:
        """매수금액"""
        return Decimal(sum(order.buy_amount * order.exchange_rate for order in self.orders))

    @property
    def sell_amount(self) -> Decimal:
        """매도금액"""
        return Decimal(sum(order.sell_amount * order.exchange_rate for order in self.orders))

    @property
    def profit(self) -> Decimal:
        """손익금액"""
        return Decimal(sum(order.profit * order.exchange_rate for order in self.orders))

    def __getitem__(self, key: int | str) -> KisOrderProfit:
        """인덱스 또는 주문번호로 주문을 조회합니다."""
        if isinstance(key, int):
            return self.orders[key]
        elif isinstance(key, str):
            for order in self.orders:
                if order.symbol == key:
                    return order

        raise KeyError(key)

    def order(self, key: str) -> KisOrderProfit | None:
        """주문번호 또는 종목코드로 주문을 조회합니다."""
        if isinstance(key, str):
            for order in self.orders:
                if order.symbol == key:
                    return order

        return None

    def __len__(self) -> int:
        return len(self.orders)

    def __iter__(self) -> Iterable[KisOrderProfit]:
        return iter(self.orders)


class KisDomesticOrderProfit(KisDynamic, KisOrderProfitBase):
    """한국투자증권 국내 일별 매매손익"""

    time: datetime
    """시간 (현지시간)"""
    time_kst: datetime = KisTransform(lambda x: datetime.strptime(x["trad_dt"], "%Y%m%d").replace(tzinfo=TIMEZONE))()
    """시간 (한국시간)"""
    timezone: ZoneInfo = TIMEZONE
    """시간대"""

    symbol: str = KisString["pdno"]
    """종목코드"""
    market: MARKET_TYPE = "KRX"
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    name: str = KisString["prdt_name"]
    """종목명"""

    buy_price: Decimal = KisDecimal["pchs_unpr"]
    """매수단가"""
    sell_price: Decimal = KisDecimal["sll_pric"]
    """매도단가"""

    @property
    def buy_amount(self) -> Decimal:
        """매수금액"""
        return self.buy_price * self.quantity

    sell_amount: Decimal = KisDecimal["sll_amt"]
    """매도금액"""

    quantity: ORDER_QUANTITY = KisDecimal["sll_qty"]
    """매도수량"""

    exchange_rate: Decimal = Decimal(1)
    """당일환율"""


class KisDomesticOrderProfits(KisPaginationAPIResponse, KisOrderProfitsBase):
    """한국투자증권 국내 일별 매매손익"""

    __path__ = None

    account_number: KisAccountNumber
    """계좌번호"""

    orders: list[KisOrderProfit] = KisList(KisDomesticOrderProfit)["output1"]
    """일별 체결내역"""

    fees: Decimal = KisAny(lambda x: Decimal(x["tot_fee"]))["output2"]
    """수수료"""

    def __init__(self, account_number: KisAccountNumber):
        super().__init__()
        self.account_number = account_number

    def __post_init__(self):
        super().__post_init__()

        orders = []

        for order in self.orders:
            if order.quantity <= 0:
                continue

            if isinstance(order, KisDomesticOrderProfit):
                order.account_number = self.account_number

            orders.append(order)

        self.orders = orders

    def __kis_post_init__(self):
        super().__kis_post_init__()
        self._kis_spread(self.orders)  # type: ignore


class KisForeignOrderProfit(KisDynamic, KisOrderProfitBase):
    """한국투자증권 해외 일별 매매손익"""

    time: datetime
    """시간 (현지시간)"""
    time_kst: datetime = KisTransform(lambda x: datetime.strptime(x["trad_day"], "%Y%m%d").replace(tzinfo=TIMEZONE))()
    """시간 (한국시간)"""
    timezone: ZoneInfo = KisAny(get_market_code_timezone)["ovrs_excg_cd"]
    """시간대"""

    symbol: str = KisString["ovrs_pdno"]
    """종목코드"""
    market: MARKET_TYPE = KisMarketType["ovrs_excg_cd"]
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    name: str = KisString["ovrs_item_name"]
    """종목명"""

    buy_price: Decimal = KisDecimal["pchs_avg_pric"]
    """매수단가"""
    sell_price: Decimal = KisDecimal["avg_sll_unpr"]
    """매도단가"""

    buy_amount: Decimal = KisDecimal["frcr_pchs_amt1"]
    """매수금액"""
    sell_amount: Decimal = KisDecimal["frcr_sll_amt_smtl1"]
    """매도금액"""

    quantity: ORDER_QUANTITY = KisDecimal["slcl_qty"]
    """매도수량"""

    exchange_rate: Decimal = KisDecimal["frst_bltn_exrt"]
    """당일환율"""

    def __post_init__(self):
        super().__post_init__()
        self.time = self.time_kst.astimezone(self.timezone)


class KisForeignOrderProfits(KisPaginationAPIResponse, KisOrderProfitsBase):
    """한국투자증권 해외 일별 매매손익"""

    __path__ = None

    account_number: KisAccountNumber
    """계좌번호"""

    orders: list[KisOrderProfit] = KisList(KisForeignOrderProfit)["output1"]
    """일별 체결내역"""

    _start: date
    _end: date
    _country: COUNTRY_TYPE | None = None

    # Pylance bug: cached_property[Decimal] type inference error.
    @cached_property
    def fees(self) -> Decimal:  # type: ignore
        """
        수수료 조회 (모의투자 미지원)

        국내주식주문 -> 해외주식 기간손익[v1_해외주식-032]
        """
        return foreign_order_fees(
            self.kis,
            account=self.account_number,
            start=self._start,
            end=self._end,
            country=self._country,
        )

    fees: Decimal

    def __init__(
        self,
        account_number: KisAccountNumber,
        start: date,
        end: date,
        country: COUNTRY_TYPE | None = None,
    ):
        super().__init__()
        self.account_number = account_number
        self._start = start
        self._end = end
        self._country = country

    def __post_init__(self):
        super().__post_init__()

        orders = []

        for order in self.orders:
            if order.quantity <= 0:
                continue

            if isinstance(order, KisForeignOrderProfit):
                order.account_number = self.account_number
            orders.append(order)

        self.orders = orders

    def __kis_post_init__(self):
        super().__kis_post_init__()
        self._kis_spread(self.orders)  # type: ignore


class KisIntegrationOrderProfits(KisOrderProfitsBase):
    """한국투자증권 통합 매매손익"""

    account_number: KisAccountNumber
    """계좌번호"""
    orders: list[KisOrderProfit]
    """매매손익"""

    @property
    def fees(self) -> Decimal:
        """수수료"""
        return Decimal(sum(orders.fees for orders in self._orders))

    _orders: list[KisOrderProfits]
    """내부구현 매매손익"""

    def __init__(self, kis: "PyKis", account_number: KisAccountNumber, *orders: KisOrderProfits):
        super().__init__()
        self.kis = kis
        self.account_number = account_number
        self._orders = list(orders)
        self.orders = []

        for order in orders:
            self.orders.extend(order.orders)

        self.orders.sort(key=lambda x: x.time_kst, reverse=True)


def domestic_order_profits(
    self: "PyKis",
    account: str | KisAccountNumber,
    start: date,
    end: date | None = None,
    page: KisPage | None = None,
    continuous: bool = True,
) -> KisDomesticOrderProfits:
    """
    한국투자증권 국내 기간 손익 조회

    국내주식주문 -> 기간별매매손익현황조회[v1_국내주식-060] (모의투자 미지원)
    (업데이트 날짜: 2024/04/03)

    Args:
        account (str | KisAccountNumber): 계좌번호
        start (date): 조회 시작일
        end (date | None, optional): 조회 종료일
        page (KisPage, optional): 페이지 정보
        continuous (bool, optional): 연속조회 여부

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    if self.virtual:
        raise NotImplementedError("모의투자에서는 국내 기간 손익 조회를 지원하지 않습니다.")

    if end is None:
        end = datetime.now(TIMEZONE).date()

    if start > end:
        start, end = end, start

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    page = (page or KisPage.first()).to(100)
    first = None

    while True:
        result = self.fetch(
            "/uapi/domestic-stock/v1/trading/inquire-period-trade-profit",
            api="TTTC8715R",
            params={
                "SORT_DVSN": "00",
                "PDNO": "",
                "INQR_STRT_DT": start.strftime("%Y%m%d"),
                "INQR_END_DT": end.strftime("%Y%m%d"),
                "CBLC_DVSN": "00",
            },
            form=[
                account,
                page,
            ],
            continuous=not page.is_first,
            response_type=KisDomesticOrderProfits(
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


FOREIGN_ORDER_PROFIT_MARKET_MAP: dict[COUNTRY_TYPE, MARKET_TYPE] = {
    "US": "NASDAQ",
    "HK": "HKEX",
    "CN": "SSE",
    "JP": "TYO",
    "VN": "HNX",
}


def foreign_order_profits(
    self: "PyKis",
    account: str | KisAccountNumber,
    start: date,
    end: date | None = None,
    country: COUNTRY_TYPE | None = None,
    page: KisPage | None = None,
    continuous: bool = True,
) -> KisForeignOrderProfits:
    """
    한국투자증권 해외 기간 손익 조회

    국내주식주문 -> 해외주식 기간손익[v1_해외주식-032] (모의투자 미지원)
    (업데이트 날짜: 2024/04/03)

    Args:
        account (str | KisAccountNumber): 계좌번호
        start (date): 조회 시작일
        end (date | None, optional): 조회 종료일
        country (COUNTRY_TYPE, optional): 국가
        page (KisPage, optional): 페이지 정보
        continuous (bool, optional): 연속조회 여부

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    if self.virtual:
        raise NotImplementedError("모의투자에서는 해외 기간 손익 조회를 지원하지 않습니다.")

    if end is None:
        end = datetime.now(TIMEZONE).date()

    if start > end:
        start, end = end, start

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    page = (page or KisPage.first()).to(200)
    first = None

    while True:
        result = self.fetch(
            "/uapi/overseas-stock/v1/trading/inquire-period-profit",
            api="TTTS3039R",
            params={
                "OVRS_EXCG_CD": get_market_code(FOREIGN_ORDER_PROFIT_MARKET_MAP[country]) if country else "",
                "NATN_CD": "",
                "CRCY_CD": "",
                "PDNO": "",
                "INQR_STRT_DT": start.strftime("%Y%m%d"),
                "INQR_END_DT": end.strftime("%Y%m%d"),
                "WCRC_FRCR_DVSN_CD": "01",
            },
            form=[
                account,
                page,
            ],
            continuous=not page.is_first,
            response_type=KisForeignOrderProfits(
                account_number=account,
                start=start,
                end=end,
                country=country,
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


def foreign_order_fees(
    self: "PyKis",
    account: str | KisAccountNumber,
    start: date,
    end: date | None = None,
    country: COUNTRY_TYPE | None = None,
) -> Decimal:
    """
    한국투자증권 해외 기간 손익 수수료 조회

    국내주식주문 -> 해외주식 기간손익[v1_해외주식-032] (모의투자 미지원)
    (업데이트 날짜: 2024/04/03)

    Args:
        account (str | KisAccountNumber): 계좌번호
        start (date): 조회 시작일
        end (date): 조회 종료일
        country (COUNTRY_TYPE, optional): 국가

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    if self.virtual:
        raise NotImplementedError("모의투자에서는 해외 기간 손익 조회를 지원하지 않습니다.")

    if end is None:
        end = datetime.now(TIMEZONE).date()

    if start > end:
        start, end = end, start

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    result = self.fetch(
        "/uapi/overseas-stock/v1/trading/inquire-period-profit",
        api="TTTS3039R",
        params={
            "OVRS_EXCG_CD": get_market_code(FOREIGN_ORDER_PROFIT_MARKET_MAP[country]) if country else "",
            "NATN_CD": "",
            "CRCY_CD": "",
            "PDNO": "",
            "INQR_STRT_DT": start.strftime("%Y%m%d"),
            "INQR_END_DT": end.strftime("%Y%m%d"),
            "WCRC_FRCR_DVSN_CD": "02",
            "CTX_AREA_FK200": "",
            "CTX_AREA_NK200": "",
        },
        form=[account],
    )

    return Decimal(result.output2.smtl_fee1)


def order_profits(
    self: "PyKis",
    account: str | KisAccountNumber,
    start: date,
    end: date | None = None,
    country: COUNTRY_TYPE | None = None,
) -> KisOrderProfits:
    """
    한국투자증권 통합 기간 손익 조회

    국내주식주문 -> 기간별매매손익현황조회[v1_국내주식-060] (모의투자 미지원)
    국내주식주문 -> 해외주식 기간손익[v1_해외주식-032] (모의투자 미지원)
    (업데이트 날짜: 2024/04/03)

    Args:
        account (str | KisAccountNumber): 계좌번호
        start (date): 조회 시작일
        end (date | None, optional): 조회 종료일
        country (COUNTRY_TYPE, optional): 국가

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    if country is None:
        return KisIntegrationOrderProfits(
            self,
            account,
            domestic_order_profits(
                self,
                account=account,
                start=start,
                end=end,
            ),
            foreign_order_profits(
                self,
                account=account,
                start=start,
                end=end,
            ),
        )
    elif country == "KR":
        return domestic_order_profits(
            self,
            account=account,
            start=start,
            end=end,
        )
    else:
        return foreign_order_profits(
            self,
            account=account,
            start=start,
            end=end,
            country=country,
        )


def account_order_profits(
    self: "KisAccountProtocol",
    start: date,
    end: date | None = None,
    country: COUNTRY_TYPE | None = None,
) -> KisOrderProfits:
    """
    한국투자증권 통합 기간 손익 조회

    국내주식주문 -> 기간별매매손익현황조회[v1_국내주식-060] (모의투자 미지원)
    국내주식주문 -> 해외주식 기간손익[v1_해외주식-032] (모의투자 미지원)
    (업데이트 날짜: 2024/04/03)

    Args:
        account (str | KisAccountNumber): 계좌번호
        start (date): 조회 시작일
        end (date): 조회 종료일
        country (COUNTRY_TYPE, optional): 국가

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    return order_profits(
        self.kis,
        account=self.account_number,
        start=start,
        end=end,
        country=country,
    )
