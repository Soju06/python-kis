import types

import pytest

from vmkis.api.auth import websocket as ws


def test_websocket_approval_key_real_calls_fetch_and_returns(monkeypatch):
    class FakeKis:
        def __init__(self):
            self.appkey = types.SimpleNamespace(appkey="APP", secretkey="SEC")
            self.paper_appkey = None
            self.last = None

        def fetch(self, *args, **kwargs):
            # record kwargs for assertions and return a response-like object
            self.last = kwargs
            return types.SimpleNamespace(approval_key="KEY")

    kis = FakeKis()

    res = ws.websocket_approval_key(kis, domain="live")
    assert hasattr(res, "approval_key")
    assert res.approval_key == "KEY"

    # verify fetch parameters
    assert kis.last is not None
    assert kis.last.get("response_type") is ws.KisWebsocketApprovalKey
    assert kis.last.get("method") == "POST"
    assert kis.last.get("auth") is False
    # body contains the appkey and secret
    body = kis.last.get("body")
    assert body["appkey"] == "APP"
    assert body["secretkey"] == "SEC"


def test_websocket_approval_key_uses_virtual_appkey_by_default_and_raises_when_missing():
    class FakeKisMissing:
        def __init__(self):
            self.appkey = types.SimpleNamespace(appkey="APP", secretkey="SEC")
            self.paper_appkey = None

    # default domain is None -> uses paper_appkey -> should raise when missing
    with pytest.raises(ValueError) as ei:
        ws.websocket_approval_key(FakeKisMissing(), domain=None)

    assert "모의도메인 appkey가 없습니다" in str(ei.value)


def test_websocket_approval_key_uses_virtual_when_present(monkeypatch):
    class FakeKisV:
        def __init__(self):
            self.appkey = types.SimpleNamespace(appkey="APP", secretkey="SEC")
            self.paper_appkey = types.SimpleNamespace(appkey="VAPP", secretkey="VSEC")
            self.last = None

        def fetch(self, *args, **kwargs):
            self.last = kwargs
            return types.SimpleNamespace(approval_key="VKEY")

    kis = FakeKisV()
    res = ws.websocket_approval_key(kis)  # domain None -> paper_appkey used
    assert res.approval_key == "VKEY"
    body = kis.last.get("body")
    assert body["appkey"] == "VAPP"
    assert body["secretkey"] == "VSEC"
