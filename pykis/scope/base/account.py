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

    from pykis.api.account.pending_order import (
        product_pending_orders as pending_orders,  # 미체결 조회
    )
