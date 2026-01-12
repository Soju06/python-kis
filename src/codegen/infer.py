from __future__ import annotations

import json
import re
from pathlib import Path

from .models import EndpointSpec, SpecField, SpecOutput

_ENUM_PATTERN = re.compile(r"\b([A-Za-z0-9]{1,8})\s*[:=]")


def _parse_enum(description: str | None) -> list[str]:
    if not description:
        return []
    candidates = []
    for match in _ENUM_PATTERN.finditer(description):
        code = match.group(1).strip()
        if not code:
            continue
        candidates.append(code)
    if "Y" in candidates or "N" in candidates:
        candidates = [value for value in candidates if value in {"Y", "N"}]
    unique = []
    for value in candidates:
        if value not in unique:
            unique.append(value)
    return unique if len(unique) >= 2 else []


def _text_flags(field: SpecField) -> str:
    parts = [field.code, field.name or "", field.description or "", field.type_name or ""]
    return " ".join(parts).lower()


def _is_code_like(text: str) -> bool:
    return any(token in text for token in ("코드", "code", "iscd", "id", "번호", "종목"))


def _infer_kind(field: SpecField, sample: object | None) -> dict[str, object]:
    text = _text_flags(field)
    if "y/n" in text or field.code.lower().endswith("_yn") or "여부" in text:
        return {"kind": "bool"}

    enum_values = _parse_enum(field.description or "")
    if enum_values:
        if any(token in text for token in ("비트", "bit", "첫 번째", "두 번째", "첫번째", "두번째")):
            return {"kind": "str"}
        normalized = {value.upper() for value in enum_values}
        if normalized.issubset({"Y", "N"}):
            return {"kind": "bool"}
        if sample is not None:
            sample_value = str(sample)
            if sample_value not in enum_values:
                enum_values.append(sample_value)
        if len(enum_values) >= 2:
            return {"kind": "enum", "enum": enum_values}

    if any(token in text for token in ("일자", "날짜", "기준일", "date", "ymd", "_dt")):
        return {"kind": "date"}

    time_tokens = ("시각", "hhmm", "hhmmss", "time", "_tm", "hour")
    if "시간외" not in text and not _is_code_like(text) and any(token in text for token in time_tokens):
        return {"kind": "time"}

    if any(token in text for token in ("일시", "datetime", "timestamp")):
        return {"kind": "datetime"}

    if _is_code_like(text):
        return {"kind": "str"}

    price_tokens = ("가격", "주가", "현재가", "시가", "고가", "저가", "지수", "금액", "대금", "amount", "price", "단일가")
    rate_tokens = ("비율", "율", "rate", "ratio", "percent", "pct", "ctrt")
    volume_tokens = ("수량", "거래량", "건수", "횟수", "volume", "count")

    if sample is not None:
        if isinstance(sample, (int,)):
            return {"kind": "int"}
        if isinstance(sample, (float,)):
            return {"kind": "decimal"}
        if isinstance(sample, str):
            value = sample.strip()
            if re.fullmatch(r"-?\d+\.\d+", value):
                return {"kind": "decimal"}
            if re.fullmatch(r"-?\d+", value):
                if len(value) == 8 and any(token in text for token in ("일자", "날짜", "date", "ymd")):
                    return {"kind": "date"}
                if len(value) == 6 and "시간외" not in text and any(
                    token in text for token in ("시간", "시각", "time", "hhmmss", "hhmm")
                ):
                    return {"kind": "time"}
                if any(token in text for token in price_tokens + rate_tokens):
                    return {"kind": "decimal"}
                if any(token in text for token in volume_tokens):
                    return {"kind": "int"}
                return {"kind": "int"}

    if any(token in text for token in price_tokens):
        return {"kind": "decimal"}

    if any(token in text for token in rate_tokens):
        return {"kind": "decimal"}

    if any(token in text for token in volume_tokens):
        return {"kind": "int"}

    return {"kind": "str"}


def _is_blank(value: object) -> bool:
    return isinstance(value, str) and not value.strip()


def _normalize_sample(value: object | None) -> tuple[object | None, bool]:
    if _is_blank(value):
        return None, True
    return value, False


def _is_zero_datetime(sample: object | None, kind: str | None) -> bool:
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


def _sample_from_container(container: object | None, field: SpecField) -> tuple[object | None, bool]:
    if isinstance(container, list):
        if container:
            first = container[0]
            if isinstance(first, dict):
                return first.get(field.code), field.code in first
    elif isinstance(container, dict):
        return container.get(field.code), field.code in container
    return None, False


def infer_types(specs: list[EndpointSpec], augment_dir: Path) -> dict[str, object]:
    inference: dict[str, object] = {}

    for spec in specs:
        entry: dict[str, object] = {
            "request": {},
            "response": {},
            "outputs": {},
            "output_kinds": {},
            "output_aliases": {},
            "extra_fields": {"response": [], "outputs": {}},
        }
        raw_path = augment_dir / spec.id / "raw.json"
        request_path = augment_dir / spec.id / "request.json"
        raw_payload = None
        request_payload = None

        if raw_path.exists():
            raw_payload = json.loads(raw_path.read_text(encoding="utf-8"))
        if request_path.exists():
            request_payload = json.loads(request_path.read_text(encoding="utf-8"))

        for field in spec.request.query:
            sample = None
            if request_payload:
                sample = (request_payload.get("query") or {}).get(field.code)
            entry["request"][field.code] = _infer_kind(field, sample)

        for field in spec.request.body:
            sample = None
            if request_payload:
                sample = (request_payload.get("body") or {}).get(field.code)
            entry["request"][field.code] = _infer_kind(field, sample)

        if isinstance(raw_payload, dict):
            output_codes = {output.code for output in spec.response.outputs}
            if "output" in raw_payload and "output" not in output_codes and len(output_codes) == 1:
                only_code = next(iter(output_codes))
                entry["output_aliases"][only_code] = "output"

        for field in spec.response.body:
            sample = raw_payload.get(field.code) if isinstance(raw_payload, dict) else None
            sample, _ = _normalize_sample(sample)
            hint = _infer_kind(field, sample)
            if field.required and _is_zero_datetime(sample, hint.get("kind")):
                hint["required"] = False
            if field.required and isinstance(raw_payload, dict) and sample is None:
                hint["required"] = False
            entry["response"][field.code] = hint

        if isinstance(raw_payload, dict):
            known_keys = {field.code for field in spec.response.body}
            known_keys.update(output.code for output in spec.response.outputs)
            output_aliases = entry.get("output_aliases")
            if isinstance(output_aliases, dict):
                known_keys.update(value for value in output_aliases.values() if isinstance(value, str))
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
                entry["extra_fields"]["response"].append(field.model_dump(by_alias=True))
                entry["response"][key] = _infer_kind(field, value)

        def _resolve_container(code: str) -> object | None:
            if not isinstance(raw_payload, dict):
                return None
            if code in raw_payload:
                return raw_payload.get(code)
            output_aliases = entry.get("output_aliases")
            if isinstance(output_aliases, dict):
                alias = output_aliases.get(code)
                if isinstance(alias, str):
                    return raw_payload.get(alias)
            return None

        for output in spec.response.outputs:
            container = _resolve_container(output.code)
            if isinstance(container, list):
                entry["output_kinds"][output.code] = "array"
            elif isinstance(container, dict):
                entry["output_kinds"][output.code] = "single"
            else:
                entry["output_kinds"][output.code] = output.kind

            output_map: dict[str, object] = {}
            output_known = {field.code for field in output.fields}
            for field in output.fields:
                sample, _ = _sample_from_container(container, field)
                sample, _ = _normalize_sample(sample)
                hint = _infer_kind(field, sample)
                if field.required and _is_zero_datetime(sample, hint.get("kind")):
                    hint["required"] = False
                if field.required and isinstance(container, (dict, list)) and sample is None:
                    hint["required"] = False
                if field.required and isinstance(container, list):
                    missing_in_list = any(
                        isinstance(item, dict) and field.code not in item for item in container
                    )
                    if missing_in_list:
                        hint["required"] = False
                output_map[field.code] = hint
            if isinstance(container, dict):
                extras = []
                for key, value in container.items():
                    if key in output_known:
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
                    extras.append(field.model_dump(by_alias=True))
                    output_map[key] = _infer_kind(field, value)
                entry["extra_fields"]["outputs"][output.code] = extras
            entry["outputs"][output.code] = output_map

        inference[spec.id] = entry

    return inference


def validate_samples(
    specs: list[EndpointSpec],
    augment_dir: Path,
    registry: dict[str, object],
) -> dict[str, object]:
    results: list[dict[str, object]] = []
    errors = 0
    for spec in specs:
        endpoint = registry.get(spec.id)
        if endpoint is None:
            continue
        if not spec.domains.virtual:
            results.append({"id": spec.id, "status": "skipped", "reason": "demo_only"})
            continue
        raw_path = augment_dir / spec.id / "raw.json"
        if not raw_path.exists():
            errors += 1
            results.append({"id": spec.id, "status": "missing_raw"})
            continue
        payload = json.loads(raw_path.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and str(payload.get("rt_cd")) not in ("0", "OK"):
            errors += 1
            results.append({"id": spec.id, "status": "rt_cd_error", "reason": str(payload.get("msg1") or "")})
            continue
        try:
            endpoint.response_model.model_validate(payload)
            results.append({"id": spec.id, "status": "ok"})
        except Exception as exc:  # noqa: BLE001
            errors += 1
            results.append({"id": spec.id, "status": "error", "reason": str(exc)})

    return {"total": len(results), "errors": errors, "results": results}
