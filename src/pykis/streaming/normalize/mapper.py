from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Protocol, cast

from pykis.streaming.normalize.models import (
    NormalizedEvent,
    NormalizedOrderBook,
    NormalizedOrderBookLevel,
    NormalizedTrade,
)
from pykis.streaming.raw import RAW_REGISTRY
from pykis.streaming.raw.base import StreamingRawModel


def _model_for(tr_id: str) -> type[StreamingRawModel]:
    spec = RAW_REGISTRY.get(tr_id)
    if spec is None:
        raise RuntimeError(f"Missing streaming spec for {tr_id}. Regenerate streaming raw models.")
    return spec.model


DOMESTIC_TRADE_TYPES = tuple(_model_for(tr_id) for tr_id in ("H0STCNT0", "H0NXCNT0", "H0UNCNT0", "H0UPCNT0"))
DOMESTIC_ORDERBOOK_TYPES = tuple(_model_for(tr_id) for tr_id in ("H0STASP0", "H0NXASP0", "H0UNASP0"))
OVERSEAS_TRADE_TYPES = (_model_for("HDFSCNT0"),)
OVERSEAS_ORDERBOOK_V1 = _model_for("HDFSASP0")
OVERSEAS_ORDERBOOK_V2 = _model_for("HDFSASP1")
OVERSEAS_ORDERBOOK_TYPES = (OVERSEAS_ORDERBOOK_V1, OVERSEAS_ORDERBOOK_V2)


def normalize_event(tr_id: str, record: StreamingRawModel) -> NormalizedEvent | None:
    if isinstance(record, DOMESTIC_TRADE_TYPES):
        return _normalize_domestic_trade(cast(DomesticTradeRaw, record), tr_id)
    if isinstance(record, OVERSEAS_TRADE_TYPES):
        return _normalize_overseas_trade(cast(OverseasTradeRaw, record), tr_id)
    if isinstance(record, DOMESTIC_ORDERBOOK_TYPES):
        return _normalize_domestic_orderbook(cast(DomesticOrderBookRaw, record), tr_id)
    if isinstance(record, OVERSEAS_ORDERBOOK_TYPES):
        return _normalize_overseas_orderbook(cast(OverseasOrderBookRaw, record), tr_id)
    return None


class DomesticTradeRaw(Protocol):
    MKSC_SHRN_ISCD: str
    STCK_CNTG_HOUR: datetime
    STCK_PRPR: Decimal | str
    CNTG_VOL: Decimal | str
    STCK_OPRC: Decimal | str
    STCK_HGPR: Decimal | str
    STCK_LWPR: Decimal | str
    PRDY_VRSS: Decimal | str
    PRDY_CTRT: Decimal | str
    ACML_TR_PBMN: Decimal | str
    BIDP1: Decimal | str
    ASKP1: Decimal | str


class DomesticOrderBookRaw(Protocol):
    MKSC_SHRN_ISCD: str
    BSOP_HOUR: datetime
    BIDP1: Decimal | str
    BIDP2: Decimal | str
    BIDP3: Decimal | str
    BIDP4: Decimal | str
    BIDP5: Decimal | str
    BIDP6: Decimal | str
    BIDP7: Decimal | str
    BIDP8: Decimal | str
    BIDP9: Decimal | str
    BIDP10: Decimal | str
    ASKP1: Decimal | str
    ASKP2: Decimal | str
    ASKP3: Decimal | str
    ASKP4: Decimal | str
    ASKP5: Decimal | str
    ASKP6: Decimal | str
    ASKP7: Decimal | str
    ASKP8: Decimal | str
    ASKP9: Decimal | str
    ASKP10: Decimal | str
    BIDP_RSQN1: Decimal | str
    BIDP_RSQN2: Decimal | str
    BIDP_RSQN3: Decimal | str
    BIDP_RSQN4: Decimal | str
    BIDP_RSQN5: Decimal | str
    BIDP_RSQN6: Decimal | str
    BIDP_RSQN7: Decimal | str
    BIDP_RSQN8: Decimal | str
    BIDP_RSQN9: Decimal | str
    BIDP_RSQN10: Decimal | str
    ASKP_RSQN1: Decimal | str
    ASKP_RSQN2: Decimal | str
    ASKP_RSQN3: Decimal | str
    ASKP_RSQN4: Decimal | str
    ASKP_RSQN5: Decimal | str
    ASKP_RSQN6: Decimal | str
    ASKP_RSQN7: Decimal | str
    ASKP_RSQN8: Decimal | str
    ASKP_RSQN9: Decimal | str
    ASKP_RSQN10: Decimal | str
    TOTAL_BIDP_RSQN: Decimal | str
    TOTAL_ASKP_RSQN: Decimal | str


class OverseasTradeRaw(Protocol):
    RSYM: str
    XHMS: datetime
    LAST: Decimal | str
    EVOL: Decimal | str
    OPEN: Decimal | str
    HIGH: Decimal | str
    LOW: Decimal | str
    DIFF: Decimal | str
    RATE: Decimal | str
    TAMT: Decimal | str
    PBID: Decimal | str
    PASK: Decimal | str


class OverseasOrderBookRaw(Protocol):
    RSYM: str
    XHMS: datetime


def _normalize_domestic_trade(record: DomesticTradeRaw, tr_id: str) -> NormalizedTrade:
    return NormalizedTrade(
        symbol=record.MKSC_SHRN_ISCD,
        market="domestic",
        timestamp_utc=record.STCK_CNTG_HOUR,
        price=_decimal_required(record.STCK_PRPR),
        volume=_decimal_required(record.CNTG_VOL),
        open=_decimal_optional(record.STCK_OPRC),
        high=_decimal_optional(record.STCK_HGPR),
        low=_decimal_optional(record.STCK_LWPR),
        change=_decimal_optional(record.PRDY_VRSS),
        change_rate=_decimal_optional(record.PRDY_CTRT),
        turnover=_decimal_optional(record.ACML_TR_PBMN),
        bid=_decimal_optional(record.BIDP1),
        ask=_decimal_optional(record.ASKP1),
        source_tr_id=tr_id,
    )


def _normalize_overseas_trade(record: OverseasTradeRaw, tr_id: str) -> NormalizedTrade:
    return NormalizedTrade(
        symbol=record.RSYM,
        market="overseas",
        timestamp_utc=record.XHMS,
        price=_decimal_required(record.LAST),
        volume=_decimal_required(record.EVOL),
        open=_decimal_optional(record.OPEN),
        high=_decimal_optional(record.HIGH),
        low=_decimal_optional(record.LOW),
        change=_decimal_optional(record.DIFF),
        change_rate=_decimal_optional(record.RATE),
        turnover=_decimal_optional(record.TAMT),
        bid=_decimal_optional(record.PBID),
        ask=_decimal_optional(record.PASK),
        source_tr_id=tr_id,
    )


def _normalize_domestic_orderbook(record: DomesticOrderBookRaw, tr_id: str) -> NormalizedOrderBook:
    bids = tuple(
        NormalizedOrderBookLevel(price=price, size=size)
        for price, size in _pair_levels(
            [
                record.BIDP1,
                record.BIDP2,
                record.BIDP3,
                record.BIDP4,
                record.BIDP5,
                record.BIDP6,
                record.BIDP7,
                record.BIDP8,
                record.BIDP9,
                record.BIDP10,
            ],
            [
                record.BIDP_RSQN1,
                record.BIDP_RSQN2,
                record.BIDP_RSQN3,
                record.BIDP_RSQN4,
                record.BIDP_RSQN5,
                record.BIDP_RSQN6,
                record.BIDP_RSQN7,
                record.BIDP_RSQN8,
                record.BIDP_RSQN9,
                record.BIDP_RSQN10,
            ],
        )
    )
    asks = tuple(
        NormalizedOrderBookLevel(price=price, size=size)
        for price, size in _pair_levels(
            [
                record.ASKP1,
                record.ASKP2,
                record.ASKP3,
                record.ASKP4,
                record.ASKP5,
                record.ASKP6,
                record.ASKP7,
                record.ASKP8,
                record.ASKP9,
                record.ASKP10,
            ],
            [
                record.ASKP_RSQN1,
                record.ASKP_RSQN2,
                record.ASKP_RSQN3,
                record.ASKP_RSQN4,
                record.ASKP_RSQN5,
                record.ASKP_RSQN6,
                record.ASKP_RSQN7,
                record.ASKP_RSQN8,
                record.ASKP_RSQN9,
                record.ASKP_RSQN10,
            ],
        )
    )
    return NormalizedOrderBook(
        symbol=record.MKSC_SHRN_ISCD,
        market="domestic",
        timestamp_utc=record.BSOP_HOUR,
        bids=bids,
        asks=asks,
        total_bid_size=_decimal_optional(record.TOTAL_BIDP_RSQN),
        total_ask_size=_decimal_optional(record.TOTAL_ASKP_RSQN),
        source_tr_id=tr_id,
    )


def _normalize_overseas_orderbook(
    record: OverseasOrderBookRaw,
    tr_id: str,
) -> NormalizedOrderBook:
    price_fields = _overseas_price_fields(record)
    size_fields = _overseas_size_fields(record)
    bids = _levels_from_attrs(record, price_fields["bid"], size_fields["bid"])
    asks = _levels_from_attrs(record, price_fields["ask"], size_fields["ask"])
    total_bid = _sum_sizes([level.size for level in bids])
    total_ask = _sum_sizes([level.size for level in asks])
    return NormalizedOrderBook(
        symbol=record.RSYM,
        market="overseas",
        timestamp_utc=record.XHMS,
        bids=bids,
        asks=asks,
        total_bid_size=total_bid,
        total_ask_size=total_ask,
        source_tr_id=tr_id,
    )


def _overseas_price_fields(record: OverseasOrderBookRaw) -> dict[str, list[str]]:
    if isinstance(record, OVERSEAS_ORDERBOOK_V1):
        bid = [
            "PBID1",
            "PBID2",
            "PBID3",
            "PBID3_2",
            "PBID4",
            "PBID5",
            "PBID6",
            "PBID7",
            "PBID8",
            "PBID9",
            "PBID10",
        ]
        ask = [
            "PASK1",
            "PASK2",
            "PASK3",
            "PASK3_2",
            "PASK4",
            "PASK5",
            "PASK6",
            "PASK7",
            "PASK8",
            "PASK9",
            "PASK10",
        ]
        return {"bid": bid, "ask": ask}
    bid = [
        "PBID1",
        "PBID2",
        "PBID3",
        "PBID4",
        "PBID5",
        "PBID6",
        "PBID7",
        "PBID8",
        "PBID9",
        "PBID10",
    ]
    ask = [
        "PASK1",
        "PASK2",
        "PASK3",
        "PASK4",
        "PASK5",
        "PASK6",
        "PASK7",
        "PASK8",
        "PASK9",
        "PASK10",
    ]
    return {"bid": bid, "ask": ask}


def _overseas_size_fields(record: OverseasOrderBookRaw) -> dict[str, list[str]]:
    if isinstance(record, OVERSEAS_ORDERBOOK_V1):
        bid = [
            "VBID1",
            "VBID2",
            "VBID3",
            "VBID3_2",
            "VBID4",
            "VBID5",
            "VBID6",
            "VBID7",
            "VBID8",
            "VBID9",
            "VBID10",
        ]
        ask = [
            "VASK1",
            "VASK2",
            "VASK3",
            "VASK3_2",
            "VASK4",
            "VASK5",
            "VASK6",
            "VASK7",
            "VASK8",
            "VASK9",
            "VASK10",
        ]
        return {"bid": bid, "ask": ask}
    bid = [
        "VBID1",
        "VBID2",
        "VBID3",
        "VBID4",
        "VBID5",
        "VBID6",
        "VBID7",
        "VBID8",
        "VBID9",
        "VBID10",
    ]
    ask = [
        "VASK1",
        "VASK2",
        "VASK3",
        "VASK4",
        "VASK5",
        "VASK6",
        "VASK7",
        "VASK8",
        "VASK9",
        "VASK10",
    ]
    return {"bid": bid, "ask": ask}


def _pair_levels(
    prices: list[Decimal | str | None],
    sizes: list[Decimal | str | None],
) -> list[tuple[Decimal, Decimal]]:
    levels: list[tuple[Decimal, Decimal]] = []
    for price, size in zip(prices, sizes, strict=False):
        price_value = _decimal_optional(price)
        size_value = _decimal_optional(size)
        if price_value is not None and size_value is not None:
            levels.append((price_value, size_value))
    return levels


def _levels_from_attrs(
    record: OverseasOrderBookRaw,
    prices: list[str],
    sizes: list[str],
) -> tuple[NormalizedOrderBookLevel, ...]:
    levels: list[NormalizedOrderBookLevel] = []
    for price_attr, size_attr in zip(prices, sizes, strict=False):
        price = getattr(record, price_attr, None)
        size = getattr(record, size_attr, None)
        if isinstance(price, Decimal) and isinstance(size, Decimal):
            levels.append(NormalizedOrderBookLevel(price=price, size=size))
    return tuple(levels)


def _sum_sizes(values: list[Decimal]) -> Decimal | None:
    if not values:
        return None
    total = Decimal(0)
    for value in values:
        total += value
    return total


def _decimal_required(value: Decimal | str) -> Decimal:
    if isinstance(value, Decimal):
        return value
    text = str(value).strip()
    if not text:
        raise ValueError("required decimal value is empty")
    try:
        return Decimal(text)
    except InvalidOperation as exc:
        raise ValueError("required decimal value is invalid") from exc


def _decimal_optional(value: Decimal | str | None) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return value
    text = str(value).strip()
    if not text:
        return None
    try:
        return Decimal(text)
    except InvalidOperation:
        return None
