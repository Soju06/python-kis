from __future__ import annotations

from decimal import Decimal
from typing import Iterable, Mapping, Sequence, TypeVar, cast

from pykis.api.errors import KisErrorContext, KisInvalidResponseError, KisResponseIncompleteError
from pykis.api.validation.rules import (
    AllFieldsMissing,
    AllFieldsSentinel,
    AnyFieldMissing,
    AnyFieldSentinel,
    OutputRequired,
    ValidatorRule,
)
from pykis.api.validation.types import (
    FieldEvaluation,
    ResponseValidationMode,
    RowEvaluation,
    RuleDetails,
    ValidationContext,
    ValidationDetails,
    ValidationResult,
)

_RULE_TYPE_MAP: dict[type[object], str] = {
    OutputRequired: "output_required",
    AllFieldsSentinel: "all_fields_sentinel",
    AnyFieldSentinel: "any_field_sentinel",
    AllFieldsMissing: "all_fields_missing",
    AnyFieldMissing: "any_field_missing",
}

_T = TypeVar("_T")


def evaluate_validators(
    validators: tuple[ValidatorRule, ...],
    payload: Mapping[str, object],
    context: ValidationContext,
    *,
    mode: ResponseValidationMode,
) -> ValidationResult:
    if _rt_cd_error(payload):
        return ValidationResult.ok()
    if not validators:
        fallback = _fallback_output_required(payload, context, mode)
        if fallback is not None:
            return fallback
    for rule in validators:
        if not _matches_when(rule, payload):
            continue
        result = _evaluate_rule(rule, payload, context, mode)
        if not result.is_valid:
            return result
    return ValidationResult.ok()


def _rt_cd_error(payload: Mapping[str, object]) -> bool:
    rt_cd = str(payload.get("rt_cd") or "").strip()
    return bool(rt_cd) and rt_cd not in {"0", "OK"}


def _fallback_output_required(
    payload: Mapping[str, object],
    context: ValidationContext,
    mode: ResponseValidationMode,
) -> ValidationResult | None:
    output_keys = _output_keys(payload)
    if output_keys:
        if all(_is_empty_container(payload.get(key)) for key in output_keys):
            return _build_fallback_error(payload, context, mode, output_keys, reason="output_empty")
        return None
    if _has_non_meta_data(payload):
        return None
    return _build_fallback_error(payload, context, mode, output_keys, reason="output_missing")


def _output_keys(payload: Mapping[str, object]) -> list[str]:
    keys: list[str] = []
    for key in payload:
        if key.startswith(("output", "outblock")):
            keys.append(str(key))
    return keys


def _is_empty_container(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, list):
        return len(value) == 0
    if isinstance(value, dict):
        return len(value) == 0
    return False


def _has_non_meta_data(payload: Mapping[str, object]) -> bool:
    for key, value in payload.items():
        if key in {"rt_cd", "msg_cd", "msg1"}:
            continue
        if _is_empty_container(value):
            continue
        return True
    return False


def _build_fallback_error(
    payload: Mapping[str, object],
    context: ValidationContext,
    mode: ResponseValidationMode,
    output_keys: list[str],
    *,
    reason: str,
) -> ValidationResult:
    details = ValidationDetails(
        rule=RuleDetails(
            id="implicit_output_required",
            type="output_required",
            predicates={"outputs": output_keys, "reason": reason},
            when=None,
            severity=None,
        ),
        evaluated_rows=(
            RowEvaluation(
                row_index=0,
                fields=tuple(
                    FieldEvaluation(
                        field=key,
                        value=payload.get(key),
                        state="missing" if payload.get(key) is None else "sentinel",
                    )
                    for key in (output_keys or ["output"])
                ),
            ),
        ),
    )
    error_context = KisErrorContext(
        endpoint_id=context.endpoint_id,
        method=context.method,
        path=context.path,
        status_code=context.status_code,
        message="Response output missing",
        domain=context.domain,
        request_id=context.request_id,
    )
    excerpt: dict[str, object] = {}
    for key in ("rt_cd", "msg_cd", "msg1"):
        if key in payload:
            excerpt[key] = payload.get(key)
    if output_keys:
        for key in output_keys:
            excerpt[key] = payload.get(key)
    error = KisResponseIncompleteError(
        "Response output missing",
        context=error_context,
        payload=excerpt,
        error_code="KIS_RESPONSE_INCOMPLETE",
        user_message="응답 데이터가 비어 있습니다.",
        rule_id="implicit_output_required",
        rule_type="output_required",
        details=details,
    )
    return ValidationResult(is_valid=False, error=error, mode=mode, details=details)


def _matches_when(rule: ValidatorRule, payload: Mapping[str, object]) -> bool:
    when = getattr(rule, "when", None)
    if when is None:
        return True
    if when.rt_cd:
        rt_cd = str(payload.get("rt_cd") or "")
        if rt_cd not in when.rt_cd:
            return False
    if when.msg_cd:
        msg_cd = str(payload.get("msg_cd") or "")
        if msg_cd not in when.msg_cd:
            return False
    return True


def _evaluate_rule(
    rule: ValidatorRule,
    payload: Mapping[str, object],
    context: ValidationContext,
    mode: ResponseValidationMode,
) -> ValidationResult:
    match rule:
        case OutputRequired():
            return _eval_output_required(rule, payload, context, mode)
        case AllFieldsSentinel():
            return _eval_fields_sentinel(rule, payload, context, mode, require_all=True)
        case AnyFieldSentinel():
            return _eval_fields_sentinel(rule, payload, context, mode, require_all=False)
        case AllFieldsMissing():
            return _eval_fields_missing(rule, payload, context, mode, require_all=True)
        case AnyFieldMissing():
            return _eval_fields_missing(rule, payload, context, mode, require_all=False)
        case _:
            raise ValueError(f"Unknown rule type: {type(rule)}")


def _eval_output_required(
    rule: OutputRequired, payload: Mapping[str, object], context: ValidationContext, mode: ResponseValidationMode
) -> ValidationResult:
    output_value = payload.get(rule.output)
    missing = output_value is None
    empty = False
    invalid_type = False
    if isinstance(output_value, list):
        empty = len(output_value) == 0
    elif isinstance(output_value, dict):
        empty = len(output_value) == 0
    elif output_value is not None:
        invalid_type = True

    if missing or empty or invalid_type:
        evaluated = (
            RowEvaluation(
                row_index=0,
                fields=(
                    FieldEvaluation(field=rule.output, value=output_value, state="missing" if missing else "sentinel"),
                ),
            ),
        )
        return _build_failure(rule, payload, context, evaluated, mode)
    return ValidationResult.ok()


def _eval_fields_sentinel(
    rule: AllFieldsSentinel | AnyFieldSentinel,
    payload: Mapping[str, object],
    context: ValidationContext,
    mode: ResponseValidationMode,
    *,
    require_all: bool,
) -> ValidationResult:
    rows = _rows_for_output(payload, rule.output)
    if rows is None or not rows:
        return ValidationResult.ok()

    checked_rows = _rows_for_scope(rows, rule.scope)
    sentinel_values = _normalize_sentinel_values(rule.sentinel_values)
    evaluated_rows: list[RowEvaluation] = []
    matches: list[bool] = []

    for row_index, row in checked_rows:
        evaluations: list[FieldEvaluation] = []
        field_matches = 0
        for field in rule.fields:
            if field not in row:
                evaluations.append(FieldEvaluation(field=field, value=None, state="missing"))
                continue
            value = row.get(field)
            is_sentinel = _is_sentinel(value, sentinel_values)
            evaluations.append(FieldEvaluation(field=field, value=value, state="sentinel" if is_sentinel else "ok"))
            if is_sentinel:
                field_matches += 1
        match = field_matches == len(rule.fields) if require_all else field_matches > 0
        matches.append(match)
        evaluated_rows.append(RowEvaluation(row_index=row_index, fields=tuple(evaluations)))

    if _scope_matches(rule.scope, matches):
        return _build_failure(rule, payload, context, tuple(evaluated_rows), mode)
    return ValidationResult.ok()


def _eval_fields_missing(
    rule: AllFieldsMissing | AnyFieldMissing,
    payload: Mapping[str, object],
    context: ValidationContext,
    mode: ResponseValidationMode,
    *,
    require_all: bool,
) -> ValidationResult:
    rows = _rows_for_output(payload, rule.output)
    if rows is None or not rows:
        return ValidationResult.ok()

    checked_rows = _rows_for_scope(rows, rule.scope)
    evaluated_rows: list[RowEvaluation] = []
    matches: list[bool] = []

    for row_index, row in checked_rows:
        evaluations: list[FieldEvaluation] = []
        missing_count = 0
        for field in rule.fields:
            if field not in row:
                evaluations.append(FieldEvaluation(field=field, value=None, state="missing"))
                missing_count += 1
            else:
                evaluations.append(FieldEvaluation(field=field, value=row.get(field), state="ok"))
        match = missing_count == len(rule.fields) if require_all else missing_count > 0
        matches.append(match)
        evaluated_rows.append(RowEvaluation(row_index=row_index, fields=tuple(evaluations)))

    if _scope_matches(rule.scope, matches):
        return _build_failure(rule, payload, context, tuple(evaluated_rows), mode)
    return ValidationResult.ok()


def _build_failure(
    rule: ValidatorRule,
    payload: Mapping[str, object],
    context: ValidationContext,
    evaluated_rows: Sequence[RowEvaluation],
    mode: ResponseValidationMode,
) -> ValidationResult:
    rule_type = _rule_type(rule)
    details = ValidationDetails(
        rule=RuleDetails(
            id=rule.id,
            type=rule_type,
            predicates=_rule_predicates(rule),
            when=getattr(rule, "when", None),
            severity=rule.severity,
        ),
        evaluated_rows=tuple(evaluated_rows) if evaluated_rows else None,
    )
    capture = _capture_payload(rule, payload)
    excerpt = _payload_excerpt(rule, payload, capture)
    error_type = rule.error.exception if rule.error.exception else KisInvalidResponseError
    error_context = KisErrorContext(
        endpoint_id=context.endpoint_id,
        method=context.method,
        path=context.path,
        status_code=context.status_code,
        message=rule.error.message,
        domain=context.domain,
        request_id=context.request_id,
    )
    error = error_type(
        rule.error.message,
        context=error_context,
        payload=excerpt,
        error_code=rule.error.code,
        user_message=rule.error.user_message,
        hint=rule.error.hint,
        rule_id=rule.id,
        rule_type=rule_type,
        details=details,
    )
    return ValidationResult(is_valid=False, error=error, mode=rule.mode or mode, details=details)


def _rule_type(rule: ValidatorRule) -> str:
    return _RULE_TYPE_MAP.get(type(rule), type(rule).__name__)


def _rule_predicates(rule: ValidatorRule) -> Mapping[str, object]:
    predicates: dict[str, object] = {"output": rule.output}
    if hasattr(rule, "fields"):
        predicates["fields"] = list(getattr(rule, "fields"))
    if hasattr(rule, "sentinel_values"):
        predicates["sentinel_values"] = list(getattr(rule, "sentinel_values"))
    if hasattr(rule, "scope"):
        predicates["scope"] = getattr(rule, "scope")
    return predicates


def _rows_for_output(payload: Mapping[str, object], output: str) -> list[Mapping[str, object]] | None:
    if output not in payload:
        return None
    container = payload.get(output)
    if isinstance(container, list):
        rows: list[Mapping[str, object]] = []
        for item in container:
            if isinstance(item, Mapping):
                rows.append(_coerce_row(cast(Mapping[object, object], item)))
        return rows
    if isinstance(container, Mapping):
        return [_coerce_row(cast(Mapping[object, object], container))]
    return None


def _rows_for_scope(rows: Sequence[Mapping[str, object]], scope: str | None) -> list[tuple[int, Mapping[str, object]]]:
    indexed = list(enumerate(rows))
    if scope == "first_row":
        return indexed[:1]
    return indexed


def _scope_matches(scope: str | None, matches: Sequence[bool]) -> bool:
    if not matches:
        return False
    if scope == "any_row":
        return any(matches)
    if scope == "all_rows":
        return all(matches)
    return matches[0]


def _normalize_sentinel_values(values: Iterable[str | None]) -> set[str | None]:
    return {_normalize_value(value) for value in values}


def _normalize_value(value: object | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float, Decimal)):
        return str(value)
    return str(value).strip()


def _is_sentinel(value: object | None, sentinel_values: set[str | None]) -> bool:
    return _normalize_value(value) in sentinel_values


def _capture_payload(rule: ValidatorRule, payload: Mapping[str, object]) -> dict[str, object]:
    capture = getattr(rule, "capture", None)
    outputs = capture.outputs if capture and capture.outputs else (rule.output,)
    fields = capture.fields if capture and capture.fields else getattr(rule, "fields", None)
    max_rows = capture.max_rows if capture and capture.max_rows is not None else 1
    redact_keys = capture.redact_keys if capture and capture.redact_keys else ()

    captured: dict[str, object] = {}
    for output in outputs:
        container = payload.get(output)
        if isinstance(container, list):
            rows: list[object] = []
            for item in container[:max_rows]:
                if isinstance(item, Mapping):
                    rows.append(_select_fields(_coerce_row(cast(Mapping[object, object], item)), fields))
                else:
                    rows.append(item)
            captured[output] = rows
        elif isinstance(container, Mapping):
            captured[output] = _select_fields(_coerce_row(cast(Mapping[object, object], container)), fields)
        elif container is not None:
            captured[output] = container
    return _redact(captured, redact_keys)


def _payload_excerpt(
    rule: ValidatorRule,
    payload: Mapping[str, object],
    capture: Mapping[str, object],
) -> dict[str, object]:
    excerpt: dict[str, object] = {}
    for key in ("rt_cd", "msg_cd", "msg1"):
        if key in payload:
            excerpt[key] = payload.get(key)
    for key, value in capture.items():
        excerpt.setdefault(key, value)
    return excerpt


def _select_fields(row: Mapping[str, object], fields: Iterable[str] | None) -> dict[str, object]:
    if not fields:
        return {str(key): value for key, value in row.items()}
    selected: dict[str, object] = {}
    for field in fields:
        if field in row:
            selected[field] = row.get(field)
    return selected


def _redact(payload: _T, redact_keys: Iterable[str]) -> _T:
    keys = {key.lower() for key in redact_keys}
    if not keys:
        return payload
    return cast(_T, _redact_value(payload, keys))


def _redact_value(value: object, redact_keys: set[str]) -> object:
    if isinstance(value, list):
        return [_redact_value(item, redact_keys) for item in value]
    if isinstance(value, Mapping):
        redacted: dict[str, object] = {}
        for key, item in value.items():
            if str(key).lower() in redact_keys:
                redacted[str(key)] = "***"
            else:
                redacted[str(key)] = _redact_value(item, redact_keys)
        return redacted
    return value


def _coerce_row(row: Mapping[object, object]) -> dict[str, object]:
    return {str(key): value for key, value in row.items()}


__all__ = ["evaluate_validators"]
