from __future__ import annotations

import os
import time
from pathlib import Path

import pytest

from pykis.store.raw.structs import STRUCT_DEFS
from pykis.store.registry import get_source
from pykis.store.service.indexing import detect_index_fields
from pykis.store.service.loader import load_source_def_into_sqlite, load_source_def_into_sqlite_parallel
from pykis.store.service.sqlite import StoreDb


def _write_idx_code_file(path: Path, count: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        for idx in range(count):
            idx_div = "0"
            idx_code = str(idx % 10000).zfill(4)
            name = f"NAME{idx:06d}"
            idx_name = name[:40].ljust(40)
            line = (idx_div + idx_code + idx_name).encode("euc-kr")
            if len(line) != 45:
                raise ValueError("invalid record length")
            handle.write(line)


def _create_indexes(db: StoreDb, table_name: str) -> None:
    source = get_source("idxcode")
    if source is None:
        raise RuntimeError("idxcode source not found")
    struct_def = source.struct_name
    record_spec = STRUCT_DEFS[struct_def].record_spec
    fields = detect_index_fields(struct_def, record_spec)
    columns = [name for name in (fields.symbol, fields.standard, fields.isin) if name]
    if columns:
        db.create_indexes_for_table(table_name, columns)
    db.create_global_indexes()
    db.conn.execute("ANALYZE")
    db.commit()


@pytest.mark.perf
def test_store_ingest_perf(tmp_path, record_property) -> None:
    records = int(os.getenv("PYKIS_BENCH_RECORDS", "20000"))
    parallel = os.getenv("PYKIS_BENCH_PARALLEL", "0") == "1"
    workers_env = os.getenv("PYKIS_BENCH_WORKERS")
    workers = int(workers_env) if workers_env else None
    chunk_bytes = int(os.getenv("PYKIS_BENCH_CHUNK_BYTES", str(8 * 1024 * 1024)))

    data_path = tmp_path / "idxcode.mst"
    _write_idx_code_file(data_path, records)

    source = get_source("idxcode")
    if source is None:
        raise RuntimeError("idxcode source not found")

    db_path = tmp_path / "store.sqlite"
    db = StoreDb(db_path)
    db.apply_ingest_pragmas()
    try:
        start = time.perf_counter()
        if parallel:
            result = load_source_def_into_sqlite_parallel(
                db,
                source=source,
                file_path=data_path,
                workers=workers,
                chunk_bytes=chunk_bytes,
            )
        else:
            result = load_source_def_into_sqlite(db, source=source, file_path=data_path)
        ingest_sec = time.perf_counter() - start

        start = time.perf_counter()
        _create_indexes(db, source.struct_name.lower())
        index_sec = time.perf_counter() - start
    finally:
        db.close()

    rows = result.rows
    total_sec = ingest_sec + index_sec
    rows_per_sec = rows / ingest_sec if ingest_sec else 0.0

    record_property("rows", rows)
    record_property("ingest_sec", ingest_sec)
    record_property("index_sec", index_sec)
    record_property("total_sec", total_sec)
    record_property("rows_per_sec", rows_per_sec)

    assert rows == records
    assert ingest_sec > 0
    assert total_sec > 0
