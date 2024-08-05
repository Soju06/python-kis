import time
from multiprocessing import Lock
from multiprocessing.synchronize import Lock as LockType
from typing import Callable

__all__ = [
    "RateLimiter",
]


class RateLimiter:
    """호출 유량을 제한하는 클래스입니다."""

    __slots__ = [
        "rate",
        "period",
        "_count",
        "_last",
        "_lock",
    ]

    rate: int
    """기간 호출 횟수"""
    period: float
    """기간"""

    _count: int
    """호출 횟수"""
    _last: float
    """마지막 호출 시간"""
    _lock: LockType
    """Lock 객체"""

    def __init__(self, rate: int, period: float):
        """호출 유량을 제한하는 클래스를 생성합니다.

        Args:
            rate: 초당 호출 횟수
            period: 기간(초)
        """
        self.rate = rate
        self.period = period
        self._count = 0
        self._last = 0
        self._lock = Lock()

    @property
    def count(self) -> int:
        """기간 호출 횟수를 반환합니다."""
        with self._lock:
            return 0 if time.time() - self._last > self.period else self._count

    def acquire(self, blocking: bool = True, blocking_callback: Callable[[], None] | None = None) -> bool:
        """
        호출 유량을 획득합니다.

        Args:
            blocking: 호출 횟수가 초과되었을 때 대기 여부
            blocking_callback: blocking=True일 경우 호출 횟수 초과 시 호출할 함수

        Returns:
            호출 횟수 초과 여부, blocking=True일 경우 항상 True
        """
        with self._lock:
            now = time.time()
            if now - self._last > self.period:
                self._count = 0
                self._last = now
            if self._count >= self.rate:
                if not blocking:
                    return False

                if blocking_callback is not None:
                    blocking_callback()

                time.sleep(max(self.period - (time.time() - self._last) + 0.05, 0))
                self._count = 0
                self._last = time.time()

            self._count += 1
            return True
