from decimal import Decimal

import pytest

from vmkis.api.account import order as order_mod


def test_ensure_price_quantize():
    assert order_mod.ensure_price(100) == Decimal("100")
    # quantize with digit 2
    assert order_mod.ensure_price(Decimal("1.2345"), digit=2) == Decimal("1.23")


def test_ensure_quantity_quantize():
    assert order_mod.ensure_quantity(10) == Decimal("10")
    # Decimal quantize uses ROUND_HALF_EVEN by default in this context; expect 1.99
    assert order_mod.ensure_quantity(Decimal("1.987"), digit=2) == Decimal("1.99")


def test_to_domestic_and_foreign_order_condition_accept():
    # valid domestic
    assert order_mod.to_domestic_order_condition("best") == "best"
    # valid foreign
    assert order_mod.to_foreign_order_condition("MOO") == "MOO"


def test_to_domestic_order_condition_rejects():
    with pytest.raises(ValueError):
        order_mod.to_domestic_order_condition("MOO")


def test_to_foreign_order_condition_rejects():
    with pytest.raises(ValueError):
        order_mod.to_foreign_order_condition("best")


def test_resolve_domestic_order_condition_defaults():
    # unknown code returns default (True, None, None)
    assert order_mod.resolve_domestic_order_condition("ZZ") == (True, None, None)
    # known code
    assert order_mod.resolve_domestic_order_condition("01")[1] is None


def test_order_condition_invalid_raises():
    # pass an invalid condition to trigger the ValueError path
    with pytest.raises(ValueError):
        order_mod.order_condition(paper=False, market="KRX", order="buy", price=None, condition="__invalid__")
