from __future__ import annotations

import os
import random
import time
from pathlib import Path

import pytest

from pykis.store import StoreConfig, SyncMasterStore
from pykis.store.registry import get_source
from pykis.store.service.loader import load_source_def_into_sqlite
from pykis.store.service.sqlite import StoreDb


def _write_idx_code_file(path: Path, count: int) -> list[str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys: list[str] = []
    with path.open("wb") as handle:
        for idx in range(count):
            idx_div = "0"
            idx_code = str(idx % 10000).zfill(4)
            keys.append(idx_code)
            name = f"NAME{idx:06d}"
            idx_name = name[:40].ljust(40)
            line = (idx_div + idx_code + idx_name).encode("euc-kr")
            if len(line) != 45:
                raise ValueError("invalid record length")
            handle.write(line)
    return keys


def _prepare_db(tmp_path: Path, records: int) -> tuple[Path, list[str]]:
    data_path = tmp_path / "idxcode.mst"
    keys = _write_idx_code_file(data_path, records)
    source = get_source("idxcode")
    if source is None:
        raise RuntimeError("idxcode source not found")
    db_path = tmp_path / "snapshots" / "bench" / "store.sqlite"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = StoreDb(db_path)
    try:
        load_source_def_into_sqlite(db, source=source, file_path=data_path)
        db.create_global_indexes()
        db.conn.execute("ANALYZE")
        db.commit()
    finally:
        db.close()
    return db_path, keys


def _run_lookup(store: SyncMasterStore, keys: list[str], *, queries: int, include_model: bool) -> float:
    rng = random.Random(42)
    samples = [rng.choice(keys) for _ in range(queries)]
    for key in samples[: min(100, queries)]:
        if include_model:
            store.lookup_symbol(key, limit=1)
        else:
            store.lookup_symbol_index(key, limit=1)
    start = time.perf_counter()
    if include_model:
        for key in samples:
            store.lookup_symbol(key, limit=1)
    else:
        for key in samples:
            store.lookup_symbol_index(key, limit=1)
    return time.perf_counter() - start


@pytest.mark.perf
def test_store_lookup_perf(tmp_path, record_property) -> None:
    records = int(os.getenv("PYKIS_BENCH_RECORDS", "10000"))
    queries = int(os.getenv("PYKIS_BENCH_QUERIES", "20000"))

    _, keys = _prepare_db(tmp_path, records)
    unique_keys = list(dict.fromkeys(keys))
    config = StoreConfig(root=tmp_path, snapshot="bench", auto_refresh=False)
    with SyncMasterStore(config=config) as store:
        idx_time = _run_lookup(store, unique_keys, queries=queries, include_model=False)
        full_time = _run_lookup(store, unique_keys, queries=queries, include_model=True)

    idx_avg_us = (idx_time / queries) * 1_000_000
    full_avg_us = (full_time / queries) * 1_000_000

    record_property("records", records)
    record_property("queries", queries)
    record_property("index_only_sec", idx_time)
    record_property("index_only_avg_us", idx_avg_us)
    record_property("with_model_sec", full_time)
    record_property("with_model_avg_us", full_avg_us)

    assert idx_time > 0
    assert full_time > 0
