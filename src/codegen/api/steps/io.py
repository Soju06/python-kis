from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

import yaml
from pydantic import BaseModel

from codegen.api.models import DocEndpoint, DocField, EndpointSpec
from codegen.api.overrides import DocOverrideEntry, FieldExpandSpec, FieldOverride, FieldSpecOverride
from codegen.core.types import JsonObject


def iter_yaml_files(root: Path) -> list[Path]:
    return sorted(
        p
        for p in root.rglob("*.yaml")
        if p.is_file() and "종목정보파일" not in p.parts
    )


def _format_template(value: str, index: int, pad: int) -> str:
    if "{index_pad}" in value:
        value = value.replace("{index_pad}", str(index).zfill(pad))
    if "{index}" in value:
        value = value.replace("{index}", str(index))
    return value


def _expand_fields(expand: FieldExpandSpec) -> list[DocField]:
    prefix = expand.resolved_prefix()
    if not prefix:
        return []
    range_spec = expand.range
    start = expand.start if expand.start is not None else (range_spec.start if range_spec else None)
    end = expand.end if expand.end is not None else (range_spec.end if range_spec else None)
    if not start or not end or end < start:
        return []
    pad = expand.pad if expand.pad is not None else (range_spec.pad if range_spec else 0)
    pad = int(pad or 0)

    template = expand.template
    field_spec = expand.field
    name = (
        expand.name
        or (template.name if template else None)
        or (field_spec.name if field_spec else None)
        or ""
    )
    description = (
        expand.description
        or (template.description if template else None)
        or (field_spec.description if field_spec else None)
        or ""
    )
    type_code = str(
        expand.type_code
        or (field_spec.type_code if field_spec else None)
        or ""
    )
    type_name = str(expand.type_name or (field_spec.type_name if field_spec else None) or "")
    length = expand.length if expand.length is not None else (field_spec.length if field_spec else None)
    required = (
        expand.required
        if expand.required is not None
        else (field_spec.required if field_spec and field_spec.required is not None else True)
    )

    fields: list[DocField] = []
    for index in range(start, end + 1):
        code = f"{prefix}{str(index).zfill(pad)}" if pad else f"{prefix}{index}"
        field_name = _format_template(name, index, pad) if name else code
        field_desc = _format_template(description, index, pad) if description else ""
        fields.append(
            DocField(
                code=code,
                name=field_name,
                type_code=type_code,
                type_name=type_name,
                length=str(length) if length is not None else None,
                required=bool(required),
                description=field_desc,
            )
        )
    return fields


def _doc_field_from_override(field: FieldSpecOverride, *, code: str | None = None) -> DocField | None:
    field_code = code or field.code
    if not field_code:
        return None
    name = field.name or field_code
    type_code = str(field.type_code or "")
    type_name = str(field.type_name or "")
    length = str(field.length) if field.length is not None else None
    required = field.required if field.required is not None else True
    description = field.description or ""
    return DocField(
        code=field_code,
        name=name,
        type_code=type_code,
        type_name=type_name,
        length=length,
        required=bool(required),
        description=description,
    )


def _apply_field_overrides(fields: list[DocField], override: FieldOverride) -> list[DocField]:
    if not override:
        return fields
    remove_codes = {code for code in override.remove if code}
    remove_regexes = [re.compile(pattern) for pattern in override.remove_regex if pattern]

    filtered = []
    for field in fields:
        if field.code in remove_codes:
            continue
        if any(regex.search(field.code) for regex in remove_regexes):
            continue
        filtered.append(field)

    expanded_fields = []
    for expand in override.expand:
        expanded_fields.extend(_expand_fields(expand))
    upserts = [_doc_field_from_override(item) for item in override.upsert]

    by_code = {field.code: field for field in filtered}
    for field in expanded_fields + upserts:
        if field is None:
            continue
        by_code[field.code] = field
    return list(by_code.values())


def _apply_doc_override(doc: DocEndpoint, override: DocOverrideEntry) -> DocEndpoint:
    request = doc.request.model_copy(deep=True)
    response = doc.response.model_copy(deep=True)
    request_override = override.request
    response_override = override.response

    if request_override:
        if request_override.body_override:
            request.body = _apply_field_overrides(request.body, request_override.body_override)
        if request_override.headers:
            request.headers = _apply_field_overrides(request.headers, request_override.headers)
        if request_override.params:
            request.params = _apply_field_overrides(request.params, request_override.params)
        if request_override.query:
            request.params = _apply_field_overrides(request.params, request_override.query)
        if request_override.body:
            request.body = _apply_field_overrides(request.body, request_override.body)

    if response_override:
        if response_override.headers:
            response.headers = _apply_field_overrides(response.headers, response_override.headers)
        if response_override.body:
            response.body = _apply_field_overrides(response.body, response_override.body)

    return doc.model_copy(update={"request": request, "response": response})


def load_yaml_doc(path: Path, overrides: dict[str, DocOverrideEntry] | None = None) -> DocEndpoint:
    data = _load_yaml(path)
    doc = DocEndpoint.model_validate(data)
    if overrides:
        override = overrides.get(doc.id)
        if override:
            doc = _apply_doc_override(doc, override)
    return doc


def load_spec(path: Path) -> EndpointSpec:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return EndpointSpec.model_validate(data)


def write_spec(path: Path, spec: EndpointSpec) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(spec.model_dump(by_alias=True), handle, ensure_ascii=False, indent=2)


def write_report(path: Path, report: JsonObject | BaseModel) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        payload = report.model_dump(by_alias=True) if isinstance(report, BaseModel) else report
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def iter_spec_files(root: Path) -> Iterable[Path]:
    return sorted(p for p in root.rglob("*.json") if p.is_file())


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML root: {path}")
    return data
