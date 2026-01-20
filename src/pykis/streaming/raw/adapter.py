from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Callable, Mapping, Protocol

from pykis.streaming.raw.context import StreamingParseContext, TimeProvider
from pykis.streaming.raw.overrides import NullOverrideLogger, OverrideLogger
from pykis.streaming.raw.parser import (
    PayloadDecryptor,
    StreamingParseError,
    parse_streaming_frame,
    split_streaming_frame,
)
from pykis.streaming.raw.specs import SpecRegistry, StreamingSpec


class ContextProvider(Protocol):
    def context_for(self, spec: StreamingSpec) -> StreamingParseContext: ...


@dataclass(slots=True)
class StaticContextProvider:
    domestic_timezone: str
    overseas_timezone: str | None
    overseas_timezones: Mapping[str, str]
    business_date: date | None
    time_provider: TimeProvider | None
    zdiv: int | None

    def __init__(
        self,
        *,
        domestic_timezone: str = "Asia/Seoul",
        overseas_timezone: str | None = None,
        overseas_timezones: Mapping[str, str] | None = None,
        business_date: date | None = None,
        time_provider: TimeProvider | None = None,
        zdiv: int | None = None,
    ) -> None:
        self.domestic_timezone = domestic_timezone
        self.overseas_timezone = overseas_timezone
        self.overseas_timezones = overseas_timezones or {}
        self.business_date = business_date
        self.time_provider = time_provider
        self.zdiv = zdiv

    def context_for(self, spec: StreamingSpec) -> StreamingParseContext:
        if spec.market == "domestic":
            tz = self.domestic_timezone
        else:
            tz = self.overseas_timezones.get(spec.tr_id) or self.overseas_timezone
            if tz is None:
                raise StreamingParseError("Missing overseas timezone", tr_id=spec.tr_id)
        return StreamingParseContext(
            tz,
            business_date=self.business_date,
            time_provider=self.time_provider,
            zdiv=self.zdiv,
        )


@dataclass(slots=True)
class StreamingFrameHandler:
    registry: SpecRegistry
    context_provider: ContextProvider
    override_logger: OverrideLogger
    decryptor: PayloadDecryptor | None
    on_event: Callable[[str, object], None] | None

    def __init__(
        self,
        *,
        registry: SpecRegistry,
        context_provider: ContextProvider,
        override_logger: OverrideLogger | None = None,
        decryptor: PayloadDecryptor | None = None,
        on_event: Callable[[str, object], None] | None = None,
    ) -> None:
        self.registry = registry
        self.context_provider = context_provider
        self.override_logger = override_logger or NullOverrideLogger()
        self.decryptor = decryptor
        self.on_event = on_event

    def handle_frame(self, frame: str) -> list[object] | None:
        frame = frame.strip()
        if not frame:
            return None
        if frame.startswith("{") or frame.startswith("["):
            return None

        _, tr_id, _, _ = split_streaming_frame(frame)
        spec = self.registry.get(tr_id)
        if spec is None:
            raise StreamingParseError("Unknown tr_id", tr_id=tr_id, payload=frame)
        context = self.context_provider.context_for(spec)
        result = parse_streaming_frame(
            frame,
            registry=self.registry,
            context=context,
            override_logger=self.override_logger,
            decryptor=self.decryptor,
        )
        if result is None:
            return None
        if self.on_event is not None:
            for record in result.records:
                self.on_event(result.tr_id, record)
        return result.records
