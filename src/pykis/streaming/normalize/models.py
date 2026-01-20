from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal

Market = Literal["domestic", "overseas"]


@dataclass(frozen=True, slots=True)
class NormalizedTrade:
    symbol: str
    market: Market
    timestamp_utc: datetime
    price: Decimal
    volume: Decimal
    open: Decimal | None
    high: Decimal | None
    low: Decimal | None
    change: Decimal | None
    change_rate: Decimal | None
    turnover: Decimal | None
    bid: Decimal | None
    ask: Decimal | None
    source_tr_id: str


@dataclass(frozen=True, slots=True)
class NormalizedOrderBookLevel:
    price: Decimal
    size: Decimal


@dataclass(frozen=True, slots=True)
class NormalizedOrderBook:
    symbol: str
    market: Market
    timestamp_utc: datetime
    bids: tuple[NormalizedOrderBookLevel, ...]
    asks: tuple[NormalizedOrderBookLevel, ...]
    total_bid_size: Decimal | None
    total_ask_size: Decimal | None
    source_tr_id: str


NormalizedEvent = NormalizedTrade | NormalizedOrderBook
