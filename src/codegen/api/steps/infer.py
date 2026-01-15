from __future__ import annotations

import json
import re
from pathlib import Path

from codegen.api.models import EndpointSpec, SpecField
from codegen.api.report_models import ValidationReport, ValidationSampleResult
from codegen.api.types import EndpointHints, ExtraFields, FieldHint, TypeOverrides
from codegen.core.enums import parse_enum_entries
from codegen.core.types import JsonObject, JsonValue
from pykis.api.raw.types import Endpoint


def _text_flags(field: SpecField) -> str:
    parts = [field.code, field.name or "", field.description or "", field.type_name or ""]
    return " ".join(parts).lower()


def _is_code_like(text: str) -> bool:
    return any(token in text for token in ("코드", "code", "iscd", "id", "번호", "종목"))


_DECIMAL_SPEC_RE = re.compile(r"\b\d+\s*\(\s*(\d+)\s*\.\s*(\d+)\s*\)")
_DECIMAL_TEXT_RE = re.compile(r"정수부분\s*(\d+)\s*자리.*?소수부분\s*(\d+)\s*자리")


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


def _infer_kind(field: SpecField, sample: JsonValue | None) -> FieldHint:
    text = _text_flags(field)
    if field.code.lower() == "keyb":
        return FieldHint(kind="str")
    if "y/n" in text or field.code.lower().endswith("_yn") or "여부" in text:
        return FieldHint(kind="bool")

    enum_entries = parse_enum_entries(field.description or "")
    if enum_entries:
        if any(token in text for token in ("비트", "bit", "첫 번째", "두 번째", "첫번째", "두번째")):
            return FieldHint(kind="str")
        enum_values = [entry.code for entry in enum_entries]
        enum_desc = {entry.code: entry.desc for entry in enum_entries if entry.desc}
        normalized = {value.upper() for value in enum_values}
        if normalized.issubset({"Y", "N"}):
            return FieldHint(kind="bool")
        if len(enum_values) >= 2:
            return FieldHint(kind="enum", enum=enum_values, enum_desc=enum_desc or None)

    spec = _decimal_spec(text)
    if spec:
        max_digits, decimal_places = spec
        return FieldHint(kind="decimal", max_digits=max_digits, decimal_places=decimal_places)

    if any(token in text for token in ("일자", "날짜", "기준일", "date", "ymd", "_dt")):
        return FieldHint(kind="date")

    time_tokens = ("시각", "hhmm", "hhmmss", "time", "_tm", "hour")
    if "시간외" not in text and not _is_code_like(text) and any(token in text for token in time_tokens):
        return FieldHint(kind="time")

    if any(token in text for token in ("일시", "datetime", "timestamp")):
        return FieldHint(kind="datetime")

    if _is_code_like(text):
        return FieldHint(kind="str")

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
    rate_tokens = ("비율", "율", "rate", "ratio", "percent", "pct", "ctrt")
    volume_tokens = ("수량", "거래량", "건수", "횟수", "volume", "count")

    if sample is not None:
        if isinstance(sample, (int,)):
            return FieldHint(kind="int")
        if isinstance(sample, (float,)):
            return FieldHint(kind="decimal")
        if isinstance(sample, str):
            value = sample.strip()
            if re.fullmatch(r"-?\d+\.\d+", value):
                return FieldHint(kind="decimal")
            if re.fullmatch(r"-?\d+", value):
                if len(value) == 8 and any(token in text for token in ("일자", "날짜", "date", "ymd")):
                    return FieldHint(kind="date")
                if len(value) == 6 and "시간외" not in text and any(
                    token in text for token in ("시간", "시각", "time", "hhmmss", "hhmm")
                ):
                    return FieldHint(kind="time")
                if any(token in text for token in price_tokens + rate_tokens):
                    return FieldHint(kind="decimal")
                if any(token in text for token in volume_tokens):
                    return FieldHint(kind="int")
                return FieldHint(kind="int")

    if any(token in text for token in price_tokens):
        return FieldHint(kind="decimal")

    if any(token in text for token in rate_tokens):
        return FieldHint(kind="decimal")

    if any(token in text for token in volume_tokens):
        return FieldHint(kind="int")

    return FieldHint(kind="str")


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
        if container:
            first = container[0]
            first_dict = _as_object(first)
            if first_dict is not None:
                return first_dict.get(field.code), field.code in first_dict
    else:
        container_dict = _as_object(container)
        if container_dict is not None:
            return container_dict.get(field.code), field.code in container_dict
    return None, False


def infer_types(specs: list[EndpointSpec], augment_dir: Path) -> TypeOverrides:
    endpoints: dict[str, EndpointHints] = {}

    for spec in specs:
        entry = EndpointHints(extra_fields=ExtraFields())
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
            entry.request[field.code] = _infer_kind(field, sample)

        for field in spec.request.body:
            sample = None
            if request_payload:
                sample = _as_object(request_payload.get("body")) or {}
                sample = sample.get(field.code)
            entry.request[field.code] = _infer_kind(field, sample)

        if raw_payload:
            output_codes = {output.code for output in spec.response.outputs}
            if "output" in raw_payload and "output" not in output_codes and len(output_codes) == 1:
                only_code = next(iter(output_codes))
                entry.output_aliases[only_code] = "output"

        for field in spec.response.body:
            sample = raw_payload.get(field.code) if raw_payload else None
            sample, _ = _normalize_sample(sample)
            hint = _infer_kind(field, sample)
            kind = hint.kind
            if field.required and _is_zero_datetime(sample, kind):
                hint.required = False
            if field.required and raw_payload and sample is None:
                hint.required = False
            entry.response[field.code] = hint

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
                entry.response[key] = _infer_kind(field, value)

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

            output_map: dict[str, FieldHint] = {}
            output_known = {field.code for field in output.fields}
            for field in output.fields:
                sample, _ = _sample_from_container(container, field)
                sample, _ = _normalize_sample(sample)
                hint = _infer_kind(field, sample)
                kind = hint.kind
                if field.required and _is_zero_datetime(sample, kind):
                    hint.required = False
                if field.required and isinstance(container, (dict, list)) and sample is None:
                    hint.required = False
                if field.required and isinstance(container, list):
                    missing_in_list = any(
                        isinstance(item, dict) and field.code not in item for item in container
                    )
                    if missing_in_list:
                        hint.required = False
                output_map[field.code] = hint
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
                    output_map[key_str] = _infer_kind(field, value)
                entry.extra_fields.outputs[output.code] = extras
            entry.outputs[output.code] = output_map

        endpoints[spec.id] = entry

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
        if not spec.domains.demo:
            results.append(ValidationSampleResult(id=spec.id, status="skipped", reason="demo_only"))
            continue
        raw_path = augment_dir / spec.id / "raw.json"
        if not raw_path.exists():
            errors += 1
            results.append(ValidationSampleResult(id=spec.id, status="missing_raw"))
            continue
        payload = _as_object(json.loads(raw_path.read_text(encoding="utf-8")))
        if payload is None:
            errors += 1
            results.append(ValidationSampleResult(id=spec.id, status="invalid_payload"))
            continue
        if str(payload.get("rt_cd")) not in ("0", "OK"):
            errors += 1
            results.append(
                ValidationSampleResult(
                    id=spec.id,
                    status="rt_cd_error",
                    reason=str(payload.get("msg1") or ""),
                )
            )
            continue
        try:
            endpoint.response_model.model_validate(payload)
            results.append(ValidationSampleResult(id=spec.id, status="ok"))
        except Exception as exc:  # noqa: BLE001
            errors += 1
            results.append(ValidationSampleResult(id=spec.id, status="error", reason=str(exc)))

    return ValidationReport(total=len(results), errors=errors, results=results)
