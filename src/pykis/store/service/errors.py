from pykis.errors import PykisError


class StoreError(PykisError):
    """Base error for store failures."""

    __slots__ = ()


class SnapshotNotFound(StoreError):
    """Snapshot not found on disk."""

    __slots__ = ()


class RecordNotFound(StoreError):
    """Record not found for lookup."""

    __slots__ = ()
