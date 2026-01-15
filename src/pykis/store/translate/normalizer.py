from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol

from pykis.store.raw.models import RawRecord
from pykis.store.translate.models import Instrument, InstrumentKey


class Normalizer(Protocol):
    def normalize(self, record: RawRecord) -> Instrument | None: ...


@dataclass(frozen=True, slots=True)
class FieldMap:
    symbol: str
    name: str | None = None
    market: str | None = None
    asset_class: str | None = None
    short_code: str | None = None
    standard_code: str | None = None
    isin: str | None = None


@dataclass(frozen=True, slots=True)
class FieldMapNormalizer:
    """Map raw fields into a normalized Instrument.

    This is intentionally strict and minimal. Any advanced logic should live in
    a dedicated normalizer implementation.
    """

    mapping: FieldMap
    defaults: Mapping[str, str]
    version: str | None = None

    def normalize(self, record: RawRecord) -> Instrument | None:
        fields = record.fields
        symbol = _normalize_symbol(fields.get(self.mapping.symbol))
        if not symbol:
            return None

        market = _pick_field(fields, self.mapping.market, self.defaults.get("market"))
        asset_class = _pick_field(fields, self.mapping.asset_class, self.defaults.get("asset_class"))
        if not market or not asset_class:
            return None

        key = InstrumentKey(asset_class=asset_class, market=market, symbol=symbol)
        return Instrument(
            key=key,
            name=_pick_field(fields, self.mapping.name, None),
            short_code=_pick_field(fields, self.mapping.short_code, None),
            standard_code=_pick_field(fields, self.mapping.standard_code, None),
            isin=_pick_field(fields, self.mapping.isin, None),
            source_id=record.source_id,
            version=self.version,
        )


def _pick_field(fields: Mapping[str, str], key: str | None, fallback: str | None) -> str | None:
    if key:
        value = fields.get(key)
        if value:
            return value.strip() or None
    return fallback.strip() if isinstance(fallback, str) and fallback.strip() else None


def _normalize_symbol(value: str | None) -> str | None:
    if not value:
        return None
    normalized = value.strip().upper()
    return normalized or None
