from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from pykis.store.raw.spec import RecordSpec


@dataclass(frozen=True, slots=True)
class RawSource:
    """Description of a raw master source.

    The raw layer does not fetch from network. It only describes local sources.
    """

    source_id: str
    kind: str
    path: Path
    spec: RecordSpec
    version: str | None = None


@dataclass(frozen=True, slots=True)
class RawRecord:
    """One parsed raw record (fixed-width fields, still untyped)."""

    source_id: str
    line_no: int
    fields: Mapping[str, str]
