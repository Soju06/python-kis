"""Service layer: lookup/search against prepared store indexes."""

from .config import StoreConfig
from .errors import RecordNotFound, SnapshotNotFound, StoreError
from .index import InMemoryIndex, Index
from .ingest import IngestPlan, StoreBuilder
from .loader import (
    LoadResult,
    load_source_def_into_sqlite,
    load_source_def_into_sqlite_parallel,
    load_source_into_sqlite,
)
from .paths import StorePaths, default_store_root, today_key
from .pipeline import SnapshotResult, build_snapshot, ensure_daily_snapshot
from .sqlite import StoreDb, TableDef
from .store import Store

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
    "default_store_root",
    "ensure_daily_snapshot",
    "load_source_into_sqlite",
    "today_key",
]
