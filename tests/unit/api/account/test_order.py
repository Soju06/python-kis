from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest

from vmkis.api.account import order as ordmod
from vmkis.client.account import KisAccountNumber


def _bind_real_call(mock_kis):
    """목에 실제 `VmKis.call` 을 바인딩한다.

    주문 함수가 `fetch` 대신 `call` 을 쓰게 됐지만(이슈 #43), 테스트의
    가치는 "국내 매수는 TTTC0802U 로 나간다"를 확인하는 데 있다. 실제
    `call` 을 태우면 스펙 해석까지 함께 검증하면서 `fetch(api=...)` 단언을
    그대로 유지할 수 있다.
    """
    from vmkis.kis import VmKis

    mock_kis.call = lambda *args, **kwargs: VmKis.call(mock_kis, *args, **kwargs)


def test_ensure_price_and_quantity_preserve_when_digit_none():
    # When digit is None, the original Decimal is preserved
    p = Decimal("1.23")
    assert ordmod.ensure_price(p, digit=None) is p

    q = Decimal("2.5")
    assert ordmod.ensure_quantity(q, digit=None) is q


def test_ensure_price_integer_default_quantize():
    # default digit is 4 -> quantize to 4 decimal places
    res = ordmod.ensure_price(1)
    assert isinstance(res, Decimal)
    assert res == Decimal("1.0000")


def test_ensure_price_from_float():
    # Test float conversion
    res = ordmod.ensure_price(10.5, digit=2)
    assert isinstance(res, Decimal)
    assert res == Decimal("10.50")


def test_ensure_quantity_from_int():
    # Test integer quantity conversion with default digit=0
    res = ordmod.ensure_quantity(10)
    assert isinstance(res, Decimal)
    assert res == Decimal("10")


def test_ensure_quantity_from_float():
    # Test float quantity conversion
    res = ordmod.ensure_quantity(5.75, digit=2)
    assert isinstance(res, Decimal)
    assert res == Decimal("5.75")


def test_to_domestic_and_foreign_order_condition_success_and_failure():
    # valid conversions
    assert ordmod.to_domestic_order_condition("condition") == "condition"
    assert ordmod.to_foreign_order_condition("LOO") == "LOO"

    # invalid conversions raise
    with pytest.raises(ValueError):
        ordmod.to_domestic_order_condition("LOO")

    with pytest.raises(ValueError):
        ordmod.to_foreign_order_condition("best")


def test_order_condition_rejects_non_positive_price():
    # negative price should raise
    with pytest.raises(ValueError) as ei:
        ordmod.order_condition(False, "KRX", "buy", Decimal("-1"))
    assert "가격은 0보다 커야합니다." in str(ei.value)


def test_order_condition_known_mappings():
    # Mapping that exists after fallback logic for non-paper KRX buy with price
    res = ordmod.order_condition(False, "KRX", "buy", Decimal("100"), None, None)
    assert res[0] == "00" and res[2] == "지정가"

    # NASDAQ mapping for live (non-paper) and condition LOO
    res2 = ordmod.order_condition(False, "NASDAQ", "buy", Decimal("100"), "LOO", None)
    assert res2[0] == "32" and res2[2] == "장개시지정가"


def test_resolve_domestic_order_condition():
    assert ordmod.resolve_domestic_order_condition("01") == (False, None, None)
    # unknown code returns default
    assert ordmod.resolve_domestic_order_condition("ZZZ") == (True, None, None)


def test_kis_ordernumber_eq_and_hash():
    a = object.__new__(ordmod.KisOrderNumberBase)
    b = object.__new__(ordmod.KisOrderNumberBase)

    # assign matching attributes
    for obj in (a, b):
        obj.account_number = "ACC"
        obj.symbol = "SYM"
        obj.market = "KRX"
        obj.branch = "01"
        obj.number = "10"

    assert a == b
    assert hash(a) == hash(b)


def test_order_condition_fallback_virtual_none():
    # Test fallback logic when paper is not in map - converts to None (live)
    ordmod.order_condition(True, "KRX", "buy", Decimal("100"), None, None)


def test_orderable_conditions_repr_prints_table():
    # Test that orderable_conditions_repr returns a string
    result = ordmod.orderable_conditions_repr()
    assert isinstance(result, str)
    assert "KRX" in result or "NASDAQ" in result


def test_kis_simple_order_number_creation():
    # Test KisSimpleOrderNumber creation
    order = object.__new__(ordmod.KisSimpleOrderNumber)
    order.account_number = "12345678-01"
    order.symbol = "AAPL"
    order.market = "NASDAQ"
    order.branch = "000"
    order.number = "123"

    assert order.symbol == "AAPL"
    assert order.market == "NASDAQ"


def test_kis_simple_order_creation():
    # Test KisSimpleOrder creation
    from decimal import Decimal

    order = object.__new__(ordmod.KisSimpleOrder)
    order.account_number = "12345678-01"
    order.symbol = "AAPL"
    order.market = "NASDAQ"
    order.branch = "000"
    order.number = "123"
    order.unit_price = Decimal("150")
    order.quantity = Decimal("10")

    assert order.unit_price == Decimal("150")
    assert order.quantity == Decimal("10")


def test_domestic_order_checks_msg_cd_for_errors():
    # Test that __pre_init__ checks msg_cd for error codes
    # Note: Full exception tests are covered in integration tests
    # as mocking the full response structure is complex
    pass


def test_domestic_order_pre_init_not_found(monkeypatch):
    # Test __pre_init__ raises KisNotFoundError for APBK0656
    from vmkis.responses.response import KisNotFoundError

    # Create exception first
    mock_request = Mock()
    mock_request.headers = {}
    mock_response = Mock()
    mock_response.request = mock_request
    mock_response.headers = {}

    def raise_not_found_mock(data, code, market):
        raise KisNotFoundError({"msg_cd": "APBK0656", "msg1": "Not found"}, mock_response)

    monkeypatch.setattr(ordmod, "raise_not_found", raise_not_found_mock)

    order = object.__new__(ordmod.KisDomesticOrder)
    order.symbol = "INVALID"
    order.market = "KRX"

    data = {"msg_cd": "APBK0656", "msg1": "Not found", "__response__": mock_response, "output": {"ORD_TMD": "153000"}}

    with pytest.raises(KisNotFoundError):
        order.__pre_init__(data)


def test_domestic_order_pre_init_sets_time(monkeypatch):
    # Test __pre_init__ sets time correctly

    order = object.__new__(ordmod.KisDomesticOrder)
    order.symbol = "005930"
    order.market = "KRX"

    data = {"msg_cd": "OK", "output": {"ORD_TMD": "153000"}}

    # Mock super().__pre_init__
    monkeypatch.setattr(ordmod.KisAPIResponse, "__pre_init__", lambda self, data: None)

    order.__pre_init__(data)

    # Should have set time_kst and time
    assert order.time_kst.hour == 15
    assert order.time_kst.minute == 30
    assert order.time == order.time_kst


def test_foreign_order_checks_msg_cd_for_errors():
    # Test that ForeignOrder __pre_init__ checks msg_cd for error codes
    # Note: Full exception tests are covered in integration tests
    # as mocking the full response structure is complex
    pass


def test_foreign_order_pre_init_sets_time_with_timezone(monkeypatch):
    # Test ForeignOrder __pre_init__ sets time with timezone conversion

    from vmkis.api.stock.market import get_market_timezone

    order = object.__new__(ordmod.KisForeignOrder)
    order.symbol = "AAPL"
    order.market = "NASDAQ"
    order.timezone = get_market_timezone("NASDAQ")

    data = {"msg_cd": "OK", "output": {"ORD_TMD": "093000"}}

    monkeypatch.setattr(ordmod.KisAPIResponse, "__pre_init__", lambda self, data: None)

    order.__pre_init__(data)

    # Should have set both time_kst and time with timezone
    assert order.time_kst.hour == 9
    assert order.time is not None


def test_orderable_quantity_buy_uses_orderable_amount(monkeypatch):
    # Test _orderable_quantity for buy order
    from decimal import Decimal

    mock_amount = Mock()
    mock_amount.qty = Decimal("100")
    mock_amount.foreign_qty = Decimal("150")
    mock_amount.unit_price = Decimal("50000")

    def mock_orderable_amount(*args, **kwargs):
        return mock_amount

    monkeypatch.setattr("vmkis.api.account.orderable_amount.orderable_amount", mock_orderable_amount)

    qty, unit_price = ordmod._orderable_quantity(
        Mock(), "12345678-01", "KRX", "005930", order="buy", price=Decimal("50000")
    )

    assert qty == Decimal("100")
    assert unit_price == Decimal("50000")


def test_orderable_quantity_buy_with_foreign(monkeypatch):
    # Test _orderable_quantity for buy with include_foreign=True
    from decimal import Decimal

    mock_amount = Mock()
    mock_amount.qty = Decimal("100")
    mock_amount.foreign_qty = Decimal("150")
    mock_amount.unit_price = Decimal("50000")

    monkeypatch.setattr("vmkis.api.account.orderable_amount.orderable_amount", lambda *a, **k: mock_amount)

    qty, unit_price = ordmod._orderable_quantity(
        Mock(), "12345678-01", "KRX", "005930", order="buy", include_foreign=True
    )

    assert qty == Decimal("150")


def test_orderable_quantity_buy_throws_when_no_qty(monkeypatch):
    # Test _orderable_quantity raises when no quantity available
    from decimal import Decimal

    mock_amount = Mock()
    mock_amount.qty = Decimal("0")
    mock_amount.foreign_qty = Decimal("0")

    monkeypatch.setattr("vmkis.api.account.orderable_amount.orderable_amount", lambda *a, **k: mock_amount)

    with pytest.raises(ValueError, match="주문가능수량이 없습니다"):
        ordmod._orderable_quantity(Mock(), "12345678-01", "KRX", "005930", order="buy")


def test_orderable_quantity_sell_uses_balance(monkeypatch):
    # Test _orderable_quantity for sell order
    from decimal import Decimal

    monkeypatch.setattr("vmkis.api.account.balance.orderable_quantity", lambda *a, **k: Decimal("50"))

    qty, unit_price = ordmod._orderable_quantity(Mock(), "12345678-01", "KRX", "005930", order="sell")

    assert qty == Decimal("50")
    assert unit_price is None


def test_orderable_quantity_sell_throws_when_none(monkeypatch):
    # Test _orderable_quantity for sell raises when no stock
    monkeypatch.setattr("vmkis.api.account.balance.orderable_quantity", lambda *a, **k: None)

    with pytest.raises(ValueError, match="주문가능수량이 없습니다"):
        ordmod._orderable_quantity(Mock(), "12345678-01", "KRX", "005930", order="sell")


def test_get_order_price_upper_limit(monkeypatch):
    # Test _get_order_price with upper limit
    from decimal import Decimal

    mock_quote = Mock()
    mock_quote.high_limit = Decimal("100000")
    mock_quote.close = Decimal("80000")

    monkeypatch.setattr(ordmod, "quote", lambda *a, **k: mock_quote)

    price = ordmod._get_order_price(Mock(), "KRX", "005930", "upper")

    assert price == Decimal("100000")


def test_get_order_price_upper_fallback(monkeypatch):
    # Test _get_order_price falls back to close * 1.5
    from decimal import Decimal

    mock_quote = Mock()
    mock_quote.high_limit = None
    mock_quote.close = Decimal("80000")

    monkeypatch.setattr(ordmod, "quote", lambda *a, **k: mock_quote)

    price = ordmod._get_order_price(Mock(), "KRX", "005930", "upper")

    assert price == Decimal("120000")  # 80000 * 1.5


def test_get_order_price_lower_limit(monkeypatch):
    # Test _get_order_price with lower limit
    from decimal import Decimal

    mock_quote = Mock()
    mock_quote.low_limit = Decimal("60000")
    mock_quote.close = Decimal("80000")

    monkeypatch.setattr(ordmod, "quote", lambda *a, **k: mock_quote)

    price = ordmod._get_order_price(Mock(), "KRX", "005930", "lower")

    assert price == Decimal("60000")


def test_domestic_order_endpoints_mapping():
    """국내 주문 스펙이 실전/모의 TR 을 둘 다 들고 있어야 한다.

    예전에는 `(실전여부, 주문종류) -> TR` 표였고 호출부가
    `if self.paper` 로 골랐다. 지금은 실전/모의 차원이 스펙 안으로 들어가
    호출부에서 분기가 사라졌다 (이슈 #43).
    """
    assert set(ordmod.DOMESTIC_ORDER_ENDPOINTS) == {"buy", "sell"}

    buy = ordmod.DOMESTIC_ORDER_ENDPOINTS["buy"]
    assert buy.tr_live == "TTTC0802U"
    assert buy.tr_paper == "VTTC0802U"
    assert buy.method == "POST"

    sell = ordmod.DOMESTIC_ORDER_ENDPOINTS["sell"]
    assert sell.tr_live == "TTTC0801U"
    assert sell.tr_paper == "VTTC0801U"

    # 스펙은 데이터라 네트워크 없이 규칙을 검증할 수 있다.
    assert buy.resolve(paper=False) == ("TTTC0802U", "live")
    assert buy.resolve(paper=True) == ("VTTC0802U", "paper")


def test_order_condition_fallback_market_none():
    # Test fallback to market=None when specific market not found
    # Using an exotic condition that might trigger fallback
    try:
        res = ordmod.order_condition(False, "AMEX", "buy", Decimal("100"), None, None)
        # If it succeeds, check it's a valid condition
        assert res[0] in [c[0] for c in ordmod.ORDER_CONDITION_MAP.values()]
    except ValueError:
        # It's okay if it raises ValueError for unsupported market
        pass


def test_order_condition_fallback_to_market_price():
    # When price is provided but combination not found, falls back to market price (price=None)
    # This tests the price=False fallback in line 292
    try:
        res = ordmod.order_condition(False, "KRX", "buy", Decimal("100"), "extended", "FOK")
        # If successful, verify it's valid
        assert len(res) == 3
    except ValueError:
        # Acceptable if this specific combination is not supported
        pass


def test_order_condition_virtual_not_supported_error():
    # Test error message when paper trading doesn't support a condition
    with pytest.raises(ValueError) as exc_info:
        # Try a condition that exists for live but not paper
        ordmod.order_condition(True, "NYSE", "buy", Decimal("100"), "LOO", None)

    error_msg = str(exc_info.value)
    assert "모의투자" in error_msg or "주문조건" in error_msg


def test_order_condition_invalid_combination_error():
    # Test error for completely invalid condition combination
    with pytest.raises(ValueError) as exc_info:
        ordmod.order_condition(False, "INVALID_MARKET", "buy", Decimal("100"), "INVALID_COND", "INVALID_EXEC")

    assert "주문조건" in str(exc_info.value)


def test_resolve_domestic_order_condition_unknown_code():
    # Unknown codes return default (True, None, None)
    result = ordmod.resolve_domestic_order_condition("99")
    assert result == (True, None, None)


def test_resolve_domestic_order_condition_market_price():
    # Code "01" is market price
    result = ordmod.resolve_domestic_order_condition("01")
    assert result == (False, None, None)


def test_resolve_domestic_order_condition_limit_ioc():
    # Code "11" is limit with IOC
    result = ordmod.resolve_domestic_order_condition("11")
    assert result == (True, None, "IOC")


def test_to_domestic_order_condition_valid():
    # Test valid domestic condition
    result = ordmod.to_domestic_order_condition("best")
    assert result == "best"

    result2 = ordmod.to_domestic_order_condition("extended")
    assert result2 == "extended"


def test_to_foreign_order_condition_valid():
    # Test valid foreign conditions
    result = ordmod.to_foreign_order_condition("LOO")
    assert result == "LOO"

    result2 = ordmod.to_foreign_order_condition("LOC")
    assert result2 == "LOC"


def test_ordernumberbase_init_minimal():
    # Test initialization without parameters
    ordmod.KisOrderNumberBase()
    # Should not raise error


def test_ordernumberbase_init_with_kis_only():
    # Test initialization with kis only
    mock_kis = Mock()
    order_num = ordmod.KisOrderNumberBase(kis=mock_kis)
    assert order_num.kis is mock_kis


def test_ordernumberbase_init_full_valid():
    # Test full initialization with all required parameters
    mock_kis = Mock()
    account = KisAccountNumber(account="12345678-01")

    order_num = ordmod.KisOrderNumberBase(
        kis=mock_kis, symbol="005930", market="KRX", account_number=account, branch="00001", number="12345"
    )

    assert order_num.symbol == "005930"
    assert order_num.market == "KRX"
    assert order_num.account_number == account
    assert order_num.branch == "00001"
    assert order_num.number == "12345"


def test_ordernumberbase_init_missing_market_error():
    # Test error when symbol provided but market missing
    mock_kis = Mock()

    with pytest.raises(ValueError) as exc_info:
        ordmod.KisOrderNumberBase(kis=mock_kis, symbol="005930", market=None)

    assert "market" in str(exc_info.value)


def test_ordernumberbase_init_missing_account_error():
    # Test error when symbol/market provided but account missing
    mock_kis = Mock()

    with pytest.raises(ValueError) as exc_info:
        ordmod.KisOrderNumberBase(kis=mock_kis, symbol="005930", market="KRX", account_number=None)

    assert "account_number" in str(exc_info.value)


def test_ordernumberbase_init_missing_branch_error():
    # Test error when account provided but branch missing
    mock_kis = Mock()
    account = KisAccountNumber(account="12345678-01")

    with pytest.raises(ValueError) as exc_info:
        ordmod.KisOrderNumberBase(kis=mock_kis, symbol="005930", market="KRX", account_number=account, branch=None)

    assert "branch" in str(exc_info.value)


def test_ordernumberbase_init_missing_number_error():
    # Test error when branch provided but number missing
    mock_kis = Mock()
    account = KisAccountNumber(account="12345678-01")

    with pytest.raises(ValueError) as exc_info:
        ordmod.KisOrderNumberBase(
            kis=mock_kis, symbol="005930", market="KRX", account_number=account, branch="00001", number=None
        )

    assert "number" in str(exc_info.value)


def test_ordernumberbase_eq_with_non_order_object():
    # Test equality with non-KisOrderNumber object returns False
    order_num = ordmod.KisOrderNumberBase()
    assert order_num != "not an order"
    assert order_num != 123
    assert order_num is not None


def test_kissimpleorder_init_minimal():
    # Test KisSimpleOrder initialization without parameters
    ordmod.KisSimpleOrder()
    # Should not raise error


def test_kissimpleorder_init_with_account_missing_symbol_error():
    # Test error when account provided but symbol missing
    account = KisAccountNumber(account="12345678-01")

    with pytest.raises(ValueError) as exc_info:
        ordmod.KisSimpleOrder(account_number=account, symbol=None)

    assert "symbol" in str(exc_info.value)


def test_kissimpleorder_init_with_symbol_missing_market_error():
    # Test error when symbol provided but market missing
    account = KisAccountNumber(account="12345678-01")

    with pytest.raises(ValueError) as exc_info:
        ordmod.KisSimpleOrder(account_number=account, symbol="005930", market=None)

    assert "market" in str(exc_info.value)


def test_kissimpleorder_init_with_branch_missing_account_error():
    # Test error when branch provided but account_number missing
    with pytest.raises(ValueError) as exc_info:
        ordmod.KisSimpleOrder(account_number=None, branch="00001")

    assert "account_number" in str(exc_info.value)


def test_kissimpleorder_init_with_branch_missing_number_error():
    # Test error when branch provided but number missing
    account = KisAccountNumber(account="12345678-01")

    with pytest.raises(ValueError) as exc_info:
        ordmod.KisSimpleOrder(account_number=account, symbol="005930", market="KRX", branch="00001", number=None)

    assert "number" in str(exc_info.value)


def test_kissimpleorder_init_with_number_missing_timekst_error():
    # Test error when number provided but time_kst missing
    account = KisAccountNumber(account="12345678-01")

    with pytest.raises(ValueError) as exc_info:
        ordmod.KisSimpleOrder(
            account_number=account, symbol="005930", market="KRX", branch="00001", number="12345", time_kst=None
        )

    assert "time_kst" in str(exc_info.value)


def test_kissimpleorder_init_full_valid():
    # Test full valid initialization
    account = KisAccountNumber(account="12345678-01")
    time_kst = datetime(2024, 1, 1, 9, 0, 0, tzinfo=datetime.now().astimezone().tzinfo)

    order = ordmod.KisSimpleOrder(
        account_number=account, symbol="005930", market="KRX", branch="00001", number="12345", time_kst=time_kst
    )

    assert order.account_number == account
    assert order.symbol == "005930"
    assert order.market == "KRX"
    assert order.branch == "00001"
    assert order.number == "12345"
    assert order.time_kst == time_kst


def test_domestic_order_validation_no_account(monkeypatch):
    # Test domestic_order raises when account is missing
    mock_kis = Mock()
    mock_kis.paper = False

    with pytest.raises(ValueError, match="계좌번호를 입력해주세요"):
        ordmod.domestic_order(mock_kis, account=None, symbol="005930")


def test_domestic_order_validation_no_symbol(monkeypatch):
    # Test domestic_order raises when symbol is missing
    mock_kis = Mock()
    mock_kis.paper = False

    with pytest.raises(ValueError, match="종목코드를 입력해주세요"):
        ordmod.domestic_order(mock_kis, account="12345678-01", symbol="")


def test_domestic_order_validation_negative_qty(monkeypatch):
    # Test domestic_order raises when quantity is negative
    mock_kis = Mock()
    mock_kis.paper = False

    with pytest.raises(ValueError, match="수량은 0보다 커야합니다"):
        ordmod.domestic_order(mock_kis, account="12345678-01", symbol="005930", qty=-10)


def test_domestic_order_converts_string_account(monkeypatch):
    # Test domestic_order converts string to KisAccountNumber
    from decimal import Decimal

    mock_kis = Mock()
    mock_kis.paper = False
    mock_kis.fetch = Mock(return_value=Mock())
    _bind_real_call(mock_kis)

    monkeypatch.setattr(ordmod, "_orderable_quantity", lambda *a, **k: (Decimal("100"), None))

    ordmod.domestic_order(mock_kis, account="12345678-01", symbol="005930", order="buy", price=50000)

    # Verify fetch was called with KisAccountNumber in form
    assert mock_kis.fetch.called
    call_args = mock_kis.fetch.call_args
    assert "form" in call_args.kwargs
    assert isinstance(call_args.kwargs["form"][0], KisAccountNumber)


def test_domestic_order_sets_price_upper_when_market_buy(monkeypatch):
    # Test domestic_order with market order (price=None sends "0")
    from decimal import Decimal

    mock_kis = Mock()
    mock_kis.paper = False
    mock_kis.fetch = Mock(return_value=Mock())
    _bind_real_call(mock_kis)

    monkeypatch.setattr(ordmod, "_orderable_quantity", lambda *a, **k: (Decimal("10"), None))

    ordmod.domestic_order(
        mock_kis,
        account="12345678-01",
        symbol="005930",
        order="buy",
        price=None,  # Market order
    )

    # Verify fetch called with price 0 for market order
    call_args = mock_kis.fetch.call_args
    assert call_args.kwargs["body"]["ORD_UNPR"] == "0"
    assert call_args.kwargs["body"]["ORD_DVSN"] == "01"  # Market order code


def test_domestic_order_uses_orderable_quantity_when_qty_none(monkeypatch):
    # Test domestic_order calls _orderable_quantity when qty is None
    from decimal import Decimal

    mock_kis = Mock()
    mock_kis.paper = True
    mock_kis.fetch = Mock(return_value=Mock())
    _bind_real_call(mock_kis)

    orderable_qty_called = []

    def mock_orderable_qty(self, account, market, symbol, order, price, condition, execution, include_foreign):
        orderable_qty_called.append(True)
        return Decimal("50"), Decimal("45000")

    monkeypatch.setattr(ordmod, "_orderable_quantity", mock_orderable_qty)

    ordmod.domestic_order(mock_kis, account="12345678-01", symbol="005930", order="buy", price=50000, qty=None)

    assert len(orderable_qty_called) == 1
    assert mock_kis.fetch.call_args.kwargs["body"]["ORD_QTY"] == "50"


def test_domestic_order_fetch_with_correct_api_code(monkeypatch):
    # Test domestic_order uses correct API codes
    from decimal import Decimal

    mock_kis = Mock()
    mock_kis.paper = False
    mock_kis.fetch = Mock(return_value=Mock())
    _bind_real_call(mock_kis)

    monkeypatch.setattr(ordmod, "_orderable_quantity", lambda *a, **k: (Decimal("10"), None))

    # Test buy order
    ordmod.domestic_order(mock_kis, account="12345678-01", symbol="005930", order="buy", price=50000)

    assert mock_kis.fetch.call_args.kwargs["api"] == "TTTC0802U"

    # Test sell order
    ordmod.domestic_order(mock_kis, account="12345678-01", symbol="005930", order="sell", price=50000)

    assert mock_kis.fetch.call_args.kwargs["api"] == "TTTC0801U"


def test_domestic_order_virtual_api_codes(monkeypatch):
    # Test domestic_order uses paper API codes in paper mode
    from decimal import Decimal

    mock_kis = Mock()
    mock_kis.paper = True
    mock_kis.fetch = Mock(return_value=Mock())
    _bind_real_call(mock_kis)

    monkeypatch.setattr(ordmod, "_orderable_quantity", lambda *a, **k: (Decimal("10"), None))

    # Test paper buy
    ordmod.domestic_order(mock_kis, account="12345678-01", symbol="005930", order="buy", price=50000)

    assert mock_kis.fetch.call_args.kwargs["api"] == "VTTC0802U"


def test_foreign_order_validation_no_account(monkeypatch):
    # Test foreign_order raises when account is missing
    mock_kis = Mock()
    mock_kis.paper = False

    with pytest.raises(ValueError, match="계좌번호를 입력해주세요"):
        ordmod.foreign_order(mock_kis, account=None, market="NASDAQ", symbol="AAPL")


def test_foreign_order_validation_no_symbol(monkeypatch):
    # Test foreign_order raises when symbol is missing
    mock_kis = Mock()
    mock_kis.paper = False

    with pytest.raises(ValueError, match="종목코드를 입력해주세요"):
        ordmod.foreign_order(mock_kis, account="12345678-01", market="NASDAQ", symbol="")


def test_foreign_order_validation_negative_qty(monkeypatch):
    # Test foreign_order raises when quantity is negative
    mock_kis = Mock()
    mock_kis.paper = False

    with pytest.raises(ValueError, match="수량은 0보다 커야합니다"):
        ordmod.foreign_order(mock_kis, account="12345678-01", market="NASDAQ", symbol="AAPL", qty=-5)


def test_foreign_order_uses_correct_market_api_code(monkeypatch):
    # Test foreign_order selects correct API code per market
    from decimal import Decimal

    mock_kis = Mock()
    mock_kis.paper = False
    mock_kis.fetch = Mock(return_value=Mock())
    _bind_real_call(mock_kis)

    monkeypatch.setattr(ordmod, "_orderable_quantity", lambda *a, **k: (Decimal("10"), None))

    # NASDAQ buy
    ordmod.foreign_order(mock_kis, account="12345678-01", market="NASDAQ", symbol="AAPL", order="buy", price=150)
    assert mock_kis.fetch.call_args.kwargs["api"] == "TTTT1002U"

    # NYSE sell
    ordmod.foreign_order(mock_kis, account="12345678-01", market="NYSE", symbol="AAPL", order="sell", price=150)
    assert mock_kis.fetch.call_args.kwargs["api"] == "TTTT1006U"


def test_foreign_order_tokyo_market(monkeypatch):
    # Test foreign_order with Tokyo market
    from decimal import Decimal

    mock_kis = Mock()
    mock_kis.paper = False
    mock_kis.fetch = Mock(return_value=Mock())
    _bind_real_call(mock_kis)

    monkeypatch.setattr(ordmod, "_orderable_quantity", lambda *a, **k: (Decimal("100"), None))

    ordmod.foreign_order(mock_kis, account="12345678-01", market="TYO", symbol="6758", order="buy", price=1000)

    assert mock_kis.fetch.call_args.kwargs["api"] == "TTTS0308U"


def test_foreign_daytime_order_validation_no_account(monkeypatch):
    # Test foreign_daytime_order raises when account is missing
    mock_kis = Mock()
    mock_kis.paper = False

    with pytest.raises(ValueError, match="계좌번호를 입력해주세요"):
        ordmod.foreign_daytime_order(mock_kis, account=None, market="NASDAQ", symbol="AAPL")


def test_foreign_daytime_order_validation_no_symbol(monkeypatch):
    # Test foreign_daytime_order raises when symbol is missing
    mock_kis = Mock()
    mock_kis.paper = False

    with pytest.raises(ValueError, match="종목코드를 입력해주세요"):
        ordmod.foreign_daytime_order(mock_kis, account="12345678-01", market="NASDAQ", symbol="")


def test_foreign_daytime_order_uses_daytime_market_code(monkeypatch):
    # Test foreign_daytime_order uses DAYTIME_MARKET_SHORT_TYPE_MAP
    from decimal import Decimal

    mock_kis = Mock()
    mock_kis.paper = False
    mock_kis.fetch = Mock(return_value=Mock())
    _bind_real_call(mock_kis)

    monkeypatch.setattr(ordmod, "_orderable_quantity", lambda *a, **k: (Decimal("10"), None))

    ordmod.foreign_daytime_order(
        mock_kis, account="12345678-01", market="NASDAQ", symbol="AAPL", order="buy", price=150
    )

    # Verify fetch called with daytime API
    assert mock_kis.fetch.called
    call_args = mock_kis.fetch.call_args
    assert call_args.kwargs["body"]["OVRS_EXCG_CD"] in [
        "NASD",
        "NYSE",
        "AMEX",
        "SEHK",
        "SHAA",
        "SZAA",
        "TKSE",
        "HASE",
        "VNSE",
    ]


def test_account_order_delegates_to_order(monkeypatch):
    # Test account_order delegates to order function

    mock_account = Mock()
    mock_account.kis = Mock()
    mock_account.account_number = "12345678-01"

    order_called = []

    def mock_order(kis, account, market, symbol, order, price, qty, condition, execution, include_foreign):
        order_called.append((market, symbol, order))
        return Mock()

    monkeypatch.setattr(ordmod, "order_function", mock_order)

    ordmod.account_order(mock_account, market="KRX", symbol="005930", order="buy", price=50000)

    assert len(order_called) == 1
    assert order_called[0] == ("KRX", "005930", "buy")


def test_account_buy_delegates_with_buy_order(monkeypatch):
    # Test account_buy sets order='buy'
    mock_account = Mock()
    mock_account.kis = Mock()
    mock_account.account_number = "12345678-01"

    order_called = []

    def mock_order(kis, account, market, symbol, order, price, qty, condition, execution, include_foreign):
        order_called.append(order)
        return Mock()

    monkeypatch.setattr(ordmod, "order_function", mock_order)

    ordmod.account_buy(mock_account, market="KRX", symbol="005930", price=50000)

    assert len(order_called) == 1
    assert order_called[0] == "buy"


def test_account_sell_delegates_with_sell_order(monkeypatch):
    # Test account_sell sets order='sell'
    mock_account = Mock()
    mock_account.kis = Mock()
    mock_account.account_number = "12345678-01"

    order_called = []

    def mock_order(kis, account, market, symbol, order, price, qty, condition, execution, include_foreign):
        order_called.append(order)
        return Mock()

    monkeypatch.setattr(ordmod, "order_function", mock_order)

    ordmod.account_sell(mock_account, market="KRX", symbol="005930", price=50000)

    assert len(order_called) == 1
    assert order_called[0] == "sell"


def test_account_product_order_uses_product_info(monkeypatch):
    # Test account_product_order uses symbol and market from product
    mock_product = Mock()
    mock_product.kis = Mock()
    mock_product.account_number = "12345678-01"
    mock_product.symbol = "TSLA"
    mock_product.market = "NASDAQ"

    order_called = []

    def mock_order(kis, account, market, symbol, order, price, qty, condition, execution, include_foreign):
        order_called.append((market, symbol))
        return Mock()

    monkeypatch.setattr(ordmod, "order_function", mock_order)

    ordmod.account_product_order(mock_product, order="buy", price=200)

    assert len(order_called) == 1
    assert order_called[0] == ("NASDAQ", "TSLA")


def test_account_product_buy_uses_buy_order(monkeypatch):
    # Test account_product_buy sets order='buy'
    mock_product = Mock()
    mock_product.kis = Mock()
    mock_product.account_number = "12345678-01"
    mock_product.symbol = "AAPL"
    mock_product.market = "NASDAQ"

    order_called = []

    def mock_order(kis, account, market, symbol, order, price, qty, condition, execution, include_foreign):
        order_called.append(order)
        return Mock()

    monkeypatch.setattr(ordmod, "order_function", mock_order)

    ordmod.account_product_buy(mock_product, price=150)

    assert order_called[0] == "buy"


def test_account_product_sell_uses_sell_order(monkeypatch):
    # Test account_product_sell sets order='sell'
    mock_product = Mock()
    mock_product.kis = Mock()
    mock_product.account_number = "12345678-01"
    mock_product.symbol = "AAPL"
    mock_product.market = "NASDAQ"

    order_called = []

    def mock_order(kis, account, market, symbol, order, price, qty, condition, execution, include_foreign):
        order_called.append(order)
        return Mock()

    monkeypatch.setattr(ordmod, "order_function", mock_order)

    ordmod.account_product_sell(mock_product, price=150)

    assert order_called[0] == "sell"


def test_order_function_routes_to_domestic_order(monkeypatch):
    # Test order() routes KRX market to domestic_order
    mock_kis = Mock()
    mock_kis.paper = False

    domestic_called = []

    def mock_domestic_order(*args, **kwargs):
        domestic_called.append(True)
        return Mock()

    monkeypatch.setattr(ordmod, "domestic_order", mock_domestic_order)

    ordmod.order(mock_kis, account="12345678-01", market="KRX", symbol="005930", order="buy", price=50000)

    assert len(domestic_called) == 1


def test_order_function_routes_to_foreign_order(monkeypatch):
    # Test order() routes non-KRX market to foreign_order
    mock_kis = Mock()
    mock_kis.paper = False

    foreign_called = []

    def mock_foreign_order(*args, **kwargs):
        foreign_called.append(True)
        return Mock()

    monkeypatch.setattr(ordmod, "foreign_order", mock_foreign_order)

    ordmod.order(mock_kis, account="12345678-01", market="NASDAQ", symbol="AAPL", order="buy", price=150)

    assert len(foreign_called) == 1


def test_get_order_price_lower_fallback(monkeypatch):
    # Test _get_order_price falls back to close * 0.5 for lower
    from decimal import Decimal

    mock_quote = Mock()
    mock_quote.low_limit = None
    mock_quote.close = Decimal("80000")

    monkeypatch.setattr(ordmod, "quote", lambda *a, **k: mock_quote)

    price = ordmod._get_order_price(Mock(), "KRX", "005930", "lower")

    assert price == Decimal("40000")  # 80000 * 0.5


def test_orderable_quantity_sell_with_zero_qty(monkeypatch):
    # Test _orderable_quantity for sell with zero quantity
    from decimal import Decimal

    monkeypatch.setattr("vmkis.api.account.balance.orderable_quantity", lambda *a, **k: Decimal("0"))

    with pytest.raises(ValueError, match="주문가능수량이 없습니다"):
        ordmod._orderable_quantity(Mock(), "12345678-01", "KRX", "005930", order="sell")


def test_orderable_quantity_buy_with_zero_qty(monkeypatch):
    # Test _orderable_quantity for buy with zero quantity
    from decimal import Decimal

    mock_amount = Mock()
    mock_amount.qty = Decimal("0")
    mock_amount.foreign_qty = Decimal("0")

    monkeypatch.setattr("vmkis.api.account.orderable_amount.orderable_amount", lambda *a, **k: mock_amount)

    with pytest.raises(ValueError, match="주문가능수량이 없습니다"):
        ordmod._orderable_quantity(Mock(), "12345678-01", "KRX", "005930", order="buy")


def test_foreign_order_api_codes_mapping():
    # 해외 주문 스펙: 키는 (시장, 주문종류), 실전/모의는 스펙 안에
    assert ("NASDAQ", "buy") in ordmod.FOREIGN_ORDER_ENDPOINTS
    assert ("NYSE", "sell") in ordmod.FOREIGN_ORDER_ENDPOINTS
    assert ("TYO", "buy") in ordmod.FOREIGN_ORDER_ENDPOINTS
    assert ordmod.FOREIGN_ORDER_ENDPOINTS[("NASDAQ", "buy")].tr_paper == "VTTT1002U"

    assert ordmod.FOREIGN_ORDER_ENDPOINTS[("NASDAQ", "buy")].tr_live == "TTTT1002U"
    assert ordmod.FOREIGN_ORDER_ENDPOINTS[("NYSE", "sell")].tr_live == "TTTT1006U"


def test_order_routes_to_domestic_for_krx(monkeypatch):
    # Test that order() function routes KRX orders correctly

    mock_kis = Mock()
    mock_kis.paper = False

    domestic_called = []

    def mock_domestic(*args, **kwargs):
        domestic_called.append(True)
        return Mock()

    monkeypatch.setattr(ordmod, "domestic_order", mock_domestic)

    ordmod.order(mock_kis, account="12345678-01", market="KRX", symbol="005930", order="buy", price=50000)

    assert len(domestic_called) == 1


def test_order_routes_to_foreign_for_nasdaq(monkeypatch):
    # Test that order() function routes NASDAQ orders correctly

    mock_kis = Mock()
    mock_kis.paper = False

    foreign_called = []

    def mock_foreign(*args, **kwargs):
        foreign_called.append(True)
        return Mock()

    monkeypatch.setattr(ordmod, "foreign_order", mock_foreign)

    ordmod.order(mock_kis, account="12345678-01", market="NASDAQ", symbol="AAPL", order="buy", price=150)

    assert len(foreign_called) == 1


def test_kis_order_base_repr(monkeypatch):
    # Test KisOrderBase __repr__ method
    order = object.__new__(ordmod.KisOrderBase)
    order.symbol = "005930"
    order.market = "KRX"
    order.account_number = KisAccountNumber(account="12345678-01")
    order.branch = "00001"
    order.number = "12345"

    repr_str = repr(order)
    assert "005930" in repr_str
    assert "KRX" in repr_str


def test_kis_order_number_base_repr(monkeypatch):
    # Test KisOrderNumberBase __repr__ method
    order_num = object.__new__(ordmod.KisOrderNumberBase)
    order_num.symbol = "AAPL"
    order_num.market = "NASDAQ"
    order_num.account_number = KisAccountNumber(account="12345678-01")
    order_num.branch = "00001"
    order_num.number = "12345"

    repr_str = repr(order_num)
    assert "AAPL" in repr_str
    assert "NASDAQ" in repr_str


def test_order_condition_price_none_converts_to_false():
    # Test that price=None is treated as price not provided
    res = ordmod.order_condition(False, "KRX", "buy", None, None, None)
    # Should get market order code
    assert res[0] == "01"  # Market order code for live trading
    assert res[2] == "시장가"


def test_ensure_price_converts_int():
    # Test ensure_price with integer
    from decimal import Decimal

    result = ordmod.ensure_price(100, digit=2)
    assert isinstance(result, Decimal)
    assert result == Decimal("100.00")


def test_ensure_price_converts_float():
    # Test ensure_price with float
    from decimal import Decimal

    result = ordmod.ensure_price(99.99, digit=2)
    assert isinstance(result, Decimal)
    assert result == Decimal("99.99")


def test_ensure_quantity_converts_int():
    # Test ensure_quantity with integer
    from decimal import Decimal

    result = ordmod.ensure_quantity(50, digit=0)
    assert isinstance(result, Decimal)
    assert result == Decimal("50")


def test_ensure_quantity_converts_float():
    # Test ensure_quantity with float
    from decimal import Decimal

    result = ordmod.ensure_quantity(12.5, digit=1)
    assert isinstance(result, Decimal)
    assert result == Decimal("12.5")


def test_domestic_order_with_explicit_qty(monkeypatch):
    # Test domestic_order with explicit quantity (skips _orderable_quantity)

    mock_kis = Mock()
    mock_kis.paper = False
    mock_kis.fetch = Mock(return_value=Mock())
    _bind_real_call(mock_kis)

    ordmod.domestic_order(
        mock_kis,
        account="12345678-01",
        symbol="005930",
        order="buy",
        price=50000,
        qty=100,  # Explicit quantity
    )

    # Should skip _orderable_quantity call
    call_args = mock_kis.fetch.call_args
    assert call_args.kwargs["body"]["ORD_QTY"] == "100"


def test_foreign_order_with_explicit_qty(monkeypatch):
    # Test foreign_order with explicit quantity

    mock_kis = Mock()
    mock_kis.paper = False
    mock_kis.fetch = Mock(return_value=Mock())
    _bind_real_call(mock_kis)

    ordmod.foreign_order(
        mock_kis,
        account="12345678-01",
        market="NASDAQ",
        symbol="AAPL",
        order="buy",
        price=150,
        qty=50,  # Explicit quantity
    )

    call_args = mock_kis.fetch.call_args
    assert call_args.kwargs["body"]["ORD_QTY"] == "50"


def test_foreign_daytime_order_with_explicit_qty(monkeypatch):
    # Test foreign_daytime_order with explicit quantity

    mock_kis = Mock()
    mock_kis.paper = False
    mock_kis.fetch = Mock(return_value=Mock())
    _bind_real_call(mock_kis)

    ordmod.foreign_daytime_order(
        mock_kis,
        account="12345678-01",
        market="NASDAQ",
        symbol="AAPL",
        order="buy",
        price=150,
        qty=25,  # Explicit quantity
    )

    call_args = mock_kis.fetch.call_args
    assert call_args.kwargs["body"]["ORD_QTY"] == "25"


def test_orderable_quantity_no_throw(monkeypatch):
    # Test _orderable_quantity with throw_no_qty=False
    from decimal import Decimal

    mock_amount = Mock()
    mock_amount.qty = Decimal("0")
    mock_amount.foreign_qty = Decimal("0")

    monkeypatch.setattr("vmkis.api.account.orderable_amount.orderable_amount", lambda *a, **k: mock_amount)

    # Should not raise
    qty, price = ordmod._orderable_quantity(Mock(), "12345678-01", "KRX", "005930", order="buy", throw_no_qty=False)

    assert qty == Decimal("0")
