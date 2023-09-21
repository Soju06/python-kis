from datetime import time, tzinfo
from typing import Literal

import pytz

from pykis.responses.dynamic import KisDynamic
from pykis.responses.types import KisTime


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

MARKET_TYPE_SHORT_MAP = {
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

MARKET_TYPE_KOR_MAP = {
    None: "전체",
    "KRX": "한국",
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


class KisTradingHours(KisDynamic):
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
        return pytz.timezone(MARKET_TIMEZONE_MAP[self.market])
