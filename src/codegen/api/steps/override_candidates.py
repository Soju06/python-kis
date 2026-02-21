from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import cast

from codegen.api.report_models import EnumDriftCandidateReport
from codegen.api.types import TypeOverrides
from codegen.core.types import JsonObject


@dataclass(slots=True)
class _EndpointDraftBuilder:
    endpoint_id: str
    endpoint_name: str
    path: str
    source_path: str
    changes: JsonObject = field(default_factory=dict)
    review_rows: list[JsonObject] = field(default_factory=list)
    evidence_paths: set[str] = field(default_factory=set)


def _ensure_map(target: JsonObject, key: str) -> JsonObject:
    value = target.get(key)
    if isinstance(value, dict):
        return value
    payload: JsonObject = {}
    target[key] = payload
    return payload


def _merge_enum_values(existing: object, proposed: list[str]) -> list[str]:
    values: list[str] = []
    if isinstance(existing, list):
        for item in existing:
            text = str(item).strip()
            if text and text not in values:
                values.append(text)
    for item in proposed:
        text = str(item).strip()
        if text and text not in values:
            values.append(text)
    return values


def _normalize_values(values: object) -> set[str]:
    normalized: set[str] = set()
    if not isinstance(values, list):
        return normalized
    for item in values:
        text = str(item).strip()
        if text:
            normalized.add(text)
    return normalized


def _lookup_override_enum_values(
    overrides: TypeOverrides,
    *,
    endpoint_id: str,
    location: str,
    output_code: str,
    field_code: str,
) -> set[str]:
    endpoint_hints = overrides.endpoints.get(endpoint_id)
    if endpoint_hints is None:
        return set()

    field_hint = None
    if location in {"request.query", "request.body"}:
        field_hint = endpoint_hints.request.get(field_code)
    elif location == "response.body":
        field_hint = endpoint_hints.response.get(field_code)
    elif location == "response.output":
        output_fields = endpoint_hints.outputs.get(output_code)
        if isinstance(output_fields, dict):
            field_hint = output_fields.get(field_code)

    if field_hint is None or field_hint.enum is None:
        return set()
    return _normalize_values(field_hint.enum)


def _lookup_override_kind(
    overrides: TypeOverrides,
    *,
    endpoint_id: str,
    location: str,
    output_code: str,
    field_code: str,
) -> str | None:
    endpoint_hints = overrides.endpoints.get(endpoint_id)
    if endpoint_hints is None:
        return None

    field_hint = None
    if location in {"request.query", "request.body"}:
        field_hint = endpoint_hints.request.get(field_code)
    elif location == "response.body":
        field_hint = endpoint_hints.response.get(field_code)
    elif location == "response.output":
        output_fields = endpoint_hints.outputs.get(output_code)
        if isinstance(output_fields, dict):
            field_hint = output_fields.get(field_code)

    if field_hint is None or field_hint.kind is None:
        return None
    return str(field_hint.kind).strip().lower()


def _is_candidate_covered_by_overrides(
    candidate: JsonObject,
    applied_overrides: TypeOverrides | None,
) -> bool:
    if applied_overrides is None:
        return False

    endpoint_id = str(candidate.get("endpoint_id") or "").strip()
    location = str(candidate.get("location") or "").strip()
    output_code = str(candidate.get("output") or "").strip()
    field_code = str(candidate.get("field_code") or "").strip()
    unknown_values = _normalize_values(candidate.get("unknown_values"))
    if not endpoint_id or not location or not field_code or not unknown_values:
        return False

    override_kind = _lookup_override_kind(
        applied_overrides,
        endpoint_id=endpoint_id,
        location=location,
        output_code=output_code,
        field_code=field_code,
    )
    if override_kind and override_kind != "enum":
        return True

    override_values = _lookup_override_enum_values(
        applied_overrides,
        endpoint_id=endpoint_id,
        location=location,
        output_code=output_code,
        field_code=field_code,
    )
    if not override_values:
        return False
    return unknown_values.issubset(override_values)


def _apply_enum_change(builder: _EndpointDraftBuilder, candidate: JsonObject) -> None:
    location = str(candidate.get("location") or "").strip()
    field_code = str(candidate.get("field_code") or "").strip()
    if not field_code:
        return
    proposed_values_raw = candidate.get("proposed_values")
    if not isinstance(proposed_values_raw, list):
        return
    proposed_values = [str(item).strip() for item in proposed_values_raw if str(item).strip()]
    if not proposed_values:
        return

    if location in {"request.query", "request.body"}:
        request = _ensure_map(builder.changes, "request")
        field_hint = _ensure_map(request, field_code)
        field_hint["enum"] = _merge_enum_values(field_hint.get("enum"), proposed_values)
        return

    if location == "response.body":
        response = _ensure_map(builder.changes, "response")
        field_hint = _ensure_map(response, field_code)
        field_hint["enum"] = _merge_enum_values(field_hint.get("enum"), proposed_values)
        return

    if location == "response.output":
        output_code = str(candidate.get("output") or "").strip()
        if not output_code:
            return
        outputs = _ensure_map(builder.changes, "outputs")
        output_map = _ensure_map(outputs, output_code)
        field_hint = _ensure_map(output_map, field_code)
        field_hint["enum"] = _merge_enum_values(field_hint.get("enum"), proposed_values)


def _today_utc() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _sort_review_rows(rows: list[JsonObject]) -> list[JsonObject]:
    return sorted(
        rows,
        key=lambda row: (
            str(row.get("location") or ""),
            str(row.get("output") or ""),
            str(row.get("field_code") or ""),
        ),
    )


def build_enum_type_override_candidates(
    report: EnumDriftCandidateReport,
    *,
    source_report_path: str,
    applied_overrides: TypeOverrides | None = None,
) -> JsonObject:
    today = _today_utc()
    builders: dict[str, _EndpointDraftBuilder] = {}
    covered_by_existing_overrides = 0

    for candidate in report.candidates:
        candidate_map = candidate.model_dump()
        if _is_candidate_covered_by_overrides(candidate_map, applied_overrides):
            covered_by_existing_overrides += 1
            continue

        builder = builders.get(candidate.endpoint_id)
        if builder is None:
            builder = _EndpointDraftBuilder(
                endpoint_id=candidate.endpoint_id,
                endpoint_name=candidate.endpoint_name,
                path=candidate.path,
                source_path=candidate.source_path,
            )
            builders[candidate.endpoint_id] = builder

        _apply_enum_change(builder, candidate_map)

        evidence = candidate.evidence
        raw_path = str(evidence.get("raw_path") or "").strip()
        request_path = str(evidence.get("request_path") or "").strip()
        if raw_path:
            builder.evidence_paths.add(raw_path)
        if request_path:
            builder.evidence_paths.add(request_path)

        builder.review_rows.append(
            {
                "location": candidate.location,
                "output": candidate.output,
                "field_code": candidate.field_code,
                "field_name": candidate.field_name,
                "documented_values": candidate.documented_values,
                "unknown_values": candidate.unknown_values,
                "observed_values": candidate.observed_values,
                "proposed_values": candidate.proposed_values,
                "evidence": candidate.evidence,
                "status": candidate.status,
            }
        )

    overrides: list[JsonObject] = []
    for endpoint_id in sorted(builders):
        builder = builders[endpoint_id]
        evidence_paths = sorted(builder.evidence_paths)
        overrides.append(
            {
                "id": builder.endpoint_id,
                "name": builder.endpoint_name,
                "path": builder.path,
                "source_path": builder.source_path,
                "reason": "Live samples include undocumented enum values (manual review required).",
                "source": f"enum drift candidate ({today})",
                "approved_by": "<pending>",
                "approved_at": "<YYYY-MM-DD>",
                "evidence": evidence_paths[0] if evidence_paths else "",
                "evidence_paths": evidence_paths,
                "changes": builder.changes,
                "review": _sort_review_rows(builder.review_rows),
            }
        )

    return cast(
        JsonObject,
        {
            "version": 1,
            "generated_at": report.generated_at,
            "source_report": source_report_path,
            "summary": {
                "total_candidates": report.total,
                "endpoints": report.endpoints,
                "by_location": report.by_location,
                "covered_by_existing_overrides": covered_by_existing_overrides,
                "pending_candidates": max(0, report.total - covered_by_existing_overrides),
                "draft_overrides": len(overrides),
            },
            "overrides": overrides,
        },
    )


def render_enum_type_override_candidates_markdown(payload: JsonObject) -> str:
    summary = payload.get("summary")
    summary_map = summary if isinstance(summary, dict) else {}
    lines = [
        "# Enum Type Override Draft Candidates",
        "",
        f"- generated_at: {payload.get('generated_at', '-')}",
        f"- source_report: {payload.get('source_report', '-')}",
        f"- total_candidates: {summary_map.get('total_candidates', 0)}",
        f"- endpoints: {summary_map.get('endpoints', 0)}",
        f"- draft_overrides: {summary_map.get('draft_overrides', 0)}",
        "",
        "> 이 파일은 수동 검토용 초안입니다. `data/overrides/type_overrides.yaml`에 자동 반영되지 않습니다.",
        "",
    ]

    overrides = payload.get("overrides")
    override_list = overrides if isinstance(overrides, list) else []
    for item in override_list:
        if not isinstance(item, dict):
            continue
        override_id = str(item.get("id") or "").strip()
        if not override_id:
            continue
        lines.extend(
            [
                f"## {override_id}",
                f"- name: {item.get('name', '-')}",
                f"- path: {item.get('path', '-')}",
                f"- evidence: {item.get('evidence', '-')}",
                "- suggested changes:",
                "```yaml",
                "changes:",
            ]
        )
        changes = item.get("changes")
        lines.extend(_render_yaml_like(changes, indent=2))
        lines.extend(["```", ""])

    return "\n".join(lines).rstrip() + "\n"


def _render_yaml_like(value: object, *, indent: int) -> list[str]:
    prefix = " " * indent
    lines: list[str] = []
    if isinstance(value, dict):
        mapping = cast(dict[str, object], value)
        for key in sorted(mapping):
            item = mapping[key]
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.extend(_render_yaml_like(item, indent=indent + 2))
            else:
                lines.append(f"{prefix}{key}: {item}")
        return lines
    if isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(_render_yaml_like(item, indent=indent + 2))
            else:
                lines.append(f"{prefix}- {item}")
        return lines
    lines.append(f"{prefix}{value}")
    return lines


def _is_code_field(field_code: str, field_name: str) -> bool:
    code = field_code.lower()
    name = field_name.lower()
    if code.endswith("_code") or code.endswith("_cd"):
        return True
    if "_cls_code" in code or "code" in code:
        return True
    if "코드" in field_name or "국가" in field_name:
        return True
    if "code" in name or "country" in name:
        return True
    return False


def _is_time_field(field_code: str, field_name: str) -> bool:
    code = field_code.lower()
    if any(token in code for token in ("hour", "time", "_tm", "cntg_hour")):
        return True
    return "시간" in field_name or "시각" in field_name


def _has_decimal_like(values: list[str]) -> bool:
    return any("." in value for value in values)


def _classify_review_item(review_item: JsonObject) -> tuple[str, str]:
    location = str(review_item.get("location") or "").strip()
    field_code = str(review_item.get("field_code") or "").strip()
    field_name = str(review_item.get("field_name") or "").strip()
    unknown_values_raw = review_item.get("unknown_values")
    unknown_values = (
        [str(item).strip() for item in unknown_values_raw if str(item).strip()]
        if isinstance(unknown_values_raw, list)
        else []
    )
    unknown_count = len(unknown_values)

    if location.startswith("request."):
        return "hold_request", "request enum change requires separate review"
    if unknown_count >= 20:
        return "hold_high_cardinality", "too many unknown values; likely parser/type issue"
    if _is_time_field(field_code, field_name) and unknown_count >= 5:
        return "hold_time_value_expansion", "time-like field should not expand enum with raw time values"
    if _has_decimal_like(unknown_values) and not _is_code_field(field_code, field_name):
        return "hold_parser_decimal", "decimal-like samples suggest enum parse issue"
    return "ready", "safe enum extension candidate"


def _list_len(value: object) -> int:
    return len(value) if isinstance(value, list) else 0


def build_enum_type_override_priority(draft_payload: JsonObject) -> JsonObject:
    overrides_raw = draft_payload.get("overrides")
    overrides = [item for item in overrides_raw if isinstance(item, dict)] if isinstance(overrides_raw, list) else []

    ready: list[JsonObject] = []
    hold: list[JsonObject] = []
    for override in overrides:
        review_raw = override.get("review")
        review_items = [item for item in review_raw if isinstance(item, dict)] if isinstance(review_raw, list) else []

        ready_fields: list[JsonObject] = []
        hold_fields: list[JsonObject] = []
        hold_reasons: set[str] = set()
        for review_item in review_items:
            status, reason = _classify_review_item(review_item)
            row: JsonObject = {
                "location": review_item.get("location"),
                "output": review_item.get("output"),
                "field_code": review_item.get("field_code"),
                "field_name": review_item.get("field_name"),
                "status": status,
                "reason": reason,
                "unknown_values": review_item.get("unknown_values"),
            }
            if status == "ready":
                ready_fields.append(row)
            else:
                hold_fields.append(row)
                hold_reasons.add(status)

        item = cast(
            JsonObject,
            {
                "id": override.get("id"),
                "name": override.get("name"),
                "path": override.get("path"),
                "evidence": override.get("evidence"),
                "ready_fields": ready_fields,
                "hold_fields": hold_fields,
                "hold_reasons": sorted(hold_reasons),
                "review_count": len(review_items),
            },
        )
        if hold_fields:
            hold.append(item)
        else:
            ready.append(item)

    summary = {
        "total_overrides": len(overrides),
        "ready_overrides": len(ready),
        "hold_overrides": len(hold),
        "ready_fields": sum(_list_len(item.get("ready_fields")) for item in ready),
        "hold_fields": sum(_list_len(item.get("hold_fields")) for item in hold),
    }

    return cast(
        JsonObject,
        {
            "version": 1,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_report": draft_payload.get("source_report", ""),
            "summary": summary,
            "ready": ready,
            "hold": hold,
        },
    )


def render_enum_type_override_priority_markdown(payload: JsonObject) -> str:
    summary = payload.get("summary")
    summary_map = summary if isinstance(summary, dict) else {}
    lines = [
        "# Enum Override Priority Review",
        "",
        f"- generated_at: {payload.get('generated_at', '-')}",
        f"- source_report: {payload.get('source_report', '-')}",
        f"- total_overrides: {summary_map.get('total_overrides', 0)}",
        f"- ready_overrides: {summary_map.get('ready_overrides', 0)}",
        f"- hold_overrides: {summary_map.get('hold_overrides', 0)}",
        "",
    ]

    ready_items = payload.get("ready")
    ready_list = [item for item in ready_items if isinstance(item, dict)] if isinstance(ready_items, list) else []
    lines.extend(["## Ready (승인 우선)", ""])
    if not ready_list:
        lines.append("- 없음")
        lines.append("")
    for item in ready_list:
        lines.extend(
            [
                f"### {item.get('id', '-')}",
                f"- name: {item.get('name', '-')}",
                f"- path: {item.get('path', '-')}",
                f"- review_count: {item.get('review_count', 0)}",
                f"- evidence: {item.get('evidence', '-')}",
                "",
            ]
        )

    hold_items = payload.get("hold")
    hold_list = [item for item in hold_items if isinstance(item, dict)] if isinstance(hold_items, list) else []
    lines.extend(["## Hold (추가 검토)", ""])
    if not hold_list:
        lines.append("- 없음")
        lines.append("")
    for item in hold_list:
        reasons = item.get("hold_reasons")
        reason_text = ", ".join(str(reason) for reason in reasons) if isinstance(reasons, list) else "-"
        lines.extend(
            [
                f"### {item.get('id', '-')}",
                f"- name: {item.get('name', '-')}",
                f"- path: {item.get('path', '-')}",
                f"- hold_reasons: {reason_text}",
                "",
            ]
        )
        hold_fields = item.get("hold_fields")
        hold_field_list = [row for row in hold_fields if isinstance(row, dict)] if isinstance(hold_fields, list) else []
        for row in hold_field_list:
            lines.append(
                f"- field `{row.get('field_code', '-')}` ({row.get('location', '-')}) : {row.get('reason', '-')}"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


__all__ = [
    "build_enum_type_override_candidates",
    "build_enum_type_override_priority",
    "render_enum_type_override_candidates_markdown",
    "render_enum_type_override_priority_markdown",
]
