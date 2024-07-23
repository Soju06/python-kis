from multiprocessing import Lock
from multiprocessing.synchronize import Lock as LockType
from typing import Callable


class ReferenceStore:
    __slots__ = [
        "_store",
        "_lock",
        "_callback",
    ]

    _store: dict[str, int]
    _lock: LockType
    _callback: Callable[[str, int], None] | None

    def __init__(self, callback: Callable[[str, int], None] | None = None):
        self._store = {}
        self._lock = Lock()
        self._callback = callback

    def get(self, key: str) -> int:
        with self._lock:
            return self._store.get(key, 0)

    def increment(self, key: str) -> int:
        with self._lock:
            value = self._store[key] = self._store.get(key, 0) + 1
            return value

    def decrement(self, key: str) -> int:
        with self._lock:
            value = self._store[key] = max(0, self._store.get(key, 0) - 1)

            if self._callback is not None:
                self._callback(key, value)

            return value

    def reset(self, key: str | None = None) -> None:
        with self._lock:
            if key is None:
                self._store.clear()
            else:
                self._store[key] = 0

    def ticket(self, key: str) -> "ReferenceTicket":
        return ReferenceTicket(self, key)


class ReferenceTicket:
    __slots__ = [
        "_store",
        "_key",
        "_released",
    ]

    _store: ReferenceStore
    _key: str
    _released: bool

    def __init__(self, store: ReferenceStore, key: str):
        self._store = store
        self._key = key
        self._released = False
        self._store.increment(key)

    def release(self):
        if not self._released:
            self._store.decrement(self._key)
            self._released = True

    def __del__(self):
        self.release()

    def __enter__(self) -> "ReferenceTicket":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.release()


def package_mathod(func: Callable, ticket: ReferenceTicket):
    def _(*args, **kwargs):
        return func(*args, **kwargs)

    _.__doc__ = func.__doc__
    _.__module__ = func.__module__
    _.__name__ = func.__name__
    _.__is_kis_reference_method__ = True
    _.__reference_ticket__ = ticket

    return _


def release_method(func: Callable):
    if not hasattr(func, "__is_kis_reference_method__") or not hasattr(func, "__reference_ticket__"):
        return False

    getattr(func.__reference_ticket__, "release")()

    return True
