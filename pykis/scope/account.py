from datetime import date
from typing import TYPE_CHECKING, Protocol

from pykis.adapter.account.order import KisOrderableAccount, KisOrderableAccountImpl
from pykis.adapter.websocket.execution import (
    KisRealtimeOrderableAccount,
    KisRealtimeOrderableAccountImpl,
)
from pykis.api.account.balance import KisBalance
from pykis.api.account.daily_order import KisDailyOrders
from pykis.api.account.order import (
    ORDER_CONDITION,
    ORDER_EXECUTION,
    ORDER_PRICE,
    ORDER_QUANTITY,
    ORDER_TYPE,
    KisOrder,
    KisOrderNumber,
)
from pykis.api.account.order_profit import KisOrderProfits
from pykis.api.account.orderable_amount import KisOrderableAmountResponse
from pykis.api.account.pending_order import KisPendingOrders
from pykis.api.base.account import KisAccountBase, KisAccountProtocol
from pykis.api.stock.info import COUNTRY_TYPE
from pykis.api.stock.market import MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.scope.base import KisScope, KisScopeBase
from pykis.utils.params import EMPTY, EMPTY_TYPE

if TYPE_CHECKING:
    from pykis.kis import PyKis

__all__ = [
    "KisAccount",
    "KisAccountScope",
]


class KisAccount(
    # Base
    KisScope,
    KisAccountProtocol,
    # Adapters
    KisRealtimeOrderableAccount,
    KisOrderableAccount,
    Protocol,
):
    """한국투자증권 계좌 Base Scope"""

    def balance(
        self: "KisAccountProtocol",
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
        raise NotImplementedError

    def daily_orders(
        self: "KisAccountProtocol",
        start: date,
        end: date,
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
        raise NotImplementedError

    def profits(
        self: "KisAccountProtocol",
        start: date,
        end: date,
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
        raise NotImplementedError


class KisAccountScope(
    # Base
    KisScopeBase,
    KisAccountBase,
    # Adapters
    KisRealtimeOrderableAccountImpl,
    KisOrderableAccountImpl,
):
    """한국투자증권 계좌 Base Scope"""

    account_number: KisAccountNumber
    """Scope에서 사용할 계좌 정보"""

    def __init__(self, kis: "PyKis", account: KisAccountNumber):
        super().__init__(kis=kis)
        self.account_number = account

    from pykis.api.account.balance import account_balance as balance  # 잔고 조회
    from pykis.api.account.daily_order import (
        account_daily_orders as daily_orders,  # 일별 체결내역 조회
    )
    from pykis.api.account.order_profit import (
        account_order_profits as profits,  # 주문 수익률 조회
    )
    from pykis.api.account.orderable_amount import (
        account_orderable_amount as orderable_amount,  # 주문 가능 금액 조회
    )


def account(
    self: "PyKis",
    account: str | KisAccountNumber | None = None,
    primary: bool = False,
) -> KisAccount:
    """계좌 정보를 반환합니다.

    Args:
        account: 계좌 번호. None이면 기본 계좌 정보를 사용합니다.
        primary: 기본 계좌로 설정할지 여부
    """
    if isinstance(account, str):
        account = KisAccountNumber(account)

    account = account or self.primary

    if primary:
        self.primary_account = account

    return KisAccountScope(
        kis=self,
        account=account,
    )
