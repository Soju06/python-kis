from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
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
    buffer_size: int = 1
    max_bytes: int | None = None
    max_backups: int | None = None
    _buffer: list[str] = field(default_factory=list, init=False)
    _buffer_bytes: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        if self.buffer_size < 1:
            raise ValueError("buffer_size must be >= 1")
        if self.max_bytes is not None and self.max_bytes < 1:
            raise ValueError("max_bytes must be >= 1")
        if self.max_backups is not None and self.max_backups < 0:
            raise ValueError("max_backups must be >= 0")

    def record(self, candidate: OverrideCandidate) -> None:
        payload = candidate.as_dict()
        line = json.dumps(payload, ensure_ascii=True, separators=(",", ":")) + "\n"
        self._buffer.append(line)
        self._buffer_bytes += len(line.encode("utf-8"))
        if len(self._buffer) >= self.buffer_size:
            self.flush()

    def flush(self) -> None:
        if not self._buffer:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.max_bytes is not None:
            self._rotate_if_needed(self._buffer_bytes, self.max_bytes)
        payload = "".join(self._buffer)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(payload)
        self._buffer.clear()
        self._buffer_bytes = 0

    def _rotate_if_needed(self, incoming_bytes: int, max_bytes: int) -> None:
        if not self.path.exists():
            return
        try:
            current_bytes = self.path.stat().st_size
        except OSError:
            return
        if current_bytes + incoming_bytes <= max_bytes:
            return
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        rotated = self.path.with_name(f"{self.path.name}.{timestamp}")
        try:
            self.path.rename(rotated)
        except OSError:
            return
        self._prune_backups()

    def _prune_backups(self) -> None:
        if self.max_backups is None:
            return
        pattern = f"{self.path.name}.*"
        backups = sorted(self.path.parent.glob(pattern))
        if len(backups) <= self.max_backups:
            return
        for old in backups[: len(backups) - self.max_backups]:
            try:
                old.unlink()
            except OSError:
                continue
