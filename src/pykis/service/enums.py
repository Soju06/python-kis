"""Unified service-layer enums for domain models."""

from __future__ import annotations

from enum import StrEnum


class Exchange(StrEnum):
    """Stock exchange identifier (unified across domestic/overseas)."""

    # Domestic
    KRX = "KRX"
    """Korea Exchange (KOSPI + KOSDAQ)"""
    NXT = "NXT"
    """Korea NXT exchange"""

    # US
    NYSE = "NYSE"
    """New York Stock Exchange"""
    NASDAQ = "NASDAQ"
    """NASDAQ"""
    AMEX = "AMEX"
    """NYSE American (AMEX)"""
    NYSE_EXTENDED = "NYSE_EXTENDED"
    """New York Stock Exchange (extended/daytime hours)"""
    NASDAQ_EXTENDED = "NASDAQ_EXTENDED"
    """NASDAQ (extended/daytime hours)"""
    AMEX_EXTENDED = "AMEX_EXTENDED"
    """NYSE American (extended/daytime hours)"""

    # Asia
    TSE = "TSE"
    """Tokyo Stock Exchange"""
    SEHK = "SEHK"
    """Hong Kong Stock Exchange"""
    SSE = "SSE"
    """Shanghai Stock Exchange"""
    SZSE = "SZSE"
    """Shenzhen Stock Exchange"""
    HSX = "HSX"
    """Ho Chi Minh Stock Exchange"""
    HNX = "HNX"
    """Hanoi Stock Exchange"""

    # Index
    SSE_INDEX = "SSE_INDEX"
    """Shanghai Stock Exchange Index"""
    SZSE_INDEX = "SZSE_INDEX"
    """Shenzhen Stock Exchange Index"""

    @property
    def is_domestic(self) -> bool:
        return self in _DOMESTIC_EXCHANGES

    @property
    def is_overseas(self) -> bool:
        return not self.is_domestic

    @property
    def is_extended_hours(self) -> bool:
        return self in _EXTENDED_EXCHANGES


_DOMESTIC_EXCHANGES: frozenset[Exchange] = frozenset({Exchange.KRX, Exchange.NXT})

_EXTENDED_EXCHANGES: frozenset[Exchange] = frozenset({
    Exchange.NYSE_EXTENDED,
    Exchange.NASDAQ_EXTENDED,
    Exchange.AMEX_EXTENDED,
})


class ChangeSign(StrEnum):
    """Price change direction indicator."""

    UPPER_LIMIT = "upper_limit"
    """Upper limit (상한)"""
    RISE = "rise"
    """Rise (상승)"""
    FLAT = "flat"
    """Flat / no change (보합)"""
    LOWER_LIMIT = "lower_limit"
    """Lower limit (하한)"""
    FALL = "fall"
    """Fall (하락)"""


class MarketWarning(StrEnum):
    """Market warning classification for stocks."""

    NONE = "none"
    """No warning (없음)"""
    CAUTION = "caution"
    """Investment caution (투자주의)"""
    WARNING = "warning"
    """Investment warning (투자경고)"""
    RISK = "risk"
    """Investment risk (투자위험)"""
