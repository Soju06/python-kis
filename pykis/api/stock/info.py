from datetime import timedelta
from typing import TYPE_CHECKING, Literal, Protocol, runtime_checkable

from pykis.api.stock.exchange import EXCHANGE_SHORT_TYPE_MAP, EXCHANGE_TYPE
from pykis.client.exceptions import KisAPIError
from pykis.responses.response import (
    KisAPIResponse,
    KisResponseProtocol,
    raise_not_found,
)
from pykis.responses.types import KisDynamicDict, KisString
from pykis.utils.repr import kis_repr

if TYPE_CHECKING:
    from pykis.kis import PyKis

__all__ = [
    "KisStockInfo",
    "KisStockInfoResponse",
    "COUNTRY_TYPE",
    "get_exchange_country",
    "EXCHANGE_INFO_TYPES",
    "info",
    "resolve_exchange",
]

EXCHANGE_TYPE_MAP: dict[str | None, list[str]] = {
    "KR": ["300"],  # "301", "302"
    "KRX": ["300"],  # "301", "302"
    "NASDAQ": ["512"],
    "NYSE": ["513"],
    "AMEX": ["529"],
    "US": ["512", "513", "529"],
    "TYO": ["515"],
    "JP": ["515"],
    "HKEX": ["501"],
    "HK": ["501", "543", "558"],
    "HNX": ["507"],
    "HSX": ["508"],
    "VN": ["507", "508"],
    "SSE": ["551"],
    "SZSE": ["552"],
    "CN": ["551", "552"],
    None: [
        "300",
        # "301",
        # "302",
        "512",
        "513",
        "529",
        "515",
        "501",
        "543",
        "558",
        "551",
        "552",
        "507",
        "508",
    ],
}

R_EXCHANGE_TYPE_MAP: dict[str, str] = {
    "300": "주식",
    "301": "선물옵션",
    "302": "채권",
    "512": "나스닥",
    "513": "뉴욕",
    "529": "아멕스",
    "515": "일본",
    "501": "홍콩",
    "543": "홍콩CNY",
    "558": "홍콩USD",
    "507": "하노이",
    "508": "호치민",
    "551": "상하이",
    "552": "심천",
}


EXCHANGE_CODE = Literal[
    "300",
    "301",
    "302",
    "512",
    "513",
    "529",
    "515",
    "501",
    "543",
    "558",
    "507",
    "508",
    "551",
    "552",
]

EXCHANGE_CODE_MAP: dict[str, EXCHANGE_TYPE] = {
    "300": "KRX",
    "301": "KRX",
    "302": "KRX",
    "512": "NASDAQ",
    "513": "NYSE",
    "529": "AMEX",
    "515": "TYO",
    "501": "HKEX",
    "543": "HKEX",
    "558": "HKEX",
    "507": "HNX",
    "508": "HSX",
    "551": "SSE",
    "552": "SZSE",
}


@runtime_checkable
class KisStockInfo(Protocol):
    """상품기본정보"""

    @property
    def symbol(self) -> str:
        """종목코드"""
        ...

    @property
    def std_code(self) -> str:
        """표준코드"""
        ...

    @property
    def name_kor(self) -> str:
        """종목명"""
        ...

    @property
    def full_name_kor(self) -> str:
        """종목전체명"""
        ...

    @property
    def name_eng(self) -> str:
        """종목영문명"""
        ...

    @property
    def full_name_eng(self) -> str:
        """종목영문전체명"""
        ...

    @property
    def name(self) -> str:
        """종목명"""
        ...

    @property
    def exchange(self) -> EXCHANGE_TYPE:
        """상품유형타입"""
        ...

    @property
    def exchange_name(self) -> str:
        """상품유형명"""
        ...

    @property
    def foreign(self) -> bool:
        """해외종목 여부"""
        ...

    @property
    def domestic(self) -> bool:
        """국내종목 여부"""
        ...


@runtime_checkable
class KisStockInfoResponse(KisStockInfo, KisResponseProtocol, Protocol):
    """상품기본정보 응답"""


@kis_repr(
    "exchange",
    "symbol",
    "name",
    "name_eng",
    lines="single",
)
class KisStockInfoRepr:
    """상품기본정보"""


class _KisStockInfo(KisStockInfoRepr, KisAPIResponse):
    """상품기본정보"""

    symbol: str = KisString["shtn_pdno"]
    """종목코드"""
    std_code: str = KisString["std_pdno"]
    """표준코드"""
    name_kor: str = KisString["prdt_abrv_name"]
    """종목명"""
    full_name_kor: str = KisString["prdt_name120"]
    """종목전체명"""
    name_eng: str = KisString["prdt_eng_abrv_name"]
    """종목영문명"""
    full_name_eng: str = KisString["prdt_eng_name120"]
    """종목영문전체명"""

    @property
    def name(self) -> str:
        """종목명"""
        return self.name_kor

    exchange_code: EXCHANGE_CODE = KisString["prdt_type_cd"]
    """상품유형코드"""

    @property
    def exchange(self) -> EXCHANGE_TYPE:
        """상품유형타입"""
        return EXCHANGE_CODE_MAP[self.exchange_code]  # type: ignore

    @property
    def exchange_name(self) -> str:
        """상품유형명"""
        return R_EXCHANGE_TYPE_MAP[self.exchange_code]

    @property
    def foreign(self) -> bool:
        """해외종목 여부"""
        return self.exchange_code not in EXCHANGE_TYPE_MAP["KRX"]

    @property
    def domestic(self) -> bool:
        """국내종목 여부"""
        return not self.foreign


COUNTRY_TYPE = Literal["KR", "US", "HK", "JP", "VN", "CN"]
"""국가유형명"""

EXCHANGE_COUNTRY_MAP: dict[EXCHANGE_TYPE, COUNTRY_TYPE] = {
    "KRX": "KR",
    "NASDAQ": "US",
    "NYSE": "US",
    "AMEX": "US",
    "HKEX": "HK",
    "TYO": "JP",
    "HNX": "VN",
    "HSX": "VN",
    "SSE": "CN",
    "SZSE": "CN",
}


def get_exchange_country(exchange: EXCHANGE_TYPE) -> COUNTRY_TYPE:
    """상품유형명을 국가유형명으로 변환합니다."""
    if country := EXCHANGE_COUNTRY_MAP.get(exchange):
        return country

    raise ValueError(f"지원하지 않는 상품유형명입니다. {exchange}")


EXCHANGE_INFO_TYPES = EXCHANGE_TYPE | COUNTRY_TYPE | None
"""상품유형명"""


def quotable_exchange(
    self: "PyKis",
    symbol: str,
    exchange: EXCHANGE_INFO_TYPES = None,
    use_cache: bool = True,
) -> EXCHANGE_TYPE:
    """
    시세조회 가능한 상품유형명 조회

    국내주식시세 -> 주식현재가 시세[v1_국내주식-008]
    해외주식현재가 -> 해외주식 현재가상세[v1_해외주식-029]
    (업데이트 날짜: 2024/11/05)

    Args:
        symbol (str): 종목코드
        exchange (str): 상품유형명
        use_cache (bool, optional): 캐시 사용 여부
    """
    if not symbol:
        raise ValueError("종목 코드를 입력해주세요.")

    if use_cache:
        cached: EXCHANGE_TYPE = self.cache.get(f"quotable_exchange:{exchange}:{symbol}", str)  # type: ignore

        if cached:
            return cached

    last_response: KisDynamicDict | None = None

    for exchange_code in EXCHANGE_TYPE_MAP[exchange]:
        try:
            exchange_type = EXCHANGE_CODE_MAP[exchange_code]

            if exchange_code in EXCHANGE_TYPE_MAP["KR"]:
                if not int(
                    (
                        last_response := self.fetch(
                            "/uapi/domestic-stock/v1/quotations/inquire-price",
                            api="FHKST01010100",
                            params={"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": symbol},
                            domain="real",
                        )
                    ).output.stck_prpr
                ):
                    continue
            elif not (
                (
                    last_response := self.fetch(
                        "/uapi/overseas-price/v1/quotations/price",
                        api="HHDFS00000300",
                        params={"AUTH": "", "EXCD": EXCHANGE_SHORT_TYPE_MAP[exchange_type], "SYMB": symbol},
                        domain="real",
                    )
                ).output.last
            ):
                continue

            return exchange_type
        except AttributeError:
            pass

    raise raise_not_found(
        (None if last_response is None else last_response.__data__) or {},
        "해당 종목의 정보를 조회할 수 없습니다.",
        code=symbol,
        exchange=exchange,
    )


def info(
    self: "PyKis",
    symbol: str,
    exchange: EXCHANGE_INFO_TYPES = "KR",
    use_cache: bool = True,
    quotable: bool = True,
) -> KisStockInfoResponse:
    """
    상품기본정보 조회

    국내주식시세 -> 상품기본조회[v1_국내주식-029]
    (업데이트 날짜: 2023/09/05)

    Args:
        symbol (str): 종목코드
        exchange (str): 상품유형명
        use_cache (bool, optional): 캐시 사용 여부
        quotable (bool, optional): 시세조회 가능한 상품유형명 조회

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    if not symbol:
        raise ValueError("종목 코드를 입력해주세요.")

    if use_cache:
        cached = self.cache.get(f"info:{exchange}:{symbol}", _KisStockInfo)

        if cached:
            return cached

    if quotable:
        exchange = quotable_exchange(
            self,
            symbol=symbol,
            exchange=exchange,
            use_cache=use_cache,
        )

    ex = None

    for exchange_ in EXCHANGE_TYPE_MAP[exchange]:
        try:
            result = self.fetch(
                "/uapi/domestic-stock/v1/quotations/search-info",
                api="CTPF1604R",
                params={
                    "PDNO": symbol,
                    "PRDT_TYPE_CD": exchange_,
                },
                domain="real",
                response_type=_KisStockInfo,
            )

            if use_cache:
                self.cache.set(f"info:{exchange}:{symbol}", result, expire=timedelta(days=1))

            return result
        except KisAPIError as e:
            if e.rt_cd == 7:
                # 조회된 데이터가 없는 경우
                ex = e
                continue

            raise e

    raise raise_not_found(
        ex.data if ex else {},
        "해당 종목의 정보를 조회할 수 없습니다.",
        code=symbol,
        exchange=exchange,
    )


def resolve_exchange(
    self: "PyKis",
    symbol: str,
    exchange: EXCHANGE_INFO_TYPES = None,
    use_cache: bool = True,
    quotable: bool = True,
) -> EXCHANGE_TYPE:
    """
    상품유형명 해석

    국내주식시세 -> 상품기본조회[v1_국내주식-029]
    (업데이트 날짜: 2024/03/30)

    Args:
        symbol (str): 종목코드
        exchange (str): 상품유형명
        use_cache (bool, optional): 캐시 사용 여부
        quotable (bool, optional): 시세조회 가능한 상품유형명 조회

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    return info(
        self,
        symbol=symbol,
        exchange=exchange,
        use_cache=use_cache,
        quotable=quotable,
    ).exchange
