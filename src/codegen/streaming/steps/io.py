from __future__ import annotations

from pathlib import Path
from typing import Mapping, cast

import yaml

from codegen.streaming.models import (
    DateTimeRule,
    DecimalRule,
    FieldSpec,
    StreamingSpecRoot,
    TrSpec,
)


class SpecError(ValueError):
    pass


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def load_streaming_spec(path: Path) -> StreamingSpecRoot:
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, Mapping):
        raise SpecError(f"Invalid spec root in {path}")

    tr_specs_raw = data.get("tr_specs")
    if not isinstance(tr_specs_raw, Mapping):
        raise SpecError("Spec must include tr_specs mapping")

    tr_specs: dict[str, TrSpec] = {}
    for tr_id, tr_data in tr_specs_raw.items():
        if not isinstance(tr_data, Mapping):
            raise SpecError(f"Invalid TR spec for {tr_id}")
        tr_specs[str(tr_id)] = _parse_tr_spec(str(tr_id), tr_data)

    return StreamingSpecRoot(
        version=int(data.get("version", 0)),
        source_inventory=str(data.get("source_inventory", "")),
        domestic_count=int(data.get("domestic_count", 0)),
        overseas_count=int(data.get("overseas_count", 0)),
        tr_specs=tr_specs,
    )


def _parse_tr_spec(tr_id: str, data: Mapping[str, object]) -> TrSpec:
    field_order_raw = data.get("field_order")
    if not isinstance(field_order_raw, list) or not all(isinstance(item, str) for item in field_order_raw):
        raise SpecError(f"tr_specs.{tr_id}.field_order must be list[str]")
    field_order = tuple(str(item) for item in field_order_raw)

    field_order_norm_raw = data.get("field_order_normalized")
    if field_order_norm_raw is not None:
        if not isinstance(field_order_norm_raw, list) or not all(
            isinstance(item, str) for item in field_order_norm_raw
        ):
            raise SpecError(f"tr_specs.{tr_id}.field_order_normalized must be list[str]")
        field_order_normalized: tuple[str, ...] | None = tuple(str(item) for item in field_order_norm_raw)
    else:
        field_order_normalized = None

    field_aliases_raw = data.get("field_aliases") or {}
    if not isinstance(field_aliases_raw, Mapping):
        raise SpecError(f"tr_specs.{tr_id}.field_aliases must be mapping")
    field_aliases: dict[int, str] = {}
    for key, value in field_aliases_raw.items():
        if not isinstance(value, str):
            raise SpecError(f"tr_specs.{tr_id}.field_aliases values must be str")
        try:
            index = int(key)
        except (TypeError, ValueError) as exc:
            raise SpecError(f"tr_specs.{tr_id}.field_aliases keys must be int-compatible") from exc
        field_aliases[index] = value

    field_specs_raw = data.get("field_specs")
    if not isinstance(field_specs_raw, Mapping):
        raise SpecError(f"tr_specs.{tr_id}.field_specs must be mapping")

    field_specs: dict[str, FieldSpec] = {}
    for name, spec_data in field_specs_raw.items():
        if not isinstance(spec_data, Mapping):
            raise SpecError(f"tr_specs.{tr_id}.field_specs.{name} invalid")
        field_specs[str(name)] = _parse_field_spec(str(name), cast(Mapping[str, object], spec_data))

    return TrSpec(
        tr_id=tr_id,
        endpoint_uuid=str(data.get("endpoint_uuid", "")),
        market=str(data.get("market", "domestic")),
        timezone=str(data.get("timezone", "Asia/Seoul")),
        field_order=field_order,
        field_order_normalized=field_order_normalized,
        field_aliases=field_aliases,
        requires_business_date=bool(data.get("requires_business_date", False)),
        field_specs=field_specs,
    )


def _parse_field_spec(name: str, data: Mapping[str, object]) -> FieldSpec:
    field_type = data.get("type")
    if not isinstance(field_type, str):
        raise SpecError(f"field_specs.{name}.type must be str")
    source = data.get("source", "rule")
    if not isinstance(source, str):
        raise SpecError(f"field_specs.{name}.source must be str")

    datetime_rule = None
    datetime_data = data.get("datetime")
    if datetime_data is not None:
        if not isinstance(datetime_data, Mapping):
            raise SpecError(f"field_specs.{name}.datetime must be mapping")
        datetime_data = cast(Mapping[str, object], datetime_data)
        datetime_rule = DateTimeRule(
            kind=str(datetime_data.get("kind")),
            format=str(datetime_data.get("format")),
            timezone=str(datetime_data.get("timezone")),
            date_field=_optional_str(datetime_data.get("date_field")),
            year_policy=_optional_str(datetime_data.get("year_policy")),
        )

    decimal_rule = None
    decimal_data = data.get("decimal")
    if decimal_data is not None:
        if not isinstance(decimal_data, Mapping):
            raise SpecError(f"field_specs.{name}.decimal must be mapping")
        decimal_data = cast(Mapping[str, object], decimal_data)
        decimal_rule = DecimalRule(
            scale=str(decimal_data.get("scale")),
            zdiv_field=str(decimal_data.get("zdiv_field")),
        )

    return FieldSpec(
        name=name,
        field_type=str(field_type),
        source=source,
        datetime_rule=datetime_rule,
        decimal_rule=decimal_rule,
    )
