"""Field-name pattern-based type inference for streaming specs.

Promotes financial fields from ``str`` to ``decimal`` and detects datetime
fields based on naming conventions observed across known-good KIS streaming
TR specs.
"""

from __future__ import annotations

import re
from dataclasses import replace
from pathlib import Path
from typing import Mapping

import yaml

from codegen.streaming.models import DateTimeRule, FieldSpec, StreamingSpecRoot, TrSpec

# ---------------------------------------------------------------------------
# Known-good TRs whose field types are already validated.
# Used for cross-reference fallback.
# ---------------------------------------------------------------------------
KNOWN_GOOD_TR_IDS: frozenset[str] = frozenset(
    {
        "H0STCNT0",
        "H0STASP0",
        "HDFSASP0",
        "HDFSASP1",
        "HDFSCNT0",
        "H0GSCNI0",
    }
)

# ---------------------------------------------------------------------------
# Patterns that MUST stay ``str`` (safety guard — checked first)
# ---------------------------------------------------------------------------
_STR_EXACT: frozenset[str] = frozenset(
    {
        "MKSC_SHRN_ISCD",
        "RSYM",
        "SYMB",
        "MTYP",
        "SIGN",
    }
)

_STR_SUFFIXES: tuple[str, ...] = (
    "_ISCD",
    "_CLS_CODE",
    "_CODE",
    "_SIGN",
    "_YN",
    "_DVSN",
    "_NAME",
    "_NO",
    "_GB",
    "_TP",
)

# ---------------------------------------------------------------------------
# Patterns that indicate ``decimal``
# ---------------------------------------------------------------------------
_DECIMAL_PREFIXES: tuple[str, ...] = (
    "ASKP",
    "BIDP",
    "PBID",
    "PASK",
    "VBID",
    "VASK",
    "DBID",
    "DASK",
)

_DECIMAL_SUFFIXES: tuple[str, ...] = (
    "_PRPR",
    "_PRC",
    "_OPRC",
    "_HGPR",
    "_LWPR",
    "_VRSS",
    "_CTRT",
    "_RATE",
    "_VOL",
    "_RSQN",
    "_PBMN",
    "_CSNU",
    "_SMTN",
    "_QTY",
    "_AMT",
    "_UNPR",
    "_NMIX",
    "_NAV",
    "_ICDC",
    "_VAL",
    "_VLTL",
    "_THPR",
    "_RLIM",
    "_CNT",
    "_CNQN",
    "_HVOL",
)

_DECIMAL_EXACT: frozenset[str] = frozenset(
    {
        "OPEN",
        "HIGH",
        "LOW",
        "LAST",
        "DIFF",
        "RATE",
        "PBID",
        "PASK",
        "EVOL",
        "TVOL",
        "TAMT",
        "CTTR",
        "NAV",
        "CFP",
        "PRIT",
        "DELTA",
        "GAMA",
        "VEGA",
        "THETA",
        "RHO",
        "GEAR",
        "LVRG_VAL",
        "BIVL",
        "ASVL",
        "STRN",
        "VBID",
        "VASK",
    }
)

_DECIMAL_CONTAINS: tuple[str, ...] = (
    "WGHN_AVRG",
    "ACML_VOL",
    "ACML_TR",
    "CNTG_VOL",
    "ANTC_CN",
)

_TRAILING_DIGITS = re.compile(r"_?\d+$")


# ---------------------------------------------------------------------------
# Override loading
# ---------------------------------------------------------------------------
def _load_overrides(
    path: Path | None,
) -> tuple[dict[str, str], dict[str, dict[str, str]]]:
    """Return ``(global_overrides, per_tr_overrides)`` from YAML."""
    if path is None or not path.exists():
        return {}, {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, Mapping):
        return {}, {}
    global_raw = data.get("global") or {}
    per_tr_raw = data.get("per_tr") or {}
    global_map: dict[str, str] = (
        {str(k): str(v) for k, v in global_raw.items()} if isinstance(global_raw, Mapping) else {}
    )
    per_tr_map: dict[str, dict[str, str]] = {}
    if isinstance(per_tr_raw, Mapping):
        for tr_id, fields in per_tr_raw.items():
            if isinstance(fields, Mapping):
                per_tr_map[str(tr_id)] = {str(k): str(v) for k, v in fields.items()}
    return global_map, per_tr_map


# ---------------------------------------------------------------------------
# Cross-reference sets from known-good TRs
# ---------------------------------------------------------------------------
def _build_decimal_crossref(spec: StreamingSpecRoot) -> frozenset[str]:
    """Collect uppercase field names that are ``decimal`` in known-good TRs."""
    names: set[str] = set()
    for tr_id in KNOWN_GOOD_TR_IDS:
        tr_spec = spec.tr_specs.get(tr_id)
        if tr_spec is None:
            continue
        for name, field_spec in tr_spec.field_specs.items():
            if field_spec.field_type == "decimal":
                names.add(name.upper())
    return frozenset(names)


def _build_datetime_crossref(
    spec: StreamingSpecRoot,
) -> dict[str, DateTimeRule]:
    """Collect uppercase field names → DateTimeRule from known-good TRs.

    When multiple TRs define the same field, the first encountered rule wins.
    """
    rules: dict[str, DateTimeRule] = {}
    for tr_id in sorted(KNOWN_GOOD_TR_IDS):
        tr_spec = spec.tr_specs.get(tr_id)
        if tr_spec is None:
            continue
        for name, field_spec in tr_spec.field_specs.items():
            upper = name.upper()
            if field_spec.field_type == "datetime" and field_spec.datetime_rule is not None:
                if upper not in rules:
                    rules[upper] = field_spec.datetime_rule
    return rules


# ---------------------------------------------------------------------------
# Single-field classification
# ---------------------------------------------------------------------------
def _strip_trailing_digits(name: str) -> str:
    return _TRAILING_DIGITS.sub("", name)


def _is_str_guard(name: str) -> bool:
    if name in _STR_EXACT:
        return True
    stripped = _strip_trailing_digits(name)
    return any(stripped.endswith(suffix) for suffix in _STR_SUFFIXES)


def _is_decimal_pattern(name: str) -> bool:
    if name in _DECIMAL_EXACT:
        return True
    stripped = _strip_trailing_digits(name)
    if stripped in _DECIMAL_EXACT:
        return True
    if any(stripped.startswith(prefix) for prefix in _DECIMAL_PREFIXES):
        return True
    if any(stripped.endswith(suffix) for suffix in _DECIMAL_SUFFIXES):
        return True
    return any(substr in name for substr in _DECIMAL_CONTAINS)


def _classify_field(
    name: str,
    field_spec: FieldSpec,
    global_overrides: dict[str, str],
    tr_overrides: dict[str, str],
    decimal_crossref: frozenset[str],
    datetime_crossref: dict[str, DateTimeRule],
) -> tuple[str, str, DateTimeRule | None]:
    """Return ``(new_type, reason, datetime_rule)`` for a single field.

    *reason* is one of: ``"skip_nonstr"``, ``"override"``,
    ``"str_guard"``, ``"pattern"``, ``"crossref"``,
    ``"datetime_crossref"``, ``"no_match"``.

    *datetime_rule* is non-None only when the field is promoted to datetime.
    """
    if field_spec.field_type != "str":
        return field_spec.field_type, "skip_nonstr", None

    # Override takes precedence over patterns (exact name, case-sensitive)
    if name in tr_overrides:
        return tr_overrides[name], "override", None
    if name in global_overrides:
        return global_overrides[name], "override", None

    # Normalize to uppercase for pattern matching (handles lowercase TRs like H0UPCNT0)
    upper = name.upper()

    # Safety: str-guard patterns keep the field as str
    if _is_str_guard(upper):
        return "str", "str_guard", None

    # Datetime cross-reference (before decimal to avoid misclassifying HOUR fields)
    dt_rule = datetime_crossref.get(upper)
    if dt_rule is not None:
        return "datetime", "datetime_crossref", dt_rule

    # Decimal patterns
    if _is_decimal_pattern(upper):
        return "decimal", "pattern", None

    # Decimal cross-reference from known-good TRs (case-insensitive)
    if upper in decimal_crossref:
        return "decimal", "crossref", None

    return "str", "no_match", None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def infer_field_types(
    spec: StreamingSpecRoot,
    overrides_path: Path | None = None,
) -> tuple[StreamingSpecRoot, dict[str, object]]:
    """Promote ``str`` fields to ``decimal`` where naming patterns match.

    Returns the updated spec and a JSON-serializable report dict.
    """
    global_overrides, per_tr_overrides = _load_overrides(overrides_path)
    decimal_crossref = _build_decimal_crossref(spec)
    datetime_crossref = _build_datetime_crossref(spec)

    total_fields = 0
    reclassified = 0
    reason_counts: dict[str, int] = {}
    tr_changes: dict[str, list[dict[str, str]]] = {}

    new_tr_specs: dict[str, TrSpec] = {}

    for tr_id, tr_spec in spec.tr_specs.items():
        tr_ovr = per_tr_overrides.get(tr_id, {})
        changed_fields: list[dict[str, str]] = []
        new_field_specs: dict[str, FieldSpec] = {}

        field_names = tr_spec.field_order_normalized or tr_spec.field_order

        for name in field_names:
            field_spec = tr_spec.field_specs.get(name)
            if field_spec is None:
                continue

            total_fields += 1
            new_type, reason, dt_rule = _classify_field(
                name, field_spec, global_overrides, tr_ovr, decimal_crossref, datetime_crossref
            )
            reason_counts[reason] = reason_counts.get(reason, 0) + 1

            if new_type != field_spec.field_type:
                reclassified += 1
                changed_fields.append(
                    {
                        "field": name,
                        "from": field_spec.field_type,
                        "to": new_type,
                        "reason": reason,
                    }
                )
                replacements: dict[str, object] = {
                    "field_type": new_type,
                    "source": "inferred",
                }
                if dt_rule is not None:
                    replacements["datetime_rule"] = dt_rule
                new_field_specs[name] = replace(field_spec, **replacements)
            else:
                new_field_specs[name] = field_spec

        # Propagate alias specs that weren't in field_order_normalized
        for name, field_spec in tr_spec.field_specs.items():
            if name not in new_field_specs:
                alias_new_type, _, alias_dt_rule = _classify_field(
                    name, field_spec, global_overrides, tr_ovr, decimal_crossref, datetime_crossref
                )
                if alias_new_type != field_spec.field_type:
                    alias_replacements: dict[str, object] = {
                        "field_type": alias_new_type,
                        "source": "inferred",
                    }
                    if alias_dt_rule is not None:
                        alias_replacements["datetime_rule"] = alias_dt_rule
                    new_field_specs[name] = replace(field_spec, **alias_replacements)
                else:
                    new_field_specs[name] = field_spec

        if changed_fields:
            tr_changes[tr_id] = changed_fields

        new_tr_specs[tr_id] = TrSpec(
            tr_id=tr_spec.tr_id,
            endpoint_uuid=tr_spec.endpoint_uuid,
            market=tr_spec.market,
            timezone=tr_spec.timezone,
            field_order=tr_spec.field_order,
            field_order_normalized=tr_spec.field_order_normalized,
            field_aliases=tr_spec.field_aliases,
            requires_business_date=tr_spec.requires_business_date,
            field_specs=new_field_specs,
        )

    report: dict[str, object] = {
        "total_fields": total_fields,
        "reclassified": reclassified,
        "reason_counts": reason_counts,
        "tr_changes": tr_changes,
        "decimal_crossref_size": len(decimal_crossref),
        "datetime_crossref_size": len(datetime_crossref),
        "known_good_trs": sorted(KNOWN_GOOD_TR_IDS),
    }

    new_spec = StreamingSpecRoot(
        version=spec.version,
        source_inventory=spec.source_inventory,
        domestic_count=spec.domestic_count,
        overseas_count=spec.overseas_count,
        tr_specs=new_tr_specs,
    )

    return new_spec, report
