from __future__ import annotations

import asyncio
import json
import os
import shutil
import uuid
import zipfile
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, cast

import aiopath
import httpx

from pykis.store.parser.definitions import SourceDef
from pykis.store.raw.masters import SOURCE_DEFS
from pykis.store.registry import get_struct
from pykis.store.service.indexing import detect_index_fields
from pykis.store.service.loader import LoadResult, load_source_def_into_sqlite, load_source_def_into_sqlite_parallel
from pykis.store.service.lock import AsyncFileLock, FileLock
from pykis.store.service.paths import StorePaths, atomic_write_text, default_store_root, read_text, today_key
from pykis.store.service.sqlite import StoreDb, TableDef


@dataclass(frozen=True, slots=True)
class DownloadResult:
    source_id: str
    download_path: Path


@dataclass(frozen=True, slots=True)
class ExtractResult:
    source_id: str
    data_path: Path


@dataclass(frozen=True, slots=True)
class SnapshotResult:
    date_key: str
    snapshot_dir: Path
    db_path: Path
    manifest_path: Path


def ensure_daily_snapshot(
    *,
    root: Path | None = None,
    sources: Iterable[SourceDef] | None = None,
    refresh: bool = True,
    parallel: bool = True,
    source_parallel: bool = False,
    source_workers: int | None = None,
    lock_timeout_sec: float = 900.0,
) -> SnapshotResult:
    root_path = root or default_store_root()
    paths = StorePaths(root_path)
    date_key = today_key()
    snapshot_dir = paths.snapshot_date_dir(date_key)
    db_path = paths.snapshot_db_path(date_key)
    manifest_path = paths.snapshot_manifest_path(date_key)
    done_path = paths.snapshot_done_path(date_key)

    lock = FileLock(paths.snapshot_lock_path(date_key), timeout_sec=lock_timeout_sec)
    with lock:
        latest = read_text(paths.latest_file)
        if latest == date_key and snapshot_dir.exists() and done_path.exists() and db_path.exists():
            return SnapshotResult(
                date_key=date_key,
                snapshot_dir=snapshot_dir,
                db_path=db_path,
                manifest_path=manifest_path,
            )
        if not refresh and snapshot_dir.exists() and done_path.exists():
            return SnapshotResult(
                date_key=date_key,
                snapshot_dir=snapshot_dir,
                db_path=db_path,
                manifest_path=manifest_path,
            )

        return build_snapshot(
            root=root_path,
            date_key=date_key,
            sources=sources,
            parallel=parallel,
            source_parallel=source_parallel,
            source_workers=source_workers,
            lock_timeout_sec=lock_timeout_sec,
            _lock=lock,
        )


def build_snapshot(
    *,
    root: Path | None = None,
    date_key: str | None = None,
    sources: Iterable[SourceDef] | None = None,
    parallel: bool = True,
    source_parallel: bool = False,
    source_workers: int | None = None,
    lock_timeout_sec: float = 900.0,
    _lock: FileLock | None = None,
) -> SnapshotResult:
    root_path = root or default_store_root()
    paths = StorePaths(root_path)
    date_key = date_key or today_key()
    if _lock is None:
        lock = FileLock(paths.snapshot_lock_path(date_key), timeout_sec=lock_timeout_sec)
        with lock:
            return _build_snapshot_locked(
                root_path=root_path,
                paths=paths,
                date_key=date_key,
                sources=sources,
                parallel=parallel,
                source_parallel=source_parallel,
                source_workers=source_workers,
            )
    return _build_snapshot_locked(
        root_path=root_path,
        paths=paths,
        date_key=date_key,
        sources=sources,
        parallel=parallel,
        source_parallel=source_parallel,
        source_workers=source_workers,
    )


async def ensure_daily_snapshot_async(
    *,
    root: Path | None = None,
    sources: Iterable[SourceDef] | None = None,
    refresh: bool = True,
    parallel: bool = True,
    source_parallel: bool = False,
    source_workers: int | None = None,
    lock_timeout_sec: float = 900.0,
) -> SnapshotResult:
    root_path = root or default_store_root()
    paths = StorePaths(root_path)
    date_key = today_key()
    snapshot_dir = paths.snapshot_date_dir(date_key)
    db_path = paths.snapshot_db_path(date_key)
    manifest_path = paths.snapshot_manifest_path(date_key)
    done_path = paths.snapshot_done_path(date_key)

    lock = AsyncFileLock(paths.snapshot_lock_path(date_key), timeout_sec=lock_timeout_sec)
    async with lock:
        latest = await _read_text_async(paths.latest_file)
        snapshot_ready = await _snapshot_ready(snapshot_dir, done_path, db_path)
        if latest == date_key and snapshot_ready:
            return SnapshotResult(
                date_key=date_key,
                snapshot_dir=snapshot_dir,
                db_path=db_path,
                manifest_path=manifest_path,
            )
        if not refresh and snapshot_ready:
            return SnapshotResult(
                date_key=date_key,
                snapshot_dir=snapshot_dir,
                db_path=db_path,
                manifest_path=manifest_path,
            )

        return await build_snapshot_async(
            root=root_path,
            date_key=date_key,
            sources=sources,
            parallel=parallel,
            source_parallel=source_parallel,
            source_workers=source_workers,
            lock_timeout_sec=lock_timeout_sec,
            _lock=lock,
        )


async def build_snapshot_async(
    *,
    root: Path | None = None,
    date_key: str | None = None,
    sources: Iterable[SourceDef] | None = None,
    parallel: bool = True,
    source_parallel: bool = False,
    source_workers: int | None = None,
    lock_timeout_sec: float = 900.0,
    _lock: AsyncFileLock | None = None,
) -> SnapshotResult:
    root_path = root or default_store_root()
    paths = StorePaths(root_path)
    date_key = date_key or today_key()
    if _lock is None:
        lock = AsyncFileLock(paths.snapshot_lock_path(date_key), timeout_sec=lock_timeout_sec)
        async with lock:
            return await _build_snapshot_locked_async(
                root_path=root_path,
                paths=paths,
                date_key=date_key,
                sources=sources,
                parallel=parallel,
                source_parallel=source_parallel,
                source_workers=source_workers,
            )
    return await _build_snapshot_locked_async(
        root_path=root_path,
        paths=paths,
        date_key=date_key,
        sources=sources,
        parallel=parallel,
        source_parallel=source_parallel,
        source_workers=source_workers,
    )


def _build_snapshot_locked(
    *,
    root_path: Path,
    paths: StorePaths,
    date_key: str,
    sources: Iterable[SourceDef] | None,
    parallel: bool,
    source_parallel: bool,
    source_workers: int | None,
) -> SnapshotResult:
    snapshot_dir = paths.snapshot_date_dir(date_key)
    tmp_dir = paths.snapshot_dir / f".tmp-{uuid.uuid4().hex}"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    cache_dir = paths.cache_date_dir(date_key)
    downloads_dir = cache_dir / "downloads"
    extracted_dir = cache_dir / "extracted"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    extracted_dir.mkdir(parents=True, exist_ok=True)

    if sources is None:
        sources_list = list(SOURCE_DEFS.values())
    else:
        sources_list = list(sources)

    download_results = download_sources(sources_list, downloads_dir)
    extract_results = extract_sources(sources_list, download_results, extracted_dir)

    manifest: dict[str, object] = {
        "date": date_key,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sources": [],
    }
    _populate_db_from_extracts(
        tmp_dir=tmp_dir,
        sources=sources_list,
        extracts=extract_results,
        parallel=parallel,
        source_parallel=source_parallel,
        source_workers=source_workers,
        manifest=manifest,
    )

    manifest_path = tmp_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (tmp_dir / "DONE").write_text("ok", encoding="utf-8")

    _publish_snapshot(paths, date_key, tmp_dir)
    return SnapshotResult(
        date_key=date_key,
        snapshot_dir=snapshot_dir,
        db_path=paths.snapshot_db_path(date_key),
        manifest_path=paths.snapshot_manifest_path(date_key),
    )


def _populate_db_from_extracts(
    *,
    tmp_dir: Path,
    sources: list[SourceDef],
    extracts: list[ExtractResult],
    parallel: bool,
    source_parallel: bool,
    source_workers: int | None,
    manifest: dict[str, object],
) -> Path:
    table_indexes: dict[str, list[str]] = {}
    db_path = tmp_dir / "store.sqlite"
    db = StoreDb(db_path)
    db.apply_ingest_pragmas()
    db.create_meta_tables()
    db.create_index_table()
    try:
        if source_parallel and len(sources) > 1:
            shard_dir = tmp_dir / "shards"
            shard_dir.mkdir(parents=True, exist_ok=True)
            shard_results = _load_sources_in_shards(
                sources=sources,
                extracts=extracts,
                shard_dir=shard_dir,
                workers=source_workers,
            )
            for source, extract, shard in shard_results:
                struct_def = get_struct(source.struct_name)
                if struct_def is None:
                    raise KeyError(f"struct not found: {source.struct_name}")
                db.create_table(TableDef(name=source.struct_name.lower(), record_spec=struct_def.record_spec))
                _merge_shard_db(db, shard.shard_path, source.struct_name.lower())
                _add_manifest_source(manifest, source, extract, shard.load_result)
                _collect_table_indexes(table_indexes, source, struct_def.record_spec)
        else:
            for source, extract in zip(sources, extracts):
                if parallel:
                    result = load_source_def_into_sqlite_parallel(db, source=source, file_path=extract.data_path)
                else:
                    result = load_source_def_into_sqlite(db, source=source, file_path=extract.data_path)
                _add_manifest_source(manifest, source, extract, result)
                struct_def = get_struct(source.struct_name)
                if struct_def is None:
                    raise KeyError(f"struct not found: {source.struct_name}")
                _collect_table_indexes(table_indexes, source, struct_def.record_spec)

        _create_indexes(db, table_indexes)
        db.create_global_indexes()
        db.conn.execute("ANALYZE")
        db.commit()
    finally:
        db.close()
    return db_path


async def _build_snapshot_locked_async(
    *,
    root_path: Path,
    paths: StorePaths,
    date_key: str,
    sources: Iterable[SourceDef] | None,
    parallel: bool,
    source_parallel: bool,
    source_workers: int | None,
) -> SnapshotResult:
    snapshot_dir = paths.snapshot_date_dir(date_key)
    tmp_dir = paths.snapshot_dir / f".tmp-{uuid.uuid4().hex}"
    await aiopath.AsyncPath(tmp_dir).mkdir(parents=True, exist_ok=True)

    cache_dir = paths.cache_date_dir(date_key)
    downloads_dir = cache_dir / "downloads"
    extracted_dir = cache_dir / "extracted"
    await aiopath.AsyncPath(downloads_dir).mkdir(parents=True, exist_ok=True)
    await aiopath.AsyncPath(extracted_dir).mkdir(parents=True, exist_ok=True)

    if sources is None:
        sources_list = list(SOURCE_DEFS.values())
    else:
        sources_list = list(sources)

    download_results = await download_sources_async(sources_list, downloads_dir)
    extract_results = await extract_sources_async(sources_list, download_results, extracted_dir)

    manifest: dict[str, object] = {
        "date": date_key,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sources": [],
    }
    await asyncio.to_thread(
        _populate_db_from_extracts,
        tmp_dir=tmp_dir,
        sources=sources_list,
        extracts=extract_results,
        parallel=parallel,
        source_parallel=source_parallel,
        source_workers=source_workers,
        manifest=manifest,
    )

    manifest_path = tmp_dir / "manifest.json"
    await aiopath.AsyncPath(manifest_path).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    await aiopath.AsyncPath(tmp_dir / "DONE").write_text("ok", encoding="utf-8")

    await asyncio.to_thread(_publish_snapshot, paths, date_key, tmp_dir)
    return SnapshotResult(
        date_key=date_key,
        snapshot_dir=snapshot_dir,
        db_path=paths.snapshot_db_path(date_key),
        manifest_path=paths.snapshot_manifest_path(date_key),
    )


def download_source(source: SourceDef, downloads_dir: Path, *, refresh: bool = False) -> DownloadResult:
    file_name = Path(source.download_url).name
    dest = downloads_dir / file_name
    if dest.exists() and not refresh:
        return DownloadResult(source_id=source.source_id, download_path=dest)

    temporary_path = dest.with_suffix(dest.suffix + ".tmp")
    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        with client.stream("GET", source.download_url) as response:
            response.raise_for_status()
            with temporary_path.open("wb") as handle:
                for chunk in response.iter_bytes(chunk_size=1024 * 1024):
                    if chunk:
                        handle.write(chunk)
    temporary_path.replace(dest)
    return DownloadResult(source_id=source.source_id, download_path=dest)


def download_sources(sources: Iterable[SourceDef], downloads_dir: Path, *, workers: int = 4) -> list[DownloadResult]:
    source_list = list(sources)
    if not source_list:
        return []
    results: list[DownloadResult] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(download_source, source, downloads_dir): source for source in source_list}
        for future in as_completed(futures):
            results.append(future.result())
    result_map = {result.source_id: result for result in results}
    return [result_map[source.source_id] for source in source_list]


def extract_source(
    source: SourceDef,
    download_path: Path,
    extracted_dir: Path,
    *,
    refresh: bool = False,
) -> ExtractResult:
    if download_path.suffix.lower() == ".zip":
        target = _resolve_extracted_path(extracted_dir, source)
        if target.exists() and not refresh:
            return ExtractResult(source_id=source.source_id, data_path=target)
        target = _extract_single_file(download_path, target)
        return ExtractResult(source_id=source.source_id, data_path=target)
    return ExtractResult(source_id=source.source_id, data_path=download_path)


def extract_sources(
    sources: Iterable[SourceDef],
    downloads: Iterable[DownloadResult],
    extracted_dir: Path,
    *,
    workers: int = 4,
) -> list[ExtractResult]:
    source_list = list(sources)
    download_list = list(downloads)
    if len(source_list) != len(download_list):
        raise ValueError("sources and downloads must be aligned")
    results: list[ExtractResult] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(extract_source, source, download.download_path, extracted_dir): source
            for source, download in zip(source_list, download_list)
        }
        for future in as_completed(futures):
            results.append(future.result())
    result_map = {result.source_id: result for result in results}
    return [result_map[source.source_id] for source in source_list]


async def download_source_async(
    source: SourceDef,
    downloads_dir: Path,
    *,
    refresh: bool = False,
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
) -> DownloadResult:
    file_name = Path(source.download_url).name
    dest = downloads_dir / file_name
    dest_path = aiopath.AsyncPath(dest)
    if await dest_path.exists() and not refresh:
        return DownloadResult(source_id=source.source_id, download_path=dest)

    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp_path = aiopath.AsyncPath(tmp)
    await dest_path.parent.mkdir(parents=True, exist_ok=True)
    async with semaphore:
        async with client.stream("GET", source.download_url) as resp:
            resp.raise_for_status()
            async with tmp_path.open("wb") as handle:
                async for chunk in resp.aiter_bytes(chunk_size=1024 * 1024):
                    if chunk:
                        await handle.write(chunk)
    await tmp_path.replace(dest)
    return DownloadResult(source_id=source.source_id, download_path=dest)


async def download_sources_async(
    sources: Iterable[SourceDef],
    downloads_dir: Path,
    *,
    workers: int = 4,
    refresh: bool = False,
) -> list[DownloadResult]:
    source_list = list(sources)
    if not source_list:
        return []
    semaphore = asyncio.Semaphore(max(1, workers))
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        tasks = [
            download_source_async(
                source,
                downloads_dir,
                refresh=refresh,
                client=client,
                semaphore=semaphore,
            )
            for source in source_list
        ]
        results = await asyncio.gather(*tasks)
    result_map = {result.source_id: result for result in results}
    return [result_map[source.source_id] for source in source_list]


async def extract_source_async(
    source: SourceDef,
    download_path: Path,
    extracted_dir: Path,
    *,
    refresh: bool = False,
    semaphore: asyncio.Semaphore,
) -> ExtractResult:
    if download_path.suffix.lower() == ".zip":
        target = _resolve_extracted_path(extracted_dir, source)
        target_path = aiopath.AsyncPath(target)
        if await target_path.exists() and not refresh:
            return ExtractResult(source_id=source.source_id, data_path=target)
        async with semaphore:
            extracted = await asyncio.to_thread(_extract_single_file, download_path, target)
        return ExtractResult(source_id=source.source_id, data_path=extracted)
    return ExtractResult(source_id=source.source_id, data_path=download_path)


async def extract_sources_async(
    sources: Iterable[SourceDef],
    downloads: Iterable[DownloadResult],
    extracted_dir: Path,
    *,
    workers: int = 4,
    refresh: bool = False,
) -> list[ExtractResult]:
    source_list = list(sources)
    download_list = list(downloads)
    if len(source_list) != len(download_list):
        raise ValueError("sources and downloads must be aligned")
    semaphore = asyncio.Semaphore(max(1, workers))
    tasks = [
        extract_source_async(
            source,
            download.download_path,
            extracted_dir,
            refresh=refresh,
            semaphore=semaphore,
        )
        for source, download in zip(source_list, download_list)
    ]
    results = await asyncio.gather(*tasks)
    result_map = {result.source_id: result for result in results}
    return [result_map[source.source_id] for source in source_list]


async def _snapshot_ready(snapshot_dir: Path, done_path: Path, db_path: Path) -> bool:
    snapshot_exists = await aiopath.AsyncPath(snapshot_dir).exists()
    done_exists = await aiopath.AsyncPath(done_path).exists()
    db_exists = await aiopath.AsyncPath(db_path).exists()
    return snapshot_exists and done_exists and db_exists


async def _read_text_async(path: Path) -> str | None:
    async_path = aiopath.AsyncPath(path)
    if not await async_path.exists():
        return None
    return (await async_path.read_text(encoding="utf-8")).strip() or None


def _resolve_extracted_path(extracted_dir: Path, source: SourceDef) -> Path:
    return extracted_dir / f"{source.source_id}.mst"


def _extract_single_file(zip_path: Path, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zipf:
        members = [name for name in zipf.namelist() if name.lower().endswith((".mst", ".cod"))]
        if not members:
            raise RuntimeError(f"No .mst/.cod file found in {zip_path}")
        member = members[0]
        suffix = Path(member).suffix.lower()
        final_path = out_path.with_suffix(suffix if suffix else out_path.suffix)
        if final_path != out_path:
            out_path = final_path
        with zipf.open(member) as src, out_path.open("wb") as dst:
            shutil.copyfileobj(src, dst, length=1024 * 1024)
    return out_path


def _collect_table_indexes(table_indexes: dict[str, list[str]], source: SourceDef, record_spec) -> None:
    index_fields = detect_index_fields(source.struct_name, record_spec)
    columns = [name for name in (index_fields.symbol, index_fields.standard, index_fields.isin) if name]
    if not columns:
        return
    table_name = source.struct_name.lower()
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


def _add_manifest_source(
    manifest: dict[str, object],
    source: SourceDef,
    extract: ExtractResult,
    result: LoadResult,
) -> None:
    items = manifest.setdefault("sources", [])
    if isinstance(items, list):
        payload: dict[str, object] = {
            "source_id": source.source_id,
            "struct": source.struct_name,
            "download_url": source.download_url,
            "header_url": source.header_url,
            "file": str(extract.data_path),
            "rows": result.rows,
        }
        sources = cast(list[dict[str, object]], items)
        sources.append(payload)


def _publish_snapshot(paths: StorePaths, date_key: str, tmp_dir: Path) -> None:
    snapshot_dir = paths.snapshot_date_dir(date_key)
    snapshot_dir.parent.mkdir(parents=True, exist_ok=True)
    if snapshot_dir.exists():
        shutil.rmtree(snapshot_dir)
    tmp_dir.replace(snapshot_dir)
    atomic_write_text(paths.latest_file, date_key)
    _publish_latest_db(paths.root, snapshot_dir / "store.sqlite")


def _publish_latest_db(root: Path, db_path: Path) -> None:
    target = root / "store.sqlite"
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        target.unlink()
    try:
        os.link(db_path, target)
    except OSError:
        shutil.copy2(db_path, target)


@dataclass(frozen=True, slots=True)
class ShardResult:
    source_id: str
    shard_path: Path
    load_result: LoadResult


def _load_sources_in_shards(
    *,
    sources: list[SourceDef],
    extracts: list[ExtractResult],
    shard_dir: Path,
    workers: int | None,
) -> list[tuple[SourceDef, ExtractResult, ShardResult]]:
    if len(sources) != len(extracts):
        raise ValueError("sources and extracts must be aligned")
    source_workers = workers or max(1, (os.cpu_count() or 1) // 2)
    max_workers = min(len(sources), source_workers) if sources else 1
    futures = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for source, extract in zip(sources, extracts):
            shard_path = shard_dir / f"{source.source_id}.sqlite"
            futures.append(
                executor.submit(
                    _load_source_shard,
                    source,
                    str(extract.data_path),
                    str(shard_path),
                )
            )
        results = [future.result() for future in as_completed(futures)]
    shard_map = {result.source_id: result for result in results}
    return [(source, extract, shard_map[source.source_id]) for source, extract in zip(sources, extracts)]


def _load_source_shard(source: SourceDef, data_path: str, shard_path: str) -> ShardResult:
    from pathlib import Path

    db = StoreDb(Path(shard_path))
    db.apply_ingest_pragmas()
    try:
        result = load_source_def_into_sqlite(db, source=source, file_path=Path(data_path))
        db.commit()
    finally:
        db.close()
    return ShardResult(source_id=source.source_id, shard_path=Path(shard_path), load_result=result)


def _merge_shard_db(db: StoreDb, shard_path: Path, table_name: str) -> None:
    alias = f"shard_{uuid.uuid4().hex}"
    db.conn.execute(f"ATTACH DATABASE ? AS {alias}", (str(shard_path),))
    try:
        db.conn.execute(f'INSERT INTO "{table_name}" SELECT * FROM {alias}."{table_name}"')
        db.conn.execute(
            f"""
            INSERT INTO store_sources (
                source_id, group_name, label, download_url, header_url, struct_name, loaded_at
            )
            SELECT source_id, group_name, label, download_url, header_url, struct_name, loaded_at
            FROM {alias}.store_sources
            ON CONFLICT(source_id) DO UPDATE SET
                group_name=excluded.group_name,
                label=excluded.label,
                download_url=excluded.download_url,
                header_url=excluded.header_url,
                struct_name=excluded.struct_name,
                loaded_at=excluded.loaded_at
            """
        )
        db.conn.execute(f"INSERT INTO instrument_index SELECT * FROM {alias}.instrument_index")
    finally:
        db.conn.execute(f"DETACH DATABASE {alias}")
