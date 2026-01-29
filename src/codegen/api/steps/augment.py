from __future__ import annotations

import hashlib
import json
import logging
from datetime import date, datetime, time
from decimal import Decimal
from pathlib import Path
from typing import Mapping, cast
from urllib.parse import urljoin

from pydantic import ValidationError

from codegen.api.models import EndpointSpec
from codegen.api.overrides import AugmentOverrides
from codegen.api.report_models import (
    AugmentEndpointResult,
    AugmentMeta,
    AugmentRequestPayload,
    AugmentSummary,
    MultiScenarioReport,
    ScenarioResult,
)
from codegen.api.runtime import (
    SKIP_ENDPOINT_IDS,
    UNSAFE_KEYWORDS,
    ValueResolver,
    build_payload_with_trace,
    is_empty_payload,
    load_overrides,
)
from codegen.api.scenarios import AugmentScenario
from codegen.core.types import JsonObject, JsonValue
from pykis.api.client import SyncKisRawClient
from pykis.api.raw.types import Endpoint

logger = logging.getLogger("pykis.codegen.augment")


def _apply_output_alias(payload: JsonObject, endpoint: EndpointSpec) -> JsonObject:
    output_codes = {output.code for output in endpoint.response.outputs}
    if "output" in payload and "output" not in output_codes and len(output_codes) == 1:
        only_code = next(iter(output_codes))
        if only_code not in payload:
            payload = dict(payload)
            payload[only_code] = payload["output"]
    return payload


def _outputs_empty(payload: JsonObject, endpoint: EndpointSpec) -> bool:
    outputs = endpoint.response.outputs
    if not outputs:
        return False
    for output in outputs:
        container = payload.get(output.code)
        if container is None and "output" in payload and len(outputs) == 1:
            container = payload.get("output")
        if isinstance(container, list):
            if container:
                return False
            continue
        if isinstance(container, dict):
            if container:
                return False
            continue
        return False
    return True


def _response_ok(response: object) -> bool:
    is_success = getattr(response, "is_success", None)
    if isinstance(is_success, bool):
        return is_success
    ok = getattr(response, "ok", None)
    if isinstance(ok, bool):
        return ok
    return False


SKIP_PATHS = {"/oauth2/revokeP", "/oauth2/tokenP", "/uapi/hashkey"}


def _fingerprint(
    spec: EndpointSpec,
    overrides: AugmentOverrides,
    domain: str,
    *,
    scenario_id: str,
    request_template: str | None,
    template_values: Mapping[str, JsonValue] | None,
) -> str:
    payload = {
        "spec": spec.model_dump(),
        "overrides": overrides.model_dump(by_alias=True),
        "domain": domain,
        "scenario": scenario_id,
        "request_template": request_template,
        "template_values": template_values or {},
        "augment_version": 3,
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _json_default(value: object) -> object:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    return str(value)


def _dump_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=_json_default),
        encoding="utf-8",
    )


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
    normalized: JsonObject = {}
    for key, value in payload.items():
        normalized[str(key)] = _coerce_json_value(value)
    return normalized


def _coerce_query_params(payload: JsonObject) -> dict[str, str | int | float | None]:
    params: dict[str, str | int | float | None] = {}
    for key, value in payload.items():
        if value is None:
            params[str(key)] = None
        elif isinstance(value, (str, int, float)):
            params[str(key)] = value
        else:
            params[str(key)] = str(value)
    return params


def _select_tr_id(endpoint: EndpointSpec, domain: str) -> str | None:
    if domain == "demo" and endpoint.demo_tr_id:
        return endpoint.demo_tr_id
    if domain == "real" and endpoint.real_tr_id:
        return endpoint.real_tr_id
    return None


def _scenario_suffix(scenario_id: str) -> str:
    return "" if scenario_id == "success" else f"_{scenario_id}"


def _resolve_request_template(
    endpoint: EndpointSpec,
    scenario: AugmentScenario,
    request_templates: Mapping[str, Mapping[str, Mapping[str, JsonValue]]] | None,
) -> Mapping[str, JsonValue] | None:
    if not scenario.request_template:
        return None
    if not request_templates:
        return None
    endpoint_templates = request_templates.get(endpoint.id)
    if not endpoint_templates:
        return None
    return endpoint_templates.get(scenario.request_template)


def _apply_request_template(
    endpoint: EndpointSpec,
    query: dict[str, JsonValue],
    body: dict[str, JsonValue],
    template: Mapping[str, JsonValue],
    *,
    template_name: str | None,
) -> tuple[list[JsonObject], list[str]]:
    overrides: list[JsonObject] = []
    missing: list[str] = []
    query_fields = {field.code.lower(): field for field in endpoint.request.query}
    body_fields = {field.code.lower(): field for field in endpoint.request.body}

    for key, value in template.items():
        key_lower = str(key).lower()
        location = None
        field = None
        if key_lower in query_fields:
            location = "query"
            field = query_fields[key_lower]
        elif key_lower in body_fields:
            location = "body"
            field = body_fields[key_lower]
        else:
            continue

        code = field.code
        if value is None:
            if location == "query":
                query.pop(code, None)
            else:
                body.pop(code, None)
            if field.required:
                missing.append(code)
        else:
            if location == "query":
                query[code] = value
            else:
                body[code] = value

        overrides.append(
            {
                "code": code,
                "location": location,
                "value": value,
                "template": template_name,
            }
        )

    return overrides, missing


def _is_unsafe(endpoint: EndpointSpec) -> bool:
    haystack = " ".join(
        filter(None, [endpoint.name, endpoint.section, endpoint.category, endpoint.subcategory, endpoint.path])
    ).lower()
    return any(keyword.lower() in haystack for keyword in UNSAFE_KEYWORDS)


def _expected_flags(scenario: AugmentScenario | None) -> tuple[bool, bool]:
    expected = (scenario.expected or "") if scenario else ""
    expected_lower = expected.lower()
    allow_empty = "empty" in expected_lower or "sentinel" in expected_lower
    allow_error = "error" in expected_lower
    return allow_empty, allow_error


def _scenario_payload_path(result_dir: Path, scenario: AugmentScenario, outcome: str) -> Path:
    if scenario.id != "success":
        return result_dir / scenario.output_filename()
    if outcome == "empty":
        return result_dir / "empty.json"
    if outcome == "error":
        return result_dir / "error_success.json"
    return result_dir / "success.json"


def _has_cached_payload(result_dir: Path, scenario: AugmentScenario, meta: JsonObject | None) -> bool:
    if not meta or not meta.get("ok"):
        return False
    if (result_dir / scenario.output_filename()).exists():
        return True
    if scenario.id == "success":
        if meta.get("empty") and (result_dir / "empty.json").exists():
            return True
        if (result_dir / "error_success.json").exists():
            return True
    return False


def _build_headers_with_trace(
    endpoint: EndpointSpec,
    resolver: ValueResolver,
    domain: str,
) -> tuple[dict[str, str], list[str], list[JsonObject]]:
    headers: dict[str, str] = {}
    missing: list[str] = []
    traces: list[JsonObject] = []
    tr_id = _select_tr_id(endpoint, domain)

    for field in endpoint.request.headers:
        key = field.code
        key_lower = key.lower()
        value: JsonValue | None = None
        source = "missing"
        reason: str | None = None
        notes: list[str] = []

        if key_lower == "content-type":
            value = "application/json; charset=utf-8"
            key = "content-type"
            source = "system"
        elif key_lower == "authorization":
            value = "__AUTH__"
            key = "authorization"
            source = "auth_required"
        elif key_lower == "appkey":
            value, source, reason = resolver.resolve_with_source(endpoint.id, "headers", key)
            key = "appkey"
        elif key_lower == "appsecret":
            value, source, reason = resolver.resolve_with_source(endpoint.id, "headers", key)
            key = "appsecret"
        elif key_lower == "tr_id":
            value = tr_id
            key = "tr_id"
            source = "tr_id"
            if value is None:
                notes.append("missing_tr_id")
        else:
            value, source, reason = resolver.resolve_with_source(endpoint.id, "headers", key)

        if value is None:
            if field.required:
                missing.append(field.code)
            trace = cast(
                JsonObject,
                {
                    "code": field.code,
                    "location": "headers",
                    "value": None,
                    "required": field.required,
                    "used": False,
                    "source": source,
                    "notes": notes,
                },
            )
            if reason:
                trace["reason"] = reason
            traces.append(trace)
            continue

        headers[key] = str(value)
        trace = cast(
            JsonObject,
            {
                "code": field.code,
                "location": "headers",
                "value": value,
                "required": field.required,
                "used": True,
                "source": source,
                "notes": notes,
            },
        )
        if reason:
            trace["reason"] = reason
        traces.append(trace)

    return headers, missing, traces


def augment_endpoint(
    endpoint: EndpointSpec,
    endpoint_def: Endpoint,
    client: SyncKisRawClient,
    resolver: ValueResolver,
    overrides: AugmentOverrides,
    out_dir: Path,
    domain: str,
    base_url: str,
    *,
    scenario: AugmentScenario | None = None,
    request_templates: Mapping[str, Mapping[str, Mapping[str, JsonValue]]] | None = None,
) -> AugmentEndpointResult:
    if not base_url:
        return AugmentEndpointResult(id=endpoint.id, status="skipped", reason="domain_not_available")

    if base_url.startswith(("ws://", "wss://")):
        return AugmentEndpointResult(id=endpoint.id, status="skipped", reason="websocket")

    if endpoint.id in SKIP_ENDPOINT_IDS:
        return AugmentEndpointResult(id=endpoint.id, status="skipped", reason="skip_endpoint")

    if _is_unsafe(endpoint):
        return AugmentEndpointResult(id=endpoint.id, status="skipped", reason="unsafe")
    if endpoint.path in SKIP_PATHS:
        return AugmentEndpointResult(id=endpoint.id, status="skipped", reason="skip_path")

    scenario = scenario or AugmentScenario(
        id="success",
        description="Valid request with expected parameters",
        request_template="default",
        expected="valid_response",
        store_as="success.json",
    )
    scenario_id = scenario.id
    suffix = _scenario_suffix(scenario_id)
    template_values = _resolve_request_template(endpoint, scenario, request_templates)

    result_dir = out_dir / endpoint.id
    fingerprint = _fingerprint(
        endpoint,
        overrides,
        domain,
        scenario_id=scenario_id,
        request_template=scenario.request_template,
        template_values=template_values,
    )
    meta_path = result_dir / f"meta{suffix}.json"
    if meta_path.exists():
        try:
            cached_meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            cached_meta = None
        if (
            cached_meta
            and cached_meta.get("fingerprint") == fingerprint
            and _has_cached_payload(result_dir, scenario, cached_meta)
        ):
            return AugmentEndpointResult(id=endpoint.id, status="cached", scenario=scenario_id)

    headers, header_missing, header_trace = _build_headers_with_trace(endpoint, resolver, domain)
    query, query_missing, query_trace = build_payload_with_trace(endpoint, resolver, "query", endpoint.request.query)
    body, body_missing, body_trace = build_payload_with_trace(endpoint, resolver, "body", endpoint.request.body)
    scenario_overrides: list[JsonObject] = []
    scenario_missing: list[str] = []
    if template_values:
        scenario_overrides, scenario_missing = _apply_request_template(
            endpoint,
            query,
            body,
            template_values,
            template_name=scenario.request_template,
        )

    missing = header_missing + query_missing + body_missing + scenario_missing
    if header_missing:
        return AugmentEndpointResult(
            id=endpoint.id,
            status="skipped",
            reason=f"missing_required_headers: {header_missing}",
            scenario=scenario_id,
        )

    request_payload_data: JsonObject = {**query, **body}
    try:
        endpoint_def.request_model.model_validate(request_payload_data)
    except ValidationError as exc:
        logger.error("augment request validation failed: %s -> %s", endpoint.id, exc)
        raise

    response = client.request(
        method=endpoint.method,
        base_url=base_url,
        path=endpoint.path,
        headers=headers,
        params=_coerce_query_params(query) if query else None,
        body=body if body else None,
        auth_required=endpoint_def.auth_required,
        hashkey_required=endpoint_def.hashkey_required,
    )

    result_dir.mkdir(parents=True, exist_ok=True)

    request_payload = AugmentRequestPayload(
        method=endpoint.method,
        url=urljoin(base_url, endpoint.path),
        headers=headers,
        query=query,
        body=body,
    )
    request_path = result_dir / f"request{suffix}.json"
    _dump_json(request_path, request_payload.model_dump())
    _dump_json(
        result_dir / f"request_resolution{suffix}.json",
        {
            "headers": header_trace,
            "query": query_trace,
            "body": body_trace,
            "scenario_overrides": scenario_overrides,
            "missing_required": missing,
        },
    )

    ok = _response_ok(response)
    meta = AugmentMeta(
        status_code=response.status_code,
        ok=ok,
        domain=domain,
        endpoint=endpoint.id,
        missing_required=missing,
        fingerprint=fingerprint,
        scenario=scenario_id,
        request_template=scenario.request_template,
        expected=scenario.expected,
    )
    allow_empty, allow_error = _expected_flags(scenario)
    raw_path = result_dir / f"raw{suffix}.json"

    try:
        raw_payload = response.json()
    except Exception:
        raw_payload = None
    payload = _coerce_payload(raw_payload)

    if not ok:
        meta = meta.model_copy(update={"ok": False})
        error_payload = raw_payload if raw_payload is not None else {"raw": response.text}
        if raw_payload is not None:
            _dump_json(raw_path, raw_payload)
        _dump_json(meta_path, meta.model_dump())
        _dump_json(_scenario_payload_path(result_dir, scenario, "error"), error_payload)
        raise RuntimeError(f"[augment] HTTP {response.status_code} for {endpoint.id}")

    if payload is None:
        meta = meta.model_copy(update={"ok": False})
        _dump_json(meta_path, meta.model_dump())
        _dump_json(
            _scenario_payload_path(result_dir, scenario, "error"),
            raw_payload if raw_payload is not None else {"raw": response.text},
        )
        raise RuntimeError(f"[augment] invalid JSON for {endpoint.id}")

    payload = _apply_output_alias(payload, endpoint)
    _dump_json(raw_path, payload)

    if str(payload.get("rt_cd")) not in ("0", "OK"):
        if is_empty_payload(payload):
            meta = meta.model_copy(update={"ok": True, "empty": True})
            _dump_json(meta_path, meta.model_dump())
            _dump_json(_scenario_payload_path(result_dir, scenario, "empty"), payload)
            return AugmentEndpointResult(
                id=endpoint.id,
                status="ok",
                status_code=response.status_code,
                note="empty",
                scenario=scenario_id,
            )
        if allow_error:
            _dump_json(meta_path, meta.model_dump())
            _dump_json(_scenario_payload_path(result_dir, scenario, "error"), payload)
            return AugmentEndpointResult(
                id=endpoint.id,
                status="ok",
                status_code=response.status_code,
                note="rt_cd_error",
                scenario=scenario_id,
            )
        meta = meta.model_copy(update={"ok": False})
        _dump_json(meta_path, meta.model_dump())
        _dump_json(_scenario_payload_path(result_dir, scenario, "error"), payload)
        raise RuntimeError(f"[augment] rt_cd error for {endpoint.id}")

    if _outputs_empty(payload, endpoint):
        meta = meta.model_copy(update={"ok": True, "empty": True})
        _dump_json(meta_path, meta.model_dump())
        _dump_json(_scenario_payload_path(result_dir, scenario, "empty"), payload)
        return AugmentEndpointResult(
            id=endpoint.id,
            status="ok",
            status_code=response.status_code,
            note="empty",
            scenario=scenario_id,
        )

    if scenario_id == "success":
        try:
            response_model = endpoint_def.response_model.model_validate(payload)
        except ValidationError as exc:
            meta = meta.model_copy(update={"ok": False})
            _dump_json(meta_path, meta.model_dump())
            _dump_json(
                _scenario_payload_path(result_dir, scenario, "error"),
                {"validation_error": exc.errors(), "payload": payload},
            )
            raise

        _dump_json(meta_path, meta.model_dump())
        _dump_json(result_dir / "success.json", response_model.model_dump(by_alias=True))

        error_payload = _probe_error(endpoint, client, headers, query, body, base_url)
        if error_payload is not None:
            _dump_json(result_dir / "error_probe.json", error_payload)
    else:
        _dump_json(meta_path, meta.model_dump())
        _dump_json(_scenario_payload_path(result_dir, scenario, "success"), payload)

    return AugmentEndpointResult(id=endpoint.id, status="ok", status_code=response.status_code, scenario=scenario_id)


def _probe_error(
    endpoint: EndpointSpec,
    client: SyncKisRawClient,
    headers: dict[str, str],
    query: JsonObject,
    body: JsonObject,
    base_url: str,
) -> JsonObject | None:
    missing_field = None
    if endpoint.request.query:
        for field in endpoint.request.query:
            if field.required and field.code in query:
                missing_field = ("query", field.code)
                break
    if missing_field is None and endpoint.request.body:
        for field in endpoint.request.body:
            if field.required and field.code in body:
                missing_field = ("body", field.code)
                break
    if missing_field is None:
        return None

    location, code = missing_field
    query_copy = dict(query)
    body_copy = dict(body)
    if location == "query":
        query_copy.pop(code, None)
    else:
        body_copy.pop(code, None)

    response = client.request(
        method=endpoint.method,
        base_url=base_url,
        path=endpoint.path,
        headers=dict(headers),
        params=_coerce_query_params(query_copy) if query_copy else None,
        body=body_copy if body_copy else None,
        auth_required="authorization" in {h.code.lower() for h in endpoint.request.headers},
        hashkey_required="hashkey" in {h.code.lower() for h in endpoint.request.headers},
    )
    try:
        raw_payload = response.json()
    except Exception:
        return {"raw": response.text}
    payload = _coerce_payload(raw_payload)
    if payload is None:
        raw_value = _coerce_json_value(raw_payload) if raw_payload is not None else response.text
        return {"raw": raw_value}
    return payload


def run_multi_scenario_augmentation(
    specs: list[EndpointSpec],
    registry: dict[str, Endpoint],
    demo_client: SyncKisRawClient,
    real_client: SyncKisRawClient,
    overrides_path: Path,
    out_dir: Path,
    *,
    scenarios: list[AugmentScenario],
    request_templates: Mapping[str, Mapping[str, Mapping[str, JsonValue]]] | None = None,
) -> MultiScenarioReport:
    overrides = load_overrides(overrides_path)
    results: list[ScenarioResult] = []
    errors = 0
    cached = 0
    ok = 0
    skipped = 0
    resolver_demo = ValueResolver(demo_client, overrides) if demo_client else None
    resolver_real = ValueResolver(real_client, overrides) if real_client else None

    demo_auth_available = True
    needs_demo_auth = any(
        spec.domains.demo and registry[spec.id].auth_required for spec in specs if spec.id in registry
    )
    if needs_demo_auth and demo_client:
        try:
            demo_client.ensure_token()
        except Exception as exc:
            demo_auth_available = False
            logger.warning("augment demo auth unavailable: %s", exc)

    real_auth_available = True
    needs_real_auth = any(
        spec.domains.real and registry[spec.id].auth_required for spec in specs if spec.id in registry
    )
    if needs_real_auth and real_client:
        try:
            real_client.ensure_token()
        except Exception as exc:
            real_auth_available = False
            logger.warning("augment real auth unavailable: %s", exc)

    for idx, spec in enumerate(specs, start=1):
        endpoint_def = registry.get(spec.id)
        if endpoint_def is None:
            raise RuntimeError(f"[augment] missing generated endpoint for {spec.id}")

        domain = None
        client = None
        resolver = None
        base_url = ""
        if spec.domains.demo:
            domain = "demo"
            client = demo_client
            resolver = resolver_demo
            base_url = spec.domains.demo or ""
        elif spec.domains.real:
            domain = "real"
            client = real_client
            resolver = resolver_real
            base_url = spec.domains.real or ""
        else:
            for scenario in scenarios:
                skipped += 1
                results.append(
                    ScenarioResult(
                        endpoint_id=spec.id,
                        scenario=scenario.id,
                        status="skipped",
                        reason="no_domain",
                    )
                )
            continue

        if client is None or resolver is None:
            for scenario in scenarios:
                skipped += 1
                results.append(
                    ScenarioResult(
                        endpoint_id=spec.id,
                        scenario=scenario.id,
                        status="skipped",
                        reason=f"{domain}_client_unavailable",
                    )
                )
            continue

        if endpoint_def.auth_required:
            if domain == "demo" and not demo_auth_available:
                for scenario in scenarios:
                    skipped += 1
                    results.append(
                        ScenarioResult(
                            endpoint_id=spec.id,
                            scenario=scenario.id,
                            status="skipped",
                            reason="auth_unavailable",
                        )
                    )
                continue
            if domain == "real" and not real_auth_available:
                for scenario in scenarios:
                    skipped += 1
                    results.append(
                        ScenarioResult(
                            endpoint_id=spec.id,
                            scenario=scenario.id,
                            status="skipped",
                            reason="auth_unavailable",
                        )
                    )
                continue

        for scenario in scenarios:
            try:
                result = augment_endpoint(
                    spec,
                    endpoint_def,
                    client,
                    resolver,
                    overrides,
                    out_dir,
                    domain,
                    base_url,
                    scenario=scenario,
                    request_templates=request_templates,
                )
                status = result.status
                if status == "cached":
                    cached += 1
                elif status == "ok":
                    ok += 1
                elif status == "skipped":
                    skipped += 1
                results.append(
                    ScenarioResult(
                        endpoint_id=spec.id,
                        scenario=scenario.id,
                        status=status,
                        status_code=result.status_code,
                        reason=result.reason,
                        note=result.note,
                    )
                )
            except Exception as exc:
                errors += 1
                logger.error("augment error %s (%s): %s", spec.id, scenario.id, exc)
                results.append(
                    ScenarioResult(
                        endpoint_id=spec.id,
                        scenario=scenario.id,
                        status="error",
                        reason=str(exc),
                    )
                )

        if idx % 10 == 0 or idx == len(specs):
            logger.info(
                "augment scenarios progress %s/%s ok=%s cached=%s skipped=%s errors=%s",
                idx,
                len(specs),
                ok,
                cached,
                skipped,
                errors,
            )

    report = MultiScenarioReport(
        total=len(results),
        processed=len(results),
        ok=ok,
        cached=cached,
        skipped=skipped,
        errors=errors,
        results=results,
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary_multi.json").write_text(
        json.dumps(report.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return report


def summarize_scenarios(report: MultiScenarioReport, scenario_id: str) -> AugmentSummary:
    results: list[AugmentEndpointResult] = []
    errors = 0
    cached = 0
    ok = 0
    skipped = 0
    for item in report.results:
        if item.scenario != scenario_id:
            continue
        status = item.status
        if status == "cached":
            cached += 1
        elif status == "ok":
            ok += 1
        elif status == "skipped":
            skipped += 1
        elif status == "error":
            errors += 1
        results.append(
            AugmentEndpointResult(
                id=item.endpoint_id,
                status=status,
                status_code=item.status_code,
                reason=item.reason,
                note=item.note,
                scenario=item.scenario,
            )
        )
    return AugmentSummary(
        total=len(results),
        processed=len(results),
        ok=ok,
        cached=cached,
        skipped=skipped,
        errors=errors,
        results=results,
    )


def run_augmentation(
    specs: list[EndpointSpec],
    registry: dict[str, Endpoint],
    demo_client: SyncKisRawClient,
    real_client: SyncKisRawClient,
    overrides_path: Path,
    out_dir: Path,
) -> AugmentSummary:
    overrides = load_overrides(overrides_path)
    results: list[AugmentEndpointResult] = []
    errors = 0
    cached = 0
    ok = 0
    skipped = 0
    resolver_demo = ValueResolver(demo_client, overrides) if demo_client else None
    resolver_real = ValueResolver(real_client, overrides) if real_client else None

    demo_auth_available = True
    needs_demo_auth = any(
        spec.domains.demo and registry[spec.id].auth_required for spec in specs if spec.id in registry
    )
    if needs_demo_auth and demo_client:
        try:
            demo_client.ensure_token()
        except Exception as exc:
            demo_auth_available = False
            logger.warning("augment demo auth unavailable: %s", exc)

    real_auth_available = True
    needs_real_auth = any(
        spec.domains.real and registry[spec.id].auth_required for spec in specs if spec.id in registry
    )
    if needs_real_auth and real_client:
        try:
            real_client.ensure_token()
        except Exception as exc:
            real_auth_available = False
            logger.warning("augment real auth unavailable: %s", exc)

    for idx, spec in enumerate(specs, start=1):
        endpoint_def = registry.get(spec.id)
        if endpoint_def is None:
            raise RuntimeError(f"[augment] missing generated endpoint for {spec.id}")

        domain = None
        client = None
        resolver = None
        base_url = ""
        if spec.domains.demo:
            domain = "demo"
            client = demo_client
            resolver = resolver_demo
            base_url = spec.domains.demo or ""
        elif spec.domains.real:
            domain = "real"
            client = real_client
            resolver = resolver_real
            base_url = spec.domains.real or ""
        else:
            skipped += 1
            results.append(AugmentEndpointResult(id=spec.id, status="skipped", reason="no_domain"))
            continue

        if client is None or resolver is None:
            skipped += 1
            results.append(AugmentEndpointResult(id=spec.id, status="skipped", reason=f"{domain}_client_unavailable"))
            continue

        if endpoint_def.auth_required:
            if domain == "demo" and not demo_auth_available:
                skipped += 1
                results.append(AugmentEndpointResult(id=spec.id, status="skipped", reason="auth_unavailable"))
                continue
            if domain == "real" and not real_auth_available:
                skipped += 1
                results.append(AugmentEndpointResult(id=spec.id, status="skipped", reason="auth_unavailable"))
                continue

        try:
            result = augment_endpoint(spec, endpoint_def, client, resolver, overrides, out_dir, domain, base_url)
            status = result.status
            if status == "cached":
                cached += 1
            elif status == "ok":
                ok += 1
            elif status == "skipped":
                skipped += 1
            results.append(result)
        except Exception as exc:
            errors += 1
            logger.error("augment error %s: %s", spec.id, exc)
            results.append(AugmentEndpointResult(id=spec.id, status="error", reason=str(exc)))

        if idx % 10 == 0 or idx == len(specs):
            logger.info(
                "augment progress %s/%s ok=%s cached=%s skipped=%s errors=%s",
                idx,
                len(specs),
                ok,
                cached,
                skipped,
                errors,
            )

    summary = AugmentSummary(
        total=len(specs),
        processed=len(results),
        ok=ok,
        cached=cached,
        skipped=skipped,
        errors=errors,
        results=results,
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(
        json.dumps(summary.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return summary
