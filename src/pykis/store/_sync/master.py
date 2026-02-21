from __future__ import annotations

from pathlib import Path
from typing import Iterable

from pydantic import BaseModel

from pykis.store._sync.backend.sqlite import SqliteBackend
from pykis.store.service.config import StoreConfig
from pykis.store.types import IndexRow


class SyncMasterStore:
    """Public master store API."""

    _config: StoreConfig | None
    _parallel: bool
    _source_parallel: bool
    _source_workers: int | None
    _lock_timeout_sec: float
    _backend: SqliteBackend | None

    __slots__ = (
        "_config",
        "_parallel",
        "_source_parallel",
        "_source_workers",
        "_lock_timeout_sec",
        "_backend",
    )

    def __init__(
        self,
        *,
        config: StoreConfig | None = None,
        parallel: bool = True,
        source_parallel: bool = False,
        source_workers: int | None = None,
        lock_timeout_sec: float = 900.0,
    ) -> None:
        self._config = config
        self._parallel = parallel
        self._source_parallel = source_parallel
        self._source_workers = source_workers
        self._lock_timeout_sec = lock_timeout_sec
        self._backend = None

    def __enter__(self) -> "SyncMasterStore":
        self._get_backend()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    @property
    def db_path(self) -> Path:
        if self._backend is None:
            raise RuntimeError("MasterStore is not initialized yet; use the context manager or call a method first.")
        return self._backend.db_path

    def get_db_path(self) -> Path:
        backend = self._get_backend()
        return backend.db_path

    def close(self) -> None:
        backend = self._backend
        if backend is None:
            return
        backend.close()
        self._backend = None

    def lookup_symbol(self, symbol: str, *, limit: int = 50) -> list[BaseModel]:
        indexes = self.lookup_symbol_index(symbol, limit=limit)
        return self._resolve_all(indexes)

    def lookup_standard(self, standard_code: str, *, limit: int = 50) -> list[BaseModel]:
        indexes = self.lookup_standard_index(standard_code, limit=limit)
        return self._resolve_all(indexes)

    def lookup_isin(self, isin: str, *, limit: int = 50) -> list[BaseModel]:
        indexes = self.lookup_isin_index(isin, limit=limit)
        return self._resolve_all(indexes)

    def lookup_symbol_index(self, symbol: str, *, limit: int = 50) -> list[IndexRow]:
        backend = self._get_backend()
        return backend.lookup_symbol_index(symbol, limit=limit)

    def lookup_standard_index(self, standard_code: str, *, limit: int = 50) -> list[IndexRow]:
        backend = self._get_backend()
        return backend.lookup_standard_index(standard_code, limit=limit)

    def lookup_isin_index(self, isin: str, *, limit: int = 50) -> list[IndexRow]:
        backend = self._get_backend()
        return backend.lookup_isin_index(isin, limit=limit)

    def resolve(self, index: IndexRow) -> BaseModel:
        backend = self._get_backend()
        return backend.resolve(index)

    def fetch_model(self, *, table_name: str, source_id: str, line_no: int) -> BaseModel | None:
        backend = self._get_backend()
        return backend.fetch_model(table_name=table_name, source_id=source_id, line_no=line_no)

    def _resolve_all(self, indexes: Iterable[IndexRow]) -> list[BaseModel]:
        backend = self._get_backend()
        resolved: list[BaseModel] = []
        for index in indexes:
            resolved.append(backend.resolve(index))
        return resolved

    def _get_backend(self) -> SqliteBackend:
        if self._backend is None:
            self._backend = SqliteBackend.open(
                config=self._config,
                parallel=self._parallel,
                source_parallel=self._source_parallel,
                source_workers=self._source_workers,
                lock_timeout_sec=self._lock_timeout_sec,
            )
        return self._backend
