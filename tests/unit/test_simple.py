"""`vmkis.simple.SimpleKIS` 테스트.

`SimpleKIS`는 `VmKis`로 위임만 하는 얇은 파사드다. 따라서 검증할 것은
"어떤 호출로 위임되는가"이며, 네트워크는 필요 없다.
"""

import pytest

from vmkis.simple import SimpleKIS


class FakeOrder:
    def __init__(self):
        self.cancelled = False

    def cancel(self):
        self.cancelled = True
        return "cancelled"


class FakeStock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.buy_calls = []

    def quote(self):
        return f"quote:{self.symbol}"

    def buy(self, **kwargs):
        self.buy_calls.append(kwargs)
        return f"order:{self.symbol}"


class FakeAccount:
    def balance(self):
        return "balance"


class FakeVmKis:
    def __init__(self):
        self.stocks = {}

    def stock(self, symbol):
        return self.stocks.setdefault(symbol, FakeStock(symbol))

    def account(self):
        return FakeAccount()


@pytest.fixture
def kis():
    return FakeVmKis()


@pytest.fixture
def simple(kis):
    return SimpleKIS.from_client(kis)


def test_from_client_wraps_instance(kis):
    """from_client는 전달받은 클라이언트를 그대로 보관한다."""
    assert SimpleKIS.from_client(kis).kis is kis


def test_get_price_delegates_to_stock_quote(simple):
    assert simple.get_price("005930") == "quote:005930"


def test_get_balance_delegates_to_account_balance(simple):
    assert simple.get_balance() == "balance"


def test_place_order_without_price_is_market_order(simple, kis):
    """가격을 주지 않으면 수량만 넘겨 시장가로 낸다."""
    assert simple.place_order("005930", qty=3) == "order:005930"
    assert kis.stock("005930").buy_calls == [{"qty": 3}]


def test_place_order_with_price_is_limit_order(simple, kis):
    """가격을 주면 지정가로 낸다."""
    simple.place_order("005930", qty=3, price=70000)

    assert kis.stock("005930").buy_calls == [{"price": 70000, "qty": 3}]


def test_cancel_order_delegates_to_order_object(simple):
    """취소는 주문 객체의 cancel()로 위임한다."""
    order = FakeOrder()

    assert simple.cancel_order(order) == "cancelled"
    assert order.cancelled is True
