from __future__ import annotations

import asyncio
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Callable, Literal


@dataclass(frozen=True, slots=True)
class RateLimits:
    per_second: float | None
    per_minute: float | None


def default_rate_limits(domain: Literal["demo", "real"]) -> RateLimits:
    if domain == "real":
        return RateLimits(per_second=20.0, per_minute=None)
    return RateLimits(per_second=2.0, per_minute=None)


def resolve_rate_limits(
    *,
    domain: Literal["demo", "real"],
    rate_limit: float | None,
    per_second: float | None,
    per_minute: float | None,
) -> RateLimits:
    if per_second is None and per_minute is None:
        if rate_limit is None:
            return default_rate_limits(domain)
        if rate_limit <= 0:
            return RateLimits(per_second=None, per_minute=per_minute)
        return RateLimits(per_second=1.0 / rate_limit, per_minute=per_minute)
    return RateLimits(per_second=per_second, per_minute=per_minute)


def retry_backoff_hint(per_second: float | None) -> float:
    if per_second is None or per_second <= 0:
        return 0.0
    return 1.0 / per_second


def parse_retry_after(value: str | None) -> float | None:
    if not value:
        return None
    text = value.strip()
    if text.isdigit():
        return float(text)
    try:
        parsed = parsedate_to_datetime(text)
    except Exception:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    delta = (parsed - datetime.now(timezone.utc)).total_seconds()
    return max(delta, 0.0)


@dataclass(slots=True)
class TokenBucket:
    rate_per_sec: float
    capacity: float
    tokens: float
    updated_at: float

    def __init__(self, *, rate_per_sec: float, capacity: float, now: float) -> None:
        if rate_per_sec <= 0:
            raise ValueError("rate_per_sec must be > 0")
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self.rate_per_sec = rate_per_sec
        self.capacity = capacity
        self.tokens = capacity
        self.updated_at = now

    def required_wait(self, now: float, amount: float = 1.0) -> float:
        self._refill(now)
        if self.tokens >= amount:
            return 0.0
        missing = amount - self.tokens
        return missing / self.rate_per_sec

    def consume(self, now: float, amount: float = 1.0) -> None:
        self._refill(now)
        if self.tokens < amount:
            raise RuntimeError("insufficient tokens")
        self.tokens -= amount

    def _refill(self, now: float) -> None:
        elapsed = now - self.updated_at
        if elapsed <= 0:
            return
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate_per_sec)
        self.updated_at = now


@dataclass(slots=True)
class AsyncRateLimiter:
    per_second: float | None
    per_minute: float | None
    min_backoff: float
    _buckets: tuple[TokenBucket, ...]
    _lock: asyncio.Lock
    _cooldown_until: float
    _clock: Callable[[], float]

    def __init__(
        self,
        *,
        per_second: float | None,
        per_minute: float | None,
        min_backoff: float = 0.5,
        clock: Callable[[], float] | None = None,
    ) -> None:
        self.per_second = per_second
        self.per_minute = per_minute
        self.min_backoff = min_backoff
        self._clock = clock or time.monotonic
        now = self._clock()
        buckets: list[TokenBucket] = []
        if per_second is not None and per_second > 0:
            buckets.append(TokenBucket(rate_per_sec=per_second, capacity=per_second, now=now))
        if per_minute is not None and per_minute > 0:
            buckets.append(TokenBucket(rate_per_sec=per_minute / 60.0, capacity=per_minute, now=now))
        self._buckets = tuple(buckets)
        self._lock = asyncio.Lock()
        self._cooldown_until = 0.0

    async def acquire(self) -> None:
        async with self._lock:
            while True:
                now = self._clock()
                wait = max(self._cooldown_until - now, 0.0)
                for bucket in self._buckets:
                    wait = max(wait, bucket.required_wait(now))
                if wait <= 0:
                    for bucket in self._buckets:
                        bucket.consume(now)
                    return
                await asyncio.sleep(wait)

    def on_rate_limited(self, retry_after: float | None) -> float:
        wait = retry_after if retry_after and retry_after > 0 else self.min_backoff
        now = self._clock()
        self._cooldown_until = max(self._cooldown_until, now + wait)
        return wait


@dataclass(slots=True)
class SyncRateLimiter:
    per_second: float | None
    per_minute: float | None
    min_backoff: float
    _buckets: tuple[TokenBucket, ...]
    _lock: threading.Lock
    _cooldown_until: float
    _clock: Callable[[], float]

    def __init__(
        self,
        *,
        per_second: float | None,
        per_minute: float | None,
        min_backoff: float = 0.5,
        clock: Callable[[], float] | None = None,
    ) -> None:
        self.per_second = per_second
        self.per_minute = per_minute
        self.min_backoff = min_backoff
        self._clock = clock or time.monotonic
        now = self._clock()
        buckets: list[TokenBucket] = []
        if per_second is not None and per_second > 0:
            buckets.append(TokenBucket(rate_per_sec=per_second, capacity=per_second, now=now))
        if per_minute is not None and per_minute > 0:
            buckets.append(TokenBucket(rate_per_sec=per_minute / 60.0, capacity=per_minute, now=now))
        self._buckets = tuple(buckets)
        self._lock = threading.Lock()
        self._cooldown_until = 0.0

    def acquire(self) -> None:
        with self._lock:
            while True:
                now = self._clock()
                wait = max(self._cooldown_until - now, 0.0)
                for bucket in self._buckets:
                    wait = max(wait, bucket.required_wait(now))
                if wait <= 0:
                    for bucket in self._buckets:
                        bucket.consume(now)
                    return
                time.sleep(wait)

    def on_rate_limited(self, retry_after: float | None) -> float:
        wait = retry_after if retry_after and retry_after > 0 else self.min_backoff
        now = self._clock()
        self._cooldown_until = max(self._cooldown_until, now + wait)
        return wait
