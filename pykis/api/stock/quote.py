from datetime import date, datetime
from typing import Literal
from pykis.__env__ import TIMEZONE
from pykis.api.stock.base.product import KisProductBase
from pykis.responses.dynamic import KisDynamic, KisObject, KisTransform
from pykis.responses.types import KisAny, KisBool, KisDate, KisFloat, KisString

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


class KisDomesticQuote(KisQuote):
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

    prev_price: float = KisFloat["stck_prdy_clpr"]
    """전일종가"""
    prev_volume_rate: float = KisFloat["prdy_vrss_vol_rate"]
    """전일대비거래량비율 (-100~100)"""

    @property
    def prev_volume(self) -> float:
        """전일거래량"""
        return self.volume / (1 + self.prev_volume_rate / 100)

    change: float = KisFloat["prdy_vrss"]
    """전일대비"""

    indicator: KisDomesticIndicator = KisTransform(
        lambda x: KisObject.transform_(
            x,
            KisDomesticIndicator,
            ignore_missing=True,
        )
    )["output1"]
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
