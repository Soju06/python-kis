from typing import TYPE_CHECKING, Protocol, runtime_checkable

from pykis.client.account import KisAccountNumber
from pykis.client.object import KisObjectBase, KisObjectProtocol
from pykis.utils.repr import kis_repr

if TYPE_CHECKING:
    from pykis.kis import PyKis
    from pykis.scope.account import KisAccount

__all__ = [
    "KisAccountProtocol",
    "KisAccountBase",
]


@runtime_checkable
class KisAccountProtocol(KisObjectProtocol, Protocol):
    """한국투자증권 계좌 프로토콜"""

    @property
    def account_number(self) -> KisAccountNumber:
        """계좌번호"""
        ...

    @property
    def account(self) -> "KisAccount":
        """계좌 Scope"""
        ...


@kis_repr(
    "account_number",
    lines="single",
)
class KisAccountBase(KisObjectBase):
    """한국투자증권 계좌 기본정보"""

    kis: "PyKis"
    """
    한국투자증권 API.
    
    Note:
        기본적으로 __init__ 호출 이후 라이브러리 단위에서 lazy initialization 되며,
        라이브러리 내에서는 해당 속성을 사용할 때 초기화 단계에서 사용하지 않도록 해야합니다.
    """

    account_number: KisAccountNumber
    """계좌번호"""

    @property
    def account(self) -> "KisAccount":
        """
        계좌 Scope

        해당 `KisAccountBase`의 계좌 Scope는 전체 시장에 대한 정보를 제공합니다.
        Product에 따라 시장 정보를 제공받으려면 `KisAccountProductBase`를 사용하세요.
        """
        return self.kis.account(account=self.account_number)
