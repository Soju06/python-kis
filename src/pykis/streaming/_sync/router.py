from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Protocol

from pykis.streaming._sync.queue import SyncStreamQueue
from pykis.streaming._sync.subscriptions import SyncSubscriptionKey
from pykis.streaming.raw.adapter import StreamingFrameHandler
from pykis.streaming.raw.parser import split_streaming_frame


class EventTransformer(Protocol):
    def __call__(self, tr_id: str, record: object) -> object | None: ...


class RecordKeyResolver(Protocol):
    def __call__(self, tr_id: str, record: object) -> str | None: ...


def default_record_key(tr_id: str, record: object) -> str | None:
    for attr in ("MKSC_SHRN_ISCD", "STCK_SHRN_ISCD", "RSYM", "TR_KEY", "SYMB"):
        value = getattr(record, attr, None)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


@dataclass(slots=True)
class SyncStreamingEventRouter:
    frame_handler: StreamingFrameHandler
    transformer: EventTransformer | None
    key_resolver: RecordKeyResolver
    _queues: dict[SyncSubscriptionKey, list[SyncStreamQueue[object]]] = field(default_factory=dict)

    def __init__(
        self,
        *,
        frame_handler: StreamingFrameHandler,
        transformer: EventTransformer | None = None,
        key_resolver: RecordKeyResolver | None = None,
    ) -> None:
        self.frame_handler = frame_handler
        self.transformer = transformer
        self.key_resolver = key_resolver or default_record_key
        self._queues = {}

    def register(self, key: SyncSubscriptionKey, queue: SyncStreamQueue[object]) -> None:
        queues = self._queues.setdefault(key, [])
        if queue not in queues:
            queues.append(queue)

    def unregister(self, key: SyncSubscriptionKey, queue: SyncStreamQueue[object]) -> bool:
        queues = self._queues.get(key)
        if not queues:
            return False
        if queue in queues:
            queues.remove(queue)
        if not queues:
            self._queues.pop(key, None)
            return True
        return False

    def handle_frame(self, frame: str) -> None:
        frame = frame.strip()
        if not frame:
            return
        if frame.startswith("{") or frame.startswith("["):
            return
        _, tr_id, _, _ = split_streaming_frame(frame)
        records = self.frame_handler.handle_frame(frame)
        if records is None:
            return
        for record in records:
            tr_key = self.key_resolver(tr_id, record)
            self.dispatch(tr_id, tr_key, record)

    def dispatch(self, tr_id: str, tr_key: str | None, record: object) -> None:
        payload = self._transform(tr_id, record)
        if payload is None:
            return
        if tr_key:
            self._emit(SyncSubscriptionKey(tr_id=tr_id, tr_key=tr_key), payload)
        self._emit(SyncSubscriptionKey(tr_id=tr_id, tr_key="*"), payload)

    def _transform(self, tr_id: str, record: object) -> object | None:
        if self.transformer is None:
            return record
        return self.transformer(tr_id, record)

    def _emit(self, key: SyncSubscriptionKey, payload: object) -> None:
        queues = self._queues.get(key)
        if not queues:
            return
        for queue in queues:
            queue.put(payload)
