from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, cast

import yaml

from codegen.core.enums import parse_enum_entries
from codegen.streaming.models import FieldSpec, StreamingSpecRoot, TrSpec


@dataclass(frozen=True, slots=True)
class DocConflict:
    tr_id: str
    code: str
    previous: str
    current: str
    path: str


@dataclass(frozen=True, slots=True)
class DocMapResult:
    fields_by_tr: dict[str, dict[str, str | None]]
    sources_by_tr: dict[str, list[str]]
    conflicts: list[DocConflict]
    errors: list[dict[str, str]]
    docs_count: int


def build_doc_map(docs_root: Path) -> DocMapResult:
    if not docs_root.exists():
        return DocMapResult(fields_by_tr={}, sources_by_tr={}, conflicts=[], errors=[], docs_count=0)

    fields_by_tr: dict[str, dict[str, str | None]] = {}
    sources_by_tr: dict[str, list[str]] = {}
    conflicts: list[DocConflict] = []
    errors: list[dict[str, str]] = []
    docs_count = 0

    for path in _iter_yaml_files(docs_root):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            errors.append({"path": str(path), "error": str(exc)})
            continue
        if not isinstance(data, Mapping):
            continue
        if not _is_streaming_doc(data, path):
            continue
        fields = _extract_response_fields(data)
        if not fields:
            continue
        docs_count += 1
        tr_id = path.stem.upper()
        sources_by_tr.setdefault(tr_id, []).append(str(path))
        field_map = fields_by_tr.setdefault(tr_id, {})
        for code, desc in fields.items():
            if code in field_map:
                previous = field_map[code]
                if desc and previous and desc != previous:
                    conflicts.append(
                        DocConflict(
                            tr_id=tr_id,
                            code=code,
                            previous=previous,
                            current=desc,
                            path=str(path),
                        )
                    )
                if not previous and desc:
                    field_map[code] = desc
                continue
            field_map[code] = desc

    for tr_id in sources_by_tr:
        sources_by_tr[tr_id] = sorted(sources_by_tr[tr_id])

    return DocMapResult(
        fields_by_tr=fields_by_tr,
        sources_by_tr=sources_by_tr,
        conflicts=conflicts,
        errors=errors,
        docs_count=docs_count,
    )


def merge_doc_descriptions(
    spec: StreamingSpecRoot,
    doc_map: DocMapResult,
    docs_root: Path | None = None,
) -> tuple[StreamingSpecRoot, dict[str, object]]:
    tr_ids = set(spec.tr_specs)
    doc_tr_ids = set(doc_map.fields_by_tr)

    updated_fields_total = 0
    alias_updates_total = 0
    enum_desc_added_total = 0

    tr_reports: dict[str, dict[str, object]] = {}
    new_tr_specs: dict[str, TrSpec] = {}

    for tr_id, tr_spec in spec.tr_specs.items():
        doc_fields = doc_map.fields_by_tr.get(tr_id, {})
        base_names = set(tr_spec.field_order)

        missing_in_docs = sorted(name for name in base_names if name not in doc_fields)
        missing_in_spec = sorted(code for code in doc_fields if code not in tr_spec.field_specs)

        updated_fields = 0
        alias_updates = 0
        enum_desc_added = 0

        new_field_specs: dict[str, FieldSpec] = {}
        for name, field_spec in tr_spec.field_specs.items():
            doc_desc = doc_fields.get(name)
            desc = field_spec.desc
            if doc_desc:
                if doc_desc != desc:
                    updated_fields += 1
                desc = doc_desc

            enum_desc = field_spec.enum_desc
            if not enum_desc:
                entries = parse_enum_entries(desc or "")
                if entries:
                    candidate = {entry.code: entry.desc for entry in entries if entry.desc}
                    if candidate:
                        enum_desc = candidate
                        enum_desc_added += 1

            new_field_specs[name] = FieldSpec(
                name=field_spec.name,
                field_type=field_spec.field_type,
                source=field_spec.source,
                desc=desc,
                datetime_rule=field_spec.datetime_rule,
                decimal_rule=field_spec.decimal_rule,
                enum=field_spec.enum,
                enum_desc=enum_desc,
            )

        for index, alias in tr_spec.field_aliases.items():
            if index < 0 or index >= len(tr_spec.field_order):
                continue
            original_name = tr_spec.field_order[index]
            original_spec = new_field_specs.get(original_name)
            alias_spec = new_field_specs.get(alias)
            if original_spec is None or alias_spec is None:
                continue
            if alias_spec.desc != original_spec.desc or alias_spec.enum_desc != original_spec.enum_desc:
                alias_updates += 1
                new_field_specs[alias] = FieldSpec(
                    name=alias_spec.name,
                    field_type=alias_spec.field_type,
                    source=alias_spec.source,
                    desc=original_spec.desc,
                    datetime_rule=alias_spec.datetime_rule,
                    decimal_rule=alias_spec.decimal_rule,
                    enum=alias_spec.enum,
                    enum_desc=original_spec.enum_desc,
                )

        updated_fields_total += updated_fields
        alias_updates_total += alias_updates
        enum_desc_added_total += enum_desc_added

        doc_field_total = len(doc_fields)
        doc_fields_with_desc = sum(1 for value in doc_fields.values() if value)
        base_field_total = len(base_names)
        base_fields_with_doc = base_field_total - len(missing_in_docs)
        base_fields_with_desc = sum(1 for name in base_names if doc_fields.get(name))

        tr_reports[tr_id] = {
            "sources": doc_map.sources_by_tr.get(tr_id, []),
            "field_total": base_field_total,
            "fields_with_docs": base_fields_with_doc,
            "fields_with_desc": base_fields_with_desc,
            "doc_fields_total": doc_field_total,
            "doc_fields_with_desc": doc_fields_with_desc,
            "missing_in_docs": missing_in_docs,
            "missing_in_spec": missing_in_spec,
            "updated_fields": updated_fields,
            "alias_updates": alias_updates,
            "enum_desc_added": enum_desc_added,
        }

        new_tr_specs[tr_id] = TrSpec(
            tr_id=tr_spec.tr_id,
            endpoint_uuid=tr_spec.endpoint_uuid,
            market=tr_spec.market,
            timezone=tr_spec.timezone,
            field_order=tr_spec.field_order,
            field_order_normalized=tr_spec.field_order_normalized,
            field_aliases=tr_spec.field_aliases,
            requires_business_date=tr_spec.requires_business_date,
            field_specs=new_field_specs,
        )

    report = {
        "docs_root": str(docs_root) if docs_root else "",
        "docs_count": doc_map.docs_count,
        "parse_errors": doc_map.errors,
        "conflicts": [
            {
                "tr_id": conflict.tr_id,
                "code": conflict.code,
                "previous": conflict.previous,
                "current": conflict.current,
                "path": conflict.path,
            }
            for conflict in doc_map.conflicts
        ],
        "tr_ids_with_docs": sorted(doc_tr_ids),
        "tr_ids_missing_docs": sorted(tr_ids - doc_tr_ids),
        "docs_unmatched_tr": sorted(doc_tr_ids - tr_ids),
        "stats": {
            "updated_fields": updated_fields_total,
            "alias_updates": alias_updates_total,
            "enum_desc_added": enum_desc_added_total,
        },
        "tr_reports": tr_reports,
    }

    return (
        StreamingSpecRoot(
            version=spec.version,
            source_inventory=spec.source_inventory,
            domestic_count=spec.domestic_count,
            overseas_count=spec.overseas_count,
            tr_specs=new_tr_specs,
        ),
        report,
    )


def _iter_yaml_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.yaml") if path.is_file())


def _is_streaming_doc(data: Mapping[str, object], path: Path) -> bool:
    if "실시간시세" in path.parts:
        return True
    for key in ("subcategory", "section", "category", "name"):
        value = data.get(key)
        if isinstance(value, str) and "실시간시세" in value:
            return True
    return False


def _extract_response_fields(data: Mapping[str, object]) -> dict[str, str | None]:
    response = data.get("response")
    if not isinstance(response, Mapping):
        return {}
    response = cast(Mapping[str, object], response)
    body = response.get("body")
    if not isinstance(body, list):
        return {}

    fields: dict[str, str | None] = {}
    for item in body:
        if not isinstance(item, Mapping):
            continue
        item = cast(Mapping[str, object], item)
        code = _optional_text(item.get("code"))
        if not code:
            continue
        desc = _optional_text(item.get("description") or item.get("desc")) or _optional_text(item.get("name"))
        fields[code] = desc
    return fields


def _optional_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
