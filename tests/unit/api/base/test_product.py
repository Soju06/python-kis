import types

from vmkis.api.base import product as pb


def test_name_property_uses_info_call(monkeypatch):
    # Ensure .name obtains value via the info property which calls stock.info.info
    def fake_info(kis, symbol, market):
        return types.SimpleNamespace(name="MyProduct")

    monkeypatch.setattr("vmkis.api.stock.info.info", fake_info)

    p = pb.KisProductBase()
    p.kis = object()
    p.symbol = "AAA"
    p.market = "KRX"

    assert p.name == "MyProduct"


def test_info_calls_stock_info(monkeypatch):
    # ensure that property `info` calls vmkis.api.stock.info.info
    called = {}

    def fake_info(kis, symbol, market):
        called["args"] = (kis, symbol, market)
        return "INFO-OBJ"

    monkeypatch.setattr("vmkis.api.stock.info.info", fake_info)

    p = pb.KisProductBase()
    p.kis = object()
    p.symbol = "AAA"
    p.market = "KRX"

    assert p.info == "INFO-OBJ"
    assert called["args"] == (p.kis, "AAA", "KRX")


def test_stock_property_calls_scope_stock(monkeypatch):
    monkeypatch.setattr("vmkis.scope.stock.stock", lambda kis, symbol, market: "SCOPE")

    p = pb.KisProductBase()
    p.kis = object()
    p.symbol = "AAA"
    p.market = "KRX"

    assert p.stock == "SCOPE"
