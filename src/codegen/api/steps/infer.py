from __future__ import annotations

import json
import re
from pathlib import Path

from codegen.api.models import EndpointSpec, SpecField
from codegen.api.report_models import ValidationReport, ValidationSampleResult
from codegen.api.runtime import SKIP_ENDPOINT_IDS, UNSAFE_KEYWORDS, is_empty_payload
from codegen.api.types import EndpointHints, ExtraFields, FieldHint, TypeOverrides
from codegen.core.enums import EnumEntry, parse_enum_entries
from codegen.core.text import is_blank_description
from codegen.core.types import JsonObject, JsonValue
from pykis.api.raw.types import Endpoint


def _text_flags(field: SpecField) -> str:
    parts = [field.code, field.name or "", field.description or "", field.type_name or ""]
    return " ".join(parts).lower()


def _is_unsafe(spec: EndpointSpec) -> bool:
    haystack = " ".join(filter(None, [spec.name, spec.section, spec.category, spec.subcategory, spec.path])).lower()
    return any(keyword.lower() in haystack for keyword in UNSAFE_KEYWORDS)


def _is_code_like(text: str) -> bool:
    return any(token in text for token in ("코드", "code", "iscd", "id", "번호", "종목"))


_DECIMAL_SPEC_RE = re.compile(r"\b\d+\s*\(\s*(\d+)\s*\.\s*(\d+)\s*\)")
_DECIMAL_TEXT_RE = re.compile(r"정수부분\s*(\d+)\s*자리.*?소수부분\s*(\d+)\s*자리")
_DT_TOKEN_RE = re.compile(r"(?<![a-z0-9])dt(?![a-z0-9])")
_RATE_TOKENS = ("비율", "율", "rate", "ratio", "percent", "pct", "ctrt")
_DATE_TOKENS = ("일자", "날짜", "기준일", "date", "ymd")


def _has_dt_token(text: str) -> bool:
    return bool(_DT_TOKEN_RE.search(text))


def _has_n_day_marker(text: str) -> bool:
    return "n일" in text


def _prefer_enum(text: str, code_lower: str, enum_entries: list[EnumEntry]) -> bool:
    if not enum_entries:
        return False
    if _has_n_day_marker(text):
        return True
    if any(token in text for token in ("구분", "분류", "코드", "dvsn", "gubn")):
        return True
    if code_lower.endswith("_cd") or code_lower.endswith("cd"):
        return True
    if code_lower.startswith("gb") or code_lower.startswith("gubn") or "dvsn" in code_lower:
        return True
    return False


def _decimal_spec(text: str) -> tuple[int, int] | None:
    match = _DECIMAL_TEXT_RE.search(text)
    if match:
        integer_digits = int(match.group(1))
        decimal_digits = int(match.group(2))
        if integer_digits > 0 and decimal_digits > 0:
            return integer_digits + decimal_digits, decimal_digits
    match = _DECIMAL_SPEC_RE.search(text)
    if match:
        integer_digits = int(match.group(1))
        decimal_digits = int(match.group(2))
        if integer_digits > 0 and decimal_digits > 0:
            return integer_digits + decimal_digits, decimal_digits
    return None


def _enum_sample_values(sample: JsonValue | None) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    items = sample if isinstance(sample, list) else [sample]
    for item in items:
        if item is None:
            continue
        if isinstance(item, str):
            text = item.strip()
        else:
            text = str(item)
        if not text or text in seen:
            continue
        seen.add(text)
        values.append(text)
    return values


def _values_numeric(values: list[str]) -> bool:
    return all(value.isdigit() for value in values)


def _preview_value(value: JsonValue | None, limit: int = 5) -> JsonValue | None:
    if isinstance(value, list):
        return value[:limit]
    if isinstance(value, dict):
        preview: dict[str, JsonValue] = {}
        for idx, (key, item) in enumerate(value.items()):
            if idx >= limit:
                break
            preview[str(key)] = item
        return preview
    return value


def _infer_kind(field: SpecField, sample: JsonValue | None, trace: JsonObject | None = None) -> FieldHint:
    text = _text_flags(field)
    code_lower = field.code.lower()
    sample_values = _enum_sample_values(sample)
    if isinstance(sample, list):
        sample = sample_values[0] if sample_values else None
    has_rate_token = any(token in text for token in _RATE_TOKENS)
    has_date_token = any(token in text for token in _DATE_TOKENS) or _has_dt_token(text)

    if trace is not None:
        trace.update(
            {
                "field": {
                    "code": field.code,
                    "name": field.name,
                    "type_name": field.type_name,
                },
                "text_flags": text,
                "sample": _preview_value(sample),
                "sample_values": sample_values[:5],
                "signals": {
                    "has_rate_token": has_rate_token,
                    "has_date_token": has_date_token,
                },
            }
        )

    def _final(hint: FieldHint, reason: str) -> FieldHint:
        if trace is not None:
            decision: JsonObject = {"kind": hint.kind, "reason": reason}
            if hint.enum:
                decision["enum"] = hint.enum
            if hint.enum_desc:
                decision["enum_desc"] = hint.enum_desc
            if hint.max_digits is not None:
                decision["max_digits"] = hint.max_digits
            if hint.decimal_places is not None:
                decision["decimal_places"] = hint.decimal_places
            trace["decision"] = decision
        return hint

    if field.code.lower() == "keyb":
        return _final(FieldHint(kind="str"), "special_keyb")
    if field.code.lower() in {"rsym", "symb"}:
        return _final(FieldHint(kind="str"), "symbol_field")
    if "y/n" in text or field.code.lower().endswith("_yn") or "여부" in text:
        return _final(FieldHint(kind="bool"), "boolean_yn")
    if "name" in code_lower or "명" in (field.name or ""):
        return _final(FieldHint(kind="str"), "name_field")
    if ("input" in code_lower or "iscd" in code_lower) and _is_code_like(text):
        return _final(FieldHint(kind="str"), "input_code_like")
    if any(token in text for token in ("yyyymm", "yyymm", "yymmww", "년월", "년월주차")):
        return _final(FieldHint(kind="str"), "year_month_token")

    enum_entries = parse_enum_entries(field.description or "")
    enum_values = [entry.code for entry in enum_entries]
    enum_desc = {entry.code: entry.desc for entry in enum_entries if entry.desc}
    enum_hint: FieldHint | None = None
    if enum_entries:
        normalized = {value.upper() for value in enum_values}
        if normalized.issubset({"Y", "N"}):
            enum_hint = FieldHint(kind="bool")
        elif len(enum_values) >= 2:
            if sample_values and any(value not in enum_values for value in sample_values):
                if _values_numeric(enum_values) and _values_numeric(sample_values):
                    for value in sample_values:
                        if value not in enum_values:
                            enum_values.append(value)
                else:
                    enum_hint = FieldHint(kind="str")
            if enum_hint is None:
                enum_hint = FieldHint(kind="enum", enum=enum_values, enum_desc=enum_desc or None)

    if trace is not None and enum_entries:
        trace["enum"] = {"values": enum_values, "desc": enum_desc or None}

    if enum_hint and _prefer_enum(text, code_lower, enum_entries):
        return _final(enum_hint, "enum_preferred")

    if any(token in text for token in ("일시", "datetime", "timestamp", "dtime")):
        return _final(FieldHint(kind="datetime"), "datetime_token")

    if has_date_token and has_rate_token:
        return _final(FieldHint(kind="decimal"), "rate_over_date")
    if has_date_token:
        return _final(FieldHint(kind="date"), "date_token")

    time_tokens = ("시각", "hhmm", "hhmmss", "time", "_tm", "hour")
    if "시간외" not in text and not _is_code_like(text) and any(token in text for token in time_tokens):
        return _final(FieldHint(kind="time"), "time_token")

    spec = _decimal_spec(text)
    if spec:
        max_digits, decimal_places = spec
        return _final(
            FieldHint(kind="decimal", max_digits=max_digits, decimal_places=decimal_places),
            "decimal_spec",
        )

    if enum_hint:
        if any(token in text for token in ("비트", "bit", "첫 번째", "두 번째", "첫번째", "두번째")):
            return _final(FieldHint(kind="str"), "enum_forced_str")
        return _final(enum_hint, "enum_default")

    if "vol" in code_lower and "volat" not in code_lower and "vltl" not in code_lower:
        rate_hint = any(
            token in text
            for token in (
                "비율",
                "율",
                "rate",
                "ratio",
                "percent",
                "pct",
                "ctrt",
                "rlim",
            )
        )
        return _final(FieldHint(kind="decimal" if rate_hint else "int"), "volume_token")

    if _is_code_like(text):
        return _final(FieldHint(kind="str"), "code_like")

    price_tokens = (
        "가격",
        "주가",
        "현재가",
        "시가",
        "고가",
        "저가",
        "지수",
        "금액",
        "대금",
        "amount",
        "price",
        "단일가",
    )
    rate_tokens = _RATE_TOKENS
    volume_tokens = ("수량", "거래량", "건수", "횟수", "volume", "count")

    if sample is not None:
        if isinstance(sample, (int,)):
            return _final(FieldHint(kind="int"), "sample_int")
        if isinstance(sample, (float,)):
            return _final(FieldHint(kind="decimal"), "sample_float")
        if isinstance(sample, str):
            value = sample.strip()
            if re.fullmatch(r"-?\d+\.\d+", value):
                return _final(FieldHint(kind="decimal"), "sample_decimal_str")
            if re.fullmatch(r"-?\d+", value):
                if len(value) == 8 and (
                    (any(token in text for token in ("일자", "날짜", "date", "ymd")) or _has_dt_token(text))
                    and not has_rate_token
                ):
                    return _final(FieldHint(kind="date"), "sample_date_str")
                if (
                    len(value) == 6
                    and "시간외" not in text
                    and any(token in text for token in ("시간", "시각", "time", "hhmmss", "hhmm"))
                ):
                    return _final(FieldHint(kind="time"), "sample_time_str")
                if any(token in text for token in price_tokens + rate_tokens):
                    return _final(FieldHint(kind="decimal"), "sample_numeric_price_or_rate")
                if any(token in text for token in volume_tokens):
                    return _final(FieldHint(kind="int"), "sample_numeric_volume")
                return _final(FieldHint(kind="int"), "sample_numeric_int")

    if any(token in text for token in price_tokens):
        return _final(FieldHint(kind="decimal"), "price_token")

    if any(token in text for token in rate_tokens):
        return _final(FieldHint(kind="decimal"), "rate_token")

    if any(token in text for token in volume_tokens):
        return _final(FieldHint(kind="int"), "volume_token_fallback")

    return _final(FieldHint(kind="str"), "fallback_str")


def _is_blank(value: JsonValue) -> bool:
    return isinstance(value, str) and not value.strip()


def _normalize_sample(value: JsonValue | None) -> tuple[JsonValue | None, bool]:
    if _is_blank(value):
        return None, True
    return value, False


def _is_zero_datetime(sample: JsonValue | None, kind: str | None) -> bool:
    if not isinstance(sample, str):
        return False
    text = sample.strip()
    if not text:
        return False
    if kind == "date" and text in {"0", "00000000"}:
        return True
    if kind == "time" and text in {"0", "000000", "0000"}:
        return True
    if kind == "datetime" and text in {"0", "00000000000000"}:
        return True
    return False


def _as_object(payload: JsonValue | None) -> JsonObject | None:
    if not isinstance(payload, dict):
        return None
    return {str(key): value for key, value in payload.items()}


def _sample_from_container(container: JsonValue | None, field: SpecField) -> tuple[JsonValue | None, bool]:
    if isinstance(container, list):
        values: list[JsonValue] = []
        found = False
        for item in container:
            item_dict = _as_object(item)
            if item_dict is None:
                continue
            if field.code in item_dict:
                found = True
                values.append(item_dict.get(field.code))
        if found:
            return values, True
    else:
        container_dict = _as_object(container)
        if container_dict is not None:
            return container_dict.get(field.code), field.code in container_dict
    return None, False


def infer_types(
    specs: list[EndpointSpec],
    augment_dir: Path,
    trace_out: dict[str, JsonObject] | None = None,
) -> TypeOverrides:
    endpoints: dict[str, EndpointHints] = {}

    for spec in specs:
        entry = EndpointHints(extra_fields=ExtraFields())
        trace_request: dict[str, JsonObject] | None = None
        trace_response: dict[str, JsonObject] | None = None
        trace_outputs: dict[str, dict[str, JsonObject]] | None = None
        trace_output_aliases: dict[str, str] | None = None
        trace_output_kinds: dict[str, str] | None = None
        if trace_out is not None:
            trace_request = {}
            trace_response = {}
            trace_outputs = {}
            trace_output_aliases = {}
            trace_output_kinds = {}
        success_path = augment_dir / spec.id / "success.json"
        raw_path = augment_dir / spec.id / "raw.json"
        request_path = augment_dir / spec.id / "request.json"
        raw_payload: JsonObject | None = None
        request_payload: JsonObject | None = None

        if success_path.exists():
            raw_payload = _as_object(json.loads(success_path.read_text(encoding="utf-8")))
        elif raw_path.exists():
            raw_payload = _as_object(json.loads(raw_path.read_text(encoding="utf-8")))
        if request_path.exists():
            request_payload = _as_object(json.loads(request_path.read_text(encoding="utf-8")))

        for field in spec.request.query:
            sample = None
            if request_payload:
                sample = _as_object(request_payload.get("query")) or {}
                sample = sample.get(field.code)
            trace: JsonObject | None = {} if trace_request is not None else None
            hint = _infer_kind(field, sample, trace=trace)
            if is_blank_description(field.description):
                hint.required = False
                if trace is not None:
                    trace["blank_allowed"] = True
            entry.request[field.code] = hint
            if trace_request is not None:
                trace_request[field.code] = trace or {}

        for field in spec.request.body:
            sample = None
            if request_payload:
                sample = _as_object(request_payload.get("body")) or {}
                sample = sample.get(field.code)
            trace = {} if trace_request is not None else None
            hint = _infer_kind(field, sample, trace=trace)
            if is_blank_description(field.description):
                hint.required = False
                if trace is not None:
                    trace["blank_allowed"] = True
            entry.request[field.code] = hint
            if trace_request is not None:
                trace_request[field.code] = trace or {}

        if raw_payload:
            output_codes = {output.code for output in spec.response.outputs}
            if "output" in raw_payload and "output" not in output_codes and len(output_codes) == 1:
                only_code = next(iter(output_codes))
                entry.output_aliases[only_code] = "output"
                if trace_output_aliases is not None:
                    trace_output_aliases[only_code] = "output"

        for field in spec.response.body:
            sample = raw_payload.get(field.code) if raw_payload else None
            sample, _ = _normalize_sample(sample)
            trace = {} if trace_response is not None else None
            hint = _infer_kind(field, sample, trace=trace)
            kind = hint.kind
            if field.required and _is_zero_datetime(sample, kind):
                hint.required = False
            if field.required and raw_payload and sample is None:
                hint.required = False
            entry.response[field.code] = hint
            if trace_response is not None:
                trace_response[field.code] = trace or {}

        if raw_payload:
            known_keys = {field.code for field in spec.response.body}
            known_keys.update(output.code for output in spec.response.outputs)
            known_keys.update(entry.output_aliases.values())
            for key, value in raw_payload.items():
                if key in known_keys:
                    continue
                if key in {"rt_cd", "msg_cd", "msg1"}:
                    continue
                field = SpecField.model_validate(
                    {
                        "code": key,
                        "name": key,
                        "type": "A0001",
                        "type_name": "String",
                        "required": False,
                        "description": "inferred from raw payload",
                    }
                )
                entry.extra_fields.response.append(field)
                trace = {} if trace_response is not None else None
                entry.response[key] = _infer_kind(field, value, trace=trace)
                if trace_response is not None:
                    trace_response[key] = trace or {}

        def _resolve_container(code: str) -> JsonValue | None:
            if not raw_payload:
                return None
            if code in raw_payload:
                return raw_payload.get(code)
            alias = entry.output_aliases.get(code)
            if isinstance(alias, str):
                return raw_payload.get(alias)
            return None

        for output in spec.response.outputs:
            container = _resolve_container(output.code)
            if isinstance(container, list):
                entry.output_kinds[output.code] = "array"
            elif isinstance(container, dict):
                entry.output_kinds[output.code] = "single"
            else:
                entry.output_kinds[output.code] = output.kind
            if trace_output_kinds is not None:
                trace_output_kinds[output.code] = entry.output_kinds[output.code]

            output_map: dict[str, FieldHint] = {}
            output_known = {field.code for field in output.fields}
            for field in output.fields:
                sample, _ = _sample_from_container(container, field)
                sample, _ = _normalize_sample(sample)
                trace = {} if trace_outputs is not None else None
                hint = _infer_kind(field, sample, trace=trace)
                kind = hint.kind
                if field.required and _is_zero_datetime(sample, kind):
                    hint.required = False
                if field.required and isinstance(container, (dict, list)) and sample is None:
                    hint.required = False
                if field.required and isinstance(container, list):
                    missing_in_list = any(isinstance(item, dict) and field.code not in item for item in container)
                    if missing_in_list:
                        hint.required = False
                    blank_in_list = any(
                        isinstance(item, dict) and field.code in item and _is_blank(item.get(field.code))
                        for item in container
                    )
                    if blank_in_list:
                        hint.required = False
                output_map[field.code] = hint
                if trace_outputs is not None:
                    trace_outputs.setdefault(output.code, {})[field.code] = trace or {}
            if isinstance(container, dict):
                extras: list[SpecField] = []
                for key, value in container.items():
                    key_str = str(key)
                    if key_str in output_known:
                        continue
                    field = SpecField.model_validate(
                        {
                            "code": key_str,
                            "name": key_str,
                            "type": "A0001",
                            "type_name": "String",
                            "required": False,
                            "description": "inferred from raw payload",
                        }
                    )
                    extras.append(field)
                    trace = {} if trace_outputs is not None else None
                    output_map[key_str] = _infer_kind(field, value, trace=trace)
                    if trace_outputs is not None:
                        trace_outputs.setdefault(output.code, {})[key_str] = trace or {}
                entry.extra_fields.outputs[output.code] = extras
            entry.outputs[output.code] = output_map

        endpoints[spec.id] = entry
        if trace_out is not None and trace_request is not None and trace_response is not None:
            trace_out[spec.id] = {
                "request": trace_request,
                "response": trace_response,
                "outputs": trace_outputs or {},
                "output_aliases": trace_output_aliases or {},
                "output_kinds": trace_output_kinds or {},
            }

    return TypeOverrides(endpoints=endpoints)


def validate_samples(
    specs: list[EndpointSpec],
    augment_dir: Path,
    registry: dict[str, Endpoint],
) -> ValidationReport:
    results: list[ValidationSampleResult] = []
    errors = 0
    for spec in specs:
        endpoint = registry.get(spec.id)
        if endpoint is None:
            continue
        if spec.id in SKIP_ENDPOINT_IDS:
            results.append(ValidationSampleResult(id=spec.id, status="skipped", reason="skip_endpoint"))
            continue
        if _is_unsafe(spec):
            results.append(ValidationSampleResult(id=spec.id, status="skipped", reason="unsafe"))
            continue
        domain = "demo" if spec.domains.demo else "real" if spec.domains.real else None
        if domain is None:
            results.append(ValidationSampleResult(id=spec.id, status="skipped", reason="no_domain"))
            continue
        raw_path = augment_dir / spec.id / "raw.json"
        if not raw_path.exists():
            errors += 1
            results.append(ValidationSampleResult(id=spec.id, domain=domain, status="missing_raw"))
            continue
        payload = _as_object(json.loads(raw_path.read_text(encoding="utf-8")))
        if payload is None:
            errors += 1
            results.append(ValidationSampleResult(id=spec.id, domain=domain, status="invalid_payload"))
            continue
        if str(payload.get("rt_cd")) not in ("0", "OK"):
            if is_empty_payload(payload):
                results.append(
                    ValidationSampleResult(
                        id=spec.id,
                        domain=domain,
                        status="skipped",
                        reason="empty_response",
                    )
                )
                continue
            errors += 1
            results.append(
                ValidationSampleResult(
                    id=spec.id,
                    domain=domain,
                    status="rt_cd_error",
                    reason=str(payload.get("msg1") or ""),
                )
            )
            continue
        try:
            endpoint.response_model.model_validate(payload)
            results.append(ValidationSampleResult(id=spec.id, domain=domain, status="ok"))
        except Exception as exc:  # noqa: BLE001
            errors += 1
            results.append(ValidationSampleResult(id=spec.id, domain=domain, status="error", reason=str(exc)))

    return ValidationReport(total=len(results), errors=errors, results=results)
