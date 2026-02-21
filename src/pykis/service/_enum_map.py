"""Bidirectional mapping between L0 raw enum codes and L1 service enums."""

from __future__ import annotations

from pykis.service.enums import ChangeSign, Exchange, MarketWarning

# ---------------------------------------------------------------------------
# Exchange mappings
# ---------------------------------------------------------------------------

# Domestic: FID_COND_MRKT_DIV_CODE → Exchange
DOMESTIC_MARKET_CODE_TO_EXCHANGE: dict[str, Exchange] = {
    "J": Exchange.KRX,
    "NX": Exchange.NXT,
    "UN": Exchange.KRX,  # "통합" maps to KRX as the primary domestic exchange
}

# Overseas: EXCD → Exchange
OVERSEAS_EXCD_TO_EXCHANGE: dict[str, Exchange] = {
    "NYS": Exchange.NYSE,
    "NAS": Exchange.NASDAQ,
    "AMS": Exchange.AMEX,
    "TSE": Exchange.TSE,
    "HKS": Exchange.SEHK,
    "SHS": Exchange.SSE,
    "SZS": Exchange.SZSE,
    "SHI": Exchange.SSE_INDEX,
    "SZI": Exchange.SZSE_INDEX,
    "HSX": Exchange.HSX,
    "HNX": Exchange.HNX,
    "BAY": Exchange.NYSE_EXTENDED,
    "BAQ": Exchange.NASDAQ_EXTENDED,
    "BAA": Exchange.AMEX_EXTENDED,
}

# Reverse: Exchange → EXCD (overseas request parameter)
EXCHANGE_TO_OVERSEAS_EXCD: dict[Exchange, str] = {v: k for k, v in OVERSEAS_EXCD_TO_EXCHANGE.items()}

# Reverse: Exchange → FID_COND_MRKT_DIV_CODE (domestic request parameter)
EXCHANGE_TO_DOMESTIC_MARKET_CODE: dict[Exchange, str] = {
    Exchange.KRX: "J",
    Exchange.NXT: "NX",
}

# ---------------------------------------------------------------------------
# ChangeSign mappings
# ---------------------------------------------------------------------------

# L0 sign code (str) → ChangeSign
# Used by both domestic (prdy_vrss_sign as int-string) and overseas (sign enum)
SIGN_CODE_TO_CHANGE_SIGN: dict[str, ChangeSign] = {
    "1": ChangeSign.UPPER_LIMIT,
    "2": ChangeSign.RISE,
    "3": ChangeSign.FLAT,
    "4": ChangeSign.LOWER_LIMIT,
    "5": ChangeSign.FALL,
}

# ---------------------------------------------------------------------------
# MarketWarning mappings
# ---------------------------------------------------------------------------

MARKET_WARNING_CODE_TO_WARNING: dict[str, MarketWarning] = {
    "00": MarketWarning.NONE,
    "01": MarketWarning.CAUTION,
    "02": MarketWarning.WARNING,
    "03": MarketWarning.RISK,
}
