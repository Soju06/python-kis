from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Callable, Literal, Protocol

from pykis.streaming._sync.queue import DropPolicy, SyncStreamQueue
from pykis.streaming._sync.router import EventTransformer, SyncStreamingEventRouter
from pykis.streaming._sync.session import SyncStreamingSession
from pykis.streaming._sync.subscriptions import SyncSubscriptionKey, SyncSubscriptionRegistry


@dataclass(frozen=True, slots=True)
class SyncSessionKey:
    app_key: str
    domain: Literal["demo", "real"]


class SessionFactory(Protocol):
    def create(self, *, app_key: str, domain: Literal["demo", "real"]) -> SyncStreamingSession: ...


@dataclass(slots=True)
class SyncSessionEntry:
    session: SyncStreamingSession
    registry: SyncSubscriptionRegistry
    router: SyncStreamingEventRouter
    ref_count: int
    approval_key: str | None
    custtype: str
    content_type: str

    def __init__(
        self,
        *,
        session: SyncStreamingSession,
        registry: SyncSubscriptionRegistry,
        router: SyncStreamingEventRouter,
        ref_count: int,
    ) -> None:
        self.session = session
        self.registry = registry
        self.router = router
        self.ref_count = ref_count
        self.approval_key = None
        self.custtype = "P"
        self.content_type = "utf-8"

    def subscribe_stream(
        self,
        *,
        approval_key: str,
        tr_id: str,
        tr_key: str,
        custtype: str = "P",
        content_type: str = "utf-8",
        maxsize: int = 1000,
        policy: DropPolicy = DropPolicy.DROP_OLDEST,
    ) -> "SyncSubscriptionStream":
        self._set_subscription_context(approval_key, custtype, content_type)
        key = SyncSubscriptionKey(tr_id=tr_id, tr_key=tr_key)
        queue = SyncStreamQueue[object](maxsize=maxsize, policy=policy)
        self.router.register(key, queue)
        added = self.registry.add(key)
        if added:
            try:
                self.session.subscribe(
                    approval_key=approval_key,
                    tr_id=tr_id,
                    tr_key=tr_key,
                    custtype=custtype,
                    tr_type="1",
                    content_type=content_type,
                )
            except Exception:
                self.router.unregister(key, queue)
                self.registry.remove(key)
                raise
        return SyncSubscriptionStream(
            tr_id=tr_id,
            tr_key=tr_key,
            queue=queue,
            close_callback=self._build_close_callback(key, queue),
        )

    def resubscribe_all(self) -> None:
        if self.approval_key is None:
            return
        items = sorted(self.registry.snapshot(), key=lambda item: (item.tr_id, item.tr_key))
        for item in items:
            self.session.subscribe(
                approval_key=self.approval_key,
                tr_id=item.tr_id,
                tr_key=item.tr_key,
                custtype=self.custtype,
                tr_type="1",
                content_type=self.content_type,
            )

    def _set_subscription_context(self, approval_key: str, custtype: str, content_type: str) -> None:
        if self.approval_key is None:
            self.approval_key = approval_key
            self.custtype = custtype
            self.content_type = content_type
            return
        if self.approval_key != approval_key:
            raise ValueError("approval_key mismatch for session")
        if self.custtype != custtype:
            raise ValueError("custtype mismatch for session")
        if self.content_type != content_type:
            raise ValueError("content_type mismatch for session")

    def _build_close_callback(
        self,
        key: SyncSubscriptionKey,
        queue: SyncStreamQueue[object],
    ) -> Callable[[], None]:
        def _close() -> None:
            last = self.router.unregister(key, queue)
            if last and self.approval_key is not None:
                self.session.unsubscribe(
                    approval_key=self.approval_key,
                    tr_id=key.tr_id,
                    tr_key=key.tr_key,
                    custtype=self.custtype,
                    content_type=self.content_type,
                )
                self.registry.remove(key)

        return _close


@dataclass(slots=True)
class SyncSessionPool:
    _sessions: dict[SyncSessionKey, SyncSessionEntry]
    _lock: threading.Lock

    def __init__(self) -> None:
        self._sessions = {}
        self._lock = threading.Lock()

    def acquire(
        self,
        *,
        key: SyncSessionKey,
        factory: SessionFactory,
        transformer: EventTransformer | None = None,
    ) -> SyncSessionEntry:
        with self._lock:
            entry = self._sessions.get(key)
            if entry is not None:
                entry.ref_count += 1
                return entry
            session = factory.create(app_key=key.app_key, domain=key.domain)
            registry = SyncSubscriptionRegistry()
            router = SyncStreamingEventRouter(frame_handler=session.frame_handler, transformer=transformer)
            session.router = router
            entry = SyncSessionEntry(session=session, registry=registry, router=router, ref_count=1)
            session.on_reconnect = entry.resubscribe_all
            self._sessions[key] = entry
        entry.session.connect()
        return entry

    def release(self, *, key: SyncSessionKey) -> None:
        entry: SyncSessionEntry | None = None
        with self._lock:
            entry = self._sessions.get(key)
            if entry is None:
                return
            entry.ref_count -= 1
            if entry.ref_count <= 0:
                self._sessions.pop(key, None)
        if entry is not None and entry.ref_count <= 0:
            entry.session.close()

    def snapshot(self) -> tuple[SyncSessionKey, ...]:
        return tuple(self._sessions.keys())


@dataclass(slots=True)
class SyncSubscriptionStream:
    tr_id: str
    tr_key: str
    queue: SyncStreamQueue[object]
    close_callback: Callable[[], None]

    def __iter__(self) -> "SyncSubscriptionStream":
        return self

    def __next__(self) -> object:
        return self.queue.get()

    def close(self) -> None:
        self.close_callback()
