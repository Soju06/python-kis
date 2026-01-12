from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Mapping
import os

from ..raw.models import RawRecord, RawSource
from ..raw.parser import FixedWidthParser
from ..raw.reader import FixedWidthReader
from ..raw.spec import RecordSpec
from ..translate.models import Instrument
from ..translate.normalizer import Normalizer

from .index import InMemoryIndex


@dataclass(frozen=True, slots=True)
class IngestPlan:
    sources: Iterable[RawSource]
    workers: int | None = None


class StoreBuilder:
    """Build store indexes from raw sources.

    This builder keeps I/O in the raw layer and normalization in the translation
    layer, then assembles service-layer indexes.
    """

    __slots__ = ("_normalizers",)

    def __init__(self, normalizers: Mapping[str, Normalizer]) -> None:
        self._normalizers = normalizers

    def build_index(self, plan: IngestPlan, *, parallel: bool = True) -> InMemoryIndex:
        instruments: list[Instrument] = []
        for source in plan.sources:
            if parallel:
                instruments.extend(self.iter_instruments_parallel(source, workers=plan.workers))
            else:
                instruments.extend(self.iter_instruments(source))
        return InMemoryIndex(instruments)

    def iter_instruments(self, source: RawSource) -> Iterator[Instrument]:
        normalizer = self._get_normalizer(source)
        reader = FixedWidthReader(source)
        with source.path.open("rb") as stream:
            for record in reader.iter_records(stream):
                instrument = normalizer.normalize(record)
                if instrument is not None:
                    yield instrument

    def iter_instruments_parallel(self, source: RawSource, *, workers: int | None = None) -> Iterator[Instrument]:
        normalizer = self._get_normalizer(source)
        record_length = source.spec.record_length
        file_size = source.path.stat().st_size
        aligned_size = (file_size // record_length) * record_length
        ranges = _split_ranges(aligned_size, record_length, workers or _default_workers())
        if not ranges:
            return

        with ProcessPoolExecutor(max_workers=workers or _default_workers()) as executor:
            futures = [
                executor.submit(_parse_range, source.path, source.spec, start, end)
                for start, end in ranges
            ]
            for future in as_completed(futures):
                for line_no, fields in future.result():
                    record = RawRecord(source_id=source.source_id, line_no=line_no, fields=fields)
                    instrument = normalizer.normalize(record)
                    if instrument is not None:
                        yield instrument

    def _get_normalizer(self, source: RawSource) -> Normalizer:
        normalizer = self._normalizers.get(source.source_id)
        if normalizer is None:
            raise KeyError(f"missing normalizer for source: {source.source_id}")
        return normalizer


def _default_workers() -> int:
    return max(1, os.cpu_count() or 1)


def _split_ranges(file_size: int, record_length: int, workers: int) -> list[tuple[int, int]]:
    if file_size <= 0:
        return []
    if workers <= 1:
        return [(0, file_size)]

    chunk = file_size // workers
    ranges: list[tuple[int, int]] = []
    start = 0
    for idx in range(workers):
        if idx == workers - 1:
            end = file_size
        else:
            end = start + chunk
            end = (end // record_length) * record_length
            if end <= start:
                end = min(file_size, start + record_length)
        if end > start:
            ranges.append((start, end))
        start = end
        if start >= file_size:
            break
    return ranges


def _parse_range(path: Path, spec: RecordSpec, start: int, end: int) -> list[tuple[int, dict[str, str]]]:
    if end <= start:
        return []
    parser = FixedWidthParser(spec)
    record_length = spec.record_length
    start_line = start // record_length
    with path.open("rb") as stream:
        stream.seek(start)
        data = stream.read(end - start)
    view = memoryview(data)
    total = (len(view) // record_length) * record_length
    results: list[tuple[int, dict[str, str]]] = []
    for offset in range(0, total, record_length):
        block = view[offset : offset + record_length]
        fields = dict(parser.parse(block))
        results.append((start_line + (offset // record_length), fields))
    return results
