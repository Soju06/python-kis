from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MasterField(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, str_strip_whitespace=True)

    name: str
    type_code: str = Field(alias="type")
    length: int
    description: str | None = ""
    length_source: str | None = None


class MasterStructSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str
    header_url: str
    fields: list[MasterField] = Field(default_factory=list)
    record_length: int | None = None


class MasterSourceSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, str_strip_whitespace=True)

    source_id: str
    group: str
    label: str
    download_url: str
    header_url: str
    struct_name: str = Field(alias="struct")


class MasterCatalog(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    version: str | None = None
    sources: list[MasterSourceSpec] = Field(default_factory=list)
    structs: list[MasterStructSpec] = Field(default_factory=list)
