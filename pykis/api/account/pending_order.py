from decimal import Decimal
from typing import TYPE_CHECKING

from pykis.api.account.order import (
    ORDER_CONDITION,
    ORDER_EXECUTION,
    ORDER_TYPE,
    KisOrderNumber,
    resolve_domestic_order_condition,
)
from pykis.api.base.account import KisAccountBase
from pykis.api.base.account_product import KisAccountProductBase
from pykis.api.stock.market import CURRENCY_TYPE, MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.client.page import KisPage
from pykis.responses.dynamic import KisDynamic, KisList
from pykis.responses.response import KisPaginationAPIResponse
from pykis.responses.types import KisAny, KisBool, KisDecimal, KisString

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisPendingOrder(KisDynamic, KisAccountProductBase):
    """한국투자증권 미체결 주식"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""
    order_number: KisOrderNumber
    """주문번호"""

    @property
    def account_number(self) -> KisAccountNumber:
        """계좌번호"""
        return self.order_number.account_number

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
    def remaining_quantity(self) -> Decimal:
        """미체결수량"""
        return self.quantity - self.executed_quantity

    @property
    def remaining_qty(self) -> Decimal:
        """미체결수량"""
        return self.remaining_quantity

    condition: ORDER_CONDITION | None
    """주문조건"""
    execution: ORDER_EXECUTION | None
    """체결조건"""

    rejected: bool
    """거부여부"""
    rejected_reason: str | None
    """거부사유"""

    cancelled: bool
    """취소여부"""

    currency: CURRENCY_TYPE
    """통화"""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(order_number={self.order_number!r}, type={self.type!r}, price={self.price!r}, quantity={self.quantity!r}, executed_quantity={self.executed_quantity!r}, condition={self.condition!r}, execution={self.execution!r})"


class KisPendingOrders(KisDynamic, KisAccountBase):
    """한국투자증권 미체결 주식"""

    account_number: KisAccountNumber
    """계좌번호"""

    orders: list[KisPendingOrder]
    """미체결주문"""

    @property
    def quantity(self) -> Decimal:
        """총주문수량 (취소된 주문 제외)"""
        return Decimal(sum(order.quantity for order in self.orders if not order.cancelled))

    @property
    def qty(self) -> Decimal:
        """총주문수량 (취소된 주문 제외)"""
        return self.quantity

    @property
    def executed_quantity(self) -> Decimal:
        """총체결수량"""
        return Decimal(sum(order.executed_quantity for order in self.orders))

    @property
    def executed_qty(self) -> Decimal:
        """총체결수량"""
        return self.executed_quantity

    @property
    def executed_amount(self) -> Decimal:
        """총체결금액"""
        return Decimal(sum(order.executed_amount for order in self.orders))

    def __repr__(self) -> str:
        nl = "\n    "
        nll = "\n        "
        return f"{self.__class__.__name__}({nl}account_number={self.account_number!r},{nl}quantity={self.quantity!r},{nl}executed_quantity={self.executed_quantity!r},{nl}orders=[{nll}{f',{nll}'.join(map(repr, self.orders))}{nl}]\n)"


class KisDomesticPendingOrder(KisPendingOrder, KisAccountProductBase):
    """한국투자증권 국내 미체결 주식"""

    symbol: str = KisString["pdno"]
    """종목코드"""
    market: MARKET_TYPE = "KRX"
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    order_number: KisOrderNumber
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

    cancelled: bool = KisBool["cncl_yn"]
    """취소여부"""

    currency: CURRENCY_TYPE = "KRW"
    """통화"""

    def __post_init__(self):
        super().__post_init__()

        has_price, self.condition, self.execution = resolve_domestic_order_condition(
            self.__data__["ord_dvsn_cd"]
        )

        if not has_price:
            self.unit_price = None

    def __kis_post_init__(self):
        super().__kis_post_init__()

        self.order_number = KisOrderNumber(
            kis=self.kis,
            symbol=self.symbol,
            market=self.market,
            account_number=self.account_number,
            branch=self.__data__["ord_gno_brno"],
            number=self.__data__["odno"],
        )


class KisDomesticPendingOrders(KisPaginationAPIResponse, KisPendingOrders):
    """한국투자증권 국내 미체결 주식"""

    __path__ = None

    account_number: KisAccountNumber
    """계좌번호"""

    orders: list[KisDomesticPendingOrder] = KisList(KisDomesticPendingOrder)("output")
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
