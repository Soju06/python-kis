from typing import TYPE_CHECKING
from pykis.api.stock.info import KisStockInfo
from pykis.api.stock.info import info as _info
from pykis.api.stock.market import MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.scope.stock.stock import KisStock

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisInfoStock(KisStock):
    """한국투자증권 주식 정보 Scope"""

    _info: KisStockInfo
    """주식 정보"""

    def __init__(self, kis: "PyKis", info: KisStockInfo, account: KisAccountNumber | None = None):
        super().__init__(
            kis=kis,
            code=info.code,
            name=info.name,
            market=info.market,
            account=account,
        )
        self._info = info

    @property
    def info(self) -> KisStockInfo:
        """종목정보 조회"""
        return self._info


def stock(
    self: "PyKis",
    code: str,
    market: MARKET_TYPE | None = None,
) -> KisInfoStock:
    """
    종목을 조회하고 종목 Scope를 반환합니다.

    Args:
        code (str): 종목코드
        market (str): 상품유형명
    """

    return KisInfoStock(
        kis=self,
        info=_info(
            self,
            code=code,
            market=market,  # type: ignore
        ),
    )
