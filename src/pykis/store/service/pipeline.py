from __future__ import annotations

import json
import os
import shutil
import uuid
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from ..generated.specs import SOURCE_DEFS, SourceDef
from ..registry import get_struct
from .indexing import detect_index_fields
from .loader import LoadResult, load_source_def_into_sqlite, load_source_def_into_sqlite_parallel
from .paths import StorePaths, atomic_write_text, default_store_root, read_text, today_key
from .sqlite import StoreDb


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
) -> SnapshotResult:
    root_path = root or default_store_root()
    paths = StorePaths(root_path)
    date_key = today_key()
    snapshot_dir = paths.snapshot_date_dir(date_key)
    db_path = paths.snapshot_db_path(date_key)
    manifest_path = paths.snapshot_manifest_path(date_key)
    done_path = paths.snapshot_done_path(date_key)

    latest = read_text(paths.latest_file)
    if latest == date_key and snapshot_dir.exists() and done_path.exists() and db_path.exists():
        return SnapshotResult(date_key=date_key, snapshot_dir=snapshot_dir, db_path=db_path, manifest_path=manifest_path)
    if not refresh and snapshot_dir.exists() and done_path.exists():
        return SnapshotResult(date_key=date_key, snapshot_dir=snapshot_dir, db_path=db_path, manifest_path=manifest_path)

    return build_snapshot(
        root=root_path,
        date_key=date_key,
        sources=sources,
        parallel=parallel,
    )


def build_snapshot(
    *,
    root: Path | None = None,
    date_key: str | None = None,
    sources: Iterable[SourceDef] | None = None,
    parallel: bool = True,
) -> SnapshotResult:
    root_path = root or default_store_root()
    paths = StorePaths(root_path)
    date_key = date_key or today_key()
    snapshot_dir = paths.snapshot_date_dir(date_key)
    tmp_dir = paths.snapshot_dir / f".tmp-{uuid.uuid4().hex}"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    cache_dir = paths.cache_date_dir(date_key)
    downloads_dir = cache_dir / "downloads"
    extracted_dir = cache_dir / "extracted"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    extracted_dir.mkdir(parents=True, exist_ok=True)

    if sources is None:
        sources = list(SOURCE_DEFS.values())

    download_results = download_sources(sources, downloads_dir)
    extract_results = extract_sources(sources, download_results, extracted_dir)

    db_path = tmp_dir / "store.sqlite"
    db = StoreDb(db_path)
    db.apply_ingest_pragmas()

    manifest: dict[str, object] = {
        "date": date_key,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sources": [],
    }
    try:
        for source, extract in zip(sources, extract_results):
            if parallel:
                result = load_source_def_into_sqlite_parallel(db, source=source, file_path=extract.data_path)
            else:
                result = load_source_def_into_sqlite(db, source=source, file_path=extract.data_path)
            _add_manifest_source(manifest, source, extract, result)
            _create_indexes(db, source)
        db.create_global_indexes()
        db.conn.execute("ANALYZE")
        db.commit()
    finally:
        db.close()

    manifest_path = tmp_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (tmp_dir / "DONE").write_text("ok", encoding="utf-8")

    _publish_snapshot(paths, date_key, tmp_dir)
    return SnapshotResult(date_key=date_key, snapshot_dir=snapshot_dir, db_path=paths.snapshot_db_path(date_key), manifest_path=paths.snapshot_manifest_path(date_key))


def download_source(source: SourceDef, downloads_dir: Path, *, refresh: bool = False) -> DownloadResult:
    file_name = Path(source.download_url).name
    dest = downloads_dir / file_name
    if dest.exists() and not refresh:
        return DownloadResult(source_id=source.source_id, download_path=dest)

    tmp = dest.with_suffix(dest.suffix + ".tmp")
    with requests.get(source.download_url, stream=True, timeout=30) as resp:
        resp.raise_for_status()
        with tmp.open("wb") as handle:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)
    tmp.replace(dest)
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


def extract_source(source: SourceDef, download_path: Path, extracted_dir: Path, *, refresh: bool = False) -> ExtractResult:
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


def _create_indexes(db: StoreDb, source: SourceDef) -> None:
    struct_def = get_struct(source.struct_name)
    if struct_def is None:
        return
    index_fields = detect_index_fields(source.struct_name, struct_def.record_spec)
    columns = [name for name in (index_fields.symbol, index_fields.standard, index_fields.isin) if name]
    if columns:
        db.create_indexes_for_table(source.struct_name.lower(), columns)


def _add_manifest_source(
    manifest: dict[str, object],
    source: SourceDef,
    extract: ExtractResult,
    result: LoadResult,
) -> None:
    items = manifest.setdefault("sources", [])
    if isinstance(items, list):
        items.append(
            {
                "source_id": source.source_id,
                "struct": source.struct_name,
                "download_url": source.download_url,
                "header_url": source.header_url,
                "file": str(extract.data_path),
                "rows": result.rows,
            }
        )


def _publish_snapshot(paths: StorePaths, date_key: str, tmp_dir: Path) -> None:
    snapshot_dir = paths.snapshot_date_dir(date_key)
    snapshot_dir.parent.mkdir(parents=True, exist_ok=True)
    if snapshot_dir.exists():
        shutil.rmtree(snapshot_dir)
    tmp_dir.replace(snapshot_dir)
    atomic_write_text(paths.latest_file, date_key)
