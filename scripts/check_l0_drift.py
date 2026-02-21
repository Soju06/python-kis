#!/usr/bin/env python3
"""L0 drift detection: compare current L0 endpoint signatures against a saved manifest.

Usage:
    python scripts/check_l0_drift.py              # Check for drift
    python scripts/check_l0_drift.py --update      # Update manifest to current state
    python scripts/check_l0_drift.py --domain quote # Check only endpoints consumed by 'quote'

Exit codes:
    0 — No drift (or manifest updated successfully)
    1 — Drift detected in endpoints with L1 consumers
    2 — Drift detected only in endpoints without L1 consumers (informational)
"""

from __future__ import annotations

import argparse
import enum
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = PROJECT_ROOT / "data" / "service" / "_l0_manifest.yaml"


def _normalize_type_annotation(annotation: Any) -> str:
    """Normalize a type annotation to a stable string representation."""
    if annotation is None:
        return "None"
    origin = getattr(annotation, "__origin__", None)
    args = getattr(annotation, "__args__", None)
    if origin is not None and args is not None:
        origin_name = getattr(origin, "__name__", str(origin))
        arg_strs = [_normalize_type_annotation(a) for a in args]
        return f"{origin_name}[{', '.join(arg_strs)}]"
    if isinstance(annotation, type):
        return annotation.__qualname__
    return str(annotation)


def _extract_enum_definitions(model_cls: type[BaseModel]) -> dict[str, dict[str, str]]:
    """Extract enum definitions referenced by model fields."""
    enums: dict[str, dict[str, str]] = {}
    for _name, field_info in model_cls.model_fields.items():
        _collect_enums_from_annotation(field_info.annotation, enums)
    return enums


def _collect_enums_from_annotation(annotation: Any, enums: dict[str, dict[str, str]]) -> None:
    """Recursively collect enum types from an annotation."""
    if annotation is None:
        return
    if isinstance(annotation, type) and issubclass(annotation, enum.Enum):
        enums[annotation.__qualname__] = {m.name: str(m.value) for m in annotation}
        return
    for arg in getattr(annotation, "__args__", ()):
        _collect_enums_from_annotation(arg, enums)


def _extract_nested_models(model_cls: type[BaseModel]) -> dict[str, dict[str, Any]]:
    """Recursively extract nested Pydantic model shapes."""
    nested: dict[str, dict[str, Any]] = {}
    for _name, field_info in model_cls.model_fields.items():
        _collect_nested_from_annotation(field_info.annotation, nested)
    return nested


def _collect_nested_from_annotation(annotation: Any, nested: dict[str, dict[str, Any]]) -> None:
    """Recursively collect nested BaseModel types from an annotation."""
    if annotation is None:
        return
    if isinstance(annotation, type) and issubclass(annotation, BaseModel) and annotation is not BaseModel:
        if annotation.__qualname__ not in nested:
            nested[annotation.__qualname__] = extract_model_shape(annotation)
        return
    for arg in getattr(annotation, "__args__", ()):
        _collect_nested_from_annotation(arg, nested)


def _field_info_to_dict(field_info: FieldInfo) -> dict[str, Any]:
    """Convert a Pydantic FieldInfo to a stable dict for hashing."""
    type_str = _normalize_type_annotation(field_info.annotation)
    return {
        "type": type_str,
        "alias": field_info.alias,
        "required": field_info.is_required(),
        "default": repr(field_info.default) if field_info.default is not PydanticUndefined else None,
    }


def extract_model_shape(model_cls: type[BaseModel]) -> dict[str, Any]:
    """Extract the structural shape of a Pydantic model for hashing."""
    fields = {}
    for name, field_info in model_cls.model_fields.items():
        fields[name] = _field_info_to_dict(field_info)
    enums = _extract_enum_definitions(model_cls)
    nested = _extract_nested_models(model_cls)
    return {"fields": fields, "enums": enums, "nested": nested}


def compute_endpoint_signature(endpoint: Any) -> str:
    """Compute a structural signature hash for an L0 endpoint."""
    shape = {
        "meta": {
            "method": endpoint.method,
            "path": endpoint.path,
            "real_tr_id": endpoint.real_tr_id,
            "demo_tr_id": endpoint.demo_tr_id,
        },
        "request": extract_model_shape(endpoint.request_model),
        "response": extract_model_shape(endpoint.response_model),
    }
    canonical = json.dumps(shape, sort_keys=True, ensure_ascii=False)
    return f"sha256:{hashlib.sha256(canonical.encode()).hexdigest()}"


def load_manifest() -> dict[str, Any]:
    """Load the existing manifest file, or return empty structure."""
    if not MANIFEST_PATH.exists():
        return {"version": 1, "generated_at": "", "endpoints": {}}

    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
        sys.exit(1)

    with open(MANIFEST_PATH) as f:
        data = yaml.safe_load(f) or {}
    return data


def save_manifest(data: dict[str, Any]) -> None:
    """Save manifest data to YAML file."""
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
        sys.exit(1)

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_PATH, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)


def get_current_signatures() -> dict[str, dict[str, Any]]:
    """Compute signatures for all currently registered L0 endpoints."""
    sys.path.insert(0, str(PROJECT_ROOT / "src"))
    from pykis.api.raw import ensure_registry

    endpoints = ensure_registry()
    result: dict[str, dict[str, Any]] = {}
    for endpoint_id, endpoint in sorted(endpoints.items()):
        result[endpoint_id] = {
            "name": endpoint.name,
            "path": endpoint.path,
            "signature": compute_endpoint_signature(endpoint),
        }
    return result


def check_drift(domain_filter: str | None = None) -> int:
    """Compare current endpoint signatures against the manifest.

    Returns exit code: 0=no drift, 1=consumer-affecting drift, 2=non-consumer drift only.
    """
    manifest = load_manifest()
    baseline_endpoints = manifest.get("endpoints", {})
    current = get_current_signatures()

    changed: list[dict[str, Any]] = []
    added: list[dict[str, Any]] = []
    removed: list[dict[str, Any]] = []

    # Check for changed/removed
    for eid, baseline_info in baseline_endpoints.items():
        consumers = baseline_info.get("consumers", [])
        if domain_filter and domain_filter not in consumers:
            continue

        if eid not in current:
            removed.append({"id": eid, "name": baseline_info.get("name", "?"), "consumers": consumers})
        elif current[eid]["signature"] != baseline_info.get("signature", ""):
            changed.append({
                "id": eid,
                "name": current[eid]["name"],
                "consumers": consumers,
                "old_sig": baseline_info.get("signature", "")[:20],
                "new_sig": current[eid]["signature"][:20],
            })

    # Check for added
    for eid, current_info in current.items():
        if eid not in baseline_endpoints:
            if domain_filter:
                continue
            added.append({"id": eid, "name": current_info["name"]})

    # Report
    print("L0 Drift Report")
    print(f"{'=' * 50}")
    print(f"Scanned: {len(current)} endpoints")
    print(f"Baseline: {len(baseline_endpoints)} endpoints")
    print()

    if changed:
        print(f"CHANGED ({len(changed)}):")
        for entry in changed:
            consumers_str = ", ".join(entry["consumers"]) if entry["consumers"] else "(no L1 consumers)"
            print(f"  [{entry['id'][:8]}] {entry['name']}")
            print(f"    → Affects L1: {consumers_str}")
        print()

    if added:
        print(f"ADDED ({len(added)}):")
        for entry in added:
            print(f"  [{entry['id'][:8]}] {entry['name']} — new endpoint (no L1 consumers)")
        print()

    if removed:
        print(f"REMOVED ({len(removed)}):")
        for entry in removed:
            consumers_str = ", ".join(entry["consumers"]) if entry["consumers"] else "(no L1 consumers)"
            print(f"  [{entry['id'][:8]}] {entry['name']}")
            print(f"    → Previously used by L1: {consumers_str}")
        print()

    if not changed and not added and not removed:
        print("No drift detected.")
        return 0

    # Determine exit code
    consumer_affected = any(e.get("consumers") for e in changed + removed)
    affected_domains: set[str] = set()
    for e in changed + removed:
        affected_domains.update(e.get("consumers", []))

    domains_str = ", ".join(sorted(affected_domains)) if affected_domains else "none"
    print(
        f"Summary: {len(changed)} changed, {len(added)} added, {len(removed)} removed"
        f" — L1 modules affected: {domains_str}"
    )

    if consumer_affected:
        print()
        print("L0 Drift Detected — commit blocked")
        print("=" * 50)
        print()
        print("Resolution:")
        print("  1. Review affected L1 service modules")
        print("  2. Update service code to handle changes")
        print("  3. Run: python scripts/check_l0_drift.py --update")
        print("  4. Stage the updated manifest: git add data/service/_l0_manifest.yaml")
        print("  5. Re-commit")
        return 1

    return 2


def update_manifest() -> None:
    """Update the manifest with current endpoint signatures."""
    current = get_current_signatures()
    old_manifest = load_manifest()
    old_endpoints = old_manifest.get("endpoints", {})

    # Preserve consumer annotations from existing manifest
    new_endpoints: dict[str, Any] = {}
    for eid, info in current.items():
        consumers = old_endpoints.get(eid, {}).get("consumers", [])
        new_endpoints[eid] = {
            "name": info["name"],
            "path": info["path"],
            "signature": info["signature"],
            "consumers": consumers,
        }

    manifest = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "endpoints": new_endpoints,
    }

    save_manifest(manifest)
    print(f"Manifest updated: {len(new_endpoints)} endpoints written to {MANIFEST_PATH}")


def main() -> None:
    parser = argparse.ArgumentParser(description="L0 drift detection")
    parser.add_argument("--update", action="store_true", help="Update manifest to current state")
    parser.add_argument("--domain", type=str, default=None, help="Filter by L1 domain (e.g., quote)")
    args = parser.parse_args()

    if args.update:
        update_manifest()
        sys.exit(0)

    exit_code = check_drift(domain_filter=args.domain)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
