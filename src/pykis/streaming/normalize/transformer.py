from __future__ import annotations

from dataclasses import dataclass

from pykis.streaming.normalize.mapper import normalize_event
from pykis.streaming.normalize.models import NormalizedEvent
from pykis.streaming.raw.base import StreamingRawModel


@dataclass(slots=True)
class NormalizeEventTransformer:
    def __call__(self, tr_id: str, record: object) -> NormalizedEvent | None:
        if isinstance(record, StreamingRawModel):
            return normalize_event(tr_id, record)
        return None
