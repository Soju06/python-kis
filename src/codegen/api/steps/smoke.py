from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from codegen.api.models import EndpointSpec
from codegen.api.report_models import SmokeReport, SmokeResult
from codegen.api.runtime import (
    SKIP_ENDPOINT_IDS,
    UNSAFE_KEYWORDS,
    ValueResolver,
    build_payload_with_trace,
    is_empty_payload,
    load_overrides,
)
from codegen.core.types import JsonObject, JsonValue
from pykis.api.client import SyncKisRawClient
from pykis.api.errors import KisResponseError
from pykis.api.raw.types import Endpoint


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

            for attempt in range(2):
                try:
                    response, raw = client.call(endpoint, request_payload)
                except KisResponseError as exc:
                    payload = _coerce_payload(exc.payload)
                    if is_empty_payload(payload):
                        results.append(
                            SmokeResult(
                                id=spec.id,
                                domain=domain,
                                attempt=attempt + 1,
                                status="skipped",
                                reason="empty_response",
                            )
                        )
                        continue
                    errors += 1
                    results.append(
                        SmokeResult(
                            id=spec.id,
                            domain=domain,
                            attempt=attempt + 1,
                            status="error",
                            reason=str(exc),
                        )
                    )
                    continue
                except Exception as exc:  # noqa: BLE001
                    errors += 1
                    results.append(
                        SmokeResult(
                            id=spec.id,
                            domain=domain,
                            attempt=attempt + 1,
                            status="error",
                            reason=str(exc),
                        )
                    )
                    continue

                rt_cd = getattr(response, "rt_cd", None)
                rt_cd_value = None if rt_cd is None else str(rt_cd)
                if rt_cd is False or rt_cd_value in {"0", "OK"}:
                    results.append(
                        SmokeResult(
                            id=spec.id,
                            domain=domain,
                            attempt=attempt + 1,
                            status="ok",
                            status_code=raw.status_code,
                        )
                    )
                    continue
                if rt_cd_value is None:
                    errors += 1
                    results.append(
                        SmokeResult(
                            id=spec.id,
                            domain=domain,
                            attempt=attempt + 1,
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
                    errors += 1
                    results.append(
                        SmokeResult(
                            id=spec.id,
                            domain=domain,
                            attempt=attempt + 1,
                            status="error",
                            reason="rt_cd=1",
                        )
                    )
                    continue
                if is_empty_payload(payload):
                    results.append(
                        SmokeResult(
                            id=spec.id,
                            domain=domain,
                            attempt=attempt + 1,
                            status="skipped",
                            reason="empty_response",
                        )
                    )
                    continue

                errors += 1
                results.append(
                    SmokeResult(
                        id=spec.id,
                        domain=domain,
                        attempt=attempt + 1,
                        status="error",
                        reason=f"rt_cd={rt_cd!r}",
                    )
                )

    report = SmokeReport(total=len(results), errors=errors, results=results)
    out_path.write_text(json.dumps(report.model_dump(), ensure_ascii=False, indent=2), encoding="utf-8")
    detail_out_path.write_text(json.dumps(request_details, ensure_ascii=False, indent=2), encoding="utf-8")
    return report
