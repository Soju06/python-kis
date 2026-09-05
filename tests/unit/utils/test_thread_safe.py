import threading
import time

import pytest

from vmkis.utils import thread_safe as ts_mod
from vmkis.utils.thread_safe import get_lock, thread_safe


def test_get_lock_sets_and_returns_same_lock():
    class C:
        pass

    inst = C()
    lock1 = get_lock(inst, "foo")
    assert hasattr(inst, "__thread_safe_foo_lock")
    lock2 = get_lock(inst, "foo")
    # same object returned on subsequent calls
    assert lock1 is lock2


def test_decorator_creates_instance_lock_and_preserves_metadata():
    class S:
        @thread_safe()
        def incr(self, x: int) -> int:
            "docstring"
            return x + 1

    s = S()
    # calling method creates the per-instance lock attribute
    assert not hasattr(s, "__thread_safe_incr_lock")
    assert s.incr(1) == 2
    assert hasattr(s, "__thread_safe_incr_lock")
    lock_obj = getattr(s, "__thread_safe_incr_lock")
    assert lock_obj is ts_mod.get_lock(s, "incr")

    # wrapper should preserve metadata from wraps
    assert s.incr.__name__ == "incr"
    assert s.incr.__doc__ == "docstring"


def test_decorator_with_custom_name_uses_that_key():
    class S:
        @thread_safe("custom")
        def foo(self):
            return "ok"

    s = S()
    assert not hasattr(s, "__thread_safe_custom_lock")
    assert s.foo() == "ok"
    assert hasattr(s, "__thread_safe_custom_lock")


def test_exception_propagates_through_wrapper():
    class S:
        @thread_safe()
        def boom(self):
            raise RuntimeError("boom")

    s = S()
    with pytest.raises(RuntimeError, match="boom"):
        s.boom()


def test_locks_are_per_instance_not_shared():
    class S:
        @thread_safe()
        def nop(self):
            return None

    a = S()
    b = S()
    a.nop()
    b.nop()
    la = getattr(a, "__thread_safe_nop_lock")
    lb = getattr(b, "__thread_safe_nop_lock")
    assert la is not lb


def test_thread_safety_ensures_no_overlapping_starts():
    """
    Start two threads that run a decorated method which appends 'start', sleeps,
    then appends 'end'. Because of the lock, each 'start' must be immediately
    followed by its 'end' (no interleaved 'start','start').
    """

    class S:
        def __init__(self):
            self.seq = []

        @thread_safe()
        def work(self, delay: float = 0.05):
            self.seq.append("start")
            # simulate work
            time.sleep(delay)
            self.seq.append("end")

    s = S()
    t1 = threading.Thread(target=lambda: s.work(0.06))
    t2 = threading.Thread(target=lambda: s.work(0.06))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # ensure each 'start' is immediately followed by 'end'
    seq = s.seq
    assert len(seq) == 4
    for i, v in enumerate(seq):
        if v == "start":
            assert i + 1 < len(seq)
            assert seq[i + 1] == "end"
