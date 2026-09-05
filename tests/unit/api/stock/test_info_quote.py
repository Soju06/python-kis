from vmkis.api.stock import info as info_mod
from vmkis.api.stock import quote as quote_mod


def test_info_empty_symbol_raises():
    """`info()` should validate that symbol is provided and raise ValueError otherwise."""
    fake = object()
    try:
        # symbol is empty -> should raise before touching `self`
        info_mod.info(fake, "")
    except ValueError as e:
        assert "종목 코드를 입력해주세요" in str(e)
    else:
        raise AssertionError("Expected ValueError for empty symbol")


def test_quote_maps_and_validation():
    """Verify basic mapping constants and empty symbol validation in quote APIs."""
    # mapping dicts exist and map expected keys
    assert "0" in quote_mod.STOCK_SIGN_TYPE_MAP
    assert "00" in quote_mod.STOCK_RISK_TYPE_MAP

    fake = object()
    try:
        quote_mod.domestic_quote(fake, "")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for empty symbol in domestic_quote")
