from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True, slots=True)
class OverrideCandidate:
    endpoint_uuid: str
    tr_id: str
    field: str
    raw_value: str
    rule: str
    decision: str
    confidence: float
    reason: str
    market: str
    timezone: str
    sample_payload: str | None
    timestamp_utc: datetime
    notes: str | None = None

    def as_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["timestamp_utc"] = self.timestamp_utc.isoformat()
        return payload


class OverrideLogger(Protocol):
    def record(self, candidate: OverrideCandidate) -> None: ...


@dataclass(slots=True)
class NullOverrideLogger:
    def record(self, candidate: OverrideCandidate) -> None:
        return None


@dataclass(slots=True)
class JsonlOverrideLogger:
    path: Path

    def record(self, candidate: OverrideCandidate) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = candidate.as_dict()
        line = json.dumps(payload, ensure_ascii=True, separators=(",", ":"))
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
