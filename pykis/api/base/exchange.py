from typing import TYPE_CHECKING, Protocol, runtime_checkable

from pykis.client.object import KisObjectBase, KisObjectProtocol
from pykis.utils.repr import kis_repr

if TYPE_CHECKING:
    from pykis.api.stock.exchange import CURRENCY_TYPE, EXCHANGE_TYPE


__all__ = [
    "KisExchangeProtocol",
    "KisExchangeBase",
]


@runtime_checkable
class KisExchangeProtocol(KisObjectProtocol, Protocol):
    """한국투자증권 시장 프로토콜"""

    @property
    def exchange(self) -> "EXCHANGE_TYPE":
        """시장유형"""
        ...

    @property
    def exchange_name(self) -> str:
        """실제 상품유형명"""
        ...

    @property
    def foreign(self) -> bool:
        """해외종목 여부"""
        ...

    @property
    def domestic(self) -> bool:
        """국내종목 여부"""
        ...

    @property
    def currency(self) -> "CURRENCY_TYPE":
        """통화"""
        ...


@kis_repr(
    "exchange",
    lines="single",
)
class KisExchangeBase(KisObjectBase):
    """한국투자증권 시장 베이스"""

    exchange: "EXCHANGE_TYPE"
    """시장유형"""

    @property
    def exchange_name(self) -> str:
        """실제 상품유형명"""
        from pykis.api.stock.exchange import get_exchange_name

        return get_exchange_name(self.exchange)

    @property
    def foreign(self) -> bool:
        """해외종목 여부"""
        from pykis.api.stock.info import EXCHANGE_TYPE_MAP

        return self.exchange not in EXCHANGE_TYPE_MAP["KRX"]

    @property
    def domestic(self) -> bool:
        """국내종목 여부"""
        return not self.foreign

    @property
    def currency(self) -> "CURRENCY_TYPE":
        """통화"""
        from pykis.api.stock.exchange import get_exchange_currency

        return get_exchange_currency(self.exchange)
