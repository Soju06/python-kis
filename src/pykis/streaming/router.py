from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from pykis.streaming.raw.adapter import StreamingFrameHandler
from pykis.streaming.raw.parser import split_streaming_frame

EventHandler = Callable[[object], None]


@dataclass(slots=True)
class StreamingEventRouter:
    frame_handler: StreamingFrameHandler
    _handlers: dict[str, list[EventHandler]] = field(default_factory=dict)

    def register(self, tr_id: str, handler: EventHandler) -> None:
        handlers = self._handlers.setdefault(tr_id, [])
        if handler not in handlers:
            handlers.append(handler)

    def unregister(self, tr_id: str, handler: EventHandler) -> None:
        handlers = self._handlers.get(tr_id)
        if not handlers:
            return
        if handler in handlers:
            handlers.remove(handler)
        if not handlers:
            self._handlers.pop(tr_id, None)

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
            self.dispatch(tr_id, record)

    def dispatch(self, tr_id: str, record: object) -> None:
        handlers = self._handlers.get(tr_id)
        if not handlers:
            return
        for handler in handlers:
            handler(record)
