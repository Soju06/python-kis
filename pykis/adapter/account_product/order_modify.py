from types import EllipsisType
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from pykis.api.account.order import (
        IN_ORDER_QUANTITY,
        ORDER_CONDITION,
        ORDER_EXECUTION,
        ORDER_PRICE,
        KisOrder,
        KisOrderNumber,
    )

__all__ = [
    "KisCancelableOrder",
    "KisModifyableOrder",
    "KisOrderableOrder",
    "KisCancelableOrderMixin",
    "KisModifyableOrderMixin",
    "KisOrderableOrderMixin",
]


@runtime_checkable
class KisCancelableOrder(Protocol):
    """취소 가능 주문 프로토콜"""

    def cancel(self) -> "KisOrder":
        """
        한국투자증권 통합 주식 주문취소 (해외 주간거래 모의투자 미지원)

        국내주식주문 -> 주식주문(정정취소)[v1_국내주식-003]
        국내주식주문 -> 해외주식 정정취소주문[v1_해외주식-003]
        """
        ...


class KisModifyableOrder(Protocol):
    """정정 가능 주문 프로토콜"""

    def modify(
        self,
        price: "ORDER_PRICE | None | EllipsisType" = ...,
        qty: "IN_ORDER_QUANTITY | None" = None,
        condition: "ORDER_CONDITION | None | EllipsisType" = ...,
        execution: "ORDER_EXECUTION | None | EllipsisType" = ...,
    ) -> "KisOrder":
        """
        한국투자증권 통합 주식 주문정정 (국내 모의투자 미지원, 해외 주간거래 모의투자 미지원)

        국내주식주문 -> 주식주문(정정취소)[v1_국내주식-003]
        국내주식주문 -> 해외주식 정정취소주문[v1_해외주식-003]

        Args:
            price (ORDER_PRICE, optional): 주문가격
            qty (IN_ORDER_QUANTITY, optional): 주문수량
            condition (ORDER_CONDITION, optional): 주문조건
            execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
        """
        ...


@runtime_checkable
class KisOrderableOrder(KisCancelableOrder, KisModifyableOrder, Protocol):
    """주문 가능 주문 프로토콜"""


class KisCancelableOrderMixin:
    """취소 가능 주문"""

    def cancel(
        self: "KisOrderNumber",
    ) -> "KisOrder":
        """
        한국투자증권 통합 주식 주문취소 (해외 주간거래 모의투자 미지원)

        국내주식주문 -> 주식주문(정정취소)[v1_국내주식-003]
        국내주식주문 -> 해외주식 정정취소주문[v1_해외주식-003]
        """
        from pykis.api.account.order_modify import cancel_order

        return cancel_order(self.kis, order=self)


class KisModifyableOrderMixin:
    """정정 가능 주문"""

    def modify(
        self: "KisOrderNumber",
        price: "ORDER_PRICE | None | EllipsisType" = ...,
        qty: "IN_ORDER_QUANTITY | None" = None,
        condition: "ORDER_CONDITION | None | EllipsisType" = ...,
        execution: "ORDER_EXECUTION | None | EllipsisType" = ...,
    ) -> "KisOrder":
        """
        한국투자증권 통합 주식 주문정정 (국내 모의투자 미지원, 해외 주간거래 모의투자 미지원)

        국내주식주문 -> 주식주문(정정취소)[v1_국내주식-003]
        국내주식주문 -> 해외주식 정정취소주문[v1_해외주식-003]

        Args:
            price (ORDER_PRICE, optional): 주문가격
            qty (IN_ORDER_QUANTITY, optional): 주문수량
            condition (ORDER_CONDITION, optional): 주문조건
            execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
        """
        from pykis.api.account.order_modify import modify_order

        return modify_order(
            self.kis,
            order=self,
            price=price,
            qty=qty,
            condition=condition,
            execution=execution,
        )


class KisOrderableOrderMixin(KisCancelableOrderMixin, KisModifyableOrderMixin):
    """주문 가능 주문"""
