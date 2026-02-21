from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InstrumentKey:
    asset_class: str
    market: str
    symbol: str


@dataclass(frozen=True, slots=True)
class Instrument:
    """Normalized instrument representation used by the store service layer."""

    key: InstrumentKey
    name: str | None
    short_code: str | None
    standard_code: str | None
    isin: str | None
    source_id: str
    version: str | None = None
