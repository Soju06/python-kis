from __future__ import annotations

from dataclasses import dataclass

from pykis.api.errors import KisResponseError
from pykis.api.validation.types import ResponseValidationMode, RuleCapture, RuleScope, RuleSeverity, RuleWhen


@dataclass(frozen=True, slots=True)
class ErrorConfig:
    code: str
    message: str
    user_message: str
    hint: str | None = None
    exception: type[KisResponseError] = KisResponseError


@dataclass(frozen=True, slots=True)
class OutputRequired:
    id: str
    output: str
    error: ErrorConfig
    when: RuleWhen | None = None
    mode: ResponseValidationMode | None = None
    severity: RuleSeverity | None = None
    capture: RuleCapture | None = None


@dataclass(frozen=True, slots=True)
class AllFieldsSentinel:
    id: str
    output: str
    fields: tuple[str, ...]
    sentinel_values: tuple[str | None, ...]
    error: ErrorConfig
    scope: RuleScope | None = None
    when: RuleWhen | None = None
    mode: ResponseValidationMode | None = None
    severity: RuleSeverity | None = None
    capture: RuleCapture | None = None


@dataclass(frozen=True, slots=True)
class AnyFieldSentinel:
    id: str
    output: str
    fields: tuple[str, ...]
    sentinel_values: tuple[str | None, ...]
    error: ErrorConfig
    scope: RuleScope | None = None
    when: RuleWhen | None = None
    mode: ResponseValidationMode | None = None
    severity: RuleSeverity | None = None
    capture: RuleCapture | None = None


@dataclass(frozen=True, slots=True)
class AllFieldsMissing:
    id: str
    output: str
    fields: tuple[str, ...]
    error: ErrorConfig
    scope: RuleScope | None = None
    when: RuleWhen | None = None
    mode: ResponseValidationMode | None = None
    severity: RuleSeverity | None = None
    capture: RuleCapture | None = None


@dataclass(frozen=True, slots=True)
class AnyFieldMissing:
    id: str
    output: str
    fields: tuple[str, ...]
    error: ErrorConfig
    scope: RuleScope | None = None
    when: RuleWhen | None = None
    mode: ResponseValidationMode | None = None
    severity: RuleSeverity | None = None
    capture: RuleCapture | None = None


ValidatorRule = OutputRequired | AllFieldsSentinel | AnyFieldSentinel | AllFieldsMissing | AnyFieldMissing


__all__ = [
    "AllFieldsMissing",
    "AllFieldsSentinel",
    "AnyFieldMissing",
    "AnyFieldSentinel",
    "ErrorConfig",
    "OutputRequired",
    "RuleCapture",
    "RuleScope",
    "RuleSeverity",
    "RuleWhen",
    "ValidatorRule",
]
