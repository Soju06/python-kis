from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from codegen.api.models import EndpointSpec, SpecField
from codegen.api.overrides import (
    AugmentOverrides,
    EndpointOverrideLocations,
    load_augment_overrides,
)
from codegen.core.enums import parse_enum_entries, parse_enum_values
from codegen.core.text import is_forced_null_description
from codegen.core.types import JsonObject, JsonValue
from pykis.api.client import SyncKisRawClient

UNSAFE_KEYWORDS = ("주문", "정정", "취소", "매수", "매도", "trading", "order")

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
    payload: dict[str, JsonValue] = {}
    missing: list[str] = []

    for field in fields:
        desc = (field.description or "").strip()
        if is_forced_null_description(desc):
            continue
        value = resolver.resolve(endpoint.id, location, field.code)
        enum_values = _enum_values(field)
        enum_alt_values = _enum_alt_values(field)
        if enum_values:
            if value is None:
                value = _enum_default(field)
            else:
                if not resolver.has_override(endpoint.id, location, field.code):
                    normalized = str(value)
                    if normalized not in enum_values and normalized not in enum_alt_values:
                        value = _enum_default(field)
        elif value is None:
            value = _enum_default(field)
        if value is None:
            value = _heuristic_value(field.code)
        desc_lower = desc.lower()
        if "공백" in desc_lower or "blank" in desc_lower:
            value = "" if value is None else value
        if value is None and field.required:
            value = ""
            missing.append(field.code)
        if value is None:
            continue
        payload[field.code] = value

    return payload, missing


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
    code = code.lower()
    if code == "keyb":
        return ""
    if code in ("icod", "industry_code"):
        return "000"
    if code in ("prdt_type_cd", "prdt_type"):
        return "512"
    if code in ("pdno",):
        return "AAPL"
    if code in ("auth",):
        return ""
    if code.endswith("etc_cls_code"):
        return ""
    if code.endswith("hour_1"):
        return "100000"
    if any(token in code for token in ("date", "_dt", "ymd", "bass_dt", "bsop_date")):
        return datetime.now().strftime("%Y%m%d")
    if any(token in code for token in ("time", "hour", "tm")):
        return "090000"
    if code.endswith("_yn") or code.endswith("yn"):
        return "N"
    if any(token in code for token in ("qty", "cnt", "count", "vol")):
        return "1"
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
        return "0"
    if code.startswith("fid_") and re.search(r"\d+$", code):
        return "0"
    if code.startswith("ctx_area"):
        return ""
    if code in ("seq", "nmin", "pinc", "next", "nrec", "fill"):
        return "0"
    if code in ("cts_area",):
        return ""
    if any(token in code for token in ("code", "cls", "cd", "div", "type", "gb", "gubn")):
        return "0"
    if "symb" in code:
        return "AAPL"
    if any(token in code for token in ("excd", "exch", "exchange")):
        return "NAS"
    return None


__all__ = [
    "UNSAFE_KEYWORDS",
    "ValueResolver",
    "build_payload",
    "is_empty_payload",
    "load_overrides",
]
