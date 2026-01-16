from __future__ import annotations

from typing import Mapping

from pykis.store.parser.spec import FieldSpec, RecordSpec


class FixedWidthParser:
    """Parse fixed-width byte records into a field mapping."""

    _spec: RecordSpec
    _fields: tuple[FieldSpec, ...]
    _encoding: str

    __slots__ = ("_spec", "_fields", "_encoding")

    def __init__(self, spec: RecordSpec) -> None:
        spec.validate()
        self._spec = spec
        self._fields: tuple[FieldSpec, ...] = spec.fields
        self._encoding = spec.encoding

    @property
    def record_length(self) -> int:
        return self._spec.record_length

    def parse(self, block: memoryview) -> Mapping[str, str]:
        if len(block) < self._spec.record_length:
            raise ValueError("record block is shorter than record_length")
        encoding = self._encoding
        result: dict[str, str] = {}
        for field in self._fields:
            raw = block[field.start : field.end].tobytes()
            text = raw.decode(encoding, errors="ignore")
            result[field.name] = text.strip() if field.strip else text
        return result
