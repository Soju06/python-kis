from types import SimpleNamespace

from vmkis.client.messaging import KisWebsocketTR
from vmkis.event.handler import KisEventArgs
from vmkis.event.subscription import (
    KisSubscribedEventArgs,
    KisSubscriptionEventArgs,
    KisUnsubscribedEventArgs,
)


def test_kis_subscribed_event_args_stores_tr():
    tr = KisWebsocketTR("T1", "K1")
    ev = KisSubscribedEventArgs(tr)

    # stores the TR and is a KisEventArgs
    assert ev.tr == tr
    assert isinstance(ev, KisEventArgs)


def test_kis_unsubscribed_event_args_stores_tr():
    tr = KisWebsocketTR("T2", "")
    ev = KisUnsubscribedEventArgs(tr)

    assert ev.tr == tr
    assert isinstance(ev, KisEventArgs)


def test_kis_subscription_event_args_stores_response_and_tr():
    tr = KisWebsocketTR("T3", "K3")
    response = SimpleNamespace(value=123)
    ev = KisSubscriptionEventArgs(tr, response)

    assert ev.tr == tr
    # response preserved
    assert ev.response is response
    assert isinstance(ev, KisEventArgs)
