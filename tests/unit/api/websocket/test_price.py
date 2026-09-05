from vmkis.api.websocket import price


class FakeTicket:
    def __init__(self, id, key):
        self.id = id
        self.key = key

    def unsubscribe(self):
        self.unsubscribed = True


class FakeClient:
    def __init__(self):
        self.calls = []

    def on(self, **kwargs):
        # return a simple ticket capturing id and key
        t = FakeTicket(kwargs.get("id"), kwargs.get("key"))
        self.calls.append(kwargs)
        return t


def test_build_and_parse_foreign_realtime_symbol_roundtrip():
    """build_foreign_realtime_symbol and parse_foreign_realtime_symbol roundtrip for D/R prefixes."""
    symbol = "AAPL"
    market = "NASDAQ"

    s = price.build_foreign_realtime_symbol(market=market, symbol=symbol, extended=False)
    m, cond, sym = price.parse_foreign_realtime_symbol(s)
    assert sym == symbol
    assert m == market
    assert cond is None

    s2 = price.build_foreign_realtime_symbol(market=market, symbol=symbol, extended=True)
    m2, cond2, sym2 = price.parse_foreign_realtime_symbol(s2)
    assert sym2 == symbol
    assert m2 == market
    assert cond2 == "extended"


def test_parse_foreign_realtime_symbol_invalid_raises():
    """Invalid prefix to parse_foreign_realtime_symbol raises ValueError."""
    try:
        price.parse_foreign_realtime_symbol("XZZAAPL")
    except ValueError as e:
        assert "Invalid foreign realtime symbol" in str(e)
    else:
        raise AssertionError("Expected ValueError for invalid symbol")


def test_on_price_dispatch_for_domestic_and_foreign():
    """on_price dispatches to websocket.on with correct id and key for KRX and foreign markets."""
    fake = FakeClient()
    # domestic
    ticket_dom = price.on_price(fake, "KRX", "SYM", lambda *_: None)
    assert ticket_dom.id == "H0STCNT0"
    assert ticket_dom.key == "SYM"

    # foreign
    ticket_for = price.on_price(fake, "NASDAQ", "AAPL", lambda *_: None, extended=True)
    assert ticket_for.id == "HDFSCNT0"
    # key should be built and start with 'R' or 'D'
    assert isinstance(ticket_for.key, str) and ticket_for.key[0] in ("R", "D")


def test_on_product_price_forwarding():
    """on_product_price forwards to on_price using the product's kis.websocket."""

    class FakeProduct:
        pass

    prod = FakeProduct()
    prod.market = "KRX"
    prod.symbol = "XYZ"
    prod.kis = type("K", (), {"websocket": FakeClient()})()

    ticket = price.on_product_price(prod, lambda *_: None)
    assert ticket.id == "H0STCNT0"
    assert ticket.key == "XYZ"
