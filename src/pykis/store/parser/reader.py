from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import BinaryIO

from pykis.store.parser.io import iter_fixed_width_blocks
from pykis.store.parser.models import RawRecord, RawSource
from pykis.store.parser.parser import FixedWidthParser


class FixedWidthReader:
    """Stream parsed records from a fixed-width file."""

    _source: RawSource
    _parser: FixedWidthParser

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


def _detect_delimiter(
    stream: BinaryIO,
    field_count: int,
    *,
    delimiters: tuple[bytes, ...],
    sample_bytes: int = 4096,
) -> bytes | None:
    pos = stream.tell()
    chunk = stream.read(sample_bytes)
    stream.seek(pos)
    if not chunk:
        return None
    line = chunk.splitlines()[0] if b"\n" in chunk else chunk
    line = line.rstrip(b"\r\n")
    if not line:
        return None
    for delimiter in delimiters:
        if delimiter not in line:
            continue
        parts = line.split(delimiter)
        while parts and parts[-1] == b"" and len(parts) > field_count:
            parts = parts[:-1]
        if len(parts) == field_count:
            return delimiter
    return None


def _detect_line_fixed(stream: BinaryIO, record_length: int, *, sample_bytes: int = 4096) -> bool:
    pos = stream.tell()
    line = stream.readline(sample_bytes)
    stream.seek(pos)
    if not line:
        return False
    stripped = line.rstrip(b"\r\n")
    return len(stripped) == record_length


def is_delimited_file(path: Path, field_count: int, *, delimiter: bytes = b"|", sample_bytes: int = 4096) -> bool:
    with path.open("rb") as stream:
        if delimiter == b"|":
            delimiters = (delimiter, b"\t")
        else:
            delimiters = (delimiter,)
        detected = _detect_delimiter(stream, field_count, delimiters=delimiters, sample_bytes=sample_bytes)
        return detected is not None


def is_line_fixed_file(path: Path, record_length: int, *, sample_bytes: int = 4096) -> bool:
    with path.open("rb") as stream:
        return _detect_line_fixed(stream, record_length, sample_bytes=sample_bytes)


class DelimitedReader:
    """Stream parsed records from a delimiter-separated file."""

    _source: RawSource
    _delimiter: bytes
    _field_names: tuple[str, ...]
    _encoding: str

    __slots__ = ("_source", "_delimiter", "_field_names", "_encoding")

    def __init__(self, source: RawSource, *, delimiter: str = "|") -> None:
        self._source = source
        self._delimiter = delimiter.encode()
        self._field_names = tuple(field.name for field in source.spec.fields)
        self._encoding = source.spec.encoding

    def iter_records(self, stream: BinaryIO, *, start_line: int = 0) -> Iterator[RawRecord]:
        field_count = len(self._field_names)
        for line_no, raw in enumerate(stream):
            if line_no < start_line:
                continue
            raw = raw.rstrip(b"\r\n")
            if not raw:
                continue
            parts = raw.split(self._delimiter)
            if parts and parts[-1] == b"":
                parts = parts[:-1]
            if len(parts) < field_count:
                parts.extend([b""] * (field_count - len(parts)))
            elif len(parts) > field_count:
                parts = parts[:field_count]
            values = [part.decode(self._encoding, errors="ignore").strip() for part in parts]
            fields = dict(zip(self._field_names, values))
            yield RawRecord(source_id=self._source.source_id, line_no=line_no, fields=fields)


class RecordReader:
    """Stream parsed records from fixed-width or delimiter-separated files."""

    _source: RawSource
    _fixed: FixedWidthReader
    _delimited: DelimitedReader
    _tab_delimited: DelimitedReader

    __slots__ = ("_source", "_fixed", "_delimited", "_tab_delimited")

    def __init__(self, source: RawSource, *, delimiter: str = "|") -> None:
        self._source = source
        self._fixed = FixedWidthReader(source)
        self._delimited = DelimitedReader(source, delimiter=delimiter)
        self._tab_delimited = DelimitedReader(source, delimiter="\t")

    def iter_records(self, stream: BinaryIO, *, start_line: int = 0) -> Iterator[RawRecord]:
        field_count = len(self._source.spec.fields)
        detected = _detect_delimiter(
            stream,
            field_count,
            delimiters=(self._delimited._delimiter, self._tab_delimited._delimiter),
        )
        if detected == self._delimited._delimiter:
            yield from self._delimited.iter_records(stream, start_line=start_line)
        elif detected == self._tab_delimited._delimiter:
            yield from self._tab_delimited.iter_records(stream, start_line=start_line)
        elif _detect_line_fixed(stream, self._source.spec.record_length):
            parser = FixedWidthParser(self._source.spec)
            line_no = 0
            for raw in stream:
                if line_no < start_line:
                    line_no += 1
                    continue
                line = raw.rstrip(b"\r\n")
                if len(line) < self._source.spec.record_length:
                    line_no += 1
                    continue
                fields = parser.parse(memoryview(line[: self._source.spec.record_length]))
                yield RawRecord(source_id=self._source.source_id, line_no=line_no, fields=fields)
                line_no += 1
        else:
            yield from self._fixed.iter_records(stream, start_line=start_line)
