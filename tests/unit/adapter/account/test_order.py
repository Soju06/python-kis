"""Unit tests for vmkis.adapter.account.order"""

from types import SimpleNamespace


def test_buy_forwards_to_account_buy():
    """KisOrderableAccountMixin.buy should forward to account_buy with all parameters."""
    from vmkis.adapter.account.order import KisOrderableAccountMixin

    calls = []

    def fake_buy(self, market, symbol, price=None, qty=None, condition=None, execution=None, include_foreign=False):
        calls.append(("buy", market, symbol, price, qty, condition, execution, include_foreign))
        return "buy-result"

    class TestAccount(KisOrderableAccountMixin):
        def __init__(self):
            self.kis = SimpleNamespace()
            self.account_number = "12345678-01"

    # Patch the mixin's class attribute
    original = KisOrderableAccountMixin.buy
    KisOrderableAccountMixin.buy = fake_buy

    try:
        acct = TestAccount()
        result = acct.buy("KRX", "005930", price=100, qty=10, condition=None, execution=None, include_foreign=True)
        assert result == "buy-result"
        assert calls[0][1:] == ("KRX", "005930", 100, 10, None, None, True)
    finally:
        KisOrderableAccountMixin.buy = original


def test_sell_forwards_to_account_sell():
    """KisOrderableAccountMixin.sell should forward to account_sell."""
    from vmkis.adapter.account.order import KisOrderableAccountMixin

    calls = []

    def fake_sell(self, market, symbol, price=None, qty=None, condition=None, execution=None, include_foreign=False):
        calls.append(("sell", market, symbol))
        return "sell-result"

    class TestAccount(KisOrderableAccountMixin):
        def __init__(self):
            self.kis = SimpleNamespace()
            self.account_number = "12345678-01"

    # Patch the mixin's class attribute
    original = KisOrderableAccountMixin.sell
    KisOrderableAccountMixin.sell = fake_sell

    try:
        acct = TestAccount()
        result = acct.sell("KRX", "005930", price=100)
        assert result == "sell-result"
        assert calls[0][1:] == ("KRX", "005930")
    finally:
        KisOrderableAccountMixin.sell = original


def test_order_forwards_correctly():
    """KisOrderableAccountMixin.order should forward to account_order."""
    from vmkis.adapter.account.order import KisOrderableAccountMixin

    calls = []

    def fake_order(
        self, market, symbol, order, price=None, qty=None, condition=None, execution=None, include_foreign=False
    ):
        calls.append(("order", market, symbol, order))
        return "order-result"

    class TestAccount(KisOrderableAccountMixin):
        def __init__(self):
            self.kis = SimpleNamespace()
            self.account_number = "12345678-01"

    # Patch the mixin's class attribute
    original = KisOrderableAccountMixin.order
    KisOrderableAccountMixin.order = fake_order

    try:
        acct = TestAccount()
        result = acct.order("KRX", "005930", "buy", price=100)
        assert result == "order-result"
        assert calls[0][1:] == ("KRX", "005930", "buy")
    finally:
        KisOrderableAccountMixin.order = original


def test_modify_and_cancel_forward():
    """KisOrderableAccountMixin modify/cancel should forward to order_modify functions."""
    from vmkis.adapter.account.order import KisOrderableAccountMixin

    modify_calls = []
    cancel_calls = []

    def fake_modify(self, order, price=..., qty=None, condition=..., execution=...):
        modify_calls.append(("modify", order))
        return "modify-result"

    def fake_cancel(self, order):
        cancel_calls.append(("cancel", order))
        return "cancel-result"

    class TestAccount(KisOrderableAccountMixin):
        def __init__(self):
            self.kis = SimpleNamespace()
            self.account_number = "12345678-01"

    # Patch the mixin's class attributes
    orig_mod = KisOrderableAccountMixin.modify
    orig_can = KisOrderableAccountMixin.cancel
    KisOrderableAccountMixin.modify = fake_modify
    KisOrderableAccountMixin.cancel = fake_cancel

    try:
        acct = TestAccount()
        fake_order = SimpleNamespace(number="12345")

        m_result = acct.modify(fake_order, price=200)
        assert m_result == "modify-result"
        assert modify_calls[0][1] == fake_order

        c_result = acct.cancel(fake_order)
        assert c_result == "cancel-result"
        assert cancel_calls[0][1] == fake_order
    finally:
        KisOrderableAccountMixin.modify = orig_mod
        KisOrderableAccountMixin.cancel = orig_can


def test_orderable_amount_and_pending_orders_forward():
    """orderable_amount and pending_orders should forward correctly."""
    from vmkis.adapter.account.order import KisOrderableAccountMixin

    amount_calls = []
    pending_calls = []

    def fake_amount(self, market, symbol, price=None, condition=None, execution=None):
        amount_calls.append(("amount", market, symbol))
        return "amount-result"

    def fake_pending(self, country=None):
        pending_calls.append(("pending", country))
        return "pending-result"

    class TestAccount(KisOrderableAccountMixin):
        def __init__(self):
            self.kis = SimpleNamespace()
            self.account_number = "12345678-01"

    # Patch the mixin's class attributes
    orig_amt = KisOrderableAccountMixin.orderable_amount
    orig_pend = KisOrderableAccountMixin.pending_orders
    KisOrderableAccountMixin.orderable_amount = fake_amount
    KisOrderableAccountMixin.pending_orders = fake_pending

    try:
        acct = TestAccount()

        amt_result = acct.orderable_amount("KRX", "SYM", price=100)
        assert amt_result == "amount-result"
        assert amount_calls[0][1:] == ("KRX", "SYM")

        pend_result = acct.pending_orders(country="US")
        assert pend_result == "pending-result"
        assert pending_calls[0][1] == "US"
    finally:
        KisOrderableAccountMixin.orderable_amount = orig_amt
        KisOrderableAccountMixin.pending_orders = orig_pend
