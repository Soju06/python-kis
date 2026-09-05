import pytest

from vmkis.event.handler import (
    KisEventArgs,
    KisEventHandler,
    KisLambdaEventCallback,
    KisLambdaEventFilter,
    KisMultiEventFilter,
)


def test_kis_lambda_event_filter_basics():
    f = KisLambdaEventFilter(lambda s, e: True)
    # __filter__ should call underlying callable
    assert f.__filter__(None, "S", KisEventArgs()) is True
    # hash/representation
    assert hash(f) == hash(f.filter)
    assert "KisLambdaEventFilter" in repr(f)


def test_kis_multi_event_filter_or_and():
    f_true = KisLambdaEventFilter(lambda s, e: True)
    f_false = KisLambdaEventFilter(lambda s, e: False)

    # OR gate: any true -> True
    mf_or = KisMultiEventFilter(f_true, f_false, gate="or")
    assert mf_or.__filter__(None, "S", KisEventArgs()) is True

    # AND gate: all true -> False because one is false
    mf_and = KisMultiEventFilter(f_true, f_false, gate="and")
    assert mf_and.__filter__(None, "S", KisEventArgs()) is False

    # support plain callables as filters
    mf_callable = KisMultiEventFilter(lambda s, e: False, gate="or")
    assert mf_callable.__filter__(None, "S", KisEventArgs()) is False


def test_kis_lambda_event_callback_invoke_and_filter_and_once():
    # simple invocation path
    handler = KisEventHandler()
    called = []

    def cb(sender, e):
        called.append((sender, e))

    lec = KisLambdaEventCallback(cb)
    # call the callback directly to test KisLambdaEventCallback.__callback__ behavior
    lec.__callback__(handler, "S1", KisEventArgs())
    assert len(called) == 1
    assert called[0][0] == "S1"

    # where filter that returns True should indicate filtered
    called.clear()
    lec2 = KisLambdaEventCallback(cb, where=KisLambdaEventFilter(lambda s, e: True))
    assert lec2.__filter__(handler, "S2", KisEventArgs()) is True

    # once: callback removed after first invocation
    called.clear()
    handler3 = KisEventHandler()

    def cb3(sender, e):
        called.append((sender, e))

    ticket = handler3.on(cb3, once=True)
    handler3.invoke("S3", KisEventArgs())
    handler3.invoke("S3", KisEventArgs())
    assert len(called) == 1
    # ticket.once should reflect the callback once property
    assert ticket.once is True


def test_event_ticket_properties_and_unsubscribe_and_context_manager():
    handler = KisEventHandler()

    called = []

    def cb(sender, e):
        called.append((sender, e))

    ticket = handler.on(cb)
    # ticket reflects registration
    assert ticket.registered is True
    # once property for plain on() without once arg is False
    assert ticket.once is False

    # unsubscribing removes handler
    ticket.unsubscribe()
    assert ticket.registered is False

    # context manager should unsubscribe on exit
    ticket2 = handler.on(cb)
    with ticket2:
        assert ticket2.registered is True
    assert ticket2.registered is False


def test_event_handler_add_remove_clear_and_operators():
    handler = KisEventHandler()

    def cb(sender, e):
        pass

    # add returns a ticket and contains callback
    t = handler.add(cb)  # noqa: F841 - 티켓을 붙잡지 않으면 GC가 구독을 해지한다
    assert cb in handler
    # __len__ and __bool__
    assert len(handler) >= 1
    assert bool(handler) is True

    # remove non-existent should not raise
    handler.remove(lambda a, b: None)

    # clear empties
    handler.clear()
    assert len(handler) == 0

    # iadd and isub
    handler += cb
    assert cb in handler
    handler -= cb
    assert cb not in handler


def test_handler_call_and_iter_and_repr_and_eq_hash():
    a = KisEventHandler()
    b = KisEventHandler()

    def cb(sender, e):
        pass

    a += cb
    b += cb
    # handlers equality
    assert a == b
    # __hash__ will attempt to hash the handlers set and therefore raises TypeError
    with pytest.raises(TypeError):
        hash(a)
    # __call__ delegates to invoke
    invoked = []

    def spy(s, e):
        invoked.append((s, e))

    a.clear()
    a += spy
    a("S", KisEventArgs())
    assert invoked and invoked[0][0] == "S"
