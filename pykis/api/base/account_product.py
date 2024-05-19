from typing import TYPE_CHECKING

from pykis.api.base.account import KisAccountBase
from pykis.api.base.product import KisProductBase
from pykis.api.stock.market import MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.utils.repr import kis_repr

if TYPE_CHECKING:
    from pykis.kis import PyKis


@kis_repr(
    "account_number",
    "market",
    "symbol",
    lines="single",
)
class KisAccountProductBase(KisAccountBase, KisProductBase):
    """한국투자증권 계좌 상품 기본정보"""

    kis: "PyKis"
    """
    한국투자증권 API.
    
    Note:
        기본적으로 __init__ 호출 이후 라이브러리 단위에서 lazy initialization 되며,
        라이브러리 내에서는 해당 속성을 사용할 때 초기화 단계에서 사용하지 않도록 해야합니다.
    """

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    account_number: KisAccountNumber
    """계좌번호"""
