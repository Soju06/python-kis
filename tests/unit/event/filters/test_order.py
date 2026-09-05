from types import SimpleNamespace

import pytest

from vmkis.event.filters.order import (
    KisOrderNumberEventFilter,
    KisSimpleOrderNumber,
)
from vmkis.event.subscription import KisSubscriptionEventArgs


def test_init_string_requires_all_fields():
    # missing market
    with pytest.raises(ValueError):
        KisOrderNumberEventFilter("SYM")

    # missing branch
    with pytest.raises(ValueError):
        KisOrderNumberEventFilter("SYM", "MKT")

    # missing number
    with pytest.raises(ValueError):
        KisOrderNumberEventFilter("SYM", "MKT", "BR")

    # missing account
    with pytest.raises(ValueError):
        KisOrderNumberEventFilter("SYM", "MKT", "BR", "1")


def make_value_order():
    # simple value object used by the filter
    account = SimpleNamespace(id="A123")
    return KisSimpleOrderNumber(symbol="AAA", market="MKT", branch="BR", number="10", account=account)


def test_filter_ignores_non_realtime_response():
    value = make_value_order()
    f = KisOrderNumberEventFilter(value)

    # response without order_number should be ignored (filter returns True)
    resp = SimpleNamespace()  # no order_number attribute
    args = KisSubscriptionEventArgs(tr=None, response=resp)

    assert f.__filter__(None, None, args) is True


def test_filter_matches_and_non_matches(monkeypatch):
    value = make_value_order()
    f = KisOrderNumberEventFilter(value)

    # create a response that is considered a realtime execution by monkeypatching
    class Resp:
        def __init__(self, order_number):
            self.order_number = order_number

    # monkeypatch the protocol name in module to a simple base class so isinstance passes
    import vmkis.event.filters.order as order_mod

    monkeypatch.setattr(order_mod, "KisSimpleRealtimeExecution", Resp)

    # matching order -> filter should return False (do not ignore)
    match_order = SimpleNamespace(
        symbol="AAA", market="MKT", foreign=False, branch="BR", number="10", account_number=value.account_number
    )
    args_match = KisSubscriptionEventArgs(tr=None, response=Resp(match_order))
    assert f.__filter__(None, None, args_match) is False

    # different number -> ignored
    nonmatch_order = SimpleNamespace(
        symbol="AAA", market="MKT", foreign=False, branch="BR", number="11", account_number=value.account_number
    )
    args_nonmatch = KisSubscriptionEventArgs(tr=None, response=Resp(nonmatch_order))
    assert f.__filter__(None, None, args_nonmatch) is True
