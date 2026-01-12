"""Optional master-data store for pykis.

This package is intentionally decoupled from the main API surface. Import and
use it only when you need local master data lookups.
"""

from .service.config import StoreConfig
from .service.errors import RecordNotFound, SnapshotNotFound, StoreError
from .service.pipeline import build_snapshot, ensure_daily_snapshot
from .service.store import Store
from .translate.models import Instrument, InstrumentKey
from .registry import build_raw_source, get_model, get_source, get_struct, list_sources, list_structs

__all__ = [
    "Instrument",
    "InstrumentKey",
    "RecordNotFound",
    "SnapshotNotFound",
    "Store",
    "StoreConfig",
    "StoreError",
    "build_snapshot",
    "build_raw_source",
    "get_model",
    "get_source",
    "get_struct",
    "list_sources",
    "list_structs",
    "ensure_daily_snapshot",
]
