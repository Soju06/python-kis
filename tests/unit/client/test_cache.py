from datetime import datetime, timedelta

from vmkis.client.cache import KisCacheStorage


def test_set_get_without_expire_and_type_check():
    store = KisCacheStorage()
    store.set("k1", 123)

    # correct type -> returns value
    assert store.get("k1", int) == 123

    # wrong type -> returns default but does not remove stored data
    default = -1
    got = store.get("k1", str, default)
    assert got == default

    # subsequent correct-type get still returns stored value
    assert store.get("k1", int) == 123


def test_set_with_datetime_expired_immediately():
    store = KisCacheStorage()
    past = datetime.now() - timedelta(seconds=1)
    store.set("k_exp", "v", expire=past)

    # expired on set -> get should return default and remove data
    assert store.get("k_exp", str, None) is None

    # repeated get still returns default (data was removed)
    assert store.get("k_exp", str, "def") == "def"


def test_set_with_timedelta_not_expired_until_time_passes(monkeypatch):
    store = KisCacheStorage()

    # create a controllable datetime.now replacement
    class DummyDateTime:
        _now = datetime.now()

        @classmethod
        def now(cls):
            return cls._now

    # patch the module-level datetime used in vmkis.client.cache
    monkeypatch.setattr("vmkis.client.cache.datetime", DummyDateTime)

    # expire after 1 second from current fake now
    store.set("t", "val", expire=timedelta(seconds=1))
    assert store.get("t", str) == "val"

    # advance fake time past expiration
    DummyDateTime._now = DummyDateTime._now + timedelta(seconds=2)
    assert store.get("t", str, "x") == "x"


def test_set_with_float_seconds_expire(monkeypatch):
    store = KisCacheStorage()

    class DummyDateTime:
        _now = datetime.now()

        @classmethod
        def now(cls):
            return cls._now

    monkeypatch.setattr("vmkis.client.cache.datetime", DummyDateTime)

    # expire in 0.05 seconds from fake now
    store.set("f", 3.14, expire=0.05)
    assert store.get("f", float) == 3.14

    # advance time beyond expire
    DummyDateTime._now = DummyDateTime._now + timedelta(seconds=1)
    assert store.get("f", float, "no") == "no"


def test_remove_and_clear_behavior():
    store = KisCacheStorage()
    store.set("a", 1)
    store.set("b", 2, expire=timedelta(seconds=60))

    assert store.get("a", int) == 1
    assert store.get("b", int) == 2

    store.remove("a")
    assert store.get("a", int, None) is None
    # b still there
    assert store.get("b", int) == 2

    store.clear()
    assert store.get("b", int, None) is None


def test_get_returns_default_when_missing_key_or_wrong_type():
    store = KisCacheStorage()
    # missing key
    assert store.get("no", int, 99) == 99

    # store a dict but request int -> default
    store.set("x", {"a": 1})
    assert store.get("x", int, 0) == 0
