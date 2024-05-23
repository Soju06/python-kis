from typing import TYPE_CHECKING

from pykis.client.account import KisAccountNumber
from pykis.scope.base.account import KisAccountScope

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisAccount(KisAccountScope):
    """한국투자증권 계좌 Scope"""


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

    return KisAccount(
        kis=self,
        account=account,
    )
