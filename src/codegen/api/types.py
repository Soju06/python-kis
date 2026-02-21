from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from codegen.api.models import SpecField

FieldKind = Literal["str", "int", "decimal", "date", "time", "datetime", "bool", "enum"]
ValidatorRuleType = Literal[
    "output_required",
    "all_fields_sentinel",
    "any_field_sentinel",
    "all_fields_missing",
    "any_field_missing",
]
RuleScope = Literal["first_row", "all_rows", "any_row"]
RuleSeverity = Literal["error", "warn"]
ResponseValidationMode = Literal["raise", "warn", "ignore"]


class FieldHint(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    kind: FieldKind | None = None
    required: bool | None = None
    enum: list[str] | None = None
    enum_desc: dict[str, str] | None = None
    max_digits: int | None = None
    decimal_places: int | None = None

    def merge(self, override: FieldHint) -> FieldHint:
        merged = self.model_dump()
        for field_name in override.model_fields_set:
            merged[field_name] = getattr(override, field_name)
        return FieldHint(**merged)


class ExtraFields(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    response: list[SpecField] = Field(default_factory=list)
    outputs: dict[str, list[SpecField]] = Field(default_factory=dict)

    def merge(self, override: ExtraFields) -> ExtraFields:
        response = self.response
        if "response" in override.model_fields_set:
            response = override.response

        outputs = dict(self.outputs)
        if "outputs" in override.model_fields_set:
            outputs = {}
            for key, fields in override.outputs.items():
                outputs[key] = fields
        return ExtraFields(response=response, outputs=outputs)


class ValidatorWhen(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    rt_cd: list[str] | None = None
    msg_cd: list[str] | None = None


class ValidatorCapture(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    fields: list[str] | None = None
    outputs: list[str] | None = None
    max_rows: int | None = None
    redact_keys: list[str] | None = None


class ValidatorError(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    code: str
    message: str
    user_message: str
    hint: str | None = None
    exception: str


class ValidatorRule(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    id: str
    type: ValidatorRuleType
    output: str
    fields: list[str] | None = None
    sentinel_values: list[str | None] | None = None
    scope: RuleScope | None = None
    error: ValidatorError
    when: ValidatorWhen | None = None
    mode: ResponseValidationMode | None = None
    severity: RuleSeverity | None = None
    capture: ValidatorCapture | None = None


class ValidatorSpec(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    rules: list[ValidatorRule] = Field(default_factory=list)


class EndpointHints(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    request: dict[str, FieldHint] = Field(default_factory=dict)
    response: dict[str, FieldHint] = Field(default_factory=dict)
    outputs: dict[str, dict[str, FieldHint]] = Field(default_factory=dict)
    output_kinds: dict[str, str] = Field(default_factory=dict)
    output_aliases: dict[str, str] = Field(default_factory=dict)
    extra_fields: ExtraFields = Field(default_factory=ExtraFields)
    validator: ValidatorSpec | None = None

    def merge(self, override: EndpointHints) -> EndpointHints:
        validator = self.validator
        if "validator" in override.model_fields_set:
            validator = override.validator
        return EndpointHints(
            request=_merge_field_map(self.request, override.request),
            response=_merge_field_map(self.response, override.response),
            outputs=_merge_output_map(self.outputs, override.outputs),
            output_kinds={**self.output_kinds, **override.output_kinds},
            output_aliases={**self.output_aliases, **override.output_aliases},
            extra_fields=self.extra_fields.merge(override.extra_fields),
            validator=validator,
        )


class TypeOverrides(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    endpoints: dict[str, EndpointHints] = Field(default_factory=dict)

    def merge(self, override: TypeOverrides) -> TypeOverrides:
        merged = dict(self.endpoints)
        for endpoint_id, hints in override.endpoints.items():
            base = merged.get(endpoint_id)
            merged[endpoint_id] = base.merge(hints) if base else hints
        return TypeOverrides(endpoints=merged)


def _merge_field_map(
    base: dict[str, FieldHint],
    override: dict[str, FieldHint],
) -> dict[str, FieldHint]:
    if not override:
        return dict(base)
    merged = dict(base)
    for code, hint in override.items():
        existing = merged.get(code)
        merged[code] = existing.merge(hint) if existing else hint
    return merged


def _merge_output_map(
    base: dict[str, dict[str, FieldHint]],
    override: dict[str, dict[str, FieldHint]],
) -> dict[str, dict[str, FieldHint]]:
    if not override:
        return dict(base)
    merged = dict(base)
    for output_code, output_fields in override.items():
        existing = merged.get(output_code, {})
        merged[output_code] = _merge_field_map(existing, output_fields)
    return merged


__all__ = [
    "EndpointHints",
    "ExtraFields",
    "FieldHint",
    "FieldKind",
    "ResponseValidationMode",
    "RuleScope",
    "RuleSeverity",
    "TypeOverrides",
    "ValidatorCapture",
    "ValidatorError",
    "ValidatorRule",
    "ValidatorRuleType",
    "ValidatorSpec",
    "ValidatorWhen",
]
