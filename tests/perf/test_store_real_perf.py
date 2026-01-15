from __future__ import annotations

import os
import random
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import pytest

from pykis.store import StoreConfig, SyncMasterStore
from pykis.store.registry import get_source, get_struct
from pykis.store.service.indexing import detect_index_fields
from pykis.store.service.loader import load_source_def_into_sqlite, load_source_def_into_sqlite_parallel
from pykis.store.service.pipeline import download_sources, extract_sources
from pykis.store.service.sqlite import StoreDb, TableDef


def _collect_table_indexes(table_indexes: dict[str, list[str]], struct_name: str, record_spec) -> None:
    fields = detect_index_fields(struct_name, record_spec)
    columns = [name for name in (fields.symbol, fields.standard, fields.isin) if name]
    if not columns:
        return
    table_name = struct_name.lower()
    existing = table_indexes.get(table_name)
    if existing is None:
        table_indexes[table_name] = columns
    else:
        for column in columns:
            if column not in existing:
                existing.append(column)


def _create_indexes(db: StoreDb, table_indexes: dict[str, list[str]]) -> None:
    for table_name, columns in table_indexes.items():
        db.create_indexes_for_table(table_name, columns)
    db.create_global_indexes()
    db.conn.execute("ANALYZE")
    db.commit()


def _sample_symbols(db: StoreDb, limit: int) -> list[str]:
    rows = db.conn.execute(
        "SELECT DISTINCT symbol FROM instrument_index WHERE symbol IS NOT NULL LIMIT ?",
        (limit,),
    ).fetchall()
    return [row["symbol"] for row in rows if row["symbol"]]


def _run_lookup(store: SyncMasterStore, symbols: list[str], *, queries: int, include_model: bool) -> float:
    rng = random.Random(42)
    samples = [rng.choice(symbols) for _ in range(queries)]
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


def _load_source_shard(source_id: str, data_path: str, shard_path: str) -> tuple[str, int, str]:
    source = get_source(source_id)
    if source is None:
        raise RuntimeError(f"source not found: {source_id}")
    db = StoreDb(Path(shard_path))
    db.apply_ingest_pragmas()
    try:
        result = load_source_def_into_sqlite(db, source=source, file_path=Path(data_path))
        db.commit()
    finally:
        db.close()
    return source_id, result.rows, shard_path


def _merge_shard_db(db: StoreDb, shard_path: Path, table_name: str) -> None:
    alias = f"shard_{os.urandom(4).hex()}"
    db.conn.execute(f"ATTACH DATABASE ? AS {alias}", (str(shard_path),))
    try:
        db.conn.execute(f'INSERT INTO "{table_name}" SELECT * FROM {alias}."{table_name}"')
        db.conn.execute(
            f"""
            INSERT OR REPLACE INTO store_sources (
                source_id, group_name, label, download_url, header_url, struct_name, loaded_at
            )
            SELECT source_id, group_name, label, download_url, header_url, struct_name, loaded_at
            FROM {alias}.store_sources
            """
        )
        db.conn.execute(f"INSERT INTO instrument_index SELECT * FROM {alias}.instrument_index")
        db.conn.commit()
    except Exception:
        db.conn.rollback()
        raise
    finally:
        try:
            db.conn.execute(f"DETACH DATABASE {alias}")
        except Exception:
            db.conn.rollback()
            raise


def _load_sources_in_shards(
    *,
    source_ids: list[str],
    extracts: list[Path],
    shard_dir: Path,
    workers: int | None,
) -> dict[str, tuple[int, Path]]:
    if len(source_ids) != len(extracts):
        raise ValueError("sources and extracts must be aligned")
    source_workers = workers or max(1, (os.cpu_count() or 1) // 2)
    max_workers = min(len(source_ids), source_workers) if source_ids else 1
    futures = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for source_id, data_path in zip(source_ids, extracts):
            source = get_source(source_id)
            if source is None:
                raise RuntimeError(f"source not found: {source_id}")
            shard_path = shard_dir / f"{source_id}.sqlite"
            futures.append(
                executor.submit(
                    _load_source_shard,
                    source_id,
                    str(data_path),
                    str(shard_path),
                )
            )
        results = [future.result() for future in as_completed(futures)]
    return {source_id: (rows, Path(path)) for source_id, rows, path in results}


@pytest.mark.integration
@pytest.mark.perf
def test_store_real_data_perf(tmp_path, record_property) -> None:
    source_ids = os.getenv("PYKIS_REAL_BENCH_SOURCES", "kospi_code").split(",")
    parallel = os.getenv("PYKIS_REAL_BENCH_PARALLEL", "1") == "1"
    source_parallel = os.getenv("PYKIS_REAL_BENCH_SOURCE_PARALLEL", "0") == "1"
    workers_env = os.getenv("PYKIS_REAL_BENCH_WORKERS")
    workers = int(workers_env) if workers_env else None
    chunk_bytes = int(os.getenv("PYKIS_REAL_BENCH_CHUNK_BYTES", str(8 * 1024 * 1024)))
    lookup_queries = int(os.getenv("PYKIS_REAL_BENCH_LOOKUP", "5000"))

    sources = []
    for source_id in source_ids:
        source = get_source(source_id)
        if source is None:
            raise RuntimeError(f"source not found: {source_id}")
        sources.append(source)

    downloads_dir = tmp_path / "downloads"
    extracted_dir = tmp_path / "extracted"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    extracted_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.perf_counter()
    download_results = download_sources(sources, downloads_dir)
    download_sec = time.perf_counter() - t0

    t1 = time.perf_counter()
    extract_results = extract_sources(sources, download_results, extracted_dir)
    extract_sec = time.perf_counter() - t1

    snapshot_dir = tmp_path / "snapshots" / "bench"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    db_path = snapshot_dir / "store.sqlite"
    db = StoreDb(db_path)
    db.apply_ingest_pragmas()
    symbols: list[str] = []
    lookup_sec = 0.0
    lookup_full_sec = 0.0
    try:
        start = time.perf_counter()
        db.create_meta_tables()
        db.create_index_table()
        table_indexes: dict[str, list[str]] = {}
        total_rows = 0

        if source_parallel and len(sources) > 1:
            shard_dir = tmp_path / "shards"
            shard_dir.mkdir(parents=True, exist_ok=True)
            shard_results = _load_sources_in_shards(
                source_ids=source_ids,
                extracts=[result.data_path for result in extract_results],
                shard_dir=shard_dir,
                workers=workers,
            )
            for source in sources:
                struct_def = get_struct(source.struct_name)
                if struct_def is None:
                    raise KeyError(f"struct not found: {source.struct_name}")
                db.create_table(TableDef(name=source.struct_name.lower(), record_spec=struct_def.record_spec))
                rows, shard_path = shard_results[source.source_id]
                _merge_shard_db(db, shard_path, source.struct_name.lower())
                _collect_table_indexes(table_indexes, source.struct_name, struct_def.record_spec)
                total_rows += rows
        else:
            for source, extract in zip(sources, extract_results):
                if parallel:
                    load_result = load_source_def_into_sqlite_parallel(
                        db,
                        source=source,
                        file_path=extract.data_path,
                        workers=workers,
                        chunk_bytes=chunk_bytes,
                    )
                else:
                    load_result = load_source_def_into_sqlite(db, source=source, file_path=extract.data_path)
                struct_def = get_struct(source.struct_name)
                if struct_def is None:
                    raise KeyError(f"struct not found: {source.struct_name}")
                _collect_table_indexes(table_indexes, source.struct_name, struct_def.record_spec)
                total_rows += load_result.rows

        ingest_sec = time.perf_counter() - start

        start = time.perf_counter()
        _create_indexes(db, table_indexes)
        index_sec = time.perf_counter() - start

        if lookup_queries > 0:
            symbols = _sample_symbols(db, min(5000, lookup_queries))
    finally:
        db.close()

    if lookup_queries > 0 and symbols:
        config = StoreConfig(root=tmp_path, snapshot="bench", auto_refresh=False)
        with SyncMasterStore(config=config) as store:
            lookup_sec = _run_lookup(store, symbols, queries=lookup_queries, include_model=False)
            lookup_full_sec = _run_lookup(store, symbols, queries=lookup_queries, include_model=True)

    bytes_total = sum(result.data_path.stat().st_size for result in extract_results)
    rows_per_sec = total_rows / ingest_sec if ingest_sec else 0.0

    record_property("sources", ",".join(source_ids))
    record_property("rows", total_rows)
    record_property("bytes", bytes_total)
    record_property("download_sec", download_sec)
    record_property("extract_sec", extract_sec)
    record_property("ingest_sec", ingest_sec)
    record_property("index_sec", index_sec)
    record_property("rows_per_sec", rows_per_sec)
    record_property("lookup_sec", lookup_sec)
    record_property("lookup_full_sec", lookup_full_sec)

    assert total_rows > 0
    assert bytes_total > 0
    assert ingest_sec > 0
