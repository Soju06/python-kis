from __future__ import annotations

from pathlib import Path

import pytest

from pykis.store import StoreConfig, SyncMasterStore
from pykis.store.parser.reader import FixedWidthReader
from pykis.store.registry import build_raw_source, get_source
from pykis.store.service.loader import load_source_def_into_sqlite
from pykis.store.service.sqlite import StoreDb

pytestmark = pytest.mark.unit


def _write_idx_code_file(path: Path, rows: list[tuple[str, str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        for idx_div, idx_code, idx_name in rows:
            idx_div = (idx_div or "")[:1].ljust(1)
            idx_code = (idx_code or "")[:4].ljust(4)
            idx_name = (idx_name or "")[:40].ljust(40)
            line = (idx_div + idx_code + idx_name).encode("euc-kr")
            assert len(line) == 45
            handle.write(line)


def _load_idx_code_db(db_path: Path, file_path: Path) -> None:
    source = get_source("idxcode")
    if source is None:
        raise AssertionError("idxcode source not found")
    db = StoreDb(db_path)
    try:
        load_source_def_into_sqlite(db, source=source, file_path=file_path, batch_size=2)
    finally:
        db.close()


def test_fixed_width_reader_parses_records(tmp_path: Path) -> None:
    file_path = tmp_path / "idxcode.mst"
    rows = [
        ("0", "0001", "ALPHA"),
        ("1", "0002", "BETA"),
    ]
    _write_idx_code_file(file_path, rows)

    raw_source = build_raw_source(source_id="idxcode", file_path=file_path)
    reader = FixedWidthReader(raw_source)
    with file_path.open("rb") as stream:
        records = list(reader.iter_records(stream))

    assert records[0].fields["idx_code"] == "0001"
    assert records[1].fields["idx_name"].strip() == "BETA"


def test_loader_creates_rows_and_index(tmp_path: Path) -> None:
    file_path = tmp_path / "idxcode.mst"
    rows = [
        ("0", "0001", "ALPHA"),
        ("0", "0002", "BETA"),
        ("0", "0003", "GAMMA"),
    ]
    _write_idx_code_file(file_path, rows)

    db_path = tmp_path / "store.sqlite"
    source = get_source("idxcode")
    assert source is not None

    db = StoreDb(db_path)
    try:
        result = load_source_def_into_sqlite(db, source=source, file_path=file_path, batch_size=2)
        assert result.rows == len(rows)
        table_name = source.struct_name.lower()
        count = db.conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        assert count == len(rows)
        idx_count = db.conn.execute("SELECT COUNT(*) FROM instrument_index").fetchone()[0]
        assert idx_count == len(rows)
        first = db.conn.execute(
            "SELECT symbol, standard_code, isin FROM instrument_index ORDER BY line_no LIMIT 1"
        ).fetchone()
        assert first["symbol"] == "0001"
        assert first["standard_code"] is None
        assert first["isin"] is None
    finally:
        db.close()


def test_sqlite_store_lookup(tmp_path: Path) -> None:
    file_path = tmp_path / "idxcode.mst"
    rows = [
        ("0", "0001", "ALPHA"),
        ("0", "0002", "BETA"),
    ]
    _write_idx_code_file(file_path, rows)

    snapshot_dir = tmp_path / "snapshots" / "test"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    db_path = snapshot_dir / "store.sqlite"
    _load_idx_code_db(db_path, file_path)

    config = StoreConfig(root=tmp_path, snapshot="test", auto_refresh=False)
    with SyncMasterStore(config=config) as store:
        records = store.lookup_symbol("0002")

    assert records
    record = records[0]
    assert record.idx_code == "0002"
