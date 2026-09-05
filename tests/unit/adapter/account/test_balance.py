"""Unit tests for vmkis.adapter.account.balance"""

from datetime import date
from types import SimpleNamespace


def test_balance_forwards_to_account_balance():
    """KisQuotableAccountMixin.balance should forward to account_balance with country param."""
    from vmkis.adapter.account.balance import KisQuotableAccountMixin

    calls = []

    def fake_balance(self, country=None):
        calls.append(("balance", country))
        return "balance-result"

    # Create a test instance with the mixin
    class TestAccount(KisQuotableAccountMixin):
        def __init__(self):
            self.kis = SimpleNamespace()
            self.account_number = "12345678-01"

    # Patch the mixin's class attribute directly
    original = KisQuotableAccountMixin.balance
    KisQuotableAccountMixin.balance = fake_balance

    try:
        acct = TestAccount()
        result = acct.balance(country="US")
        assert result == "balance-result"
        assert calls == [("balance", "US")]
    finally:
        KisQuotableAccountMixin.balance = original


def test_daily_orders_forwards_correctly():
    """KisQuotableAccountMixin.daily_orders should forward to account_daily_orders."""
    from vmkis.adapter.account.balance import KisQuotableAccountMixin

    calls = []

    def fake_daily_orders(self, start, end=None, country=None):
        calls.append(("daily_orders", start, end, country))
        return "orders-result"

    class TestAccount(KisQuotableAccountMixin):
        def __init__(self):
            self.kis = SimpleNamespace()
            self.account_number = "12345678-01"

    # Patch the mixin's class attribute directly
    original = KisQuotableAccountMixin.daily_orders
    KisQuotableAccountMixin.daily_orders = fake_daily_orders

    try:
        acct = TestAccount()
        start_date = date(2023, 1, 1)
        end_date = date(2023, 1, 31)
        result = acct.daily_orders(start=start_date, end=end_date, country="KR")
        assert result == "orders-result"
        assert calls == [("daily_orders", start_date, end_date, "KR")]
    finally:
        KisQuotableAccountMixin.daily_orders = original


def test_profits_forwards_correctly():
    """KisQuotableAccountMixin.profits should forward to account_order_profits."""
    from vmkis.adapter.account.balance import KisQuotableAccountMixin

    calls = []

    def fake_profits(self, start, end=None, country=None):
        calls.append(("profits", start, end, country))
        return "profits-result"

    class TestAccount(KisQuotableAccountMixin):
        def __init__(self):
            self.kis = SimpleNamespace()
            self.account_number = "12345678-01"

    # Patch the mixin's class attribute directly
    original = KisQuotableAccountMixin.profits
    KisQuotableAccountMixin.profits = fake_profits

    try:
        acct = TestAccount()
        start_date = date(2023, 1, 1)
        result = acct.profits(start=start_date, country="US")
        assert result == "profits-result"
        assert calls == [("profits", start_date, None, "US")]
    finally:
        KisQuotableAccountMixin.profits = original
