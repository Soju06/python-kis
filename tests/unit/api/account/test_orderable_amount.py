import types
from decimal import Decimal

from vmkis.api.account import orderable_amount as oa


def test_domestic_foreign_amount_and_foreign_quantity(monkeypatch):
    # instantiate a domestic response and ensure foreign_amount sums correctly
    inst = oa.KisDomesticOrderableAmount(
        account_number="1234",
        symbol="AAA",
        market="KRX",
        price=Decimal(100),
        condition=None,
        execution=None,
    )

    # set amounts directly
    inst.amount = Decimal("1000")
    inst.foreign_only_amount = Decimal("250")

    # monkeypatch the internal _domestic_orderable_amount used by .foreign_quantity
    monkeypatch.setattr(oa, "_domestic_orderable_amount", lambda *a, **k: types.SimpleNamespace(quantity=Decimal("5")))
    # set a kis instance (some code expects inst.kis)
    inst.kis = types.SimpleNamespace(paper=False)

    assert inst.foreign_amount == Decimal("1250")
    assert inst.foreign_quantity == Decimal("5")


def test_condition_kor_calls_order_condition(monkeypatch):
    # For domestic, condition_kor uses order_condition(...)[-1]
    inst = oa.KisDomesticOrderableAmount(
        account_number="1234",
        symbol="AAA",
        market="KRX",
        price=None,
        condition="best",
        execution=None,
    )

    monkeypatch.setattr(oa, "order_condition", lambda **kwargs: ("C", "설명"))
    # domestic property should pick last element
    assert inst.condition_kor == "설명"

    # For foreign, ensure the paper flag is passed through to order_condition
    finst = oa.KisForeignOrderableAmount(
        account_number="1234",
        symbol="BBB",
        market="NASDAQ",
        price=None,
        unit_price=Decimal(10),
        condition="LOO",
        execution=None,
    )

    # supply kis with paper True to validate parameter path
    finst.kis = types.SimpleNamespace(paper=True)

    captured = {}

    def fake_order_condition(**kwargs):
        captured.update(kwargs)
        return ("X", "외국설명")

    monkeypatch.setattr(oa, "order_condition", fake_order_condition)

    assert finst.condition_kor == "외국설명"
    # check that paper and market were forwarded
    assert captured.get("paper") is True
    assert captured.get("market") == "NASDAQ"
