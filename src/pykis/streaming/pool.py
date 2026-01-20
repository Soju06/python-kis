from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Literal, Protocol

from pykis.streaming.session import StreamingSession
from pykis.streaming.subscriptions import SubscriptionRegistry


@dataclass(frozen=True, slots=True)
class SessionKey:
    app_key: str
    domain: Literal["demo", "real"]


class SessionFactory(Protocol):
    def create(self, *, app_key: str, domain: Literal["demo", "real"]) -> StreamingSession: ...


@dataclass(slots=True)
class SessionEntry:
    session: StreamingSession
    registry: SubscriptionRegistry
    ref_count: int


@dataclass(slots=True)
class SessionPool:
    _sessions: dict[SessionKey, SessionEntry]
    _lock: asyncio.Lock

    def __init__(self) -> None:
        self._sessions = {}
        self._lock = asyncio.Lock()

    async def acquire(self, *, key: SessionKey, factory: SessionFactory) -> SessionEntry:
        async with self._lock:
            entry = self._sessions.get(key)
            if entry is not None:
                entry.ref_count += 1
                return entry
            session = factory.create(app_key=key.app_key, domain=key.domain)
            registry = SubscriptionRegistry()
            entry = SessionEntry(session=session, registry=registry, ref_count=1)
            self._sessions[key] = entry
        await entry.session.connect()
        return entry

    async def release(self, *, key: SessionKey) -> None:
        entry: SessionEntry | None = None
        async with self._lock:
            entry = self._sessions.get(key)
            if entry is None:
                return
            entry.ref_count -= 1
            if entry.ref_count <= 0:
                self._sessions.pop(key, None)
        if entry is not None and entry.ref_count <= 0:
            await entry.session.close()

    def snapshot(self) -> tuple[SessionKey, ...]:
        return tuple(self._sessions.keys())
