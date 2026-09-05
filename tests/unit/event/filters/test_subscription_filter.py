from types import SimpleNamespace

from vmkis.event.filters.subscription import KisSubscriptionEventFilter
from vmkis.event.subscription import KisSubscriptionEventArgs


def test_filter_matches_with_key():
    f = KisSubscriptionEventFilter("TR1", "K1")
    tr = SimpleNamespace(id="TR1", key="K1")
    args = KisSubscriptionEventArgs(tr=tr, response=SimpleNamespace())

    # matching id and key -> do not ignore (filter returns False)
    assert f.__filter__(None, None, args) is False


def test_filter_matches_without_key():
    f = KisSubscriptionEventFilter("TR2")
    tr = SimpleNamespace(id="TR2", key="ANY")
    args = KisSubscriptionEventArgs(tr=tr, response=SimpleNamespace())

    # key is None on filter -> any tr.key should match -> filter returns False
    assert f.__filter__(None, None, args) is False


def test_filter_non_matching_cases():
    f = KisSubscriptionEventFilter("TR3", "K3")

    # id mismatch
    tr1 = SimpleNamespace(id="OTHER", key="K3")
    args1 = KisSubscriptionEventArgs(tr=tr1, response=SimpleNamespace())
    assert f.__filter__(None, None, args1) is True

    # key mismatch
    tr2 = SimpleNamespace(id="TR3", key="DIFF")
    args2 = KisSubscriptionEventArgs(tr=tr2, response=SimpleNamespace())
    assert f.__filter__(None, None, args2) is True


def test_hash_and_repr_and_str():
    f = KisSubscriptionEventFilter("TRX", "KX")
    h = hash(f)
    assert isinstance(h, int)

    r = repr(f)
    assert "KisSubscriptionEventFilter" in r
    assert "TRX" in r and "KX" in r

    assert str(f) == r
