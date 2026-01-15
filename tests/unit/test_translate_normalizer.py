from __future__ import annotations

import pytest

from pykis.store.raw.models import RawRecord
from pykis.store.translate.normalizer import FieldMap, FieldMapNormalizer

pytestmark = pytest.mark.unit


def test_field_map_normalizer_builds_instrument() -> None:
    mapping = FieldMap(
        symbol="sym",
        name="name",
        market="market",
        asset_class="asset",
        short_code="short",
        standard_code="std",
        isin="isin",
    )
    normalizer = FieldMapNormalizer(mapping=mapping, defaults={"market": "KR", "asset_class": "STOCK"}, version="v1")

    record = RawRecord(
        source_id="src",
        line_no=1,
        fields={
            "sym": " 005930 ",
            "name": "Samsung",
            "market": " kr ",
            "asset": " equity ",
            "short": "5930",
            "std": "KR7005930003",
            "isin": "KR7005930003",
        },
    )

    instrument = normalizer.normalize(record)
    assert instrument is not None
    assert instrument.key.symbol == "005930"
    assert instrument.key.market == "kr"
    assert instrument.key.asset_class == "equity"
    assert instrument.name == "Samsung"
    assert instrument.short_code == "5930"
    assert instrument.standard_code == "KR7005930003"
    assert instrument.isin == "KR7005930003"
    assert instrument.source_id == "src"
    assert instrument.version == "v1"


def test_field_map_normalizer_uses_defaults() -> None:
    mapping = FieldMap(symbol="sym", market="market", asset_class="asset")
    normalizer = FieldMapNormalizer(mapping=mapping, defaults={"market": "KR", "asset_class": "STOCK"})

    record = RawRecord(source_id="src", line_no=1, fields={"sym": " 1234 "})
    instrument = normalizer.normalize(record)

    assert instrument is not None
    assert instrument.key.symbol == "1234"
    assert instrument.key.market == "KR"
    assert instrument.key.asset_class == "STOCK"


def test_field_map_normalizer_requires_symbol() -> None:
    mapping = FieldMap(symbol="sym", market="market", asset_class="asset")
    normalizer = FieldMapNormalizer(mapping=mapping, defaults={"market": "KR", "asset_class": "STOCK"})

    record = RawRecord(source_id="src", line_no=1, fields={"market": "KR", "asset": "STOCK"})
    instrument = normalizer.normalize(record)

    assert instrument is None
