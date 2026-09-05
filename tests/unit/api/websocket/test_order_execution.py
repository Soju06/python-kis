from types import SimpleNamespace

from vmkis.api.websocket import order_execution


class FakeTicket:
    def __init__(self):
        self.unsubscribed_callbacks = []

    def unsubscribe(self):
        self.unsubscribed = True


class FakeWebsocket:
    def __init__(self, name):
        self.name = name
        self.called = []

    def on(self, **kwargs):
        self.called.append(kwargs)
        return FakeTicket()


def test_on_execution_raises_when_no_appkey():
    """on_execution should raise if the client's appkey (or paper_appkey) is None."""
    client = SimpleNamespace(kis=SimpleNamespace(paper=False, appkey=None))
    try:
        order_execution.on_execution(client, lambda *_: None)
    except ValueError as e:
        assert "appkey" in str(e)
    else:
        raise AssertionError("Expected ValueError when appkey is None")


def test_on_execution_registers_domestic_and_foreign_and_links_unsubscribe():
    """on_execution registers two event handlers and links foreign unsubscribe to domestic callbacks."""
    # Create a kis object with appkey
    appkey = SimpleNamespace(id="key-id")
    kis = SimpleNamespace(paper=False, appkey=appkey)

    ws = FakeWebsocket("ws")
    # client has kis and on method as itself
    client = SimpleNamespace(kis=kis, on=ws.on)

    ticket = order_execution.on_execution(client, lambda *_: None)
    assert isinstance(ticket, FakeTicket)


def test_on_account_execution_forwards_to_on_execution():
    """on_account_execution should call on_execution using the account protocol's kis.websocket."""
    appkey = SimpleNamespace(id="k")
    ws = FakeWebsocket("w")
    kis = SimpleNamespace(paper=False, appkey=appkey, websocket=ws)
    # websocket should reference its parent kis (the production code expects self.kis on websocket)
    ws.kis = kis
    acct = SimpleNamespace(kis=kis)

    ticket = order_execution.on_account_execution(acct, lambda *_: None)
    assert isinstance(ticket, FakeTicket)


def test_domestic_execution_executed_amount_calculation():
    """Test executed_amount property calculates correctly."""
    from decimal import Decimal

    exec_obj = order_execution.KisDomesticRealtimeOrderExecution()
    exec_obj.executed_quantity = Decimal("100")
    exec_obj.price = Decimal("50000")

    assert exec_obj.executed_amount == Decimal("5000000")


def test_domestic_execution_executed_amount_with_zero_price():
    """Test executed_amount when price is None or 0."""
    from decimal import Decimal

    exec_obj = order_execution.KisDomesticRealtimeOrderExecution()
    exec_obj.executed_quantity = Decimal("100")
    exec_obj.price = None

    assert exec_obj.executed_amount == Decimal("0")


def test_foreign_execution_executed_amount_calculation():
    """Test executed_amount property for foreign execution."""
    from decimal import Decimal

    exec_obj = order_execution.KisForeignRealtimeOrderExecution()
    exec_obj.executed_quantity = Decimal("50")
    exec_obj.price = Decimal("148.50")

    assert exec_obj.executed_amount == Decimal("7425.00")


def test_domestic_pre_init_sets_canceled_flag():
    """Test __pre_init__ sets canceled flag when data[14] == '3'."""
    exec_obj = order_execution.KisDomesticRealtimeOrderExecution()
    # Create mock data with 23 elements (matching __fields__ length)
    data = [""] * 23
    data[14] = "3"  # ACPT_YN = 3 means canceled
    data[6] = "00"  # ODER_KIND for resolve_domestic_order_condition

    exec_obj.__pre_init__(data)

    assert exec_obj.canceled is True
    assert exec_obj.receipt is False


def test_domestic_pre_init_sets_receipt_flag():
    """Test __pre_init__ sets receipt flag when data[14] == '1'."""
    exec_obj = order_execution.KisDomesticRealtimeOrderExecution()
    data = [""] * 23
    data[14] = "1"  # ACPT_YN = 1 means receipt
    data[6] = "00"

    exec_obj.__pre_init__(data)

    assert exec_obj.canceled is False
    assert exec_obj.receipt is True


def test_foreign_pre_init_sets_canceled_flag():
    """Test __pre_init__ sets canceled flag for foreign execution."""
    exec_obj = order_execution.KisForeignRealtimeOrderExecution()
    data = [""] * 21
    data[13] = "3"  # ACPT_YN = 3 means canceled

    exec_obj.__pre_init__(data)

    assert exec_obj.canceled is True
    assert exec_obj.receipt is False


def test_foreign_pre_init_sets_receipt_flag():
    """Test __pre_init__ sets receipt flag for foreign execution."""
    exec_obj = order_execution.KisForeignRealtimeOrderExecution()
    data = [""] * 21
    data[13] = "1"  # ACPT_YN = 1 means receipt

    exec_obj.__pre_init__(data)

    assert exec_obj.canceled is False
    assert exec_obj.receipt is True


def test_foreign_post_init_price_decimal_adjustment():
    """Test __post_init__ adjusts price based on country decimal places."""
    from decimal import Decimal

    exec_obj = order_execution.KisForeignRealtimeOrderExecution()
    exec_obj.price = Decimal("1480100")  # Raw price from API
    exec_obj.market = "NASDAQ"  # US market, 4 decimal places
    exec_obj.quantity = Decimal("10")
    exec_obj.executed_quantity = Decimal("5")
    exec_obj.receipt = False

    data = [""] * 21
    data[6] = "2"  # Limit order with price

    exec_obj.__data__ = data
    exec_obj.__post_init__()

    # Should divide by 10^4 for US markets
    assert exec_obj.price == Decimal("148.0100")
    assert exec_obj.unit_price == Decimal("148.0100")


def test_foreign_post_init_market_order_no_unit_price():
    """Test __post_init__ sets unit_price to None for market orders."""
    from decimal import Decimal

    exec_obj = order_execution.KisForeignRealtimeOrderExecution()
    exec_obj.price = Decimal("1480100")
    exec_obj.market = "NYSE"
    exec_obj.quantity = Decimal("10")
    exec_obj.executed_quantity = Decimal("5")
    exec_obj.receipt = False

    data = [""] * 21
    data[6] = "1"  # Market order, no price

    exec_obj.__data__ = data
    exec_obj.__post_init__()

    assert exec_obj.price == Decimal("148.0100")
    assert exec_obj.unit_price is None
    assert exec_obj.condition is None


def test_foreign_post_init_with_moo_condition():
    """Test __post_init__ sets MOO condition correctly."""
    from decimal import Decimal

    exec_obj = order_execution.KisForeignRealtimeOrderExecution()
    exec_obj.price = Decimal("1000000")
    exec_obj.market = "NYSE"
    exec_obj.quantity = Decimal("10")
    exec_obj.executed_quantity = Decimal("10")
    exec_obj.receipt = False

    data = [""] * 21
    data[6] = "A"  # MOO order

    exec_obj.__data__ = data
    exec_obj.__post_init__()

    assert exec_obj.condition == "MOO"
    assert exec_obj.unit_price is None


def test_foreign_post_init_with_loo_condition():
    """Test __post_init__ sets LOO condition with price."""
    from decimal import Decimal

    exec_obj = order_execution.KisForeignRealtimeOrderExecution()
    exec_obj.price = Decimal("1000000")
    exec_obj.market = "NASDAQ"
    exec_obj.quantity = Decimal("10")
    exec_obj.executed_quantity = Decimal("10")
    exec_obj.receipt = False

    data = [""] * 21
    data[6] = "B"  # LOO order (limit on open)

    exec_obj.__data__ = data
    exec_obj.__post_init__()

    assert exec_obj.condition == "LOO"
    assert exec_obj.unit_price is not None


def test_foreign_post_init_negative_quantity_uses_executed():
    """Test __post_init__ uses executed_quantity when quantity is negative."""
    from decimal import Decimal

    exec_obj = order_execution.KisForeignRealtimeOrderExecution()
    exec_obj.price = Decimal("1000000")
    exec_obj.market = "TYO"  # Japan market, 1 decimal place
    exec_obj.quantity = Decimal("-1")  # Negative means use executed_quantity
    exec_obj.executed_quantity = Decimal("50")
    exec_obj.receipt = False

    data = [""] * 21
    data[6] = "2"

    exec_obj.__data__ = data
    exec_obj.__post_init__()

    assert exec_obj.quantity == Decimal("50")


def test_foreign_post_init_receipt_adjusts_quantities():
    """Test __post_init__ adjusts quantities for receipt orders."""
    from decimal import Decimal

    exec_obj = order_execution.KisForeignRealtimeOrderExecution()
    exec_obj.price = Decimal("1000000")
    exec_obj.market = "HKEX"  # Hong Kong, 3 decimal places
    exec_obj.quantity = Decimal("100")
    exec_obj.executed_quantity = Decimal("100")
    exec_obj.receipt = True

    data = [""] * 21
    data[6] = "2"

    exec_obj.__data__ = data
    exec_obj.__post_init__()

    # Receipt orders: quantity = executed_quantity, executed_quantity = 0
    assert exec_obj.quantity == Decimal("100")
    assert exec_obj.executed_quantity == Decimal("0")


def test_domestic_post_init_receipt_adjusts_quantities():
    """Test domestic __post_init__ adjusts quantities for receipt orders."""
    from decimal import Decimal

    exec_obj = order_execution.KisDomesticRealtimeOrderExecution()
    exec_obj.quantity = Decimal("200")
    exec_obj.executed_quantity = Decimal("200")
    exec_obj.receipt = True
    exec_obj._has_price = True
    exec_obj.unit_price = Decimal("50000")
    exec_obj.time = SimpleNamespace()

    # Mock astimezone
    exec_obj.time.astimezone = lambda tz: SimpleNamespace()

    exec_obj.__post_init__()

    assert exec_obj.quantity == Decimal("200")
    assert exec_obj.executed_quantity == Decimal("0")


def test_domestic_post_init_no_price_sets_unit_price_none():
    """Test domestic __post_init__ sets unit_price to None when _has_price is False."""
    from decimal import Decimal

    exec_obj = order_execution.KisDomesticRealtimeOrderExecution()
    exec_obj.quantity = Decimal("100")
    exec_obj.executed_quantity = Decimal("50")
    exec_obj.receipt = False
    exec_obj._has_price = False
    exec_obj.unit_price = Decimal("50000")
    exec_obj.time = SimpleNamespace()
    exec_obj.time.astimezone = lambda tz: SimpleNamespace()

    exec_obj.__post_init__()

    assert exec_obj.unit_price is None


def test_on_execution_with_virtual_appkey():
    """Test on_execution uses paper appkey in paper mode."""
    paper_appkey = SimpleNamespace(id="paper-key-id")
    ws = FakeWebsocket("ws")
    kis = SimpleNamespace(paper=True, appkey=None, paper_appkey=paper_appkey)
    ws.kis = kis
    client = SimpleNamespace(kis=kis, on=ws.on)

    ticket = order_execution.on_execution(client, lambda *_: None)

    assert isinstance(ticket, FakeTicket)
    # Should have registered with paper IDs
    assert len(ws.called) == 2
    assert ws.called[0]["id"] == "H0STCNI9"  # Domestic paper
    assert ws.called[1]["id"] == "H0GSCNI9"  # Foreign paper


def test_on_execution_with_real_appkey():
    """Test on_execution uses live appkey in production mode."""
    appkey = SimpleNamespace(id="live-key-id")
    ws = FakeWebsocket("ws")
    kis = SimpleNamespace(paper=False, appkey=appkey)
    ws.kis = kis
    client = SimpleNamespace(kis=kis, on=ws.on)

    ticket = order_execution.on_execution(client, lambda *_: None)

    assert isinstance(ticket, FakeTicket)
    # Should have registered with live IDs
    assert len(ws.called) == 2
    assert ws.called[0]["id"] == "H0STCNI0"  # Domestic live
    assert ws.called[1]["id"] == "H0GSCNI0"  # Foreign live


def test_on_execution_with_where_filter():
    """Test on_execution passes where filter to both registrations."""
    appkey = SimpleNamespace(id="key")
    ws = FakeWebsocket("ws")
    kis = SimpleNamespace(paper=False, appkey=appkey)
    ws.kis = kis
    client = SimpleNamespace(kis=kis, on=ws.on)

    def my_filter(*args):
        return True

    ticket = order_execution.on_execution(client, lambda *_: None, where=my_filter)  # noqa: F841 - 티켓을 붙잡지 않으면 GC가 구독을 해지한다

    assert ws.called[0]["where"] == my_filter
    assert ws.called[1]["where"] == my_filter


def test_on_execution_with_once_flag():
    """Test on_execution passes once flag to both registrations."""
    appkey = SimpleNamespace(id="key")
    ws = FakeWebsocket("ws")
    kis = SimpleNamespace(paper=False, appkey=appkey)
    ws.kis = kis
    client = SimpleNamespace(kis=kis, on=ws.on)

    ticket = order_execution.on_execution(client, lambda *_: None, once=True)  # noqa: F841 - 티켓을 붙잡지 않으면 GC가 구독을 해지한다

    assert ws.called[0]["once"] is True
    assert ws.called[1]["once"] is True


def test_on_account_execution_with_where_and_once():
    """Test on_account_execution forwards all parameters correctly."""
    appkey = SimpleNamespace(id="k")
    ws = FakeWebsocket("w")
    kis = SimpleNamespace(paper=False, appkey=appkey, websocket=ws)
    ws.kis = kis
    acct = SimpleNamespace(kis=kis)

    def my_filter(*args):
        return True

    ticket = order_execution.on_account_execution(acct, lambda *_: None, where=my_filter, once=True)

    assert isinstance(ticket, FakeTicket)
    assert ws.called[0]["where"] == my_filter
    assert ws.called[0]["once"] is True


def test_realtime_execution_base_properties():
    """Test KisRealtimeExecutionBase property accessors."""
    from decimal import Decimal

    exec_obj = order_execution.KisDomesticRealtimeOrderExecution()
    exec_obj.quantity = Decimal("100")
    exec_obj.executed_quantity = Decimal("50")
    exec_obj.unit_price = Decimal("10000")

    # Test qty property
    assert exec_obj.qty == Decimal("100")

    # Test executed_qty property
    assert exec_obj.executed_qty == Decimal("50")

    # Test order_price property (alias for unit_price)
    assert exec_obj.order_price == Decimal("10000")


def test_domestic_kis_post_init_creates_order_number():
    """Test __kis_post_init__ creates KisOrderNumber correctly."""
    from datetime import datetime
    from unittest.mock import Mock

    from vmkis.client.account import KisAccountNumber

    exec_obj = order_execution.KisDomesticRealtimeOrderExecution()
    exec_obj.symbol = "005930"
    exec_obj.market = "KRX"
    exec_obj.account_number = KisAccountNumber("12345678-01")
    exec_obj.time_kst = datetime(2024, 1, 15, 9, 30, 0)

    # Mock kis object
    mock_kis = Mock()
    exec_obj.kis = mock_kis

    # Create mock data
    data = [""] * 23
    data[2] = "0001234"  # order number
    data[15] = "06010"  # branch number
    exec_obj.__data__ = data

    # Mock KisSimpleOrder.from_order to avoid complex dependencies
    original_from_order = order_execution.KisSimpleOrder.from_order
    mock_order_number = Mock()
    order_execution.KisSimpleOrder.from_order = Mock(return_value=mock_order_number)

    try:
        exec_obj.__kis_post_init__()

        # Verify from_order was called with correct parameters
        order_execution.KisSimpleOrder.from_order.assert_called_once_with(
            kis=mock_kis,
            symbol="005930",
            market="KRX",
            account_number=exec_obj.account_number,
            branch="06010",
            number="0001234",
            time_kst=exec_obj.time_kst,
        )

        assert exec_obj.order_number == mock_order_number
    finally:
        order_execution.KisSimpleOrder.from_order = original_from_order


def test_foreign_kis_post_init_creates_order_number():
    """Test __kis_post_init__ creates KisOrderNumber for foreign execution."""
    from datetime import datetime
    from unittest.mock import Mock

    from vmkis.client.account import KisAccountNumber

    exec_obj = order_execution.KisForeignRealtimeOrderExecution()
    exec_obj.symbol = "AAPL"
    exec_obj.market = "NASDAQ"
    exec_obj.account_number = KisAccountNumber("12345678-01")
    exec_obj.time_kst = datetime(2024, 1, 15, 9, 30, 0)

    # Mock kis object
    mock_kis = Mock()
    exec_obj.kis = mock_kis

    # Create mock data
    data = [""] * 21
    data[2] = "0005678"  # order number
    data[14] = "06010"  # branch number
    exec_obj.__data__ = data

    # Mock KisSimpleOrder.from_order
    original_from_order = order_execution.KisSimpleOrder.from_order
    mock_order_number = Mock()
    order_execution.KisSimpleOrder.from_order = Mock(return_value=mock_order_number)

    try:
        exec_obj.__kis_post_init__()

        # Verify from_order was called
        order_execution.KisSimpleOrder.from_order.assert_called_once_with(
            kis=mock_kis,
            symbol="AAPL",
            market="NASDAQ",
            account_number=exec_obj.account_number,
            branch="06010",
            number="0005678",
            time_kst=exec_obj.time_kst,
        )

        assert exec_obj.order_number == mock_order_number
    finally:
        order_execution.KisSimpleOrder.from_order = original_from_order


def test_foreign_order_conditions_all_types():
    """Test all foreign order condition types are handled correctly."""
    from decimal import Decimal

    # Test all condition codes
    test_cases = [
        ("1", False, None),  # Market order
        ("2", True, None),  # Limit order
        ("6", False, None),  # Odd lot market
        ("7", True, None),  # Odd lot limit
        ("A", False, "MOO"),  # Market on open
        ("B", True, "LOO"),  # Limit on open
        ("C", False, "MOC"),  # Market on close
        ("D", True, "LOC"),  # Limit on close
    ]

    for code, has_price, expected_condition in test_cases:
        exec_obj = order_execution.KisForeignRealtimeOrderExecution()
        exec_obj.price = Decimal("1000000")
        exec_obj.market = "NYSE"
        exec_obj.quantity = Decimal("10")
        exec_obj.executed_quantity = Decimal("10")
        exec_obj.receipt = False

        data = [""] * 21
        data[6] = code
        exec_obj.__data__ = data

        exec_obj.__post_init__()

        assert exec_obj.condition == expected_condition, f"Failed for code {code}"
        if has_price:
            assert exec_obj.unit_price is not None, f"Expected price for code {code}"
        else:
            assert exec_obj.unit_price is None, f"Expected no price for code {code}"


def test_foreign_decimal_places_all_markets():
    """Test decimal place adjustment for all supported markets."""
    from decimal import Decimal

    # Test market types with different decimal places
    test_cases = [
        ("NASDAQ", "1480100", "148.0100"),  # US: 4 decimals
        ("NYSE", "1480100", "148.0100"),  # US: 4 decimals
        ("AMEX", "1480100", "148.0100"),  # US: 4 decimals
        ("TYO", "12345", "1234.5"),  # JP: 1 decimal
        ("SSE", "1234567", "1234.567"),  # CN: 3 decimals
        ("SZSE", "1234567", "1234.567"),  # CN: 3 decimals
        ("HKEX", "1234567", "1234.567"),  # HK: 3 decimals
        ("HNX", "12345", "12345"),  # VN: 0 decimals
        ("HSX", "12345", "12345"),  # VN: 0 decimals
    ]

    for market, raw_price, expected_price in test_cases:
        exec_obj = order_execution.KisForeignRealtimeOrderExecution()
        exec_obj.price = Decimal(raw_price)
        exec_obj.market = market
        exec_obj.quantity = Decimal("10")
        exec_obj.executed_quantity = Decimal("10")
        exec_obj.receipt = False

        data = [""] * 21
        data[6] = "2"  # Limit order
        exec_obj.__data__ = data

        exec_obj.__post_init__()

        assert exec_obj.price == Decimal(expected_price), f"Failed for market {market}"
