import pytest

from vmkis.client.object import (
    KisObjectBase,
    KisObjectProtocol,
    kis_object_init,
)


class DummyKis:
    pass


class SpyObject(KisObjectBase):
    def __init__(self):
        self.init_called = False
        self.post_called = False
        self.kis_value = None

    def __kis_init__(self, kis):
        # call base behaviour then record
        super().__kis_init__(kis)
        self.init_called = True
        self.kis_value = kis

    def __kis_post_init__(self):
        self.post_called = True


def test___kis_init_sets_kis_and_post_can_be_overridden():
    k = DummyKis()
    s = SpyObject()
    # before init
    assert not s.init_called
    assert not s.post_called

    s.__kis_init__(k)
    s.__kis_post_init__()

    assert s.init_called is True
    assert s.post_called is True
    assert s.kis_value is k


def test_kis_object_init_helpers_calls_both():
    k = DummyKis()
    s = SpyObject()
    kis_object_init(k, s)
    assert s.init_called
    assert s.post_called


def test__kis_spread_single_object_and_ignores_none():
    k = DummyKis()
    parent = KisObjectBase()
    parent.__kis_init__(k)

    child = SpyObject()
    # single object
    parent._kis_spread(child)
    assert child.init_called
    assert child.post_called

    # None is ignored
    child2 = SpyObject()
    parent._kis_spread(None)
    assert not child2.init_called


def test__kis_spread_iterables_and_dicts_process_nested_items():
    k = DummyKis()
    parent = KisObjectBase()
    parent.__kis_init__(k)

    a = SpyObject()
    b = SpyObject()
    SpyObject()

    parent._kis_spread(
        [a, None, (b,)],
    )
    assert a.init_called and a.post_called
    assert b.init_called and b.post_called

    # dict values
    d = SpyObject()
    e = SpyObject()
    parent._kis_spread({"one": d, "two": None, "three": [e]})
    assert d.init_called and d.post_called
    assert e.init_called and e.post_called


def test__kis_spread_raises_on_invalid_leaf_type():
    parent = KisObjectBase()
    parent.__kis_init__(DummyKis())

    # list containing non-KisObjectBase should raise
    with pytest.raises(ValueError):
        parent._kis_spread([1, 2, 3])

    # dict with invalid value
    with pytest.raises(ValueError):
        parent._kis_spread({"bad": 123})


def test_protocol_runtime_checkable():
    class ImplementsProtocol:
        @property
        def kis(self):
            return DummyKis()

    inst = ImplementsProtocol()
    # runtime_checkable Protocol should accept this instance
    assert isinstance(inst, KisObjectProtocol)
