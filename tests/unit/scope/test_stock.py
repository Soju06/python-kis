from types import SimpleNamespace

import pytest

import vmkis.scope.stock as stock_mod


class DummyKis:
    def __init__(self, primary=None):
        self.primary = primary


def test_stock_uses_info_and_primary_account(monkeypatch):
    # arrange: fake _info to return different symbol/market
    def fake_info(self, symbol, market):
        assert isinstance(self, DummyKis)
        # ensure original args forwarded
        return SimpleNamespace(symbol="RET_SYM", market="RET_MKT")

    # fake KisProductEventFilter to record registration
    class FakeFilter:
        def __init__(self, owner):
            owner._filter_registered = True

    monkeypatch.setattr(stock_mod, "_info", fake_info)
    monkeypatch.setattr(stock_mod, "KisProductEventFilter", FakeFilter)

    primary_acc = object()
    kis = DummyKis(primary=primary_acc)

    # act
    res = stock_mod.stock(kis, symbol="INPUT", market=None, account=None)

    # assert
    assert isinstance(res, stock_mod.KisStockScope)
    assert res.symbol == "RET_SYM"
    assert res.market == "RET_MKT"
    # when account is None, should use kis.primary
    assert res.account_number is primary_acc
    # filter registration happened
    assert getattr(res, "_filter_registered", False) is True


def test_stock_uses_given_account_and_market_forwarding(monkeypatch):
    # ensure market argument forwarded to _info
    called = {}

    def fake_info(self, symbol, market):
        called["symbol"] = symbol
        called["market"] = market
        return SimpleNamespace(symbol=symbol + "_X", market=(market or "DEF"))

    monkeypatch.setattr(stock_mod, "_info", fake_info)
    # make filter noop to avoid side effects
    monkeypatch.setattr(stock_mod, "KisProductEventFilter", type("F", (), {"__init__": lambda self, owner: None}))

    kis = DummyKis(primary=None)
    account_obj = object()

    res = stock_mod.stock(kis, symbol="SYM1", market="MKT1", account=account_obj)

    assert called["symbol"] == "SYM1"
    assert called["market"] == "MKT1"
    assert res.symbol == "SYM1_X"
    assert res.market == "MKT1"
    assert res.account_number is account_obj


def test_stock_propagates_exceptions_from_info(monkeypatch):
    def raise_not_found(self, symbol, market):
        raise ValueError("not found")

    monkeypatch.setattr(stock_mod, "_info", raise_not_found)
    monkeypatch.setattr(stock_mod, "KisProductEventFilter", type("F", (), {"__init__": lambda self, owner: None}))

    kis = DummyKis(primary=None)

    with pytest.raises(ValueError, match="not found"):
        stock_mod.stock(kis, symbol="X", market=None, account=None)


def test_kisstockscope_init_registers_filter_direct_instantiation(monkeypatch):
    # Directly test KisStockScope __init__ calls KisProductEventFilter.__init__
    recorded = {}

    class FakeFilter:
        def __init__(self, owner):
            # record that filter init received owner and set attribute
            recorded["owner"] = owner
            owner._was_filtered = True

    monkeypatch.setattr(stock_mod, "KisProductEventFilter", FakeFilter)

    kis = DummyKis()
    acc = object()
    scope = stock_mod.KisStockScope(kis=kis, market="MKT", symbol="S", account=acc)

    assert scope.kis is kis
    assert scope.market == "MKT"
    assert scope.symbol == "S"
    assert scope.account_number is acc
    assert recorded["owner"] is scope
    assert getattr(scope, "_was_filtered", False) is True
