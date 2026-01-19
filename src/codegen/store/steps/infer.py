from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from dataclasses import field as dataclass_field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Iterable

from pydantic import BaseModel, ConfigDict

from codegen.core.enums import parse_enum_entries
from codegen.store.models import MasterCatalog, MasterField, MasterStructSpec

_INT_RE = re.compile(r"^-?\d+$")
_DECIMAL_RE = re.compile(r"^-?\d+\.\d+$")
_BOOL_VALUES = {"Y", "N", "YES", "NO", "TRUE", "FALSE", "1", "0"}
_DATE_TOKENS = ("일자", "날짜", "기준일", "date", "ymd", "_dt")
_TIME_TOKENS = ("시각", "시간", "hhmm", "hhmmss", "time", "_tm", "hour")
_DATETIME_TOKENS = ("일시", "datetime", "timestamp", "_dttm")
_CODE_TOKENS = ("코드", "code", "iscd", "isin", "symbol", "symb", "sym", "id", "번호", "종목", "구분값")
_CODE_BOUNDARY_TOKENS = ("id", "sym")
_CODE_BOUNDARY_RE = re.compile(
    r"(?:^|[^0-9a-z])(" + "|".join(re.escape(token) for token in _CODE_BOUNDARY_TOKENS) + r")(?:$|[^0-9a-z])"
)
_DECIMAL_HINTS = (
    "가격",
    "주가",
    "현재가",
    "시가",
    "고가",
    "저가",
    "지수",
    "금액",
    "대금",
    "rate",
    "ratio",
    "percent",
    "pct",
    "amount",
    "price",
    "단일가",
    "비율",
    "율",
    "ctrt",
)
_INT_HINTS = (
    "수량",
    "거래량",
    "건수",
    "횟수",
    "volume",
    "count",
    "digit",
    "진법",
    "표시진법",
    "자리",
    "자릿수",
    "disp",
)
_DECIMAL_BLOCK_TOKENS = (
    "지수명",
    "index name",
    "자산명",
    "참조자산",
    "관련선물",
    "관련 선물",
    "종목코드",
    "ticker",
)
_DISABLED_TOKENS = ("사용안함", "사용 안함", "미사용", "사용하지 않음", "deprecated", "obsolete")

if TYPE_CHECKING:
    from pykis.store.parser.spec import RecordSpec


@dataclass(frozen=True, slots=True)
class InferConfig:
    max_enum_values: int = 64
    numeric_threshold: float = 0.95
    numeric_hint_threshold: float = 0.6
    date_threshold: float = 0.95
    time_threshold: float = 0.95
    datetime_threshold: float = 0.95
    numeric_sample_size: int = 5000
    conflict_examples: int = 5


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
    distinct: Counter[str] = dataclass_field(default_factory=Counter)
    distinct_overflow: bool = False
    has_alpha: bool = False
    has_leading_zero: bool = False
    numeric_samples: list[str] = dataclass_field(default_factory=list)

    def observe(self, raw: str, config: InferConfig) -> None:
        self.total += 1
        value = raw.strip()
        if not value or value in {".", "-", ","}:
            self.empty += 1
            return
        self.non_empty += 1
        if len(self.numeric_samples) < config.numeric_sample_size:
            self.numeric_samples.append(value)

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
    enum: list[str] | None = None
    enum_desc: dict[str, str] | None = None
    stats: FieldStatsSummary


@dataclass(frozen=True, slots=True)
class NumericStats:
    sample_size: int
    numeric_count: int
    numeric_ratio: float
    decimal_count: int
    decimal_ratio: float


@dataclass(frozen=True, slots=True)
class NumericConflict:
    struct_name: str
    field_name: str
    heuristic_kind: str
    data_kind: str
    inferred_kind: str
    numeric_ratio: float
    decimal_ratio: float
    sample_size: int
    has_alpha: bool
    has_leading_zero: bool
    description: str | None
    examples: list[str]


@dataclass(frozen=True, slots=True)
class NumericWarning:
    struct_name: str
    field_name: str
    heuristic_kind: str | None
    inferred_kind: str
    numeric_ratio: float
    decimal_ratio: float
    sample_size: int
    has_alpha: bool
    has_leading_zero: bool
    description: str | None
    examples: list[str]
    reasons: list[str]
    expected: bool


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
) -> tuple[CatalogInference, list[NumericConflict], list[NumericWarning]]:
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
    conflicts: list[NumericConflict] = []
    warnings: list[NumericWarning] = []
    for struct in catalog.structs:
        fields = {}
        for field in struct.fields:
            stats = stats_map[struct.name][field.name]
            fields[field.name] = _finalize_field(
                field,
                stats,
                config,
                struct_name=struct.name,
                conflicts=conflicts,
                warnings=warnings,
            )
        inference[struct.name] = StructInference(
            name=struct.name,
            sources=sorted(struct_sources.get(struct.name, [])),
            fields=fields,
        )

    return (
        CatalogInference(
            version="1",
            generated_at=datetime.now(timezone.utc).isoformat(),
            structs=inference,
        ),
        conflicts,
        warnings,
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


def write_numeric_conflicts(path: Path, conflicts: list[NumericConflict]) -> None:
    if not conflicts:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(conflict) for conflict in conflicts]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_numeric_warnings(path: Path, warnings: list[NumericWarning]) -> None:
    if not warnings:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(warning) for warning in warnings]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _infer_from_file(
    struct: MasterStructSpec,
    path: Path,
    field_stats: dict[str, FieldStats],
    config: InferConfig,
) -> None:
    from pykis.store.parser.models import RawSource
    from pykis.store.parser.reader import RecordReader

    record_spec = _build_record_spec(struct)
    raw_source = RawSource(source_id=struct.name, kind=struct.name, path=path, spec=record_spec)
    reader = RecordReader(raw_source)
    with path.open("rb") as handle:
        for record in reader.iter_records(handle):
            for name, value in record.fields.items():
                field_stats[name].observe(value, config)


def _build_record_spec(struct: MasterStructSpec) -> RecordSpec:
    from pykis.store.parser.spec import RecordSpec

    names = [field.name for field in struct.fields]
    lengths = [field.length for field in struct.fields]
    total_length = struct.record_length or sum(lengths)
    return RecordSpec.from_lengths(names, lengths, record_length=total_length)


def _finalize_field(
    field: MasterField,
    stats: FieldStats,
    config: InferConfig,
    *,
    struct_name: str | None = None,
    conflicts: list[NumericConflict] | None = None,
    warnings: list[NumericWarning] | None = None,
) -> FieldInference:
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

    if _has_disabled_hint(text):
        return FieldInference(
            name=field.name,
            kind="str",
            nullable=nullable,
            enum=None,
            enum_desc=None,
            stats=_stats_summary(stats),
        )

    numeric_stats = _numeric_stats(stats.numeric_samples, stats)
    heuristic_kind = _heuristic_numeric_kind(text)
    data_kind = _data_numeric_kind(numeric_stats, stats, config, heuristic_kind=heuristic_kind)
    inferred_kind = _pick_numeric_kind(data_kind, heuristic_kind, numeric_stats, stats, config)
    if inferred_kind:
        if warnings is not None and struct_name is not None:
            warnings.extend(
                _numeric_warnings(
                    struct_name,
                    field,
                    stats,
                    numeric_stats,
                    heuristic_kind,
                    inferred_kind,
                    config,
                )
            )
        if conflicts is not None and struct_name is not None:
            conflict = _numeric_conflict(
                struct_name,
                field,
                stats,
                numeric_stats,
                data_kind,
                heuristic_kind,
                inferred_kind,
                config,
            )
            if conflict is not None:
                conflicts.append(conflict)
        return FieldInference(
            name=field.name,
            kind=inferred_kind,
            nullable=nullable,
            enum=None,
            enum_desc=None,
            stats=_stats_summary(stats),
        )

    if warnings is not None and struct_name is not None:
        warnings.extend(
            _numeric_warnings(
                struct_name,
                field,
                stats,
                numeric_stats,
                heuristic_kind,
                "str",
                config,
            )
        )
    if conflicts is not None and struct_name is not None:
        conflict = _numeric_conflict(
            struct_name,
            field,
            stats,
            numeric_stats,
            data_kind,
            heuristic_kind,
            "str",
            config,
        )
        if conflict is not None:
            conflicts.append(conflict)

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
    if _CODE_BOUNDARY_RE.search(text):
        return True
    return any(token in text for token in _CODE_TOKENS if token not in _CODE_BOUNDARY_TOKENS)


def _has_date_hint(text: str) -> bool:
    return any(token in text for token in _DATE_TOKENS)


def _has_decimal_hint(text: str) -> bool:
    if any(token in text for token in _DECIMAL_BLOCK_TOKENS):
        return False
    return any(token in text for token in _DECIMAL_HINTS)


def _has_int_hint(text: str) -> bool:
    return any(token in text for token in _INT_HINTS)


def _has_bool_hint(text: str) -> bool:
    tokens = ("y/n", "_yn", "여부", "flag", "yn")
    return any(token in text for token in tokens)


def _has_disabled_hint(text: str) -> bool:
    return any(token in text for token in _DISABLED_TOKENS)


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


def _normalize_numeric_text(value: str) -> str:
    text = value.strip()
    if not text:
        return text
    text = text.replace(",", "")
    if text.startswith("+"):
        text = text[1:]
    return text


def _numeric_stats(samples: list[str], field_stats: FieldStats) -> NumericStats:
    normalized: list[str] = []
    for value in samples:
        text = value.strip()
        if not text or text in {".", "-", ","}:
            continue
        normalized.append(_normalize_numeric_text(text))

    sample_size = len(normalized)
    if sample_size == 0:
        return NumericStats(sample_size=0, numeric_count=0, numeric_ratio=0.0, decimal_count=0, decimal_ratio=0.0)

    import pandas as pd

    series = pd.Series(normalized, dtype="string")
    numeric = pd.to_numeric(series, errors="coerce")
    numeric_mask = numeric.notna()
    numeric_count = int(numeric_mask.sum())
    numeric_ratio = 0.0
    if field_stats.non_empty:
        numeric_ratio = (field_stats.int_count + field_stats.decimal_count) / field_stats.non_empty
    decimal_markers = series[numeric_mask].str.contains(r"[.eE]", regex=True)
    decimal_count = int(decimal_markers.sum()) if numeric_count else 0
    decimal_ratio = decimal_count / numeric_count if numeric_count else 0.0
    return NumericStats(
        sample_size=sample_size,
        numeric_count=numeric_count,
        numeric_ratio=numeric_ratio,
        decimal_count=decimal_count,
        decimal_ratio=decimal_ratio,
    )


def _heuristic_numeric_kind(text: str) -> str | None:
    if _is_code_like(text):
        return "non_numeric"
    if _has_disabled_hint(text):
        return None
    if _has_int_hint(text):
        return "int"
    if _has_decimal_hint(text):
        return "decimal"
    return None


def _data_numeric_kind(
    stats: NumericStats,
    field_stats: FieldStats,
    config: InferConfig,
    *,
    heuristic_kind: str | None,
) -> str | None:
    if heuristic_kind in {"decimal", "int", "non_numeric"}:
        return heuristic_kind
    if stats.sample_size == 0:
        return None
    if stats.numeric_ratio < config.numeric_threshold:
        return "non_numeric"
    if field_stats.has_alpha:
        return "non_numeric"
    if field_stats.decimal_count > 0 or stats.decimal_count > 0:
        return "decimal"
    return "int"


def _pick_numeric_kind(
    data_kind: str | None,
    heuristic_kind: str | None,
    stats: NumericStats,
    field_stats: FieldStats,
    config: InferConfig,
) -> str | None:
    if heuristic_kind == "non_numeric":
        return None
    if heuristic_kind == "decimal":
        if stats.numeric_ratio >= config.numeric_hint_threshold and not field_stats.has_alpha:
            return "decimal"
        return None
    if heuristic_kind == "int":
        if field_stats.decimal_count > 0 or stats.decimal_count > 0:
            if stats.numeric_ratio >= config.numeric_hint_threshold and not field_stats.has_alpha:
                return "decimal"
            return None
        if stats.numeric_ratio >= config.numeric_hint_threshold and not field_stats.has_alpha:
            return "int"
        return None
    if data_kind == "decimal":
        if stats.numeric_ratio >= config.numeric_threshold and not field_stats.has_alpha:
            return "decimal"
        return None
    if data_kind == "int":
        if stats.numeric_ratio >= config.numeric_threshold and not field_stats.has_alpha:
            return "int"
        return None
    if data_kind == "non_numeric":
        return None
    return None


def _numeric_warnings(
    struct_name: str,
    field: MasterField,
    stats: FieldStats,
    numeric_stats: NumericStats,
    heuristic_kind: str | None,
    inferred_kind: str,
    config: InferConfig,
) -> list[NumericWarning]:
    if heuristic_kind is None:
        return []
    reasons: list[str] = []
    numeric_ratio = numeric_stats.numeric_ratio
    if heuristic_kind in {"decimal", "int"}:
        if stats.has_alpha:
            reasons.append("numeric_hint_has_alpha")
        if numeric_ratio < config.numeric_hint_threshold:
            reasons.append("numeric_hint_low_ratio")
        if heuristic_kind == "int" and (stats.decimal_count > 0 or numeric_stats.decimal_count > 0):
            reasons.append("int_hint_has_decimal_values")
    if heuristic_kind == "non_numeric":
        if numeric_ratio >= config.numeric_threshold and not stats.has_alpha:
            reasons.append("code_like_numeric_data")
    if heuristic_kind in {"decimal", "int"} and inferred_kind != heuristic_kind:
        reasons.append("numeric_hint_overridden")
    if not reasons:
        return []
    examples = list(stats.distinct.keys())[: config.conflict_examples]
    expected = all(reason == "code_like_numeric_data" for reason in reasons)
    return [
        NumericWarning(
            struct_name=struct_name,
            field_name=field.name,
            heuristic_kind=heuristic_kind,
            inferred_kind=inferred_kind,
            numeric_ratio=round(numeric_ratio, 4),
            decimal_ratio=round(numeric_stats.decimal_ratio, 4),
            sample_size=numeric_stats.sample_size,
            has_alpha=stats.has_alpha,
            has_leading_zero=stats.has_leading_zero,
            description=field.description or None,
            examples=examples,
            reasons=reasons,
            expected=expected,
        )
    ]


def _numeric_conflict(
    struct_name: str,
    field: MasterField,
    stats: FieldStats,
    numeric_stats: NumericStats,
    data_kind: str | None,
    heuristic_kind: str | None,
    inferred_kind: str,
    config: InferConfig,
) -> NumericConflict | None:
    if not data_kind or heuristic_kind not in {"decimal", "int", "non_numeric"}:
        return None
    if data_kind == heuristic_kind:
        return None
    examples = list(stats.distinct.keys())[: config.conflict_examples]
    return NumericConflict(
        struct_name=struct_name,
        field_name=field.name,
        heuristic_kind=heuristic_kind,
        data_kind=data_kind,
        inferred_kind=inferred_kind,
        numeric_ratio=round(numeric_stats.numeric_ratio, 4),
        decimal_ratio=round(numeric_stats.decimal_ratio, 4),
        sample_size=numeric_stats.sample_size,
        has_alpha=stats.has_alpha,
        has_leading_zero=stats.has_leading_zero,
        description=field.description or None,
        examples=examples,
    )


__all__ = [
    "CatalogInference",
    "FieldInference",
    "InferConfig",
    "NumericConflict",
    "NumericWarning",
    "StructInference",
    "infer_catalog_types",
    "infer_field_from_values",
    "write_inference",
    "write_numeric_conflicts",
    "write_numeric_warnings",
]
