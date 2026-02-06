from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import cast

from codegen.api.models import EndpointSpec, SpecField
from codegen.api.overrides import (
    AugmentOverrides,
    EndpointOverrideLocations,
    load_augment_overrides,
)
from codegen.core.enums import parse_enum_entries, parse_enum_values
from codegen.core.text import is_blank_description, is_forced_null_description
from codegen.core.types import JsonObject, JsonValue
from pykis.api.client import SyncKisRawClient

UNSAFE_KEYWORDS = ("주문", "정정", "취소", "매수", "매도", "trading", "order")
SKIP_ENDPOINT_IDS = frozenset()

_EMPTY_MESSAGE_CODES = {"APBN0024"}
_EMPTY_MESSAGE_SNIPPETS = (
    "조회된 데이터가 없습니다",
    "조회할 자료가 없습니다",
    "조회가 계속 됩니다",
    "CME SUB거래소 신청 계좌가 아닙니다",
)


def load_overrides(path: Path) -> AugmentOverrides:
    return load_augment_overrides(path)


class ValueResolver:
    _defaults: dict[str, JsonValue]
    _endpoints: dict[str, EndpointOverrideLocations]

    __slots__ = ("_defaults", "_endpoints")

    def __init__(self, client: SyncKisRawClient, overrides: AugmentOverrides) -> None:
        account_number, account_product = client.auth.account_number
        self._defaults = {
            "appkey": client.auth.app_key,
            "appsecret": client.auth.secret_key,
            "id": client.auth.id,
            "custtype": "P",
            "cano": account_number,
            "acnt_prdt_cd": account_product,
            "acca_dvsn_cd": "00",
            "inqr_dvsn": "00",
            "ctx_area_fk100": "",
            "ctx_area_nk100": "",
            "ctx_area_fk200": "",
            "ctx_area_nk200": "",
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": "005930",
            "pdno": "005930",
        }
        if overrides.defaults:
            self._defaults.update(overrides.defaults)
        self._endpoints = overrides.endpoints

    def resolve(
        self,
        endpoint_id: str,
        location: str,
        code: str,
    ) -> JsonValue | None:
        key = code.lower()
        if key == "grant_type":
            return "client_credentials"
        if key in ("user_id", "userid"):
            return self._defaults.get("user_id") or self._defaults.get("userid") or self._defaults.get("id")
        endpoint_overrides = self._endpoints.get(endpoint_id)
        if endpoint_overrides:
            location_overrides = _endpoint_location(endpoint_overrides, location)
            if key in location_overrides:
                return location_overrides[key]
        if key in self._defaults:
            return self._defaults[key]
        return _heuristic_value(key)

    def resolve_with_source(
        self,
        endpoint_id: str,
        location: str,
        code: str,
    ) -> tuple[JsonValue | None, str, str | None]:
        key = code.lower()
        if key == "grant_type":
            return "client_credentials", "special", "grant_type"
        if key in ("user_id", "userid"):
            value = self._defaults.get("user_id") or self._defaults.get("userid") or self._defaults.get("id")
            if value is not None:
                return value, "special", "user_id"
        endpoint_overrides = self._endpoints.get(endpoint_id)
        if endpoint_overrides:
            location_overrides = _endpoint_location(endpoint_overrides, location)
            if key in location_overrides:
                return location_overrides[key], "override", None
        if key in self._defaults:
            return self._defaults[key], "default", None
        value, reason = _heuristic_value_with_reason(key)
        if value is not None:
            return value, "heuristic", reason
        return None, "missing", None

    def has_override(self, endpoint_id: str, location: str, code: str) -> bool:
        endpoint_overrides = self._endpoints.get(endpoint_id)
        if not endpoint_overrides:
            return False
        location_overrides = _endpoint_location(endpoint_overrides, location)
        return code.lower() in location_overrides


def build_payload(
    endpoint: EndpointSpec,
    resolver: ValueResolver,
    location: str,
    fields: list[SpecField],
) -> tuple[dict[str, JsonValue], list[str]]:
    payload, missing, _ = build_payload_with_trace(endpoint, resolver, location, fields)
    return payload, missing


def build_payload_with_trace(
    endpoint: EndpointSpec,
    resolver: ValueResolver,
    location: str,
    fields: list[SpecField],
) -> tuple[dict[str, JsonValue], list[str], list[JsonObject]]:
    payload: dict[str, JsonValue] = {}
    missing: list[str] = []
    traces: list[JsonObject] = []

    for field in fields:
        desc = (field.description or "").strip()
        if is_forced_null_description(desc):
            traces.append(
                {
                    "code": field.code,
                    "location": location,
                    "value": None,
                    "required": field.required,
                    "used": False,
                    "source": "forced_null",
                    "notes": ["forced_null_description"],
                }
            )
            continue

        value, source, reason = resolver.resolve_with_source(endpoint.id, location, field.code)
        enum_values = _enum_values(field)
        enum_alt_values = _enum_alt_values(field)
        notes: list[str] = []

        if enum_values:
            if value is None:
                enum_default = _enum_default(field)
                if enum_default is not None:
                    value = enum_default
                    source = "enum_default"
            else:
                if not resolver.has_override(endpoint.id, location, field.code):
                    normalized = str(value)
                    if normalized not in enum_values and normalized not in enum_alt_values:
                        enum_default = _enum_default(field)
                        if enum_default is not None:
                            value = enum_default
                            source = "enum_default"
                            notes.append("enum_coerced")
        elif value is None:
            enum_default = _enum_default(field)
            if enum_default is not None:
                value = enum_default
                source = "enum_default"

        desc_value, desc_reason = _description_value_with_reason(field)
        if desc_value is not None and (value is None or source in {"default", "heuristic"}):
            value = desc_value
            source = "description"
            reason = desc_reason
        if value is None:
            heuristic_value, heuristic_reason = _heuristic_value_with_reason(field.code)
            if heuristic_value is not None:
                value = heuristic_value
                source = "heuristic"
                reason = heuristic_reason

        if is_blank_description(desc):
            if value is None:
                value = ""
                if source == "missing":
                    source = "blank_default"
            notes.append("blank_allowed")

        if value is None and field.required:
            value = ""
            source = "required_blank"
            missing.append(field.code)
            notes.append("required_blank")

        used = value is not None
        if used:
            payload[field.code] = value

        trace = cast(
            JsonObject,
            {
                "code": field.code,
                "location": location,
                "value": value,
                "required": field.required,
                "used": used,
                "source": source,
                "notes": notes,
            },
        )
        if reason:
            trace["reason"] = reason
        traces.append(trace)

    return payload, missing, traces


def is_empty_payload(payload: JsonObject | None) -> bool:
    if not payload:
        return False
    msg_code = str(payload.get("msg_cd") or "")
    if msg_code in _EMPTY_MESSAGE_CODES:
        return True
    message = str(payload.get("msg1") or "")
    if not msg_code and not message:
        rt_cd = str(payload.get("rt_cd") or "").strip()
        if not rt_cd:
            return True
    return any(snippet in message for snippet in _EMPTY_MESSAGE_SNIPPETS)


def _endpoint_location(
    overrides: EndpointOverrideLocations,
    location: str,
) -> dict[str, JsonValue]:
    if location == "headers":
        return overrides.headers
    if location == "query":
        return overrides.query
    if location == "body":
        return overrides.body
    return {}


def _enum_values(field: SpecField) -> list[str]:
    return parse_enum_values(field.description)


def _enum_alt_values(field: SpecField) -> list[str]:
    entries = parse_enum_entries(field.description or "")
    values: list[str] = []
    for entry in entries:
        desc = (entry.desc or "").strip()
        if _is_code_like(desc):
            values.append(desc)
    return values


def _is_code_like(value: str) -> bool:
    if not value:
        return False
    if not value.isalnum():
        return False
    return len(value) <= 4


def _enum_default(field: SpecField) -> str | None:
    values = _enum_values(field)
    if values:
        if set(values) == {"Y", "N"}:
            return "N"
        return values[0]
    desc = (field.description or "").strip()
    if not desc:
        return None
    lowered = desc.lower()
    if "y/n" in lowered or "여부" in desc:
        return "N"
    return None


def _heuristic_value(code: str) -> JsonValue | None:
    value, _ = _heuristic_value_with_reason(code)
    return value


def _heuristic_value_with_reason(code: str) -> tuple[JsonValue | None, str | None]:
    code = code.lower()
    if code == "keyb":
        return "", "keyb_blank"
    if code in ("index_key", "cts", "cts_area"):
        return "", "continuation_blank"
    if code in ("icod", "industry_code"):
        return "000", "industry_code_default"
    if code in ("prdt_type_cd", "prdt_type"):
        return "512", "product_type_default"
    if code in ("pdno",):
        return "AAPL", "pdno_symbol_default"
    if code in ("auth",):
        return "", "auth_blank"
    if code.endswith("etc_cls_code"):
        return "", "etc_cls_blank"
    if code.endswith("hour_1"):
        return "100000", "hour_1_default"
    if any(token in code for token in ("date", "_dt", "ymd", "bass_dt", "bsop_date")):
        return datetime.now().strftime("%Y%m%d"), "date_today"
    if any(token in code for token in ("time", "hour", "tm")):
        return "090000", "time_default"
    if code.endswith("_yn") or code.endswith("yn"):
        return "N", "yn_default"
    if any(token in code for token in ("qty", "cnt", "count", "vol")):
        return "1", "qty_default"
    if any(
        token in code
        for token in (
            "price",
            "prc",
            "amt",
            "rate",
            "rt",
            "ratio",
            "val",
            "delta",
            "gear",
            "prmm",
            "vltl",
        )
    ):
        return "0", "price_default"
    if code.startswith("fid_") and re.search(r"\d+$", code):
        return "0", "fid_numeric_default"
    if code.startswith("ctx_area"):
        return "", "ctx_area_default"
    if code in ("seq", "nmin", "pinc", "next", "nrec", "fill"):
        return "0", "seq_default"
    if code in ("cts_area",):
        return "", "cts_area_default"
    if any(token in code for token in ("code", "cls", "cd", "div", "type", "gb", "gubn")):
        return "0", "code_like_default"
    if "symb" in code:
        return "AAPL", "symbol_default"
    if any(token in code for token in ("excd", "exch", "exchange")):
        return "NAS", "exchange_default"
    return None, None


_FIXED_VALUE_RE = re.compile(r"(?P<value>[A-Za-z0-9]+)\s*[:\-]?\s*고정값")
_FIXED_VALUE_TRAIL_RE = re.compile(r"고정값\s*[:\-]?\s*(?P<value>[A-Za-z0-9]+)")
_UNIQUE_KEY_RE = re.compile(r"unique\s*key\s*\(?\s*(?P<value>\d{3,6})\s*\)?", re.IGNORECASE)
_EXAMPLE_RE = re.compile(r"(?i)(?:ex\)|예\)|예:|ex:)\s*(?P<value>[^,;\)\n]{1,40})")
_DATE_EXAMPLE_RE = re.compile(r"(?P<value>\d{4}[./-]\d{1,2}[./-]\d{1,2})")
_DATE_EXAMPLE_COMPACT_RE = re.compile(r"(?<!\d)(?P<value>\d{8})(?!\d)")
_TIME_EXAMPLE_RE = re.compile(r"(?P<value>\d{1,2}:\d{2}:\d{2})")
_ALL_VALUE_RE = re.compile(r"(?:전체\s*[:=]?\s*0000|0000\s*[:=]?\s*전체)")
_ALL_ZERO_RE = re.compile(r"(?:전체\s*[:=]?\s*0|\b0\s*[:=]?\s*전체)")
_FIRST_ALNUM_RE = re.compile(r"[A-Za-z0-9]+")
_LEADING_NUM_RE = re.compile(r"^\s*(\d+)")


def _description_value_with_reason(field: SpecField) -> tuple[JsonValue | None, str | None]:
    desc = (field.description or "").strip()
    if not desc:
        return None, None
    normalized = " ".join(desc.replace("\r", "\n").replace("\t", " ").split())
    if field.code.lower() in {"srs_cd", "srs_code"}:
        normalized = _strip_example_suffix(normalized)

    match = _FIXED_VALUE_RE.search(normalized) or _FIXED_VALUE_TRAIL_RE.search(normalized)
    if match:
        value = _sanitize_example_value(field, match.group("value"))
        return value, "fixed_value"

    match = _UNIQUE_KEY_RE.search(normalized)
    if match:
        value = _sanitize_example_value(field, match.group("value"))
        return value, "unique_key"

    if is_blank_description(desc):
        return "", "blank_description"

    if _ALL_VALUE_RE.search(normalized):
        return "0000", "all_value"
    if _ALL_ZERO_RE.search(normalized):
        return "0", "all_value"

    if field.code.lower() in {"nday", "nmin"} and "N일전" in desc:
        return "0", "nday_default"

    match = _DATE_EXAMPLE_RE.search(normalized)
    if match:
        digits = re.sub(r"[^0-9]", "", match.group("value"))
        if len(digits) == 8:
            return digits, "date_example"

    match = _DATE_EXAMPLE_COMPACT_RE.search(normalized)
    if match and any(token in field.code.lower() for token in ("date", "_dt", "ymd", "bass_dt", "bsop_date")):
        value = _sanitize_example_value(field, match.group("value"))
        return value, "date_example"

    match = _TIME_EXAMPLE_RE.search(normalized)
    if match:
        value = _sanitize_example_value(field, match.group("value").replace(":", ""))
        return value, "time_example"

    match = _EXAMPLE_RE.search(normalized)
    if match:
        value = _strip_example_suffix(match.group("value").strip())
        value = _sanitize_example_value(field, value)
        if value:
            return value, "example_value"

    return None, None


def _strip_example_suffix(value: str) -> str:
    if not value:
        return value
    for token in ("※", "참고", "포럼", "FAQ", "다운로드", "해외", "국내"):
        index = value.find(token)
        if index > 0:
            return value[:index].strip()
    return value.strip()


def _sanitize_example_value(field: SpecField, value: str) -> str:
    if not value:
        return value
    code = field.code.lower()
    sanitized = value.strip()

    if "최대" in sanitized:
        match = _LEADING_NUM_RE.search(sanitized)
        if match:
            sanitized = match.group(1)

    if "(" in sanitized:
        if code not in {"srs_cd", "srs_code"}:
            prefix = sanitized.split("(", 1)[0].strip()
            if prefix:
                sanitized = prefix
            else:
                token_match = _FIRST_ALNUM_RE.search(sanitized)
                if token_match:
                    sanitized = token_match.group(0)

    if code not in {"srs_cd", "srs_code"} and " " in sanitized:
        token_match = _FIRST_ALNUM_RE.search(sanitized)
        if token_match:
            sanitized = token_match.group(0)

    if _is_date_code(code):
        digits = re.sub(r"[^0-9]", "", sanitized)
        if len(digits) in {9, 10} and digits.startswith("00"):
            trimmed = digits.lstrip("0")
            if len(trimmed) == 8:
                return trimmed
        if len(digits) == 8:
            return digits

    return sanitized


def _is_date_code(code: str) -> bool:
    return any(token in code for token in ("date", "_dt", "ymd", "bass_dt", "bsop_date"))


__all__ = [
    "SKIP_ENDPOINT_IDS",
    "UNSAFE_KEYWORDS",
    "ValueResolver",
    "build_payload",
    "build_payload_with_trace",
    "is_empty_payload",
    "load_overrides",
]
