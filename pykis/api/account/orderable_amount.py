from decimal import Decimal
from functools import cached_property
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

from pykis.api.account.order import (
    DOMESTIC_ORDER_CONDITION,
    ORDER_CONDITION,
    ORDER_EXECUTION,
    ORDER_PRICE,
    ORDER_QUANTITY,
    ensure_price,
    order_condition,
)
from pykis.api.base.account_product import (
    KisAccountProductBase,
    KisAccountProductProtocol,
)
from pykis.api.stock.market import MARKET_TYPE, get_market_code
from pykis.api.stock.quote import quote
from pykis.client.account import KisAccountNumber
from pykis.responses.response import (
    KisAPIResponse,
    KisResponseProtocol,
    raise_not_found,
)
from pykis.responses.types import KisDecimal
from pykis.utils.repr import kis_repr

if TYPE_CHECKING:
    from pykis.api.base.account import KisAccountProtocol
    from pykis.kis import PyKis

__all__ = [
    "KisOrderableAmount",
    "KisOrderableAmountResponse",
    "orderable_amount",
]


@runtime_checkable
class KisOrderableAmount(KisAccountProductProtocol, Protocol):
    """한국투자증권 주문가능금액"""

    @property
    def price(self) -> Decimal | None:
        """주문단가"""
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
    def unit_price(self) -> Decimal:
        """계산단가"""
        ...

    @property
    def amount(self) -> Decimal:
        """주문가능금액 (통화)"""
        ...

    @property
    def quantity(self) -> ORDER_QUANTITY:
        """주문가능수량 (통화)"""
        ...

    @property
    def qty(self) -> ORDER_QUANTITY:
        """주문가능수량"""
        ...

    @property
    def foreign_amount(self) -> Decimal:
        """
        주문가능금액 (통합)

        국내주식의 경우, 원화주문가능금액 + 외화주문가능금액을 합산한 금액
        해외주식의 경우, 주문가능금액 (통화) + 주문가능금액 (원화 등)을 합산한 금액
        """
        ...

    @property
    def foreign_quantity(self) -> ORDER_QUANTITY:
        """
        주문가능수량 (통합)

        국내주식의 경우, 원화주문가능수량 + 외화주문가능수량을 합산한 금액으로 계산한 수량
        해외주식의 경우, 주문가능수량 (통화) + 주문가능수량 (원화 등)을 합산한 금액으로 계산한 수량
        """
        ...

    @property
    def foreign_qty(self) -> ORDER_QUANTITY:
        """주문가능수량 (통합)"""
        ...

    @property
    def exchange_rate(self) -> Decimal:
        """당일환율"""
        ...

    @property
    def condition_kor(self) -> str:
        """주문조건 (한글)"""
        ...


@runtime_checkable
class KisOrderableAmountResponse(KisOrderableAmount, KisResponseProtocol, Protocol):
    """한국투자증권 주문가능금액 응답"""


@kis_repr(
    "account_number",
    "symbol",
    "market",
    "unit_price",
    "qty",
    "amount",
    "condition",
    "execution",
    lines="multiple",
)
class KisOrderableAmountBase(KisAccountProductBase):
    """한국투자증권 주문가능금액"""

    price: Decimal | None
    """주문단가"""
    condition: ORDER_CONDITION | None
    """주문조건"""
    execution: ORDER_EXECUTION | None
    """체결조건"""

    unit_price: Decimal
    """계산단가"""

    amount: Decimal
    """주문가능금액 (통화)"""
    quantity: ORDER_QUANTITY
    """주문가능수량 (통화)"""

    @property
    def qty(self) -> ORDER_QUANTITY:
        """주문가능수량"""
        return self.quantity

    foreign_amount: Decimal
    """
    주문가능금액 (통합)
    
    국내주식의 경우, 원화주문가능금액 + 외화주문가능금액을 합산한 금액
    해외주식의 경우, 주문가능금액 (통화) + 주문가능금액 (원화 등)을 합산한 금액
    """
    foreign_quantity: ORDER_QUANTITY
    """
    주문가능수량 (통합)

    국내주식의 경우, 원화주문가능수량 + 외화주문가능수량을 합산한 금액으로 계산한 수량
    해외주식의 경우, 주문가능수량 (통화) + 주문가능수량 (원화 등)을 합산한 금액으로 계산한 수량
    """

    @property
    def foreign_qty(self) -> ORDER_QUANTITY:
        """주문가능수량 (통합)"""
        return self.foreign_quantity

    exchange_rate: Decimal
    """당일환율"""

    condition_kor: str
    """주문조건 (한글)"""


class KisDomesticOrderableAmount(KisAPIResponse, KisOrderableAmountBase):
    """한국투자증권 국내주식 주문가능금액"""

    unit_price: Decimal = KisDecimal["psbl_qty_calc_unpr"]
    """계산단가"""
    amount: Decimal = KisDecimal["ord_psbl_cash"]
    """주문가능금액 (통화)"""
    quantity: ORDER_QUANTITY = KisDecimal["max_buy_qty"]
    """주문가능수량 (통화)"""

    foreign_only_amount: Decimal = KisDecimal["ord_psbl_frcr_amt_wcrc"]
    """외화주문가능금액 (원화환산)"""

    @cached_property
    def _foreign(self) -> "KisDomesticOrderableAmount":
        """
        한국투자증권 국내 주식 주문가능금액 조회

        국내주식주문 -> 매수가능조회[v1_국내주식-007]

        (캐시됨)

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 주문조건이 잘못된 경우
        """
        return _domestic_orderable_amount(
            self.kis,
            account=self.account_number,
            symbol=self.symbol,
            price=self.price,
            condition=self.condition,  # type: ignore
            execution=self.execution,
            foreign=True,
        )

    @property
    def foreign_amount(self) -> Decimal:
        """
        주문가능금액 (통합)

        원화주문가능금액 + 외화주문가능금액을 합산한 금액
        """
        return self.amount + self.foreign_only_amount

    @property
    def foreign_quantity(self) -> ORDER_QUANTITY:
        """
        주문가능수량 (통합)

        한국투자증권 국내 주식 주문가능금액 조회

        국내주식주문 -> 매수가능조회[v1_국내주식-007]

        (캐시됨)

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 주문조건이 잘못된 경우
        """
        return self._foreign.quantity

    exchange_rate: Decimal = Decimal(1)
    """당일환율"""

    @property
    def condition_kor(self) -> str:
        """주문조건 (한글)"""
        return order_condition(
            price=self.price,
            condition=self.condition,  # type: ignore
            execution=self.execution,
        )[-1]

    def __init__(
        self,
        account_number: KisAccountNumber,
        symbol: str,
        market: MARKET_TYPE,
        price: Decimal | None,
        condition: ORDER_CONDITION | None,
        execution: ORDER_EXECUTION | None,
    ):
        super().__init__()
        self.account_number = account_number
        self.symbol = symbol
        self.market = market
        self.price = price
        self.condition = condition
        self.execution = execution

    def __pre_init__(self, data: dict[str, Any]):
        super().__pre_init__(data)

        if data["output"]["psbl_qty_calc_unpr"] == "0":
            raise_not_found(
                data,
                "해당 종목의 주문가능금액을 조회할 수 없습니다.",
                code=self.symbol,
                market=self.market,
            )


class KisForeignOrderableAmount(KisAPIResponse, KisOrderableAmountBase):
    """한국투자증권 해외주식 주문가능금액"""

    amount: Decimal = KisDecimal["ovrs_ord_psbl_amt"]
    """주문가능금액 (통화)"""
    quantity: ORDER_QUANTITY = KisDecimal["max_ord_psbl_qty"]
    """주문가능수량 (통화)"""

    foreign_amount: Decimal = KisDecimal["frcr_ord_psbl_amt1"]
    """
    주문가능금액 (통합)
    
    주문가능금액 (통화) + 주문가능금액 (원화 등)을 합산한 금액
    """
    foreign_quantity: ORDER_QUANTITY = KisDecimal["ovrs_max_ord_psbl_qty"]
    """
    주문가능수량 (통합)

    주문가능수량 (통화) + 주문가능수량 (원화 등)을 합산한 금액으로 계산한 수량
    """

    exchange_rate: Decimal = KisDecimal["exrt"]
    """당일환율"""

    @property
    def condition_kor(self) -> str:
        """주문조건 (한글)"""
        return order_condition(
            virtual=self.kis.virtual,
            market=self.market,
            order="buy",
            price=self.price,
            condition=self.condition,  # type: ignore
            execution=self.execution,
        )[-1]

    def __init__(
        self,
        account_number: KisAccountNumber,
        symbol: str,
        market: MARKET_TYPE,
        price: Decimal | None,
        unit_price: Decimal,
        condition: ORDER_CONDITION | None,
        execution: ORDER_EXECUTION | None,
    ):
        super().__init__()
        self.account_number = account_number
        self.symbol = symbol
        self.market = market
        self.price = price
        self.condition = condition
        self.execution = execution
        self.unit_price = unit_price

    def __pre_init__(self, data: dict[str, Any]):
        # 에러 메시지의 통일성을 위해 직접 예외를 발생시킴
        if int(data["rt_cd"]) == 7:
            raise_not_found(
                data,
                "해당 종목의 주문가능금액을 조회할 수 없습니다.",
                code=self.symbol,
                market=self.market,
            )

        super().__pre_init__(data)


def _domestic_orderable_amount(
    self: "PyKis",
    account: str | KisAccountNumber,
    symbol: str,
    price: ORDER_PRICE | None = None,
    condition: DOMESTIC_ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
    foreign: bool = False,
) -> KisDomesticOrderableAmount:
    if not account:
        raise ValueError("계좌번호를 입력해주세요.")

    if not symbol:
        raise ValueError("종목코드를 입력해주세요.")

    price = None if price is None else ensure_price(price, 0)

    condition_code, price_setting, _ = order_condition(
        virtual=self.virtual,
        market="KRX",
        order="buy",
        price=price,
        condition=condition,
        execution=execution,
    )

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    if price_setting:
        price = quote(self, symbol=symbol, market="KRX").close

    result = KisDomesticOrderableAmount(
        account_number=account,
        symbol=symbol,
        market="KRX",
        price=price,
        condition=condition,
        execution=execution,
    )

    return self.fetch(
        "/uapi/domestic-stock/v1/trading/inquire-psbl-order",
        api="VTTC8908R" if self.virtual else "TTTC8908R",
        form=[account],
        params={
            "PDNO": symbol,
            "ORD_UNPR": str(price) if price else "0",
            "ORD_DVSN": condition_code,
            "CMA_EVLU_AMT_ICLD_YN": "N",
            "OVRS_ICLD_YN": "Y" if foreign else "N",
        },
        response_type=result,
    )


def domestic_orderable_amount(
    self: "PyKis",
    account: str | KisAccountNumber,
    symbol: str,
    price: ORDER_PRICE | None = None,
    condition: DOMESTIC_ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
) -> KisDomesticOrderableAmount:
    """
    한국투자증권 국내 주식 주문가능금액 조회

    국내주식주문 -> 매수가능조회[v1_국내주식-007]
    (업데이트 날짜: 2023/10/09)

    Args:
        account (str | KisAccountNumber): 계좌번호
        symbol (str): 종목코드
        price (int | None, optional): 주문가격. None인 경우 시장가 주문
        condition (DOMESTIC_ORDER_CONDITION | None, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION | None, optional): 체결조건

    Examples:
        >>> domestic_orderable_amount(account, code, price=100, condition=None, execution=None) # 지정가 매수
        >>> domestic_orderable_amount(account, code, price=None, condition=None, execution=None) # 시장가 매수
        >>> domestic_orderable_amount(account, code, price=100, condition='condition', execution=None) # 조건부지정가 매수
        >>> domestic_orderable_amount(account, code, price=100, condition='best', execution=None) # 최유리지정가 매수
        >>> domestic_orderable_amount(account, code, price=100, condition='priority', execution=None) # 최우선지정가 매수
        >>> domestic_orderable_amount(account, code, price=100, condition='extended', execution=None) # 시간외단일가 매수 (모의투자 미지원)
        >>> domestic_orderable_amount(account, code, price=None, condition='before', execution=None) # 장전시간외 매수 (모의투자 미지원)
        >>> domestic_orderable_amount(account, code, price=None, condition='after', execution=None) # 장후시간외 매수 (모의투자 미지원)
        >>> domestic_orderable_amount(account, code, price=100, condition=None, execution='IOC') # IOC지정가 매수 (모의투자 미지원)
        >>> domestic_orderable_amount(account, code, price=100, condition=None, execution='FOK') # FOK지정가 매수 (모의투자 미지원)
        >>> domestic_orderable_amount(account, code, price=None, condition=None, execution='IOC') # IOC시장가 매수 (모의투자 미지원)
        >>> domestic_orderable_amount(account, code, price=None, condition=None, execution='FOK') # FOK시장가 매수 (모의투자 미지원)
        >>> domestic_orderable_amount(account, code, price=100, condition='best', execution='IOC') # IOC최유리 매수 (모의투자 미지원)
        >>> domestic_orderable_amount(account, code, price=100, condition='best', execution='FOK') # FOK최유리 매수 (모의투자 미지원)

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 주문조건이 잘못된 경우
    """

    return _domestic_orderable_amount(
        self,
        account,
        symbol,
        price=price,
        condition=condition,
        execution=execution,
        foreign=False,
    )


def foreign_orderable_amount(
    self: "PyKis",
    account: str | KisAccountNumber,
    market: MARKET_TYPE,
    symbol: str,
    price: ORDER_PRICE | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
) -> KisForeignOrderableAmount:
    """
    한국투자증권 해외 주식 주문가능금액 조회

    해외주식주문 -> 해외주식 매수가능금액조회[v1_해외주식-014]
    (업데이트 날짜: 2024/03/24)

    Args:
        account (str | KisAccountNumber): 계좌번호
        market (MARKET_TYPE): 시장코드
        symbol (str): 종목코드
        price (int | None, optional): 주문가격. None인 경우 시장가 주문
        condition (ORDER_CONDITION | None, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION | None, optional): 체결조건

    Examples:
        >>> foreign_orderable_amount(account, 전체, code, price=100, condition=None, execution=None) # 전체 지정가 매수
        >>> foreign_orderable_amount(account, 전체, code, price=None, condition=None, execution=None) # 전체 시장가 매수
        >>> foreign_orderable_amount(account, 'NASDAQ', code, price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
        >>> foreign_orderable_amount(account, 'NASDAQ', code, price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
        >>> foreign_orderable_amount(account, 'NASDAQ', code, price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
        >>> foreign_orderable_amount(account, 'NASDAQ', code, price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
        >>> foreign_orderable_amount(account, 'NYSE', code, price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
        >>> foreign_orderable_amount(account, 'NYSE', code, price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
        >>> foreign_orderable_amount(account, 'NYSE', code, price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
        >>> foreign_orderable_amount(account, 'NYSE', code, price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
        >>> foreign_orderable_amount(account, 'AMEX', code, price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
        >>> foreign_orderable_amount(account, 'AMEX', code, price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
        >>> foreign_orderable_amount(account, 'AMEX', code, price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
        >>> foreign_orderable_amount(account, 'AMEX', code, price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
        >>> foreign_orderable_amount(account, 'NASDAQ', code, price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수
        >>> foreign_orderable_amount(account, 'NASDAQ', code, price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수
        >>> foreign_orderable_amount(account, 'NYSE', code, price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수
        >>> foreign_orderable_amount(account, 'NYSE', code, price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수
        >>> foreign_orderable_amount(account, 'AMEX', code, price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수
        >>> foreign_orderable_amount(account, 'AMEX', code, price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 주문조건이 잘못된 경우
    """
    if not account:
        raise ValueError("계좌번호를 입력해주세요.")

    if not symbol:
        raise ValueError("종목코드를 입력해주세요.")

    price = None if price is None else ensure_price(price)

    # 주문조건보장
    if condition != "extended":
        order_condition(
            virtual=self.virtual,
            market=market,
            order="buy",
            price=price,
            condition=condition,
            execution=execution,
        )

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    unit_price = (
        quote(
            self,
            symbol=symbol,
            market=market,
            extended=condition == "extended",
        ).close
        if not price
        else price
    )

    result = KisForeignOrderableAmount(
        account_number=account,
        symbol=symbol,
        market=market,
        price=price,
        unit_price=unit_price,
        condition=condition,
        execution=execution,
    )

    return self.fetch(
        "/uapi/overseas-stock/v1/trading/inquire-psamount",
        api="VTTS3007R" if self.virtual else "TTTS3007R",
        form=[account],
        params={
            "OVRS_EXCG_CD": get_market_code(market),
            "OVRS_ORD_UNPR": str(unit_price),
            "ITEM_CD": symbol,
        },
        response_type=result,
    )


def orderable_amount(
    self: "PyKis",
    account: str | KisAccountNumber,
    market: MARKET_TYPE,
    symbol: str,
    price: ORDER_PRICE | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
) -> KisOrderableAmountResponse:
    """
    한국투자증권 주문가능금액 조회

    국내주식주문 -> 매수가능조회[v1_국내주식-007]
    해외주식주문 -> 해외주식 매수가능금액조회[v1_해외주식-014]

    Args:
        account (str | KisAccountNumber): 계좌번호
        market (MARKET_TYPE): 시장코드
        symbol (str): 종목코드
        price (int | None, optional): 주문가격. None인 경우 시장가 주문
        condition (ORDER_CONDITION | None, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION | None, optional): 체결조건

    Examples:
        >>> orderable_amount(account, 전체, code, price=100, condition=None, execution=None) # 전체 지정가 매수
        >>> orderable_amount(account, 전체, code, price=None, condition=None, execution=None) # 전체 시장가 매수
        >>> orderable_amount(account, "KRX", code, price=100, condition='condition', execution=None) # 국내 조건부지정가 매수
        >>> orderable_amount(account, "KRX", code, price=100, condition='best', execution=None) # 국내 최유리지정가 매수
        >>> orderable_amount(account, "KRX", code, price=100, condition='priority', execution=None) # 국내 최우선지정가 매수
        >>> orderable_amount(account, "KRX", code, price=100, condition='extended', execution=None) # 국내 시간외단일가 매수 (모의투자 미지원)
        >>> orderable_amount(account, "KRX", code, price=None, condition='before', execution=None) # 국내 장전시간외 매수
        >>> orderable_amount(account, "KRX", code, price=None, condition='after', execution=None) # 국내 장후시간외 매수
        >>> orderable_amount(account, "KRX", code, price=100, condition=None, execution='IOC') # 국내 IOC지정가 매수 (모의투자 미지원)
        >>> orderable_amount(account, "KRX", code, price=100, condition=None, execution='FOK') # 국내 FOK지정가 매수 (모의투자 미지원)
        >>> orderable_amount(account, "KRX", code, price=None, condition=None, execution='IOC') # 국내 IOC시장가 매수 (모의투자 미지원)
        >>> orderable_amount(account, "KRX", code, price=None, condition=None, execution='FOK') # 국내 FOK시장가 매수 (모의투자 미지원)
        >>> orderable_amount(account, "KRX", code, price=100, condition='best', execution='IOC') # 국내 IOC최유리 매수 (모의투자 미지원)
        >>> orderable_amount(account, "KRX", code, price=100, condition='best', execution='FOK') # 국내 FOK최유리 매수 (모의투자 미지원)
        >>> orderable_amount(account, 'NASDAQ', code, price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
        >>> orderable_amount(account, 'NASDAQ', code, price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
        >>> orderable_amount(account, 'NASDAQ', code, price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
        >>> orderable_amount(account, 'NASDAQ', code, price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
        >>> orderable_amount(account, 'NYSE', code, price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
        >>> orderable_amount(account, 'NYSE', code, price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
        >>> orderable_amount(account, 'NYSE', code, price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
        >>> orderable_amount(account, 'NYSE', code, price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
        >>> orderable_amount(account, 'AMEX', code, price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
        >>> orderable_amount(account, 'AMEX', code, price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
        >>> orderable_amount(account, 'AMEX', code, price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
        >>> orderable_amount(account, 'AMEX', code, price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
        >>> orderable_amount(account, 'NASDAQ', code, price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수
        >>> orderable_amount(account, 'NASDAQ', code, price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수
        >>> orderable_amount(account, 'NYSE', code, price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수
        >>> orderable_amount(account, 'NYSE', code, price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수
        >>> orderable_amount(account, 'AMEX', code, price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수
        >>> orderable_amount(account, 'AMEX', code, price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 주문조건이 잘못된 경우
    """
    if market == "KRX":
        return domestic_orderable_amount(
            self,
            account,
            symbol,
            price=price,
            condition=condition,  # type: ignore
            execution=execution,
        )
    else:
        return foreign_orderable_amount(
            self,
            account,
            market,
            symbol,
            price=price,
            condition=condition,  # type: ignore
            execution=execution,
        )


def account_orderable_amount(
    self: "KisAccountProtocol",
    market: MARKET_TYPE,
    symbol: str,
    price: ORDER_PRICE | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
) -> KisOrderableAmountResponse:
    """
    한국투자증권 주문가능금액 조회

    국내주식주문 -> 매수가능조회[v1_국내주식-007]
    해외주식주문 -> 해외주식 매수가능금액조회[v1_해외주식-014]

    Args:
        market (MARKET_TYPE): 시장코드
        symbol (str): 종목코드
        price (int | None, optional): 주문가격. None인 경우 시장가 주문
        condition (ORDER_CONDITION | None, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION | None, optional): 체결조건

    Examples:
        >>> orderable_amount(전체, code, price=100, condition=None, execution=None) # 전체 지정가 매수
        >>> orderable_amount(전체, code, price=None, condition=None, execution=None) # 전체 시장가 매수
        >>> orderable_amount("KRX", code, price=100, condition='condition', execution=None) # 국내 조건부지정가 매수
        >>> orderable_amount("KRX", code, price=100, condition='best', execution=None) # 국내 최유리지정가 매수
        >>> orderable_amount("KRX", code, price=100, condition='priority', execution=None) # 국내 최우선지정가 매수
        >>> orderable_amount("KRX", code, price=100, condition='extended', execution=None) # 국내 시간외단일가 매수 (모의투자 미지원)
        >>> orderable_amount("KRX", code, price=None, condition='before', execution=None) # 국내 장전시간외 매수
        >>> orderable_amount("KRX", code, price=None, condition='after', execution=None) # 국내 장후시간외 매수
        >>> orderable_amount("KRX", code, price=100, condition=None, execution='IOC') # 국내 IOC지정가 매수 (모의투자 미지원)
        >>> orderable_amount("KRX", code, price=100, condition=None, execution='FOK') # 국내 FOK지정가 매수 (모의투자 미지원)
        >>> orderable_amount("KRX", code, price=None, condition=None, execution='IOC') # 국내 IOC시장가 매수 (모의투자 미지원)
        >>> orderable_amount("KRX", code, price=None, condition=None, execution='FOK') # 국내 FOK시장가 매수 (모의투자 미지원)
        >>> orderable_amount("KRX", code, price=100, condition='best', execution='IOC') # 국내 IOC최유리 매수 (모의투자 미지원)
        >>> orderable_amount("KRX", code, price=100, condition='best', execution='FOK') # 국내 FOK최유리 매수 (모의투자 미지원)
        >>> orderable_amount('NASDAQ', code, price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
        >>> orderable_amount('NASDAQ', code, price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
        >>> orderable_amount('NASDAQ', code, price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
        >>> orderable_amount('NASDAQ', code, price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
        >>> orderable_amount('NYSE', code, price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
        >>> orderable_amount('NYSE', code, price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
        >>> orderable_amount('NYSE', code, price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
        >>> orderable_amount('NYSE', code, price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
        >>> orderable_amount('AMEX', code, price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
        >>> orderable_amount('AMEX', code, price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
        >>> orderable_amount('AMEX', code, price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
        >>> orderable_amount('AMEX', code, price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
        >>> orderable_amount('NASDAQ', code, price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수
        >>> orderable_amount('NASDAQ', code, price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수
        >>> orderable_amount('NYSE', code, price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수
        >>> orderable_amount('NYSE', code, price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수
        >>> orderable_amount('AMEX', code, price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수
        >>> orderable_amount('AMEX', code, price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 주문조건이 잘못된 경우
    """
    return orderable_amount(
        self.kis,
        account=self.account_number,
        market=market,
        symbol=symbol,
        price=price,
        condition=condition,
        execution=execution,
    )


def account_product_orderable_amount(
    self: "KisAccountProductProtocol",
    price: ORDER_PRICE | None = None,
    condition: ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION | None = None,
) -> KisOrderableAmountResponse:
    """
    한국투자증권 주문가능금액 조회

    국내주식주문 -> 매수가능조회[v1_국내주식-007]
    해외주식주문 -> 해외주식 매수가능금액조회[v1_해외주식-014]

    Args:
        price (int | None, optional): 주문가격. None인 경우 시장가 주문
        condition (ORDER_CONDITION | None, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION | None, optional): 체결조건

    Examples:
        >>> orderable_amount(price=100, condition=None, execution=None) # 전체 지정가 매수
        >>> orderable_amount(price=None, condition=None, execution=None) # 전체 시장가 매수
        >>> orderable_amount(price=100, condition='condition', execution=None) # 국내 조건부지정가 매수
        >>> orderable_amount(price=100, condition='best', execution=None) # 국내 최유리지정가 매수
        >>> orderable_amount(price=100, condition='priority', execution=None) # 국내 최우선지정가 매수
        >>> orderable_amount(price=100, condition='extended', execution=None) # 국내 시간외단일가 매수 (모의투자 미지원)
        >>> orderable_amount(price=None, condition='before', execution=None) # 국내 장전시간외 매수
        >>> orderable_amount(price=None, condition='after', execution=None) # 국내 장후시간외 매수
        >>> orderable_amount(price=100, condition=None, execution='IOC') # 국내 IOC지정가 매수 (모의투자 미지원)
        >>> orderable_amount(price=100, condition=None, execution='FOK') # 국내 FOK지정가 매수 (모의투자 미지원)
        >>> orderable_amount(price=None, condition=None, execution='IOC') # 국내 IOC시장가 매수 (모의투자 미지원)
        >>> orderable_amount(price=None, condition=None, execution='FOK') # 국내 FOK시장가 매수 (모의투자 미지원)
        >>> orderable_amount(price=100, condition='best', execution='IOC') # 국내 IOC최유리 매수 (모의투자 미지원)
        >>> orderable_amount(price=100, condition='best', execution='FOK') # 국내 FOK최유리 매수 (모의투자 미지원)
        >>> orderable_amount(price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
        >>> orderable_amount(price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
        >>> orderable_amount(price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
        >>> orderable_amount(price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
        >>> orderable_amount(price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
        >>> orderable_amount(price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
        >>> orderable_amount(price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
        >>> orderable_amount(price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
        >>> orderable_amount(price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
        >>> orderable_amount(price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
        >>> orderable_amount(price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
        >>> orderable_amount(price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
        >>> orderable_amount(price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수
        >>> orderable_amount(price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수
        >>> orderable_amount(price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수
        >>> orderable_amount(price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수
        >>> orderable_amount(price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수
        >>> orderable_amount(price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 주문조건이 잘못된 경우
    """
    return orderable_amount(
        self.kis,
        account=self.account_number,
        market=self.market,
        symbol=self.symbol,
        price=price,
        condition=condition,
        execution=execution,
    )
