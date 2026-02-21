from __future__ import annotations

import queue
from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

T = TypeVar("T")


class DropPolicy(str, Enum):
    DROP_OLDEST = "drop_oldest"
    DROP_NEWEST = "drop_newest"
    LATEST_ONLY = "latest_only"


@dataclass(slots=True)
class SyncStreamQueue(Generic[T]):
    maxsize: int
    policy: DropPolicy
    _queue: queue.Queue[T]

    def __init__(
        self,
        *,
        maxsize: int = 1000,
        policy: DropPolicy = DropPolicy.DROP_OLDEST,
    ) -> None:
        if maxsize < 1:
            raise ValueError("maxsize must be >= 1")
        self.maxsize = maxsize
        self.policy = policy
        self._queue = queue.Queue(maxsize=maxsize)

    def put(self, item: T) -> None:
        if not self._queue.full():
            self._queue.put_nowait(item)
            return
        if self.policy == DropPolicy.DROP_NEWEST:
            return
        if self.policy == DropPolicy.LATEST_ONLY:
            self._drain()
            self._queue.put_nowait(item)
            return
        if self.policy == DropPolicy.DROP_OLDEST:
            self._drop_oldest()
            self._queue.put_nowait(item)
            return
        self._queue.put_nowait(item)

    def get(self) -> T:
        return self._queue.get()

    def qsize(self) -> int:
        return self._queue.qsize()

    def _drop_oldest(self) -> None:
        try:
            self._queue.get_nowait()
        except queue.Empty:
            return

    def _drain(self) -> None:
        while True:
            try:
                self._queue.get_nowait()
            except queue.Empty:
                return
