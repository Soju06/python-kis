from datetime import datetime, timedelta
from multiprocessing import Lock
from multiprocessing.synchronize import Lock as LockType
from typing import Any, TypeVar

__all__ = [
    "TObject",
    "KisCacheStorage",
]

TObject = TypeVar("TObject")


class KisCacheStorage:
    """캐시 저장소"""

    __slots__ = [
        "_data",
        "_expire",
        "_lock",
    ]

    _data: dict[str, Any]
    """캐시 데이터"""
    _expire: dict[str, datetime]
    """캐시 만료 시간"""
    _lock: LockType
    """Lock 객체"""

    def __init__(self):
        self._data = {}
        self._expire = {}
        self._lock = Lock()

    def set(self, key: str, value: Any, expire: datetime | timedelta | float | None = None):
        """캐시에 데이터를 저장합니다."""
        with self._lock:
            self._data[key] = value

            if expire is not None:
                if isinstance(expire, timedelta):
                    expire = datetime.now() + expire
                elif isinstance(expire, (float, int)):
                    expire = datetime.now() + timedelta(seconds=expire)
                elif isinstance(expire, datetime):
                    expire = expire

                self._expire[key] = expire

    def get(self, key: str, type: type[TObject], default: TObject | None = None) -> TObject | None:
        """캐시에서 데이터를 조회합니다."""
        with self._lock:
            if (data := self._data.get(key)) is None:
                return default

            if (expire := self._expire.get(key)) is not None and expire < datetime.now():
                del self._data[key]
                return default

            if not isinstance(data, type):
                return default

            return data

    def remove(self, key: str):
        """캐시에서 데이터를 삭제합니다."""
        with self._lock:
            if key in self._data:
                del self._data[key]

            if key in self._expire:
                del self._expire[key]

    def clear(self):
        """캐시를 초기화합니다."""
        with self._lock:
            self._data.clear()
            self._expire.clear()
