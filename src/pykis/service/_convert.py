"""Common conversion helpers for L0 raw → L1 service model mapping."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation


def decimal_required(value: Decimal | int | str) -> Decimal:
    """Convert a raw value to Decimal, raising on empty/invalid input."""
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    text = str(value).strip()
    if not text:
        raise ValueError("required decimal value is empty")
    return Decimal(text)


def decimal_optional(value: Decimal | int | str | None) -> Decimal | None:
    """Convert a raw value to Decimal, returning None on empty/invalid input."""
    if value is None:
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    text = str(value).strip()
    if not text:
        return None
    try:
        return Decimal(text)
    except InvalidOperation:
        return None


def int_to_decimal(value: int) -> Decimal:
    """Convert an int field to Decimal (common for domestic price fields stored as int)."""
    return Decimal(value)
