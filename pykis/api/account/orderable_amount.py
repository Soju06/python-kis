from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Literal

from pykis.__env__ import TIMEZONE
from pykis.api.account.order import (
    DOMESTIC_ORDER_CONDITION,
    DOMESTIC_ORDER_CONDITION_CODE_KOR_MAP,
    ORDER_CONDITION,
    ORDER_EXECUTION_CONDITION,
    _domestic_order_condition,
)
from pykis.api.stock.base.account_product import KisAccountProductBase
from pykis.api.stock.market import CURRENCY_TYPE, MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.responses.dynamic import KisDynamic
from pykis.responses.response import KisAPIResponse, raise_not_found
from pykis.responses.types import KisDecimal, KisInt, KisString
from pykis.utils.cache import cached

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisOrderableAmount(KisDynamic, KisAccountProductBase):
    """한국투자증권 주문가능금액"""

    price: int | None
    """주문가격"""
    condition: ORDER_CONDITION | None
    """주문조건"""
    execution: ORDER_EXECUTION_CONDITION | None
    """채결조건"""

    amount: Decimal
    """주문가능금액 (통화)"""
    quantity: int
    """주문가능수량 (통화)"""

    @property
    def qty(self) -> int:
        """주문가능수량"""
        return self.quantity

    foreign_amount: Decimal
    """
    주문가능금액 (통합)
    
    국내주식의 경우, 원화주문가능금액 + 외화주문가능금액을 합산한 금액
    해외주식의 경우, 주문가능금액 (통화) + 주문가능금액 (원화 등)을 합산한 금액
    """
    foreign_quantity: int
    """
    주문가능수량 (통합)

    국내주식의 경우, 원화주문가능수량 + 외화주문가능수량을 합산한 금액으로 계산한 수량
    해외주식의 경우, 주문가능수량 (통화) + 주문가능수량 (원화 등)을 합산한 금액으로 계산한 수량
    """

    @property
    def foreign_qty(self) -> int:
        """주문가능수량 (통합)"""
        return self.foreign_quantity

    currency: CURRENCY_TYPE
    """통화코드"""
    exchange_rate: Decimal
    """당일환율"""

    condition_kor: str
    """주문조건 (한글)"""

    def __init__(
        self,
        account_number: KisAccountNumber,
        code: str,
        market: MARKET_TYPE,
        price: int | None,
        condition: ORDER_CONDITION | None,
        execution: ORDER_EXECUTION_CONDITION | None,
    ):
        super().__init__()
        self.account_number = account_number
        self.code = code
        self.market = market
        self.price = price
        self.condition = condition
        self.execution = execution


class KisDomesticOrderableAmount(KisAPIResponse, KisOrderableAmount):
    """한국투자증권 국내주식 주문가능금액"""

    amount: Decimal = KisDecimal["ord_psbl_cash"]
    """주문가능금액 (통화)"""
    quantity: int = KisInt["nrcvb_buy_qty"]
    """주문가능수량 (통화)"""

    foreign_only_amount: Decimal = KisDecimal["ord_psbl_frcr_amt_wcrc"]
    """외화주문가능금액 (원화환산)"""

    @property
    @cached
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
            code=self.code,
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
    def foreign_quantity(self) -> int:
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

    currency: CURRENCY_TYPE = "KRW"
    """통화코드"""
    exchange_rate: Decimal = Decimal(1)
    """당일환율"""

    @property
    def condition_kor(self) -> str:
        """주문조건 (한글)"""
        return DOMESTIC_ORDER_CONDITION_CODE_KOR_MAP[
            _domestic_order_condition(
                price=self.price,
                condition=self.condition,  # type: ignore
                execution=self.execution,
            )
        ]

    def __pre_init__(self, data: dict[str, Any]):
        super().__pre_init__(data)

        if data["output"]["psbl_qty_calc_unpr"] == "0":
            raise_not_found(
                data,
                "해당 종목의 주문가능금액을 조회할 수 없습니다.",
                code=self.code,
                market=self.market,
            )


def _domestic_orderable_amount(
    self: "PyKis",
    account: str | KisAccountNumber,
    code: str,
    price: int | None = None,
    condition: DOMESTIC_ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION_CONDITION | None = None,
    foreign: bool = False,
) -> KisDomesticOrderableAmount:
    if not account:
        raise ValueError("계좌번호를 입력해주세요.")

    if not code:
        raise ValueError("종목코드를 입력해주세요.")

    condition_code = _domestic_order_condition(
        price=price,
        condition=condition,
        execution=execution,
    )

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    result = KisDomesticOrderableAmount(
        account_number=account,
        code=code,
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
            "PDNO": code,
            "ORD_UNPR": str(price) if price else "",
            "ORD_DVSN": condition_code,
            "CMA_EVLU_AMT_ICLD_YN": "N",
            "OVRS_ICLD_YN": "Y" if foreign else "N",
        },
        response_type=result,
    )


def domestic_orderable_amount(
    self: "PyKis",
    account: str | KisAccountNumber,
    code: str,
    price: int | None = None,
    condition: DOMESTIC_ORDER_CONDITION | None = None,
    execution: ORDER_EXECUTION_CONDITION | None = None,
) -> KisDomesticOrderableAmount:
    """
    한국투자증권 국내 주식 주문가능금액 조회

    국내주식주문 -> 매수가능조회[v1_국내주식-007]
    (업데이트 날짜: 2023/10/09)

    Args:
        account (str | KisAccountNumber): 계좌번호
        code (str): 종목코드
        price (int | None, optional): 주문가격. None인 경우 시장가 주문
        condition (DOMESTIC_ORDER_CONDITION | None, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION | None, optional): 채결조건

    Examples:
        >>> domestic_orderable_amount(account, code, price=100, condition=None, execution=None) # 지정가
        >>> domestic_orderable_amount(account, code, price=None, condition=None, execution=None) # 시장가
        >>> domestic_orderable_amount(account, code, price=100, condition='condition', execution=None) # 조건부지정가
        >>> domestic_orderable_amount(account, code, price=100, condition='best', execution=None) # 최유리지정가
        >>> domestic_orderable_amount(account, code, price=100, condition='priority', execution=None) # 최우선지정가
        >>> domestic_orderable_amount(account, code, price=100, condition='extended', execution=None) # 시간외단일가
        >>> domestic_orderable_amount(account, code, price=None, condition='before', execution=None) # 장전시간외
        >>> domestic_orderable_amount(account, code, price=None, condition='after', execution=None) # 장후시간외
        >>> domestic_orderable_amount(account, code, price=100, condition=None, execution='IOC') # IOC지정가
        >>> domestic_orderable_amount(account, code, price=100, condition=None, execution='FOK') # FOK지정가
        >>> domestic_orderable_amount(account, code, price=None, condition=None, execution='IOC') # IOC시장가
        >>> domestic_orderable_amount(account, code, price=None, condition=None, execution='FOK') # FOK시장가
        >>> domestic_orderable_amount(account, code, price=100, condition='best', execution='IOC') # IOC최유리
        >>> domestic_orderable_amount(account, code, price=100, condition='best', execution='FOK') # FOK최유리

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 주문조건이 잘못된 경우
    """

    return _domestic_orderable_amount(
        self,
        account,
        code,
        price=price,
        condition=condition,
        execution=execution,
        foreign=False,
    )
