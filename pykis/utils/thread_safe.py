from functools import wraps
from multiprocessing import Lock
from typing import Any, Callable

global_lock = Lock()

__all__ = [
    "thread_safe",
]


def thread_safe(name: str | None = None):
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            with global_lock:
                key = f"__thread_safe_{name or fn.__name__}_lock"

                if not (lock := getattr(self, key, None)):
                    lock = Lock()
                    setattr(self, key, lock)

            with lock:
                return fn(self, *args, **kwargs)

        return wrapper

    return decorator


def get_lock(self, name: str):
    key = f"__thread_safe_{name}_lock"

    if not (lock := getattr(self, key, None)):
        lock = Lock()
        setattr(self, key, lock)

    return lock
