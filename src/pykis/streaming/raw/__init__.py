from importlib import import_module
from typing import cast

from pykis.streaming.raw.adapter import ContextProvider, MarketTimezoneResolver, StaticContextProvider, StreamingFrameHandler
from pykis.streaming.raw.base import StreamingRawModel
from pykis.streaming.raw.context import StreamingParseContext, SystemTimeProvider, TimeProvider
from pykis.streaming.raw.market import (
    MARKET_TIMEZONES,
    DefaultMarketTimezoneResolver,
    extract_market_code,
    resolve_timezone_from_fields,
    resolve_timezone_from_symbol,
)
from pykis.streaming.raw.overrides import JsonlOverrideLogger, NullOverrideLogger, OverrideCandidate, OverrideLogger
from pykis.streaming.raw.parser import PayloadDecryptor, StreamingParseError, StreamingParseResult, parse_streaming_frame, split_streaming_frame
from pykis.streaming.raw.specs import DateTimeRule, DecimalRule, FieldSource, FieldType, SpecRegistry, StreamingSpec


def _load_registry(module_path: str) -> SpecRegistry:
    module = import_module(module_path)
    registry = getattr(module, "REGISTRY", None)
    if registry is None:
        raise RuntimeError(f"Missing REGISTRY in {module_path}")
    return cast(SpecRegistry, registry)


try:
    RAW_REGISTRY = _load_registry("pykis.streaming.raw.structs.registry")
except ModuleNotFoundError as exc:
    if exc.name not in {"pykis.streaming.raw.structs", "pykis.streaming.raw.structs.registry"}:
        raise
    RAW_REGISTRY = _load_registry("pykis.streaming.raw.generated.registry")

__all__ = [
    "DateTimeRule",
    "DecimalRule",
    "FieldSource",
    "FieldType",
    "ContextProvider",
    "MarketTimezoneResolver",
    "DefaultMarketTimezoneResolver",
    "MARKET_TIMEZONES",
    "JsonlOverrideLogger",
    "NullOverrideLogger",
    "OverrideCandidate",
    "OverrideLogger",
    "PayloadDecryptor",
    "RAW_REGISTRY",
    "StaticContextProvider",
    "StreamingFrameHandler",
    "StreamingParseContext",
    "StreamingParseError",
    "StreamingParseResult",
    "StreamingRawModel",
    "StreamingSpec",
    "SystemTimeProvider",
    "TimeProvider",
    "extract_market_code",
    "parse_streaming_frame",
    "resolve_timezone_from_fields",
    "resolve_timezone_from_symbol",
    "split_streaming_frame",
]
