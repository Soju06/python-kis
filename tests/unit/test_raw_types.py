from __future__ import annotations

from datetime import date

from pykis.api.raw.base import _parse_kis_date


def test_parse_kis_date_slash_format() -> None:
    assert _parse_kis_date("2024/04/02") == date(2024, 4, 2)


def test_parse_kis_date_dot_format() -> None:
    assert _parse_kis_date("2024.04.02") == date(2024, 4, 2)
