import types
from datetime import datetime, timedelta

import pytest

from vmkis.api.account import pending_order as po


def make_o(symbol, number, when):
    o = types.SimpleNamespace()
    o.symbol = symbol
    o.order_number = types.SimpleNamespace(branch="000", number=number)
    o.time_kst = when
    return o


def test_kissimplependingorders_indexing_and_order():
    now = datetime.utcnow()
    o1 = make_o("AAA", "1", now)
    o2 = make_o("BBB", "2", now - timedelta(days=1))

    coll = po.KisSimplePendingOrders(account_number="acct", orders=[o1, o2])

    # list is sorted reverse by time_kst in constructor
    assert coll.orders[0].time_kst >= coll.orders[1].time_kst

    assert coll[0] is coll.orders[0]
    assert coll["BBB"].symbol == "BBB"

    with pytest.raises(IndexError):
        _ = coll[999]

    assert coll.order("AAA") is not None
    assert coll.order("NOPE") is None

    assert len(coll) == 2
    assert list(iter(coll)) == coll.orders


def test_integration_pending_orders_merges_and_sorts():
    now = datetime.utcnow()
    a1 = make_o("A", "1", now)
    b1 = make_o("B", "2", now - timedelta(hours=1))
    part1 = types.SimpleNamespace(orders=[b1])
    part2 = types.SimpleNamespace(orders=[a1])

    integ = po.KisIntegrationPendingOrders(object(), "acct", part1, part2)

    # merged and sorted reverse by time_kst
    assert len(integ.orders) == 2
    assert integ.orders[0].time_kst >= integ.orders[1].time_kst


def test_domestic_pending_orders_raises_on_virtual():
    class FakeKis:
        def __init__(self):
            self.paper = True

    with pytest.raises(NotImplementedError):
        po.domestic_pending_orders(FakeKis(), account="123")


def test_foreign_pending_orders_uses_foreign_map_and_calls_internal(monkeypatch):
    # ensure foreign_pending_orders calls _foreign_pending_orders for each mapped market
    called = []

    def fake_internal(kis, account, market=None, page=None, continuous=True):
        called.append(market)
        return types.SimpleNamespace(orders=[1])

    monkeypatch.setattr(po, "_foreign_pending_orders", fake_internal)

    res = po.foreign_pending_orders(object(), account="acct", country="US")
    # US maps to ['NASDAQ'] so our fake_internal should be called with that market
    assert called[0] == "NASDAQ"
    assert hasattr(res, "orders")


def test_kis_pending_order_base_properties():
    """Test KisPendingOrderBase property aliases."""
    from decimal import Decimal

    order = types.SimpleNamespace(
        unit_price=Decimal("50000"), quantity=100, executed_quantity=60, orderable_quantity=40, price=Decimal("50000")
    )

    # Create instance
    pending_order = object.__new__(po.KisPendingOrderBase)
    pending_order.unit_price = order.unit_price
    pending_order.quantity = order.quantity
    pending_order.executed_quantity = order.executed_quantity
    pending_order.orderable_quantity = order.orderable_quantity
    pending_order.price = order.price

    # Test property aliases
    assert pending_order.order_price == Decimal("50000")
    assert pending_order.qty == 100
    assert pending_order.executed_qty == 60
    assert pending_order.orderable_qty == 40
    assert pending_order.pending_quantity == 40  # quantity - executed_quantity
    assert pending_order.pending_qty == 40
    assert pending_order.executed_amount == Decimal("3000000")  # 60 * 50000


def test_kis_pending_order_base_executed_amount_with_none_price():
    """Test executed_amount when price is None."""
    from decimal import Decimal

    pending_order = object.__new__(po.KisPendingOrderBase)
    pending_order.executed_quantity = 100
    pending_order.price = None

    assert pending_order.executed_amount == Decimal(0)


def test_kis_pending_order_base_pending_property():
    """Test pending property returns True."""
    pending_order = object.__new__(po.KisPendingOrderBase)
    assert pending_order.pending is True


def test_kis_pending_order_base_pending_order_property():
    """Test pending_order property returns self."""
    pending_order = object.__new__(po.KisPendingOrderBase)
    assert pending_order.pending_order is pending_order


def test_kis_pending_orders_base_getitem_by_index():
    """Test __getitem__ with integer index."""
    orders_list = [make_o("005930", "1", datetime.utcnow()), make_o("AAPL", "2", datetime.utcnow())]

    pending_orders = object.__new__(po.KisPendingOrdersBase)
    pending_orders.orders = orders_list

    assert pending_orders[0].symbol == "005930"
    assert pending_orders[1].symbol == "AAPL"


def test_kis_pending_orders_base_getitem_by_symbol():
    """Test __getitem__ with symbol string."""
    orders_list = [make_o("005930", "1", datetime.utcnow()), make_o("AAPL", "2", datetime.utcnow())]

    pending_orders = object.__new__(po.KisPendingOrdersBase)
    pending_orders.orders = orders_list

    assert pending_orders["005930"].order_number.number == "1"
    assert pending_orders["AAPL"].order_number.number == "2"


def test_kis_pending_orders_base_getitem_keyerror():
    """Test __getitem__ raises KeyError for non-existent key."""
    orders_list = [make_o("005930", "1", datetime.utcnow())]

    pending_orders = object.__new__(po.KisPendingOrdersBase)
    pending_orders.orders = orders_list

    with pytest.raises(KeyError):
        _ = pending_orders["NONEXISTENT"]


def test_kis_pending_orders_base_order_by_symbol():
    """Test order() method with symbol."""
    orders_list = [make_o("005930", "1", datetime.utcnow()), make_o("AAPL", "2", datetime.utcnow())]

    pending_orders = object.__new__(po.KisPendingOrdersBase)
    pending_orders.orders = orders_list

    result = pending_orders.order("005930")
    assert result is not None
    assert result.order_number.number == "1"

    # Non-existent symbol returns None
    result = pending_orders.order("NONEXISTENT")
    assert result is None


def test_kis_pending_orders_base_len():
    """Test __len__ method."""
    orders_list = [
        make_o("005930", "1", datetime.utcnow()),
        make_o("AAPL", "2", datetime.utcnow()),
        make_o("MSFT", "3", datetime.utcnow()),
    ]

    pending_orders = object.__new__(po.KisPendingOrdersBase)
    pending_orders.orders = orders_list

    assert len(pending_orders) == 3


def test_kis_pending_orders_base_iter():
    """Test __iter__ method."""
    orders_list = [make_o("005930", "1", datetime.utcnow()), make_o("AAPL", "2", datetime.utcnow())]

    pending_orders = object.__new__(po.KisPendingOrdersBase)
    pending_orders.orders = orders_list

    symbols = [order.symbol for order in pending_orders]
    assert symbols == ["005930", "AAPL"]


def test_kis_pending_order_base_equality():
    """Test __eq__ method compares order_number."""
    order1 = object.__new__(po.KisPendingOrderBase)
    order1.order_number = types.SimpleNamespace(branch="000", number="123")

    order2 = object.__new__(po.KisPendingOrderBase)
    order2.order_number = types.SimpleNamespace(branch="000", number="123")

    # Should be equal if order_number is equal
    assert order1 == order1.order_number
    assert order1 == order2.order_number


def test_kis_pending_order_base_hash():
    """Test __hash__ method uses order_number."""

    # Create a hashable mock order number
    class MockOrderNumber:
        def __init__(self, branch, number):
            self.branch = branch
            self.number = number

        def __hash__(self):
            return hash((self.branch, self.number))

        def __eq__(self, other):
            return self.branch == other.branch and self.number == other.number

    order = object.__new__(po.KisPendingOrderBase)
    order.order_number = MockOrderNumber("000", "123")

    # Should be hashable
    assert isinstance(hash(order), int)
    assert hash(order) == hash(order.order_number)


def test_kis_pending_order_base_deprecated_from_number(monkeypatch):
    """Test deprecated from_number static method."""
    from vmkis.client.account import KisAccountNumber

    mock_kis = types.SimpleNamespace()
    account = KisAccountNumber("12345678-01")

    # Test that from_number delegates to KisSimpleOrderNumber.from_number
    result = po.KisPendingOrderBase.from_number(
        kis=mock_kis, symbol="005930", market="KRX", account_number=account, branch="00001", number="12345"
    )

    assert result is not None
    assert result.symbol == "005930"
    assert result.market == "KRX"


def test_kis_pending_order_base_deprecated_from_order(monkeypatch):
    """Test deprecated from_order static method."""
    from vmkis.client.account import KisAccountNumber
    from vmkis.utils.timezone import TIMEZONE

    mock_kis = types.SimpleNamespace()
    account = KisAccountNumber("12345678-01")
    time_kst = datetime.now(TIMEZONE)

    # Test that from_order delegates to KisSimpleOrder.from_order
    result = po.KisPendingOrderBase.from_order(
        kis=mock_kis,
        symbol="005930",
        market="KRX",
        account_number=account,
        branch="00001",
        number="12345",
        time_kst=time_kst,
    )

    assert result is not None
    assert result.symbol == "005930"
    assert result.market == "KRX"


def test_kis_domestic_pending_order_pre_init():
    """Test KisDomesticPendingOrder.__pre_init__ sets time correctly."""

    from vmkis.utils.timezone import TIMEZONE

    order = object.__new__(po.KisDomesticPendingOrder)
    order.__data__ = {"ord_tmd": "093000", "ord_dvsn_cd": "00", "ord_gno_brno": "00001", "odno": "12345"}

    data = {
        "ord_tmd": "093000",
        "ord_dvsn_cd": "00",
        "ord_gno_brno": "00001",
        "odno": "12345",
        "pdno": "005930",
        "sll_buy_dvsn_cd": "02",
        "ord_unpr": "50000",
        "ord_qty": "10",
        "tot_ccld_qty": "5",
        "psbl_qty": "5",
    }

    # Mock super().__pre_init__
    order.__pre_init__(data)

    # Should have set time_kst and time
    assert order.time_kst.hour == 9
    assert order.time_kst.minute == 30
    assert order.time_kst.tzinfo == TIMEZONE


def test_kis_domestic_pending_order_post_init():
    """Test KisDomesticPendingOrder.__post_init__ resolves order condition."""
    from decimal import Decimal

    order = object.__new__(po.KisDomesticPendingOrder)
    order.__data__ = {"ord_dvsn_cd": "01"}  # Market order code
    order.unit_price = Decimal("0")
    order.condition = None
    order.execution = None

    order.__post_init__()

    # Market order (01) should set has_price=False, so unit_price should be None
    assert order.unit_price is None


def test_kis_domestic_pending_order_post_init_with_price():
    """Test KisDomesticPendingOrder.__post_init__ keeps price for limit orders."""
    from decimal import Decimal

    order = object.__new__(po.KisDomesticPendingOrder)
    order.__data__ = {"ord_dvsn_cd": "00"}  # Limit order code
    order.unit_price = Decimal("50000")
    order.condition = None
    order.execution = None

    order.__post_init__()

    # Limit order (00) should keep the price
    assert order.unit_price == Decimal("50000")
    assert order.condition is None


def test_kis_foreign_pending_order_pre_init():
    """Test KisForeignPendingOrder.__pre_init__ sets time_kst correctly."""
    from vmkis.utils.timezone import TIMEZONE

    order = object.__new__(po.KisForeignPendingOrder)
    order.__data__ = {"ord_tmd": "153000", "ovrs_excg_cd": "NASD", "ord_gno_brno": "00001", "odno": "12345"}

    data = {
        "ord_tmd": "153000",
        "ovrs_excg_cd": "NASD",
        "ord_gno_brno": "00001",
        "odno": "12345",
        "pdno": "AAPL",
        "sll_buy_dvsn_cd": "02",
        "ft_ccld_unpr3": "150.00",
        "ft_ord_unpr3": "150.50",
        "ft_ord_qty": "10",
        "ft_ccld_qty": "5",
        "nccs_qty": "5",
        "rjct_rson": "",
        "rjct_rson_name": "",
    }

    order.__pre_init__(data)

    # Should have set time_kst
    assert order.time_kst.hour == 15
    assert order.time_kst.minute == 30
    assert order.time_kst.tzinfo == TIMEZONE


def test_kis_foreign_pending_order_post_init_timezone_conversion():
    """Test KisForeignPendingOrder.__post_init__ converts timezone."""

    from vmkis.api.stock.market import get_market_timezone
    from vmkis.utils.timezone import TIMEZONE

    order = object.__new__(po.KisForeignPendingOrder)
    order.__data__ = {"ovrs_excg_cd": "NASD"}
    order.time_kst = datetime.now(TIMEZONE)
    order.timezone = get_market_timezone("NASDAQ")
    order.unit_price = "150.00"

    order.__post_init__()

    # Should have converted time to local timezone
    assert order.time is not None
    assert order.time.tzinfo is not None


def test_kis_foreign_pending_order_post_init_none_unit_price():
    """Test KisForeignPendingOrder.__post_init__ handles empty unit_price."""
    from vmkis.utils.timezone import TIMEZONE

    order = object.__new__(po.KisForeignPendingOrder)
    order.__data__ = {"ovrs_excg_cd": "NASD"}
    order.time_kst = datetime.now(TIMEZONE)
    order.timezone = TIMEZONE
    order.unit_price = ""  # Empty string

    order.__post_init__()

    # Empty string should be converted to None
    assert order.unit_price is None


def test_pending_orders_kr_country(monkeypatch):
    """Test pending_orders with country='KR' calls domestic_pending_orders."""
    from vmkis.client.account import KisAccountNumber

    called = []

    def mock_domestic(kis, account):
        called.append("domestic")
        return types.SimpleNamespace(orders=[])

    monkeypatch.setattr(po, "domestic_pending_orders", mock_domestic)

    mock_kis = types.SimpleNamespace(paper=False)
    account = KisAccountNumber("12345678-01")

    result = po.pending_orders(mock_kis, account, country="KR")

    assert "domestic" in called
    assert hasattr(result, "orders")


def test_pending_orders_foreign_country(monkeypatch):
    """Test pending_orders with foreign country calls foreign_pending_orders."""
    from vmkis.client.account import KisAccountNumber

    called = []

    def mock_foreign(kis, account, country=None):
        called.append(("foreign", country))
        return types.SimpleNamespace(orders=[])

    monkeypatch.setattr(po, "foreign_pending_orders", mock_foreign)

    mock_kis = types.SimpleNamespace(paper=False)
    account = KisAccountNumber("12345678-01")

    result = po.pending_orders(mock_kis, account, country="US")

    assert ("foreign", "US") in called
    assert hasattr(result, "orders")


def test_pending_orders_integration_none_country_not_virtual(monkeypatch):
    """Test pending_orders with None country and not paper returns integration."""
    from vmkis.client.account import KisAccountNumber

    def mock_domestic(kis, account):
        return types.SimpleNamespace(orders=[make_o("A", "1", datetime.utcnow())])

    def mock_foreign(kis, account):
        return types.SimpleNamespace(orders=[make_o("B", "2", datetime.utcnow())])

    monkeypatch.setattr(po, "domestic_pending_orders", mock_domestic)
    monkeypatch.setattr(po, "foreign_pending_orders", mock_foreign)

    mock_kis = types.SimpleNamespace(paper=False)
    account = KisAccountNumber("12345678-01")

    result = po.pending_orders(mock_kis, account, country=None)

    # Should be KisIntegrationPendingOrders with both domestic and foreign
    assert len(result.orders) == 2


def test_pending_orders_virtual(monkeypatch):
    """Test pending_orders with paper=True only calls foreign_pending_orders."""
    from vmkis.client.account import KisAccountNumber

    called = []

    def mock_foreign(kis, account, country=None):
        called.append("foreign")
        return types.SimpleNamespace(orders=[])

    monkeypatch.setattr(po, "foreign_pending_orders", mock_foreign)

    mock_kis = types.SimpleNamespace(paper=True)
    account = KisAccountNumber("12345678-01")

    result = po.pending_orders(mock_kis, account, country=None)

    # Virtual should only call foreign
    assert "foreign" in called
    assert hasattr(result, "orders")


def test_account_pending_orders_delegates():
    """Test account_pending_orders delegates to pending_orders."""
    from vmkis.client.account import KisAccountNumber

    mock_kis = types.SimpleNamespace(paper=False)
    account = KisAccountNumber("12345678-01")

    mock_account = types.SimpleNamespace(kis=mock_kis, account_number=account)

    # This will fail at fetch, but we're just testing delegation
    with pytest.raises(AttributeError):
        po.account_pending_orders(mock_account, country="US")


def test_account_product_pending_orders_filters_by_symbol(monkeypatch):
    """Test account_product_pending_orders filters orders by symbol and market."""
    from vmkis.client.account import KisAccountNumber

    mock_kis = types.SimpleNamespace(paper=False)
    account = KisAccountNumber("12345678-01")

    # Create mock orders
    order1 = make_o("005930", "1", datetime.utcnow())
    order1.market = "KRX"

    order2 = make_o("AAPL", "2", datetime.utcnow())
    order2.market = "NASDAQ"

    order3 = make_o("005930", "3", datetime.utcnow())
    order3.market = "KRX"

    def mock_pending_orders(kis, account, country):
        return types.SimpleNamespace(orders=[order1, order2, order3])

    monkeypatch.setattr(po, "pending_orders", mock_pending_orders)

    mock_product = types.SimpleNamespace(kis=mock_kis, account_number=account, symbol="005930", market="KRX")

    result = po.account_product_pending_orders(mock_product)

    # Should only have orders matching symbol and market
    assert len(result.orders) == 2
    assert all(order.symbol == "005930" and order.market == "KRX" for order in result.orders)


def test_foreign_country_market_map():
    """Test FOREIGN_COUNTRY_MARKET_MAP contains expected mappings."""
    assert None in po.FOREIGN_COUNTRY_MARKET_MAP
    assert "US" in po.FOREIGN_COUNTRY_MARKET_MAP
    assert "HK" in po.FOREIGN_COUNTRY_MARKET_MAP
    assert "CN" in po.FOREIGN_COUNTRY_MARKET_MAP
    assert "JP" in po.FOREIGN_COUNTRY_MARKET_MAP
    assert "VN" in po.FOREIGN_COUNTRY_MARKET_MAP

    # US maps to NASDAQ
    assert po.FOREIGN_COUNTRY_MARKET_MAP["US"] == ["NASDAQ"]

    # CN maps to both SSE and SZSE
    assert "SSE" in po.FOREIGN_COUNTRY_MARKET_MAP["CN"]
    assert "SZSE" in po.FOREIGN_COUNTRY_MARKET_MAP["CN"]


def test_kis_pending_order_base_branch_property():
    """Test branch property delegates to order_number.branch."""
    order = object.__new__(po.KisPendingOrderBase)
    order.order_number = types.SimpleNamespace(branch="00001", number="12345")

    assert order.branch == "00001"


def test_kis_pending_order_base_number_property():
    """Test number property delegates to order_number.number."""
    order = object.__new__(po.KisPendingOrderBase)
    order.order_number = types.SimpleNamespace(branch="00001", number="12345")

    assert order.number == "12345"


def test_kis_domestic_pending_order_kis_post_init():
    """Test KisDomesticPendingOrder.__kis_post_init__ creates order_number."""
    from vmkis.client.account import KisAccountNumber
    from vmkis.utils.timezone import TIMEZONE

    mock_kis = types.SimpleNamespace()
    account = KisAccountNumber("12345678-01")

    order = object.__new__(po.KisDomesticPendingOrder)
    order.__data__ = {"ord_gno_brno": "00001", "odno": "12345"}
    order.kis = mock_kis
    order.symbol = "005930"
    order.market = "KRX"
    order.account_number = account
    order.time_kst = datetime.now(TIMEZONE)

    # Call __kis_post_init__ which creates order_number from __data__
    order.__kis_post_init__()

    # Should have created order_number
    assert order.order_number is not None
    assert order.order_number.symbol == "005930"
    assert order.order_number.branch == "00001"
    assert order.order_number.number == "12345"


def test_kis_foreign_pending_order_kis_post_init():
    """Test KisForeignPendingOrder.__kis_post_init__ creates order_number."""
    from vmkis.client.account import KisAccountNumber
    from vmkis.utils.timezone import TIMEZONE

    mock_kis = types.SimpleNamespace()
    account = KisAccountNumber("12345678-01")

    order = object.__new__(po.KisForeignPendingOrder)
    order.__data__ = {"ord_gno_brno": "00001", "odno": "12345"}
    order.kis = mock_kis
    order.symbol = "AAPL"
    order.market = "NASDAQ"
    order.account_number = account
    order.time_kst = datetime.now(TIMEZONE)

    # Call __kis_post_init__ which creates order_number from __data__
    order.__kis_post_init__()

    # Should have created order_number
    assert order.order_number is not None
    assert order.order_number.symbol == "AAPL"
    assert order.order_number.market == "NASDAQ"


def test_kis_domestic_pending_orders_post_init():
    """Test KisDomesticPendingOrders.__post_init__ sets account_number on orders."""
    from vmkis.client.account import KisAccountNumber

    account = KisAccountNumber("12345678-01")

    orders_instance = object.__new__(po.KisDomesticPendingOrders)
    orders_instance.account_number = account

    # Create mock orders
    order1 = types.SimpleNamespace()
    order2 = types.SimpleNamespace()
    orders_instance.orders = [order1, order2]

    orders_instance.__post_init__()

    # Should have set account_number on all orders
    assert order1.account_number == account
    assert order2.account_number == account


def test_kis_domestic_pending_orders_kis_post_init(monkeypatch):
    """Test KisDomesticPendingOrders.__kis_post_init__ spreads kis."""
    from vmkis.client.account import KisAccountNumber

    account = KisAccountNumber("12345678-01")

    orders_instance = object.__new__(po.KisDomesticPendingOrders)
    orders_instance.account_number = account
    orders_instance.orders = [types.SimpleNamespace(), types.SimpleNamespace()]

    # Mock super().__kis_post_init__ and _kis_spread
    monkeypatch.setattr(po.KisPaginationAPIResponse, "__kis_post_init__", lambda self: None)

    spread_called = []
    orders_instance._kis_spread = lambda orders: spread_called.append(orders)

    orders_instance.__kis_post_init__()

    # Should have called _kis_spread with orders
    assert len(spread_called) == 1


def test_kis_foreign_pending_orders_post_init():
    """Test KisForeignPendingOrders.__post_init__ sets account_number on orders."""
    from vmkis.client.account import KisAccountNumber

    account = KisAccountNumber("12345678-01")

    orders_instance = object.__new__(po.KisForeignPendingOrders)
    orders_instance.account_number = account

    # Create mock orders
    order1 = types.SimpleNamespace()
    order2 = types.SimpleNamespace()
    orders_instance.orders = [order1, order2]

    orders_instance.__post_init__()

    # Should have set account_number on all orders
    assert order1.account_number == account
    assert order2.account_number == account


def test_kis_foreign_pending_orders_kis_post_init(monkeypatch):
    """Test KisForeignPendingOrders.__kis_post_init__ spreads kis."""
    from vmkis.client.account import KisAccountNumber

    account = KisAccountNumber("12345678-01")

    orders_instance = object.__new__(po.KisForeignPendingOrders)
    orders_instance.account_number = account
    orders_instance.orders = [types.SimpleNamespace(), types.SimpleNamespace()]

    # Mock super().__kis_post_init__ and _kis_spread
    monkeypatch.setattr(po.KisPaginationAPIResponse, "__kis_post_init__", lambda self: None)

    spread_called = []
    orders_instance._kis_spread = lambda orders: spread_called.append(orders)

    orders_instance.__kis_post_init__()

    # Should have called _kis_spread with orders
    assert len(spread_called) == 1
