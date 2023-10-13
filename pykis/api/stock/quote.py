from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Literal

from pykis.__env__ import TIMEZONE
from pykis.api.stock.base.product import KisProductBase
from pykis.api.stock.market import CURRENCY_TYPE, MARKET_TYPE, MARKET_TYPE_SHORT_MAP
from pykis.responses.dynamic import KisDynamic, KisObject, KisTransform
from pykis.responses.response import KisAPIResponse, raise_not_found
from pykis.responses.types import KisAny, KisBool, KisDate, KisDecimal, KisDynamicDict, KisInt, KisString

if TYPE_CHECKING:
    from pykis.kis import PyKis

STOCK_SIGN_TYPE = Literal["upper", "rise", "steady", "decline", "lower"]
STOCK_SIGN_TYPE_MAP = {
    "0": "steady",
    "1": "upper",
    "2": "rise",
    "3": "steady",
    "4": "lower",
    "5": "decline",
}
STOCK_SIGN_TYPE_KOR_MAP: dict[STOCK_SIGN_TYPE, str] = {
    "upper": "상한",
    "rise": "상승",
    "steady": "보합",
    "decline": "하락",
    "lower": "하한",
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

    eps: Decimal
    """EPS (주당순이익)"""
    bps: Decimal
    """BPS (주당순자산)"""
    per: Decimal
    """PER (주가수익비율)"""
    pbr: Decimal
    """PBR (주가순자산비율)"""

    week52_high: Decimal
    """52주 최고가"""
    week52_low: Decimal
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
    price: Decimal
    """현재가"""
    volume: int
    """거래량"""
    amount: Decimal
    """거래대금"""
    market_cap: Decimal
    """시가총액"""
    sign: STOCK_SIGN_TYPE
    """대비부호"""
    risk: STOCK_RISK_TYPE
    """위험도"""
    halt: bool
    """거래정지"""
    overbought: bool
    """단기과열구분"""

    prev_price: Decimal
    """전일종가"""
    prev_volume: Decimal
    """전일거래량"""
    change: Decimal
    """전일대비"""

    indicator: KisIndicator
    """종목 지표"""

    open: Decimal
    """당일시가"""
    high: Decimal
    """당일고가"""
    low: Decimal
    """당일저가"""

    @property
    def close(self) -> Decimal:
        """당일종가 (현재가)"""
        return self.price

    high_limit: Decimal
    """상한가"""
    low_limit: Decimal
    """하한가"""
    unit: Decimal
    """거래단위"""
    tick: Decimal
    """호가단위"""
    decimal_places: int
    """소수점 자리수"""

    currency: CURRENCY_TYPE
    """통화코드"""
    exchange_rate: Decimal
    """당일환율"""

    @property
    def rate(self) -> Decimal:
        """등락율 (-100~100)"""
        return self.change / self.prev_price * 100

    @property
    def sign_name(self) -> str:
        """대비부호명"""
        return STOCK_SIGN_TYPE_KOR_MAP[self.sign]


class KisDomesticIndicator(KisIndicator):
    """한국투자증권 국내 종목 지표"""

    eps: Decimal = KisDecimal["eps"]
    """EPS (주당순이익)"""
    bps: Decimal = KisDecimal["bps"]
    """BPS (주당순자산)"""
    per: Decimal = KisDecimal["per"]
    """PER (주가수익비율)"""
    pbr: Decimal = KisDecimal["pbr"]
    """PBR (주가순자산비율)"""

    week52_high: Decimal = KisDecimal["w52_hgpr"]
    """52주 최고가"""
    week52_low: Decimal = KisDecimal["w52_lwpr"]
    """52주 최저가"""
    week52_high_date: date = KisDate(timezone=TIMEZONE)["w52_hgpr_date"]
    """52주 최고가 날짜"""
    week52_low_date: date = KisDate(timezone=TIMEZONE)["w52_lwpr_date"]
    """52주 최저가 날짜"""


class KisDomesticQuote(KisAPIResponse, KisQuote):
    """한국투자증권 국내 상품 시세"""

    code: str = KisString["stck_shrn_iscd"]
    """종목코드"""

    @property
    def name(self) -> str:
        """종목명"""
        return self.info.name

    sector_name: str = KisString["bstp_kor_isnm"]
    """업종명"""
    price: Decimal = KisDecimal["stck_prpr"]
    """현재가"""
    volume: int = KisInt["acml_vol"]
    """거래량"""
    amount: Decimal = KisDecimal["acml_tr_pbmn"]
    """거래대금"""
    market_cap: Decimal = KisDecimal["hts_avls"]
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
    def prev_price(self) -> Decimal:
        """전일종가"""
        return self.price - self.change

    prev_volume_rate: Decimal = KisDecimal["prdy_vrss_vol_rate"]
    """전일대비거래량비율 (-100~100)"""

    @property
    def prev_volume(self) -> Decimal:
        """전일거래량"""
        return self.volume / (1 + self.prev_volume_rate / 100)

    change: Decimal = KisDecimal["prdy_vrss"]
    """전일대비"""

    indicator: KisDomesticIndicator = KisTransform(
        lambda x: KisObject.transform_(
            x,
            KisDomesticIndicator,
            ignore_missing=True,
        )
    )()
    """종목 지표"""

    open: Decimal = KisDecimal["stck_oprc"]
    """당일시가"""
    high: Decimal = KisDecimal["stck_hgpr"]
    """당일고가"""
    low: Decimal = KisDecimal["stck_lwpr"]
    """당일저가"""

    high_limit: Decimal = KisDecimal["stck_mxpr"]
    """상한가"""
    low_limit: Decimal = KisDecimal["stck_llam"]
    """하한가"""
    base_price: Decimal = KisDecimal["stck_sdpr"]
    """기준가"""
    unit: Decimal = Decimal(1)
    """거래단위"""
    tick: Decimal = KisDecimal["aspr_unit"]
    """호가단위"""
    decimal_places: int = 0
    """소수점 자리수"""

    currency: CURRENCY_TYPE = "KRW"
    """통화코드"""
    exchange_rate: Decimal = Decimal(1)
    """당일환율"""

    def __pre_init__(self, data: dict):
        if data["output"]["stck_prpr"] == "0":
            raise_not_found(
                data,
                "해당 종목의 현재가를 조회할 수 없습니다.",
                code=self.code,
                market=self.market,
            )

        super().__pre_init__(data)


class KisOverseasIndicator(KisIndicator):
    """한국투자증권 해외 종목 지표"""

    eps: Decimal = KisDecimal["epsx"]
    """EPS (주당순이익)"""
    bps: Decimal = KisDecimal["bpsx"]
    """BPS (주당순자산)"""
    per: Decimal = KisDecimal["perx"]
    """PER (주가수익비율)"""
    pbr: Decimal = KisDecimal["pbrx"]
    """PBR (주가순자산비율)"""

    week52_high: Decimal = KisDecimal["h52p"]
    """52주 최고가"""
    week52_low: Decimal = KisDecimal["l52p"]
    """52주 최저가"""
    week52_high_date: date = KisDate(timezone=TIMEZONE)["h52d"]
    """52주 최고가 날짜"""
    week52_low_date: date = KisDate(timezone=TIMEZONE)["l52d"]
    """52주 최저가 날짜"""


class KisOverseasQuote(KisAPIResponse, KisQuote):
    """한국투자증권 해외 상품 시세"""

    @property
    def name(self) -> str:
        """종목명"""
        return self.info.name

    sector_name: str = KisString["e_icod"]
    """업종명"""
    price: Decimal = KisDecimal["last"]
    """현재가"""
    volume: int = KisInt["tvol"]
    """거래량"""
    amount: Decimal = KisDecimal["tamt"]
    """거래대금"""
    market_cap: Decimal = KisDecimal["tomv"]
    """시가총액"""

    sign: STOCK_SIGN_TYPE = KisAny(lambda x: STOCK_SIGN_TYPE_MAP[x])["t_xsgn"]
    """대비부호"""
    risk: STOCK_RISK_TYPE = "none"
    """위험도"""
    halt: bool = KisAny(lambda x: x != "매매 가능")["e_ordyn"]
    """거래정지"""
    overbought: bool = False
    """단기과열구분"""

    prev_price: Decimal = KisDecimal["base"]
    """전일종가"""

    @property
    def prev_volume_rate(self) -> Decimal:
        """전일대비거래량비율 (-100~100)"""
        return self.volume / self.prev_volume * 100 - 100

    prev_volume: Decimal = KisDecimal["pvol"]
    """전일거래량"""

    @property
    def change(self) -> Decimal:
        """전일대비"""
        return self.price - self.prev_price

    indicator: KisOverseasIndicator = KisTransform(
        lambda x: KisObject.transform_(
            x,
            KisOverseasIndicator,
            ignore_missing=True,
        )
    )()
    """종목 지표"""

    open: Decimal = KisDecimal["open"]
    """당일시가"""
    high: Decimal = KisDecimal["high"]
    """당일고가"""
    low: Decimal = KisDecimal["low"]
    """당일저가"""

    high_limit: Decimal = KisDecimal["uplp"]
    """상한가"""
    low_limit: Decimal = KisDecimal["dnlp"]
    """하한가"""
    unit: Decimal = KisDecimal["vnit"]
    """거래단위"""
    tick: Decimal = KisDecimal["e_hogau"]
    """호가단위"""
    decimal_places: int = KisInt["zdiv"]
    """소수점 자리수"""

    currency: CURRENCY_TYPE = KisString["curr"]
    """통화코드"""
    exchange_rate: Decimal = KisDecimal["t_rate"]
    """당일환율"""

    def __pre_init__(self, data: dict):
        if not data["output"]["last"]:
            raise_not_found(
                data,
                "해당 종목의 현재가를 조회할 수 없습니다.",
                code=self.code,
                market=self.market,
            )

        super().__pre_init__(data)


def domestic_quote(
    self: "PyKis",
    code: str,
) -> KisDomesticQuote:
    """
    한국투자증권 국내 주식 현재가 조회

    주식, ETF, ETN 조회가 가능합니다.

    국내주식시세 -> 주식현재가 시세[v1_국내주식-008]
    (업데이트 날짜: 2023/09/24)

    Args:
        code (str): 종목코드

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
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


def overseas_quote(
    self: "PyKis",
    code: str,
    market: MARKET_TYPE,
) -> KisOverseasQuote:
    """
    한국투자증권 해외 주식 현재가 조회

    해외주식현재가 -> 해외주식 현재가상세[v1_해외주식-029]
    (업데이트 날짜: 2023/10/01)

    Args:
        code (str): 종목코드
        market (MARKET_TYPE): 시장구분

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    if not code:
        raise ValueError("종목코드를 입력해주세요.")

    result = KisOverseasQuote(code, market)

    return self.fetch(
        "/uapi/overseas-price/v1/quotations/price-detail",
        api="HHDFS76200200",
        params={
            "AUTH": "",
            "EXCD": MARKET_TYPE_SHORT_MAP[market],
            "SYMB": code,
        },
        response_type=result,
        domain="real",
    )


def _overseas_quote(
    self: "PyKis",
    code: str,
    market: MARKET_TYPE,
) -> KisDynamicDict:
    """
    한국투자증권 해외 주식 현재가 조회

    해외주식현재가 -> 해외주식 현재가[v1_해외주식-009]
    (업데이트 날짜: 2023/10/11)

    Args:
        code (str): 종목코드
        market (MARKET_TYPE): 시장구분

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    result = self.fetch(
        "/uapi/overseas-price/v1/quotations/price",
        api="HHDFS00000300",
        params={
            "AUTH": "",
            "EXCD": MARKET_TYPE_SHORT_MAP[market],
            "SYMB": code,
        },
        response_type=KisDynamicDict,
        domain="real",
    )

    if not result.output.last:
        raise_not_found(
            result.__data__,
            "해당 종목의 현재가를 조회할 수 없습니다.",
            code=code,
            market=market,
        )

    return result


def quote(
    self: "PyKis",
    code: str,
    market: MARKET_TYPE,
) -> KisQuote:
    """
    한국투자증권 주식 현재가 조회

    국내주식시세 -> 주식현재가 시세[v1_국내주식-008]
    해외주식현재가 -> 해외주식 현재가상세[v1_해외주식-029]

    Args:
        code (str): 종목코드
        market (MARKET_TYPE): 시장구분

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    if market == "KRX":
        return domestic_quote(self, code)
    else:
        return overseas_quote(self, code, market)
