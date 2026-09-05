import gc

from vmkis.utils.reference import (
    ReferenceStore,
    package_mathod,
    release_method,
)


def test_increment_decrement_and_callback():
    calls = []

    def cb(key, value):
        calls.append((key, value))

    store = ReferenceStore(callback=cb)

    assert store.get("a") == 0

    assert store.increment("a") == 1
    assert store.get("a") == 1

    assert store.increment("a") == 2
    assert store.get("a") == 2

    # decrement calls the callback and does not go below 0
    assert store.decrement("a") == 1
    assert calls[-1] == ("a", 1)

    assert store.decrement("a") == 0
    assert calls[-1] == ("a", 0)

    # extra decrement stays at 0 and callback still invoked with 0
    assert store.decrement("a") == 0
    assert calls[-1] == ("a", 0)


def test_reset_key_and_reset_all():
    store = ReferenceStore()
    store.increment("x")
    store.increment("y")
    assert store.get("x") == 1
    assert store.get("y") == 1

    store.reset("x")
    assert store.get("x") == 0
    assert store.get("y") == 1

    store.reset()
    assert store.get("y") == 0


def test_ticket_release_contextmanager_and_del_is_idempotent():
    store = ReferenceStore()

    # ticket increments on creation
    ticket = store.ticket("t")
    assert store.get("t") == 1

    # explicit release decrements and is idempotent
    ticket.release()
    assert store.get("t") == 0
    ticket.release()
    assert store.get("t") == 0

    # context manager releases on exit
    with store.ticket("ctx"):
        assert store.get("ctx") == 1
    assert store.get("ctx") == 0

    # __del__ should release when object is garbage collected
    t2 = store.ticket("gcd")
    assert store.get("gcd") == 1
    del t2
    gc.collect()
    assert store.get("gcd") == 0


def test_package_method_and_release_method_behavior():
    store = ReferenceStore()
    ticket = store.ticket("pkg")

    def original(x, y=1):
        """orig doc"""
        return x + y

    wrapped = package_mathod(original, ticket)

    # wrapper should call original and preserve metadata
    assert wrapped(2, y=3) == 5
    assert wrapped.__doc__ == original.__doc__
    assert wrapped.__name__ == original.__name__
    assert wrapped.__module__ == original.__module__
    assert getattr(wrapped, "__is_kis_reference_method__", False) is True
    assert getattr(wrapped, "__reference_ticket__", None) is ticket

    # release_method should release the associated ticket and return True
    assert release_method(wrapped) is True
    assert store.get("pkg") == 0

    # release_method on a regular function returns False
    def not_wrapped():
        pass

    assert release_method(not_wrapped) is False
