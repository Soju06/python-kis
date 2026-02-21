"""Optional master-data store for pykis.

This package is intentionally decoupled from the main API surface. Import and
use it only when you need local master data lookups.
"""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
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

_LAZY_IMPORTS = {
    "IndexRow": "pykis.store.types",
    "MasterStore": "pykis.store._async.master",
    "RecordNotFound": "pykis.store.service.errors",
    "SnapshotNotFound": "pykis.store.service.errors",
    "SyncMasterStore": "pykis.store._sync.master",
    "StoreConfig": "pykis.store.service.config",
    "StoreError": "pykis.store.service.errors",
    "build_snapshot": "pykis.store.service.pipeline",
    "build_snapshot_async": "pykis.store.service.pipeline",
    "ensure_daily_snapshot": "pykis.store.service.pipeline",
    "ensure_daily_snapshot_async": "pykis.store.service.pipeline",
}


def __getattr__(name: str):
    module_name = _LAZY_IMPORTS.get(name)
    if not module_name:
        raise AttributeError(f"module {__name__} has no attribute {name}")
    module = importlib.import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value
