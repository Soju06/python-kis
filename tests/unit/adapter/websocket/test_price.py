"""Unit tests for vmkis.adapter.websocket.price."""

from types import SimpleNamespace

import pytest

from vmkis.adapter.websocket.price import KisWebsocketQuotableProductMixin


def test_websocket_quotable_product_mixin_on_price():
    """KisWebsocketQuotableProductMixin.on should forward to on_product_price for 'price' event."""

    calls = []

    def fake_on(self, event, callback, where=None, once=False, extended=False):
        calls.append((event, callback, where, once, extended))
        return "price-ticket"

    class TestProduct(KisWebsocketQuotableProductMixin):
        pass

    orig_on = KisWebsocketQuotableProductMixin.on

    try:
        KisWebsocketQuotableProductMixin.on = fake_on

        prod = TestProduct()
        cb = lambda *_: None
        ticket = prod.on("price", cb, where=None, once=False, extended=True)
        assert ticket == "price-ticket"
        assert calls[0][0] == "price"
        assert calls[0][4] is True  # extended=True
    finally:
        KisWebsocketQuotableProductMixin.on = orig_on


def test_websocket_quotable_product_mixin_on_orderbook():
    """KisWebsocketQuotableProductMixin.on should forward to on_product_order_book for 'orderbook' event."""
    from vmkis.adapter.websocket.price import KisWebsocketQuotableProductMixin

    calls = []

    def fake_on(self, event, callback, where=None, once=False, extended=False):
        calls.append((event, callback, where, once, extended))
        return "orderbook-ticket"

    class TestProduct(KisWebsocketQuotableProductMixin):
        pass

    orig_on = KisWebsocketQuotableProductMixin.on

    try:
        KisWebsocketQuotableProductMixin.on = fake_on

        prod = TestProduct()
        cb = lambda *_: None
        ticket = prod.on("orderbook", cb, where=None, once=True, extended=False)
        assert ticket == "orderbook-ticket"
        assert calls[0][0] == "orderbook"
        assert calls[0][3] is True  # once=True
    finally:
        KisWebsocketQuotableProductMixin.on = orig_on


def test_mixin_on_raises_for_unknown_event():
    """Mixin.on should raise ValueError for unknown event types."""
    from vmkis.adapter.websocket.price import KisWebsocketQuotableProductMixin

    class TestProduct(KisWebsocketQuotableProductMixin):
        pass

    prod = TestProduct()

    try:
        prod.on("unknown", lambda *_: None)
    except ValueError as e:
        assert "Unknown event" in str(e)
    else:
        raise AssertionError("Expected ValueError for unknown event")


def test_websocket_quotable_product_mixin_once_price():
    """KisWebsocketQuotableProductMixin.once should call on_product_price with once=True."""
    from vmkis.adapter.websocket.price import KisWebsocketQuotableProductMixin

    calls = []

    def fake_once(self, event, callback, where=None, extended=False):
        calls.append((event, True))  # once is always True for once method
        return "price-ticket"

    class TestProduct(KisWebsocketQuotableProductMixin):
        pass

    orig_once = KisWebsocketQuotableProductMixin.once

    try:
        KisWebsocketQuotableProductMixin.once = fake_once

        prod = TestProduct()
        ticket = prod.once("price", lambda *_: None, extended=True)
        assert ticket == "price-ticket"
        assert calls[0][1] is True  # once=True
    finally:
        KisWebsocketQuotableProductMixin.once = orig_once


def test_websocket_quotable_product_mixin_once_orderbook():
    """KisWebsocketQuotableProductMixin.once should call on_product_order_book with once=True."""
    from vmkis.adapter.websocket.price import KisWebsocketQuotableProductMixin

    calls = []

    def fake_once(self, event, callback, where=None, extended=False):
        calls.append((event, True))  # once is always True for once method
        return "orderbook-ticket"

    class TestProduct(KisWebsocketQuotableProductMixin):
        pass

    orig_once = KisWebsocketQuotableProductMixin.once

    try:
        KisWebsocketQuotableProductMixin.once = fake_once

        prod = TestProduct()
        ticket = prod.once("orderbook", lambda *_: None)
        assert ticket == "orderbook-ticket"
        assert calls[0][1] is True  # once=True
    finally:
        KisWebsocketQuotableProductMixin.once = orig_once


def test_once_raises_for_unknown_event():
    """Mixin.once should raise ValueError for unknown event types."""
    from vmkis.adapter.websocket.price import KisWebsocketQuotableProductMixin

    class TestProduct(KisWebsocketQuotableProductMixin):
        def __init__(self):
            self.kis = SimpleNamespace()
            self.symbol = "005930"
            self.market = "KRX"

    prod = TestProduct()

    try:
        prod.once("invalid", lambda *_: None)
    except ValueError as e:
        assert "Unknown event" in str(e)
    else:
        raise AssertionError("Expected ValueError for unknown event in once")


# ---------------------------------------------------------------------------
# 실제 디스패치 경로 테스트
#
# 위쪽 테스트들은 `KisWebsocketQuotableProductMixin.on`/`.once` 자체를 페이크로
# 교체한 뒤 그 페이크가 호출됐는지를 확인한다. 즉 mixin의 실제 분기 코드를 한 줄도
# 실행하지 않는다(그래서 해당 구간이 미커버로 남아 있었다).
#
# 아래 테스트들은 mixin의 진짜 본문을 실행하고, 지연 import되는 하위 함수
# (`on_product_price`, `on_product_order_book`)를 대체해 전달 인자를 검증한다.
# ---------------------------------------------------------------------------


class Product(KisWebsocketQuotableProductMixin):
    """디스패치만 확인하므로 상품 속성은 필요 없다."""


@pytest.fixture
def spy(monkeypatch):
    """지연 import되는 하위 등록 함수를 기록용으로 교체합니다."""
    import vmkis.api.websocket.order_book as order_book_module
    import vmkis.api.websocket.price as price_module

    calls = {}

    def make(name):
        def fake(self, callback, *, where=None, once=False, extended=False):
            calls[name] = {
                "self": self,
                "callback": callback,
                "where": where,
                "once": once,
                "extended": extended,
            }
            return f"{name}-ticket"

        return fake

    monkeypatch.setattr(price_module, "on_product_price", make("price"))
    monkeypatch.setattr(order_book_module, "on_product_order_book", make("orderbook"))
    return calls


def test_on_price_dispatches_to_on_product_price(spy):
    """On("price", ...)는 on_product_price로 인자를 그대로 전달한다."""
    product = Product()
    callback = lambda *_: None
    condition = object()

    ticket = product.on("price", callback, where=condition, once=False, extended=True)

    assert ticket == "price-ticket"
    assert spy["price"] == {
        "self": product,
        "callback": callback,
        "where": condition,
        "once": False,
        "extended": True,
    }
    assert "orderbook" not in spy


def test_on_orderbook_dispatches_to_on_product_order_book(spy):
    """On("orderbook", ...)는 on_product_order_book으로 전달한다."""
    product = Product()
    callback = lambda *_: None

    ticket = product.on("orderbook", callback, once=True)

    assert ticket == "orderbook-ticket"
    assert spy["orderbook"]["once"] is True
    assert spy["orderbook"]["extended"] is False
    assert "price" not in spy


def test_on_rejects_unknown_event(spy):
    """알 수 없는 이벤트는 ValueError."""
    with pytest.raises(ValueError, match="Unknown event: unknown"):
        Product().on("unknown", lambda *_: None)

    assert not spy


@pytest.mark.parametrize("event", ["price", "orderbook"])
def test_once_forces_once_true(spy, event):
    """Once()는 이벤트 종류와 무관하게 once=True로 등록한다."""
    product = Product()

    ticket = product.once(event, lambda *_: None, extended=True)

    assert ticket == f"{event}-ticket"
    assert spy[event]["once"] is True
    assert spy[event]["extended"] is True


def test_once_rejects_unknown_event(spy):
    """Once()도 알 수 없는 이벤트는 ValueError."""
    with pytest.raises(ValueError, match="Unknown event: invalid"):
        Product().once("invalid", lambda *_: None)

    assert not spy
