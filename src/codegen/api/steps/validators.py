from __future__ import annotations

import json
from pathlib import Path

from codegen.api.models import EndpointSpec
from codegen.api.validation_models import (
    ComparisonResult,
    DiscoveryHeuristics,
    DiscoverySummary,
    FieldDiff,
    InvalidProbeEvidence,
    InvalidProbeHint,
    MessageSignal,
    MissingComparisonResult,
    MissingFieldDiff,
    OutputSnapshot,
    ResponseMeta,
    ValidationCandidate,
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
    "nan_marker": ("nan", "-nan", "NaN", "-NaN"),
}

DISCOVERY_THRESHOLDS = DiscoveryHeuristics(min_sentinel_ratio=0.5, min_fields_differ=3)
INVALID_THRESHOLDS = DiscoveryHeuristics(min_sentinel_ratio=0.4, min_fields_differ=2)
INVALID_MISSING_RATIO = 0.4
PROBE_SENTINEL_MIN_RATIO = 0.8
PROBE_SENTINEL_MIN_FIELDS = 1
PROBE_SENTINEL_MIN_ROWS = 10

MESSAGE_SUCCESS_CODES = {"MCA00000"}
MESSAGE_EMPTY_CODES = {"APBN0024"}
MESSAGE_EMPTY_SNIPPETS = (
    "조회된 데이터가 없습니다",
    "조회된 자료가 없습니다",
    "조회할 자료가 없습니다",
    "조회할 내용이 없습니다",
    "조회된 정보가 없습니다",
    "조회할 정보가 없습니다",
)
MESSAGE_ERROR_SNIPPETS = (
    "오류",
    "실패",
    "불가",
    "불가능",
    "유효하지",
    "잘못",
    "미등록",
    "존재하지",
    "권한",
    "거부",
    "초과",
    "만료",
    "필수",
    "파라미터",
    "입력값",
    "형식",
    "invalid",
    "error",
    "fail",
    "denied",
    "unauthorized",
    "forbidden",
)


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
        error_probe = _load_json(endpoint_dir / "error.json")

        hint = _discover_empty_candidates(spec.id, success, empty)
        invalid_hint = _discover_invalid_candidates(spec, success, error_probe)
        if invalid_hint is not None:
            hint = hint.model_copy(update={"invalid_probe": invalid_hint})

        (endpoint_dir / "validation_hints.json").write_text(
            json.dumps(hint.model_dump(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        hints[spec.id] = hint

    return hints


def build_validation_candidates(
    specs: list[EndpointSpec],
    augment_dir: Path,
    hints: dict[str, ValidationHint],
) -> list[ValidationCandidate]:
    candidates: list[ValidationCandidate] = []
    for spec in specs:
        hint = hints.get(spec.id)
        if hint is None or hint.invalid_probe is None:
            continue
        invalid = hint.invalid_probe
        if not invalid.rule_type:
            continue

        output_key = invalid.output_key or _primary_output_key(spec)
        success = _load_json(augment_dir / spec.id / "success.json")
        probe = _load_json(augment_dir / spec.id / "error.json")
        output_state = _build_output_snapshot(probe, output_key)
        success_meta = _extract_meta(success)
        probe_meta = _extract_meta(probe)
        evidence = _build_candidate_evidence(success, probe, output_key, invalid.candidate_fields)
        reason = _candidate_reason(invalid, invalid.rule_type)
        invalid_template = _load_invalid_template(augment_dir / spec.id / "request_resolution_invalid_params.json")

        candidates.append(
            ValidationCandidate(
                endpoint_id=spec.id,
                rule_type=invalid.rule_type,
                output=output_key,
                status=invalid.status,
                rt_cd=invalid.rt_cd,
                msg_cd=invalid.msg_cd,
                msg1=invalid.msg1,
                candidate_fields=list(invalid.candidate_fields or []),
                reason=reason,
                output_state=output_state,
                success_meta=success_meta,
                probe_meta=probe_meta,
                evidence=evidence,
                invalid_template=invalid_template,
            )
        )

    return candidates


def _discover_empty_candidates(
    endpoint_id: str,
    success: JsonObject | None,
    empty: JsonObject | None,
) -> ValidationHint:
    if not success or not empty:
        return ValidationHint.now(endpoint_id, "no_candidates")

    comparison = compare_responses(success, empty)
    if comparison.total_fields == 0:
        return ValidationHint.now(endpoint_id, "no_candidates")

    if comparison.sentinel_ratio < DISCOVERY_THRESHOLDS.min_sentinel_ratio:
        return ValidationHint.now(endpoint_id, "no_candidates")

    candidate_fields = [diff.field for diff in comparison.diffs]
    if len(candidate_fields) < DISCOVERY_THRESHOLDS.min_fields_differ:
        return ValidationHint.now(endpoint_id, "too_few_fields")

    success_row, empty_row, output_key = _select_rows(success, empty)
    evidence = ValidationEvidence(
        success_sample=_pick_fields(success_row, candidate_fields),
        empty_sample=_pick_fields(empty_row, candidate_fields),
    )
    return ValidationHint(
        endpoint_id=endpoint_id,
        generated_at=ValidationHint.now(endpoint_id, "pending_review").generated_at,
        status="pending_review",
        discovery=DiscoverySummary(
            heuristics_used=DISCOVERY_THRESHOLDS,
            results=comparison,
        ),
        candidate_fields=candidate_fields,
        evidence=evidence,
    )


def _discover_invalid_candidates(
    spec: EndpointSpec,
    success: JsonObject | None,
    probe: JsonObject | None,
) -> InvalidProbeHint | None:
    if probe is None:
        return InvalidProbeHint(status="missing_probe")

    rt_cd = str(probe.get("rt_cd") or "")
    msg_cd = str(probe.get("msg_cd") or "") or None
    msg1 = str(probe.get("msg1") or "") or None
    rt_ok = rt_cd in {"0", "OK"}
    message_signal = _classify_message(spec, msg_cd, msg1)

    output_key = _primary_output_key(spec)
    output_missing, output_empty = _output_state(probe, output_key)
    if not rt_ok:
        return InvalidProbeHint(
            status="rt_cd_error",
            rt_cd=rt_cd,
            msg_cd=msg_cd,
            msg1=msg1,
            message_signal=message_signal,
            output_key=output_key,
            output_missing=output_missing,
            output_empty=output_empty,
        )

    if success is None:
        return InvalidProbeHint(
            status="missing_success",
            rt_cd=rt_cd,
            msg_cd=msg_cd,
            msg1=msg1,
            message_signal=message_signal,
            output_key=output_key,
            output_missing=output_missing,
            output_empty=output_empty,
        )

    if output_missing or output_empty:
        return InvalidProbeHint(
            status="pending_review",
            rt_cd=rt_cd,
            msg_cd=msg_cd,
            msg1=msg1,
            message_signal=message_signal,
            rule_type="output_required",
            output_key=output_key,
            output_missing=output_missing,
            output_empty=output_empty,
            candidate_fields=[output_key],
            evidence=InvalidProbeEvidence(
                success_sample=_pick_fields(_first_row(success, output_key), []),
                probe_sample=_pick_fields(_first_row(probe, output_key), []),
            ),
        )

    probe_sentinel = _probe_sentinel_ratio(probe, output_key)
    if probe_sentinel is not None and probe_sentinel.diffs:
        candidate_fields = [diff.field for diff in probe_sentinel.diffs]
        rule_type = "all_fields_sentinel" if probe_sentinel.sentinel_ratio >= 0.9 else "any_field_sentinel"
        success_row = _first_row(success, output_key) if success else {}
        probe_row = _first_row(probe, output_key)
        return InvalidProbeHint(
            status="pending_review",
            rt_cd=rt_cd,
            msg_cd=msg_cd,
            msg1=msg1,
            message_signal=message_signal,
            rule_type=rule_type,
            output_key=output_key,
            output_missing=output_missing,
            output_empty=output_empty,
            sentinel=probe_sentinel,
            candidate_fields=candidate_fields,
            evidence=InvalidProbeEvidence(
                success_sample=_pick_fields(success_row, candidate_fields),
                probe_sample=_pick_fields(probe_row, candidate_fields),
            ),
        )

    sentinel = compare_responses(success, probe)
    missing = compare_missing_fields(success, probe)
    candidate_fields: list[str] = []
    rule_type = None

    if sentinel.total_fields and sentinel.sentinel_ratio >= INVALID_THRESHOLDS.min_sentinel_ratio:
        candidate_fields = [diff.field for diff in sentinel.diffs]
        if len(candidate_fields) >= INVALID_THRESHOLDS.min_fields_differ:
            rule_type = "all_fields_sentinel" if sentinel.sentinel_ratio >= 0.8 else "any_field_sentinel"
    if not rule_type and missing.total_fields and missing.missing_ratio >= INVALID_MISSING_RATIO:
        candidate_fields = [diff.field for diff in missing.diffs]
        if len(candidate_fields) >= INVALID_THRESHOLDS.min_fields_differ:
            rule_type = "all_fields_missing" if missing.missing_ratio >= 0.8 else "any_field_missing"

    if not rule_type:
        return InvalidProbeHint(
            status="message_error" if message_signal and message_signal.error else "no_candidates",
            rt_cd=rt_cd,
            msg_cd=msg_cd,
            msg1=msg1,
            message_signal=message_signal,
            output_key=output_key,
            output_missing=output_missing,
            output_empty=output_empty,
            sentinel=sentinel,
            missing=missing,
        )

    success_row, probe_row, _ = _select_rows(success, probe)
    return InvalidProbeHint(
        status="pending_review",
        rt_cd=rt_cd,
        msg_cd=msg_cd,
        msg1=msg1,
        message_signal=message_signal,
        rule_type=rule_type,
        output_key=output_key,
        output_missing=output_missing,
        output_empty=output_empty,
        sentinel=sentinel,
        missing=missing,
        candidate_fields=candidate_fields,
        evidence=InvalidProbeEvidence(
            success_sample=_pick_fields(success_row, candidate_fields),
            probe_sample=_pick_fields(probe_row, candidate_fields),
        ),
    )


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


def _probe_sentinel_ratio(payload: JsonObject, output_key: str) -> ComparisonResult | None:
    rows = _as_rows(payload.get(output_key))
    if not rows and output_key != "output":
        rows = _as_rows(payload.get("output"))
    if len(rows) < PROBE_SENTINEL_MIN_ROWS:
        return None

    field_names = list(rows[0].keys())
    if not field_names:
        return None

    diffs: list[FieldDiff] = []
    max_ratio = 0.0
    for field in field_names:
        sentinel_values = []
        for row in rows:
            value = row.get(field)
            if is_sentinel(value):
                sentinel_values.append(value)
        ratio = len(sentinel_values) / len(rows) if rows else 0.0
        if ratio >= PROBE_SENTINEL_MIN_RATIO:
            sentinel_value = sentinel_values[0] if sentinel_values else None
            diffs.append(
                FieldDiff(
                    field=field,
                    success_value=_stringify(rows[0].get(field)),
                    empty_value=_stringify(sentinel_value),
                    sentinel_type=classify_sentinel(sentinel_value),
                )
            )
            max_ratio = max(max_ratio, ratio)

    if len(diffs) < PROBE_SENTINEL_MIN_FIELDS:
        return None

    return ComparisonResult(diffs=diffs, sentinel_ratio=max_ratio, total_fields=len(field_names))


def _extract_meta(payload: JsonObject | None) -> ResponseMeta | None:
    if not payload:
        return None
    return ResponseMeta(
        rt_cd=str(payload.get("rt_cd") or "") or None,
        msg_cd=str(payload.get("msg_cd") or "") or None,
        msg1=str(payload.get("msg1") or "") or None,
    )


def _build_output_snapshot(payload: JsonObject | None, output_key: str) -> OutputSnapshot | None:
    if not payload:
        return None
    container = None
    present = False
    if output_key in payload:
        container = payload.get(output_key)
        present = True
    elif output_key != "output" and "output" in payload:
        container = payload.get("output")
        present = True

    if not present:
        return OutputSnapshot(output=output_key, present=False, empty=False, kind="missing")

    if isinstance(container, list):
        return OutputSnapshot(
            output=output_key,
            present=True,
            empty=len(container) == 0,
            kind="list",
            length=len(container),
        )
    if isinstance(container, dict):
        return OutputSnapshot(
            output=output_key,
            present=True,
            empty=len(container) == 0,
            kind="dict",
            length=len(container),
        )
    if container is None:
        return OutputSnapshot(output=output_key, present=True, empty=True, kind="null")
    return OutputSnapshot(output=output_key, present=True, empty=False, kind="scalar")


def _build_candidate_evidence(
    success: JsonObject | None,
    probe: JsonObject | None,
    output_key: str,
    fields: list[str],
) -> InvalidProbeEvidence | None:
    if not success or not probe:
        return None
    success_row = _first_row(success, output_key)
    probe_row = _first_row(probe, output_key)
    if fields:
        return InvalidProbeEvidence(
            success_sample=_pick_fields(success_row, fields),
            probe_sample=_pick_fields(probe_row, fields),
        )
    return InvalidProbeEvidence(
        success_sample=_pick_fields(success_row, list(success_row.keys())[:8]),
        probe_sample=_pick_fields(probe_row, list(probe_row.keys())[:8]),
    )


def _candidate_reason(invalid: InvalidProbeHint, rule_type: str | None) -> str | None:
    if rule_type == "output_required":
        if invalid.output_missing:
            return "output_missing"
        if invalid.output_empty:
            return "output_empty"
        return "output_invalid"
    if rule_type in {"all_fields_sentinel", "any_field_sentinel"} and invalid.sentinel:
        return f"sentinel_ratio={invalid.sentinel.sentinel_ratio:.2f}"
    if rule_type in {"all_fields_missing", "any_field_missing"} and invalid.missing:
        return f"missing_ratio={invalid.missing.missing_ratio:.2f}"
    if invalid.candidate_fields:
        return "candidate_fields_detected"
    return None


def _load_invalid_template(path: Path) -> JsonObject | None:
    payload = _load_json(path)
    if not payload:
        return None
    invalid_template = payload.get("invalid_template")
    if isinstance(invalid_template, dict):
        return invalid_template
    return None


def _classify_message(
    spec: EndpointSpec,
    msg_cd: str | None,
    msg1: str | None,
) -> MessageSignal | None:
    if not msg_cd and not msg1:
        return None

    error_codes = {error.code for error in spec.errors if error.code}
    msg_cd_matches: list[str] = []
    msg1_error_matches: list[str] = []
    msg1_empty_matches: list[str] = []
    empty = False
    error = False

    if msg_cd:
        if msg_cd in MESSAGE_EMPTY_CODES:
            empty = True
        if msg_cd in error_codes and msg_cd not in MESSAGE_SUCCESS_CODES:
            msg_cd_matches.append(msg_cd)
            error = True

    if msg1:
        for snippet in MESSAGE_EMPTY_SNIPPETS:
            if snippet in msg1:
                msg1_empty_matches.append(snippet)
        if msg1_empty_matches:
            empty = True
        if not empty:
            for snippet in MESSAGE_ERROR_SNIPPETS:
                if snippet in msg1:
                    msg1_error_matches.append(snippet)
            if msg1_error_matches:
                error = True

    if not msg_cd_matches and not msg1_error_matches and not msg1_empty_matches and not empty:
        return None

    return MessageSignal(
        error=error,
        empty=empty,
        msg_cd_matches=msg_cd_matches,
        msg1_error_matches=msg1_error_matches,
        msg1_empty_matches=msg1_empty_matches,
    )


def compare_missing_fields(success: JsonObject, probe: JsonObject) -> MissingComparisonResult:
    diffs: list[MissingFieldDiff] = []
    total_fields = 0
    for output_key in ("output", "output1", "output2"):
        success_rows = _as_rows(success.get(output_key))
        probe_rows = _as_rows(probe.get(output_key))
        if not success_rows:
            continue
        success_row = success_rows[0]
        probe_row = probe_rows[0] if probe_rows else {}
        total_fields = max(total_fields, len(success_row))
        for field, value in success_row.items():
            if field not in probe_row:
                diffs.append(MissingFieldDiff(field=field, success_value=_stringify(value)))

    missing_ratio = (len(diffs) / total_fields) if total_fields else 0.0
    return MissingComparisonResult(diffs=diffs, missing_ratio=missing_ratio, total_fields=total_fields)


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


def _first_row(payload: JsonObject, output_key: str) -> JsonObject:
    rows = _as_rows(payload.get(output_key))
    if rows:
        return rows[0]
    return {}


def _primary_output_key(spec: EndpointSpec) -> str:
    if spec.response.outputs:
        return spec.response.outputs[0].code
    return "output"


def _output_state(payload: JsonObject, output_key: str) -> tuple[bool, bool]:
    if output_key in payload:
        container = payload.get(output_key)
    elif output_key != "output" and "output" in payload:
        container = payload.get("output")
    else:
        return True, False

    if isinstance(container, list):
        return False, len(container) == 0
    if isinstance(container, dict):
        return False, len(container) == 0
    if container is None:
        return True, False
    return False, False


def _load_json(path: Path) -> JsonObject | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


__all__ = [
    "build_validation_candidates",
    "compare_missing_fields",
    "compare_responses",
    "discover_validators",
]
