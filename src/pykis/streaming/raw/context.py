from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Protocol
from zoneinfo import ZoneInfo


class TimeProvider(Protocol):
    def now_utc(self) -> datetime: ...


@dataclass(slots=True)
class SystemTimeProvider:
    def now_utc(self) -> datetime:
        return datetime.now(timezone.utc)


@dataclass(slots=True)
class StreamingParseContext:
    market_timezone: str
    business_date: date | None
    time_provider: TimeProvider
    zdiv: int | None
    last_inferred_date: date | None
    time_backwards: bool

    def __init__(
        self,
        market_timezone: str,
        *,
        business_date: date | None = None,
        time_provider: TimeProvider | None = None,
        zdiv: int | None = None,
        last_inferred_date: date | None = None,
    ) -> None:
        self.market_timezone = market_timezone
        self.business_date = business_date
        self.time_provider = time_provider or SystemTimeProvider()
        self.zdiv = zdiv
        self.last_inferred_date = last_inferred_date
        self.time_backwards = False

    def resolve_business_date(self) -> date:
        if self.business_date is not None:
            return self.business_date
        now_local = self.time_provider.now_utc().astimezone(ZoneInfo(self.market_timezone))
        inferred = now_local.date()
        if self.last_inferred_date is not None and inferred < self.last_inferred_date:
            self.time_backwards = True
            return self.last_inferred_date
        self.last_inferred_date = inferred
        return inferred
