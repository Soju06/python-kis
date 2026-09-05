from decimal import Decimal
from types import SimpleNamespace

from vmkis.api.stock import order_book


def test_orderbook_item_equality_and_iter():
    """KisOrderbookItemBase equality and iteration return expected tuples."""
    a = order_book.KisOrderbookItemBase(Decimal("1.23"), 100)
    b = order_book.KisOrderbookItemBase(Decimal("1.23"), 100)
    c = order_book.KisOrderbookItemBase(Decimal("2.00"), 50)

    assert a == b
    assert not (a == c)

    it = iter(a)
    assert next(it) == Decimal("1.23")
    assert next(it) == 100


def test_domestic_and_foreign_orderbook_empty_symbol_raises():
    """domestic_orderbook and foreign_orderbook validate symbol argument."""
    fake = SimpleNamespace()
    try:
        order_book.domestic_orderbook(fake, "")
    except ValueError as e:
        # implementation message has no space between words
        assert "종목" in str(e) and "입력" in str(e)
    else:
        raise AssertionError("Expected ValueError for empty symbol")

    try:
        order_book.foreign_orderbook(fake, "NASDAQ", "")
    except ValueError as e:
        assert "종목" in str(e) and "입력" in str(e)
    else:
        raise AssertionError("Expected ValueError for empty symbol")


def test_orderbook_dispatch_calls_fetch_for_domestic_and_foreign():
    """`orderbook` dispatches to the appropriate fetch call on the kis client."""
    calls = {}

    def fetch_domestic(path, api=None, params=None, response_type=None, domain=None):
        calls["domestic"] = (path, api, params)
        return "domestic-result"

    def fetch_foreign(path, api=None, params=None, response_type=None, domain=None):
        calls["foreign"] = (path, api, params)
        return "foreign-result"

    kis_dom = SimpleNamespace(fetch=fetch_domestic)
    res_dom = order_book.orderbook(kis_dom, "KRX", "SYM")
    assert res_dom == "domestic-result"
    assert "domestic" in calls

    kis_for = SimpleNamespace(fetch=fetch_foreign)
    res_for = order_book.orderbook(kis_for, "NASDAQ", "SYM")
    assert res_for == "foreign-result"
    assert "foreign" in calls
