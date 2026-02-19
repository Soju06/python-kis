"""투자자별 매매동향 조회 API"""

from decimal import Decimal
from typing import TYPE_CHECKING, List, Protocol, runtime_checkable

from pykis.responses.dynamic import KisDynamic, KisList
from pykis.responses.response import KisAPIResponse
from pykis.responses.types import KisDecimal, KisInt, KisString
from pykis.utils.repr import kis_repr

if TYPE_CHECKING:
    from pykis.kis import PyKis

__all__ = [
    "KisInvestorItem",
    "KisInvestorResponse",
    "investor",
]


@runtime_checkable
class KisInvestorItem(Protocol):
    """투자자별 매매동향 일별 데이터"""

    @property
    def date(self) -> str:
        """영업일자"""
        ...

    @property
    def close(self) -> Decimal | None:
        """종가"""
        ...

    @property
    def change(self) -> Decimal | None:
        """전일대비"""
        ...

    @property
    def change_rate(self) -> Decimal | None:
        """등락률"""
        ...

    @property
    def foreign_net(self) -> int | None:
        """외국인 순매수"""
        ...

    @property
    def institution_net(self) -> int | None:
        """기관 순매수"""
        ...

    @property
    def individual_net(self) -> int | None:
        """개인 순매수"""
        ...


@kis_repr(
    "date",
    "close",
    "change_rate",
    "foreign_net",
    "institution_net",
    "individual_net",
    lines="multiple",
)
class KisInvestorItemImpl(KisDynamic):
    """투자자별 매매동향 일별 데이터 구현"""

    __ignore_missing__ = True

    date: str = KisString["stck_bsop_date"]
    """영업일자 (YYYYMMDD)"""

    close: Decimal | None = KisDecimal["stck_clpr"]
    """종가"""

    change: Decimal | None = KisDecimal["prdy_vrss"]
    """전일대비"""

    change_rate: Decimal | None = KisDecimal["prdy_ctrt"]
    """등락률"""

    foreign_net: int | None = KisInt["frgn_ntby_qty"]
    """외국인 순매수 수량"""

    institution_net: int | None = KisInt["orgn_ntby_qty"]
    """기관 순매수 수량"""

    individual_net: int | None = KisInt["prsn_ntby_qty"]
    """개인 순매수 수량"""


@runtime_checkable
class KisInvestorResponse(Protocol):
    """투자자별 매매동향 응답"""

    @property
    def symbol(self) -> str:
        """종목코드"""
        ...

    @property
    def items(self) -> List[KisInvestorItem]:
        """일별 매매동향 리스트"""
        ...

    @property
    def foreign_total(self) -> int:
        """외국인 순매수 합계"""
        ...

    @property
    def institution_total(self) -> int:
        """기관 순매수 합계"""
        ...

    @property
    def individual_total(self) -> int:
        """개인 순매수 합계"""
        ...


@kis_repr(
    "symbol",
    "foreign_total",
    "institution_total",
    "individual_total",
    lines="multiple",
)
class KisDomesticInvestor(KisAPIResponse):
    """한국투자증권 국내 주식 투자자별 매매동향"""

    __path__ = None

    symbol: str
    """종목코드"""

    items: List[KisInvestorItemImpl] = KisList(KisInvestorItemImpl)["output"]
    """일별 매매동향 리스트"""

    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol

    @property
    def foreign_total(self) -> int:
        """외국인 순매수 합계"""
        return sum(item.foreign_net or 0 for item in self.items)

    @property
    def institution_total(self) -> int:
        """기관 순매수 합계"""
        return sum(item.institution_net or 0 for item in self.items)

    @property
    def individual_total(self) -> int:
        """개인 순매수 합계"""
        return sum(item.individual_net or 0 for item in self.items)


def investor(
    self: "PyKis",
    symbol: str,
) -> KisDomesticInvestor:
    """
    한국투자증권 국내 주식 투자자별 매매동향 조회

    외국인, 기관, 개인의 일별 순매수 수량을 조회합니다.

    국내주식시세 -> 종목별투자자[v1_국내주식-019]

    Args:
        symbol (str): 종목코드

    Returns:
        KisDomesticInvestor: 투자자별 매매동향 데이터

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 종목 코드가 올바르지 않은 경우

    Examples:
        >>> kis = PyKis(...)
        >>> result = kis.investor("005930")
        >>> print(f"외국인 순매수: {result.foreign_total:,}")
        >>> for item in result.items[:5]:
        ...     print(f"{item.date}: 외국인 {item.foreign_net:+,}")
    """
    if not symbol:
        raise ValueError("종목코드를 입력해주세요.")

    return self.fetch(
        "/uapi/domestic-stock/v1/quotations/inquire-investor",
        api="FHKST01010900",
        params={
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
        },
        response_type=KisDomesticInvestor(symbol),
        domain="real",
    )
