from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True, slots=True)
class FieldSpec:
    name: str
    start: int
    end: int
    strip: bool = True

    @property
    def length(self) -> int:
        return self.end - self.start


@dataclass(frozen=True, slots=True)
class RecordSpec:
    record_length: int
    fields: tuple[FieldSpec, ...]
    encoding: str = "euc-kr"

    @classmethod
    def from_lengths(
        cls,
        names: Sequence[str],
        lengths: Sequence[int],
        *,
        encoding: str = "euc-kr",
        record_length: int | None = None,
    ) -> "RecordSpec":
        if len(names) != len(lengths):
            raise ValueError("names and lengths must have the same size")
        offset = 0
        fields: list[FieldSpec] = []
        for name, length in zip(names, lengths, strict=True):
            if length <= 0:
                raise ValueError(f"field length must be positive: {name}={length}")
            fields.append(FieldSpec(name=name, start=offset, end=offset + length))
            offset += length
        total_length = record_length if record_length is not None else offset
        if total_length < offset:
            raise ValueError("record_length is shorter than field sum")
        return cls(record_length=total_length, fields=tuple(fields), encoding=encoding)

    def field_names(self) -> tuple[str, ...]:
        return tuple(field.name for field in self.fields)

    def validate(self) -> None:
        if self.record_length <= 0:
            raise ValueError("record_length must be positive")
        for field in self.fields:
            if field.start < 0 or field.end <= field.start:
                raise ValueError(f"invalid field range: {field}")
        if self.fields:
            max_end = max(field.end for field in self.fields)
            if max_end > self.record_length:
                raise ValueError("field range exceeds record_length")


def compile_fields(names: Iterable[str], widths: Iterable[int]) -> tuple[FieldSpec, ...]:
    offset = 0
    fields: list[FieldSpec] = []
    for name, width in zip(names, widths, strict=True):
        fields.append(FieldSpec(name=name, start=offset, end=offset + width))
        offset += width
    return tuple(fields)
