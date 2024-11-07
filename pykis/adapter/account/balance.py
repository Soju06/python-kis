from datetime import date
from typing import Protocol, runtime_checkable

from pykis.api.account.balance import KisBalance
from pykis.api.account.daily_order import KisDailyOrders
from pykis.api.account.order_profit import KisOrderProfits
from pykis.api.base.account import KisAccountProtocol
from pykis.api.stock.info import COUNTRY_TYPE

__all__ = [
    "KisQuotableAccount",
    "KisQuotableAccountMixin",
]


@runtime_checkable
class KisQuotableAccount(Protocol):
    """한국투자증권 잔고조회가능 프로토콜"""

    def balance(
        self: KisAccountProtocol,
        country: COUNTRY_TYPE | None = None,
    ) -> KisBalance:
        """
        한국투자증권 통합주식 잔고 조회

        국내주식주문 -> 주식잔고조회[v1_국내주식-006]
        해외주식주문 -> 해외주식 체결기준현재잔고[v1_해외주식-008] (실전투자, 모의투자)
        해외주식주문 -> 해외주식 잔고[v1_해외주식-006] (모의투자)
        (업데이트 날짜: 2024/03/30)

        Args:
            country (COUNTRY_TYPE, optional): 국가코드

        Raises:
            KisAPIError: API 호출에 실패한 경우
            ValueError: 계좌번호가 잘못된 경우
        """
        ...

    def daily_orders(
        self: KisAccountProtocol,
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
            end (date, optional): 조회 종료일. Defaults to None.
            country (COUNTRY_TYPE, optional): 국가코드

        Raises:
            KisAPIError: API 호출에 실패한 경우
            ValueError: 계좌번호가 잘못된 경우
        """
        ...

    def profits(
        self: KisAccountProtocol,
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
            end (date, optional): 조회 종료일. Defaults to None.
            country (COUNTRY_TYPE, optional): 국가

        Raises:
            KisAPIError: API 호출에 실패한 경우
            ValueError: 계좌번호가 잘못된 경우
        """
        ...


class KisQuotableAccountMixin:
    """한국투자증권 잔고조회가능 프로토콜"""

    from pykis.api.account.balance import account_balance as balance  # 잔고 조회
    from pykis.api.account.daily_order import (
        account_daily_orders as daily_orders,  # 일별 체결내역 조회
    )
    from pykis.api.account.order_profit import (
        account_order_profits as profits,  # 주문 수익률 조회
    )
