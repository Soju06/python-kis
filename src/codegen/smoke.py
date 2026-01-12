from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from pykis.api.client import KisRawClient
from pykis.api.raw.types import Endpoint

from .augment import UNSAFE_KEYWORDS, ValueResolver, _build_payload, load_overrides
from .models import EndpointSpec


def _is_read_only(spec: EndpointSpec) -> bool:
    if spec.method != "GET":
        return False
    haystack = " ".join(
        filter(None, [spec.name, spec.section, spec.category, spec.subcategory, spec.path])
    ).lower()
    return not any(keyword.lower() in haystack for keyword in UNSAFE_KEYWORDS)


def run_smoke(
    specs: list[EndpointSpec],
    registry: dict[str, Endpoint],
    demo_client: KisRawClient,
    real_client: KisRawClient,
    overrides_path: Path,
    out_path: Path,
) -> dict[str, object]:
    overrides = load_overrides(overrides_path)
    resolvers = {
        "demo": ValueResolver(demo_client, overrides),
        "real": ValueResolver(real_client, overrides),
    }
    results: list[dict[str, object]] = []
    errors = 0

    for spec in specs:
        endpoint = registry.get(spec.id)
        if endpoint is None:
            errors += 1
            results.append({"id": spec.id, "status": "missing_endpoint"})
            continue
        if not _is_read_only(spec):
            results.append({"id": spec.id, "status": "skipped", "reason": "not_read_only"})
            continue

        for domain, client in (("demo", demo_client), ("real", real_client)):
            if domain == "demo" and not spec.domains.virtual:
                results.append({"id": spec.id, "domain": domain, "status": "skipped", "reason": "demo_only"})
                continue
            if domain == "real" and not spec.domains.real:
                results.append({"id": spec.id, "domain": domain, "status": "skipped", "reason": "real_only"})
                continue

            resolver = resolvers[domain]
            query, query_missing = _build_payload(spec, resolver, "query", spec.request.query)
            body, body_missing = _build_payload(spec, resolver, "body", spec.request.body)
            missing = query_missing + body_missing
            if missing:
                errors += 1
                results.append(
                    {"id": spec.id, "domain": domain, "status": "error", "reason": f"missing_required: {missing}"}
                )
                continue

            request_payload = {**query, **body}
            try:
                endpoint.request_model.model_validate(request_payload)
            except ValidationError as exc:
                errors += 1
                results.append({"id": spec.id, "domain": domain, "status": "error", "reason": str(exc)})
                continue

            for attempt in range(2):
                try:
                    response, raw = client.call(endpoint, request_payload)
                except Exception as exc:  # noqa: BLE001
                    errors += 1
                    results.append(
                        {"id": spec.id, "domain": domain, "attempt": attempt + 1, "status": "error", "reason": str(exc)}
                    )
                    continue

                rt_cd = getattr(response, "rt_cd", None)
                if rt_cd is False or str(rt_cd) in {"0", "OK"}:
                    results.append(
                        {"id": spec.id, "domain": domain, "attempt": attempt + 1, "status": "ok", "status_code": raw.status_code}
                    )
                    continue

                errors += 1
                results.append(
                    {"id": spec.id, "domain": domain, "attempt": attempt + 1, "status": "error", "reason": f"rt_cd={rt_cd!r}"}
                )

    report = {"total": len(results), "errors": errors, "results": results}
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report
