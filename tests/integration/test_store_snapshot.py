from __future__ import annotations

import pytest

from pykis.store import StoreConfig, SyncMasterStore
from pykis.store.raw.masters import SOURCE_DEFS
from pykis.store.service.pipeline import build_snapshot
from pykis.store.service.sqlite import StoreDb


@pytest.mark.integration
def test_snapshot_build_and_lookup(tmp_path) -> None:
    source = SOURCE_DEFS.get("idxcode")
    if source is None:
        raise AssertionError("idxcode source not found")

    result = build_snapshot(root=tmp_path, date_key="test-snapshot", sources=[source], parallel=False)
    assert result.db_path.exists()
    assert result.manifest_path.exists()

    db = StoreDb(result.db_path, read_only=True)
    try:
        row = db.conn.execute("SELECT symbol FROM instrument_index WHERE symbol IS NOT NULL LIMIT 1").fetchone()
        assert row is not None
        symbol = row["symbol"]
        assert symbol
    finally:
        db.close()

    config = StoreConfig(root=tmp_path, snapshot="test-snapshot", auto_refresh=False)
    with SyncMasterStore(config=config) as store:
        records = store.lookup_symbol(symbol, limit=1)

    assert records
    assert records[0].idx_code == symbol
