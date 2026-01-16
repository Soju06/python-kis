from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from codegen.api.models import EndpointSpec
from codegen.api.report_models import SmokeReport, SmokeResult
from codegen.api.runtime import (
    UNSAFE_KEYWORDS,
    ValueResolver,
    build_payload,
    is_empty_payload,
    load_overrides,
)
from codegen.core.types import JsonObject, JsonValue
from pykis.api.client import SyncKisRawClient
from pykis.api.errors import KisResponseError
from pykis.raw.types import Endpoint


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
) -> SmokeReport:
    overrides = load_overrides(overrides_path)
    resolvers = {
        "demo": ValueResolver(demo_client, overrides),
        "real": ValueResolver(real_client, overrides),
    }
    results: list[SmokeResult] = []
    errors = 0

    for spec in specs:
        endpoint = registry.get(spec.id)
        if endpoint is None:
            errors += 1
            results.append(SmokeResult(id=spec.id, status="missing_endpoint"))
            continue
        if not _is_read_only(spec):
            results.append(SmokeResult(id=spec.id, status="skipped", reason="not_read_only"))
            continue

        for domain, client in (("demo", demo_client), ("real", real_client)):
            if domain == "demo" and not spec.domains.demo:
                results.append(SmokeResult(id=spec.id, domain=domain, status="skipped", reason="demo_only"))
                continue
            if domain == "real" and not spec.domains.real:
                results.append(SmokeResult(id=spec.id, domain=domain, status="skipped", reason="real_only"))
                continue

            resolver = resolvers[domain]
            query, query_missing = build_payload(spec, resolver, "query", spec.request.query)
            body, body_missing = build_payload(spec, resolver, "body", spec.request.body)
            missing = query_missing + body_missing
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
                if rt_cd is False or str(rt_cd) in {"0", "OK"}:
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

                payload = None
                try:
                    payload = _coerce_payload(raw.json())
                except Exception:  # noqa: BLE001
                    payload = None
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
    return report
