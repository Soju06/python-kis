from __future__ import annotations

import pytest

from pykis.store.service.index import InMemoryIndex
from pykis.store.translate.models import Instrument, InstrumentKey

pytestmark = pytest.mark.unit


def test_in_memory_index_lookup_and_search() -> None:
    inst1 = Instrument(
        key=InstrumentKey(asset_class="STOCK", market="KR", symbol="005930"),
        name="Samsung Electronics",
        short_code="5930",
        standard_code="KR7005930003",
        isin="KR7005930003",
        source_id="kospi",
    )
    inst2 = Instrument(
        key=InstrumentKey(asset_class="STOCK", market="KR", symbol="000660"),
        name="SK Hynix",
        short_code="0660",
        standard_code="KR7000660001",
        isin="KR7000660001",
        source_id="kospi",
    )

    index = InMemoryIndex([inst1, inst2])

    assert index.lookup(inst1.key) is inst1
    assert index.lookup(InstrumentKey(asset_class="STOCK", market="KR", symbol="NOPE")) is None

    results = index.search_name("samsung", limit=10)
    assert inst1 in results
    assert inst2 not in results
