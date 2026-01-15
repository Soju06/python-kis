from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from pydantic import BaseModel, ConfigDict

from codegen.core.enums import parse_enum_entries
from codegen.store.models import MasterCatalog, MasterField, MasterStructSpec
from pykis.store.raw.models import RawSource
from pykis.store.raw.reader import RecordReader
from pykis.store.raw.spec import RecordSpec

_INT_RE = re.compile(r"^-?\d+$")
_DECIMAL_RE = re.compile(r"^-?\d+\.\d+$")
_BOOL_VALUES = {"Y", "N", "YES", "NO", "TRUE", "FALSE", "1", "0"}
_DATE_TOKENS = ("일자", "날짜", "기준일", "date", "ymd", "_dt")
_TIME_TOKENS = ("시각", "시간", "hhmm", "hhmmss", "time", "_tm", "hour")
_DATETIME_TOKENS = ("일시", "datetime", "timestamp", "_dttm")
_CODE_TOKENS = ("코드", "code", "iscd", "isin", "symbol", "sym", "id", "번호", "종목")
_DECIMAL_HINTS = ("가격", "주가", "금액", "지수", "rate", "ratio", "percent", "pct", "amount", "price", "비율", "률")


@dataclass(frozen=True, slots=True)
class InferConfig:
    max_enum_values: int = 64
    numeric_threshold: float = 0.95
    date_threshold: float = 0.95
    time_threshold: float = 0.95
    datetime_threshold: float = 0.95


@dataclass(slots=True)
class FieldStats:
    total: int = 0
    empty: int = 0
    non_empty: int = 0
    int_count: int = 0
    decimal_count: int = 0
    date_count: int = 0
    time_count: int = 0
    datetime_count: int = 0
    bool_count: int = 0
    zero_date_count: int = 0
    zero_time_count: int = 0
    zero_datetime_count: int = 0
    distinct: Counter[str] = field(default_factory=Counter)
    distinct_overflow: bool = False
    has_alpha: bool = False
    has_leading_zero: bool = False

    def observe(self, raw: str, config: InferConfig) -> None:
        self.total += 1
        value = raw.strip()
        if not value or value in {".", "-", ","}:
            self.empty += 1
            return
        self.non_empty += 1

        if any(ch.isalpha() for ch in value):
            self.has_alpha = True

        if len(value) > 1 and value[0] == "0" and value.isdigit():
            self.has_leading_zero = True

        normalized = value.replace(",", "")
        if normalized:
            if _INT_RE.fullmatch(normalized):
                self.int_count += 1
            elif _DECIMAL_RE.fullmatch(normalized):
                self.decimal_count += 1

        upper = value.upper()
        if upper in _BOOL_VALUES:
            self.bool_count += 1

        if value in {"0", "00000000"}:
            self.zero_date_count += 1

        if value in {"0", "000000", "0000"}:
            self.zero_time_count += 1

        if value in {"0", "00000000000000"}:
            self.zero_datetime_count += 1

        if _is_date_candidate(value):
            self.date_count += 1

        if _is_time_candidate(value):
            self.time_count += 1

        if _is_datetime_candidate(value):
            self.datetime_count += 1

        if not self.distinct_overflow:
            if len(self.distinct) < config.max_enum_values:
                self.distinct[value] += 1
            elif value not in self.distinct:
                self.distinct_overflow = True


class FieldStatsSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    total: int
    empty: int
    non_empty: int
    int_count: int
    decimal_count: int
    date_count: int
    time_count: int
    datetime_count: int
    bool_count: int
    zero_date_count: int
    zero_time_count: int
    zero_datetime_count: int
    distinct: dict[str, int]
    distinct_overflow: bool
    has_alpha: bool
    has_leading_zero: bool


class FieldInference(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str
    kind: str
    nullable: bool
    enum: list[str] | None
    enum_desc: dict[str, str] | None
    stats: FieldStatsSummary


class StructInference(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str
    sources: list[str]
    fields: dict[str, FieldInference]


class CatalogInference(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    version: str
    generated_at: str
    structs: dict[str, StructInference]


def infer_catalog_types(
    catalog: MasterCatalog,
    data_paths: dict[str, Path],
    *,
    config: InferConfig | None = None,
) -> CatalogInference:
    config = config or InferConfig()
    struct_map = {struct.name: struct for struct in catalog.structs}
    struct_sources: dict[str, list[str]] = {}
    for source in catalog.sources:
        struct_sources.setdefault(source.struct_name, []).append(source.source_id)

    stats_map: dict[str, dict[str, FieldStats]] = {}
    for struct in catalog.structs:
        stats_map[struct.name] = {field.name: FieldStats() for field in struct.fields}

    for source in catalog.sources:
        struct = struct_map.get(source.struct_name)
        if struct is None:
            continue
        data_path = data_paths.get(source.source_id)
        if data_path is None:
            continue
        _infer_from_file(struct, data_path, stats_map[struct.name], config)

    inference: dict[str, StructInference] = {}
    for struct in catalog.structs:
        fields = {}
        for field in struct.fields:
            stats = stats_map[struct.name][field.name]
            fields[field.name] = _finalize_field(field, stats, config)
        inference[struct.name] = StructInference(
            name=struct.name,
            sources=sorted(struct_sources.get(struct.name, [])),
            fields=fields,
        )

    return CatalogInference(
        version="1",
        generated_at=datetime.now(timezone.utc).isoformat(),
        structs=inference,
    )


def infer_field_from_values(
    field: MasterField,
    values: Iterable[str],
    *,
    config: InferConfig | None = None,
) -> FieldInference:
    config = config or InferConfig()
    stats = FieldStats()
    for value in values:
        stats.observe(value, config)
    return _finalize_field(field, stats, config)


def write_inference(path: Path, inference: CatalogInference) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(inference.model_dump(exclude_none=True), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _infer_from_file(
    struct: MasterStructSpec,
    path: Path,
    field_stats: dict[str, FieldStats],
    config: InferConfig,
) -> None:
    record_spec = _build_record_spec(struct)
    raw_source = RawSource(source_id=struct.name, kind=struct.name, path=path, spec=record_spec)
    reader = RecordReader(raw_source)
    with path.open("rb") as handle:
        for record in reader.iter_records(handle):
            for name, value in record.fields.items():
                field_stats[name].observe(value, config)


def _build_record_spec(struct: MasterStructSpec) -> RecordSpec:
    names = [field.name for field in struct.fields]
    lengths = [field.length for field in struct.fields]
    total_length = struct.record_length or sum(lengths)
    return RecordSpec.from_lengths(names, lengths, record_length=total_length)


def _finalize_field(field: MasterField, stats: FieldStats, config: InferConfig) -> FieldInference:
    text = _text_flags(field)
    non_empty = stats.non_empty
    nullable = stats.empty > 0

    if non_empty == 0:
        return FieldInference(
            name=field.name,
            kind="str",
            nullable=True,
            enum=None,
            enum_desc=None,
            stats=_stats_summary(stats),
        )

    desc_entries = parse_enum_entries(field.description)
    if desc_entries:
        desc_enum = [entry.code for entry in desc_entries]
        enum_desc = {entry.code: entry.desc for entry in desc_entries if entry.desc}
        if set(desc_enum).issubset({"Y", "N"}):
            return FieldInference(
                name=field.name,
                kind="bool",
                nullable=nullable,
                enum=None,
                enum_desc=None,
                stats=_stats_summary(stats),
            )
        if len(desc_enum) <= config.max_enum_values:
            return FieldInference(
                name=field.name,
                kind="enum",
                nullable=nullable,
                enum=desc_enum,
                enum_desc=enum_desc or None,
                stats=_stats_summary(stats),
            )

    bool_hint = _has_bool_hint(text)
    if bool_hint:
        return FieldInference(
            name=field.name,
            kind="bool",
            nullable=nullable,
            enum=None,
            enum_desc=None,
            stats=_stats_summary(stats),
        )

    date_ratio = stats.date_count / non_empty
    datetime_ratio = stats.datetime_count / non_empty
    time_ratio = stats.time_count / non_empty

    if not _is_code_like(text):
        if datetime_ratio >= config.datetime_threshold and (_has_datetime_hint(text) or datetime_ratio == 1.0):
            dt_nullable = stats.empty > 0 or stats.zero_datetime_count > 0
            return FieldInference(
                name=field.name,
                kind="datetime",
                nullable=dt_nullable,
                enum=None,
                enum_desc=None,
                stats=_stats_summary(stats),
            )

        if time_ratio >= config.time_threshold and (_has_time_hint(text) or time_ratio == 1.0):
            time_nullable = stats.empty > 0 or stats.zero_time_count > 0
            return FieldInference(
                name=field.name,
                kind="time",
                nullable=time_nullable,
                enum=None,
                enum_desc=None,
                stats=_stats_summary(stats),
            )

        if date_ratio >= config.date_threshold and (_has_date_hint(text) or date_ratio == 1.0):
            date_nullable = stats.empty > 0 or stats.zero_date_count > 0
            return FieldInference(
                name=field.name,
                kind="date",
                nullable=date_nullable,
                enum=None,
                enum_desc=None,
                stats=_stats_summary(stats),
            )

    if _is_code_like(text):
        return FieldInference(
            name=field.name,
            kind="str",
            nullable=nullable,
            enum=None,
            enum_desc=None,
            stats=_stats_summary(stats),
        )

    numeric_ratio = (stats.int_count + stats.decimal_count) / non_empty
    if numeric_ratio >= config.numeric_threshold and not stats.has_alpha:
        if stats.decimal_count > 0 or _has_decimal_hint(text):
            return FieldInference(
                name=field.name,
                kind="decimal",
                nullable=nullable,
                enum=None,
                enum_desc=None,
                stats=_stats_summary(stats),
            )
        if not stats.has_leading_zero:
            return FieldInference(
                name=field.name,
                kind="int",
                nullable=nullable,
                enum=None,
                enum_desc=None,
                stats=_stats_summary(stats),
            )

    return FieldInference(
        name=field.name,
        kind="str",
        nullable=nullable,
        enum=None,
        enum_desc=None,
        stats=_stats_summary(stats),
    )


def _text_flags(field: MasterField) -> str:
    parts = [field.name, field.description or "", field.type_code or ""]
    return " ".join(parts).lower()


def _is_code_like(text: str) -> bool:
    return any(token in text for token in _CODE_TOKENS)


def _has_date_hint(text: str) -> bool:
    return any(token in text for token in _DATE_TOKENS)


def _has_decimal_hint(text: str) -> bool:
    return any(token in text for token in _DECIMAL_HINTS)


def _has_bool_hint(text: str) -> bool:
    tokens = ("y/n", "_yn", "여부", "flag", "yn")
    return any(token in text for token in tokens)


def _has_time_hint(text: str) -> bool:
    return "시간외" not in text and any(token in text for token in _TIME_TOKENS)


def _has_datetime_hint(text: str) -> bool:
    return any(token in text for token in _DATETIME_TOKENS)


def _is_time_candidate(value: str) -> bool:
    if value in {"0", "000000", "0000"}:
        return True
    if value.isdigit() and len(value) in (4, 6):
        return True
    if ":" in value:
        parts = value.split(":")
        return len(parts) in (2, 3) and all(part.isdigit() for part in parts)
    return False


def _is_datetime_candidate(value: str) -> bool:
    if value in {"0", "00000000000000"}:
        return True
    if value.isdigit() and len(value) == 14:
        return True
    return False


def _is_date_candidate(value: str) -> bool:
    if value in {"0", "00000000"}:
        return True
    if not (value.isdigit() and len(value) == 8):
        return False
    try:
        datetime.strptime(value, "%Y%m%d")
    except ValueError:
        return False
    return True


def _stats_summary(stats: FieldStats) -> FieldStatsSummary:
    return FieldStatsSummary(
        total=stats.total,
        empty=stats.empty,
        non_empty=stats.non_empty,
        int_count=stats.int_count,
        decimal_count=stats.decimal_count,
        date_count=stats.date_count,
        time_count=stats.time_count,
        datetime_count=stats.datetime_count,
        bool_count=stats.bool_count,
        zero_date_count=stats.zero_date_count,
        zero_time_count=stats.zero_time_count,
        zero_datetime_count=stats.zero_datetime_count,
        distinct=dict(stats.distinct),
        distinct_overflow=stats.distinct_overflow,
        has_alpha=stats.has_alpha,
        has_leading_zero=stats.has_leading_zero,
    )


__all__ = [
    "CatalogInference",
    "FieldInference",
    "InferConfig",
    "StructInference",
    "infer_catalog_types",
    "infer_field_from_values",
    "write_inference",
]
