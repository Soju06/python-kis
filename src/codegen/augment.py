from __future__ import annotations

import json
import hashlib
from decimal import Decimal
from datetime import date, datetime, time
from pathlib import Path
from urllib.parse import urljoin

import yaml

from pydantic import ValidationError
import re

from pykis.api.client import KisRawClient
from pykis.api.raw.types import Endpoint

from .models import EndpointSpec, SpecField


def _lower_map(values: dict[str, object]) -> dict[str, object]:
    return {str(k).lower(): v for k, v in values.items()}


_ENUM_DESC_RE = re.compile(r"\b([A-Za-z0-9]{1,8})\s*[:=]")
_ENUM_DESC_RE_ALT = re.compile(r"\b([A-Za-z0-9]{1,8})\s*[-–]")
_ENUM_DESC_RE_POST = re.compile(r"[:=]\s*([0-9]{1,8})")


def _enum_values(field: SpecField) -> list[str]:
    desc = (field.description or "").strip()
    if not desc:
        return []
    matches = _ENUM_DESC_RE.findall(desc)
    matches += _ENUM_DESC_RE_ALT.findall(desc)
    matches += _ENUM_DESC_RE_POST.findall(desc)
    if not matches:
        return []
    if "Y" in matches or "N" in matches:
        matches = [value for value in matches if value in {"Y", "N"}]
    unique: list[str] = []
    for value in matches:
        if value not in unique:
            unique.append(value)
    return unique


def _enum_default(field: SpecField) -> str | None:
    values = _enum_values(field)
    if values:
        if set(values) == {"Y", "N"}:
            return "N"
        return values[0]
    desc = (field.description or "").strip()
    if not desc:
        return None
    lowered = desc.lower()
    if "y/n" in lowered or "여부" in desc:
        return "N"
    return None


def load_overrides(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        return {}
    defaults = _lower_map(data.get("defaults", {}) if isinstance(data.get("defaults"), dict) else {})
    endpoints = data.get("endpoints", {}) if isinstance(data.get("endpoints"), dict) else {}
    normalized_endpoints: dict[str, dict[str, dict[str, object]]] = {}
    for endpoint_id, payload in endpoints.items():
        if not isinstance(payload, dict):
            continue
        normalized_endpoints[endpoint_id] = {
            "headers": _lower_map(payload.get("headers", {}) if isinstance(payload.get("headers"), dict) else {}),
            "query": _lower_map(payload.get("query", {}) if isinstance(payload.get("query"), dict) else {}),
            "body": _lower_map(payload.get("body", {}) if isinstance(payload.get("body"), dict) else {}),
        }
    return {"defaults": defaults, "endpoints": normalized_endpoints}


UNSAFE_KEYWORDS = ("주문", "정정", "취소", "매수", "매도", "trading", "order")
SKIP_PATHS = {"/oauth2/revokeP", "/oauth2/tokenP", "/uapi/hashkey"}


class ValueResolver:
    __slots__ = ("_defaults", "_endpoints")

    def __init__(self, client: KisRawClient, overrides: dict[str, object]) -> None:
        account_no, account_product = client.auth.account_number
        self._defaults = {
            "appkey": client.auth.appkey,
            "appsecret": client.auth.appsecret,
            "id": client.auth.id,
            "custtype": client.auth.custtype,
            "cano": account_no,
            "acnt_prdt_cd": account_product,
            "acca_dvsn_cd": "00",
            "inqr_dvsn": "00",
            "ctx_area_fk100": "",
            "ctx_area_nk100": "",
            "ctx_area_fk200": "",
            "ctx_area_nk200": "",
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": "005930",
            "pdno": "005930",
        }
        defaults = overrides.get("defaults")
        if isinstance(defaults, dict):
            self._defaults.update(_lower_map(defaults))
        endpoints = overrides.get("endpoints")
        self._endpoints = endpoints if isinstance(endpoints, dict) else {}

    def resolve(
        self,
        endpoint_id: str,
        location: str,
        code: str,
    ) -> object | None:
        key = code.lower()
        if key in ("secretkey", "secret_key"):
            return self._defaults.get("appsecret")
        if key == "grant_type":
            return "client_credentials"
        if key in ("user_id", "userid"):
            return self._defaults.get("user_id") or self._defaults.get("userid") or self._defaults.get("id")
        endpoint_overrides = self._endpoints.get(endpoint_id, {})
        if endpoint_overrides:
            location_overrides = endpoint_overrides.get(location, {})
            if key in location_overrides:
                return location_overrides[key]
        if key in self._defaults:
            return self._defaults[key]
        return _heuristic_value(key)


def _heuristic_value(code: str) -> object | None:
    code = code.lower()
    if code.endswith("etc_cls_code"):
        return ""
    if code.endswith("hour_1"):
        return "100000"
    if any(token in code for token in ("date", "_dt", "ymd", "bass_dt", "bsop_date")):
        return datetime.now().strftime("%Y%m%d")
    if any(token in code for token in ("time", "hour", "tm")):
        return "090000"
    if code.endswith("_yn") or code.endswith("yn"):
        return "N"
    if any(token in code for token in ("qty", "cnt", "count", "vol")):
        return "1"
    if any(token in code for token in ("price", "prc", "amt", "rate", "rt", "ratio", "val", "delta", "gear", "prmm", "vltl")):
        return "0"
    if code.startswith("fid_") and re.search(r"\d+$", code):
        return "0"
    if code.startswith("ctx_area"):
        return ""
    if code in ("seq", "nmin", "pinc", "next", "nrec", "fill"):
        return "0"
    if code in ("cts_area",):
        return ""
    if any(token in code for token in ("code", "cls", "cd", "div", "type", "gb", "gubn")):
        return "0"
    if "symb" in code:
        return "AAPL"
    if any(token in code for token in ("excd", "exch", "exchange")):
        return "NAS"
    return None


def _fingerprint(spec: EndpointSpec, overrides: dict[str, object], domain: str) -> str:
    payload = {
        "spec": spec.model_dump(),
        "overrides": overrides,
        "domain": domain,
        "augment_version": 2,
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


def _select_tr_id(endpoint: EndpointSpec, domain: str) -> str | None:
    if domain == "demo" and endpoint.virtual_tr_id:
        return endpoint.virtual_tr_id
    if domain == "real" and endpoint.real_tr_id:
        return endpoint.real_tr_id
    for tr_id in endpoint.tr_ids:
        if isinstance(tr_id, str) and "미지원" not in tr_id:
            return tr_id
    return None


def _is_unsafe(endpoint: EndpointSpec) -> bool:
    haystack = " ".join(
        filter(None, [endpoint.name, endpoint.section, endpoint.category, endpoint.subcategory, endpoint.path])
    ).lower()
    return any(keyword.lower() in haystack for keyword in UNSAFE_KEYWORDS)


def _build_headers(
    endpoint: EndpointSpec,
    resolver: ValueResolver,
    domain: str,
) -> tuple[dict[str, str], list[str]]:
    headers: dict[str, str] = {}
    missing: list[str] = []
    tr_id = _select_tr_id(endpoint, domain)

    for field in endpoint.request.headers:
        key = field.code
        key_lower = key.lower()
        value: object | None = None

        if key_lower == "content-type":
            value = "application/json; charset=utf-8"
            key = "content-type"
        elif key_lower == "authorization":
            value = "__AUTH__"
            key = "authorization"
        elif key_lower == "appkey":
            value = resolver.resolve(endpoint.id, "headers", key)
            key = "appkey"
        elif key_lower == "appsecret":
            value = resolver.resolve(endpoint.id, "headers", key)
            key = "appsecret"
        elif key_lower == "tr_id":
            value = tr_id
            key = "tr_id"
        else:
            value = resolver.resolve(endpoint.id, "headers", key)

        if value is None:
            if field.required:
                missing.append(field.code)
            continue

        headers[key] = str(value)

    return headers, missing


def _build_payload(
    endpoint: EndpointSpec,
    resolver: ValueResolver,
    location: str,
    fields: list[SpecField],
) -> tuple[dict[str, object], list[str]]:
    payload: dict[str, object] = {}
    missing: list[str] = []

    for field in fields:
        value = resolver.resolve(endpoint.id, location, field.code)
        enum_values = _enum_values(field)
        if enum_values:
            if value is None or str(value) not in enum_values:
                value = _enum_default(field)
        elif value is None:
            value = _enum_default(field)
        if value is None:
            value = _heuristic_value(field.code)
        desc = (field.description or "").strip().lower()
        if "공백" in desc or "blank" in desc:
            value = "" if value is None else value
        if value is None and field.required:
            value = ""
            missing.append(field.code)
        if value is None:
            continue
        payload[field.code] = value

    return payload, missing


def augment_endpoint(
    endpoint: EndpointSpec,
    endpoint_def: Endpoint,
    client: KisRawClient,
    resolver: ValueResolver,
    overrides: dict[str, object],
    out_dir: Path,
    domain: str,
    base_url: str,
) -> dict[str, object]:
    if not base_url:
        return {"id": endpoint.id, "status": "skipped", "reason": "domain_not_available"}

    if base_url.startswith(("ws://", "wss://")):
        return {"id": endpoint.id, "status": "skipped", "reason": "websocket"}

    if _is_unsafe(endpoint):
        return {"id": endpoint.id, "status": "skipped", "reason": "unsafe"}
    if endpoint.path in SKIP_PATHS:
        return {"id": endpoint.id, "status": "skipped", "reason": "skip_path"}

    result_dir = out_dir / endpoint.id
    fingerprint = _fingerprint(endpoint, overrides, domain)
    meta_path = result_dir / "meta.json"
    if meta_path.exists() and (result_dir / "success.json").exists():
        try:
            cached_meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            cached_meta = None
        if cached_meta and cached_meta.get("fingerprint") == fingerprint and cached_meta.get("ok"):
            return {"id": endpoint.id, "status": "cached"}

    headers, header_missing = _build_headers(endpoint, resolver, domain)
    query, query_missing = _build_payload(endpoint, resolver, "query", endpoint.request.query)
    body, body_missing = _build_payload(endpoint, resolver, "body", endpoint.request.body)

    missing = header_missing + query_missing + body_missing
    if header_missing:
        return {"id": endpoint.id, "status": "skipped", "reason": f"missing_required_headers: {header_missing}"}

    request_payload = {**query, **body}
    try:
        request_model = endpoint_def.request_model.model_validate(request_payload)
    except ValidationError as exc:
        print(f"[augment] request validation failed: {endpoint.id} -> {exc}")
        raise

    response = client.request(
        method=endpoint.method,
        base_url=base_url,
        path=endpoint.path,
        headers=headers,
        params=query if query else None,
        body=body if body else None,
        auth_required=endpoint_def.auth_required,
        hashkey_required=endpoint_def.hashkey_required,
    )

    result_dir.mkdir(parents=True, exist_ok=True)

    request_payload = {
        "method": endpoint.method,
        "url": urljoin(base_url, endpoint.path),
        "headers": headers,
        "query": query,
        "body": body,
    }
    _dump_json(result_dir / "request.json", request_payload)

    meta = {
        "status_code": response.status_code,
        "ok": response.ok,
        "domain": domain,
        "endpoint": endpoint.id,
        "missing_required": missing,
        "fingerprint": fingerprint,
    }

    try:
        payload = response.json()
    except Exception:
        payload = None

    if not response.ok:
        meta["ok"] = False
        error_payload = payload if payload is not None else {"raw": response.text}
        if payload is not None:
            _dump_json(result_dir / "raw.json", payload)
        _dump_json(result_dir / "meta.json", meta)
        _dump_json(result_dir / "error.json", error_payload)
        raise RuntimeError(f"[augment] HTTP {response.status_code} for {endpoint.id}")

    if payload is None:
        meta["ok"] = False
        _dump_json(result_dir / "meta.json", meta)
        _dump_json(result_dir / "error.json", {"raw": response.text})
        raise RuntimeError(f"[augment] invalid JSON for {endpoint.id}")

    _dump_json(result_dir / "raw.json", payload)

    if isinstance(payload, dict) and str(payload.get("rt_cd")) not in ("0", "OK"):
        meta["ok"] = False
        _dump_json(result_dir / "meta.json", meta)
        _dump_json(result_dir / "error.json", payload)
        raise RuntimeError(f"[augment] rt_cd error for {endpoint.id}")

    try:
        response_model = endpoint_def.response_model.model_validate(payload)
    except ValidationError as exc:
        meta["ok"] = False
        _dump_json(result_dir / "meta.json", meta)
        _dump_json(result_dir / "error.json", {"validation_error": exc.errors(), "payload": payload})
        raise

    _dump_json(result_dir / "meta.json", meta)
    _dump_json(result_dir / "success.json", response_model.model_dump(by_alias=True))

    error_payload = _probe_error(endpoint, client, headers, query, body, base_url)
    if error_payload is not None:
        _dump_json(result_dir / "error.json", error_payload)

    return {"id": endpoint.id, "status": "ok", "status_code": response.status_code}


def _probe_error(
    endpoint: EndpointSpec,
    client: KisRawClient,
    headers: dict[str, str],
    query: dict[str, object],
    body: dict[str, object],
    base_url: str,
) -> dict[str, object] | None:
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
        params=query_copy if query_copy else None,
        body=body_copy if body_copy else None,
        auth_required="authorization" in {h.code.lower() for h in endpoint.request.headers},
        hashkey_required="hashkey" in {h.code.lower() for h in endpoint.request.headers},
    )
    try:
        return response.json()
    except Exception:
        return {"raw": response.text}


def run_augmentation(
    specs: list[EndpointSpec],
    registry: dict[str, Endpoint],
    demo_client: KisRawClient,
    real_client: KisRawClient,
    overrides_path: Path,
    out_dir: Path,
) -> dict[str, object]:
    overrides = load_overrides(overrides_path)
    results: list[dict[str, object]] = []
    errors = 0
    cached = 0
    ok = 0
    skipped = 0
    resolver_demo = ValueResolver(demo_client, overrides) if demo_client else None
    resolver_real = ValueResolver(real_client, overrides) if real_client else None

    demo_auth_available = True
    needs_demo_auth = any(
        spec.domains.virtual and registry[spec.id].auth_required for spec in specs if spec.id in registry
    )
    if needs_demo_auth and demo_client:
        try:
            demo_client.ensure_token()
        except Exception as exc:
            demo_auth_available = False
            print(f"[augment] demo auth unavailable: {exc}")

    real_auth_available = True
    needs_real_auth = any(
        spec.domains.real and registry[spec.id].auth_required for spec in specs if spec.id in registry
    )
    if needs_real_auth and real_client:
        try:
            real_client.ensure_token()
        except Exception as exc:
            real_auth_available = False
            print(f"[augment] real auth unavailable: {exc}")

    for idx, spec in enumerate(specs, start=1):
        endpoint_def = registry.get(spec.id)
        if endpoint_def is None:
            raise RuntimeError(f"[augment] missing generated endpoint for {spec.id}")

        domain = None
        client = None
        resolver = None
        base_url = ""
        if spec.domains.virtual:
            domain = "demo"
            client = demo_client
            resolver = resolver_demo
            base_url = spec.domains.virtual or ""
        elif spec.domains.real:
            domain = "real"
            client = real_client
            resolver = resolver_real
            base_url = spec.domains.real or ""
        else:
            skipped += 1
            results.append({"id": spec.id, "status": "skipped", "reason": "no_domain"})
            continue

        if client is None or resolver is None:
            skipped += 1
            results.append({"id": spec.id, "status": "skipped", "reason": f"{domain}_client_unavailable"})
            continue

        if endpoint_def.auth_required:
            if domain == "demo" and not demo_auth_available:
                skipped += 1
                results.append({"id": spec.id, "status": "skipped", "reason": "auth_unavailable"})
                continue
            if domain == "real" and not real_auth_available:
                skipped += 1
                results.append({"id": spec.id, "status": "skipped", "reason": "auth_unavailable"})
                continue

        try:
            result = augment_endpoint(spec, endpoint_def, client, resolver, overrides, out_dir, domain, base_url)
            status = result.get("status")
            if status == "cached":
                cached += 1
            elif status == "ok":
                ok += 1
            elif status == "skipped":
                skipped += 1
            results.append(result)
        except Exception as exc:
            errors += 1
            print(f"[augment] error {spec.id}: {exc}")
            results.append({"id": spec.id, "status": "error", "reason": str(exc)})

        if idx % 10 == 0 or idx == len(specs):
            print(
                f"[augment] progress {idx}/{len(specs)} ok={ok} cached={cached} "
                f"skipped={skipped} errors={errors}"
            )

    summary = {
        "total": len(specs),
        "processed": len(results),
        "ok": ok,
        "cached": cached,
        "skipped": skipped,
        "errors": errors,
        "results": results,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary
