from typing import TYPE_CHECKING, Protocol, runtime_checkable

from vmkis.adapter.account.balance import KisQuotableAccount, KisQuotableAccountMixin
from vmkis.adapter.account.order import KisOrderableAccount, KisOrderableAccountMixin
from vmkis.adapter.websocket.execution import (
    KisRealtimeOrderableAccount,
    KisRealtimeOrderableAccountMixin,
)
from vmkis.api.base.account import KisAccountBase, KisAccountProtocol
from vmkis.client.account import KisAccountNumber
from vmkis.scope.base import KisScope, KisScopeBase

if TYPE_CHECKING:
    from vmkis.kis import VmKis

__all__ = [
    "KisAccount",
    "KisAccountScope",
]


@runtime_checkable
class KisAccount(
    # Base
    KisScope,
    KisAccountProtocol,
    # Adapters
    KisRealtimeOrderableAccount,
    KisOrderableAccount,
    KisQuotableAccount,
    Protocol,
):
    """한국투자증권 계좌 Scope"""


class KisAccountScope(
    # Base
    KisScopeBase,
    KisAccountBase,
    # Adapters
    KisRealtimeOrderableAccountMixin,
    KisOrderableAccountMixin,
    KisQuotableAccountMixin,
):
    """한국투자증권 계좌 Scope"""

    account_number: KisAccountNumber
    """Scope에서 사용할 계좌 정보"""

    def __init__(self, kis: "VmKis", account: KisAccountNumber):
        super().__init__(kis=kis)
        self.account_number = account


def account(
    self: "VmKis",
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
