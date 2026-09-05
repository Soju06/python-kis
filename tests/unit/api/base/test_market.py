from vmkis.api.base import market as mb


def test_market_name_calls_get_market_name(monkeypatch):
    monkeypatch.setattr("vmkis.api.stock.market.get_market_name", lambda m: f"NAME-{m}")

    m = mb.KisMarketBase()
    m.market = "KRX"

    assert m.market_name == "NAME-KRX"


def test_foreign_and_domestic_and_currency(monkeypatch):
    # patch MARKET_TYPE_MAP to control foreign/domestic behavior
    monkeypatch.setattr("vmkis.api.stock.info.MARKET_TYPE_MAP", {"KRX": ["KRX"]}, raising=False)

    m = mb.KisMarketBase()
    m.market = "KRX"
    # KRX is in MARKET_TYPE_MAP['KRX'] so foreign should be False
    assert m.foreign is False
    assert m.domestic is True

    # other market => foreign True
    m.market = "NASDAQ"
    assert m.foreign is True
    assert m.domestic is False

    # currency property calls get_market_currency
    monkeypatch.setattr("vmkis.api.stock.market.get_market_currency", lambda x: "USD")
    assert m.currency == "USD"
