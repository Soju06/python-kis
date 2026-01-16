from __future__ import annotations

from typing import TypeAlias

from pydantic import BaseModel, ConfigDict, Field, RootModel

from codegen.core.types import JsonValue

ValidationErrorLoc: TypeAlias = list[str | int]


class ValidationErrorEntry(BaseModel):
    model_config = ConfigDict(extra="allow", str_strip_whitespace=True)

    loc: ValidationErrorLoc | None = None
    type: str | None = None
    input: JsonValue | None = None
    msg: str | None = None


class EnumMismatchMap(RootModel[dict[str, dict[str, dict[str, int]]]]):
    model_config = ConfigDict(str_strip_whitespace=True)

    root: dict[str, dict[str, dict[str, int]]] = Field(default_factory=dict)

    def increment(self, struct_name: str, field_name: str, value: str, count: int = 1) -> None:
        struct_map = self.root.setdefault(struct_name, {})
        field_map = struct_map.setdefault(field_name, {})
        field_map[value] = field_map.get(value, 0) + count

    def merge(self, other: EnumMismatchMap) -> None:
        for struct_name, fields in other.root.items():
            for field_name, values in fields.items():
                for value, count in values.items():
                    self.increment(struct_name, field_name, value, count=count)


class ValidationSplitResult(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    hard_errors: list[ValidationErrorEntry] = Field(default_factory=list)
    mismatches: EnumMismatchMap = Field(default_factory=EnumMismatchMap)


class ValidationErrorRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    source_id: str
    struct: str
    line_no: int
    error: str


class ValidationSourceSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    struct: str
    records: int
    errors: int


class StoreValidationReport(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    errors: list[ValidationErrorRecord] = Field(default_factory=list)
    total_errors: int = 0
    sources: dict[str, ValidationSourceSummary] = Field(default_factory=dict)
    enum_mismatches: EnumMismatchMap = Field(default_factory=EnumMismatchMap)


__all__ = [
    "EnumMismatchMap",
    "StoreValidationReport",
    "ValidationErrorEntry",
    "ValidationErrorRecord",
    "ValidationSourceSummary",
    "ValidationSplitResult",
]
