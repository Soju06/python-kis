"""주식 순위 조회 API (시가총액, 거래량, 등락률)"""

from decimal import Decimal
from typing import TYPE_CHECKING, List, Literal, Protocol, runtime_checkable

from pykis.responses.dynamic import KisDynamic, KisList
from pykis.responses.response import KisAPIResponse
from pykis.responses.types import KisDecimal, KisInt, KisString
from pykis.utils.repr import kis_repr

if TYPE_CHECKING:
    from pykis.kis import PyKis

__all__ = [
    "KisRankingItem",
    "KisRankingResponse",
    "ranking_market_cap",
    "ranking_volume",
    "ranking_fluctuation",
]

# 시장 구분 코드
MARKET_CODE = Literal["J", "Q", "K"]  # J: 코스피, Q: 코스닥, K: 코넥스


@runtime_checkable
class KisRankingItem(Protocol):
    """순위 항목"""

    @property
    def rank(self) -> int:
        """순위"""
        ...

    @property
    def symbol(self) -> str:
        """종목코드"""
        ...

    @property
    def name(self) -> str:
        """종목명"""
        ...

    @property
    def price(self) -> Decimal:
        """현재가"""
        ...

    @property
    def change(self) -> Decimal:
        """전일대비"""
        ...

    @property
    def change_sign(self) -> str:
        """전일대비부호 (1:상한, 2:상승, 3:보합, 4:하한, 5:하락)"""
        ...

    @property
    def change_rate(self) -> Decimal:
        """등락률"""
        ...

    @property
    def volume(self) -> int:
        """누적거래량"""
        ...

    @property
    def trading_value(self) -> Decimal:
        """누적거래대금"""
        ...

    @property
    def listed_shares(self) -> int:
        """상장주수"""
        ...


@kis_repr(
    "rank",
    "symbol",
    "name",
    "price",
    "change_rate",
    "volume",
    lines="multiple",
)
class KisRankingItemImpl(KisDynamic):
    """순위 항목 구현"""

    __ignore_missing__ = True

    rank: int = KisInt["data_rank"]
    """순위"""

    symbol: str = KisString["mksc_shrn_iscd"]
    """종목코드"""

    name: str = KisString["hts_kor_isnm"]
    """종목명"""

    price: Decimal | None = KisDecimal["stck_prpr"]
    """현재가"""

    change: Decimal | None = KisDecimal["prdy_vrss"]
    """전일대비"""

    change_sign: str = KisString["prdy_vrss_sign"]
    """전일대비부호 (1:상한, 2:상승, 3:보합, 4:하한, 5:하락)"""

    change_rate: Decimal | None = KisDecimal["prdy_ctrt"]
    """등락률"""

    volume: int | None = KisInt["acml_vol"]
    """누적거래량"""

    prev_volume: int | None = KisInt["prdy_vol"]
    """전일거래량"""

    trading_value: Decimal | None = KisDecimal["acml_tr_pbmn"]
    """누적거래대금"""

    listed_shares: int | None = KisInt["lstn_stcn"]
    """상장주수"""

    volume_rate: Decimal | None = KisDecimal["vol_inrt"]
    """거래량증가율"""

    turnover_rate: Decimal | None = KisDecimal["vol_tnrt"]
    """거래회전율"""


@runtime_checkable
class KisRankingResponse(Protocol):
    """순위 응답"""

    @property
    def market(self) -> str:
        """시장구분"""
        ...

    @property
    def ranking_type(self) -> str:
        """순위유형"""
        ...

    @property
    def items(self) -> List[KisRankingItem]:
        """순위 리스트"""
        ...


@kis_repr(
    "market",
    "ranking_type",
    lines="multiple",
)
class KisRanking(KisAPIResponse):
    """한국투자증권 주식 순위 조회"""

    __path__ = None

    market: str
    """시장구분 (J:코스피, Q:코스닥, K:코넥스)"""

    ranking_type: str
    """순위유형"""

    items: List[KisRankingItemImpl] = KisList(KisRankingItemImpl)["output"]
    """순위 리스트"""

    def __init__(self, market: str, ranking_type: str):
        super().__init__()
        self.market = market
        self.ranking_type = ranking_type


def _fetch_ranking(
    kis: "PyKis",
    market: MARKET_CODE,
    scr_div_code: str,
    ranking_type: str,
    target_cls_code: str = "111111111",
    exclude_cls_code: str = "000000",
) -> KisRanking:
    """순위 조회 공통 함수"""
    return kis.fetch(
        "/uapi/domestic-stock/v1/ranking/market-cap",
        api="FHPST01710000",
        params={
            "FID_COND_MRKT_DIV_CODE": market,
            "FID_COND_SCR_DIV_CODE": scr_div_code,
            "FID_INPUT_ISCD": "0000",
            "FID_DIV_CLS_CODE": "0",
            "FID_BLNG_CLS_CODE": "0",
            "FID_TRGT_CLS_CODE": target_cls_code,
            "FID_TRGT_EXLS_CLS_CODE": exclude_cls_code,
            "FID_INPUT_PRICE_1": "",
            "FID_INPUT_PRICE_2": "",
            "FID_VOL_CNT": "",
            "FID_INPUT_DATE_1": "",
        },
        response_type=KisRanking(market, ranking_type),
        domain="real",
    )


def ranking_market_cap(
    self: "PyKis",
    market: MARKET_CODE = "J",
) -> KisRanking:
    """
    한국투자증권 시가총액 순위 조회

    시가총액 기준 상위 종목을 조회합니다.

    국내주식시세 -> 국내주식 시가총액순위[v1_국내주식-047]

    Args:
        market: 시장구분 (J:코스피, Q:코스닥, K:코넥스)

    Returns:
        KisRanking: 시가총액 순위 데이터

    Raises:
        KisAPIError: API 호출에 실패한 경우

    Examples:
        >>> kis = PyKis(...)
        >>> result = kis.ranking_market_cap()
        >>> for item in result.items[:10]:
        ...     print(f"{item.rank}. {item.name} ({item.symbol})")
    """
    return _fetch_ranking(self, market, "20174", "시가총액")


def ranking_volume(
    self: "PyKis",
    market: MARKET_CODE = "J",
) -> KisRanking:
    """
    한국투자증권 거래량 순위 조회

    거래량 기준 상위 종목을 조회합니다.

    국내주식시세 -> 국내주식 거래량순위[v1_국내주식-047]

    Args:
        market: 시장구분 (J:코스피, Q:코스닥, K:코넥스)

    Returns:
        KisRanking: 거래량 순위 데이터

    Raises:
        KisAPIError: API 호출에 실패한 경우

    Examples:
        >>> kis = PyKis(...)
        >>> result = kis.ranking_volume()
        >>> for item in result.items[:10]:
        ...     print(f"{item.rank}. {item.name}: {item.volume:,}주")
    """
    return _fetch_ranking(self, market, "20171", "거래량")


def ranking_fluctuation(
    self: "PyKis",
    market: MARKET_CODE = "J",
) -> KisRanking:
    """
    한국투자증권 등락률 순위 조회

    등락률(상승률) 기준 상위 종목을 조회합니다.

    국내주식시세 -> 국내주식 등락률순위[v1_국내주식-047]

    Args:
        market: 시장구분 (J:코스피, Q:코스닥, K:코넥스)

    Returns:
        KisRanking: 등락률 순위 데이터

    Raises:
        KisAPIError: API 호출에 실패한 경우

    Examples:
        >>> kis = PyKis(...)
        >>> result = kis.ranking_fluctuation()
        >>> for item in result.items[:10]:
        ...     print(f"{item.rank}. {item.name}: {item.change_rate:+.2f}%")
    """
    return _fetch_ranking(self, market, "20170", "등락률")
