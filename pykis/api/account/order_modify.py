from datetime import datetime
from types import EllipsisType
from typing import TYPE_CHECKING, Any, Literal

from pykis.api.account.order import (
    IN_ORDER_QUANTITY,
    ORDER_CONDITION,
    ORDER_EXECUTION,
    ORDER_PRICE,
    KisOrder,
    KisOrderBase,
    KisOrderNumber,
    ensure_price,
    order_condition,
)
from pykis.api.stock.info import get_market_country
from pykis.api.stock.market import DAYTIME_MARKETS, MARKET_TYPE, get_market_code
from pykis.api.stock.quote import quote
from pykis.client.exceptions import KisAPIError
from pykis.responses.response import KisAPIResponse
from pykis.responses.types import KisString
from pykis.utils.timezone import TIMEZONE

if TYPE_CHECKING:
    from pykis.api.base.account import KisAccountProtocol
    from pykis.kis import PyKis


__all__ = [
    "modify_order",
    "cancel_order",
]


class KisDomesticModifyOrder(KisAPIResponse, KisOrderBase):
    """한국투자증권 국내주식 정정 주문"""

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
            datetime.strptime(data["output"]["ORD_TMD"], "%H%M%S").time(),
            tzinfo=TIMEZONE,
        )


class KisForeignModifyOrder(KisAPIResponse, KisOrderBase):
    """한국투자증권 해외주식 정정 주문"""

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

        self.time_kst = datetime.combine(
            datetime.now(TIMEZONE).date(),
            datetime.strptime(data["output"]["ORD_TMD"], "%H%M%S").time(),
            tzinfo=TIMEZONE,
        )
        self.time = self.time_kst.astimezone(self.timezone)


class KisForeignDaytimeModifyOrder(KisAPIResponse, KisOrderBase):
    """한국투자증권 해외주식 정정 주문 (주간)"""

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

        self.time_kst = datetime.combine(
            datetime.now(TIMEZONE).date(),
            datetime.strptime(data["output"]["ORD_TMD"], "%H%M%S").time(),
            tzinfo=TIMEZONE,
        )
        self.time = self.time_kst.astimezone(self.timezone)


def domestic_modify_order(
    self: "PyKis",
    order: KisOrderNumber,
    price: ORDER_PRICE | None | EllipsisType = ...,
    qty: IN_ORDER_QUANTITY | None = None,
    condition: ORDER_CONDITION | None | EllipsisType = ...,
    execution: ORDER_EXECUTION | None | EllipsisType = ...,
) -> KisDomesticModifyOrder:
    """
    한국투자증권 국내 주식 주문정정 (모의투자 미지원)

    국내주식주문 -> 주식주문(정정취소)[v1_국내주식-003]
    (업데이트 날짜: 2024/04/01)

    Args:
        order (KisOrderNumber): 주문번호
        price (ORDER_PRICE, optional): 주문가격
        qty (IN_ORDER_QUANTITY, optional): 주문수량
        condition (ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
    """
    if self.virtual:
        # 모의투자에서 domestic_pending_orders를 지원하지 않으므로, 일관된 구현이 어려워 정정주문도 지원하지 않습니다.
        raise NotImplementedError("모의투자에서는 정정주문을 지원하지 않습니다.")

    if isinstance(qty, int) and qty <= 0:
        raise ValueError("수량은 0보다 커야합니다.")

    from pykis.api.account.pending_order import pending_orders

    order_info = pending_orders(
        self,
        account=order.account_number,
        country="KR",
    ).order(order)

    if not order_info:
        raise ValueError("주문정보를 찾을 수 없습니다. 이미 체결되었거나 취소된 주문일 수 있습니다.")

    if isinstance(price, EllipsisType):
        price = order_info.price

    if isinstance(qty, EllipsisType):
        qty = order_info.qty

    if isinstance(condition, EllipsisType):
        condition = order_info.condition

    if isinstance(execution, EllipsisType):
        execution = order_info.execution

    price = None if price is None else ensure_price(price, 0)

    condition_code, price_setting, _ = order_condition(
        virtual=self.virtual,
        market="KRX",
        order=order_info.type,
        price=price,
        condition=condition,
        execution=execution,
    )

    if price_setting:
        quote_data = quote(self, symbol=order.symbol, market="KRX")
        price = quote_data.high_limit if price_setting == "upper" else quote_data.low_limit

    return self.fetch(
        "/uapi/domestic-stock/v1/trading/order-rvsecncl",
        api="VTTC0803U" if self.virtual else "TTTC0803U",
        body={
            "KRX_FWDG_ORD_ORGNO": order.branch,
            "ORGN_ODNO": order.number,
            "ORD_DVSN": condition_code,
            "RVSE_CNCL_DVSN_CD": "01",
            "ORD_QTY": str(int(qty or 0)),
            "ORD_UNPR": str(price or 0),
            "QTY_ALL_ORD_YN": "N" if qty else "Y",
        },
        form=[order.account_number],
        response_type=KisDomesticModifyOrder(
            account_number=order.account_number,
            symbol=order.symbol,
            market="KRX",
        ),
        method="POST",
    )


def domestic_cancel_order(
    self: "PyKis",
    order: KisOrderNumber,
) -> KisDomesticModifyOrder:
    """
    한국투자증권 국내 주식 주문취소

    국내주식주문 -> 주식주문(정정취소)[v1_국내주식-003]
    (업데이트 날짜: 2024/04/01)

    Args:
        order (KisOrderNumber): 주문번호
    """
    return self.fetch(
        "/uapi/domestic-stock/v1/trading/order-rvsecncl",
        api="VTTC0803U" if self.virtual else "TTTC0803U",
        body={
            "KRX_FWDG_ORD_ORGNO": order.branch,
            "ORGN_ODNO": order.number,
            "ORD_DVSN": "00",
            "RVSE_CNCL_DVSN_CD": "02",
            "ORD_QTY": "0",
            "ORD_UNPR": "0",
            "QTY_ALL_ORD_YN": "Y",
        },
        form=[order.account_number],
        response_type=KisDomesticModifyOrder(
            account_number=order.account_number,
            symbol=order.symbol,
            market="KRX",
        ),
        method="POST",
    )


FOREIGN_ORDER_MODIFY_API_CODES: dict[tuple[bool, MARKET_TYPE, Literal["modify", "cancel"]], str] = {
    # (실전투자여부, 시장, 주문종류): API코드
    (True, "NASDAQ", "modify"): "TTTT1004U",  # 미국 정정 주문
    (True, "NYSE", "modify"): "TTTT1004U",  # 미국 정정 주문
    (True, "AMEX", "modify"): "TTTT1004U",  # 미국 정정 주문
    (True, "NASDAQ", "cancel"): "TTTT1004U",  # 미국 취소 주문
    (True, "NYSE", "cancel"): "TTTT1004U",  # 미국 취소 주문
    (True, "AMEX", "cancel"): "TTTT1004U",  # 미국 취소 주문
    (True, "HKEX", "modify"): "TTTS1003U",  # 홍콩 정정 주문
    (True, "HKEX", "cancel"): "TTTS1003U",  # 홍콩 취소 주문
    (True, "TYO", "modify"): "TTTS0309U",  # 일본 정정 주문
    (True, "TYO", "cancel"): "TTTS0309U",  # 일본 취소 주문
    (True, "SSE", "cancel"): "TTTS0302U",  # 상하이 취소 주문
    (True, "SZSE", "cancel"): "TTTS0302U",  # 상하이 취소 주문
    (True, "HSX", "cancel"): "TTTS0312U",  # 베트남 취소 주문
    (True, "HNX", "cancel"): "TTTS0312U",  # 베트남 취소 주문
    (False, "NASDAQ", "modify"): "VTTT1004U",  # 미국 정정 주문
    (False, "NYSE", "modify"): "VTTT1004U",  # 미국 정정 주문
    (False, "AMEX", "modify"): "VTTT1004U",  # 미국 정정 주문
    (False, "NASDAQ", "cancel"): "VTTT1004U",  # 미국 취소 주문
    (False, "NYSE", "cancel"): "VTTT1004U",  # 미국 취소 주문
    (False, "AMEX", "cancel"): "VTTT1004U",  # 미국 취소 주문
    (False, "HKEX", "modify"): "VTTS1003U",  # 홍콩 정정 주문
    (False, "HKEX", "cancel"): "VTTS1003U",  # 홍콩 취소 주문
    (False, "TYO", "modify"): "VTTS0309U",  # 일본 정정 주문
    (False, "TYO", "cancel"): "VTTS0309U",  # 일본 취소 주문
    (False, "SSE", "cancel"): "VTTS0302U",  # 상하이 취소 주문
    (False, "SZSE", "cancel"): "VTTS0302U",  # 상하이 취소 주문
    (False, "HSX", "cancel"): "VTTS0312U",  # 베트남 취소 주문
    (False, "HNX", "cancel"): "VTTS0312U",  # 베트남 취소 주문
}


def foreign_modify_order(
    self: "PyKis",
    order: KisOrderNumber,
    price: ORDER_PRICE | None | EllipsisType = ...,
    qty: IN_ORDER_QUANTITY | None = None,
    condition: ORDER_CONDITION | None | EllipsisType = ...,
    execution: ORDER_EXECUTION | None | EllipsisType = ...,
) -> KisForeignModifyOrder:
    """
    한국투자증권 해외 주식 주문정정

    국내주식주문 -> 해외주식 정정취소주문[v1_해외주식-003]
    (업데이트 날짜: 2024/04/01)

    Args:
        order (KisOrderNumber): 주문번호
        price (ORDER_PRICE, optional): 주문가격
        qty (IN_ORDER_QUANTITY, optional): 주문수량
        condition (ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
    """
    if qty != None and qty <= 0:
        raise ValueError("수량은 0보다 커야합니다.")

    from pykis.api.account.pending_order import pending_orders

    order_info = pending_orders(
        self,
        account=order.account_number,
        country=get_market_country(order.market),
    ).order(order)

    if not order_info:
        raise ValueError("주문정보를 찾을 수 없습니다. 이미 체결되었거나 취소된 주문일 수 있습니다.")

    if isinstance(price, EllipsisType):
        price = order_info.price

    if isinstance(qty, EllipsisType):
        qty = order_info.qty

    if isinstance(condition, EllipsisType):
        condition = order_info.condition

    if isinstance(execution, EllipsisType):
        execution = order_info.execution

    price = None if price is None else ensure_price(price)

    _, price_setting, _ = order_condition(
        virtual=self.virtual,
        market=order.market,
        order=order_info.type,
        price=price,
        condition=condition,
        execution=execution,
    )

    if price_setting:
        quote_data = quote(self, symbol=order.symbol, market=order.market)
        price = quote_data.high_limit if price_setting == "upper" else quote_data.low_limit

    if qty is None:
        qty = order_info.qty

    api = FOREIGN_ORDER_MODIFY_API_CODES.get((not self.virtual, order.market, "modify"))

    if not api:
        raise ValueError("해당 시장은 정정 주문을 지원하지 않습니다.")

    return self.fetch(
        "/uapi/overseas-stock/v1/trading/order-rvsecncl",
        api=api,
        body={
            "OVRS_EXCG_CD": get_market_code(order.market),
            "PDNO": order.symbol,
            "ORGN_ODNO": order.number,
            "RVSE_CNCL_DVSN_CD": "01",
            "ORD_QTY": str(int(qty)),
            "OVRS_ORD_UNPR": str(price or 0),
        },
        form=[order.account_number],
        response_type=KisForeignModifyOrder(
            account_number=order.account_number,
            symbol=order.symbol,
            market=order.market,
        ),
        method="POST",
    )


def foreign_cancel_order(
    self: "PyKis",
    order: KisOrderNumber,
) -> KisForeignModifyOrder:
    """
    한국투자증권 해외 주식 주문취소

    국내주식주문 -> 해외주식 정정취소주문[v1_해외주식-003]
    (업데이트 날짜: 2024/04/02)

    Args:
        order (KisOrderNumber): 주문번호
    """
    api = FOREIGN_ORDER_MODIFY_API_CODES.get((not self.virtual, order.market, "cancel"))

    if not api:
        raise ValueError("해당 시장은 취소 주문을 지원하지 않습니다.")

    return self.fetch(
        "/uapi/overseas-stock/v1/trading/order-rvsecncl",
        api=api,
        body={
            "OVRS_EXCG_CD": get_market_code(order.market),
            "PDNO": order.symbol,
            "ORGN_ODNO": order.number,
            "RVSE_CNCL_DVSN_CD": "02",
            "ORD_QTY": "0",
            "OVRS_ORD_UNPR": "0",
        },
        form=[order.account_number],
        response_type=KisForeignModifyOrder(
            account_number=order.account_number,
            symbol=order.symbol,
            market=order.market,
        ),
        method="POST",
    )


def foreign_daytime_modify_order(
    self: "PyKis",
    order: KisOrderNumber,
    price: ORDER_PRICE | None | EllipsisType = ...,
    qty: IN_ORDER_QUANTITY | None = None,
) -> KisForeignDaytimeModifyOrder:
    """
    한국투자증권 해외 주간거래 주문정정

    국내주식주문 -> 해외주식 미국주간정정취소[v1_해외주식-027] (모의투자 미지원)
    (업데이트 날짜: 2024/04/02)

    Args:
        order (KisOrderNumber): 주문번호
        price (ORDER_PRICE, optional): 주문가격
        qty (IN_ORDER_QUANTITY, optional): 주문수량
        condition (ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
    """
    if order.market not in DAYTIME_MARKETS:
        raise ValueError("해당 시장은 주간거래를 지원하지 않습니다.")

    if self.virtual:
        raise NotImplementedError("모의투자에서는 주간거래 정정 주문을 지원하지 않습니다.")

    if qty != None and qty <= 0:
        raise ValueError("수량은 0보다 커야합니다.")

    from pykis.api.account.pending_order import pending_orders

    order_info = pending_orders(
        self,
        account=order.account_number,
        country=get_market_country(order.market),
    ).order(order)

    if not order_info:
        raise ValueError("주문정보를 찾을 수 없습니다. 이미 체결되었거나 취소된 주문일 수 있습니다.")

    if isinstance(price, EllipsisType):
        price = order_info.price

    if isinstance(qty, EllipsisType):
        qty = order_info.qty

    price = None if price is None else ensure_price(price)

    if qty is None:
        qty = order_info.qty

    if not price:
        quote_data = quote(self, symbol=order.symbol, market=order.market, extended=True)
        price = quote_data.high_limit if order == "buy" else quote_data.low_limit

    return self.fetch(
        "/uapi/overseas-stock/v1/trading/daytime-order-rvsecncl",
        api="TTTS6038U",
        body={
            "OVRS_EXCG_CD": get_market_code(order.market),
            "PDNO": order.symbol,
            "ORGN_ODNO": order.number,
            "RVSE_CNCL_DVSN_CD": "01",
            "ORD_QTY": str(int(qty)),
            "OVRS_ORD_UNPR": str(price),
            "CTAC_TLNO": "",
            "MGCO_APTM_ODNO": "",
            "ORD_SVR_DVSN_CD": "0",
        },
        form=[order.account_number],
        response_type=KisForeignDaytimeModifyOrder(
            account_number=order.account_number,
            symbol=order.symbol,
            market=order.market,
        ),
        method="POST",
    )


def foreign_daytime_cancel_order(
    self: "PyKis",
    order: KisOrderNumber,
) -> KisForeignModifyOrder:
    """
    한국투자증권 해외 주식 주문취소

    국내주식주문 -> 해외주식 미국주간정정취소[v1_해외주식-027] (모의투자 미지원)
    (업데이트 날짜: 2024/04/02)

    Args:
        order (KisOrderNumber): 주문번호
    """
    if order.market not in DAYTIME_MARKETS:
        raise ValueError("해당 시장은 주간거래를 지원하지 않습니다.")

    if self.virtual:
        raise NotImplementedError("모의투자에서는 주간거래 정정 주문을 지원하지 않습니다.")

    from pykis.api.account.pending_order import pending_orders

    order_info = pending_orders(
        self,
        account=order.account_number,
        country=get_market_country(order.market),
    ).order(order)

    if not order_info:
        raise ValueError("주문정보를 찾을 수 없습니다. 이미 체결되었거나 취소된 주문일 수 있습니다.")

    return self.fetch(
        "/uapi/overseas-stock/v1/trading/daytime-order-rvsecncl",
        api="TTTS6038U",
        body={
            "OVRS_EXCG_CD": get_market_code(order.market),
            "PDNO": order.symbol,
            "ORGN_ODNO": order.number,
            "RVSE_CNCL_DVSN_CD": "02",
            "ORD_QTY": str(int(order_info.qty)),
            "OVRS_ORD_UNPR": "0",
            "CTAC_TLNO": "",
            "MGCO_APTM_ODNO": "",
            "ORD_SVR_DVSN_CD": "0",
        },
        form=[order.account_number],
        response_type=KisForeignModifyOrder(
            account_number=order.account_number,
            symbol=order.symbol,
            market=order.market,
        ),
        method="POST",
    )


def modify_order(
    self: "PyKis",
    order: KisOrderNumber,
    price: ORDER_PRICE | None | EllipsisType = ...,
    qty: IN_ORDER_QUANTITY | None = None,
    condition: ORDER_CONDITION | None | EllipsisType = ...,
    execution: ORDER_EXECUTION | None | EllipsisType = ...,
) -> KisOrder:
    """
    한국투자증권 통합 주식 주문정정 (국내 모의투자 미지원, 해외 주간거래 모의투자 미지원)

    국내주식주문 -> 주식주문(정정취소)[v1_국내주식-003]
    국내주식주문 -> 해외주식 정정취소주문[v1_해외주식-003]
    (업데이트 날짜: 2024/04/02)

    Args:
        order (KisOrderNumber): 주문번호
        price (ORDER_PRICE, optional): 주문가격
        qty (IN_ORDER_QUANTITY, optional): 주문수량
        condition (ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
    """
    if order.market == "KRX":
        return domestic_modify_order(
            self,
            order=order,
            price=price,
            qty=qty,
            condition=condition,
            execution=execution,
        )

    try:
        return foreign_modify_order(
            self,
            order=order,
            price=price,
            qty=qty,
            condition=condition,
            execution=execution,
        )
    except KisAPIError as e:
        if e.error_code != "APBK0918":
            raise e

        return foreign_daytime_modify_order(
            self,
            order=order,
            price=price,
            qty=qty,
        )


def account_modify_order(
    self: "KisAccountProtocol",
    order: KisOrderNumber,
    price: ORDER_PRICE | None | EllipsisType = ...,
    qty: IN_ORDER_QUANTITY | None = None,
    condition: ORDER_CONDITION | None | EllipsisType = ...,
    execution: ORDER_EXECUTION | None | EllipsisType = ...,
) -> KisOrder:
    """
    한국투자증권 통합 주식 주문정정 (국내 모의투자 미지원, 해외 주간거래 모의투자 미지원)

    국내주식주문 -> 주식주문(정정취소)[v1_국내주식-003]
    국내주식주문 -> 해외주식 정정취소주문[v1_해외주식-003]
    (업데이트 날짜: 2024/04/02)

    Args:
        account (str | KisAccountNumber): 계좌번호
        order (KisOrderNumber): 주문번호
        price (ORDER_PRICE, optional): 주문가격
        qty (IN_ORDER_QUANTITY, optional): 주문수량
        condition (ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
    """
    return modify_order(
        self.kis,
        order=order,
        price=price,
        qty=qty,
        condition=condition,
        execution=execution,
    )


def cancel_order(
    self: "PyKis",
    order: KisOrderNumber,
) -> KisOrder:
    """
    한국투자증권 통합 주식 주문취소 (해외 주간거래 모의투자 미지원)

    국내주식주문 -> 주식주문(정정취소)[v1_국내주식-003]
    국내주식주문 -> 해외주식 정정취소주문[v1_해외주식-003]
    (업데이트 날짜: 2024/04/02)

    Args:
        order (KisOrderNumber): 주문번호
    """
    if order.market == "KRX":
        return domestic_cancel_order(self, order=order)

    try:
        return foreign_cancel_order(self, order=order)
    except KisAPIError as e:
        if e.error_code != "APBK0918":
            raise e

        return foreign_daytime_cancel_order(self, order=order)


def account_cancel_order(
    self: "KisAccountProtocol",
    order: KisOrderNumber,
) -> KisOrder:
    """
    한국투자증권 통합 주식 주문취소 (해외 주간거래 모의투자 미지원)

    국내주식주문 -> 주식주문(정정취소)[v1_국내주식-003]
    국내주식주문 -> 해외주식 정정취소주문[v1_해외주식-003]
    (업데이트 날짜: 2024/04/02)

    Args:
        account (str | KisAccountNumber): 계좌번호
        order (KisOrderNumber): 주문번호
    """
    return cancel_order(
        self.kis,
        order=order,
    )
