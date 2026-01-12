from __future__ import annotations

from collections.abc import Iterator
from typing import BinaryIO

from .io import iter_fixed_width_blocks
from .models import RawRecord, RawSource
from .parser import FixedWidthParser


class FixedWidthReader:
    """Stream parsed records from a fixed-width file."""

    __slots__ = ("_source", "_parser")

    def __init__(self, source: RawSource) -> None:
        self._source = source
        self._parser = FixedWidthParser(source.spec)

    def iter_records(self, stream: BinaryIO, *, start_line: int = 0) -> Iterator[RawRecord]:
        line_no = start_line
        for block in iter_fixed_width_blocks(stream, self._parser.record_length):
            fields = self._parser.parse(block)
            yield RawRecord(source_id=self._source.source_id, line_no=line_no, fields=fields)
            line_no += 1
