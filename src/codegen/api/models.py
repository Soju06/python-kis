from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from codegen.core.types import JsonValue


class DocField(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, str_strip_whitespace=True)

    code: str
    name: str
    type_code: str = Field(alias="type")
    type_name: str
    length: str | None = None
    required: bool
    description: str | None = ""


class DocRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    headers: list[DocField] = Field(default_factory=list)
    params: list[DocField] = Field(default_factory=list)
    body: list[DocField] = Field(default_factory=list)
    example: JsonValue | None = None


class DocResponse(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    headers: list[DocField] = Field(default_factory=list)
    body: list[DocField] = Field(default_factory=list)
    example: JsonValue | None = None


class DocError(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    code: str
    message: str
    description: str | None = ""


class DocDomains(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    real: str | None = None
    demo: str | None = None


class DocMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    organization: str | None = ""
    billing_policy: str | None = ""
    status: str | None = ""
    created_date: str | None = ""
    last_modified_date: str | None = ""


class DocEndpoint(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str
    name: str
    section: str
    category: str | None = ""
    subcategory: str | None = ""
    method: str
    url: str
    content_type: str | None = ""
    req_format: str | None = ""
    domains: DocDomains
    tr_ids: list[str] = Field(default_factory=list)
    real_tr_id: str | None = None
    demo_tr_id: str | None = None
    summary: str | None = ""
    description: str | None = ""
    metadata: DocMetadata | None = None
    request: DocRequest
    response: DocResponse
    errors: list[DocError] = Field(default_factory=list)


class SpecField(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, str_strip_whitespace=True)

    code: str
    name: str
    type_code: str = Field(alias="type")
    type_name: str
    length: str | None = None
    required: bool
    description: str | None = ""


class SpecRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    headers: list[SpecField] = Field(default_factory=list)
    query: list[SpecField] = Field(default_factory=list)
    body: list[SpecField] = Field(default_factory=list)
    example: JsonValue | None = None


class SpecOutput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    code: str
    name: str
    kind: Literal["single", "array", "unknown"] = "unknown"
    fields: list[SpecField] = Field(default_factory=list)


class SpecResponse(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    headers: list[SpecField] = Field(default_factory=list)
    body: list[SpecField] = Field(default_factory=list)
    outputs: list[SpecOutput] = Field(default_factory=list)
    example: JsonValue | None = None


class SpecDomains(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    real: str | None = None
    demo: str | None = None


class EndpointSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str
    name: str
    section: str
    category: str | None = ""
    subcategory: str | None = ""
    method: Literal["GET", "POST"]
    path: str
    content_type: str | None = ""
    req_format: str | None = ""
    domains: SpecDomains
    tr_ids: list[str] = Field(default_factory=list)
    real_tr_id: str | None = None
    demo_tr_id: str | None = None
    description: str | None = ""
    metadata: DocMetadata | None = None
    request: SpecRequest
    response: SpecResponse
    errors: list[DocError] = Field(default_factory=list)
    source_path: str
