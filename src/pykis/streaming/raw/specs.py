from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from pykis.streaming.raw.base import StreamingRawModel


class FieldType(str, Enum):
    DECIMAL = "decimal"
    STR = "str"
    INT = "int"
    DATETIME = "datetime"


class FieldSource(str, Enum):
    DOC_TYPE = "doc_type"
    RULE = "rule"
    HEURISTIC = "heuristic"
    INFERRED = "inferred"


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
class StreamingSpec:
    tr_id: str
    endpoint_uuid: str
    market: str
    timezone_hint: str
    model: type[StreamingRawModel]
    field_order: tuple[str, ...]
    field_aliases: Mapping[int, str]
    field_types: Mapping[str, FieldType]
    field_sources: Mapping[str, FieldSource]
    datetime_rules: Mapping[str, DateTimeRule]
    decimal_rules: Mapping[str, DecimalRule]
    requires_business_date: bool


SpecRegistry = Mapping[str, StreamingSpec]
