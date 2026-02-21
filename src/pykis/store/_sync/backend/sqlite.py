from __future__ import annotations

import pathlib
import sqlite3
from pathlib import Path
from sqlite3 import Row

from pydantic import BaseModel

from pykis.store.raw.structs import STRUCT_DEFS
from pykis.store.registry import get_model
from pykis.store.service.config import StoreConfig
from pykis.store.service.errors import RecordNotFound, SnapshotNotFound
from pykis.store.service.paths import StorePaths, today_key
from pykis.store.service.pipeline import ensure_daily_snapshot
from pykis.store.types import IndexRow

_TABLE_TO_STRUCT: dict[str, str] = {name.lower(): name for name in STRUCT_DEFS}
_INDEX_COLUMNS = {"symbol", "standard_code", "isin"}


class SqliteBackend:
    """SQLite-backed backend for master data lookup."""

    _conn: sqlite3.Connection
    _db_path: Path
    _root: Path
    _auto_refresh: bool
    _date_key: str | None
    _parallel: bool
    _source_parallel: bool
    _source_workers: int | None
    _lock_timeout_sec: float
    _model_cache: dict[str, type[BaseModel]]

    __slots__ = (
        "_conn",
        "_db_path",
        "_root",
        "_auto_refresh",
        "_date_key",
        "_parallel",
        "_source_parallel",
        "_source_workers",
        "_lock_timeout_sec",
        "_model_cache",
    )

    def __init__(
        self,
        *,
        conn: sqlite3.Connection,
        db_path: Path,
        root: Path,
        auto_refresh: bool,
        date_key: str | None,
        parallel: bool,
        source_parallel: bool,
        source_workers: int | None,
        lock_timeout_sec: float,
    ) -> None:
        self._conn = conn
        self._db_path = db_path
        self._root = root
        self._auto_refresh = auto_refresh
        self._date_key = date_key
        self._parallel = parallel
        self._source_parallel = source_parallel
        self._source_workers = source_workers
        self._lock_timeout_sec = lock_timeout_sec
        self._model_cache = {}

    @classmethod
    def open(
        cls,
        *,
        config: StoreConfig | None = None,
        parallel: bool = True,
        source_parallel: bool = False,
        source_workers: int | None = None,
        lock_timeout_sec: float = 900.0,
    ) -> "SqliteBackend":
        store_config = config or StoreConfig()
        auto_refresh = store_config.auto_refresh
        root = store_config.root
        if auto_refresh:
            snapshot = ensure_daily_snapshot(
                root=root,
                parallel=parallel,
                source_parallel=source_parallel,
                source_workers=source_workers,
                lock_timeout_sec=lock_timeout_sec,
            )
            date_key = snapshot.date_key
            db_path = snapshot.db_path
        else:
            date_key = None
            snapshot_dir = _resolve_snapshot_dir(store_config)
            db_path = snapshot_dir / "store.sqlite"
        if not pathlib.Path(db_path).exists():
            raise SnapshotNotFound(f"Snapshot DB not found: {db_path}")
        conn = _open_connection(db_path, read_only=True)
        _apply_fast_pragmas(conn, read_only=True)
        return cls(
            conn=conn,
            db_path=db_path,
            root=root,
            auto_refresh=auto_refresh,
            date_key=date_key,
            parallel=parallel,
            source_parallel=source_parallel,
            source_workers=source_workers,
            lock_timeout_sec=lock_timeout_sec,
        )

    @property
    def db_path(self) -> Path:
        return self._db_path

    def close(self) -> None:
        self._conn.close()

    def lookup_symbol_index(self, symbol: str, *, limit: int = 50) -> list[IndexRow]:
        self._ensure_fresh()
        return self._lookup_index("symbol", symbol, limit)

    def lookup_standard_index(self, standard_code: str, *, limit: int = 50) -> list[IndexRow]:
        self._ensure_fresh()
        return self._lookup_index("standard_code", standard_code, limit)

    def lookup_isin_index(self, isin: str, *, limit: int = 50) -> list[IndexRow]:
        self._ensure_fresh()
        return self._lookup_index("isin", isin, limit)

    def resolve(self, index: IndexRow) -> BaseModel:
        model = self.fetch_model(table_name=index.table_name, source_id=index.source_id, line_no=index.line_no)
        if model is None:
            raise RecordNotFound(f"Record not found: {index}")
        return model

    def fetch_row(self, *, table_name: str, source_id: str, line_no: int) -> dict[str, object] | None:
        sql = f'SELECT * FROM "{table_name}" WHERE source_id = ? AND line_no = ?'
        cursor = self._conn.execute(sql, (source_id, line_no))
        try:
            row = cursor.fetchone()
        finally:
            cursor.close()
        if row is None:
            return None
        return dict(row)

    def fetch_model(self, *, table_name: str, source_id: str, line_no: int) -> BaseModel | None:
        row = self.fetch_row(table_name=table_name, source_id=source_id, line_no=line_no)
        if row is None:
            return None
        model_type = self._model_for_table(table_name)
        return model_type.model_validate(row)

    def _ensure_fresh(self) -> None:
        if not self._auto_refresh:
            return
        current = today_key()
        if self._date_key == current:
            return
        snapshot = ensure_daily_snapshot(
            root=self._root,
            parallel=self._parallel,
            source_parallel=self._source_parallel,
            source_workers=self._source_workers,
            lock_timeout_sec=self._lock_timeout_sec,
        )
        if snapshot.db_path != self._db_path:
            self._conn.close()
            self._db_path = snapshot.db_path
            self._conn = _open_connection(self._db_path, read_only=True)
            _apply_fast_pragmas(self._conn, read_only=True)
        self._date_key = snapshot.date_key

    def _lookup_index(self, column: str, value: str, limit: int) -> list[IndexRow]:
        if column not in _INDEX_COLUMNS:
            raise ValueError(f"Unsupported index column: {column}")
        if limit <= 0:
            return []
        key = _normalize_key(value)
        if not key:
            return []
        sql = (
            "SELECT symbol, standard_code, isin, source_id, line_no, table_name "
            f"FROM instrument_index WHERE {column} = ? LIMIT ?"
        )
        cursor = self._conn.execute(sql, (key, limit))
        try:
            rows = cursor.fetchall()
        finally:
            cursor.close()
        return [
            IndexRow(
                symbol=row["symbol"],
                standard_code=row["standard_code"],
                isin=row["isin"],
                source_id=row["source_id"],
                line_no=row["line_no"],
                table_name=row["table_name"],
            )
            for row in rows
        ]

    def _model_for_table(self, table_name: str) -> type[BaseModel]:
        cached = self._model_cache.get(table_name)
        if cached is not None:
            return cached
        struct_name = _TABLE_TO_STRUCT.get(table_name.lower())
        if struct_name is None:
            raise KeyError(f"Unknown table name: {table_name}")
        model = get_model(struct_name)
        self._model_cache[table_name] = model
        return model


def _open_connection(db_path: Path, *, read_only: bool) -> sqlite3.Connection:
    if read_only:
        uri = f"file:{db_path}?mode=ro"
        conn = sqlite3.connect(uri, uri=True)
    else:
        conn = sqlite3.connect(db_path)
    conn.row_factory = Row
    return conn


def _apply_fast_pragmas(conn: sqlite3.Connection, *, read_only: bool) -> None:
    if not read_only:
        _exec_pragma(conn, "PRAGMA journal_mode=WAL")
    _exec_pragma(conn, "PRAGMA synchronous=NORMAL")
    _exec_pragma(conn, "PRAGMA temp_store=MEMORY")
    _exec_pragma(conn, "PRAGMA cache_size=-200000")
    _exec_pragma(conn, "PRAGMA locking_mode=EXCLUSIVE")


def _exec_pragma(conn: sqlite3.Connection, sql: str) -> None:
    cursor = conn.execute(sql)
    cursor.close()


def _normalize_key(value: str) -> str:
    return value.strip().upper()


def _resolve_snapshot_dir(config: StoreConfig) -> Path:
    if config.snapshot:
        return config.root / "snapshots" / config.snapshot
    paths = StorePaths(config.root)
    latest_path = pathlib.Path(paths.latest_file)
    if latest_path.exists():
        latest = (latest_path.read_text(encoding="utf-8")).strip()
        if latest:
            return paths.snapshot_date_dir(latest)
    return config.root / "snapshots" / "latest"
