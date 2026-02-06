from __future__ import annotations

from pykis.api.errors import KisResponseIncompleteError, KisResponseUnavailableError
from pykis.api.validation import (
    AllFieldsSentinel,
    AnyFieldMissing,
    ErrorConfig,
    OutputRequired,
    ValidationContext,
    evaluate_validators,
)


def _context() -> ValidationContext:
    return ValidationContext(
        endpoint_id="endpoint",
        domain="demo",
        method="GET",
        path="/path",
        status_code=200,
        request_id="req-id",
    )


def test_output_required_missing_output_raises() -> None:
    rule = OutputRequired(
        id="output_required",
        output="output",
        error=ErrorConfig(
            code="KIS_RESPONSE_INCOMPLETE",
            message="output missing",
            user_message="응답이 비어 있습니다.",
            exception=KisResponseUnavailableError,
        ),
    )
    payload: dict[str, object] = {"rt_cd": "0"}
    result = evaluate_validators((rule,), payload, _context(), mode="raise")
    assert not result.is_valid
    assert isinstance(result.error, KisResponseUnavailableError)
    assert result.error.rule_id == "output_required"


def test_all_fields_sentinel_first_row() -> None:
    rule = AllFieldsSentinel(
        id="sentinel",
        output="output",
        fields=("a", "b"),
        sentinel_values=("", "0"),
        scope="first_row",
        error=ErrorConfig(
            code="KIS_RESPONSE_UNAVAILABLE",
            message="sentinel",
            user_message="데이터 없음",
            exception=KisResponseUnavailableError,
        ),
    )
    payload = {"output": [{"a": "", "b": "0"}]}
    result = evaluate_validators((rule,), payload, _context(), mode="raise")
    assert not result.is_valid
    assert result.error is not None
    assert result.error.rule_type == "all_fields_sentinel"


def test_any_field_missing_any_row() -> None:
    rule = AnyFieldMissing(
        id="missing",
        output="output",
        fields=("a", "b"),
        scope="any_row",
        error=ErrorConfig(
            code="KIS_RESPONSE_INCOMPLETE",
            message="missing",
            user_message="필수 필드 누락",
            exception=KisResponseUnavailableError,
        ),
    )
    payload = {"output": [{"a": 1}, {"a": 2, "b": 3}]}
    result = evaluate_validators((rule,), payload, _context(), mode="raise")
    assert not result.is_valid
    assert result.error is not None


def test_rule_mode_overrides_client_mode() -> None:
    rule = OutputRequired(
        id="output_required",
        output="output",
        mode="warn",
        error=ErrorConfig(
            code="KIS_RESPONSE_INCOMPLETE",
            message="output missing",
            user_message="응답이 비어 있습니다.",
            exception=KisResponseUnavailableError,
        ),
    )
    payload: dict[str, object] = {}
    result = evaluate_validators((rule,), payload, _context(), mode="raise")
    assert result.mode == "warn"


def test_validators_skip_rt_cd_errors() -> None:
    rule = OutputRequired(
        id="output_required",
        output="output",
        error=ErrorConfig(
            code="KIS_RESPONSE_INCOMPLETE",
            message="output missing",
            user_message="응답이 비어 있습니다.",
            exception=KisResponseUnavailableError,
        ),
    )
    payload: dict[str, object] = {"rt_cd": "1"}
    result = evaluate_validators((rule,), payload, _context(), mode="raise")
    assert result.is_valid


def test_fallback_output_required_when_ok_but_empty() -> None:
    payload: dict[str, object] = {"rt_cd": "0", "msg_cd": "MCA00000", "msg1": "정상"}
    result = evaluate_validators((), payload, _context(), mode="raise")
    assert not result.is_valid
    assert isinstance(result.error, KisResponseIncompleteError)
    assert result.error.rule_id == "implicit_output_required"
    assert result.error.rule_type == "output_required"


def test_fallback_output_required_uses_output_keys() -> None:
    payload: dict[str, object] = {"rt_cd": "0", "output1": []}
    result = evaluate_validators((), payload, _context(), mode="raise")
    assert not result.is_valid
    assert isinstance(result.error, KisResponseIncompleteError)


def test_fallback_output_required_allows_non_empty_output() -> None:
    payload: dict[str, object] = {"rt_cd": "0", "output1": [{"a": 1}]}
    result = evaluate_validators((), payload, _context(), mode="raise")
    assert result.is_valid
