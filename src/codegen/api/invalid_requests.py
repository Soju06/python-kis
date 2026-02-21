from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Annotated, Iterable, Mapping, get_args, get_origin

from pydantic import BaseModel

from codegen.api.models import EndpointSpec, SpecField
from codegen.core.enums import parse_enum_values
from codegen.core.types import JsonValue

_INVALID_SKIP_FIELDS = frozenset(
    {
        "appkey",
        "appsecret",
        "authorization",
        "custtype",
        "grant_type",
        "user_id",
        "userid",
        "cano",
        "acnt_prdt_cd",
    }
)

_INVALID_SKIP_TOKENS = (
    "appkey",
    "appsecret",
    "authorization",
    "hashkey",
    "token",
    "secret",
    "grant_type",
    "custtype",
    "user_id",
    "userid",
    "cano",
    "acnt_prdt_cd",
    "acca_dvsn",
    "account",
    "acct",
    "password",
    "passwd",
    "approval",
    "ctx_area",
    "tr_cont",
    "tr_cont_key",
    "page",
    "next",
    "prev",
    "seq",
)
_INVALID_SKIP_NAME_TOKENS = (
    "연속",
    "연속조회",
    "연속 조회",
    "다음",
    "이전",
    "페이지",
    "계좌",
    "비밀번호",
    "패스",
    "토큰",
    "인증",
    "해시키",
)

_INSTRUMENT_TOKENS = ("iscd", "pdno", "symbol", "symb", "stk", "stock", "ticker", "종목", "상품", "지수")
_CODE_TOKENS = ("code", "cls", "cd", "div", "type", "gb", "gubn", "구분", "분류", "코드", "시장")
_DATE_TOKENS = ("date", "_dt", "ymd", "bass_dt", "bsop_date", "일자", "날짜", "기준일")
_TIME_TOKENS = ("time", "hour", "tm", "시간", "시각")


@dataclass(frozen=True, slots=True)
class InvalidTemplate:
    values: dict[str, JsonValue]
    reason: str
    fields: tuple[str, ...]


def build_invalid_template(
    endpoint: EndpointSpec,
    request_model: type[BaseModel],
    query: Mapping[str, JsonValue],
    body: Mapping[str, JsonValue],
) -> InvalidTemplate | None:
    annotations = _request_field_annotations(request_model)
    candidates: list[_Candidate] = []
    for field in [*endpoint.request.query, *endpoint.request.body]:
        code = field.code
        if _should_skip_field(field):
            continue
        annotation = annotations.get(code)
        if annotation is None:
            continue
        if _is_enum_annotation(annotation):
            continue
        if not _is_str_like(annotation):
            continue
        kind = _field_kind(field)
        current = _current_value(code, query, body)
        value = _invalid_value_for(field, kind, current)
        if _is_etf_endpoint(endpoint) and kind == "instrument" and "iscd" in code.lower():
            value = _ensure_diff(_fit_length("005930", _parse_length(field)), current, _parse_length(field))
        if value is None:
            continue
        candidates.append(
            _Candidate(
                code=code,
                value=value,
                kind=kind,
                score=_score(kind, field),
                required=field.required,
            )
        )

    if not candidates:
        return None

    if _is_etf_endpoint(endpoint):
        instrument_candidates = [candidate for candidate in candidates if candidate.kind == "instrument"]
        if instrument_candidates:
            candidates = instrument_candidates

    required_candidates = [candidate for candidate in candidates if candidate.required]
    if required_candidates:
        candidates = required_candidates

    candidates.sort(key=lambda item: item.score, reverse=True)
    selected = candidates[:2]
    values = {item.code: item.value for item in selected}
    reason = ", ".join(item.kind for item in selected)
    fields = tuple(item.code for item in selected)
    return InvalidTemplate(values=values, reason=reason, fields=fields)


@dataclass(frozen=True, slots=True)
class _Candidate:
    code: str
    value: JsonValue
    kind: str
    score: int
    required: bool = False


def _request_field_annotations(request_model: type[BaseModel]) -> dict[str, object]:
    annotations: dict[str, object] = {}
    for name, field in request_model.model_fields.items():
        alias = field.serialization_alias or field.alias or name
        annotations[str(alias)] = field.annotation
    return annotations


def _should_skip_field(field: SpecField) -> bool:
    code = field.code.lower()
    if code in _INVALID_SKIP_FIELDS:
        return True
    if any(token in code for token in _INVALID_SKIP_TOKENS):
        return True
    name = field.name or ""
    description = field.description or ""
    haystack = f"{name} {description}".lower()
    return any(token in haystack for token in _INVALID_SKIP_NAME_TOKENS)


def _strip_annotated(annotation: object) -> object:
    if get_origin(annotation) is Annotated:
        return get_args(annotation)[0]
    return annotation


def _flatten_types(annotation: object) -> Iterable[object]:
    annotation = _strip_annotated(annotation)
    origin = get_origin(annotation)
    if origin is None:
        return (annotation,)
    return get_args(annotation)


def _is_enum_annotation(annotation: object) -> bool:
    for candidate in _flatten_types(annotation):
        if isinstance(candidate, type) and issubclass(candidate, Enum):
            return True
    return False


def _is_str_like(annotation: object) -> bool:
    for candidate in _flatten_types(annotation):
        if candidate is str:
            return True
    return False


def _field_kind(field: SpecField) -> str:
    name = field.name or ""
    description = field.description or ""
    lowered = f"{field.code} {name} {description}".lower()
    if any(token in lowered for token in _INSTRUMENT_TOKENS):
        return "instrument"
    if any(token in lowered for token in _CODE_TOKENS):
        return "code"
    if any(token in lowered for token in _DATE_TOKENS):
        return "date"
    if any(token in lowered for token in _TIME_TOKENS):
        return "time"
    return "generic"


def _score(kind: str, field: SpecField) -> int:
    if kind == "instrument":
        score = 100
    elif kind == "code":
        score = 80
    elif kind in {"date", "time"}:
        score = 60
    else:
        score = 10

    if field.required:
        score += 25
    length = _parse_length(field)
    if length and 2 <= length <= 10:
        score += 5
    return score


def _is_etf_endpoint(endpoint: EndpointSpec) -> bool:
    path = endpoint.path.lower()
    return "/etf" in path or "/etn" in path


def _parse_length(field: SpecField) -> int | None:
    if not field.length:
        return None
    digits = "".join(ch for ch in field.length if ch.isdigit())
    if not digits:
        return None
    try:
        value = int(digits)
    except ValueError:
        return None
    return value if value > 0 else None


def _invalid_value_for(field: SpecField, kind: str, current: JsonValue | None) -> str | None:
    length = _parse_length(field)
    enum_values = parse_enum_values(field.description)
    if enum_values:
        return _invalid_enum_value(enum_values, length, current)

    if kind == "instrument":
        return _ensure_diff(_repeat_value("0", length or 6), current, length)
    if kind == "code":
        return _ensure_diff(_repeat_value("9", length or 2), current, length)
    if kind == "date":
        return _ensure_diff(_repeat_value("0", length or 8), current, length)
    if kind == "time":
        return _ensure_diff(_repeat_value("9", length or 6), current, length)
    return _ensure_diff(_fit_length("INVALID", length), current, length)


def _invalid_enum_value(values: list[str], length: int | None, current: JsonValue | None) -> str:
    candidates = []
    if length:
        candidates.append(_repeat_value("9", length))
        candidates.append(_repeat_value("0", length))
        candidates.append(_repeat_value("Z", length))
    candidates += ["Z", "9", "UNKNOWN", "INVALID"]
    current_value = str(current) if current is not None else None
    for candidate in candidates:
        adjusted = _fit_length(candidate, length)
        if adjusted in values:
            continue
        if current_value and adjusted == current_value:
            continue
        return adjusted
    return _ensure_diff(_fit_length("INVALID", length), current, length)


def _repeat_value(ch: str, length: int) -> str:
    return ch * max(1, length)


def _fit_length(value: str, length: int | None) -> str:
    if not length:
        return value
    if len(value) == length:
        return value
    if len(value) > length:
        return value[:length]
    pad_char = value[-1] if value else "X"
    return value + (pad_char * (length - len(value)))


def _ensure_diff(value: str, current: JsonValue | None, length: int | None) -> str:
    current_value = str(current) if current is not None else None
    if current_value and value == current_value:
        if set(value) == {"0"}:
            value = _repeat_value("9", length or len(value))
        else:
            value = f"{value}1"
    return _fit_length(value, length)


def _current_value(code: str, query: Mapping[str, JsonValue], body: Mapping[str, JsonValue]) -> JsonValue | None:
    if code in query:
        return query.get(code)
    if code in body:
        return body.get(code)
    return None


__all__ = ["InvalidTemplate", "build_invalid_template"]
