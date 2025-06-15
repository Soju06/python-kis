from enum import Flag
from typing import Any, Literal
from zoneinfo import ZoneInfo

from pykis.responses.dynamic import KisType, KisTypeMeta

__all__ = [
    "EXCHANGE_TYPE",
    "CURRENCY_TYPE",
    "get_exchange_name",
    "get_exchange_currency",
    "get_exchange_timezone",
    "ExDateType",
]


EXCHANGE_TYPE = Literal[
    "KRX",
    "NASDAQ",
    "NYSE",
    "AMEX",
    "TYO",
    "HKEX",
    "HNX",
    "HSX",
    "SSE",
    "SZSE",
]
"""시장 종류"""

CURRENCY_TYPE = Literal[
    "KRW",
    "USD",
    "JPY",
    "HKD",
    "VND",
    "CNY",
]
"""통화 종류"""

EXCHANGE_CODE_MAP: dict[EXCHANGE_TYPE, str] = {
    "NASDAQ": "NASD",
    "NYSE": "NYSE",
    "AMEX": "AMEX",
    "TYO": "TKSE",
    "HKEX": "SEHK",
    "HNX": "HASE",
    "HSX": "VNSE",
    "SSE": "SHAA",
    "SZSE": "SZAA",
}

REVERSE_EXCHANGE_CODE_MAP: dict[str, EXCHANGE_TYPE] = {value: key for key, value in EXCHANGE_CODE_MAP.items()}


def get_exchange_code(exchange: EXCHANGE_TYPE) -> str:
    """시장 종류로 시장 코드 반환"""
    return EXCHANGE_CODE_MAP[exchange]


def get_exchange_type(code: str) -> EXCHANGE_TYPE:
    """시장 코드로 시장 종류 반환"""
    return REVERSE_EXCHANGE_CODE_MAP[code]


EXCHANGE_SHORT_TYPE_MAP: dict[EXCHANGE_TYPE, str] = {
    "NASDAQ": "NAS",
    "NYSE": "NYS",
    "AMEX": "AMS",
    "TYO": "TSE",
    "HKEX": "HKS",
    "HNX": "HNX",
    "HSX": "HSX",
    "SSE": "SHS",
    "SZSE": "SZS",
}

REVERSE_EXCHANGE_SHORT_TYPE_MAP: dict[str, EXCHANGE_TYPE] = {
    value: key for key, value in EXCHANGE_SHORT_TYPE_MAP.items()
}

DAYTIME_EXCHANGES = {
    "NASDAQ",
    "NYSE",
    "AMEX",
}

DAYTIME_EXCHANGE_SHORT_TYPE_MAP: dict[EXCHANGE_TYPE, str] = {
    "NASDAQ": "BAQ",
    "NYSE": "BAY",
    "AMEX": "BAA",
}

REVERSE_DAYTIME_EXCHANGE_SHORT_TYPE_MAP: dict[str, EXCHANGE_TYPE] = {
    value: key for key, value in DAYTIME_EXCHANGE_SHORT_TYPE_MAP.items()
}

EXCHANGE_TYPE_KOR_MAP: dict[EXCHANGE_TYPE | None, str] = {
    None: "전체",
    "KRX": "국내",
    "NASDAQ": "나스닥",
    "NYSE": "뉴욕",
    "AMEX": "아멕스",
    "TYO": "일본",
    "HKEX": "홍콩",
    "HNX": "하노이",
    "HSX": "호치민",
    "SSE": "상하이",
    "SZSE": "심천",
}


def get_exchange_name(exchange: EXCHANGE_TYPE | None) -> str:
    """시장 종류로 시장 이름 반환"""
    return EXCHANGE_TYPE_KOR_MAP[exchange]


EXCHANGE_CURRENCY_MAP: dict[EXCHANGE_TYPE, CURRENCY_TYPE] = {
    "KRX": "KRW",
    "NASDAQ": "USD",
    "NYSE": "USD",
    "AMEX": "USD",
    "TYO": "JPY",
    "HKEX": "HKD",
    "HNX": "VND",
    "HSX": "VND",
    "SSE": "CNY",
    "SZSE": "CNY",
}


def get_exchange_currency(exchange: EXCHANGE_TYPE) -> CURRENCY_TYPE:
    """시장 종류로 통화 종류 반환"""
    return EXCHANGE_CURRENCY_MAP[exchange]


EXCHANGE_TIMEZONE_MAP = {
    "KRX": "Asia/Seoul",
    "NASDAQ": "America/New_York",
    "NYSE": "America/New_York",
    "AMEX": "America/New_York",
    "TYO": "Asia/Tokyo",
    "HKEX": "Asia/Hong_Kong",
    "HNX": "Asia/Ho_Chi_Minh",
    "HSX": "Asia/Ho_Chi_Minh",
    "SSE": "Asia/Shanghai",
    "SZSE": "Asia/Shanghai",
}

EXCHANGE_TIMEZONE_OBJECT_MAP = {key: ZoneInfo(value) for key, value in EXCHANGE_TIMEZONE_MAP.items()}


def get_exchange_timezone(exchange: EXCHANGE_TYPE) -> ZoneInfo:
    """시장 종류로 시간대 반환"""
    return EXCHANGE_TIMEZONE_OBJECT_MAP[exchange]


def get_exchange_code_timezone(exchange: str) -> ZoneInfo:
    """시장 종류로 시간대 반환"""
    return get_exchange_timezone(get_exchange_type(exchange))


class ExDateType(Flag):
    """락 구분"""

    NONE = 0
    """없음"""

    INTERIM = 1
    """중간 구분"""
    QUARTERLY = 2
    """분기 구분"""

    EX_DIVIDEND = 4
    """배당락"""
    EX_RIGHTS = 8
    """권리락"""
    EX_DISTRIBUTION = 16
    """분배락"""

    def __str__(self) -> str:
        """락 구분 한글로 변환"""
        return EX_DATE_TYPE_KOR_MAP[self]

    @classmethod
    def from_code(cls, code: str) -> "ExDateType":
        """락 구분 코드로 락 구분 생성"""
        return cls(EX_DATE_TYPE_CODE_MAP[code])


EX_DATE_TYPE_CODE_MAP = {
    "00": ExDateType.NONE,
    "01": ExDateType.EX_RIGHTS,
    "02": ExDateType.EX_DIVIDEND,
    "03": ExDateType.EX_DISTRIBUTION,
    "04": ExDateType.EX_RIGHTS | ExDateType.EX_DIVIDEND,
    "05": ExDateType.INTERIM | ExDateType.QUARTERLY | ExDateType.EX_DIVIDEND,
    "06": ExDateType.INTERIM | ExDateType.EX_RIGHTS | ExDateType.EX_DIVIDEND,
    "07": ExDateType.QUARTERLY | ExDateType.EX_RIGHTS | ExDateType.EX_DIVIDEND,
}

EX_DATE_TYPE_KOR_MAP = {
    ExDateType.NONE: "없음",
    ExDateType.INTERIM: "중간",
    ExDateType.QUARTERLY: "분기",
    ExDateType.EX_DIVIDEND: "배당락",
    ExDateType.EX_RIGHTS: "권리락",
    ExDateType.EX_DISTRIBUTION: "분배락",
    ExDateType.EX_RIGHTS | ExDateType.EX_DIVIDEND: "권리락/배당락",
    ExDateType.INTERIM | ExDateType.QUARTERLY | ExDateType.EX_DIVIDEND: "중간/분기/배당락",
    ExDateType.INTERIM | ExDateType.EX_RIGHTS | ExDateType.EX_DIVIDEND: "중간/권리락/배당락",
    ExDateType.QUARTERLY | ExDateType.EX_RIGHTS | ExDateType.EX_DIVIDEND: "분기/권리락/배당락",
}


class KisExchangeType(KisType[EXCHANGE_TYPE], metaclass=KisTypeMeta[EXCHANGE_TYPE]):
    __default__ = []

    def __init__(self):
        super().__init__()

    def transform(self, data: Any) -> EXCHANGE_TYPE:
        try:
            return get_exchange_type(data)
        except KeyError:
            raise ValueError(f"올바르지 않은 시장 종류입니다: {data}")
