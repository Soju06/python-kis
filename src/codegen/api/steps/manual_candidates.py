from __future__ import annotations

import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal, cast

from codegen.api.models import EndpointSpec, SpecField
from codegen.api.report_models import (
    EnumManualReviewEndpoint,
    EnumManualReviewField,
    EnumManualReviewReport,
    SmokeReport,
)
from codegen.api.types import EndpointHints, FieldHint, TypeOverrides
from codegen.core.types import JsonObject

_SMOKE_RANK = {"error": 0, "skipped": 1, "ok": 2, "unknown": 3}
_UPPER_CODE_RE = re.compile(r"^[A-Z0-9]{1,6}$")
_WORD_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{2,}$")
_LOWER_ENUM_PATTERN_RE = re.compile(r"^[a-z][0-9]{1,4}$")
_SUSPICIOUS_KEYWORDS = {
    "header",
    "type",
    "length",
    "default",
    "id",
    "code",
    "odno",
    "inquire",
    "overseas",
    "nccs",
    "buy",
    "in",
    "mutual",
    "ritz",
    "fghin",
}
_MIXED_CASE_ALLOWLIST = {"HKEx"}
SmokeStatus = Literal["error", "skipped", "ok", "unknown"]
ConfidenceLevel = Literal["high", "medium", "low"]
ManualPriorityDecision = Literal["parser_fix", "override_review"]


def _parse_length(length: str | None) -> int | None:
    if length is None:
        return None
    text = length.strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def _normalize_enum_values(values: list[str] | None) -> list[str]:
    if not values:
        return []
    normalized: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = value.strip()
        if not text or text in seen:
            continue
        seen.add(text)
        normalized.append(text)
    return normalized


def _is_suspicious_token(value: str, field_length: int | None) -> tuple[bool, set[str]]:
    reasons: set[str] = set()
    lower = value.lower()
    has_lowercase = any(char.islower() for char in value)
    is_lower_enum_pattern = bool(_LOWER_ENUM_PATTERN_RE.fullmatch(value)) or (
        len(value) == 1 and value.islower()
    )
    length_violation = field_length is not None and len(value) > field_length
    keyword = lower in _SUSPICIOUS_KEYWORDS
    looks_word = bool(_WORD_RE.fullmatch(value))
    upper_code = bool(_UPPER_CODE_RE.fullmatch(value))

    if keyword:
        reasons.add("keyword_token")
    if value == "FGHIN":
        reasons.add("collapsed_token")
    if has_lowercase and value not in _MIXED_CASE_ALLOWLIST and not is_lower_enum_pattern:
        reasons.add("lowercase_token")
    if length_violation and (reasons or (looks_word and not upper_code)):
        reasons.add("length_violation")

    return bool(reasons), reasons


def _detect_suspicious_values(enum_values: list[str], field_length: int | None) -> tuple[list[str], list[str]]:
    suspicious_values: list[str] = []
    reasons: set[str] = set()
    for value in enum_values:
        is_suspicious, token_reasons = _is_suspicious_token(value, field_length)
        if not is_suspicious:
            continue
        if value not in suspicious_values:
            suspicious_values.append(value)
        reasons.update(token_reasons)
    return suspicious_values, sorted(reasons)


def _build_smoke_status_map(smoke: SmokeReport) -> dict[str, SmokeStatus]:
    status_map: dict[str, SmokeStatus] = {}
    for result in smoke.results:
        status: SmokeStatus
        if result.status in _SMOKE_RANK:
            status = cast(SmokeStatus, result.status)
        else:
            status = "unknown"
        current = status_map.get(result.id)
        if current is None or _SMOKE_RANK[status] < _SMOKE_RANK[current]:
            status_map[result.id] = status
    return status_map


def _build_request_field_lookup(spec: EndpointSpec) -> dict[str, tuple[str, SpecField]]:
    lookup: dict[str, tuple[str, SpecField]] = {}
    for field in spec.request.query:
        lookup.setdefault(field.code, ("request.query", field))
    for field in spec.request.body:
        lookup.setdefault(field.code, ("request.body", field))
    for field in spec.request.headers:
        lookup.setdefault(field.code, ("request.headers", field))
    return lookup


def _build_response_field_lookup(spec: EndpointSpec) -> dict[str, SpecField]:
    return {field.code: field for field in spec.response.body}


def _build_output_field_lookup(spec: EndpointSpec) -> dict[tuple[str, str], SpecField]:
    lookup: dict[tuple[str, str], SpecField] = {}
    for output in spec.response.outputs:
        for field in output.fields:
            lookup[(output.code, field.code)] = field
    return lookup


def _to_confidence(smoke_status: SmokeStatus, reasons: list[str]) -> ConfidenceLevel:
    reason_set = set(reasons)
    if smoke_status == "error" or {"keyword_token", "collapsed_token"} & reason_set:
        return "high"
    if smoke_status == "skipped" or "length_violation" in reason_set:
        return "medium"
    return "low"


def _build_field_candidate(
    *,
    hint: FieldHint,
    field: SpecField,
    location: str,
    output: str | None,
    smoke_status: SmokeStatus,
) -> EnumManualReviewField | None:
    enum_values = _normalize_enum_values(hint.enum)
    if hint.kind != "enum" or not enum_values:
        return None

    field_length = _parse_length(field.length)
    suspicious_values, reasons = _detect_suspicious_values(enum_values, field_length)
    if not suspicious_values:
        return None

    confidence = _to_confidence(smoke_status, reasons)
    return EnumManualReviewField(
        location=location,
        output=output,
        field_code=field.code,
        field_name=field.name or field.code,
        field_length=field_length,
        suspicious_values=suspicious_values,
        enum_values=enum_values,
        reasons=reasons,
        confidence=confidence,
    )


def _collect_endpoint_candidates(
    *,
    spec: EndpointSpec,
    hints: EndpointHints,
    smoke_status: SmokeStatus,
) -> list[EnumManualReviewField]:
    request_lookup = _build_request_field_lookup(spec)
    response_lookup = _build_response_field_lookup(spec)
    output_lookup = _build_output_field_lookup(spec)
    fields: list[EnumManualReviewField] = []

    for field_code, hint in hints.request.items():
        request_field = request_lookup.get(field_code)
        if request_field is None:
            continue
        location, field = request_field
        candidate = _build_field_candidate(
            hint=hint,
            field=field,
            location=location,
            output=None,
            smoke_status=smoke_status,
        )
        if candidate is not None:
            fields.append(candidate)

    for field_code, hint in hints.response.items():
        field = response_lookup.get(field_code)
        if field is None:
            continue
        candidate = _build_field_candidate(
            hint=hint,
            field=field,
            location="response.body",
            output=None,
            smoke_status=smoke_status,
        )
        if candidate is not None:
            fields.append(candidate)

    for output_code, output_hints in hints.outputs.items():
        for field_code, hint in output_hints.items():
            field = output_lookup.get((output_code, field_code))
            if field is None:
                continue
            candidate = _build_field_candidate(
                hint=hint,
                field=field,
                location="response.output",
                output=output_code,
                smoke_status=smoke_status,
            )
            if candidate is not None:
                fields.append(candidate)

    fields.sort(key=lambda item: (item.location, item.output or "", item.field_code))
    return fields


def _join_values(values: list[str], *, limit: int) -> str:
    if not values:
        return "-"
    if len(values) <= limit:
        return ", ".join(values)
    head = ", ".join(values[:limit])
    return f"{head}, … (+{len(values) - limit})"


def build_enum_manual_review_candidates(
    specs: list[EndpointSpec],
    inference: TypeOverrides,
    smoke: SmokeReport,
    *,
    augment_dir: Path,
) -> EnumManualReviewReport:
    spec_map = {spec.id: spec for spec in specs}
    smoke_status = _build_smoke_status_map(smoke)
    candidates: list[EnumManualReviewEndpoint] = []

    for endpoint_id in sorted(inference.endpoints):
        hints = inference.endpoints[endpoint_id]
        spec = spec_map.get(endpoint_id)
        if spec is None:
            continue
        status = smoke_status.get(endpoint_id, "unknown")
        fields = _collect_endpoint_candidates(spec=spec, hints=hints, smoke_status=status)
        if not fields:
            continue
        evidence = {
            "normalized_path": spec.source_path,
            "request_path": str(augment_dir / endpoint_id / "request.json"),
            "raw_path": str(augment_dir / endpoint_id / "raw.json"),
        }
        candidates.append(
            EnumManualReviewEndpoint(
                endpoint_id=endpoint_id,
                endpoint_name=spec.name,
                path=spec.path,
                source_path=spec.source_path,
                smoke_status=status,
                fields=fields,
                evidence=evidence,
            )
        )

    candidates.sort(key=lambda item: (_SMOKE_RANK.get(item.smoke_status, 99), item.endpoint_id))
    by_smoke_status = dict(Counter(item.smoke_status for item in candidates))
    by_confidence = dict(Counter(field.confidence for item in candidates for field in item.fields))
    total_fields = sum(len(item.fields) for item in candidates)

    return EnumManualReviewReport(
        generated_at=datetime.now(timezone.utc).isoformat(),
        total_fields=total_fields,
        endpoints=len(candidates),
        by_smoke_status=by_smoke_status,
        by_confidence=by_confidence,
        candidates=candidates,
    )


def render_enum_manual_review_candidates_markdown(report: EnumManualReviewReport) -> str:
    lines = [
        "# Enum Parser Manual Review Candidates",
        "",
        f"- generated_at: {report.generated_at}",
        f"- total_fields: {report.total_fields}",
        f"- endpoints: {report.endpoints}",
        f"- by_smoke_status: {report.by_smoke_status}",
        f"- by_confidence: {report.by_confidence}",
        "",
    ]

    if not report.candidates:
        lines.append("(no candidates)")
        return "\n".join(lines).rstrip() + "\n"

    for endpoint in report.candidates:
        lines.extend(
            [
                f"## {endpoint.endpoint_id}",
                f"- name: {endpoint.endpoint_name}",
                f"- path: {endpoint.path}",
                f"- smoke_status: {endpoint.smoke_status}",
                f"- evidence: {endpoint.evidence.get('raw_path', '-')}",
                "",
                "| Location | Field | Suspicious Values | Reasons | Confidence |",
                "| :--- | :--- | :--- | :--- | :--- |",
            ]
        )
        for field in endpoint.fields:
            location = f"{field.location}.{field.output}" if field.output else field.location
            lines.append(
                "| "
                + " | ".join(
                    [
                        location,
                        field.field_code,
                        _join_values(field.suspicious_values, limit=8),
                        _join_values(field.reasons, limit=6),
                        field.confidence,
                    ]
                )
                + " |"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _classify_manual_field(field: EnumManualReviewField) -> tuple[ManualPriorityDecision, str]:
    reasons = set(field.reasons)
    if {"collapsed_token", "keyword_token", "lowercase_token"} & reasons:
        return "parser_fix", "description token contamination likely"
    if "length_violation" in reasons:
        return "override_review", "length-only anomaly; verify true enum expansion"
    return "override_review", "manual review required"


def build_enum_manual_review_priority(
    report: EnumManualReviewReport,
    *,
    source_report_path: str,
) -> JsonObject:
    ready: list[JsonObject] = []
    hold: list[JsonObject] = []
    parser_fix_fields = 0
    override_review_fields = 0
    ready_fields_total = 0
    hold_fields_total = 0

    for endpoint in report.candidates:
        ready_fields: list[JsonObject] = []
        hold_fields: list[JsonObject] = []
        hold_reasons: set[str] = set()
        for field in endpoint.fields:
            decision, decision_reason = _classify_manual_field(field)
            row = cast(
                JsonObject,
                {
                    "location": field.location,
                    "output": field.output,
                    "field_code": field.field_code,
                    "field_name": field.field_name,
                    "suspicious_values": field.suspicious_values,
                    "reasons": field.reasons,
                    "confidence": field.confidence,
                    "decision": decision,
                    "decision_reason": decision_reason,
                },
            )
            if decision == "parser_fix":
                parser_fix_fields += 1
                ready_fields.append(row)
            else:
                override_review_fields += 1
                hold_fields.append(row)
                hold_reasons.add("override_review")

        ready_fields_total += len(ready_fields)
        hold_fields_total += len(hold_fields)
        item = cast(
            JsonObject,
            {
                "id": endpoint.endpoint_id,
                "name": endpoint.endpoint_name,
                "path": endpoint.path,
                "smoke_status": endpoint.smoke_status,
                "evidence": endpoint.evidence.get("raw_path") if isinstance(endpoint.evidence, dict) else None,
                "ready_fields": ready_fields,
                "hold_fields": hold_fields,
                "hold_reasons": sorted(hold_reasons),
                "review_count": len(endpoint.fields),
            },
        )
        if hold_fields:
            hold.append(item)
        else:
            ready.append(item)

    summary = cast(
        JsonObject,
        {
            "total_endpoints": report.endpoints,
            "total_fields": report.total_fields,
            "ready_endpoints": len(ready),
            "hold_endpoints": len(hold),
            "ready_fields": ready_fields_total,
            "hold_fields": hold_fields_total,
            "parser_fix_fields": parser_fix_fields,
            "override_review_fields": override_review_fields,
        },
    )
    return cast(
        JsonObject,
        {
            "version": 1,
            "generated_at": report.generated_at,
            "source_report": source_report_path,
            "summary": summary,
            "ready": ready,
            "hold": hold,
        },
    )


def render_enum_manual_review_priority_markdown(payload: JsonObject) -> str:
    summary = payload.get("summary")
    summary_map = summary if isinstance(summary, dict) else {}
    lines = [
        "# Enum Parser Review Priority",
        "",
        f"- generated_at: {payload.get('generated_at', '-')}",
        f"- source_report: {payload.get('source_report', '-')}",
        f"- total_endpoints: {summary_map.get('total_endpoints', 0)}",
        f"- total_fields: {summary_map.get('total_fields', 0)}",
        f"- ready_endpoints: {summary_map.get('ready_endpoints', 0)}",
        f"- hold_endpoints: {summary_map.get('hold_endpoints', 0)}",
        f"- parser_fix_fields: {summary_map.get('parser_fix_fields', 0)}",
        f"- override_review_fields: {summary_map.get('override_review_fields', 0)}",
        "",
    ]

    ready_raw = payload.get("ready")
    ready_items = (
        [cast(JsonObject, item) for item in ready_raw if isinstance(item, dict)]
        if isinstance(ready_raw, list)
        else []
    )
    hold_raw = payload.get("hold")
    hold_items = (
        [cast(JsonObject, item) for item in hold_raw if isinstance(item, dict)]
        if isinstance(hold_raw, list)
        else []
    )

    lines.extend(
        [
            "## Ready (파서 수정 우선)",
            "",
            "| Endpoint ID | Name | Smoke | Ready Fields | Hold Fields |",
            "| :--- | :--- | :--- | ---: | ---: |",
        ]
    )
    for item in ready_items:
        ready_fields_raw = item.get("ready_fields")
        hold_fields_raw = item.get("hold_fields")
        ready_fields_count = len(ready_fields_raw) if isinstance(ready_fields_raw, list) else 0
        hold_fields_count = len(hold_fields_raw) if isinstance(hold_fields_raw, list) else 0
        lines.append(
            "| "
            + " | ".join(
                [
                    str(item.get("id") or "-"),
                    str(item.get("name") or "-"),
                    str(item.get("smoke_status") or "-"),
                    str(ready_fields_count),
                    str(hold_fields_count),
                ]
            )
            + " |"
        )
    if not ready_items:
        lines.append("| - | - | - | 0 | 0 |")
    lines.append("")

    lines.extend(
        [
            "## Hold (override 검토)",
            "",
            "| Endpoint ID | Name | Smoke | Ready Fields | Hold Fields | Reasons |",
            "| :--- | :--- | :--- | ---: | ---: | :--- |",
        ]
    )
    for item in hold_items:
        ready_fields_raw = item.get("ready_fields")
        hold_fields_raw = item.get("hold_fields")
        ready_fields_count = len(ready_fields_raw) if isinstance(ready_fields_raw, list) else 0
        hold_fields_count = len(hold_fields_raw) if isinstance(hold_fields_raw, list) else 0
        reasons_raw = item.get("hold_reasons")
        reasons = [str(reason) for reason in reasons_raw] if isinstance(reasons_raw, list) else []
        reason_text = ", ".join(str(reason) for reason in reasons) if reasons else "-"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(item.get("id") or "-"),
                    str(item.get("name") or "-"),
                    str(item.get("smoke_status") or "-"),
                    str(ready_fields_count),
                    str(hold_fields_count),
                    reason_text,
                ]
            )
            + " |"
        )
    if not hold_items:
        lines.append("| - | - | - | 0 | 0 | - |")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


__all__ = [
    "build_enum_manual_review_candidates",
    "build_enum_manual_review_priority",
    "render_enum_manual_review_candidates_markdown",
    "render_enum_manual_review_priority_markdown",
]
