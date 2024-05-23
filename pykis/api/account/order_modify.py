from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Literal

from pykis.__env__ import EMPTY, EMPTY_TYPE, TIMEZONE
from pykis.api.account.order import (
    ORDER_CONDITION,
    ORDER_EXECUTION,
    ORDER_PRICE,
    KisOrder,
    KisOrderNumber,
    ensure_price,
    order_condition,
)
from pykis.api.stock.info import get_market_country
from pykis.api.stock.market import DAYTIME_MARKETS, MARKET_TYPE
from pykis.api.stock.quote import quote
from pykis.client.account import KisAccountNumber
from pykis.client.exception import KisAPIError
from pykis.responses.response import KisAPIResponse
from pykis.responses.types import KisString

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisDomesticModifyOrder(KisAPIResponse, KisOrder):
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


class KisForeignModifyOrder(KisAPIResponse, KisOrder):
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


class KisForeignDaytimeModifyOrder(KisAPIResponse, KisOrder):
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
    account: str | KisAccountNumber,
    order: KisOrderNumber,
    price: ORDER_PRICE | None | EMPTY_TYPE = EMPTY,
    qty: Decimal | None = None,
    condition: ORDER_CONDITION | None | EMPTY_TYPE = EMPTY,
    execution: ORDER_EXECUTION | None | EMPTY_TYPE = EMPTY,
) -> KisDomesticModifyOrder:
    """
    한국투자증권 국내 주식 주문정정 (모의투자 미지원)

    국내주식주문 -> 주식주문(정정취소)[v1_국내주식-003]
    (업데이트 날짜: 2024/04/01)

    Args:
        account (str | KisAccountNumber): 계좌번호
        order (KisOrderNumber): 주문번호
        price (ORDER_PRICE, optional): 주문가격
        qty (Decimal, optional): 주문수량
        condition (ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
    """
    if self.virtual:
        # 모의투자에서 domestic_pending_orders를 지원하지 않으므로, 일관된 구현이 어려워 정정주문도 지원하지 않습니다.
        raise NotImplementedError("모의투자에서는 정정주문을 지원하지 않습니다.")

    if not account:
        raise ValueError("계좌번호를 입력해주세요.")

    if isinstance(qty, Decimal) and qty <= 0:
        raise ValueError("수량은 0보다 커야합니다.")

    from pykis.api.account.pending_order import pending_orders

    order_info = pending_orders(self, account=account, country="KR").order(order)

    if not order_info:
        raise ValueError("주문정보를 찾을 수 없습니다. 이미 체결되었거나 취소된 주문일 수 있습니다.")

    if isinstance(price, EMPTY_TYPE):
        price = order_info.price

    if isinstance(qty, EMPTY_TYPE):
        qty = order_info.qty

    if isinstance(condition, EMPTY_TYPE):
        condition = order_info.condition

    if isinstance(execution, EMPTY_TYPE):
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

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

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
            "ORD_QTY": str(qty or 0),
            "ORD_UNPR": str(price or 0),
            "QTY_ALL_ORD_YN": "N" if qty else "Y",
        },
        form=[account],
        response_type=KisDomesticModifyOrder(
            account_number=account,
            symbol=order.symbol,
            market="KRX",
        ),
        method="POST",
    )


def domestic_cancel_order(
    self: "PyKis",
    account: str | KisAccountNumber,
    order: KisOrderNumber,
) -> KisDomesticModifyOrder:
    """
    한국투자증권 국내 주식 주문취소

    국내주식주문 -> 주식주문(정정취소)[v1_국내주식-003]
    (업데이트 날짜: 2024/04/01)

    Args:
        account (str | KisAccountNumber): 계좌번호
        order (KisOrderNumber): 주문번호
    """
    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

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
        form=[account],
        response_type=KisDomesticModifyOrder(
            account_number=account,
            symbol=order.symbol,
            market="KRX",
        ),
        method="POST",
    )


FOREIGN_ORDER_MODIFY_API_CODES: dict[tuple[bool, MARKET_TYPE, Literal["modify", "cancel"]], str] = {
    # (실전투자여부, 시장, 주문종류): API코드
    (True, "NASD", "modify"): "TTTT1004U",  # 미국 정정 주문
    (True, "NYSE", "modify"): "TTTT1004U",  # 미국 정정 주문
    (True, "AMEX", "modify"): "TTTT1004U",  # 미국 정정 주문
    (True, "NASD", "cancel"): "TTTT1004U",  # 미국 취소 주문
    (True, "NYSE", "cancel"): "TTTT1004U",  # 미국 취소 주문
    (True, "AMEX", "cancel"): "TTTT1004U",  # 미국 취소 주문
    (True, "SEHK", "modify"): "TTTS1003U",  # 홍콩 정정 주문
    (True, "SEHK", "cancel"): "TTTS1003U",  # 홍콩 취소 주문
    (True, "TKSE", "modify"): "TTTS0309U",  # 일본 정정 주문
    (True, "TKSE", "cancel"): "TTTS0309U",  # 일본 취소 주문
    (True, "SHAA", "cancel"): "TTTS0302U",  # 상해 취소 주문
    (True, "SZAA", "cancel"): "TTTS0302U",  # 상해 취소 주문
    (True, "VNSE", "cancel"): "TTTS0312U",  # 베트남 취소 주문
    (True, "HASE", "cancel"): "TTTS0312U",  # 베트남 취소 주문
    (False, "NASD", "modify"): "VTTT1004U",  # 미국 정정 주문
    (False, "NYSE", "modify"): "VTTT1004U",  # 미국 정정 주문
    (False, "AMEX", "modify"): "VTTT1004U",  # 미국 정정 주문
    (False, "NASD", "cancel"): "VTTT1004U",  # 미국 취소 주문
    (False, "NYSE", "cancel"): "VTTT1004U",  # 미국 취소 주문
    (False, "AMEX", "cancel"): "VTTT1004U",  # 미국 취소 주문
    (False, "SEHK", "modify"): "VTTS1003U",  # 홍콩 정정 주문
    (False, "SEHK", "cancel"): "VTTS1003U",  # 홍콩 취소 주문
    (False, "TKSE", "modify"): "VTTS0309U",  # 일본 정정 주문
    (False, "TKSE", "cancel"): "VTTS0309U",  # 일본 취소 주문
    (False, "SHAA", "cancel"): "VTTS0302U",  # 상해 취소 주문
    (False, "SZAA", "cancel"): "VTTS0302U",  # 상해 취소 주문
    (False, "VNSE", "cancel"): "VTTS0312U",  # 베트남 취소 주문
    (False, "HASE", "cancel"): "VTTS0312U",  # 베트남 취소 주문
}


def foreign_modify_order(
    self: "PyKis",
    account: str | KisAccountNumber,
    order: KisOrderNumber,
    price: ORDER_PRICE | None | EMPTY_TYPE = EMPTY,
    qty: Decimal | None = None,
    condition: ORDER_CONDITION | None | EMPTY_TYPE = EMPTY,
    execution: ORDER_EXECUTION | None | EMPTY_TYPE = EMPTY,
) -> KisForeignModifyOrder:
    """
    한국투자증권 해외 주식 주문정정

    국내주식주문 -> 해외주식 정정취소주문[v1_해외주식-003]
    (업데이트 날짜: 2024/04/01)

    Args:
        account (str | KisAccountNumber): 계좌번호
        order (KisOrderNumber): 주문번호
        price (ORDER_PRICE, optional): 주문가격
        qty (Decimal, optional): 주문수량
        condition (ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
    """
    if not account:
        raise ValueError("계좌번호를 입력해주세요.")

    if qty != None and qty <= 0:
        raise ValueError("수량은 0보다 커야합니다.")

    from pykis.api.account.pending_order import pending_orders

    order_info = pending_orders(self, account=account, country=get_market_country(order.market)).order(order)

    if not order_info:
        raise ValueError("주문정보를 찾을 수 없습니다. 이미 체결되었거나 취소된 주문일 수 있습니다.")

    if isinstance(price, EMPTY_TYPE):
        price = order_info.price

    if isinstance(qty, EMPTY_TYPE):
        qty = order_info.qty

    if isinstance(condition, EMPTY_TYPE):
        condition = order_info.condition

    if isinstance(execution, EMPTY_TYPE):
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

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

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
            "OVRS_EXCG_CD": order.market,
            "PDNO": order.symbol,
            "ORGN_ODNO": order.number,
            "RVSE_CNCL_DVSN_CD": "01",
            "ORD_QTY": str(int(qty)),
            "OVRS_ORD_UNPR": str(price or 0),
        },
        form=[account],
        response_type=KisForeignModifyOrder(
            account_number=account,
            symbol=order.symbol,
            market=order.market,
        ),
        method="POST",
    )


def foreign_cancel_order(
    self: "PyKis",
    account: str | KisAccountNumber,
    order: KisOrderNumber,
) -> KisForeignModifyOrder:
    """
    한국투자증권 해외 주식 주문취소

    국내주식주문 -> 해외주식 정정취소주문[v1_해외주식-003]
    (업데이트 날짜: 2024/04/02)

    Args:
        account (str | KisAccountNumber): 계좌번호
        order (KisOrderNumber): 주문번호
    """
    if not account:
        raise ValueError("계좌번호를 입력해주세요.")

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    api = FOREIGN_ORDER_MODIFY_API_CODES.get((not self.virtual, order.market, "cancel"))

    if not api:
        raise ValueError("해당 시장은 취소 주문을 지원하지 않습니다.")

    return self.fetch(
        "/uapi/overseas-stock/v1/trading/order-rvsecncl",
        api=api,
        body={
            "OVRS_EXCG_CD": order.market,
            "PDNO": order.symbol,
            "ORGN_ODNO": order.number,
            "RVSE_CNCL_DVSN_CD": "02",
            "ORD_QTY": "0",
            "OVRS_ORD_UNPR": "0",
        },
        form=[account],
        response_type=KisForeignModifyOrder(
            account_number=account,
            symbol=order.symbol,
            market=order.market,
        ),
        method="POST",
    )


def foreign_daytime_modify_order(
    self: "PyKis",
    account: str | KisAccountNumber,
    order: KisOrderNumber,
    price: ORDER_PRICE | None | EMPTY_TYPE = EMPTY,
    qty: Decimal | None = None,
) -> KisForeignDaytimeModifyOrder:
    """
    한국투자증권 해외 주간거래 주문정정

    국내주식주문 -> 해외주식 미국주간정정취소[v1_해외주식-027] (모의투자 미지원)
    (업데이트 날짜: 2024/04/02)

    Args:
        account (str | KisAccountNumber): 계좌번호
        order (KisOrderNumber): 주문번호
        price (ORDER_PRICE, optional): 주문가격
        qty (Decimal, optional): 주문수량
        condition (ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
    """
    if order.market not in DAYTIME_MARKETS:
        raise ValueError("해당 시장은 주간거래를 지원하지 않습니다.")

    if self.virtual:
        raise NotImplementedError("모의투자에서는 주간거래 정정 주문을 지원하지 않습니다.")

    if not account:
        raise ValueError("계좌번호를 입력해주세요.")

    if qty != None and qty <= 0:
        raise ValueError("수량은 0보다 커야합니다.")

    from pykis.api.account.pending_order import pending_orders

    order_info = pending_orders(self, account=account, country=get_market_country(order.market)).order(order)

    if not order_info:
        raise ValueError("주문정보를 찾을 수 없습니다. 이미 체결되었거나 취소된 주문일 수 있습니다.")

    if isinstance(price, EMPTY_TYPE):
        price = order_info.price

    if isinstance(qty, EMPTY_TYPE):
        qty = order_info.qty

    price = None if price is None else ensure_price(price)

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    if qty is None:
        qty = order_info.qty

    if not price:
        quote_data = quote(self, symbol=order.symbol, market=order.market, extended=True)
        price = quote_data.high_limit if order == "buy" else quote_data.low_limit

    return self.fetch(
        "/uapi/overseas-stock/v1/trading/daytime-order-rvsecncl",
        api="TTTS6038U",
        body={
            "OVRS_EXCG_CD": order.market,
            "PDNO": order.symbol,
            "ORGN_ODNO": order.number,
            "RVSE_CNCL_DVSN_CD": "01",
            "ORD_QTY": str(int(qty)),
            "OVRS_ORD_UNPR": str(price),
            "CTAC_TLNO": "",
            "MGCO_APTM_ODNO": "",
            "ORD_SVR_DVSN_CD": "0",
        },
        form=[account],
        response_type=KisForeignDaytimeModifyOrder(
            account_number=account,
            symbol=order.symbol,
            market=order.market,
        ),
        method="POST",
    )


def foreign_daytime_cancel_order(
    self: "PyKis",
    account: str | KisAccountNumber,
    order: KisOrderNumber,
) -> KisForeignModifyOrder:
    """
    한국투자증권 해외 주식 주문취소

    국내주식주문 -> 해외주식 미국주간정정취소[v1_해외주식-027] (모의투자 미지원)
    (업데이트 날짜: 2024/04/02)

    Args:
        account (str | KisAccountNumber): 계좌번호
        order (KisOrderNumber): 주문번호
    """
    if order.market not in DAYTIME_MARKETS:
        raise ValueError("해당 시장은 주간거래를 지원하지 않습니다.")

    if self.virtual:
        raise NotImplementedError("모의투자에서는 주간거래 정정 주문을 지원하지 않습니다.")

    if not account:
        raise ValueError("계좌번호를 입력해주세요.")

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    from pykis.api.account.pending_order import pending_orders

    order_info = pending_orders(self, account=account, country=get_market_country(order.market)).order(order)

    if not order_info:
        raise ValueError("주문정보를 찾을 수 없습니다. 이미 체결되었거나 취소된 주문일 수 있습니다.")

    return self.fetch(
        "/uapi/overseas-stock/v1/trading/daytime-order-rvsecncl",
        api="TTTS6038U",
        body={
            "OVRS_EXCG_CD": order.market,
            "PDNO": order.symbol,
            "ORGN_ODNO": order.number,
            "RVSE_CNCL_DVSN_CD": "02",
            "ORD_QTY": str(int(order_info.qty)),
            "OVRS_ORD_UNPR": "0",
            "CTAC_TLNO": "",
            "MGCO_APTM_ODNO": "",
            "ORD_SVR_DVSN_CD": "0",
        },
        form=[account],
        response_type=KisForeignModifyOrder(
            account_number=account,
            symbol=order.symbol,
            market=order.market,
        ),
        method="POST",
    )


def modify_order(
    self: "PyKis",
    account: str | KisAccountNumber,
    order: KisOrderNumber,
    price: ORDER_PRICE | None | EMPTY_TYPE = EMPTY,
    qty: Decimal | None = None,
    condition: ORDER_CONDITION | None | EMPTY_TYPE = EMPTY,
    execution: ORDER_EXECUTION | None | EMPTY_TYPE = EMPTY,
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
        qty (Decimal, optional): 주문수량
        condition (ORDER_CONDITION, optional): 주문조건
        execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
    """
    if order.market == "KRX":
        return domestic_modify_order(
            self,
            account=account,
            order=order,
            price=price,
            qty=qty,
            condition=condition,
            execution=execution,
        )

    try:
        return foreign_modify_order(
            self,
            account=account,
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
            account=account,
            order=order,
            price=price,
            qty=qty,
        )


def cancel_order(
    self: "PyKis",
    account: str | KisAccountNumber,
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
    if order.market == "KRX":
        return domestic_cancel_order(self, account=account, order=order)

    try:
        return foreign_cancel_order(self, account=account, order=order)
    except KisAPIError as e:
        if e.error_code != "APBK0918":
            raise e

        return foreign_daytime_cancel_order(self, account=account, order=order)
