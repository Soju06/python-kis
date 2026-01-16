from __future__ import annotations

import pytest

from pykis.store.parser.parser import FixedWidthParser
from pykis.store.parser.spec import RecordSpec

pytestmark = pytest.mark.unit


def test_fixed_width_parser_parses_fields() -> None:
    spec = RecordSpec.from_lengths(["code", "name"], [4, 6], encoding="utf-8")
    parser = FixedWidthParser(spec)

    block = memoryview(b"1234ABCDEF")
    result = parser.parse(block)

    assert result["code"] == "1234"
    assert result["name"] == "ABCDEF"


def test_fixed_width_parser_rejects_short_block() -> None:
    spec = RecordSpec.from_lengths(["code", "name"], [4, 6], encoding="utf-8")
    parser = FixedWidthParser(spec)

    with pytest.raises(ValueError, match="record block is shorter"):
        parser.parse(memoryview(b"123"))
