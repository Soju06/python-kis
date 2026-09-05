from types import SimpleNamespace

import pytest

import vmkis.event.filters.product as product_mod
from vmkis.event.filters.product import KisProductEventFilter, KisSimpleProduct
from vmkis.event.subscription import KisSubscriptionEventArgs


def test_init_requires_market():
    with pytest.raises(ValueError):
        KisProductEventFilter("AAA")


def test_filter_ignores_non_product_response():
    f = KisProductEventFilter("AAA", "MKT")
    # response without symbol/market attributes
    resp = SimpleNamespace()
    args = KisSubscriptionEventArgs(tr=None, response=resp)
    assert f.__filter__(None, None, args) is True


def test_filter_matches_and_nonmatches(monkeypatch):
    # prepare filter using simple product
    f = KisProductEventFilter("SYM", "MKT")

    class Resp:
        def __init__(self, symbol, market):
            self.symbol = symbol
            self.market = market

    # monkeypatch protocol name in module to Resp so isinstance check passes for Resp
    monkeypatch.setattr(product_mod, "KisSimpleProductProtocol", Resp)

    # matching response -> filter returns False (do not ignore)
    args_ok = KisSubscriptionEventArgs(tr=None, response=Resp("SYM", "MKT"))
    assert f.__filter__(None, None, args_ok) is False

    # different symbol -> ignored
    args_diff = KisSubscriptionEventArgs(tr=None, response=Resp("DIFF", "MKT"))
    assert f.__filter__(None, None, args_diff) is True

    # different market -> ignored
    args_diff2 = KisSubscriptionEventArgs(tr=None, response=Resp("SYM", "OTHER"))
    assert f.__filter__(None, None, args_diff2) is True


def test_init_with_product_object_and_repr_hash():
    prod = KisSimpleProduct("AAA", "MKT")
    f = KisProductEventFilter(prod)

    # hashable
    assert isinstance(hash(f), int)

    r = repr(f)
    assert "KisProductEventFilter" in r or "symbol=" in r
    assert str(f) == r
