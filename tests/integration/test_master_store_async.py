from __future__ import annotations

import pytest

from pykis.store import MasterStore, StoreConfig
from pykis.store.raw.masters import SOURCE_DEFS
from pykis.store.service.pipeline import build_snapshot
from pykis.store.service.sqlite import StoreDb


@pytest.mark.asyncio
@pytest.mark.integration
async def test_master_store_async_lookup(tmp_path) -> None:
    source = SOURCE_DEFS.get("idxcode")
    if source is None:
        raise AssertionError("idxcode source not found")

    result = build_snapshot(root=tmp_path, date_key="async-snapshot", sources=[source], parallel=False)

    db = StoreDb(result.db_path, read_only=True)
    try:
        row = db.conn.execute(
            "SELECT symbol FROM instrument_index WHERE symbol IS NOT NULL LIMIT 1"
        ).fetchone()
        assert row is not None
        symbol = row["symbol"]
    finally:
        db.close()

    config = StoreConfig(root=tmp_path, snapshot="async-snapshot", auto_refresh=False)
    async with MasterStore(config=config) as store:
        records = await store.lookup_symbol(symbol, limit=1)

    assert records
