from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from vmkis.api.account import daily_order as daily_mod
from vmkis.client.account import KisAccountNumber


def test_daily_orders_calls_domestic_and_foreign_and_constructs_integration():
    # Prepare fake return objects for domestic and foreign
    fake_domestic = SimpleNamespace(orders=[SimpleNamespace(time_kst=date(2024, 1, 1))])
    fake_foreign = SimpleNamespace(orders=[SimpleNamespace(time_kst=date(2024, 1, 2))])

    created = {}

    class FakeIntegration:
        def __init__(self, kis, account_number, dom, fori):
            created["args"] = (kis, account_number, dom, fori)

    with (
        patch.object(daily_mod, "domestic_daily_orders", return_value=fake_domestic) as pd,
        patch.object(daily_mod, "foreign_daily_orders", return_value=fake_foreign) as pf,
        patch.object(daily_mod, "KisIntegrationDailyOrders", new=FakeIntegration),
    ):
        kis = object()
        account = "12345678"
        daily_mod.daily_orders(kis, account, start=date(2024, 1, 1), end=date(2024, 1, 2), country=None)

    # Assert the internal domestic/foreign were called
    assert pd.called
    assert pf.called
    # Integration class was constructed with the domestic and foreign results
    assert "args" in created
    _, acct, dom_arg, for_arg = created["args"]
    assert isinstance(acct, KisAccountNumber)
    assert dom_arg is fake_domestic
    assert for_arg is fake_foreign


def test_daily_orders_kr_calls_domestic_only():
    fake_domestic = SimpleNamespace(orders=[])
    with patch.object(daily_mod, "domestic_daily_orders", return_value=fake_domestic) as pd:
        kis = object()
        account = "12345678"
        res = daily_mod.daily_orders(kis, account, start=date(2024, 1, 1), end=date(2024, 1, 2), country="KR")

    assert pd.called
    assert res is fake_domestic


def test_daily_orders_other_country_calls_foreign_only():
    fake_foreign = SimpleNamespace(orders=[])
    with patch.object(daily_mod, "foreign_daily_orders", return_value=fake_foreign) as pf:
        kis = object()
        account = "12345678"
        res = daily_mod.daily_orders(kis, account, start=date(2024, 1, 1), end=date(2024, 1, 2), country="US")

    assert pf.called
    assert res is fake_foreign
