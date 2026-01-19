from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class DateTimeRule:
    kind: str
    format: str
    timezone: str
    date_field: str | None = None
    year_policy: str | None = None


@dataclass(frozen=True, slots=True)
class DecimalRule:
    scale: str
    zdiv_field: str


@dataclass(frozen=True, slots=True)
class FieldSpec:
    name: str
    field_type: str
    source: str
    datetime_rule: DateTimeRule | None = None
    decimal_rule: DecimalRule | None = None


@dataclass(frozen=True, slots=True)
class TrSpec:
    tr_id: str
    endpoint_uuid: str
    market: str
    timezone: str
    field_order: tuple[str, ...]
    field_order_normalized: tuple[str, ...] | None
    field_aliases: Mapping[int, str]
    requires_business_date: bool
    field_specs: Mapping[str, FieldSpec]


@dataclass(frozen=True, slots=True)
class StreamingSpecRoot:
    version: int
    source_inventory: str
    domestic_count: int
    overseas_count: int
    tr_specs: Mapping[str, TrSpec]
