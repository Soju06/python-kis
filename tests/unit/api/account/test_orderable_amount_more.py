import types
from decimal import Decimal

import pytest

from vmkis.api.account import orderable_amount as oa


def test__domestic_orderable_amount_calls_fetch_and_uses_quote(monkeypatch):
    # prepare fake order_condition to require quote
    monkeypatch.setattr(oa, "order_condition", lambda **kwargs: ("C", True, None))

    # fake quote returns close Decimal
    monkeypatch.setattr(
        oa, "quote", lambda self, symbol, market, extended=False: types.SimpleNamespace(close=Decimal("123.45"))
    )

    # fake kis with fetch that returns the provided response_type
    class FakeKis:
        def __init__(self):
            self.paper = False
            self.last_fetch = None

        # 이슈 #43 이후 api/ 는 `call()` 을 거친다. 실제 구현을 붙여
        # 스펙 해석(TR ID·도메인)까지 함께 검증한다.
        def call(self, *args, **kwargs):
            from vmkis.kis import VmKis

            return VmKis.call(self, *args, **kwargs)

        def fetch(self, *args, **kwargs):
            self.last_fetch = {"args": args, "kwargs": kwargs}
            return kwargs.get("response_type")

    kis = FakeKis()

    res = oa._domestic_orderable_amount(
        kis, account="12345678", symbol="AAA", price=None, condition=None, execution=None
    )

    # fetch should have been called and returned a KisDomesticOrderableAmount
    assert isinstance(res, oa.KisDomesticOrderableAmount)
    assert kis.last_fetch is not None
    # api should be TTTC8908R when not paper
    assert kis.last_fetch["kwargs"]["api"] == "TTTC8908R"


def test__domestic_orderable_amount_value_errors():
    with pytest.raises(ValueError):
        oa._domestic_orderable_amount(object(), account="", symbol="AAA")

    with pytest.raises(ValueError):
        oa._domestic_orderable_amount(object(), account="123", symbol="")


def test_foreign_orderable_amount_unit_price_and_order_condition(monkeypatch):
    # ensure order_condition is called for non-extended
    called = {}

    def fake_order_condition(**kwargs):
        called.update(kwargs)
        return ("C", False, None)

    monkeypatch.setattr(oa, "order_condition", fake_order_condition)

    # fake quote when price is None
    monkeypatch.setattr(
        oa, "quote", lambda self, symbol, market, extended=False: types.SimpleNamespace(close=Decimal("9.99"))
    )

    class FakeKis:
        def __init__(self):
            self.paper = False
            self.last = None

        # 이슈 #43 이후 api/ 는 `call()` 을 거친다. 실제 구현을 붙여
        # 스펙 해석(TR ID·도메인)까지 함께 검증한다.
        def call(self, *args, **kwargs):
            from vmkis.kis import VmKis

            return VmKis.call(self, *args, **kwargs)

        def fetch(self, *args, **kwargs):
            self.last = kwargs
            return kwargs.get("response_type")

    kis = FakeKis()

    res = oa.foreign_orderable_amount(
        kis, account="12345678", market="NASDAQ", symbol="XYZ", price=None, condition=None, execution=None
    )
    assert isinstance(res, oa.KisForeignOrderableAmount)
    assert called.get("paper") is False
    # API for non-paper should be TTTS3007R
    assert kis.last["api"] == "TTTS3007R"


def test_orderable_amount_dispatch_and_wrappers(monkeypatch):
    # dispatch to domestic when market == 'KRX'
    monkeypatch.setattr(oa, "domestic_orderable_amount", lambda *a, **k: "DOM")
    monkeypatch.setattr(oa, "foreign_orderable_amount", lambda *a, **k: "FOR")

    assert oa.orderable_amount(object(), account="123", market="KRX", symbol="A") == "DOM"
    assert oa.orderable_amount(object(), account="123", market="NASDAQ", symbol="A") == "FOR"

    # account wrapper should forward to orderable_amount
    class A:
        def __init__(self):
            self.kis = "KIS"
            self.account_number = "ACC"

    called = {}

    def fake_orderable_amount(kis, account, market, symbol, price=None, condition=None, execution=None):
        called["kis"] = kis
        called["account"] = account
        return "X"

    monkeypatch.setattr(oa, "orderable_amount", fake_orderable_amount)

    acc = A()
    res = oa.account_orderable_amount(acc, market="KRX", symbol="A")
    assert res == "X"
    assert called["kis"] == "KIS"

    # account_product wrapper
    class P:
        def __init__(self):
            self.kis = "KIS"
            self.account_number = "ACC"
            self.market = "KRX"
            self.symbol = "SYM"

    p = P()
    # reuse fake_orderable_amount via monkeypatch
    res2 = oa.account_product_orderable_amount(p, price=None, condition=None, execution=None)
    assert res2 == "X"
