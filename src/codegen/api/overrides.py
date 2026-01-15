from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field

from codegen.api.types import EndpointHints, TypeOverrides
from codegen.core.types import JsonValue


class FieldRange(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    start: int | None = None
    end: int | None = None
    pad: int | None = None


class FieldTemplate(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    name: str | None = None
    description: str | None = None


class FieldSpecOverride(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True, str_strip_whitespace=True)

    code: str | None = None
    name: str | None = None
    type_code: str | None = Field(default=None, alias="type")
    type_name: str | None = None
    length: str | None = None
    required: bool | None = None
    description: str | None = None


class FieldExpandSpec(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True, str_strip_whitespace=True)

    code_prefix: str | None = None
    prefix: str | None = None
    start: int | None = None
    end: int | None = None
    pad: int | None = None
    range: FieldRange | None = None
    template: FieldTemplate | None = None
    field: FieldSpecOverride | None = None

    name: str | None = None
    description: str | None = None
    type_code: str | None = Field(default=None, alias="type")
    type_name: str | None = None
    length: str | None = None
    required: bool | None = None

    def resolved_prefix(self) -> str:
        return (self.code_prefix or self.prefix or "").strip()


class FieldOverride(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    remove: list[str] = Field(default_factory=list)
    remove_regex: list[str] = Field(default_factory=list)
    expand: list[FieldExpandSpec] = Field(default_factory=list)
    upsert: list[FieldSpecOverride] = Field(default_factory=list)


class RequestOverride(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    headers: FieldOverride | None = None
    params: FieldOverride | None = None
    query: FieldOverride | None = None
    body: FieldOverride | None = None
    body_override: FieldOverride | None = None


class ResponseOverride(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    headers: FieldOverride | None = None
    body: FieldOverride | None = None


class DocOverrideEntry(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    reason: str | None = None
    request: RequestOverride | None = None
    response: ResponseOverride | None = None


class DocOverrideFile(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    overrides: list[DocOverrideEntry] = Field(default_factory=list)

    def index(self) -> dict[str, DocOverrideEntry]:
        return {entry.id: entry for entry in self.overrides}


class TypeOverrideEntry(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    changes: EndpointHints = Field(default_factory=EndpointHints)
    reason: str | None = None
    source: str | None = None


class TypeOverrideFile(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    overrides: list[TypeOverrideEntry] = Field(default_factory=list)

    def to_overrides(self) -> TypeOverrides:
        merged = TypeOverrides()
        for entry in self.overrides:
            merged = merged.merge(TypeOverrides(endpoints={entry.id: entry.changes}))
        return merged


class EndpointOverrideLocations(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    headers: dict[str, JsonValue] = Field(default_factory=dict)
    query: dict[str, JsonValue] = Field(default_factory=dict)
    body: dict[str, JsonValue] = Field(default_factory=dict)

    def normalized(self) -> EndpointOverrideLocations:
        return EndpointOverrideLocations(
            headers=_lower_map(self.headers),
            query=_lower_map(self.query),
            body=_lower_map(self.body),
        )


class AugmentOverrides(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    defaults: dict[str, JsonValue] = Field(default_factory=dict)
    endpoints: dict[str, EndpointOverrideLocations] = Field(default_factory=dict)

    def normalized(self) -> AugmentOverrides:
        endpoints = {endpoint_id: location.normalized() for endpoint_id, location in self.endpoints.items()}
        return AugmentOverrides(defaults=_lower_map(self.defaults), endpoints=endpoints)


def load_doc_overrides(path: Path) -> dict[str, DocOverrideEntry]:
    if not path.exists():
        return {}
    data = _load_yaml(path)
    overrides = DocOverrideFile.model_validate(data)
    return overrides.index()


def load_type_overrides(path: Path) -> TypeOverrides:
    if not path.exists():
        return TypeOverrides()
    data = _load_yaml(path)
    overrides = TypeOverrideFile.model_validate(data)
    return overrides.to_overrides()


def load_augment_overrides(path: Path) -> AugmentOverrides:
    if not path.exists():
        return AugmentOverrides()
    data = _load_yaml(path)
    overrides = AugmentOverrides.model_validate(data)
    return overrides.normalized()


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML root: {path}")
    return data


def _lower_map(values: dict[str, JsonValue]) -> dict[str, JsonValue]:
    return {str(key).lower(): value for key, value in values.items()}


__all__ = [
    "AugmentOverrides",
    "DocOverrideEntry",
    "EndpointOverrideLocations",
    "FieldExpandSpec",
    "FieldOverride",
    "FieldRange",
    "FieldSpecOverride",
    "FieldTemplate",
    "RequestOverride",
    "ResponseOverride",
    "TypeOverrides",
    "load_augment_overrides",
    "load_doc_overrides",
    "load_type_overrides",
]
