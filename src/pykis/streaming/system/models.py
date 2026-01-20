from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pykis.streaming.normalize.models import NormalizedOrderBookLevel

Market = Literal["domestic", "overseas"]


@dataclass(frozen=True, slots=True)
class SystemTrade:
    symbol: str
    market: Market
    timestamp_utc: datetime
    price: Decimal
    volume: Decimal
    notional: Decimal
    open: Decimal | None
    high: Decimal | None
    low: Decimal | None
    change: Decimal | None
    change_rate: Decimal | None
    turnover: Decimal | None
    bid: Decimal | None
    ask: Decimal | None
    mid: Decimal | None
    spread: Decimal | None
    source_tr_id: str


@dataclass(frozen=True, slots=True)
class SystemOrderBook:
    symbol: str
    market: Market
    timestamp_utc: datetime
    bids: tuple[NormalizedOrderBookLevel, ...]
    asks: tuple[NormalizedOrderBookLevel, ...]
    total_bid_size: Decimal | None
    total_ask_size: Decimal | None
    mid: Decimal | None
    spread: Decimal | None
    imbalance: Decimal | None
    source_tr_id: str


SystemEvent = SystemTrade | SystemOrderBook
