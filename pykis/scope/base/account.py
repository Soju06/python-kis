from typing import TYPE_CHECKING

from pykis.api.base.account import KisAccountBase
from pykis.client.account import KisAccountNumber
from pykis.scope.base.scope import KisScope

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisAccountScope(KisScope, KisAccountBase):
    """한국투자증권 계좌 Base Scope"""

    kis: "PyKis"
    """
    한국투자증권 API.
    
    Note:
        기본적으로 __init__ 호출 이후 라이브러리 단위에서 lazy initialization 되며,
        라이브러리 내에서는 해당 속성을 사용할 때 초기화 단계에서 사용하지 않도록 해야합니다.
    """

    account_number: KisAccountNumber
    """Scope에서 사용할 계좌 정보"""

    def __init__(self, kis: "PyKis", account: KisAccountNumber):
        super().__init__(kis=kis)
        self.account_number = account

    from pykis.api.account.balance import account_balance as balance  # 잔고 조회
    from pykis.api.account.daily_order import (
        account_daily_orders as daily_orders,  # 일별 체결내역 조회
    )
    from pykis.api.account.order import account_order as order  # 주문
    from pykis.api.account.order_modify import account_cancel_order as cancel  # 주문 취소
    from pykis.api.account.order_modify import account_modify_order as modify  # 주문 정정
    from pykis.api.account.order_profit import (
        account_order_profits as profits,  # 주문 수익률 조회
    )
    from pykis.api.account.orderable_amount import (
        account_orderable_amount as orderable_amount,  # 주문 가능 금액 조회
    )
    from pykis.api.account.pending_order import (
        account_pending_orders as pending_orders,  # 미체결 조회
    )
