import types

import pytest

from vmkis.api.account import order_modify as om
from vmkis.client.exceptions import KisAPIError


class FakeOrder:
    def __init__(self, *, account_number="12345678", branch="001", number="1", symbol="AAA", market="KRX", type_="buy"):
        self.account_number = account_number
        self.branch = branch
        self.number = number
        self.symbol = symbol
        self.market = market
        self.type = type_


class FakeKis:
    def __init__(self, paper=False):
        self.paper = paper
        self._fetch_calls = []

    # 이슈 #43 이후 api/ 는 `call()` 을 거친다. 실제 구현을 붙여
    # 스펙 해석(TR ID·도메인)까지 함께 검증한다.
    def call(self, *args, **kwargs):
        from vmkis.kis import VmKis

        return VmKis.call(self, *args, **kwargs)

    def fetch(self, *args, **kwargs):
        # record call and return a sentinel
        self._fetch_calls.append((args, kwargs))
        return {
            "called_args": args,
            "called_kwargs": kwargs,
        }


def test_domestic_modify_virtual_raises():
    kis = FakeKis(paper=True)
    order = FakeOrder()

    with pytest.raises(NotImplementedError):
        om.domestic_modify_order(kis, order)


def test_domestic_modify_qty_zero_raises():
    kis = FakeKis(paper=False)
    order = FakeOrder()

    with pytest.raises(ValueError):
        om.domestic_modify_order(kis, order, qty=0)


def test_domestic_modify_order_not_found_raises(monkeypatch):
    kis = FakeKis()
    order = FakeOrder()

    class Pending:
        def order(self, _):
            return None

    def fake_pending(k, account, country):
        return Pending()

    monkeypatch.setattr("vmkis.api.account.pending_order.pending_orders", fake_pending)

    with pytest.raises(ValueError):
        om.domestic_modify_order(kis, order)


def test_domestic_modify_price_setting_uses_quote_and_fetch(monkeypatch):
    kis = FakeKis()
    order = FakeOrder()

    sample_info = types.SimpleNamespace(price=50, qty=10, condition=None, execution=None, branch="001", number="1")
    sample_info.type = "buy"

    class Pending:
        def order(self, _):
            return sample_info

    def fake_pending(k, account, country):
        return Pending()

    monkeypatch.setattr("vmkis.api.account.pending_order.pending_orders", fake_pending)

    # make order_condition return a price-setting demanding 'upper' limit
    monkeypatch.setattr(om, "order_condition", lambda **kwargs: ("01", "upper", None))

    # quote returns object with high_limit/low_limit
    monkeypatch.setattr(om, "quote", lambda self, symbol, market: types.SimpleNamespace(high_limit=123, low_limit=1))

    om.domestic_modify_order(kis, order, price=..., qty=..., condition=..., execution=...)

    # fetch should have been called and ORD_UNPR should equal '123' (from high_limit)
    assert kis._fetch_calls, "fetch was not called"
    called = kis._fetch_calls[-1][1]
    assert called["body"]["ORD_UNPR"] == "123"


def test_foreign_modify_qty_zero_raises():
    kis = FakeKis()
    order = FakeOrder(market="NASDAQ")

    with pytest.raises(ValueError):
        om.foreign_modify_order(kis, order, qty=0)


def test_foreign_modify_missing_api_raises(monkeypatch):
    kis = FakeKis()
    # choose a market that is not present in mapping
    order = FakeOrder(market="UNKNOWN")

    sample_info = types.SimpleNamespace(price=10, qty=1, condition=None, execution=None, branch="001", number="1")

    class Pending:
        def order(self, _):
            return sample_info

    monkeypatch.setattr("vmkis.api.account.pending_order.pending_orders", lambda self, account, country: Pending())
    monkeypatch.setattr(om, "order_condition", lambda **kwargs: ("01", None, None))

    with pytest.raises(ValueError):
        om.foreign_modify_order(kis, order)


def test_foreign_cancel_missing_api_raises():
    kis = FakeKis()
    order = FakeOrder(market="UNKNOWN")

    with pytest.raises(ValueError):
        om.foreign_cancel_order(kis, order)


def test_foreign_daytime_modify_market_not_supported():
    kis = FakeKis()
    order = FakeOrder(market="NOT_DAYTIME")

    with pytest.raises(ValueError):
        om.foreign_daytime_modify_order(kis, order)


def test_modify_order_routes_and_handles_kisapierror(monkeypatch):
    kis = FakeKis()
    order = FakeOrder(market="NASDAQ")

    called = {}

    def fake_domestic(*args, **kwargs):
        called["domestic"] = True

    def fake_foreign(*args, **kwargs):
        called["foreign"] = True

        # construct a minimal fake response to build a KisAPIError with msg_cd set
        class FakeResp:
            def __init__(self):
                self.status_code = 400
                self.headers = {"tr_id": "T", "gt_uid": "G"}
                self.request = types.SimpleNamespace(method="POST", url="https://api", headers={}, body=None)
                self.text = "err"
                self.reason = "Bad Request"

        data = {"msg_cd": "APBK0918", "rt_cd": "1", "msg1": "err"}
        raise KisAPIError(data, FakeResp())

    def fake_daytime(*args, **kwargs):
        called["daytime"] = True
        return "daytime-result"

    monkeypatch.setattr(om, "domestic_modify_order", fake_domestic)
    monkeypatch.setattr(om, "foreign_modify_order", fake_foreign)
    monkeypatch.setattr(om, "foreign_daytime_modify_order", fake_daytime)

    # route to foreign branch and handle KisAPIError path
    res = om.modify_order(kis, order)
    assert called.get("foreign")
    assert called.get("daytime")
    assert res == "daytime-result"


def test_account_modify_and_cancel_forward_to_kis(monkeypatch):
    class AccountProto:
        def __init__(self):
            self.kis = FakeKis()

    acc = AccountProto()
    order = FakeOrder()

    monkeypatch.setattr(om, "modify_order", lambda kis, **kwargs: (kis, kwargs))
    monkeypatch.setattr(om, "cancel_order", lambda kis, **kwargs: (kis, kwargs))

    r1 = om.account_modify_order(acc, order)
    r2 = om.account_cancel_order(acc, order)

    assert r1[0] is acc.kis
    assert r2[0] is acc.kis


def test_domestic_cancel_api_code_for_virtual_flag():
    order = FakeOrder()

    kis = FakeKis(paper=False)
    om.domestic_cancel_order(kis, order)
    assert kis._fetch_calls[-1][1]["api"] == "TTTC0803U"

    kis_v = FakeKis(paper=True)
    om.domestic_cancel_order(kis_v, order)
    assert kis_v._fetch_calls[-1][1]["api"] == "VTTC0803U"


def test_foreign_modify_success_calls_get_market_code_and_fetch(monkeypatch):
    kis = FakeKis(paper=False)
    order = FakeOrder(market="NASDAQ")

    sample_info = types.SimpleNamespace(price=10, qty=5, condition=None, execution=None, branch="001", number="1")
    sample_info.type = "buy"

    monkeypatch.setattr(
        "vmkis.api.account.pending_order.pending_orders",
        lambda self, account, country: types.SimpleNamespace(order=lambda o: sample_info),
    )
    monkeypatch.setattr(om, "order_condition", lambda **kwargs: ("01", None, None))
    monkeypatch.setattr(om, "get_market_code", lambda market: "MK")

    om.foreign_modify_order(kis, order)
    called = kis._fetch_calls[-1][1]
    # api mapping for (not self.paper, 'NASDAQ', 'modify') -> True key -> 'TTTT1004U'
    assert called["api"] == "TTTT1004U"
    assert called["body"]["OVRS_EXCG_CD"] == "MK"


def test_foreign_modify_price_setting_uses_quote(monkeypatch):
    kis = FakeKis(paper=False)
    order = FakeOrder(market="NASDAQ")

    sample_info = types.SimpleNamespace(price=10, qty=5, condition=None, execution=None, branch="001", number="1")
    sample_info.type = "buy"

    monkeypatch.setattr(
        "vmkis.api.account.pending_order.pending_orders",
        lambda self, account, country: types.SimpleNamespace(order=lambda o: sample_info),
    )
    monkeypatch.setattr(om, "order_condition", lambda **kwargs: ("01", "upper", None))
    monkeypatch.setattr(om, "quote", lambda self, symbol, market: types.SimpleNamespace(high_limit=999, low_limit=1))

    om.foreign_modify_order(kis, order)
    called = kis._fetch_calls[-1][1]
    assert called["body"]["OVRS_ORD_UNPR"] == "999"


def test_foreign_daytime_modify_quote_path_and_price_selection(monkeypatch):
    # pick a market that is in DAYTIME_MARKETS
    market = next(iter(om.DAYTIME_MARKETS))
    kis = FakeKis(paper=False)
    order = FakeOrder(market=market)

    # order_info with no price but with qty
    sample_info = types.SimpleNamespace(price=None, qty=2, condition=None, execution=None, branch="001", number="1")
    sample_info.type = "buy"

    monkeypatch.setattr(
        "vmkis.api.account.pending_order.pending_orders",
        lambda self, account, country: types.SimpleNamespace(order=lambda o: sample_info),
    )
    monkeypatch.setattr(om, "ensure_price", lambda p, *args, **kwargs: p)
    monkeypatch.setattr(
        om, "quote", lambda self, symbol, market, extended=False: types.SimpleNamespace(high_limit=500, low_limit=10)
    )

    om.foreign_daytime_modify_order(kis, order, price=None, qty=None)
    called = kis._fetch_calls[-1][1]
    # code uses 'order == "buy"' comparison which is False for object, so low_limit used
    assert called["body"]["OVRS_ORD_UNPR"] == "10"


def test_foreign_daytime_cancel_order_success_and_virtual(monkeypatch):
    market = next(iter(om.DAYTIME_MARKETS))
    kis = FakeKis(paper=False)
    order = FakeOrder(market=market)

    sample_info = types.SimpleNamespace(qty=7)
    sample_info.type = "buy"

    monkeypatch.setattr(
        "vmkis.api.account.pending_order.pending_orders",
        lambda self, account, country: types.SimpleNamespace(order=lambda o: sample_info),
    )

    om.foreign_daytime_cancel_order(kis, order)
    called = kis._fetch_calls[-1][1]
    assert called["body"]["ORD_QTY"] == "7"

    kis_v = FakeKis(paper=True)
    with pytest.raises(NotImplementedError):
        om.foreign_daytime_cancel_order(kis_v, order)


def test_cancel_order_handles_kisapierror_and_routes_to_daytime(monkeypatch):
    kis = FakeKis()
    order = FakeOrder(market="NASDAQ")

    def fake_foreign(*args, **kwargs):
        data = {"msg_cd": "APBK0918", "rt_cd": "1", "msg1": "err"}

        class FakeResp:
            def __init__(self):
                self.status_code = 400
                self.headers = {}
                self.request = types.SimpleNamespace(method="POST", url="https://api", headers={}, body=None)
                self.text = "err"
                self.reason = "Bad Request"

        raise KisAPIError(data, FakeResp())

    monkeypatch.setattr(om, "foreign_cancel_order", fake_foreign)
    monkeypatch.setattr(om, "foreign_daytime_cancel_order", lambda *a, **kw: "daytime-cancel")

    res = om.cancel_order(kis, order)
    assert res == "daytime-cancel"
