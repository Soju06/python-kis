"""Unit tests for vmkis.adapter.account_product.order_modify"""

from types import SimpleNamespace


def test_cancelable_order_mixin_cancel():
    """KisCancelableOrderMixin.cancel should forward to cancel_order."""
    from vmkis.adapter.account_product.order_modify import KisCancelableOrderMixin

    calls = []

    def fake_cancel(kis, order):
        calls.append(("cancel", order))
        return "cancel-result"

    class TestOrder(KisCancelableOrderMixin):
        def __init__(self):
            self.kis = SimpleNamespace()

    import vmkis.api.account.order_modify as mod_api

    original = mod_api.cancel_order
    mod_api.cancel_order = fake_cancel

    try:
        order = TestOrder()
        result = order.cancel()
        assert result == "cancel-result"
        assert len(calls) == 1
        assert calls[0][1] is order
    finally:
        mod_api.cancel_order = original


def test_modifyable_order_mixin_modify():
    """KisModifyableOrderMixin.modify should forward to modify_order with params."""
    from vmkis.adapter.account_product.order_modify import KisModifyableOrderMixin

    calls = []

    def fake_modify(kis, order, price=..., qty=None, condition=..., execution=...):
        calls.append(("modify", order, price, qty, condition, execution))
        return "modify-result"

    class TestOrder(KisModifyableOrderMixin):
        def __init__(self):
            self.kis = SimpleNamespace()

    import vmkis.api.account.order_modify as mod_api

    original = mod_api.modify_order
    mod_api.modify_order = fake_modify

    try:
        order = TestOrder()
        result = order.modify(price=200, qty=10, condition=None, execution="IOC")
        assert result == "modify-result"
        assert len(calls) == 1
        assert calls[0][1] is order
        assert calls[0][2:] == (200, 10, None, "IOC")
    finally:
        mod_api.modify_order = original


def test_orderable_order_mixin_combines_cancel_and_modify():
    """KisOrderableOrderMixin should inherit both cancel and modify."""
    from vmkis.adapter.account_product.order_modify import KisOrderableOrderMixin

    cancel_calls = []
    modify_calls = []

    def fake_cancel(kis, order):
        cancel_calls.append("cancel")
        return "cancel-result"

    def fake_modify(kis, order, price=..., qty=None, condition=..., execution=...):
        modify_calls.append("modify")
        return "modify-result"

    class TestOrder(KisOrderableOrderMixin):
        def __init__(self):
            self.kis = SimpleNamespace()

    import vmkis.api.account.order_modify as mod_api

    orig_cancel = mod_api.cancel_order
    orig_modify = mod_api.modify_order
    mod_api.cancel_order = fake_cancel
    mod_api.modify_order = fake_modify

    try:
        order = TestOrder()

        c_result = order.cancel()
        assert c_result == "cancel-result"
        assert len(cancel_calls) == 1

        m_result = order.modify(price=100)
        assert m_result == "modify-result"
        assert len(modify_calls) == 1
    finally:
        mod_api.cancel_order = orig_cancel
        mod_api.modify_order = orig_modify
