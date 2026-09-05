from zoneinfo import ZoneInfo

from vmkis.api.stock import market


def test_get_market_code_and_type():
    """Ensure market codes round-trip between type and code."""
    assert market.get_market_code("NASDAQ") == "NASD"
    assert market.get_market_type("NASD") == "NASDAQ"


def test_name_currency_timezone():
    """Verify name, currency and timezone mappings for known markets."""
    assert market.get_market_name("KRX") == "국내"
    assert market.get_market_currency("NASDAQ") == "USD"
    tz = market.get_market_timezone("TYO")
    assert isinstance(tz, ZoneInfo)


def test_kismarkettype_transform_invalid():
    """KisMarketType.transform should raise ValueError for unknown codes."""
    kt = market.KisMarketType()
    try:
        kt.transform("UNKNOWN_CODE")
    except ValueError as e:
        assert "올바르지 않은 시장 종류입니다" in str(e)
    else:
        raise AssertionError("Expected ValueError for unknown market code")
