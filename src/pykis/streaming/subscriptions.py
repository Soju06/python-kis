from __future__ import annotations

from dataclasses import dataclass

from pykis.streaming.constants import MAX_SUBSCRIPTIONS_PER_SESSION
from pykis.streaming.errors import StreamingLimitError


@dataclass(frozen=True, slots=True)
class SubscriptionKey:
    tr_id: str
    tr_key: str


@dataclass(slots=True)
class SubscriptionRegistry:
    limit: int
    _keys: set[SubscriptionKey]

    def __init__(self, *, limit: int = MAX_SUBSCRIPTIONS_PER_SESSION) -> None:
        if limit < 1:
            raise ValueError("limit must be >= 1")
        self.limit = limit
        self._keys = set()

    def add(self, key: SubscriptionKey) -> None:
        if key in self._keys:
            return
        if len(self._keys) >= self.limit:
            raise StreamingLimitError(f"subscription limit exceeded (limit={self.limit})")
        self._keys.add(key)

    def remove(self, key: SubscriptionKey) -> None:
        self._keys.discard(key)

    def __len__(self) -> int:
        return len(self._keys)

    def snapshot(self) -> tuple[SubscriptionKey, ...]:
        return tuple(self._keys)
