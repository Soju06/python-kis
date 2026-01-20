from __future__ import annotations

from decimal import Decimal

from pykis.streaming.normalize.models import (
    NormalizedEvent,
    NormalizedOrderBook,
    NormalizedOrderBookLevel,
    NormalizedTrade,
)
from pykis.streaming.raw.generated.h0nxcnt0 import H0NXCNT0
from pykis.streaming.raw.generated.h0nxasp0 import H0NXASP0
from pykis.streaming.raw.generated.h0stcnt0 import H0STCNT0
from pykis.streaming.raw.generated.h0stasp0 import H0STASP0
from pykis.streaming.raw.generated.h0uncnt0 import H0UNCNT0
from pykis.streaming.raw.generated.h0unasp0 import H0UNASP0
from pykis.streaming.raw.generated.h0upcnt0 import H0UPCNT0
from pykis.streaming.raw.generated.h0upasp0 import H0UPASP0
from pykis.streaming.raw.generated.hdfscnt0 import HDFSCNT0
from pykis.streaming.raw.generated.hdfsasp0 import HDFSASP0
from pykis.streaming.raw.generated.hdfsasp1 import HDFSASP1
from pykis.streaming.raw.base import StreamingRawModel


def normalize_event(tr_id: str, record: StreamingRawModel) -> NormalizedEvent | None:
    if isinstance(record, (H0STCNT0, H0NXCNT0, H0UNCNT0, H0UPCNT0)):
        return _normalize_domestic_trade(record, tr_id)
    if isinstance(record, HDFSCNT0):
        return _normalize_overseas_trade(record, tr_id)
    if isinstance(record, (H0STASP0, H0NXASP0, H0UNASP0, H0UPASP0)):
        return _normalize_domestic_orderbook(record, tr_id)
    if isinstance(record, (HDFSASP0, HDFSASP1)):
        return _normalize_overseas_orderbook(record, tr_id)
    return None


def _normalize_domestic_trade(
    record: H0STCNT0 | H0NXCNT0 | H0UNCNT0 | H0UPCNT0,
    tr_id: str,
) -> NormalizedTrade:
    return NormalizedTrade(
        symbol=record.MKSC_SHRN_ISCD,
        market="domestic",
        timestamp_utc=record.STCK_CNTG_HOUR,
        price=record.STCK_PRPR,
        volume=record.CNTG_VOL,
        open=record.STCK_OPRC,
        high=record.STCK_HGPR,
        low=record.STCK_LWPR,
        change=record.PRDY_VRSS,
        change_rate=record.PRDY_CTRT,
        turnover=record.ACML_TR_PBMN,
        bid=record.BIDP1,
        ask=record.ASKP1,
        source_tr_id=tr_id,
    )


def _normalize_overseas_trade(record: HDFSCNT0, tr_id: str) -> NormalizedTrade:
    return NormalizedTrade(
        symbol=record.RSYM,
        market="overseas",
        timestamp_utc=record.XHMS,
        price=record.LAST,
        volume=record.EVOL,
        open=record.OPEN,
        high=record.HIGH,
        low=record.LOW,
        change=record.DIFF,
        change_rate=record.RATE,
        turnover=record.TAMT,
        bid=record.PBID,
        ask=record.PASK,
        source_tr_id=tr_id,
    )


def _normalize_domestic_orderbook(
    record: H0STASP0 | H0NXASP0 | H0UNASP0 | H0UPASP0,
    tr_id: str,
) -> NormalizedOrderBook:
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
        total_bid_size=record.TOTAL_BIDP_RSQN,
        total_ask_size=record.TOTAL_ASKP_RSQN,
        source_tr_id=tr_id,
    )


def _normalize_overseas_orderbook(
    record: HDFSASP0 | HDFSASP1,
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


def _overseas_price_fields(record: HDFSASP0 | HDFSASP1) -> dict[str, list[str]]:
    if isinstance(record, HDFSASP0):
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


def _overseas_size_fields(record: HDFSASP0 | HDFSASP1) -> dict[str, list[str]]:
    if isinstance(record, HDFSASP0):
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
    prices: list[Decimal | None],
    sizes: list[Decimal | None],
) -> list[tuple[Decimal, Decimal]]:
    levels: list[tuple[Decimal, Decimal]] = []
    for price, size in zip(prices, sizes, strict=False):
        if isinstance(price, Decimal) and isinstance(size, Decimal):
            levels.append((price, size))
    return levels


def _levels_from_attrs(
    record: HDFSASP0 | HDFSASP1,
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
