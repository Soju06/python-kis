from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Type

from pydantic import BaseModel

from pykis.store.parser.definitions import SourceDef
from pykis.store.parser.models import RawSource
from pykis.store.parser.parser import FixedWidthParser
from pykis.store.parser.reader import RecordReader, is_delimited_file, is_line_fixed_file
from pykis.store.registry import get_model, get_struct
from pykis.store.service.indexing import IndexFields, build_index_row, detect_index_fields
from pykis.store.service.sqlite import StoreDb, TableDef


@dataclass(frozen=True, slots=True)
class LoadResult:
    source_id: str
    rows: int


def load_source_into_sqlite(
    db: StoreDb,
    *,
    source_id: str,
    file_path: Path,
    record_spec,
    model: Type[BaseModel],
    table_name: str,
    batch_size: int = 1000,
    index_fields: IndexFields | None = None,
) -> LoadResult:
    raw_source = RawSource(source_id=source_id, kind=table_name, path=file_path, spec=record_spec)
    reader = RecordReader(raw_source)
    db.create_table(TableDef(name=table_name, record_spec=record_spec))
    db.create_index_table()

    batch: list[dict[str, object]] = []
    index_batch: list[dict[str, object]] = []
    total = 0
    with file_path.open("rb") as stream:
        for record in reader.iter_records(stream):
            parsed = model.model_validate(record.fields)
            payload = parsed.model_dump()
            payload["source_id"] = source_id
            payload["line_no"] = record.line_no
            batch.append(payload)
            if index_fields is not None:
                idx_row = build_index_row(
                    fields=record.fields,
                    index_fields=index_fields,
                    source_id=source_id,
                    line_no=record.line_no,
                    table_name=table_name,
                )
                if idx_row is not None:
                    index_batch.append(idx_row)
            if len(batch) >= batch_size:
                db.insert_rows(table_name, batch)
                if index_batch:
                    db.insert_index_rows(index_batch)
                    index_batch.clear()
                db.commit()
                total += len(batch)
                batch.clear()
    if batch:
        db.insert_rows(table_name, batch)
        if index_batch:
            db.insert_index_rows(index_batch)
        db.commit()
        total += len(batch)
    return LoadResult(source_id=source_id, rows=total)


def load_source_def_into_sqlite(
    db: StoreDb,
    *,
    source: SourceDef,
    file_path: Path,
    batch_size: int = 1000,
) -> LoadResult:
    struct_def = get_struct(source.struct_name)
    if struct_def is None:
        raise KeyError(f"struct not found: {source.struct_name}")
    model = get_model(source.struct_name)
    index_fields = detect_index_fields(source.struct_name, struct_def.record_spec)
    db.upsert_source(
        source_id=source.source_id,
        group=source.group,
        label=source.label,
        download_url=source.download_url,
        header_url=source.header_url,
        struct_name=source.struct_name,
    )
    return load_source_into_sqlite(
        db,
        source_id=source.source_id,
        file_path=file_path,
        record_spec=struct_def.record_spec,
        model=model,
        table_name=source.struct_name.lower(),
        batch_size=batch_size,
        index_fields=index_fields,
    )


def load_source_def_into_sqlite_parallel(
    db: StoreDb,
    *,
    source: SourceDef,
    file_path: Path,
    batch_size: int = 2000,
    workers: int | None = None,
    chunk_bytes: int = 8 * 1024 * 1024,
) -> LoadResult:
    struct_def = get_struct(source.struct_name)
    if struct_def is None:
        raise KeyError(f"struct not found: {source.struct_name}")
    if is_delimited_file(file_path, len(struct_def.record_spec.fields)) or is_line_fixed_file(
        file_path, struct_def.record_spec.record_length
    ):
        return load_source_def_into_sqlite(
            db,
            source=source,
            file_path=file_path,
            batch_size=batch_size,
        )
    index_fields = detect_index_fields(source.struct_name, struct_def.record_spec)
    db.upsert_source(
        source_id=source.source_id,
        group=source.group,
        label=source.label,
        download_url=source.download_url,
        header_url=source.header_url,
        struct_name=source.struct_name,
    )
    db.create_table(TableDef(name=source.struct_name.lower(), record_spec=struct_def.record_spec))
    db.create_index_table()

    ranges = _split_ranges_by_bytes(file_path, struct_def.record_spec.record_length, chunk_bytes)
    if not ranges:
        return LoadResult(source_id=source.source_id, rows=0)

    rows_inserted = 0
    batch: list[dict[str, object]] = []
    index_batch: list[dict[str, object]] = []
    worker_count = workers or max(1, os.cpu_count() or 1)

    with ProcessPoolExecutor(max_workers=worker_count) as executor:
        futures = [
            executor.submit(
                _parse_validate_range,
                file_path,
                struct_def.record_spec,
                source.struct_name,
                source.source_id,
                start,
                end,
                index_fields,
            )
            for start, end in ranges
        ]
        for future in as_completed(futures):
            rows, index_rows = future.result()
            for row in rows:
                batch.append(row)
                if len(batch) >= batch_size:
                    db.insert_rows(source.struct_name.lower(), batch)
                    if index_batch:
                        db.insert_index_rows(index_batch)
                        index_batch.clear()
                    db.commit()
                    rows_inserted += len(batch)
                    batch.clear()
            if index_rows:
                index_batch.extend(index_rows)
                if len(index_batch) >= batch_size:
                    db.insert_index_rows(index_batch)
                    index_batch.clear()

    if batch:
        db.insert_rows(source.struct_name.lower(), batch)
        rows_inserted += len(batch)
    if index_batch:
        db.insert_index_rows(index_batch)
    db.commit()
    return LoadResult(source_id=source.source_id, rows=rows_inserted)


def _split_ranges_by_bytes(path: Path, record_length: int, chunk_bytes: int) -> list[tuple[int, int]]:
    size = path.stat().st_size
    if size <= 0:
        return []
    if chunk_bytes < record_length:
        chunk_bytes = record_length * 1000
    ranges: list[tuple[int, int]] = []
    start = 0
    while start < size:
        end = min(size, start + chunk_bytes)
        end = (end // record_length) * record_length
        if end <= start:
            end = min(size, start + record_length)
        ranges.append((start, end))
        start = end
    return ranges


def _parse_validate_range(
    path: Path,
    record_spec,
    struct_name: str,
    source_id: str,
    start: int,
    end: int,
    index_fields: IndexFields,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    model = get_model(struct_name)
    parser = FixedWidthParser(record_spec)
    record_length = record_spec.record_length
    if end <= start:
        return [], []
    start_line = start // record_length
    with path.open("rb") as stream:
        stream.seek(start)
        data = stream.read(end - start)
    view = memoryview(data)
    total = (len(view) // record_length) * record_length
    rows: list[dict[str, object]] = []
    index_rows: list[dict[str, object]] = []
    line_no = start_line
    for offset in range(0, total, record_length):
        block = view[offset : offset + record_length]
        record = parser.parse(block)
        parsed = model.model_validate(record)
        payload = parsed.model_dump()
        payload["source_id"] = source_id
        payload["line_no"] = line_no
        rows.append(payload)
        idx_row = build_index_row(
            fields=record,
            index_fields=index_fields,
            source_id=source_id,
            line_no=line_no,
            table_name=struct_name.lower(),
        )
        if idx_row is not None:
            index_rows.append(idx_row)
        line_no += 1
    return rows, index_rows
