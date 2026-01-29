from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import cast

import yaml

from codegen.core.paths import project_root
from codegen.core.render import render_template
from codegen.core.types import JsonObject, JsonValue

OAUTH_SECTIONS = {"OAuth인증"}
OAUTH_SUBCATEGORIES = {"OAuth인증"}
REALTIME_SUBCATEGORIES = {"실시간시세"}
EXCLUDED_PATH_PREFIXES = ("/oauth2",)


def write_api_report(root: Path | None = None) -> Path:
    target_root = root or project_root()
    report = build_api_report(target_root)
    report_dir = target_root / "tmp" / "docs" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / "api_report.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    _write_api_report_markdown(report_dir, report)
    return path


def build_api_report(root: Path) -> JsonObject:
    report_dir = root / "tmp" / "docs" / "reports"
    augment_dir = root / "tmp" / "docs" / "augment"
    normalized_dir = root / "tmp" / "docs" / "normalized"
    overrides_path = root / "docs" / "overrides" / "type_overrides.yaml"

    scan = _load_json(report_dir / "scan.json")
    normalize = _load_json(report_dir / "normalize.json")
    augment = _load_json(report_dir / "augment.json")
    validation = _load_json(report_dir / "validation.json")
    smoke = _load_json(report_dir / "smoke.json")
    inference_base = _load_json(report_dir / "inference_base.json")
    inference = _load_json(report_dir / "inference.json")
    inference_trace = _load_json(report_dir / "inference_trace.json")
    smoke_requests = _load_json(report_dir / "smoke_requests.json")

    specs = _load_specs(normalized_dir)
    spec_list = list(specs.values())
    oauth_specs = [spec for spec in spec_list if _is_oauth_spec(spec)]
    realtime_specs = [spec for spec in spec_list if _is_realtime_spec(spec)]
    api_specs = [spec for spec in spec_list if spec not in oauth_specs and spec not in realtime_specs]

    exclusion_other = _collect_other_exclusions(api_specs, scan, normalize)
    smoke_summary, smoke_warnings, smoke_errors = _collect_smoke_issues(smoke, specs)

    augment_results_list = _as_list(augment.get("results"))
    augment_results = {str(item.get("id")): item for item in augment_results_list if item.get("id") is not None}
    endpoint_details = _build_endpoint_details(specs, augment_dir, augment_results, smoke, smoke_requests)

    overrides_payload = _load_yaml(overrides_path)
    override_lifecycle = _build_override_lifecycle(
        overrides_payload,
        inference_base,
        inference,
        augment_dir,
    )

    exclusion_details = _as_list(exclusion_other.get("details"))
    report: JsonObject = cast(
        JsonObject,
        {
            "schema_version": "api-report-v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "runtime": {
                "python": sys.version.split()[0],
            },
            "summary": {
                "scan": _summary_counts(scan),
                "normalize": _summary_counts(normalize),
                "augment": _summary_counts(augment),
                "validation": _summary_counts(validation),
                "smoke": smoke_summary,
                "attention": {
                    "warnings": len(smoke_warnings),
                    "errors": len(smoke_errors),
                },
                "override_lifecycle": override_lifecycle.get("summary", {}),
            },
            "scope": {
                "docs_parsed": len(spec_list),
                "api_targets": len(api_specs),
                "excluded": {
                    "oauth": len(oauth_specs),
                    "realtime": len(realtime_specs),
                    "other": len(exclusion_details),
                },
            },
            "exclusions": {
                "oauth": _extract_ids(oauth_specs),
                "realtime": _extract_ids(realtime_specs),
                "other": exclusion_other,
            },
            "smoke": {
                "summary": smoke_summary,
                "warnings": smoke_warnings,
                "errors": smoke_errors,
            },
            "overrides": override_lifecycle,
            "inference": {
                "base": inference_base,
                "applied": inference,
                "trace": inference_trace,
            },
            "endpoints": endpoint_details,
            "sources": {
                "scan": str(report_dir / "scan.json"),
                "normalize": str(report_dir / "normalize.json"),
                "augment": str(report_dir / "augment.json"),
                "validation": str(report_dir / "validation.json"),
                "smoke": str(report_dir / "smoke.json"),
                "smoke_requests": str(report_dir / "smoke_requests.json"),
                "inference_base": str(report_dir / "inference_base.json"),
                "inference": str(report_dir / "inference.json"),
                "inference_trace": str(report_dir / "inference_trace.json"),
            },
        },
    )
    return report


def _summary_counts(payload: JsonObject) -> JsonObject:
    if not payload:
        return {}
    summary: JsonObject = {}
    for key in (
        "total_issues",
        "warnings",
        "total",
        "processed",
        "ok",
        "cached",
        "skipped",
        "errors",
    ):
        if key in payload:
            summary[key] = payload[key]
    return summary


def _load_specs(normalized_dir: Path) -> dict[str, JsonObject]:
    specs: dict[str, JsonObject] = {}
    if not normalized_dir.exists():
        return specs
    for path in normalized_dir.rglob("*.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        spec_id = payload.get("id")
        if spec_id:
            specs[str(spec_id)] = payload
    return specs


def _collect_other_exclusions(
    api_specs: list[JsonObject],
    scan: JsonObject,
    normalize: JsonObject,
) -> JsonObject:
    details: list[JsonObject] = []
    for spec in api_specs:
        domains = _as_object(spec.get("domains")) or {}
        has_domain = bool(domains.get("real") or domains.get("demo"))
        metadata = _as_object(spec.get("metadata")) or {}
        status = metadata.get("status")
        if not has_domain:
            details.append(
                {
                    "id": spec.get("id"),
                    "name": spec.get("name"),
                    "path": spec.get("path"),
                    "reason": "missing_domain",
                    "status": status,
                    "source": spec.get("source_path"),
                }
            )
        elif status and str(status).upper() != "RUNNING":
            details.append(
                {
                    "id": spec.get("id"),
                    "name": spec.get("name"),
                    "path": spec.get("path"),
                    "reason": f"status={status}",
                    "status": status,
                    "source": spec.get("source_path"),
                }
            )

    for error in _as_list(scan.get("parse_errors")):
        details.append(
            {
                "id": None,
                "name": None,
                "path": error.get("path"),
                "reason": "parse_error",
                "status": None,
                "source": error.get("path"),
                "error": error.get("error"),
            }
        )

    for error in _as_list(normalize.get("parse_errors")):
        details.append(
            {
                "id": None,
                "name": None,
                "path": error.get("path"),
                "reason": "normalize_error",
                "status": None,
                "source": error.get("path"),
                "error": error.get("error"),
            }
        )

    summary: JsonObject = {}
    for item in details:
        reason = str(item.get("reason") or "unknown")
        summary[reason] = _to_int(summary.get(reason)) + 1

    return cast(JsonObject, {"summary": summary, "details": details})


def _collect_smoke_issues(
    smoke: JsonObject,
    specs: dict[str, JsonObject],
) -> tuple[JsonObject, list[JsonObject], list[JsonObject]]:
    results = _as_list(smoke.get("results"))
    warnings: list[JsonObject] = []
    errors: list[JsonObject] = []
    for item in results:
        status = item.get("status")
        reason = item.get("reason")
        if status == "error":
            errors.append(_attach_spec_meta(item, specs))
        elif status == "skipped" and reason in {"empty_response"}:
            warnings.append(_attach_spec_meta(item, specs))
    summary = {
        "total": smoke.get("total"),
        "errors": smoke.get("errors"),
        "warnings": len(warnings),
    }
    return summary, warnings, errors


def _attach_spec_meta(item: JsonObject, specs: dict[str, JsonObject]) -> JsonObject:
    spec = specs.get(str(item.get("id"))) if item.get("id") else None
    if not spec:
        return dict(item)
    payload = dict(item)
    payload["name"] = spec.get("name")
    payload["path"] = spec.get("path")
    payload["section"] = spec.get("section")
    payload["category"] = spec.get("category")
    payload["subcategory"] = spec.get("subcategory")
    return payload


def _build_endpoint_details(
    specs: dict[str, JsonObject],
    augment_dir: Path,
    augment_results: dict[str, JsonObject],
    smoke: JsonObject,
    smoke_requests: JsonObject,
) -> dict[str, JsonObject]:
    details: dict[str, JsonObject] = {}
    smoke_results_all = _as_list(smoke.get("results"))
    for spec_id, spec in specs.items():
        augment_result = augment_results.get(spec_id, {})
        augment_payload = {
            "status": augment_result.get("status"),
            "cached": augment_result.get("status") == "cached",
            "status_code": augment_result.get("status_code"),
            "reason": augment_result.get("reason"),
            "note": augment_result.get("note"),
        }
        endpoint_dir = augment_dir / spec_id
        if endpoint_dir.exists():
            augment_payload["meta"] = _load_json(endpoint_dir / "meta.json")
            augment_payload["request"] = _load_json(endpoint_dir / "request.json")
            augment_payload["request_resolution"] = _load_json(endpoint_dir / "request_resolution.json")
            augment_payload["raw"] = _load_json(endpoint_dir / "raw.json")
            error_payload = _load_json(endpoint_dir / "error.json")
            if not error_payload:
                error_payload = _load_json(endpoint_dir / "error_success.json")
            if not error_payload:
                error_payload = _load_json(endpoint_dir / "error_probe.json")
            augment_payload["error"] = error_payload
            augment_payload["empty"] = _load_json(endpoint_dir / "empty.json")

        smoke_results = [item for item in smoke_results_all if item.get("id") == spec_id]
        details[spec_id] = {
            "spec": {
                "id": spec_id,
                "name": spec.get("name"),
                "path": spec.get("path"),
                "section": spec.get("section"),
                "category": spec.get("category"),
                "subcategory": spec.get("subcategory"),
                "domains": spec.get("domains"),
                "status": (_as_object(spec.get("metadata")) or {}).get("status"),
                "source_path": spec.get("source_path"),
            },
            "augment": augment_payload,
            "smoke": {
                "results": smoke_results,
                "request": smoke_requests.get(spec_id),
            },
        }
    return details


def _build_override_lifecycle(
    overrides_payload: JsonObject,
    inference_base: JsonObject,
    inference: JsonObject,
    augment_dir: Path,
) -> JsonObject:
    override_entries = _as_list(overrides_payload.get("overrides"))
    base_endpoints = _as_object(inference_base.get("endpoints")) or {}
    applied_endpoints = _as_object(inference.get("endpoints")) or {}

    details: list[JsonObject] = []
    summary = {"active": 0, "redundant": 0, "blocked": 0, "missing": 0}

    for entry in override_entries:
        override_id_raw = entry.get("id")
        if override_id_raw is None:
            continue
        override_id = str(override_id_raw)
        base = base_endpoints.get(override_id)
        applied = applied_endpoints.get(override_id)
        meta = _load_json(augment_dir / override_id / "meta.json")
        raw_path = augment_dir / override_id / "raw.json"
        empty_sample = False
        if meta.get("empty") is True:
            empty_sample = True
        if not raw_path.exists():
            empty_sample = True

        if base is None or applied is None:
            status = "missing"
            summary["missing"] += 1
        elif base == applied:
            status = "redundant"
            summary["redundant"] += 1
        elif empty_sample:
            status = "blocked"
            summary["blocked"] += 1
        else:
            status = "active"
            summary["active"] += 1

        details.append(
            {
                "id": override_id,
                "status": status,
                "approved_by": entry.get("approved_by"),
                "approved_at": entry.get("approved_at"),
                "reason": entry.get("reason"),
                "evidence": entry.get("evidence"),
                "changes": entry.get("changes"),
                "empty_sample": empty_sample,
            }
        )

    return cast(JsonObject, {"summary": summary, "details": details})


def _load_json(path: Path) -> JsonObject:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _load_yaml(path: Path) -> JsonObject:
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = yaml.safe_load(handle) or {}
        if isinstance(payload, dict):
            return payload
    except Exception:
        return {}
    return {}


def _as_object(value: JsonValue | None) -> JsonObject | None:
    if isinstance(value, dict):
        return cast(JsonObject, value)
    return None


def _as_list(value: JsonValue | None) -> list[JsonObject]:
    if isinstance(value, list):
        return [cast(JsonObject, item) for item in value if isinstance(item, dict)]
    return []


def _write_api_report_markdown(report_dir: Path, report: JsonObject) -> Path:
    context = _build_api_report_markdown_context(report)
    markdown = render_template("api_report.md.jinja", **context)
    path = report_dir / "api_report.md"
    path.write_text(markdown, encoding="utf-8")
    return path


def _build_api_report_markdown_context(report: JsonObject) -> dict[str, object]:
    generated_at = _as_text(report.get("generated_at"))
    title_date = _iso_date(generated_at)
    runtime = _as_object(report.get("runtime")) or {}
    python_version = _as_text(runtime.get("python"))

    summary = _as_object(report.get("summary")) or {}
    scope = _as_object(report.get("scope")) or {}
    smoke = _as_object(report.get("smoke")) or {}
    overrides = _as_object(report.get("overrides")) or {}
    exclusions = _as_object(report.get("exclusions")) or {}
    other_exclusion = _as_object(exclusions.get("other")) or {}

    metadata_rows = _build_kv_rows(
        [
            ("생성 시각 (UTC)", generated_at),
            ("Python", python_version),
        ]
    )

    summary_rows = _build_kv_rows(
        [
            ("Scan", _format_counts(summary.get("scan"), ("total_issues", "errors", "warnings"))),
            ("Normalize", _format_counts(summary.get("normalize"), ("total_issues", "errors", "warnings"))),
            (
                "Augment",
                _format_counts(summary.get("augment"), ("total", "processed", "ok", "cached", "skipped", "errors")),
            ),
            ("Validation", _format_counts(summary.get("validation"), ("total", "errors"))),
            ("Smoke", _format_counts(smoke.get("summary"), ("total", "errors", "warnings"))),
            (
                "Attention",
                _format_counts(summary.get("attention"), ("warnings", "errors")),
            ),
            (
                "Override Lifecycle",
                _format_counts(
                    summary.get("override_lifecycle"),
                    ("active", "redundant", "blocked", "missing"),
                ),
            ),
        ]
    )

    scope_rows = _build_kv_rows(
        [
            ("Docs parsed", _format_value(scope.get("docs_parsed"))),
            ("API targets", _format_value(scope.get("api_targets"))),
            ("Excluded (OAuth)", _format_value(_deep_get(scope, "excluded", "oauth"))),
            ("Excluded (Realtime)", _format_value(_deep_get(scope, "excluded", "realtime"))),
            ("Excluded (Other)", _format_value(_deep_get(scope, "excluded", "other"))),
        ]
    )

    exclusion_summary_rows = _build_exclusion_summary_rows(other_exclusion)
    exclusion_detail_rows = _build_exclusion_detail_rows(other_exclusion)

    smoke_warning_details = _build_smoke_detail_rows(_as_list(smoke.get("warnings")))
    smoke_error_details = _build_smoke_detail_rows(_as_list(smoke.get("errors")))
    smoke_warning_summary_rows = _build_smoke_summary_rows(smoke_warning_details)
    smoke_error_summary_rows = _build_smoke_summary_rows(smoke_error_details)
    smoke_error_messages = _build_smoke_message_rows(smoke_error_details)

    override_details = _as_list(overrides.get("details"))
    override_summary = _as_object(overrides.get("summary")) or {}
    override_summary_rows = _build_kv_rows(
        [
            ("Active", _format_value(override_summary.get("active"))),
            ("Redundant", _format_value(override_summary.get("redundant"))),
            ("Blocked", _format_value(override_summary.get("blocked"))),
            ("Missing", _format_value(override_summary.get("missing"))),
        ]
    )
    override_redundant_rows = _build_override_rows(override_details, "redundant")
    override_blocked_rows = _build_override_rows(override_details, "blocked")
    override_missing_rows = _build_override_rows(override_details, "missing")

    sources_rows = _build_sources_rows(_as_object(report.get("sources")) or {})

    return {
        "title_date": title_date or "unknown",
        "metadata_rows": metadata_rows,
        "summary_rows": summary_rows,
        "scope_rows": scope_rows,
        "exclusion_summary_rows": exclusion_summary_rows,
        "exclusion_detail_rows": exclusion_detail_rows,
        "smoke_warning_summary_rows": smoke_warning_summary_rows,
        "smoke_warning_details": smoke_warning_details,
        "smoke_error_summary_rows": smoke_error_summary_rows,
        "smoke_error_details": smoke_error_details,
        "smoke_error_messages": smoke_error_messages,
        "override_summary_rows": override_summary_rows,
        "override_redundant_rows": override_redundant_rows,
        "override_blocked_rows": override_blocked_rows,
        "override_missing_rows": override_missing_rows,
        "sources_rows": sources_rows,
    }


def _iso_date(value: str) -> str:
    if not value:
        return ""
    if "T" in value:
        return value.split("T", 1)[0]
    return value[:10]


def _as_text(value: JsonValue | None) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _format_value(value: JsonValue | None) -> str:
    if value is None:
        return "-"
    if isinstance(value, str):
        return value.strip() or "-"
    return str(value)


def _format_counts(value: JsonValue | None, keys: tuple[str, ...]) -> str:
    payload = _as_object(value) or {}
    parts = []
    for key in keys:
        if key in payload:
            parts.append(f"{key}={payload[key]}")
    return " ".join(parts) if parts else "-"


def _table_text(value: str) -> str:
    text = value.replace("|", "\\|").replace("\n", " ").strip()
    return text if text else "-"


def _table_value(value: JsonValue | None) -> str:
    return _table_text(_format_value(value))


def _compact_text(value: str, max_len: int = 160) -> str:
    text = " ".join(value.split())
    if not text:
        return "-"
    if len(text) <= max_len:
        return text
    return f"{text[: max_len - 3]}..."


def _build_kv_rows(items: list[tuple[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for label, value in items:
        if not label:
            continue
        rows.append({"label": label, "value": value or "-"})
    return rows


def _build_exclusion_summary_rows(other_exclusion: JsonObject) -> list[dict[str, str]]:
    summary = _as_object(other_exclusion.get("summary")) or {}
    rows: list[dict[str, str]] = []
    for reason, count in sorted(summary.items(), key=lambda item: (-_to_int(item[1]), str(item[0]))):
        reason_text = _as_text(reason)
        rows.append(
            {
                "reason": reason_text,
                "count": str(_to_int(count)),
                "note": _exclusion_note(reason_text),
            }
        )
    return rows


def _build_exclusion_detail_rows(other_exclusion: JsonObject) -> list[dict[str, str]]:
    details = _as_list(other_exclusion.get("details"))
    rows: list[dict[str, str]] = []
    for item in details:
        reason = _as_text(item.get("reason"))
        rows.append(
            {
                "id": _table_value(item.get("id")),
                "name": _table_value(item.get("name")),
                "reason": _table_text(reason or "-"),
                "source": _table_value(item.get("source") or item.get("path")),
                "action": _table_text(_exclusion_action(reason)),
            }
        )
    rows.sort(key=lambda row: (row["reason"], row["id"]))
    return rows


def _exclusion_note(reason: str) -> str:
    if reason == "missing_domain":
        return "실전/모의 도메인 누락"
    if reason.startswith("status="):
        return "문서 상태가 RUNNING 아님"
    if reason == "parse_error":
        return "문서 파싱 오류"
    if reason == "normalize_error":
        return "정규화 실패"
    return "-"


def _exclusion_action(reason: str) -> str:
    if reason == "missing_domain":
        return "문서 도메인 확인"
    if reason.startswith("status="):
        return "상태 확인 후 제외 유지/복원 결정"
    if reason in {"parse_error", "normalize_error"}:
        return "문서 YAML 수정"
    return "검토 필요"


def _build_smoke_summary_rows(items: list[dict[str, str]]) -> list[dict[str, str]]:
    counts: dict[str, int] = {}
    for item in items:
        reason = item.get("reason_key", "").strip() or item.get("reason", "").strip() or "unknown"
        counts[reason] = counts.get(reason, 0) + 1
    rows: list[dict[str, str]] = []
    for reason, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        rows.append(
            {
                "reason": _table_text(reason),
                "count": str(count),
                "note": _table_text(_smoke_reason_note(reason)),
            }
        )
    return rows


def _build_smoke_detail_rows(items: list[JsonObject]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in items:
        reason_full = _as_text(item.get("reason"))
        reason_key = _normalize_smoke_reason(reason_full)
        reason_short = _compact_text(reason_full)
        rows.append(
            {
                "id": _table_value(item.get("id")),
                "name": _table_value(item.get("name")),
                "domain": _table_value(item.get("domain")),
                "reason": _table_text(reason_short),
                "reason_full": reason_full,
                "reason_key": reason_key,
                "status": _table_value(item.get("status")),
                "attempt": _table_value(item.get("attempt")),
                "status_code": _table_value(item.get("status_code")),
                "path": _table_value(item.get("path")),
            }
        )
    rows.sort(key=lambda row: (row["reason"], row["id"]))
    return rows


def _smoke_reason_note(reason: str) -> str:
    if reason == "empty_response":
        return "빈 응답/출력 없음"
    if reason == "missing_rt_cd":
        return "rt_cd 누락"
    if reason == "rt_cd=1":
        return "rt_cd=1 오류 응답"
    if reason.startswith("missing_required"):
        return "필수 파라미터 누락"
    if reason.startswith("request transport error"):
        return "전송/네트워크 오류"
    return "-"


def _normalize_smoke_reason(reason: str) -> str:
    text = reason.strip()
    if not text:
        return "unknown"
    if "validation errors" in text:
        return "validation_error"
    if text.startswith("missing_required"):
        return "missing_required"
    if text.startswith("request transport error"):
        return "request_transport_error"
    if text.startswith("rt_cd="):
        return text
    return text.splitlines()[0].strip() or "unknown"


def _build_smoke_message_rows(items: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in items:
        reason_full = item.get("reason_full", "")
        if not reason_full:
            continue
        if len(reason_full) <= 160 and "\n" not in reason_full:
            continue
        rows.append(
            {
                "id": item.get("id", "-"),
                "name": item.get("name", "-"),
                "domain": item.get("domain", "-"),
                "path": item.get("path", "-"),
                "reason": reason_full,
            }
        )
    rows.sort(key=lambda row: (row["id"], row["domain"]))
    return rows


def _build_override_rows(details: list[JsonObject], status: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for entry in details:
        if entry.get("status") != status:
            continue
        rows.append(
            {
                "id": _table_value(entry.get("id")),
                "reason": _table_value(entry.get("reason")),
                "change_summary": _table_text(_summarize_changes(_as_object(entry.get("changes")))),
                "approved_at": _table_value(entry.get("approved_at")),
                "evidence": _table_value(entry.get("evidence")),
                "action": _table_text(_override_action(status, entry)),
            }
        )
    rows.sort(key=lambda row: row["id"])
    return rows


def _summarize_changes(changes: JsonObject | None) -> str:
    if not changes:
        return "-"
    keys = [str(key) for key in changes.keys()]
    if not keys:
        return "-"
    keys.sort()
    if len(keys) <= 3:
        return ", ".join(keys)
    return f"{', '.join(keys[:3])} +{len(keys) - 3}"


def _override_action(status: str, entry: JsonObject) -> str:
    if status == "redundant":
        return "override 제거 후보"
    if status == "blocked":
        return "샘플 확보 후 재검증"
    if status == "missing":
        return "추론 결과/샘플 확인"
    if entry.get("empty_sample"):
        return "샘플 확보 후 재검증"
    return "검토 필요"


def _build_sources_rows(sources: JsonObject) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for key, value in sorted(sources.items(), key=lambda item: item[0]):
        rows.append({"label": key, "value": _table_value(value)})
    return rows


def _deep_get(payload: JsonObject, *keys: str) -> JsonValue | None:
    current: JsonValue | None = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _to_int(value: JsonValue | None) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return 0
        try:
            return int(text)
        except ValueError:
            return 0
    return 0


def _extract_ids(specs: list[JsonObject]) -> list[str]:
    ids: list[str] = []
    for spec in specs:
        spec_id = spec.get("id")
        if spec_id is not None:
            ids.append(str(spec_id))
    return ids


def _normalize_label(value: JsonValue | None) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _is_oauth_spec(spec: JsonObject) -> bool:
    section = _normalize_label(spec.get("section"))
    category = _normalize_label(spec.get("category"))
    subcategory = _normalize_label(spec.get("subcategory"))
    path = _normalize_label(spec.get("path"))
    if section in OAUTH_SECTIONS:
        return True
    if category in OAUTH_SECTIONS:
        return True
    if subcategory in OAUTH_SUBCATEGORIES:
        return True
    return any(path.startswith(prefix) for prefix in EXCLUDED_PATH_PREFIXES)


def _is_realtime_spec(spec: JsonObject) -> bool:
    section = _normalize_label(spec.get("section"))
    category = _normalize_label(spec.get("category"))
    subcategory = _normalize_label(spec.get("subcategory"))
    if "실시간시세" in section:
        return True
    if "실시간시세" in category:
        return True
    return subcategory in REALTIME_SUBCATEGORIES
