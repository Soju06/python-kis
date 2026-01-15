from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class IndexRow:
    symbol: str | None
    standard_code: str | None
    isin: str | None
    source_id: str
    line_no: int
    table_name: str
