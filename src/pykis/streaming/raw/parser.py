from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from decimal import Decimal, InvalidOperation
from typing import Iterable, Protocol
from zoneinfo import ZoneInfo

from pydantic import ValidationError

from pykis.errors import PykisError
from pykis.streaming.raw.context import StreamingParseContext
from pykis.streaming.raw.overrides import NullOverrideLogger, OverrideCandidate, OverrideLogger
from pykis.streaming.raw.specs import FieldSource, FieldType, SpecRegistry, StreamingSpec


@dataclass(frozen=True, slots=True)
class StreamingParseResult:
    tr_id: str
    encrypted: bool
    expected_count: int | None
    records: list[object]


class StreamingParseError(PykisError):
    __slots__ = ("message", "tr_id", "payload")

    def __init__(self, message: str, *, tr_id: str | None = None, payload: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.tr_id = tr_id
        self.payload = payload


class PayloadDecryptor(Protocol):
    def decrypt(self, tr_id: str, payload: str) -> str: ...


def parse_streaming_frame(
    frame: str,
    *,
    registry: SpecRegistry,
    context: StreamingParseContext,
    override_logger: OverrideLogger | None = None,
    decryptor: PayloadDecryptor | None = None,
) -> StreamingParseResult | None:
    frame = frame.strip()
    if not frame:
        return None
    if frame.startswith("{") or frame.startswith("["):
        return None

    encrypted, tr_id, expected_count, payload = split_streaming_frame(frame)
    if tr_id not in registry:
        raise StreamingParseError("Unknown tr_id", tr_id=tr_id, payload=payload)

    spec = registry[tr_id]
    if encrypted:
        if decryptor is None:
            raise StreamingParseError("Encrypted payload without decryptor", tr_id=tr_id, payload=payload)
        payload = decryptor.decrypt(tr_id, payload)
    records = _parse_payload(
        payload,
        spec,
        context,
        override_logger=override_logger or NullOverrideLogger(),
    )

    if expected_count is not None and expected_count != len(records):
        _record_candidate(
            override_logger or NullOverrideLogger(),
            spec,
            field="_count",
            raw_value=str(expected_count),
            decision="count_mismatch",
            reason=f"expected {expected_count} but parsed {len(records)}",
            payload=payload,
        )

    return StreamingParseResult(
        tr_id=tr_id,
        encrypted=encrypted,
        expected_count=expected_count,
        records=records,
    )


def split_streaming_frame(frame: str) -> tuple[bool, str, int | None, str]:
    parts = frame.split("|", 3)
    if len(parts) < 4:
        raise StreamingParseError("Invalid frame: missing header sections", payload=frame)
    enc_flag, tr_id, count_text, payload = parts
    encrypted = enc_flag.strip() == "1"
    expected_count = None
    if count_text.strip().isdigit():
        expected_count = int(count_text.strip())
    return encrypted, tr_id.strip(), expected_count, payload


def _parse_payload(
    payload: str,
    spec: StreamingSpec,
    context: StreamingParseContext,
    *,
    override_logger: OverrideLogger,
) -> list[object]:
    values = payload.split("^")
    field_count = len(spec.field_order)
    if field_count == 0:
        raise StreamingParseError("Spec has no fields", tr_id=spec.tr_id, payload=payload)
    if len(values) % field_count != 0:
        raise StreamingParseError(
            "Payload length is not a multiple of field_count",
            tr_id=spec.tr_id,
            payload=payload,
        )

    records: list[object] = []
    for offset in range(0, len(values), field_count):
        chunk = values[offset : offset + field_count]
        record = _parse_record(chunk, spec, context, override_logger, payload)
        records.append(record)
    return records


def _parse_record(
    values: Iterable[str],
    spec: StreamingSpec,
    context: StreamingParseContext,
    override_logger: OverrideLogger,
    payload: str,
) -> object:
    values_list = list(values)
    field_names = _field_names(spec)
    raw_map: dict[str, str] = {}
    for idx, name in enumerate(field_names):
        raw_map[name] = values_list[idx].strip()

    zdiv_value = _resolve_zdiv(raw_map, spec, context, override_logger, payload)
    parsed: dict[str, object] = {}

    for name in field_names:
        raw_value = raw_map[name]
        field_type = spec.field_types[name]
        if field_type == FieldType.STR:
            parsed[name] = raw_value
            continue
        if field_type == FieldType.INT:
            parsed[name] = _parse_int(raw_value, spec, name, override_logger, payload)
            continue
        if field_type == FieldType.DECIMAL:
            rule = spec.decimal_rules.get(name)
            parsed[name] = _parse_decimal(
                raw_value,
                rule,
                zdiv_value,
                spec,
                name,
                override_logger,
                payload,
            )
            continue
        if field_type == FieldType.DATETIME:
            rule = spec.datetime_rules.get(name)
            if rule is None:
                raise StreamingParseError("Missing datetime rule", tr_id=spec.tr_id, payload=payload)
            parsed[name] = _parse_datetime(
                raw_value,
                rule,
                spec,
                context,
                raw_map,
                override_logger,
                payload,
            )
            continue

    try:
        return spec.model.model_validate(parsed)
    except ValidationError as exc:
        raise StreamingParseError(f"Model validation failed: {exc}", tr_id=spec.tr_id, payload=payload) from exc


def _field_names(spec: StreamingSpec) -> list[str]:
    names: list[str] = []
    for idx, code in enumerate(spec.field_order):
        names.append(spec.field_aliases.get(idx, code))
    return names


def _resolve_zdiv(
    raw_map: dict[str, str],
    spec: StreamingSpec,
    context: StreamingParseContext,
    override_logger: OverrideLogger,
    payload: str,
) -> int | None:
    if context.zdiv is not None:
        return context.zdiv
    if "ZDIV" not in spec.field_order:
        return None
    value = raw_map.get("ZDIV")
    if not value:
        _record_candidate(
            override_logger,
            spec,
            field="ZDIV",
            raw_value=value or "",
            decision="int",
            reason="zdiv_missing",
            payload=payload,
        )
        return None
    try:
        return int(value)
    except ValueError:
        _record_candidate(
            override_logger,
            spec,
            field="ZDIV",
            raw_value=value,
            decision="int",
            reason="zdiv_invalid",
            payload=payload,
        )
        return None


def _parse_int(
    raw_value: str,
    spec: StreamingSpec,
    field: str,
    override_logger: OverrideLogger,
    payload: str,
) -> int:
    if raw_value == "":
        raise StreamingParseError("Empty int field", tr_id=spec.tr_id, payload=payload)
    try:
        return int(raw_value)
    except ValueError as exc:
        _record_candidate(
            override_logger,
            spec,
            field=field,
            raw_value=raw_value,
            decision="int",
            reason="int_parse_error",
            payload=payload,
        )
        raise StreamingParseError("Invalid int field", tr_id=spec.tr_id, payload=payload) from exc


def _parse_decimal(
    raw_value: str,
    rule,
    zdiv_value: int | None,
    spec: StreamingSpec,
    field: str,
    override_logger: OverrideLogger,
    payload: str,
) -> Decimal:
    if raw_value == "":
        raise StreamingParseError("Empty decimal field", tr_id=spec.tr_id, payload=payload)
    try:
        value = Decimal(raw_value)
    except InvalidOperation as exc:
        _record_candidate(
            override_logger,
            spec,
            field=field,
            raw_value=raw_value,
            decision="decimal",
            reason="decimal_parse_error",
            payload=payload,
        )
        raise StreamingParseError("Invalid decimal field", tr_id=spec.tr_id, payload=payload) from exc

    if rule is not None:
        if zdiv_value is None:
            _record_candidate(
                override_logger,
                spec,
                field=field,
                raw_value=raw_value,
                decision="decimal",
                reason="zdiv_missing",
                payload=payload,
            )
            return value
        try:
            value = value / (Decimal(10) ** zdiv_value)
        except InvalidOperation as exc:
            _record_candidate(
                override_logger,
                spec,
                field=field,
                raw_value=raw_value,
                decision="decimal",
                reason="zdiv_scale_error",
                payload=payload,
            )
            raise StreamingParseError("Decimal scale error", tr_id=spec.tr_id, payload=payload) from exc

    source = spec.field_sources.get(field)
    if source == FieldSource.HEURISTIC:
        _record_candidate(
            override_logger,
            spec,
            field=field,
            raw_value=raw_value,
            decision="decimal",
            reason="heuristic_decimal",
            payload=payload,
            confidence=0.5,
        )
    return value


def _parse_datetime(
    raw_value: str,
    rule,
    spec: StreamingSpec,
    context: StreamingParseContext,
    raw_map: dict[str, str],
    override_logger: OverrideLogger,
    payload: str,
) -> datetime:
    if raw_value == "":
        raise StreamingParseError("Empty datetime field", tr_id=spec.tr_id, payload=payload)

    tzinfo = _resolve_timezone(rule.timezone, context)
    if rule.kind == "date_only":
        parsed_date = _parse_date(
            raw_value,
            rule.format,
            tzinfo,
            context,
            rule.year_policy,
            raw_map,
            rule.timezone,
            override_logger,
            spec,
            payload,
        )
        return datetime.combine(parsed_date, time(0, 0), tzinfo=tzinfo).astimezone(timezone.utc)

    if rule.kind == "time_only":
        if not rule.date_field:
            raise StreamingParseError("Missing date_field for time_only", tr_id=spec.tr_id, payload=payload)
        base_date = _resolve_date_field(rule.date_field, spec, context, raw_map, override_logger, payload)
        parsed_time = _parse_time(raw_value)
        local_dt = datetime.combine(base_date, parsed_time, tzinfo=tzinfo)
        return local_dt.astimezone(timezone.utc)

    raise StreamingParseError("Unsupported datetime rule", tr_id=spec.tr_id, payload=payload)


def _resolve_date_field(
    date_field: str,
    spec: StreamingSpec,
    context: StreamingParseContext,
    raw_map: dict[str, str],
    override_logger: OverrideLogger,
    payload: str,
) -> date:
    if date_field == "business_date":
        resolved = context.resolve_business_date()
        if context.time_backwards:
            _record_candidate(
                override_logger,
                spec,
                field="business_date",
                raw_value=str(resolved),
                decision="datetime",
                reason="time_backwards",
                payload=payload,
                confidence=0.3,
            )
            context.time_backwards = False
        return resolved
    raw_value = raw_map.get(date_field, "")
    rule = spec.datetime_rules.get(date_field)
    if rule is None:
        _record_candidate(
            override_logger,
            spec,
            field=date_field,
            raw_value=raw_value,
            decision="datetime",
            reason="missing_date_rule",
            payload=payload,
        )
        raise StreamingParseError("Missing date rule for dependent field", tr_id=spec.tr_id, payload=payload)
    tzinfo = _resolve_timezone(rule.timezone, context)
    parsed_date = _parse_date(
        raw_value,
        rule.format,
        tzinfo,
        context,
        rule.year_policy,
        raw_map,
        rule.timezone,
        override_logger,
        spec,
        payload,
    )
    return parsed_date


def _parse_date(
    raw_value: str,
    fmt: str,
    tzinfo: ZoneInfo,
    context: StreamingParseContext,
    year_policy: str | None,
    raw_map: dict[str, str],
    rule_timezone: str,
    override_logger: OverrideLogger,
    spec: StreamingSpec,
    payload: str,
) -> date:
    text = raw_value.strip()
    if fmt == "YYYYMMDD":
        return datetime.strptime(text, "%Y%m%d").date()
    if fmt == "YYMMDD":
        year = int(text[:2])
        month = int(text[2:4])
        day = int(text[4:6])
        anchor_year = None
        if year_policy == "century_from_local" and rule_timezone == "market":
            anchor_year = _resolve_anchor_year(raw_map.get("TYMD"), override_logger, spec, payload)
        if anchor_year is not None:
            year = anchor_year
        else:
            if year_policy == "century_from_local":
                local_year = context.time_provider.now_utc().astimezone(tzinfo).year
                year += (local_year // 100) * 100
            else:
                year += 2000
        return date(year, month, day)
    raise StreamingParseError("Unsupported date format", payload=text)


def _parse_time(raw_value: str) -> time:
    text = raw_value.strip()
    return datetime.strptime(text, "%H%M%S").time()


def _resolve_timezone(value: str, context: StreamingParseContext) -> ZoneInfo:
    if value == "market":
        return ZoneInfo(context.market_timezone)
    return ZoneInfo(value)


def _resolve_anchor_year(
    tymd: str | None,
    override_logger: OverrideLogger,
    spec: StreamingSpec,
    payload: str,
) -> int | None:
    if not tymd:
        return None
    text = tymd.strip()
    if len(text) != 8 or not text.isdigit():
        _record_candidate(
            override_logger,
            spec,
            field="TYMD",
            raw_value=text,
            decision="datetime",
            reason="yy_anchor_invalid",
            payload=payload,
            confidence=0.4,
        )
        return None
    return int(text[:4])


def _record_candidate(
    logger: OverrideLogger,
    spec: StreamingSpec,
    *,
    field: str,
    raw_value: str,
    decision: str,
    reason: str,
    payload: str,
    confidence: float = 0.8,
) -> None:
    logger.record(
        OverrideCandidate(
            endpoint_uuid=spec.endpoint_uuid,
            tr_id=spec.tr_id,
            field=field,
            raw_value=raw_value,
            rule=spec.field_sources.get(field, FieldSource.RULE).value,
            decision=decision,
            confidence=confidence,
            reason=reason,
            market=spec.market,
            timezone=spec.timezone_hint,
            sample_payload=payload[:512],
            timestamp_utc=datetime.now(timezone.utc),
            notes=None,
        )
    )
