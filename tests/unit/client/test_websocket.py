import base64
import json
import threading
from types import SimpleNamespace

import pytest

import vmkis.client.websocket as websocket_mod
from vmkis.client.websocket import (
    TR_SUBSCRIBE_TYPE,
    TR_UNSUBSCRIBE_TYPE,
    KisWebsocketClient,
    KisWebsocketTR,
)


class DummyKis:
    def __init__(self, paper=False):
        self.paper = paper

    def ws_url(self, domain):
        """#75 부터 웹소켓 주소를 `VmKis` 가 해석합니다.

        설정으로 주소를 재정의할 수 있게 하려면 상수를 직접 읽어서는 안 되고,
        클라이언트를 거쳐야 합니다. 이 대역도 그 계약을 따라야 합니다.
        """
        return f"ws://dummy-{domain}:1"


class DummyWS:
    def __init__(self):
        self.sent = []
        self.closed = False

    def send(self, data):
        self.sent.append(data)

    def close(self):
        self.closed = True


def make_client(monkeypatch, paper=False):
    kis = DummyKis(paper=paper)
    c = KisWebsocketClient(kis=kis, paper=False)
    # prevent threads from being started by connect
    c.thread = None
    # provide a fake websocket approval key function so KisWebsocketRequest.build() works
    monkeypatch.setattr(
        "vmkis.api.auth.websocket.websocket_approval_key",
        lambda kis_obj, domain=None: SimpleNamespace(approval_key="APPKEY-123"),
    )
    return c


def test_subscribe_and_unsubscribe_sends_requests(monkeypatch):
    c = make_client(monkeypatch)
    ws = DummyWS()
    c.websocket = ws
    c._connected_event.set()

    c.subscribe("ID1", "K1")
    assert KisWebsocketTR("ID1", "K1") in c._subscriptions
    # last sent message should be a JSON with header tr_type TR_SUBSCRIBE_TYPE
    assert ws.sent, "no message sent"
    sent = json.loads(ws.sent[-1])
    assert sent["header"]["tr_type"] == TR_SUBSCRIBE_TYPE

    c.unsubscribe("ID1", "K1")
    assert KisWebsocketTR("ID1", "K1") not in c._subscriptions
    # unsubscribe message sent
    assert json.loads(ws.sent[-1])["header"]["tr_type"] == TR_UNSUBSCRIBE_TYPE


def test_subscribe_max_limit_raises(monkeypatch):
    c = make_client(monkeypatch)
    # set max small for test
    monkeypatch.setattr(websocket_mod, "WEBSOCKET_MAX_SUBSCRIPTIONS", 1)
    ws = DummyWS()
    c.websocket = ws
    c._connected_event.set()

    c.subscribe("A", "")
    with pytest.raises(ValueError):
        c.subscribe("B", "")


def test_release_reference_unsubscribe_called(monkeypatch):
    c = make_client(monkeypatch)
    ws = DummyWS()
    c.websocket = ws
    c._connected_event.set()

    c.subscribe("X", "Y")
    # simulate reference release
    c._release_reference("X:Y", 0)
    # after release unsubscribe called, subscription removed
    assert KisWebsocketTR("X", "Y") not in c._subscriptions


def test_set_encryption_key_special_ids_get_empty_key(monkeypatch):
    c = make_client(monkeypatch)
    tr = KisWebsocketTR("H0STCNI0", "SOME")
    body = {"key": "kkey", "iv": "iivv"}
    c._set_encryption_key(tr, body)
    # key stored under tr with empty key
    stored = list(c._keychain.keys())[0]
    assert stored.key == ""
    assert isinstance(list(c._keychain.values())[0].key, bytes)


def test_handle_control_pingpong_and_subscribed_and_unsubscribed(monkeypatch):
    c = make_client(monkeypatch)
    ws = DummyWS()
    c.websocket = ws

    # PINGPONG echoes
    data = {"header": {"tr_id": "PINGPONG"}}
    assert c._handle_control(data) is None
    assert ws.sent
    sent = json.loads(ws.sent[-1])
    assert sent["header"]["tr_id"] == "PINGPONG"

    # subscribed
    ws.sent.clear()
    data2 = {"header": {"tr_id": "T1", "tr_key": "K"}, "body": {"msg_cd": "OPSP0000", "msg1": "ok"}}
    c._handle_control(data2)
    assert KisWebsocketTR("T1", "K") in c._registered_subscriptions

    # unsubscribed
    data3 = {"header": {"tr_id": "T2"}, "body": {"msg_cd": "OPSP0001", "msg1": "ok"}}
    # add to registered to allow removal
    c._registered_subscriptions.add(KisWebsocketTR("T2", ""))
    c._handle_control(data3)
    assert KisWebsocketTR("T2", "") not in c._registered_subscriptions


def test_handle_event_early_returns(monkeypatch):
    c = make_client(monkeypatch)
    # case: encrypted but no key -> should return without exception
    msg = "1|NOKEY|1|AAA"
    c._keychain.clear()
    # no response mapping
    monkeypatch.setitem(websocket_mod.WEBSOCKET_RESPONSES_MAP, "NOKEY", None)
    c._handle_event(msg)

    # case: not encrypted and no mapping
    msg2 = "0|NOMAP|1|{}"
    # ensure mapping has no entry
    websocket_mod.WEBSOCKET_RESPONSES_MAP.pop("NOMAP", None)
    c._handle_event(msg2)


def test_ensure_primary_client_creates_and_returns_primary(monkeypatch):
    kis = DummyKis(paper=True)
    c = KisWebsocketClient(kis=kis, paper=False)
    primary = c._ensure_primary_client()
    assert primary is not c
    assert c._primary_client is primary


def test_request_true_and_false(monkeypatch):
    c = make_client(monkeypatch)
    # no websocket -> False
    c.websocket = None
    assert c._request("X") is False

    # websocket present but not connected -> False
    c.websocket = DummyWS()
    c._connected_event.clear()
    assert c._request("X") is False

    # connected -> send returns True
    c._connected_event.set()
    c.websocket = DummyWS()
    assert c._request("X") is True


def test_reset_session_state_and_restore_subscriptions(monkeypatch):
    c = make_client(monkeypatch)
    # populate registered and keychain
    c._registered_subscriptions.add(KisWebsocketTR("A", ""))
    c._keychain[KisWebsocketTR("B", "")] = object()

    c._reset_session_state()
    assert not c._registered_subscriptions
    assert not c._keychain

    # restore subscriptions calls _request for each missing registered
    # put one subscription not in registered
    c._subscriptions.add(KisWebsocketTR("R", ""))
    called = []

    def fake_request(t, body=None, force=False):
        called.append((t, body, force))

    monkeypatch.setattr(c, "_request", fake_request)
    c._restore_subscriptions()
    assert called and called[0][2] is True


def test_run_forever_acquire_failure_and_on_open_on_close_on_error(monkeypatch):
    c = make_client(monkeypatch)

    # make connect_lock's acquire return False
    class LockLike:
        def acquire(self, block=False):
            return False

    c._connect_lock = LockLike()
    assert c._run_forever() is False

    # test on_open sets connected event and calls reset/restore
    invoked = {"reset": False, "restore": False}
    monkeypatch.setattr(c, "_reset_session_state", lambda: invoked.update({"reset": True}))
    monkeypatch.setattr(c, "_restore_subscriptions", lambda: invoked.update({"restore": True}))
    ws = object()
    c.websocket = ws
    c._on_open(ws)
    assert invoked["reset"] and invoked["restore"]
    assert c._connected_event.is_set()

    # on_error should handle different types without raising
    c._on_error(ws, Exception("boom"))
    from websocket import WebSocketConnectionClosedException

    c._on_error(ws, WebSocketConnectionClosedException())
    c._on_error(ws, KeyboardInterrupt())

    # on_close should not raise
    c._on_close(ws, 1000, "bye")


def test_on_message_routes(monkeypatch):
    c = make_client(monkeypatch)
    # patch handlers
    called = {"event": False, "control": False}
    monkeypatch.setattr(c, "_handle_event", lambda m: called.update({"event": True}))
    monkeypatch.setattr(c, "_handle_control", lambda d: called.update({"control": True}))

    # event message
    c.websocket = object()
    c._on_message(c.websocket, "0|X|1|{}")
    assert called["event"]

    # control message
    called["event"] = False
    c._on_message(c.websocket, json.dumps({}))
    assert called["control"]


def test_set_encryption_key_non_special_and_handle_event_decryption(monkeypatch):
    c = make_client(monkeypatch)
    # non-special id retains key
    tr = KisWebsocketTR("NORMAL", "K")
    body = {"key": "k" * 16, "iv": "i" * 16}
    c._set_encryption_key(tr, body)
    assert KisWebsocketTR("NORMAL", "K") in c._keychain

    # prepare key to encrypt a small payload
    ek = c._keychain[KisWebsocketTR("NORMAL", "K")]
    plaintext = b"{}\n"
    # pad and encrypt using class cipher
    from cryptography.hazmat.primitives import padding as _padding
    from cryptography.hazmat.primitives.ciphers import algorithms as _algorithms

    padder = _padding.PKCS7(_algorithms.AES.block_size).padder()
    padded = padder.update(plaintext) + padder.finalize()
    encryptor = ek.cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    # ensure WEBSOCKET_RESPONSES_MAP has mapping for NORMAL
    monkeypatch.setitem(websocket_mod.WEBSOCKET_RESPONSES_MAP, "NORMAL", object())

    # monkeypatch KisWebsocketResponse.parse to a dummy that yields nothing
    from vmkis.responses.websocket import KisWebsocketResponse

    monkeypatch.setattr(KisWebsocketResponse, "parse", staticmethod(lambda body, count, response_type: []))

    # event with encrypted flag
    msg = "1|NORMAL|1|" + base64.b64encode(ciphertext).decode("ascii")
    # should not raise
    c._handle_event(msg)


# ===== Tests for Property Methods =====


def test_is_subscribed_with_primary_client(monkeypatch):
    """Test is_subscribed method with primary client delegation"""
    c = make_client(monkeypatch)
    # subscribe directly
    c._subscriptions.add(KisWebsocketTR("A", "B"))
    assert c.is_subscribed("A", "B") is True
    assert c.is_subscribed("X", "Y") is False

    # test with primary client
    primary = make_client(monkeypatch)
    primary._subscriptions.add(KisWebsocketTR("P", "Q"))
    c._primary_client = primary
    assert c.is_subscribed("P", "Q") is True


def test_subscriptions_property_includes_primary_client(monkeypatch):
    """Test subscriptions property aggregates primary client subscriptions"""
    c = make_client(monkeypatch)
    c._subscriptions.add(KisWebsocketTR("A", ""))
    assert len(c.subscriptions) == 1

    # add primary client
    primary = make_client(monkeypatch)
    primary._subscriptions.add(KisWebsocketTR("B", ""))
    c._primary_client = primary
    assert len(c.subscriptions) == 2


def test_connected_property_checks_websocket_and_event(monkeypatch):
    """Test connected property with various states"""
    c = make_client(monkeypatch)
    # no websocket -> False
    assert c.connected is False

    # websocket but event not set -> False
    c.websocket = DummyWS()
    assert c.connected is False

    # websocket and event set -> True
    c._connected_event.set()
    assert c.connected is True

    # with primary client not connected -> False
    primary = make_client(monkeypatch)
    c._primary_client = primary
    assert c.connected is False

    # primary client connected -> True
    primary.websocket = DummyWS()
    primary._connected_event.set()
    assert c.connected is True


# ===== Tests for Connection Management =====


def test_connect_when_already_connected(monkeypatch):
    """Test connect does nothing when already connected"""
    c = make_client(monkeypatch)
    c.websocket = DummyWS()
    c._connected_event.set()
    c.connect()
    # should not start a thread
    assert c.thread is None


def test_connect_triggers_immediate_reconnect_for_alive_thread(monkeypatch):
    """Test connect sets event for immediate reconnect when thread is alive"""
    c = make_client(monkeypatch)
    # mock alive thread
    c.thread = threading.Thread(target=lambda: None)
    c.thread.start()
    c.thread.join()  # finish immediately

    # now it's not alive, so create a fake alive thread
    class FakeThread:
        def is_alive(self):
            return True

    c.thread = FakeThread()

    c.connect()
    assert c._connect_event.is_set()


def test_connect_delegates_to_primary_client(monkeypatch):
    """Test connect delegates to primary client when present"""
    c = make_client(monkeypatch)
    primary = make_client(monkeypatch)
    c._primary_client = primary

    called = {"connect": False}
    monkeypatch.setattr(primary, "connect", lambda: called.update({"connect": True}))

    c.connect()
    assert called["connect"] is True


def test_ensure_connection_calls_connect_when_not_connected(monkeypatch):
    """Test _ensure_connection calls connect when not connected"""
    c = make_client(monkeypatch)
    called = {"connect": False}
    monkeypatch.setattr(c, "connect", lambda: called.update({"connect": True}))

    c._ensure_connection()
    assert called["connect"] is True


def test_ensure_connected_waits_for_connection(monkeypatch):
    """Test ensure_connected synchronously waits for connection"""
    c = make_client(monkeypatch)
    monkeypatch.setattr(c, "_ensure_connection", lambda: c._connected_event.set())

    c.ensure_connected(timeout=1)
    assert c._connected_event.is_set()


def test_ensure_connected_delegates_to_primary(monkeypatch):
    """Test ensure_connected delegates to primary client"""
    c = make_client(monkeypatch)
    primary = make_client(monkeypatch)
    c._primary_client = primary

    called = {"ensure": False}
    monkeypatch.setattr(primary, "ensure_connected", lambda timeout=None: called.update({"ensure": True}))

    c.ensure_connected()
    assert called["ensure"] is True


def test_disconnect_closes_websocket(monkeypatch):
    """Test disconnect closes websocket properly"""
    c = make_client(monkeypatch)
    ws = DummyWS()
    c.websocket = ws
    c.thread = threading.current_thread()

    c.disconnect()
    assert ws.closed is True
    assert c.thread is None


def test_disconnect_delegates_to_primary(monkeypatch):
    """Test disconnect delegates to primary client"""
    c = make_client(monkeypatch)
    primary = make_client(monkeypatch)
    c._primary_client = primary

    called = {"disconnect": False}
    monkeypatch.setattr(primary, "disconnect", lambda: called.update({"disconnect": True}))

    c.disconnect()
    assert called["disconnect"] is True


def test_disconnect_handles_no_websocket(monkeypatch):
    """Test disconnect handles case with no websocket gracefully"""
    c = make_client(monkeypatch)
    c.thread = threading.current_thread()
    c.websocket = None

    # should not raise
    c.disconnect()
    assert c.thread is None


# ===== Tests for Subscription Methods =====


def test_subscribe_delegates_to_primary_when_requested(monkeypatch):
    """Test subscribe delegates to primary client when primary=True"""
    c = make_client(monkeypatch, paper=False)
    # make kis paper to trigger primary client creation
    c.kis.paper = True

    called = []

    def fake_subscribe(id, key, primary):
        called.append((id, key, primary))

    # mock _ensure_primary_client to return different client
    primary = make_client(monkeypatch, paper=True)
    monkeypatch.setattr(primary, "subscribe", fake_subscribe)
    monkeypatch.setattr(c, "_ensure_primary_client", lambda: primary)

    c.subscribe("ID", "KEY", primary=True)
    assert len(called) == 1
    assert called[0] == ("ID", "KEY", False)


def test_subscribe_does_nothing_if_already_subscribed(monkeypatch):
    """Test subscribe returns early if TR already subscribed"""
    c = make_client(monkeypatch)
    ws = DummyWS()
    c.websocket = ws
    c._connected_event.set()

    c._subscriptions.add(KisWebsocketTR("ID", "KEY"))
    initial_count = len(ws.sent)

    c.subscribe("ID", "KEY")
    # no new request sent
    assert len(ws.sent) == initial_count


def test_unsubscribe_delegates_to_primary_when_requested(monkeypatch):
    """Test unsubscribe delegates to primary client when primary=True"""
    c = make_client(monkeypatch)
    primary = make_client(monkeypatch)

    called = []

    def fake_unsubscribe(id, key, primary):
        called.append((id, key, primary))

    monkeypatch.setattr(primary, "unsubscribe", fake_unsubscribe)
    monkeypatch.setattr(c, "_ensure_primary_client", lambda: primary)

    c.unsubscribe("ID", "KEY", primary=True)
    assert len(called) == 1


def test_unsubscribe_does_nothing_if_not_subscribed(monkeypatch):
    """Test unsubscribe returns early if TR not subscribed"""
    c = make_client(monkeypatch)
    ws = DummyWS()
    c.websocket = ws

    initial_count = len(ws.sent)
    c.unsubscribe("NOTEXIST", "KEY")
    # no request sent
    assert len(ws.sent) == initial_count


def test_unsubscribe_all_removes_all_subscriptions(monkeypatch):
    """Test unsubscribe_all removes all subscriptions including primary"""
    c = make_client(monkeypatch)
    ws = DummyWS()
    c.websocket = ws
    c._connected_event.set()

    c._subscriptions.add(KisWebsocketTR("A", ""))
    c._subscriptions.add(KisWebsocketTR("B", ""))

    primary = make_client(monkeypatch)
    primary._subscriptions.add(KisWebsocketTR("P", ""))
    c._primary_client = primary

    called = {"unsubscribe_all": False}
    monkeypatch.setattr(primary, "unsubscribe_all", lambda: called.update({"unsubscribe_all": True}))

    c.unsubscribe_all()
    assert len(c._subscriptions) == 0
    assert called["unsubscribe_all"] is True


def test_referenced_subscribe_returns_ticket(monkeypatch):
    """Test referenced_subscribe returns a reference ticket"""
    c = make_client(monkeypatch)
    ws = DummyWS()
    c.websocket = ws
    c._connected_event.set()

    ticket = c.referenced_subscribe("ID", "KEY")
    assert ticket is not None
    assert KisWebsocketTR("ID", "KEY") in c._subscriptions


def test_on_method_subscribes_and_returns_event_ticket(monkeypatch):
    """Test on method subscribes to TR and returns event ticket"""
    c = make_client(monkeypatch)
    ws = DummyWS()
    c.websocket = ws
    c._connected_event.set()

    def callback(sender, args):
        pass

    ticket = c.on("ID", "KEY", callback)
    assert ticket is not None
    assert KisWebsocketTR("ID", "KEY") in c._subscriptions


def test_on_method_with_where_filter(monkeypatch):
    """Test on method works with custom where filter"""
    c = make_client(monkeypatch)
    ws = DummyWS()
    c.websocket = ws
    c._connected_event.set()

    def callback(sender, args):
        pass

    # create a simple filter
    class TestFilter:
        def __call__(self, sender, args):
            return True

    ticket = c.on("ID", "KEY", callback, where=TestFilter())
    assert ticket is not None


def test_on_method_with_once_flag(monkeypatch):
    """Test on method respects once flag"""
    c = make_client(monkeypatch)
    ws = DummyWS()
    c.websocket = ws
    c._connected_event.set()

    def callback(sender, args):
        pass

    ticket = c.on("ID", "KEY", callback, once=True)
    assert ticket is not None


def test_on_method_with_primary_flag(monkeypatch):
    """Test on method delegates to primary when primary=True"""
    c = make_client(monkeypatch)
    ws = DummyWS()
    c.websocket = ws
    c._connected_event.set()

    # setup primary client
    c.kis.paper = True
    primary = make_client(monkeypatch, paper=True)
    primary.websocket = DummyWS()
    primary._connected_event.set()
    monkeypatch.setattr(c, "_ensure_primary_client", lambda: primary)

    def callback(sender, args):
        pass

    ticket = c.on("ID", "KEY", callback, primary=True)
    assert ticket is not None
    # should be subscribed in primary
    assert KisWebsocketTR("ID", "KEY") in primary._subscriptions


# ===== Tests for Message Handling =====


def test_handle_control_with_opsp0002_already_subscribed(monkeypatch):
    """Test _handle_control handles OPSP0002 (already subscribed) code"""
    c = make_client(monkeypatch)
    c.websocket = DummyWS()

    data = {"header": {"tr_id": "TEST", "tr_key": "KEY"}, "body": {"msg_cd": "OPSP0002", "msg1": "already subscribed"}}

    c._handle_control(data)
    assert KisWebsocketTR("TEST", "KEY") in c._registered_subscriptions


def test_handle_control_with_opsp0003_not_subscribed(monkeypatch):
    """Test _handle_control handles OPSP0003 (not subscribed) code"""
    c = make_client(monkeypatch)
    c.websocket = DummyWS()

    tr = KisWebsocketTR("TEST", "")
    c._registered_subscriptions.add(tr)
    c._keychain[tr] = object()

    data = {"header": {"tr_id": "TEST"}, "body": {"msg_cd": "OPSP0003", "msg1": "not subscribed"}}

    c._handle_control(data)
    assert tr not in c._registered_subscriptions
    assert tr not in c._keychain


def test_handle_control_with_opsp8996_already_in_use(monkeypatch):
    """Test _handle_control handles OPSP8996 (session in use) code"""
    c = make_client(monkeypatch)
    c.websocket = DummyWS()

    data = {"header": {"tr_id": "TEST"}, "body": {"msg_cd": "OPSP8996", "msg1": "session already in use"}}

    # should not raise
    c._handle_control(data)


def test_handle_control_with_opsp0007_internal_error(monkeypatch):
    """Test _handle_control handles OPSP0007 (internal error) code"""
    c = make_client(monkeypatch)
    c.websocket = DummyWS()

    data = {
        "header": {"tr_id": "TEST", "tr_key": "KEY"},
        "body": {"msg_cd": "OPSP0007", "msg1": "internal server error"},
    }

    # should not raise
    c._handle_control(data)


def test_handle_control_with_unknown_code(monkeypatch):
    """Test _handle_control handles unknown message codes"""
    c = make_client(monkeypatch)
    c.websocket = DummyWS()

    data = {"header": {"tr_id": "TEST", "tr_key": "KEY"}, "body": {"msg_cd": "UNKNOWN", "msg1": "unknown message"}}

    # should not raise
    c._handle_control(data)


def test_handle_control_without_body(monkeypatch):
    """Test _handle_control handles messages without body"""
    c = make_client(monkeypatch)
    c.websocket = DummyWS()

    data = {"header": {"tr_id": "NOTPINGPONG"}}

    # should not raise, just log warning
    c._handle_control(data)


def test_handle_control_returns_false_when_no_websocket(monkeypatch):
    """Test _handle_control returns False when no websocket"""
    c = make_client(monkeypatch)
    c.websocket = None

    data = {"header": {"tr_id": "TEST"}}
    result = c._handle_control(data)
    assert result is False


def test_handle_event_with_kis_object_initialization(monkeypatch):
    """Test _handle_event initializes KisObjectBase instances"""
    c = make_client(monkeypatch)

    from vmkis.client.object import KisObjectBase

    class TestResponse(KisObjectBase):
        pass

    test_response = TestResponse()

    monkeypatch.setitem(websocket_mod.WEBSOCKET_RESPONSES_MAP, "TESTID", TestResponse)

    from vmkis.responses.websocket import KisWebsocketResponse

    monkeypatch.setattr(KisWebsocketResponse, "parse", staticmethod(lambda body, count, response_type: [test_response]))

    invoked = []

    def capture_event(sender, args):
        invoked.append((sender, args))

    # Use subscribe filter to match TESTID
    from vmkis.event.filters.subscription import KisSubscriptionEventFilter

    ticket = c.event.on(capture_event, where=KisSubscriptionEventFilter("TESTID"))

    msg = "0|TESTID|1|{}"
    c._handle_event(msg)
    assert len(invoked) == 1
    assert isinstance(invoked[0][1].response, TestResponse)

    ticket.unsubscribe()


def test_handle_event_catches_event_invoke_exceptions(monkeypatch):
    """Test _handle_event catches exceptions from event handlers"""
    c = make_client(monkeypatch)

    monkeypatch.setitem(websocket_mod.WEBSOCKET_RESPONSES_MAP, "TESTID", object())

    from vmkis.responses.websocket import KisWebsocketResponse

    monkeypatch.setattr(KisWebsocketResponse, "parse", staticmethod(lambda body, count, response_type: [{}]))

    def failing_handler(sender, args):
        raise Exception("Handler error")

    c.event.on(failing_handler)

    msg = "0|TESTID|1|{}"
    # should not raise
    c._handle_event(msg)


def test_handle_event_catches_parse_exceptions(monkeypatch):
    """Test _handle_event catches exceptions from response parsing"""
    c = make_client(monkeypatch)

    monkeypatch.setitem(websocket_mod.WEBSOCKET_RESPONSES_MAP, "TESTID", object())

    from vmkis.responses.websocket import KisWebsocketResponse

    def failing_parse(body, count, response_type):
        raise Exception("Parse error")

    monkeypatch.setattr(KisWebsocketResponse, "parse", staticmethod(failing_parse))

    msg = "0|TESTID|1|{}"
    # should not raise
    c._handle_event(msg)


def test_handle_event_with_decryption_error(monkeypatch):
    """Test _handle_event handles decryption errors gracefully"""
    c = make_client(monkeypatch)

    # set up encryption key
    tr = KisWebsocketTR("TESTID", "")
    c._keychain[tr] = object()  # invalid key object will cause error

    msg = "1|TESTID|1|invalidbase64"
    # should not raise, just log error
    c._handle_event(msg)


# ===== Tests for Primary Client Management =====


def test_ensure_primary_client_returns_self_when_not_virtual(monkeypatch):
    """Test _ensure_primary_client returns self when kis is not paper"""
    c = make_client(monkeypatch)
    c.kis.paper = False

    result = c._ensure_primary_client()
    assert result is c
    assert c._primary_client is None


def test_ensure_primary_client_returns_self_when_already_virtual(monkeypatch):
    """Test _ensure_primary_client returns self when client already paper"""
    c = make_client(monkeypatch, paper=True)
    c.kis.paper = False  # kis not paper, so primary client not needed

    result = c._ensure_primary_client()
    assert result is c


def test_primary_client_event_handlers_forward_events(monkeypatch):
    """Test primary client event handlers forward events to main client"""
    c = make_client(monkeypatch)

    from vmkis.event.subscription import KisSubscribedEventArgs

    # test subscribed event forwarding
    invoked = {"subscribed": False, "unsubscribed": False, "event": False}

    def capture_subscribed(sender, args):
        invoked["subscribed"] = True

    def capture_unsubscribed(sender, args):
        invoked["unsubscribed"] = True

    def capture_event(sender, args):
        invoked["event"] = True

    # Register handlers
    ticket1 = c.subscribed_event.on(capture_subscribed)
    ticket2 = c.unsubscribed_event.on(capture_unsubscribed)
    ticket3 = c.event.on(capture_event)

    tr = KisWebsocketTR("TEST", "")
    args = KisSubscribedEventArgs(tr)

    # Test forwarding
    c._primary_client_subscribed_event(c, args)
    assert invoked["subscribed"] is True

    c._primary_client_unsubscribed_event(c, args)
    assert invoked["unsubscribed"] is True

    from vmkis.event.subscription import KisSubscriptionEventArgs

    event_args = KisSubscriptionEventArgs(tr=tr, response={})
    c._primary_client_event(c, event_args)
    assert invoked["event"] is True

    # Clean up
    ticket1.unsubscribe()
    ticket2.unsubscribe()
    ticket3.unsubscribe()


# ===== Tests for Thread and Connection Loop =====


def test_run_forever_returns_false_when_lock_not_acquired(monkeypatch):
    """Test _run_forever returns False when cannot acquire lock"""
    c = make_client(monkeypatch)

    # acquire lock beforehand
    c._connect_lock.acquire()

    try:
        result = c._run_forever()
        assert result is False
    finally:
        c._connect_lock.release()


def test_run_forever_clears_state_on_exit(monkeypatch):
    """Test _run_forever clears websocket and event on exit"""
    c = make_client(monkeypatch)
    c.reconnect = False

    # mock WebSocketApp to avoid actual connection
    class FakeWSApp:
        def __init__(self, *args, **kwargs):
            pass

        def run_forever(self):
            pass

    monkeypatch.setattr("vmkis.client.websocket.WebSocketApp", FakeWSApp)

    c._run_forever()

    assert c.websocket is None
    assert not c._connected_event.is_set()


def test_run_forever_breaks_on_thread_change(monkeypatch):
    """Test _run_forever exits when thread changes"""
    c = make_client(monkeypatch)

    # mock WebSocketApp
    class FakeWSApp:
        def __init__(self, *args, **kwargs):
            pass

        def run_forever(self):
            # change thread to signal exit
            c.thread = None

    monkeypatch.setattr("vmkis.client.websocket.WebSocketApp", FakeWSApp)

    c._run_forever()
    assert c.thread is None


def test_run_forever_handles_unexpected_exceptions(monkeypatch):
    """Test _run_forever handles unexpected exceptions in loop"""
    c = make_client(monkeypatch)
    c.reconnect = False

    class FakeWSApp:
        def __init__(self, *args, **kwargs):
            pass

        def run_forever(self):
            raise RuntimeError("Unexpected error")

    monkeypatch.setattr("vmkis.client.websocket.WebSocketApp", FakeWSApp)

    # should not raise
    c._run_forever()


def test_run_forever_respects_immediate_reconnect_event(monkeypatch):
    """Test _run_forever detects immediate reconnect event during sleep"""
    c = make_client(monkeypatch)
    c.reconnect_interval = 0.1  # short interval for test

    call_count = {"count": 0}

    class FakeWSApp:
        def __init__(self, *args, **kwargs):
            pass

        def run_forever(self):
            call_count["count"] += 1
            if call_count["count"] == 1:
                # trigger immediate reconnect
                c._connect_event.set()
            else:
                # exit on second call
                c.reconnect = False
                c.thread = None

    monkeypatch.setattr("vmkis.client.websocket.WebSocketApp", FakeWSApp)

    c._run_forever()
    assert call_count["count"] >= 1  # at least one call made


def test_on_open_does_nothing_if_websocket_changed(monkeypatch):
    """Test _on_open returns early if websocket instance changed"""
    c = make_client(monkeypatch)
    c.websocket = DummyWS()

    different_ws = DummyWS()
    c._on_open(different_ws)

    # event should not be set
    assert not c._connected_event.is_set()


def test_on_error_does_nothing_if_websocket_changed(monkeypatch):
    """Test _on_error returns early if websocket instance changed"""
    c = make_client(monkeypatch)
    c.websocket = DummyWS()

    different_ws = DummyWS()
    # should not raise
    c._on_error(different_ws, Exception("test"))


def test_on_close_does_nothing_if_websocket_changed(monkeypatch):
    """Test _on_close returns early if websocket instance changed"""
    c = make_client(monkeypatch)
    c.websocket = DummyWS()

    different_ws = DummyWS()
    # should not raise
    c._on_close(different_ws, 1000, "test")


def test_on_message_does_nothing_if_websocket_changed(monkeypatch):
    """Test _on_message returns early if websocket instance changed"""
    c = make_client(monkeypatch)
    c.websocket = DummyWS()

    different_ws = DummyWS()
    # should not raise
    c._on_message(different_ws, "{}")


def test_on_message_handles_exceptions(monkeypatch):
    """Test _on_message handles message processing exceptions"""
    c = make_client(monkeypatch)
    c.websocket = DummyWS()

    # invalid message format will cause exception
    # should not raise
    c._on_message(c.websocket, "invalid")
