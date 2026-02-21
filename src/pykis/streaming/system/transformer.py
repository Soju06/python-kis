from __future__ import annotations

from dataclasses import dataclass

from pykis.streaming.normalize.transformer import NormalizeEventTransformer
from pykis.streaming.system.mapper import build_system_event
from pykis.streaming.system.models import SystemEvent


@dataclass(slots=True)
class SystemEventTransformer:
    normalizer: NormalizeEventTransformer

    def __init__(self, normalizer: NormalizeEventTransformer | None = None) -> None:
        self.normalizer = normalizer or NormalizeEventTransformer()

    def __call__(self, tr_id: str, record: object) -> SystemEvent | None:
        normalized = self.normalizer(tr_id, record)
        if normalized is None:
            return None
        return build_system_event(normalized)
