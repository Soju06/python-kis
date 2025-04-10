from datetime import date
from decimal import Decimal
from functools import cached_property
from typing import TYPE_CHECKING, Literal, Protocol, runtime_checkable

from pykis.api.base.product import KisProductBase, KisProductProtocol
from pykis.api.stock.market import (
    DAYTIME_MARKET_SHORT_TYPE_MAP,
    MARKET_SHORT_TYPE_MAP,
    MARKET_TYPE,
)
from pykis.responses.dynamic import KisDynamic, KisObject, KisTransform
from pykis.responses.response import (
    KisAPIResponse,
    KisResponseProtocol,
    raise_not_found,
)
from pykis.responses.types import (
    KisAny,
    KisBool,
    KisDate,
    KisDecimal,
    KisInt,
    KisString,
)
from pykis.utils.math import safe_divide
from pykis.utils.repr import kis_repr
from pykis.utils.timezone import TIMEZONE

if TYPE_CHECKING:
    from pykis.kis import PyKis

__all__ = [
    "STOCK_SIGN_TYPE",
    "STOCK_RISK_TYPE",
    "KisIndicator",
    "KisQuote",
    "KisQuoteResponse",
    "quote",
]

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


@runtime_checkable
class KisQuote(KisProductProtocol, Protocol):
    """한국투자증권 상품 시세"""

    @property
    def sector_name(self) -> str | None:
        """업종명"""
        ...

    @property
    def price(self) -> Decimal:
        """현재가"""
        ...

    @property
    def volume(self) -> int:
        """거래량"""
        ...

    @property
    def amount(self) -> Decimal:
        """거래대금"""
        ...

    @property
    def market_cap(self) -> Decimal:
        """시가총액"""
        ...

    @property
    def sign(self) -> STOCK_SIGN_TYPE:
        """대비부호"""
        ...

    @property
    def risk(self) -> STOCK_RISK_TYPE:
        """위험도"""
        ...

    @property
    def halt(self) -> bool:
        """거래정지"""
        ...

    @property
    def overbought(self) -> bool:
        """단기과열구분"""
        ...

    @property
    def prev_price(self) -> Decimal:
        """전일종가"""
        ...

    @property
    def prev_volume(self) -> Decimal:
        """전일거래량"""
        ...

    @property
    def change(self) -> Decimal:
        """전일대비"""
        ...

    @property
    def indicator(self) -> "KisIndicator":
        """종목 지표"""
        ...

    @property
    def open(self) -> Decimal:
        """당일시가"""
        ...

    @property
    def high(self) -> Decimal:
        """당일고가"""
        ...

    @property
    def low(self) -> Decimal:
        """당일저가"""
        ...

    @property
    def high_limit(self) -> Decimal:
        """상한가"""
        ...

    @property
    def low_limit(self) -> Decimal:
        """하한가"""
        ...

    @property
    def unit(self) -> Decimal:
        """거래단위"""
        ...

    @property
    def tick(self) -> Decimal:
        """호가단위"""
        ...

    @property
    def decimal_places(self) -> int:
        """소수점 자리수"""
        ...

    @property
    def exchange_rate(self) -> Decimal:
        """당일환율"""
        ...

    @property
    def close(self) -> Decimal:
        """당일종가 (현재가)"""
        return self.price

    @property
    def rate(self) -> Decimal:
        """등락율 (-100~100)"""
        return safe_divide(self.change, self.prev_price) * 100

    @property
    def sign_name(self) -> str:
        """대비부호명"""
        return STOCK_SIGN_TYPE_KOR_MAP[self.sign]


@runtime_checkable
class KisIndicator(Protocol):
    """한국투자증권 종목 지표"""

    @property
    def eps(self) -> Decimal:
        """EPS (주당순이익)"""
        ...

    @property
    def bps(self) -> Decimal:
        """BPS (주당순자산)"""
        ...

    @property
    def per(self) -> Decimal:
        """PER (주가수익비율)"""
        ...

    @property
    def pbr(self) -> Decimal:
        """PBR (주가순자산비율)"""
        ...

    @property
    def week52_high(self) -> Decimal:
        """52주 최고가"""
        ...

    @property
    def week52_low(self) -> Decimal:
        """52주 최저가"""
        ...

    @property
    def week52_high_date(self) -> date:
        """52주 최고가 날짜"""
        ...

    @property
    def week52_low_date(self) -> date:
        """52주 최저가 날짜"""
        ...


@runtime_checkable
class KisQuoteResponse(KisQuote, KisResponseProtocol, Protocol):
    """한국투자증권 상품 시세 응답"""


@kis_repr(
    "eps",
    "bps",
    "per",
    "pbr",
    "week52_high",
    "week52_low",
    "week52_high_date",
    "week52_low_date",
    lines="multiple",
)
class KisIndicatorRepr:
    """한국투자증권 종목 지표"""


@kis_repr(
    "symbol",
    "market",
    "name",
    "sector_name",
    "volume",
    "amount",
    "market_cap",
    "indicator",
    "open",
    "high",
    "low",
    "close",
    "change",
    "unit",
    "tick",
    "risk",
    "halt",
    "overbought",
    lines="multiple",
    field_lines={
        "indicator": "multiple",
    },
)
class KisQuoteRepr:
    """한국투자증권 상품 시세"""


class KisQuoteBase(KisQuoteRepr, KisProductBase):
    """한국투자증권 상품 시세"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    sector_name: str | None
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
    prev_volume_rate: Decimal
    """전일대비거래량비율 (-100~100)"""

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

    high_limit: Decimal
    """상한가"""
    low_limit: Decimal
    """하한가"""
    base_price: Decimal
    """기준가"""
    unit: Decimal
    """거래단위"""
    tick: Decimal
    """호가단위"""
    decimal_places: int
    """소수점 자리수"""

    exchange_rate: Decimal
    """당일환율"""

    @property
    def close(self) -> Decimal:
        """당일종가 (현재가)"""
        return self.price

    @property
    def rate(self) -> Decimal:
        """등락율 (-100~100)"""
        return safe_divide(self.change, self.prev_price) * 100

    @property
    def sign_name(self) -> str:
        """대비부호명"""
        return STOCK_SIGN_TYPE_KOR_MAP[self.sign]


class KisDomesticIndicator(KisIndicatorRepr, KisDynamic):
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


class KisDomesticQuote(KisQuoteBase, KisAPIResponse):
    """한국투자증권 국내 상품 시세"""

    symbol: str = KisString["stck_shrn_iscd"]
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    sector_name: str | None = KisString["bstp_kor_isnm", None]
    """업종명"""
    price: Decimal = KisDecimal["stck_prpr"]
    """현재가"""
    volume: int = KisInt["acml_vol"]
    """거래량"""
    amount: Decimal = KisDecimal["acml_tr_pbmn"]
    """거래대금"""
    market_cap: Decimal = KisDecimal["hts_avls"]
    """시가총액"""
    sign: STOCK_SIGN_TYPE = KisAny(STOCK_SIGN_TYPE_MAP.__getitem__)["prdy_vrss_sign"]
    """대비부호"""
    risk: STOCK_RISK_TYPE = KisAny(STOCK_RISK_TYPE_MAP.__getitem__)["mrkt_warn_cls_code"]
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
        return safe_divide(self.volume, (1 + safe_divide(self.prev_volume_rate, 100)))

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

    exchange_rate: Decimal = Decimal(1)
    """당일환율"""

    def __init__(self, symbol: str, market: MARKET_TYPE):
        super().__init__()
        self.symbol = symbol
        self.market = market

    def __pre_init__(self, data: dict):
        if data["output"]["stck_prpr"] == "0":
            raise_not_found(
                data,
                "해당 종목의 현재가를 조회할 수 없습니다.",
                code=self.symbol,
                market=self.market,
            )

        super().__pre_init__(data)


class KisForeignIndicator(KisIndicatorRepr, KisDynamic):
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


class KisForeignQuote(KisQuoteBase, KisAPIResponse):
    """한국투자증권 해외 상품 시세"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    sector_name: str | None = KisString["e_icod"]
    """업종명"""
    price: Decimal = KisDecimal["last"]
    """현재가"""
    volume: int = KisInt["tvol"]
    """거래량"""
    amount: Decimal = KisDecimal["tamt"]
    """거래대금"""
    market_cap: Decimal = KisDecimal["tomv"]
    """시가총액"""

    sign: STOCK_SIGN_TYPE = KisAny(STOCK_SIGN_TYPE_MAP.__getitem__)["t_xsgn"]
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
        return safe_divide(self.volume, self.prev_volume) * 100 - 100

    prev_volume: Decimal = KisDecimal["pvol"]
    """전일거래량"""

    @property
    def change(self) -> Decimal:
        """전일대비"""
        return self.price - self.prev_price

    # Pylance bug: cached_property[KisForeignIndicator] type inference error.
    @cached_property
    def indicator(self) -> KisForeignIndicator:  # type: ignore
        """종목 지표"""
        return foreign_quote(
            self.kis,
            symbol=self.symbol,
            market=self.market,
            extended=False,
        ).indicator

    indicator: KisForeignIndicator

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

    exchange_rate: Decimal = KisDecimal["t_rate"]
    """당일환율"""

    extended: bool
    """주간거래 시세 조회 여부"""

    def __init__(self, symbol: str, market: MARKET_TYPE, extended: bool):
        super().__init__()
        self.symbol = symbol
        self.market = market
        self.extended = extended

    def __pre_init__(self, data: dict):
        if not data["output"]["last"]:
            raise_not_found(
                data,
                "해당 종목의 현재가를 조회할 수 없습니다.",
                code=self.symbol,
                market=self.market,
            )

        super().__pre_init__(data)

        if not self.extended:
            self.indicator = KisObject.transform_(
                data["output"],
                KisForeignIndicator,
                ignore_missing=True,
            )


def domestic_quote(
    self: "PyKis",
    symbol: str,
) -> KisDomesticQuote:
    """
    한국투자증권 국내 주식 현재가 조회

    주식, ETF, ETN 조회가 가능합니다.

    국내주식시세 -> 주식현재가 시세[v1_국내주식-008]
    (업데이트 날짜: 2023/09/24)

    Args:
        symbol (str): 종목코드

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    if not symbol:
        raise ValueError("종목코드를 입력해주세요.")

    result = KisDomesticQuote(symbol, "KRX")

    return self.fetch(
        "/uapi/domestic-stock/v1/quotations/inquire-price",
        api="FHKST01010100",
        params={
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
        },
        response_type=result,
        domain="real",
    )


def foreign_quote(
    self: "PyKis",
    symbol: str,
    market: MARKET_TYPE,
    extended: bool = False,
) -> KisForeignQuote:
    """
    한국투자증권 해외 주식 현재가 조회

    해외주식현재가 -> 해외주식 현재가상세[v1_해외주식-029]
    (업데이트 날짜: 2023/10/01)

    Args:
        symbol (str): 종목코드
        market (MARKET_TYPE): 시장구분
        extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    if not symbol:
        raise ValueError("종목코드를 입력해주세요.")

    if extended:
        market_code = DAYTIME_MARKET_SHORT_TYPE_MAP.get(market)

        if not market_code:
            raise ValueError(f"주간거래 시세 조회가 불가능한 시장입니다. ({market})")
    else:
        market_code = MARKET_SHORT_TYPE_MAP[market]

    return self.fetch(
        "/uapi/overseas-price/v1/quotations/price-detail",
        api="HHDFS76200200",
        params={
            "AUTH": "",
            "EXCD": market_code,
            "SYMB": symbol,
        },
        response_type=KisForeignQuote(
            symbol=symbol,
            market=market,
            extended=extended,
        ),
        domain="real",
    )


def quote(
    self: "PyKis",
    symbol: str,
    market: MARKET_TYPE,
    extended: bool = False,
) -> KisQuoteResponse:
    """
    한국투자증권 주식 현재가 조회

    국내주식시세 -> 주식현재가 시세[v1_국내주식-008]
    해외주식현재가 -> 해외주식 현재가상세[v1_해외주식-029]

    Args:
        symbol (str): 종목코드
        market (MARKET_TYPE): 시장구분
        extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    if market == "KRX":
        return domestic_quote(self, symbol=symbol)
    else:
        return foreign_quote(
            self,
            symbol=symbol,
            market=market,
            extended=extended,
        )


def product_quote(
    self: "KisProductProtocol",
    extended: bool = False,
) -> KisQuoteResponse:
    """
    한국투자증권 주식 현재가 조회

    국내주식시세 -> 주식현재가 시세[v1_국내주식-008]
    해외주식현재가 -> 해외주식 현재가상세[v1_해외주식-029]

    Args:
        extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    return quote(
        self.kis,
        symbol=self.symbol,
        market=self.market,
        extended=extended,
    )
