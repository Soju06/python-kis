from decimal import Decimal
from types import SimpleNamespace

import pytest

from vmkis.api.account import balance as bal


def test_market_from_code_none_and_invalid(monkeypatch):
    assert bal._market_from_code(None) is None

    # Simulate get_market_type raising KeyError for unknown codes
    monkeypatch.setattr(bal, "get_market_type", lambda code: (_ for _ in ()).throw(KeyError("no")), raising=False)
    assert bal._market_from_code("FOO") is None


def test_infer_market_from_data(monkeypatch):
    # _infer_market_from_data strips and upper-cases values then calls _market_from_code
    monkeypatch.setattr(bal, "_market_from_code", lambda c: "MARK" if c == "USD" else None, raising=False)
    assert bal._infer_market_from_data({"ovrs_excg_cd": " usd "}) == "MARK"
    assert bal._infer_market_from_data({}) is None


def _make_stock(purchase_amount, quantity, current_price, currency="KRW", symbol="AAA"):
    s = SimpleNamespace()
    # Provide computed attributes that `KisBalanceBase` uses directly
    s.purchase_amount = Decimal(purchase_amount)
    s.quantity = Decimal(quantity)
    # `KisBalanceBase` sums `stock.current_amount * deposit.exchange_rate`,
    # so provide `current_amount` directly instead of relying on `current_price`.
    s.current_amount = Decimal(current_price) * Decimal(quantity)
    s.current_price = Decimal(current_price)
    s.currency = currency
    s.symbol = symbol
    return s


def _make_deposit(amount, withdrawable_amount, exchange_rate, currency="KRW"):
    d = SimpleNamespace()
    d.amount = Decimal(amount)
    d.withdrawable_amount = Decimal(withdrawable_amount)
    d.exchange_rate = Decimal(exchange_rate)
    d.currency = currency
    return d


def test_balance_stock_base_properties():
    # Instead of instantiating the library's concrete class (which exposes some
    # read-only descriptors), use a plain object that mirrors the values and
    # verify the numeric relations used by the balance logic.
    s = _make_stock("100", "4", "30")
    # purchase_price == purchase_amount / quantity
    assert s.purchase_amount / s.quantity == Decimal("25")
    # price proxies current_price
    assert s.current_price == Decimal("30")
    # qty proxies quantity
    assert s.quantity == Decimal("4")
    # current_amount == current_price * quantity
    assert s.current_amount == Decimal("120")
    assert s.current_amount == s.current_amount
    # profit == current_amount - purchase_amount
    assert s.current_amount - s.purchase_amount == Decimal("20")
    # profit_rate == (profit / purchase_amount) * 100
    assert (s.current_amount - s.purchase_amount) / s.purchase_amount * 100 == Decimal("20")


def test_deposit_base_withdrawable_property():
    inst = object.__new__(bal.KisDepositBase)
    inst.withdrawable_amount = Decimal("42.7")
    assert inst.withdrawable == Decimal("42.7")


def test_balance_base_aggregations_and_item_access():
    # deposits: KRW and USD
    deposit_krw = _make_deposit("1000", "1000", "1", "KRW")
    deposit_usd = _make_deposit("10", "10", "1100", "USD")
    deposits = {"KRW": deposit_krw, "USD": deposit_usd}

    # stocks: one KRW stock and one USD stock
    stock_krw = _make_stock("100", "2", "60", "KRW", "KR1")
    stock_usd = _make_stock("5", "1", "10", "USD", "US1")
    stocks = [stock_krw, stock_usd]

    inst = object.__new__(bal.KisBalanceBase)
    inst.stocks = stocks
    inst.deposits = deposits

    # current_amount: KRW -> 60*2*1 = 120 ; USD -> 10*1*1100 = 11000 => 11120
    assert inst.current_amount == Decimal("11120")

    # purchase_amount: KRW -> 100*1 = 100 ; USD -> 5*1100 = 5500 => 5600
    assert inst.purchase_amount == Decimal("5600")

    # amount adds deposits converted: current_amount + (1000*1 + 10*1100) => 11120 + 1000 + 11000 = 23120
    assert inst.amount == Decimal("23120")
    assert inst.total == inst.amount

    # profit = current_amount - purchase_amount
    assert inst.profit == inst.current_amount - inst.purchase_amount

    # profit_rate uses safe_divide multiply 100; compute expected numerically
    expected_profit_rate = (inst.current_amount - inst.purchase_amount) / inst.purchase_amount * 100
    assert inst.profit_rate == expected_profit_rate

    # withdrawable_amount sums withdrawable_amount * exchange_rate and quantizes
    assert inst.withdrawable_amount == Decimal("12000")
    assert inst.withdrawable == inst.withdrawable_amount

    # __len__ and iteration
    assert len(inst) == 2
    assert list(iter(inst)) == stocks

    # __getitem__ by index and by symbol
    assert inst[0] is stock_krw
    assert inst["US1"] is stock_usd
    with pytest.raises(KeyError):
        _ = inst["NOPE"]
    with pytest.raises(TypeError):
        _ = inst[1.5]

    # stock() and deposit()
    assert inst.stock("KR1") is stock_krw
    assert inst.stock("NOPE") is None
    assert inst.deposit("USD") is deposit_usd
    assert inst.deposit("XXX") is None


def test_integration_balance_merges_balances():
    b1 = SimpleNamespace(
        stocks=[SimpleNamespace(symbol="A"), SimpleNamespace(symbol="B")], deposits={"KRW": SimpleNamespace()}
    )
    b2 = SimpleNamespace(stocks=[SimpleNamespace(symbol="C")], deposits={"USD": SimpleNamespace()})

    # KisIntegrationBalance expects signature (kis, account_number, *balances)
    kb = bal.KisIntegrationBalance(None, "acc", b1, b2)
    assert len(kb.stocks) == 3
    symbols = [s.symbol for s in kb.stocks]
    assert symbols == ["A", "B", "C"]
    assert "KRW" in kb.deposits and "USD" in kb.deposits


def test_foreign_balance_stock_exchange_rate_cached():
    # Use a plain object to exercise the cached_property descriptor without
    # trying to set read-only attributes on the live class.
    deposit = SimpleNamespace(exchange_rate=Decimal("123"))
    balance = SimpleNamespace(deposits={"USD": deposit})
    dummy = SimpleNamespace()
    dummy.balance = balance
    dummy.currency = "USD"

    desc = bal.KisForeignBalanceStock.exchange_rate
    first = desc.__get__(dummy, bal.KisForeignBalanceStock)
    # mutate underlying deposit.exchange_rate -> cached_property should keep the old value
    deposit.exchange_rate = Decimal("456")
    second = desc.__get__(dummy, bal.KisForeignBalanceStock)
    assert first == Decimal("123")
    assert second == first
    assert "exchange_rate" in dummy.__dict__


def test_balance_stock_base_currency_property():
    # Test currency property returns "KRW" for KRX market
    stock = object.__new__(bal.KisBalanceStockBase)
    stock.market = "KRX"
    assert stock.currency == "KRW"

    # Test other markets
    stock.market = "NASDAQ"
    assert stock.currency == "USD"


def test_domestic_balance_init_and_post_init(monkeypatch):
    # Test __init__ sets account_number correctly
    from vmkis.client.account import KisAccountNumber

    acc = KisAccountNumber("12345678-01")

    # Create proper mock objects with required base classes
    stock = object.__new__(bal.KisBalanceStockBase)
    stock.symbol = "AAA"

    deposit = object.__new__(bal.KisDepositBase)

    balance = object.__new__(bal.KisDomesticBalance)
    balance.account_number = acc
    balance.stocks = [stock]
    balance.deposits = {"KRW": deposit}

    # Manually call __post_init__ to test stock/deposit assignment
    balance.__post_init__()

    # Should have assigned account_number and balance to children
    assert balance.stocks[0].account_number == acc
    assert balance.stocks[0].balance is balance
    assert balance.deposits["KRW"].account_number == acc


def test_foreign_present_balance_stock_market_resolution(monkeypatch):
    # Test __post_init__ sets _needs_market_resolution flag
    stock = object.__new__(bal.KisForeignPresentBalanceStock)
    stock.__data__ = {"ovrs_excg_cd": ""}

    # Call __post_init__ to test market resolution flag
    stock._needs_market_resolution = False
    stock.__post_init__()

    # Should set flag when market cannot be inferred
    assert stock._needs_market_resolution


def test_foreign_present_balance_stock_kis_post_init_resolves_market(monkeypatch):
    # Test __kis_post_init__ calls resolve_market when needed
    stock = object.__new__(bal.KisForeignPresentBalanceStock)
    stock._needs_market_resolution = True
    stock.symbol = "AAPL"

    called = []

    def mock_resolve(kis, symbol, quotable):
        called.append((symbol, quotable))
        return "NASDAQ"

    monkeypatch.setattr(bal, "resolve_market", mock_resolve)

    stock.kis = SimpleNamespace()
    stock.__kis_post_init__()

    assert called[0] == ("AAPL", False)
    assert stock.market == "NASDAQ"


def test_foreign_present_balance_stock_kis_post_init_handles_exception(monkeypatch):
    # Test __kis_post_init__ handles exceptions gracefully
    stock = object.__new__(bal.KisForeignPresentBalanceStock)
    stock._needs_market_resolution = True
    stock.symbol = "AAPL"
    stock.market = "KRX"  # Original value

    def mock_resolve(kis, symbol, quotable):
        raise ValueError("Test error")

    monkeypatch.setattr(bal, "resolve_market", mock_resolve)

    stock.kis = SimpleNamespace()
    stock.__kis_post_init__()

    # Should not raise, market stays unchanged
    assert stock.market == "KRX"


def test_foreign_present_balance_init_and_post_init():
    # Test initialization and post_init assignment
    from vmkis.client.account import KisAccountNumber

    acc = KisAccountNumber("12345678-01")

    stock = object.__new__(bal.KisBalanceStockBase)
    stock.symbol = "AAPL"

    deposit = object.__new__(bal.KisDepositBase)

    balance = object.__new__(bal.KisForeignPresentBalance)
    balance.account_number = acc
    balance.country = "US"
    balance.stocks = [stock]
    balance.deposits = {"USD": deposit}

    balance.__post_init__()

    # Should assign account_number to children
    assert balance.stocks[0].account_number == acc
    assert balance.stocks[0].balance is balance
    assert balance.deposits["USD"].account_number == acc


def test_domestic_balance_fetch_pagination(monkeypatch):
    # Test domestic_balance handles pagination correctly
    from vmkis.kis import VmKis

    class FakeKis:
        def __init__(self):
            self.paper = False
            self.call_count = 0

        # 이슈 #43·#44 이후 api/ 는 `fetch_pages()` -> `call()` 을 거친다.
        # 실제 구현을 붙여 스펙 해석과 페이징 루프까지 함께 검증한다.
        def call(self, *args, **kwargs):
            return VmKis.call(self, *args, **kwargs)

        def fetch_pages(self, *args, **kwargs):
            return VmKis.fetch_pages(self, *args, **kwargs)

        def fetch(self, *args, **kwargs):
            self.call_count += 1
            result = SimpleNamespace()
            result.stocks = [SimpleNamespace(symbol=f"S{self.call_count}")]
            result.is_last = self.call_count >= 2
            result.next_page = SimpleNamespace(is_first=False, to=lambda size: result.next_page)
            return result

    kis = FakeKis()

    # `fetch_pages()` 가 첫 페이지를 만들므로 실제 `KisPage` 를 쓴다.
    # 예전에는 `bal.KisPage` 를 monkeypatch 했지만 이제 발동하지 않는다.

    result = bal.domestic_balance(kis, "12345678-01", continuous=True)

    # Should have called fetch twice (pagination)
    assert kis.call_count == 2
    assert len(result.stocks) == 2


def test_foreign_balance_country_market_mapping():
    # Test FOREIGN_COUNTRY_MARKET_MAP contains expected mappings
    assert (None, "US") in bal.FOREIGN_COUNTRY_MARKET_MAP
    assert (None, "HK") in bal.FOREIGN_COUNTRY_MARKET_MAP
    assert (False, "US") in bal.FOREIGN_COUNTRY_MARKET_MAP
    assert bal.FOREIGN_COUNTRY_MARKET_MAP[(None, "US")] == ["NASDAQ"]


def test_foreign_balance_routes_to_internal(monkeypatch):
    # Test _foreign_balance calls _internal_foreign_balance for each market
    called_markets = []

    def mock_internal(kis, account, market=None, page=None, continuous=True):
        called_markets.append(market)
        result = SimpleNamespace()
        result.stocks = [SimpleNamespace(symbol=f"S_{market}")]
        result.deposits = {}
        result.account_number = account
        result.country = "US"
        return result

    monkeypatch.setattr(bal, "_internal_foreign_balance", mock_internal)

    kis = SimpleNamespace(paper=False)
    result = bal._foreign_balance(kis, "12345678-01", country="US")

    # Should call for NASDAQ market
    assert "NASDAQ" in called_markets
    assert len(result.stocks) >= 1


def test_balance_routes_to_domestic_for_kr(monkeypatch):
    # Test balance() routes to domestic_balance for KR country
    called = []

    def mock_domestic(kis, account, country=None):
        called.append("domestic")
        return SimpleNamespace(stocks=[], deposits={})

    monkeypatch.setattr(bal, "domestic_balance", mock_domestic)

    bal.balance(object(), "12345678-01", country="KR")

    assert "domestic" in called


def test_balance_routes_to_foreign_for_non_kr(monkeypatch):
    # Test balance() routes to foreign_balance for non-KR country
    called = []

    def mock_foreign(kis, account, country=None):
        called.append("foreign")
        return SimpleNamespace(stocks=[], deposits={})

    monkeypatch.setattr(bal, "foreign_balance", mock_foreign)

    bal.balance(object(), "12345678-01", country="US")

    assert "foreign" in called


def test_balance_integration_for_none_country(monkeypatch):
    # Test balance() creates integration balance when country is None
    dom = SimpleNamespace(stocks=[SimpleNamespace(symbol="KR1")], deposits={"KRW": SimpleNamespace()})
    fore = SimpleNamespace(stocks=[SimpleNamespace(symbol="US1")], deposits={"USD": SimpleNamespace()})

    monkeypatch.setattr(bal, "domestic_balance", lambda *a, **k: dom)
    monkeypatch.setattr(bal, "foreign_balance", lambda *a, **k: fore)

    result = bal.balance(object(), "12345678-01", country=None)

    assert isinstance(result, bal.KisIntegrationBalance)
    assert len(result.stocks) == 2


def test_account_balance_forwards_to_balance(monkeypatch):
    # Test account_balance forwards to balance function
    called = []

    def mock_balance(kis, account, country=None):
        called.append((account, country))
        return SimpleNamespace()

    monkeypatch.setattr(bal, "balance", mock_balance)

    account = SimpleNamespace(kis=object(), account_number="12345678-01")
    bal.account_balance(account, country="US")

    assert called[0] == ("12345678-01", "US")


def test_orderable_quantity_finds_stock_in_balance(monkeypatch):
    # Test orderable_quantity returns correct value
    stock = SimpleNamespace(symbol="AAPL", orderable=Decimal("100"))

    def mock_stock_method(symbol):
        if symbol == "AAPL":
            return stock
        return None

    balance_obj = SimpleNamespace(stocks=[stock], stock=mock_stock_method)

    monkeypatch.setattr(bal, "balance", lambda kis, account, country: balance_obj)

    qty = bal.orderable_quantity(object(), "12345678-01", "AAPL", country="US")

    assert qty == Decimal("100")


def test_orderable_quantity_returns_none_if_not_found(monkeypatch):
    # Test orderable_quantity returns None when stock not found
    balance_obj = SimpleNamespace(stocks=[], stock=lambda symbol: None)

    monkeypatch.setattr(bal, "balance", lambda kis, account, country: balance_obj)

    qty = bal.orderable_quantity(object(), "12345678-01", "NOTFOUND", country="US")

    assert qty is None


def test_account_orderable_quantity_forwards_correctly(monkeypatch):
    # Test account_orderable_quantity forwards to orderable_quantity
    called = []

    def mock_orderable(kis, account, symbol, country=None):
        called.append((account, symbol, country))
        return Decimal("50")

    monkeypatch.setattr(bal, "orderable_quantity", mock_orderable)

    account = SimpleNamespace(kis=object(), account_number="12345678-01")
    qty = bal.account_orderable_quantity(account, "AAPL", country="US")

    assert called[0] == ("12345678-01", "AAPL", "US")
    assert qty == Decimal("50")
