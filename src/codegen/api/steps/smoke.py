from __future__ import annotations

import json
from pathlib import Path
from typing import cast

from pydantic import ValidationError

from codegen.api.models import EndpointSpec
from codegen.api.report_models import SmokeReport, SmokeResult
from codegen.api.runtime import (
    SKIP_ENDPOINT_IDS,
    UNSAFE_KEYWORDS,
    ValueResolver,
    build_payload_with_trace,
    is_empty_payload,
    is_nonfatal_server_error,
    load_overrides,
)
from codegen.core.types import JsonObject, JsonValue
from pykis.api.client import SyncKisRawClient
from pykis.api.errors import KisResponseError
from pykis.api.raw.types import Endpoint

SENTINEL_VALUES = {
    "",
    "0",
    "0.0",
    "0.00",
    "000000",
    "00:00:00",
    "888888",
    "00000000",
    "0000-00-00",
    "null",
    "NULL",
    "nan",
    "-nan",
    "NaN",
    "-NaN",
}
SENTINEL_MIN_FIELDS = 8
SENTINEL_DICT_RATIO = 0.75
SENTINEL_LIST_FIELD_RATIO = 0.85
SENTINEL_LIST_OVERALL_RATIO = 0.45
SENTINEL_LIST_MIN_FIELDS = 4
SENTINEL_ROW_SCAN_LIMIT = 30
DEFAULT_MAX_ATTEMPTS = 2
NONFATAL_MAX_ATTEMPTS = 4
_SENTINEL_IGNORE_FIELDS_BY_ENDPOINT = {
    "b73a4cdf-402b-4e11-a161-609ea9451835": {
        *(f"iscd{index}" for index in range(2, 11)),
        *(f"kor_isnm{index}" for index in range(2, 11)),
    },
    "fbfe7300-7096-4938-840b-9f7c328cc5fd": {
        *(f"iscd{index}" for index in range(2, 11)),
        *(f"kor_isnm{index}" for index in range(2, 11)),
    },
}


def _is_read_only(spec: EndpointSpec) -> bool:
    if spec.method != "GET":
        return False
    haystack = " ".join(filter(None, [spec.name, spec.section, spec.category, spec.subcategory, spec.path])).lower()
    return not any(keyword.lower() in haystack for keyword in UNSAFE_KEYWORDS)


def _coerce_json_value(value: object) -> JsonValue:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [_coerce_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _coerce_json_value(item) for key, item in value.items()}
    return str(value)


def _coerce_payload(payload: object | None) -> JsonObject | None:
    if not isinstance(payload, dict):
        return None
    return {str(key): _coerce_json_value(value) for key, value in payload.items()}


def _normalize_scalar(value: JsonValue | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip()
    return str(value)


def _is_sentinel_value(value: JsonValue | None) -> bool:
    normalized = _normalize_scalar(value)
    return normalized in SENTINEL_VALUES


def _as_output_rows(value: JsonValue | None) -> list[JsonObject]:
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def _primary_output_code(spec: EndpointSpec) -> str:
    if spec.response.outputs:
        return spec.response.outputs[0].code
    return "output"


def _is_sentinel_ignored_field(endpoint_id: str, field: str) -> bool:
    ignored = _SENTINEL_IGNORE_FIELDS_BY_ENDPOINT.get(endpoint_id)
    if not ignored:
        return False
    return field in ignored


def _detect_sentinel_success(spec: EndpointSpec, payload: JsonObject | None) -> JsonObject | None:
    if not payload:
        return None

    output_code = _primary_output_code(spec)
    container: JsonValue | None = payload.get(output_code)
    if container is None and output_code != "output":
        container = payload.get("output")
        if container is None:
            return None
        output_code = "output"

    rows = _as_output_rows(container)
    if not rows:
        return None
    sample_rows = rows[:SENTINEL_ROW_SCAN_LIMIT]

    first_row = sample_rows[0]
    scalar_fields = [field for field, value in first_row.items() if not isinstance(value, (dict, list))]
    scalar_fields = [field for field in scalar_fields if not _is_sentinel_ignored_field(spec.id, field)]
    if len(scalar_fields) < SENTINEL_MIN_FIELDS:
        return None

    sentinel_fields: list[str] = []
    if len(sample_rows) == 1:
        sentinel_fields = [field for field in scalar_fields if _is_sentinel_value(first_row.get(field))]
        sentinel_ratio = len(sentinel_fields) / len(scalar_fields)
        if sentinel_ratio < SENTINEL_DICT_RATIO:
            return None
    else:
        for field in scalar_fields:
            sentinel_count = sum(1 for row in sample_rows if _is_sentinel_value(row.get(field)))
            field_ratio = sentinel_count / len(sample_rows)
            if field_ratio >= SENTINEL_LIST_FIELD_RATIO:
                sentinel_fields.append(field)
        sentinel_ratio = len(sentinel_fields) / len(scalar_fields)
        if len(sentinel_fields) < SENTINEL_LIST_MIN_FIELDS:
            return None
        if sentinel_ratio < SENTINEL_LIST_OVERALL_RATIO:
            return None

    return cast(
        JsonObject,
        {
            "output": output_code,
            "sentinel_ratio": round(sentinel_ratio, 2),
            "fields": sentinel_fields[:8],
            "rows": len(sample_rows),
        },
    )


def run_smoke(
    specs: list[EndpointSpec],
    registry: dict[str, Endpoint],
    demo_client: SyncKisRawClient,
    real_client: SyncKisRawClient,
    overrides_path: Path,
    out_path: Path,
    detail_out_path: Path | None = None,
) -> SmokeReport:
    overrides = load_overrides(overrides_path)
    resolvers = {
        "demo": ValueResolver(demo_client, overrides),
        "real": ValueResolver(real_client, overrides),
    }
    results: list[SmokeResult] = []
    errors = 0
    detail_out_path = detail_out_path or out_path.with_name("smoke_requests.json")
    request_details: dict[str, JsonObject] = {}

    for spec in specs:
        if spec.id in SKIP_ENDPOINT_IDS:
            results.append(SmokeResult(id=spec.id, status="skipped", reason="skip_endpoint"))
            continue
        endpoint = registry.get(spec.id)
        if endpoint is None:
            errors += 1
            results.append(SmokeResult(id=spec.id, status="missing_endpoint"))
            continue
        if not _is_read_only(spec):
            results.append(SmokeResult(id=spec.id, status="skipped", reason="not_read_only"))
            continue

        domains: list[tuple[str, SyncKisRawClient]] = []
        if spec.domains.demo:
            domains.append(("demo", demo_client))
        if spec.domains.real:
            domains.append(("real", real_client))
        if not domains:
            results.append(SmokeResult(id=spec.id, status="skipped", reason="no_domain"))
            continue

        for domain, client in domains:
            resolver = resolvers[domain]
            query, query_missing, query_trace = build_payload_with_trace(spec, resolver, "query", spec.request.query)
            body, body_missing, body_trace = build_payload_with_trace(spec, resolver, "body", spec.request.body)
            missing = query_missing + body_missing
            request_details.setdefault(spec.id, {})[domain] = {
                "query": query,
                "body": body,
                "resolution": {
                    "query": query_trace,
                    "body": body_trace,
                    "missing_required": missing,
                },
            }
            if missing:
                errors += 1
                results.append(
                    SmokeResult(
                        id=spec.id,
                        domain=domain,
                        status="error",
                        reason=f"missing_required: {missing}",
                    )
                )
                continue

            request_payload: JsonObject = {**query, **body}
            try:
                endpoint.request_model.model_validate(request_payload)
            except ValidationError as exc:
                errors += 1
                results.append(SmokeResult(id=spec.id, domain=domain, status="error", reason=str(exc)))
                continue

            attempt_errors: list[SmokeResult] = []
            attempt_skips: list[SmokeResult] = []
            ok_result: SmokeResult | None = None
            sentinel_probe: JsonObject | None = None

            max_attempts = DEFAULT_MAX_ATTEMPTS
            attempt = 0
            while attempt < max_attempts:
                attempt += 1
                try:
                    response, raw = client.call(endpoint, request_payload)
                except KisResponseError as exc:
                    payload = _coerce_payload(exc.payload)
                    if is_nonfatal_server_error(spec.id, payload, str(exc)):
                        attempt_skips.append(
                            SmokeResult(
                                id=spec.id,
                                domain=domain,
                                attempt=attempt,
                                status="skipped",
                                reason="nonfatal_server_error",
                            )
                        )
                        if max_attempts < NONFATAL_MAX_ATTEMPTS:
                            max_attempts = NONFATAL_MAX_ATTEMPTS
                        continue
                    if is_empty_payload(payload):
                        attempt_skips.append(
                            SmokeResult(
                                id=spec.id,
                                domain=domain,
                                attempt=attempt,
                                status="skipped",
                                reason="empty_response",
                            )
                        )
                        continue
                    attempt_errors.append(
                        SmokeResult(
                            id=spec.id,
                            domain=domain,
                            attempt=attempt,
                            status="error",
                            reason=str(exc),
                        )
                    )
                    continue
                except Exception as exc:  # noqa: BLE001
                    attempt_errors.append(
                        SmokeResult(
                            id=spec.id,
                            domain=domain,
                            attempt=attempt,
                            status="error",
                            reason=str(exc),
                        )
                    )
                    continue

                rt_cd = getattr(response, "rt_cd", None)
                rt_cd_value = None if rt_cd is None else str(rt_cd)
                if rt_cd is False or rt_cd_value in {"0", "OK"}:
                    payload = None
                    try:
                        payload = _coerce_payload(raw.json())
                    except Exception:  # noqa: BLE001
                        payload = None
                    sentinel_probe = _detect_sentinel_success(spec, payload)
                    if sentinel_probe is not None:
                        attempt_skips.append(
                            SmokeResult(
                                id=spec.id,
                                domain=domain,
                                attempt=attempt,
                                status="skipped",
                                reason="sentinel_success",
                                status_code=raw.status_code,
                            )
                        )
                        continue
                    ok_result = SmokeResult(
                        id=spec.id,
                        domain=domain,
                        attempt=attempt,
                        status="ok",
                        status_code=raw.status_code,
                    )
                    break
                if rt_cd_value is None:
                    attempt_errors.append(
                        SmokeResult(
                            id=spec.id,
                            domain=domain,
                            attempt=attempt,
                            status="error",
                            reason="missing_rt_cd",
                        )
                    )
                    continue

                payload = None
                try:
                    payload = _coerce_payload(raw.json())
                except Exception:  # noqa: BLE001
                    payload = None
                if rt_cd_value == "1":
                    attempt_errors.append(
                        SmokeResult(
                            id=spec.id,
                            domain=domain,
                            attempt=attempt,
                            status="error",
                            reason="rt_cd=1",
                        )
                    )
                    continue
                if is_empty_payload(payload):
                    attempt_skips.append(
                        SmokeResult(
                            id=spec.id,
                            domain=domain,
                            attempt=attempt,
                            status="skipped",
                            reason="empty_response",
                        )
                    )
                    continue

                attempt_errors.append(
                    SmokeResult(
                        id=spec.id,
                        domain=domain,
                        attempt=attempt,
                        status="error",
                        reason=f"rt_cd={rt_cd!r}",
                    )
                )

            if ok_result is not None:
                results.append(ok_result)
                continue
            if attempt_errors:
                errors += 1
                results.append(attempt_errors[-1])
                continue
            if attempt_skips:
                if sentinel_probe is not None:
                    domain_details = request_details.setdefault(spec.id, {}).setdefault(domain, {})
                    domain_details["sentinel_probe"] = sentinel_probe
                results.append(attempt_skips[-1])
                continue

            errors += 1
            results.append(
                SmokeResult(
                    id=spec.id,
                    domain=domain,
                    status="error",
                    reason="no_attempt_result",
                )
            )

    report = SmokeReport(total=len(results), errors=errors, results=results)
    out_path.write_text(json.dumps(report.model_dump(), ensure_ascii=False, indent=2), encoding="utf-8")
    detail_out_path.write_text(json.dumps(request_details, ensure_ascii=False, indent=2), encoding="utf-8")
    return report
