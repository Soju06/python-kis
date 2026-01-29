from __future__ import annotations

import json
from pathlib import Path

from codegen.api.models import EndpointSpec
from codegen.api.validation_models import (
    ComparisonResult,
    DiscoveryHeuristics,
    DiscoverySummary,
    FieldDiff,
    ValidationEvidence,
    ValidationHint,
)
from codegen.core.types import JsonObject, JsonValue

SENTINEL_PATTERNS: dict[str, tuple[str | None, ...]] = {
    "empty_string": ("",),
    "zero_numeric": ("0", "0.0", "0.00"),
    "zero_date": ("00000000", "0000-00-00"),
    "zero_time": ("000000", "00:00:00", "888888"),
    "null_marker": (None, "null", "NULL"),
}

DISCOVERY_THRESHOLDS = DiscoveryHeuristics(min_sentinel_ratio=0.5, min_fields_differ=3)


def discover_validators(
    specs: list[EndpointSpec],
    augment_dir: Path,
) -> dict[str, ValidationHint]:
    hints: dict[str, ValidationHint] = {}
    for spec in specs:
        endpoint_dir = augment_dir / spec.id
        endpoint_dir.mkdir(parents=True, exist_ok=True)
        success = _load_json(endpoint_dir / "success.json")
        empty = _load_json(endpoint_dir / "empty.json")

        if not success or not empty:
            hint = ValidationHint.now(spec.id, "no_candidates")
            (endpoint_dir / "validation_hints.json").write_text(
                json.dumps(hint.model_dump(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            hints[spec.id] = hint
            continue

        comparison = compare_responses(success, empty)
        if comparison.total_fields == 0:
            hint = ValidationHint.now(spec.id, "no_candidates")
            (endpoint_dir / "validation_hints.json").write_text(
                json.dumps(hint.model_dump(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            hints[spec.id] = hint
            continue

        if comparison.sentinel_ratio < DISCOVERY_THRESHOLDS.min_sentinel_ratio:
            hint = ValidationHint.now(spec.id, "no_candidates")
            (endpoint_dir / "validation_hints.json").write_text(
                json.dumps(hint.model_dump(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            hints[spec.id] = hint
            continue

        candidate_fields = [diff.field for diff in comparison.diffs]
        if len(candidate_fields) < DISCOVERY_THRESHOLDS.min_fields_differ:
            hint = ValidationHint.now(spec.id, "too_few_fields")
            (endpoint_dir / "validation_hints.json").write_text(
                json.dumps(hint.model_dump(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            hints[spec.id] = hint
            continue

        success_row, empty_row, output_key = _select_rows(success, empty)
        evidence = ValidationEvidence(
            success_sample=_pick_fields(success_row, candidate_fields),
            empty_sample=_pick_fields(empty_row, candidate_fields),
        )
        hint = ValidationHint(
            endpoint_id=spec.id,
            generated_at=ValidationHint.now(spec.id, "pending_review").generated_at,
            status="pending_review",
            discovery=DiscoverySummary(
                heuristics_used=DISCOVERY_THRESHOLDS,
                results=comparison,
            ),
            candidate_fields=candidate_fields,
            evidence=evidence,
            suggested_yaml=_suggest_yaml(output_key, candidate_fields),
        )
        (endpoint_dir / "validation_hints.json").write_text(
            json.dumps(hint.model_dump(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        hints[spec.id] = hint

    return hints


def compare_responses(success: JsonObject, empty: JsonObject) -> ComparisonResult:
    diffs: list[FieldDiff] = []
    total_fields = 0
    for output_key in ("output", "output1", "output2"):
        success_rows = _as_rows(success.get(output_key))
        empty_rows = _as_rows(empty.get(output_key))
        if not success_rows or not empty_rows:
            continue

        success_row = success_rows[0]
        empty_row = empty_rows[0]
        total_fields = max(total_fields, len(empty_row))

        for field, empty_val in empty_row.items():
            success_val = success_row.get(field)
            if is_sentinel(empty_val) and not is_sentinel(success_val):
                diffs.append(
                    FieldDiff(
                        field=field,
                        success_value=_stringify(success_val),
                        empty_value=_stringify(empty_val),
                        sentinel_type=classify_sentinel(empty_val),
                    )
                )

    sentinel_ratio = (len(diffs) / total_fields) if total_fields else 0.0
    return ComparisonResult(diffs=diffs, sentinel_ratio=sentinel_ratio, total_fields=total_fields)


def classify_sentinel(value: JsonValue) -> str:
    normalized = _normalize(value)
    for sentinel_type, patterns in SENTINEL_PATTERNS.items():
        if normalized in {_normalize(item) for item in patterns}:
            return sentinel_type
    return "unknown"


def is_sentinel(value: JsonValue) -> bool:
    normalized = _normalize(value)
    for patterns in SENTINEL_PATTERNS.values():
        if normalized in {_normalize(item) for item in patterns}:
            return True
    return False


def _normalize(value: JsonValue) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip()
    return str(value)


def _stringify(value: JsonValue) -> str | None:
    if value is None:
        return None
    return str(value)


def _as_rows(value: JsonValue | None) -> list[JsonObject]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [value]
    return []


def _pick_fields(row: JsonObject, fields: list[str]) -> JsonObject:
    return {field: row.get(field) for field in fields if field in row}


def _select_rows(success: JsonObject, empty: JsonObject) -> tuple[JsonObject, JsonObject, str]:
    for output_key in ("output", "output1", "output2"):
        success_rows = _as_rows(success.get(output_key))
        empty_rows = _as_rows(empty.get(output_key))
        if success_rows and empty_rows:
            return success_rows[0], empty_rows[0], output_key
    return {}, {}, "output"


def _suggest_yaml(output_key: str, fields: list[str]) -> str:
    field_lines = "\n".join([f"      - {field}" for field in fields])
    return (
        "validator:\n"
        "  rules:\n"
        f"    - id: {output_key}_sentinel_check\n"
        "      type: all_fields_sentinel\n"
        f"      output: {output_key}\n"
        "      scope: first_row\n"
        "      fields:\n"
        f"{field_lines}\n"
        '      sentinel_values: ["", "0", "0.0"]\n'
        "      error:\n"
        "        code: KIS_RESPONSE_UNAVAILABLE\n"
        '        message: "Response unavailable"\n'
        '        user_message: "데이터 제공 시간에 다시 시도하세요."\n'
        "        exception: KisResponseUnavailableError\n"
    )


def _load_json(path: Path) -> JsonObject | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


__all__ = ["compare_responses", "discover_validators"]
