"""Unit tests for vmkis.adapter.account_product.order"""

from decimal import Decimal
from types import SimpleNamespace


def test_order_buy_sell_forward_to_account_product_functions():
    """KisOrderableAccountProductMixin order/buy/sell should forward correctly."""
    from vmkis.adapter.account_product.order import KisOrderableAccountProductMixin

    calls = []

    def fake_order(self, order, price=None, qty=None, condition=None, execution=None, include_foreign=False):
        calls.append(("order", order, price, qty))
        return "order-result"

    def fake_buy(self, price=None, qty=None, condition=None, execution=None, include_foreign=False):
        calls.append(("buy", price, qty))
        return "buy-result"

    def fake_sell(self, price=None, qty=None, condition=None, execution=None, include_foreign=False):
        calls.append(("sell", price, qty))
        return "sell-result"

    class TestProduct(KisOrderableAccountProductMixin):
        def __init__(self):
            self.kis = SimpleNamespace()
            self.account_number = "12345678-01"
            self.market = "KRX"
            self.symbol = "005930"

    orig_order = KisOrderableAccountProductMixin.order
    orig_buy = KisOrderableAccountProductMixin.buy
    orig_sell = KisOrderableAccountProductMixin.sell

    try:
        KisOrderableAccountProductMixin.order = fake_order
        KisOrderableAccountProductMixin.buy = fake_buy
        KisOrderableAccountProductMixin.sell = fake_sell

        prod = TestProduct()

        o_res = prod.order("buy", price=100, qty=10)
        assert o_res == "order-result"
        assert calls[0] == ("order", "buy", 100, 10)

        b_res = prod.buy(price=200, qty=5)
        assert b_res == "buy-result"
        assert calls[1] == ("buy", 200, 5)

        s_res = prod.sell(price=150, qty=3)
        assert s_res == "sell-result"
        assert calls[2] == ("sell", 150, 3)
    finally:
        KisOrderableAccountProductMixin.order = orig_order
        KisOrderableAccountProductMixin.buy = orig_buy
        KisOrderableAccountProductMixin.sell = orig_sell


def test_orderable_amount_and_pending_orders_forward():
    """orderable_amount and pending_orders should forward to account_product functions."""
    from vmkis.adapter.account_product.order import KisOrderableAccountProductMixin

    calls = []

    def fake_amount(self, price=None, condition=None, execution=None):
        calls.append(("amount", price))
        return "amount-result"

    def fake_pending(self):
        calls.append(("pending",))
        return "pending-result"

    class TestProduct(KisOrderableAccountProductMixin):
        def __init__(self):
            self.kis = SimpleNamespace()
            self.account_number = "12345678-01"
            self.market = "KRX"
            self.symbol = "005930"

    orig_amount = KisOrderableAccountProductMixin.orderable_amount
    orig_pending = KisOrderableAccountProductMixin.pending_orders

    try:
        KisOrderableAccountProductMixin.orderable_amount = fake_amount
        KisOrderableAccountProductMixin.pending_orders = fake_pending

        prod = TestProduct()

        amt_res = prod.orderable_amount(price=100)
        assert amt_res == "amount-result"
        assert calls[0] == ("amount", 100)

        pend_res = prod.pending_orders()
        assert pend_res == "pending-result"
        assert calls[1] == ("pending",)
    finally:
        KisOrderableAccountProductMixin.orderable_amount = orig_amount
        KisOrderableAccountProductMixin.pending_orders = orig_pending


def test_properties_return_expected_values(monkeypatch):
    """Test quantity/qty/orderable/purchase_amount properties."""
    from vmkis.adapter.account_product.order import KisOrderableAccountProductMixin

    # Create a fake balance with needed attributes
    fake_stock = SimpleNamespace(quantity=Decimal("100"), orderable=Decimal("50"), purchase_amount=Decimal("5000"))

    fake_balance = SimpleNamespace(stock=lambda symbol: fake_stock)

    fake_account = SimpleNamespace(balance=lambda country=None: fake_balance)

    class TestProduct(KisOrderableAccountProductMixin):
        symbol = "TEST"
        market = "KRX"
        account = fake_account

    prod = TestProduct()

    # quantity and qty should be same
    assert prod.quantity == Decimal("100")
    assert prod.qty == Decimal("100")

    # orderable
    assert prod.orderable == Decimal("50")

    # purchase_amount
    assert prod.purchase_amount == Decimal("5000")
