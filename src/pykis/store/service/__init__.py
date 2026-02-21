"""Service layer: lookup/search against prepared store indexes."""

from pykis.store.service.config import StoreConfig
from pykis.store.service.errors import RecordNotFound, SnapshotNotFound, StoreError
from pykis.store.service.index import Index, InMemoryIndex
from pykis.store.service.ingest import IngestPlan, StoreBuilder
from pykis.store.service.loader import (
    LoadResult,
    load_source_def_into_sqlite,
    load_source_def_into_sqlite_parallel,
    load_source_into_sqlite,
)
from pykis.store.service.paths import StorePaths, default_store_root, today_key
from pykis.store.service.pipeline import (
    SnapshotResult,
    build_snapshot,
    build_snapshot_async,
    ensure_daily_snapshot,
    ensure_daily_snapshot_async,
)
from pykis.store.service.sqlite import StoreDb, TableDef
from pykis.store.service.store import Store

__all__ = [
    "InMemoryIndex",
    "Index",
    "IngestPlan",
    "LoadResult",
    "load_source_def_into_sqlite",
    "load_source_def_into_sqlite_parallel",
    "RecordNotFound",
    "SnapshotNotFound",
    "Store",
    "StoreBuilder",
    "StoreConfig",
    "StoreError",
    "StorePaths",
    "StoreDb",
    "SnapshotResult",
    "TableDef",
    "build_snapshot",
    "build_snapshot_async",
    "default_store_root",
    "ensure_daily_snapshot",
    "ensure_daily_snapshot_async",
    "load_source_into_sqlite",
    "today_key",
]
