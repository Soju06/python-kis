"""Optional master-data store for pykis.

This package is intentionally decoupled from the main API surface. Import and
use it only when you need local master data lookups.
"""

from pykis.store._async.master import MasterStore
from pykis.store._sync.master import SyncMasterStore
from pykis.store.service.config import StoreConfig
from pykis.store.service.errors import RecordNotFound, SnapshotNotFound, StoreError
from pykis.store.service.pipeline import (
    build_snapshot,
    build_snapshot_async,
    ensure_daily_snapshot,
    ensure_daily_snapshot_async,
)
from pykis.store.types import IndexRow

__all__ = [
    "IndexRow",
    "MasterStore",
    "RecordNotFound",
    "SnapshotNotFound",
    "SyncMasterStore",
    "StoreConfig",
    "StoreError",
    "build_snapshot",
    "build_snapshot_async",
    "ensure_daily_snapshot",
    "ensure_daily_snapshot_async",
]
