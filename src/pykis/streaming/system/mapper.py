from __future__ import annotations

from decimal import Decimal

from pykis.streaming.normalize.models import NormalizedEvent, NormalizedOrderBook, NormalizedTrade
from pykis.streaming.system.models import SystemEvent, SystemOrderBook, SystemTrade


def build_system_event(event: NormalizedEvent) -> SystemEvent:
    if isinstance(event, NormalizedTrade):
        return _build_trade(event)
    return _build_orderbook(event)


def _build_trade(event: NormalizedTrade) -> SystemTrade:
    notional = event.price * event.volume
    mid = None
    spread = None
    if event.bid is not None and event.ask is not None:
        mid = (event.bid + event.ask) / Decimal(2)
        spread = event.ask - event.bid
    return SystemTrade(
        symbol=event.symbol,
        market=event.market,
        timestamp_utc=event.timestamp_utc,
        price=event.price,
        volume=event.volume,
        notional=notional,
        open=event.open,
        high=event.high,
        low=event.low,
        change=event.change,
        change_rate=event.change_rate,
        turnover=event.turnover,
        bid=event.bid,
        ask=event.ask,
        mid=mid,
        spread=spread,
        source_tr_id=event.source_tr_id,
    )


def _build_orderbook(event: NormalizedOrderBook) -> SystemOrderBook:
    mid = None
    spread = None
    if event.bids and event.asks:
        best_bid = event.bids[0].price
        best_ask = event.asks[0].price
        mid = (best_bid + best_ask) / Decimal(2)
        spread = best_ask - best_bid
    imbalance = None
    if event.total_bid_size is not None and event.total_ask_size is not None:
        imbalance = event.total_bid_size - event.total_ask_size
    return SystemOrderBook(
        symbol=event.symbol,
        market=event.market,
        timestamp_utc=event.timestamp_utc,
        bids=event.bids,
        asks=event.asks,
        total_bid_size=event.total_bid_size,
        total_ask_size=event.total_ask_size,
        mid=mid,
        spread=spread,
        imbalance=imbalance,
        source_tr_id=event.source_tr_id,
    )
