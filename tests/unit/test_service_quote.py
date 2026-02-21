"""Tests for the Quote service layer (L0 → L1 mapping)."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from pykis.service.enums import ChangeSign, Exchange, MarketWarning
from pykis.service.quote._domestic import map_domestic_quote
from pykis.service.quote._overseas import map_overseas_quote
from pykis.service.quote.models import Quote

# ---------------------------------------------------------------------------
# Fixtures: mock L0 raw outputs satisfying the Protocol contracts
# ---------------------------------------------------------------------------


@dataclass
class MockDomesticQuoteOutput:
    """Mimics InquirePrice2Output with representative field values."""

    stck_prpr: Decimal = Decimal("67300")
    stck_prdy_clpr: int = 67000
    prdy_vrss: int = 300
    prdy_ctrt: Decimal = Decimal("0.45")
    prdy_vrss_sign: int = 2  # rise
    stck_oprc: Decimal = Decimal("67100")
    stck_hgpr: Decimal = Decimal("67500")
    stck_lwpr: Decimal = Decimal("66800")
    acml_vol: int = 15_000_000
    acml_tr_pbmn: Decimal = Decimal("1009500000000")
    prdy_vol: int = 12_000_000
    stck_mxpr: int = 87100
    stck_llam: int = 46900
    mrkt_warn_cls_code: str = "00"
    trht_yn: bool = False


@dataclass
class MockOverseasQuoteOutput:
    """Mimics PriceOutput with representative field values."""

    rsym: str = "DNASAAPL"
    zdiv: int = 2
    last: Decimal = Decimal("178.72")
    base: Decimal = Decimal("177.56")
    diff: Decimal = Decimal("1.16")
    rate: Decimal = Decimal("0.65")
    sign: str = "2"  # rise
    tvol: int = 45_000_000
    tamt: Decimal = Decimal("8040000000")
    pvol: int = 42_000_000
    ordy: bool = True


# ---------------------------------------------------------------------------
# Domestic mapping tests
# ---------------------------------------------------------------------------


class TestDomesticQuoteMapping:
    def test_basic_price_fields(self) -> None:
        raw = MockDomesticQuoteOutput()
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)

        assert quote.symbol == "005930"
        assert quote.exchange == Exchange.KRX
        assert quote.price == Decimal("67300")
        assert quote.previous_close == Decimal("67000")
        assert quote.change == Decimal("300")
        assert quote.change_rate == Decimal("0.45")

    def test_change_sign_rise(self) -> None:
        raw = MockDomesticQuoteOutput(prdy_vrss_sign=2)
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)
        assert quote.change_sign == ChangeSign.RISE

    def test_change_sign_fall(self) -> None:
        raw = MockDomesticQuoteOutput(prdy_vrss_sign=5)
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)
        assert quote.change_sign == ChangeSign.FALL

    def test_change_sign_flat(self) -> None:
        raw = MockDomesticQuoteOutput(prdy_vrss_sign=3)
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)
        assert quote.change_sign == ChangeSign.FLAT

    def test_change_sign_upper_limit(self) -> None:
        raw = MockDomesticQuoteOutput(prdy_vrss_sign=1)
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)
        assert quote.change_sign == ChangeSign.UPPER_LIMIT

    def test_change_sign_lower_limit(self) -> None:
        raw = MockDomesticQuoteOutput(prdy_vrss_sign=4)
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)
        assert quote.change_sign == ChangeSign.LOWER_LIMIT

    def test_ohlcv_fields(self) -> None:
        raw = MockDomesticQuoteOutput()
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)

        assert quote.open == Decimal("67100")
        assert quote.high == Decimal("67500")
        assert quote.low == Decimal("66800")
        assert quote.volume == 15_000_000
        assert quote.turnover == Decimal("1009500000000")
        assert quote.previous_volume == 12_000_000

    def test_limit_prices(self) -> None:
        raw = MockDomesticQuoteOutput()
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)

        assert quote.upper_limit == Decimal("87100")
        assert quote.lower_limit == Decimal("46900")

    def test_market_warning_none(self) -> None:
        raw = MockDomesticQuoteOutput(mrkt_warn_cls_code="00")
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)
        assert quote.market_warning == MarketWarning.NONE

    def test_market_warning_caution(self) -> None:
        raw = MockDomesticQuoteOutput(mrkt_warn_cls_code="01")
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)
        assert quote.market_warning == MarketWarning.CAUTION

    def test_market_warning_risk(self) -> None:
        raw = MockDomesticQuoteOutput(mrkt_warn_cls_code="03")
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)
        assert quote.market_warning == MarketWarning.RISK

    def test_trading_halted_false(self) -> None:
        raw = MockDomesticQuoteOutput(trht_yn=False)
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)
        assert quote.is_trading_halted is False

    def test_trading_halted_true(self) -> None:
        raw = MockDomesticQuoteOutput(trht_yn=True)
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)
        assert quote.is_trading_halted is True

    def test_domestic_has_no_orderable(self) -> None:
        raw = MockDomesticQuoteOutput()
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)
        assert quote.is_orderable is None

    def test_frozen_immutable(self) -> None:
        raw = MockDomesticQuoteOutput()
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)
        import pytest

        with pytest.raises(AttributeError):
            quote.price = Decimal("99999")  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Overseas mapping tests
# ---------------------------------------------------------------------------


class TestOverseasQuoteMapping:
    def test_basic_price_fields(self) -> None:
        raw = MockOverseasQuoteOutput()
        quote = map_overseas_quote(raw, "AAPL", Exchange.NASDAQ)

        assert quote.symbol == "AAPL"
        assert quote.exchange == Exchange.NASDAQ
        assert quote.price == Decimal("178.72")
        assert quote.previous_close == Decimal("177.56")
        assert quote.change == Decimal("1.16")
        assert quote.change_rate == Decimal("0.65")

    def test_change_sign_rise(self) -> None:
        raw = MockOverseasQuoteOutput(sign="2")
        quote = map_overseas_quote(raw, "AAPL", Exchange.NASDAQ)
        assert quote.change_sign == ChangeSign.RISE

    def test_change_sign_fall(self) -> None:
        raw = MockOverseasQuoteOutput(sign="5")
        quote = map_overseas_quote(raw, "AAPL", Exchange.NASDAQ)
        assert quote.change_sign == ChangeSign.FALL

    def test_volume_fields(self) -> None:
        raw = MockOverseasQuoteOutput()
        quote = map_overseas_quote(raw, "AAPL", Exchange.NASDAQ)

        assert quote.volume == 45_000_000
        assert quote.turnover == Decimal("8040000000")
        assert quote.previous_volume == 42_000_000

    def test_overseas_has_no_limits(self) -> None:
        raw = MockOverseasQuoteOutput()
        quote = map_overseas_quote(raw, "AAPL", Exchange.NASDAQ)
        assert quote.upper_limit is None
        assert quote.lower_limit is None

    def test_overseas_has_no_market_warning(self) -> None:
        raw = MockOverseasQuoteOutput()
        quote = map_overseas_quote(raw, "AAPL", Exchange.NASDAQ)
        assert quote.market_warning is None

    def test_overseas_has_no_trading_halted(self) -> None:
        raw = MockOverseasQuoteOutput()
        quote = map_overseas_quote(raw, "AAPL", Exchange.NASDAQ)
        assert quote.is_trading_halted is None

    def test_overseas_is_orderable(self) -> None:
        raw = MockOverseasQuoteOutput(ordy=True)
        quote = map_overseas_quote(raw, "AAPL", Exchange.NASDAQ)
        assert quote.is_orderable is True

    def test_overseas_not_orderable(self) -> None:
        raw = MockOverseasQuoteOutput(ordy=False)
        quote = map_overseas_quote(raw, "AAPL", Exchange.NASDAQ)
        assert quote.is_orderable is False

    def test_open_high_low_zero_for_overseas(self) -> None:
        """Overseas basic quote does not provide OHLC; defaults to Decimal(0)."""
        raw = MockOverseasQuoteOutput()
        quote = map_overseas_quote(raw, "AAPL", Exchange.NASDAQ)
        assert quote.open == Decimal(0)
        assert quote.high == Decimal(0)
        assert quote.low == Decimal(0)


# ---------------------------------------------------------------------------
# Exchange enum tests
# ---------------------------------------------------------------------------


class TestExchangeEnum:
    def test_domestic_exchanges(self) -> None:
        assert Exchange.KRX.is_domestic is True
        assert Exchange.NXT.is_domestic is True

    def test_overseas_exchanges(self) -> None:
        assert Exchange.NYSE.is_overseas is True
        assert Exchange.NASDAQ.is_overseas is True
        assert Exchange.SEHK.is_overseas is True
        assert Exchange.TSE.is_overseas is True

    def test_extended_hours(self) -> None:
        assert Exchange.NYSE_EXTENDED.is_extended_hours is True
        assert Exchange.NASDAQ_EXTENDED.is_extended_hours is True
        assert Exchange.AMEX_EXTENDED.is_extended_hours is True
        assert Exchange.NYSE.is_extended_hours is False
        assert Exchange.KRX.is_extended_hours is False

    def test_domestic_is_not_overseas(self) -> None:
        assert Exchange.KRX.is_overseas is False

    def test_overseas_is_not_domestic(self) -> None:
        assert Exchange.NASDAQ.is_domestic is False


# ---------------------------------------------------------------------------
# Quote model properties
# ---------------------------------------------------------------------------


class TestQuoteModel:
    def test_quote_is_frozen_dataclass(self) -> None:
        raw = MockDomesticQuoteOutput()
        quote = map_domestic_quote(raw, "005930", Exchange.KRX)
        assert hasattr(quote, "__dataclass_fields__")

    def test_quote_has_slots(self) -> None:
        assert hasattr(Quote, "__slots__")
