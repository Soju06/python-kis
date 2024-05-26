from datetime import time, tzinfo
from enum import Flag
from typing import Literal, Protocol, runtime_checkable
from zoneinfo import ZoneInfo

from pykis.api.base.market import KisMarketBase, KisMarketProtocol

__all__ = [
    "MARKET_TYPE",
    "CURRENCY_TYPE",
    "get_market_name",
    "get_market_currency",
    "get_market_timezone",
    "ExDateType",
    "KisTradingHours",
]


MARKET_TYPE = Literal[
    "KRX",
    "NASD",
    "NYSE",
    "AMEX",
    "TKSE",
    "SEHK",
    "HASE",
    "VNSE",
    "SHAA",
    "SZAA",
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

MARKET_SHORT_TYPE_MAP: dict[MARKET_TYPE, str] = {
    "NASD": "NAS",
    "NYSE": "NYS",
    "AMEX": "AMS",
    "TKSE": "TSE",
    "SEHK": "HKS",
    "HASE": "HNX",
    "VNSE": "HSX",
    "SHAA": "SHS",
    "SZAA": "SZS",
}

REVERSE_MARKET_SHORT_TYPE_MAP: dict[str, MARKET_TYPE] = {
    value: key for key, value in MARKET_SHORT_TYPE_MAP.items()
}

DAYTIME_MARKETS = {
    "NASD",
    "NYSE",
    "AMEX",
}

DAYTIME_MARKET_SHORT_TYPE_MAP: dict[MARKET_TYPE, str] = {
    "NASD": "BAQ",
    "NYSE": "BAY",
    "AMEX": "BAA",
}

REVERSE_DAYTIME_MARKET_SHORT_TYPE_MAP: dict[str, MARKET_TYPE] = {
    value: key for key, value in DAYTIME_MARKET_SHORT_TYPE_MAP.items()
}

MARKET_TYPE_KOR_MAP: dict[MARKET_TYPE | None, str] = {
    None: "전체",
    "KRX": "국내",
    "NASD": "나스닥",
    "NYSE": "뉴욕",
    "AMEX": "아멕스",
    "TKSE": "일본",
    "SEHK": "홍콩",
    "HASE": "하노이",
    "VNSE": "호치민",
    "SHAA": "상해",
    "SZAA": "심천",
}


def get_market_name(market: MARKET_TYPE | None) -> str:
    """시장 종류로 시장 이름 반환"""
    return MARKET_TYPE_KOR_MAP[market]


MARKET_CURRENCY_MAP: dict[MARKET_TYPE, CURRENCY_TYPE] = {
    "KRX": "KRW",
    "NASD": "USD",
    "NYSE": "USD",
    "AMEX": "USD",
    "TKSE": "JPY",
    "SEHK": "HKD",
    "HASE": "VND",
    "VNSE": "VND",
    "SHAA": "CNY",
    "SZAA": "CNY",
}


def get_market_currency(market: MARKET_TYPE) -> CURRENCY_TYPE:
    """시장 종류로 통화 종류 반환"""
    return MARKET_CURRENCY_MAP[market]


MARKET_TIMEZONE_MAP = {
    "KRX": "Asia/Seoul",
    "NASD": "America/New_York",
    "NYSE": "America/New_York",
    "AMEX": "America/New_York",
    "TKSE": "Asia/Tokyo",
    "SEHK": "Asia/Hong_Kong",
    "HASE": "Asia/Ho_Chi_Minh",
    "VNSE": "Asia/Ho_Chi_Minh",
    "SHAA": "Asia/Shanghai",
    "SZAA": "Asia/Shanghai",
}

MARKET_TIMEZONE_OBJECT_MAP = {key: ZoneInfo(value) for key, value in MARKET_TIMEZONE_MAP.items()}


def get_market_timezone(market: MARKET_TYPE) -> ZoneInfo:
    """시장 종류로 시간대 반환"""
    return MARKET_TIMEZONE_OBJECT_MAP[market]


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


@runtime_checkable
class KisTradingHours(KisMarketProtocol, Protocol):
    """한국투자증권 장 운영 시간"""

    @property
    def market(self) -> MARKET_TYPE:
        """시장 종류"""
        raise NotImplementedError

    @property
    def open(self) -> time:
        """장 시작 시간"""
        raise NotImplementedError

    @property
    def open_kst(self) -> time:
        """장 시작 시간 (한국시간)"""
        raise NotImplementedError

    @property
    def close(self) -> time:
        """장 종료 시간"""
        raise NotImplementedError

    @property
    def close_kst(self) -> time:
        """장 종료 시간 (한국시간)"""
        raise NotImplementedError

    @property
    def timezone(self) -> tzinfo:
        """시간대"""
        raise NotImplementedError

    @property
    def market_name(self) -> str:
        """시장 종류"""
        raise NotImplementedError


class KisTradingHoursBase(KisMarketBase):
    """한국투자증권 장 운영 시간"""

    market: MARKET_TYPE
    """시장 종류"""
    open: time
    """장 시작 시간"""
    open_kst: time
    """장 시작 시간 (한국시간)"""
    close: time
    """장 종료 시간"""
    close_kst: time
    """장 종료 시간 (한국시간)"""

    @property
    def timezone(self) -> tzinfo:
        """시간대"""
        return get_market_timezone(self.market)

    @property
    def market_name(self) -> str:
        """시장 종류"""
        return get_market_name(self.market)
