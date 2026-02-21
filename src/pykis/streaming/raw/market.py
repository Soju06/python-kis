from __future__ import annotations

import re

MARKET_TIMEZONES: dict[str, str] = {
    "NAS": "America/New_York",
    "NYS": "America/New_York",
    "AMS": "America/New_York",
    "BAQ": "America/New_York",
    "BAY": "America/New_York",
    "BAA": "America/New_York",
    "NMS": "America/New_York",
    "ASE": "America/New_York",
    "TSE": "Asia/Tokyo",
    "HKS": "Asia/Hong_Kong",
    "SHS": "Asia/Shanghai",
    "SZS": "Asia/Shanghai",
    "HSX": "Asia/Ho_Chi_Minh",
    "HNX": "Asia/Ho_Chi_Minh",
    "SGX": "Asia/Singapore",
    "ASX": "Australia/Sydney",
    "LSE": "Europe/London",
    "FRA": "Europe/Berlin",
    "XET": "Europe/Berlin",
    "TSX": "America/Toronto",
}

_MARKET_CODE_RE = re.compile(r"^[DR]([A-Z]{3})")


def extract_market_code(value: str | None) -> str | None:
    if not value:
        return None
    text = value.strip().upper()
    match = _MARKET_CODE_RE.match(text)
    if not match:
        return None
    return match.group(1)


def resolve_timezone_from_symbol(value: str | None, fallback: str | None, mapping: dict[str, str] | None = None) -> str | None:
    code = extract_market_code(value)
    if code is None:
        return fallback
    table = mapping or MARKET_TIMEZONES
    return table.get(code, fallback)


def resolve_timezone_from_fields(fields: dict[str, str], fallback: str | None, mapping: dict[str, str] | None = None) -> str | None:
    for key in ("RSYM", "TR_KEY"):
        if key in fields:
            tz = resolve_timezone_from_symbol(fields.get(key), fallback, mapping)
            if tz is not None:
                return tz
    return fallback


class DefaultMarketTimezoneResolver:
    mapping: dict[str, str]
    fallback: str | None

    def __init__(self, mapping: dict[str, str] | None = None, fallback: str | None = None) -> None:
        self.mapping = mapping or MARKET_TIMEZONES
        self.fallback = fallback

    def resolve(self, spec, raw_fields: dict[str, str]) -> str | None:
        return resolve_timezone_from_fields(raw_fields, self.fallback, self.mapping)
