"""Domestic stock quote L0 → Quote mapping."""

from __future__ import annotations

from decimal import Decimal
from typing import Protocol

from pykis.service._convert import decimal_required, int_to_decimal
from pykis.service._enum_map import MARKET_WARNING_CODE_TO_WARNING, SIGN_CODE_TO_CHANGE_SIGN
from pykis.service.enums import ChangeSign, Exchange, MarketWarning
from pykis.service.quote.models import Quote


class DomesticQuoteRaw(Protocol):
    """Structural contract for domestic stock quote output (InquirePrice2Output)."""

    stck_prpr: Decimal
    stck_prdy_clpr: int
    prdy_vrss: int
    prdy_ctrt: Decimal
    prdy_vrss_sign: int
    stck_oprc: Decimal
    stck_hgpr: Decimal
    stck_lwpr: Decimal
    acml_vol: int
    acml_tr_pbmn: Decimal
    prdy_vol: int
    stck_mxpr: int
    stck_llam: int
    mrkt_warn_cls_code: object  # MrktWarnClsCodeEnum (str-like)
    trht_yn: bool


def map_domestic_quote(
    raw: DomesticQuoteRaw,
    symbol: str,
    exchange: Exchange,
) -> Quote:
    """Map a domestic L0 quote output to a unified Quote model."""
    sign_code = str(raw.prdy_vrss_sign)
    change_sign = SIGN_CODE_TO_CHANGE_SIGN.get(sign_code, ChangeSign.FLAT)

    warning_code = str(raw.mrkt_warn_cls_code)
    market_warning = MARKET_WARNING_CODE_TO_WARNING.get(warning_code, MarketWarning.NONE)

    return Quote(
        symbol=symbol,
        exchange=exchange,
        price=decimal_required(raw.stck_prpr),
        previous_close=int_to_decimal(raw.stck_prdy_clpr),
        change=int_to_decimal(raw.prdy_vrss),
        change_rate=decimal_required(raw.prdy_ctrt),
        change_sign=change_sign,
        open=decimal_required(raw.stck_oprc),
        high=decimal_required(raw.stck_hgpr),
        low=decimal_required(raw.stck_lwpr),
        volume=raw.acml_vol,
        turnover=decimal_required(raw.acml_tr_pbmn),
        previous_volume=raw.prdy_vol,
        upper_limit=int_to_decimal(raw.stck_mxpr),
        lower_limit=int_to_decimal(raw.stck_llam),
        market_warning=market_warning,
        is_trading_halted=bool(raw.trht_yn),
        is_orderable=None,
    )
