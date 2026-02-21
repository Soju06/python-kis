"""Quote domain models."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from pykis.service.enums import ChangeSign, Exchange, MarketWarning


@dataclass(frozen=True, slots=True)
class Quote:
    """Unified stock quote snapshot combining domestic and overseas price data."""

    symbol: str
    """Stock ticker symbol (e.g., '005930' for domestic, 'AAPL' for overseas)."""

    exchange: Exchange
    """Exchange where the stock is listed."""

    price: Decimal
    """Current price."""

    previous_close: Decimal
    """Previous trading day closing price."""

    change: Decimal
    """Price change from previous close (current - previous)."""

    change_rate: Decimal
    """Price change rate as percentage."""

    change_sign: ChangeSign
    """Direction of price change."""

    open: Decimal
    """Opening price for the current trading day."""

    high: Decimal
    """Highest price during the current trading day."""

    low: Decimal
    """Lowest price during the current trading day."""

    volume: int
    """Cumulative trading volume for the current day."""

    turnover: Decimal
    """Cumulative trading amount (value) for the current day."""

    previous_volume: int
    """Previous trading day volume."""

    upper_limit: Decimal | None
    """Upper limit price (domestic only)."""

    lower_limit: Decimal | None
    """Lower limit price (domestic only)."""

    market_warning: MarketWarning | None
    """Market warning classification (domestic only)."""

    is_trading_halted: bool | None
    """Whether trading is halted (domestic only)."""

    is_orderable: bool | None
    """Whether buy orders are possible (overseas only)."""
