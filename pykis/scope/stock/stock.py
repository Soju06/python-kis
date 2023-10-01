from typing import TYPE_CHECKING

from pykis.api.stock.info import info as _info
from pykis.api.stock.market import MARKET_TYPE
from pykis.api.stock.quote import quote as _quote
from pykis.client.account import KisAccountNumber
from pykis.scope.account.account import KisAccountScope
from pykis.utils.cache import cached

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisStock(KisAccountScope):
    """한국투자증권 주식 Scope"""

    code: str
    """종목코드"""
    name: str
    """종목명"""

    def __init__(
        self,
        kis: "PyKis",
        code: str,
        name: str,
        market: MARKET_TYPE | None = None,
        account: KisAccountNumber | None = None,
    ):
        super().__init__(
            kis=kis,
            market=market,
            account=account,
        )
        self.code = code
        self.name = name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self.code!r}, name={self.name!r})"

    @property
    @cached
    def info(self):
        """종목정보 조회 (캐시됨)"""
        return _info(
            self.kis,
            code=self.code,
            market=self.market,
        )

    def quote(self):
        """
        한국투자증권 주식 현재가 조회

        국내주식시세 -> 주식현재가 시세[v1_국내주식-008]
        해외주식현재가 -> 해외주식 현재가상세[v1_해외주식-029]

        Raises:
            KisAPIError: API 호출에 실패한 경우
            ValueError: 종목 코드가 올바르지 않은 경우
        """
        return _quote(
            self.kis,
            code=self.code,
            market=self.market or self.info.market,
        )
