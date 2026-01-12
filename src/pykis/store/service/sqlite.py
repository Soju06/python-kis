from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

from pykis.store.raw.spec import RecordSpec


@dataclass(frozen=True, slots=True)
class TableDef:
    name: str
    record_spec: RecordSpec


class StoreDb:
    __slots__ = ("path", "conn")

    def __init__(self, path: Path, *, read_only: bool = False) -> None:
        self.path = path
        if read_only:
            uri = f"file:{path}?mode=ro"
            self.conn = sqlite3.connect(uri, uri=True)
        else:
            self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row

    def close(self) -> None:
        self.conn.close()

    def commit(self) -> None:
        self.conn.commit()

    def apply_fast_pragmas(self) -> None:
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.execute("PRAGMA temp_store=MEMORY")
        self.conn.execute("PRAGMA cache_size=-200000")
        self.conn.execute("PRAGMA locking_mode=EXCLUSIVE")

    def apply_ingest_pragmas(self) -> None:
        self.conn.execute("PRAGMA journal_mode=OFF")
        self.conn.execute("PRAGMA synchronous=OFF")
        self.conn.execute("PRAGMA temp_store=MEMORY")
        self.conn.execute("PRAGMA cache_size=-400000")
        self.conn.execute("PRAGMA locking_mode=EXCLUSIVE")

    def create_meta_tables(self) -> None:
        self.conn.execute(
            \"\"\"
            CREATE TABLE IF NOT EXISTS store_sources (
                source_id TEXT PRIMARY KEY,
                group_name TEXT NOT NULL,
                label TEXT NOT NULL,
                download_url TEXT NOT NULL,
                header_url TEXT NOT NULL,
                struct_name TEXT NOT NULL,
                loaded_at TEXT
            )
            \"\"\"
        )

    def create_table(self, table: TableDef) -> None:
        columns = ["source_id TEXT NOT NULL", "line_no INTEGER NOT NULL"]
        for field in table.record_spec.fields:
            columns.append(f'"{field.name}" TEXT')
        columns.append("PRIMARY KEY (source_id, line_no)")
        sql = f"CREATE TABLE IF NOT EXISTS {table.name} (" + ", ".join(columns) + ") WITHOUT ROWID"
        self.conn.execute(sql)

    def create_index_table(self) -> None:
        self.conn.execute(
            \"\"\"
            CREATE TABLE IF NOT EXISTS instrument_index (
                symbol TEXT,
                standard_code TEXT,
                isin TEXT,
                source_id TEXT NOT NULL,
                line_no INTEGER NOT NULL,
                table_name TEXT NOT NULL
            )
            \"\"\"
        )

    def insert_index_rows(self, rows: Iterable[Mapping[str, object]]) -> None:
        rows_list = list(rows)
        if not rows_list:
            return
        columns = list(rows_list[0].keys())
        col_names = ", ".join(f'\"{name}\"' for name in columns)
        placeholders = ", ".join("?" for _ in columns)
        sql = f"INSERT INTO instrument_index ({col_names}) VALUES ({placeholders})"
        values = [[row.get(col) for col in columns] for row in rows_list]
        self.conn.executemany(sql, values)

    def create_indexes_for_table(self, table_name: str, columns: Iterable[str]) -> None:
        for column in columns:
            index_name = f"idx_{table_name}_{column}"
            self.conn.execute(f'CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} (\"{column}\")')

    def create_global_indexes(self) -> None:
        self.create_index_table()
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_instrument_symbol ON instrument_index(symbol)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_instrument_standard ON instrument_index(standard_code)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_instrument_isin ON instrument_index(isin)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_instrument_source ON instrument_index(source_id, line_no)")

    def upsert_source(self, *, source_id: str, group: str, label: str, download_url: str, header_url: str, struct_name: str, loaded_at: str | None = None) -> None:
        self.create_meta_tables()
        self.conn.execute(
            \"\"\"
            INSERT INTO store_sources (source_id, group_name, label, download_url, header_url, struct_name, loaded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_id) DO UPDATE SET
                group_name=excluded.group_name,
                label=excluded.label,
                download_url=excluded.download_url,
                header_url=excluded.header_url,
                struct_name=excluded.struct_name,
                loaded_at=excluded.loaded_at
            \"\"\",
            (source_id, group, label, download_url, header_url, struct_name, loaded_at),
        )
        self.conn.commit()

    def insert_rows(self, table_name: str, rows: Iterable[Mapping[str, object]]) -> None:
        rows_list = list(rows)
        if not rows_list:
            return
        columns = list(rows_list[0].keys())
        col_names = ", ".join(f'"{name}"' for name in columns)
        placeholders = ", ".join("?" for _ in columns)
        sql = f"INSERT OR REPLACE INTO {table_name} ({col_names}) VALUES ({placeholders})"
        values = [[row.get(col) for col in columns] for row in rows_list]
        self.conn.executemany(sql, values)
