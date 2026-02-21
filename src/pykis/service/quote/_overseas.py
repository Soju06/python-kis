"""Overseas stock quote L0 → Quote mapping."""

from __future__ import annotations

from decimal import Decimal
from typing import Protocol

from pykis.service._convert import decimal_required
from pykis.service._enum_map import SIGN_CODE_TO_CHANGE_SIGN
from pykis.service.enums import ChangeSign, Exchange
from pykis.service.quote.models import Quote


class OverseasQuoteRaw(Protocol):
    """Structural contract for overseas stock quote output (PriceOutput)."""

    last: Decimal
    base: Decimal
    diff: Decimal
    rate: Decimal
    sign: object  # SignEnum (str-like)
    tvol: int
    tamt: Decimal
    pvol: int
    ordy: bool


def map_overseas_quote(
    raw: OverseasQuoteRaw,
    symbol: str,
    exchange: Exchange,
) -> Quote:
    """Map an overseas L0 quote output to a unified Quote model."""
    sign_code = str(raw.sign)
    change_sign = SIGN_CODE_TO_CHANGE_SIGN.get(sign_code, ChangeSign.FLAT)

    return Quote(
        symbol=symbol,
        exchange=exchange,
        price=decimal_required(raw.last),
        previous_close=decimal_required(raw.base),
        change=decimal_required(raw.diff),
        change_rate=decimal_required(raw.rate),
        change_sign=change_sign,
        open=Decimal(0),
        high=Decimal(0),
        low=Decimal(0),
        volume=raw.tvol,
        turnover=decimal_required(raw.tamt),
        previous_volume=raw.pvol,
        upper_limit=None,
        lower_limit=None,
        market_warning=None,
        is_trading_halted=None,
        is_orderable=bool(raw.ordy),
    )
