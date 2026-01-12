from __future__ import annotations

from typing import Iterable

try:
    from pykis.api.raw.registry import ENDPOINTS as _GENERATED
except Exception as exc:
    _GENERATED = {}
    print(f"[pykis.api] registry import failed: {exc}")

ENDPOINTS = dict(_GENERATED)


def register(endpoint) -> None:
    ENDPOINTS[endpoint.id] = endpoint


def register_many(endpoints: Iterable) -> None:
    for endpoint in endpoints:
        register(endpoint)


def get_endpoint(endpoint_id: str):
    return ENDPOINTS.get(endpoint_id)


def list_endpoints():
    return list(ENDPOINTS.values())
