from datetime import date, datetime
from typing import TYPE_CHECKING, Literal
from pykis.__env__ import TIMEZONE
from pykis.api.stock.base.product import KisProductBase
from pykis.api.stock.market import MARKET_TYPE
from pykis.responses.dynamic import KisDynamic, KisObject
from pykis.responses.response import KisAPIResponse
from pykis.responses.types import KisAny, KisBool, KisDate, KisFloat, KisString

if TYPE_CHECKING:
    from pykis.kis import PyKis

STOCK_SIGN_TYPE = Literal["upper", "rise", "steady", "lower", "decline"]
STOCK_SIGN_TYPE_MAP = {
    "1": "upper",
    "2": "rise",
    "3": "steady",
    "4": "lower",
    "5": "decline",
}
STOCK_SIGN_TYPE_KOR_MAP = {
    "upper": "상한",
    "rise": "상승",
    "steady": "보합",
    "lower": "하한",
    "decline": "하락",
}

STOCK_RISK_TYPE = Literal["none", "caution", "warning", "risk"]
STOCK_RISK_TYPE_MAP = {
    "00": "none",
    "01": "caution",
    "02": "warning",
    "03": "risk",
}
STOCK_RISK_TYPE_KOR_MAP = {
    "none": "없음",
    "caution": "주의",
    "warning": "경고",
    "risk": "위험",
}


class KisIndicator(KisDynamic):
    """한국투자증권 종목 지표"""

    eps: float
    """EPS (주당순이익)"""
    bps: float
    """BPS (주당순자산)"""
    per: float
    """PER (주가수익비율)"""
    pbr: float
    """PBR (주가순자산비율)"""

    week52_high: float
    """52주 최고가"""
    week52_low: float
    """52주 최저가"""
    week52_high_date: datetime
    """52주 최고가 날짜"""
    week52_low_date: datetime
    """52주 최저가 날짜"""


class KisQuote(KisDynamic, KisProductBase):
    """한국투자증권 상품 시세"""

    def __init__(self, code: str, market: MARKET_TYPE):
        super().__init__()
        self.code = code
        self.market = market

    name: str
    """종목명"""
    sector_name: str
    """업종명"""
    price: float
    """현재가"""
    volume: float
    """거래량"""
    amount: float
    """거래대금"""
    market_cap: float
    """시가총액"""
    sign: STOCK_SIGN_TYPE
    """대비부호"""
    risk: STOCK_RISK_TYPE
    """위험도"""
    halt: bool
    """거래정지"""
    overbought: bool
    """단기과열구분"""

    prev_price: float
    """전일종가"""
    prev_volume: float
    """전일거래량"""
    change: float
    """전일대비"""

    indicator: KisIndicator
    """종목 지표"""

    @property
    def rate(self) -> float:
        """등락율 (-100~100)"""
        return self.change / self.prev_price * 100


class KisDomesticIndicator(KisIndicator):
    """한국투자증권 국내 종목 지표"""

    eps: float = KisFloat["eps"]
    """EPS (주당순이익)"""
    bps: float = KisFloat["bps"]
    """BPS (주당순자산)"""
    per: float = KisFloat["per"]
    """PER (주가수익비율)"""
    pbr: float = KisFloat["pbr"]
    """PBR (주가순자산비율)"""

    week52_high: float = KisFloat["w52_hgpr"]
    """52주 최고가"""
    week52_low: float = KisFloat["w52_lwpr"]
    """52주 최저가"""
    week52_high_date: date = KisDate(timezone=TIMEZONE)["w52_hgpr_date"]
    """52주 최고가 날짜"""
    week52_low_date: date = KisDate(timezone=TIMEZONE)["w52_lwpr_date"]
    """52주 최저가 날짜"""


class KisDomesticQuote(KisAPIResponse, KisQuote):
    """한국투자증권 국내 상품 시세"""

    code: str = KisString["stck_shrn_iscd"]
    """종목코드"""

    name: str = KisString["bstp_kor_isnm"]
    """종목명"""
    sector_name: str = KisString["bstp_kor_isnm"]
    """업종명"""
    price: float = KisFloat["stck_prpr"]
    """현재가"""
    volume: float = KisFloat["acml_vol"]
    """거래량"""
    amount: float = KisFloat["acml_tr_pbmn"]
    """거래대금"""
    market_cap: float = KisFloat["hts_avls"]
    """시가총액"""
    sign: STOCK_SIGN_TYPE = KisAny(lambda x: STOCK_SIGN_TYPE_MAP[x])["prdy_vrss_sign"]
    """대비부호"""
    risk: STOCK_RISK_TYPE = KisAny(lambda x: STOCK_RISK_TYPE_MAP[x])["mrkt_warn_cls_code"]
    """위험도"""
    halt: bool = KisBool["temp_stop_yn"]
    """거래정지"""
    overbought: bool = KisBool["short_over_yn"]
    """단기과열구분"""

    @property
    def prev_price(self) -> float:
        """전일종가"""
        return self.price - self.change

    prev_volume_rate: float = KisFloat["prdy_vrss_vol_rate"]
    """전일대비거래량비율 (-100~100)"""

    @property
    def prev_volume(self) -> float:
        """전일거래량"""
        return self.volume / (1 + self.prev_volume_rate / 100)

    change: float = KisFloat["prdy_vrss"]
    """전일대비"""

    indicator: KisDomesticIndicator = KisAny(
        lambda x: KisObject.transform_(
            x,
            KisDomesticIndicator,
            ignore_missing=True,
        )
    )["output"]
    """종목 지표"""

    open: float = KisFloat["stck_oprc"]
    """당일시가"""
    high: float = KisFloat["stck_hgpr"]
    """당일고가"""
    low: float = KisFloat["stck_lwpr"]
    """당일저가"""

    @property
    def close(self) -> float:
        """당일종가 (현재가)"""
        return self.price

    high_limit: float = KisFloat["stck_mxpr"]
    """상한가"""
    low_limit: float = KisFloat["stck_llam"]
    """하한가"""
    base_price: float = KisFloat["stck_sdpr"]
    """기준가"""

    def __pre_init__(self, data: dict):
        if data["output"]["stck_prpr"] == "0":
            raise ValueError(f"해당 종목의 현재가를 조회할 수 없습니다. (종목코드: {self.code})")

        super().__pre_init__(data)


def domestic_quote(
    self: "PyKis",
    code: str,
):
    """
    한국투자증권 국내 주식 현재가 조회

    주식, ETF, ETN 조회가 가능합니다.

    국내주식시세 -> 주식현재가 시세[v1_국내주식-008]
    (업데이트 날짜: 2023/09/24)

    Args:
        code (str): 종목코드

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    if not code:
        raise ValueError("종목코드를 입력해주세요.")

    result = KisDomesticQuote(code, "KRX")
    return self.fetch(
        "/uapi/domestic-stock/v1/quotations/inquire-price",
        api="FHKST01010100",
        params={
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": code,
        },
        response_type=result,
        domain="real",
    )
