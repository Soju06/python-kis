import types
from datetime import date, datetime
from decimal import Decimal

import pytest

from vmkis.api.account import order_profit as op


def make_order(buy_amount, sell_amount, exchange_rate=1, symbol="AAA", time_kst=None):
    class Order0:
        pass

    o = Order0()
    o.buy_amount = Decimal(buy_amount)
    o.sell_amount = Decimal(sell_amount)
    o.exchange_rate = Decimal(exchange_rate)
    o.quantity = Decimal(1)
    o.symbol = symbol
    o.time_kst = time_kst or datetime(2020, 1, 1)

    # provide concrete profit value (Decimal) to avoid property/function issues
    o.profit = o.sell_amount - o.buy_amount
    return o


def test_kisorderprofitbase_properties():
    # instantiate base and set attributes directly
    inst = op.KisOrderProfitBase()
    inst.buy_amount = Decimal("100")
    inst.sell_amount = Decimal("120")
    inst.quantity = Decimal("2")
    inst.exchange_rate = Decimal("1")

    assert inst.qty == inst.quantity
    assert inst.profit == Decimal("20")
    # profit_rate = (profit / buy_amount) * 100 = 20/100*100 = 20
    assert inst.profit_rate == Decimal("20")


def test_kisorderprofitsbase_aggregation_and_indexing():
    o1 = make_order("10", "15", exchange_rate=1, symbol="AAA", time_kst=datetime(2020, 1, 2))
    o2 = make_order("20", "30", exchange_rate=2, symbol="BBB", time_kst=datetime(2020, 1, 1))

    coll = op.KisOrderProfitsBase()
    coll.orders = [o1, o2]

    # buy_amount = sum(order.buy_amount * order.exchange_rate)
    assert coll.buy_amount == Decimal(o1.buy_amount * o1.exchange_rate + o2.buy_amount * o2.exchange_rate)
    assert coll.sell_amount == Decimal(o1.sell_amount * o1.exchange_rate + o2.sell_amount * o2.exchange_rate)
    assert coll.profit == Decimal(o1.profit * o1.exchange_rate + o2.profit * o2.exchange_rate)

    # indexing by int and by symbol
    assert coll[0] is o1
    assert coll["BBB"] is o2
    with pytest.raises(IndexError):
        _ = coll[999]

    assert coll.order("AAA") is o1
    assert coll.order("NOPE") is None

    assert len(coll) == 2
    assert list(iter(coll)) == coll.orders


def test_domestic_order_profits_calls_fetch_and_returns(monkeypatch):
    class FakeKis:
        def __init__(self):
            self._calls = []
            self.paper = False

        # 이슈 #43·#44 이후 `domestic_order_profits` 는 `fetch_pages()` 를
        # 거친다. 실제 구현을 붙이면 `fetch(api=...)` 단언이 그대로 살고
        # 스펙 해석과 페이징 루프까지 함께 검증된다.
        def call(self, *args, **kwargs):
            from vmkis.kis import VmKis

            return VmKis.call(self, *args, **kwargs)

        def fetch_pages(self, *args, **kwargs):
            from vmkis.kis import VmKis

            return VmKis.fetch_pages(self, *args, **kwargs)

        def fetch(self, *args, **kwargs):
            self._calls.append((args, kwargs))
            # return a response-like object that the caller will accept
            return types.SimpleNamespace(orders=["X"], is_last=True, next_page=None)

    kis = FakeKis()

    # start > end should be swapped internally
    start = date(2024, 1, 10)
    end = date(2024, 1, 1)

    res = op.domestic_order_profits(kis, account="12345678", start=start, end=end)
    assert res.orders == ["X"]
    # verify fetch called with expected api
    called = kis._calls[-1][1]
    assert called["api"] == "TTTC8715R"


def test_foreign_order_fees_parses_output(monkeypatch):
    class FakeKis:
        def fetch(self, *args, **kwargs):
            # simulate result with output2.smtl_fee1
            return types.SimpleNamespace(output2=types.SimpleNamespace(smtl_fee1="12.34"))

        def __init__(self):
            self.paper = False

    kis = FakeKis()
    val = op.foreign_order_fees(kis, account="12345678", start=date(2024, 1, 1), end=date(2024, 1, 2), country="US")
    assert isinstance(val, Decimal)
    assert val == Decimal("12.34")


def test_order_profits_routes_and_integration(monkeypatch):
    # return objects for domestic and foreign
    dom = types.SimpleNamespace(orders=[make_order("1", "2", exchange_rate=1)], fees=Decimal("1"))
    fori = types.SimpleNamespace(orders=[make_order("2", "4", exchange_rate=1)], fees=Decimal("2"))

    monkeypatch.setattr(op, "domestic_order_profits", lambda *a, **k: dom)
    monkeypatch.setattr(op, "foreign_order_profits", lambda *a, **k: fori)

    kis = object()
    # country None -> integration
    res = op.order_profits(kis, account="12345678", start=date(2024, 1, 1), end=date(2024, 1, 2), country=None)
    assert isinstance(res, op.KisIntegrationOrderProfits)
    # country == KR -> domestic
    res2 = op.order_profits(kis, account="12345678", start=date(2024, 1, 1), end=date(2024, 1, 2), country="KR")
    assert res2 is dom
    # other country -> foreign
    res3 = op.order_profits(kis, account="12345678", start=date(2024, 1, 1), end=date(2024, 1, 2), country="US")
    assert res3 is fori
