from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Mapping

from pykis.api.errors import KisResponseError

ResponseValidationMode = Literal["raise", "warn", "ignore"]
RuleSeverity = Literal["error", "warn"]
RuleScope = Literal["first_row", "all_rows", "any_row"]
FieldState = Literal["ok", "missing", "sentinel"]


@dataclass(frozen=True, slots=True)
class RuleWhen:
    rt_cd: tuple[str, ...] | None = None
    msg_cd: tuple[str, ...] | None = None


@dataclass(frozen=True, slots=True)
class RuleCapture:
    fields: tuple[str, ...] | None = None
    outputs: tuple[str, ...] | None = None
    max_rows: int | None = None
    redact_keys: tuple[str, ...] | None = None


@dataclass(frozen=True, slots=True)
class ValidationContext:
    endpoint_id: str | None
    method: str | None
    path: str | None
    status_code: int | None
    domain: str | None
    request_id: str | None


@dataclass(frozen=True, slots=True)
class FieldEvaluation:
    field: str
    value: object | None
    state: FieldState


@dataclass(frozen=True, slots=True)
class RowEvaluation:
    row_index: int
    fields: tuple[FieldEvaluation, ...]


@dataclass(frozen=True, slots=True)
class RuleDetails:
    id: str
    type: str
    predicates: Mapping[str, object]
    when: RuleWhen | None
    severity: RuleSeverity | None


@dataclass(frozen=True, slots=True)
class ValidationDetails:
    rule: RuleDetails
    evaluated_rows: tuple[RowEvaluation, ...] | None


@dataclass(frozen=True, slots=True)
class ValidationResult:
    is_valid: bool
    error: KisResponseError | None = None
    mode: ResponseValidationMode | None = None
    details: ValidationDetails | None = None

    @classmethod
    def ok(cls) -> ValidationResult:
        return cls(is_valid=True)


__all__ = [
    "FieldEvaluation",
    "FieldState",
    "ResponseValidationMode",
    "RowEvaluation",
    "RuleCapture",
    "RuleDetails",
    "RuleScope",
    "RuleSeverity",
    "RuleWhen",
    "ValidationContext",
    "ValidationDetails",
    "ValidationResult",
]
