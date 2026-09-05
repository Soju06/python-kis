from typing import TYPE_CHECKING, Protocol, runtime_checkable

from vmkis.api.base.account import KisAccountBase, KisAccountProtocol
from vmkis.api.base.product import KisProductBase, KisProductProtocol
from vmkis.client.account import KisAccountNumber
from vmkis.utils.repr import kis_repr

if TYPE_CHECKING:
    from vmkis.api.stock.market import MARKET_TYPE
    from vmkis.kis import VmKis

__all__ = [
    "KisAccountProductProtocol",
    "KisAccountProductBase",
]


@runtime_checkable
class KisAccountProductProtocol(KisAccountProtocol, KisProductProtocol, Protocol):
    """한국투자증권 계좌 상품 프로토콜"""


@kis_repr(
    "account_number",
    "market",
    "symbol",
    lines="single",
)
class KisAccountProductBase(KisAccountBase, KisProductBase):
    """한국투자증권 계좌 상품 기본정보"""

    kis: "VmKis"
    """
    한국투자증권 API.

    Note:
        기본적으로 __init__ 호출 이후 라이브러리 단위에서 lazy initialization 되며,
        라이브러리 내에서는 해당 속성을 사용할 때 초기화 단계에서 사용하지 않도록 해야합니다.
    """

    symbol: str
    """종목코드"""
    market: "MARKET_TYPE"
    """상품유형타입"""

    account_number: KisAccountNumber
    """계좌번호"""
