import json
import types
from datetime import datetime, timedelta

import pytest

from vmkis.api.auth import token as tk
from vmkis.api.auth.token import KisAccessToken, token_issue, token_revoke
from vmkis.utils.timezone import TIMEZONE


def make_token_instance(offset_seconds: int = 0) -> KisAccessToken:
    inst = KisAccessToken()
    inst.type = "Bearer"
    inst.token = "abc123"
    inst.validity_period = 3600
    inst.expired_at = datetime.now(TIMEZONE) + timedelta(seconds=offset_seconds)
    return inst


def test_kisaccess_token_properties_and_build_and_str_repr(tmp_path):
    t = make_token_instance(offset_seconds=5)

    # not expired when in future
    assert t.expired is False

    rem = t.remaining
    assert isinstance(rem, timedelta)
    assert rem.total_seconds() > 0

    hdr = t.build({})
    assert hdr["Authorization"] == f"{t.type} {t.token}"

    assert str(t) == f"{t.type} {t.token}"
    r = repr(t)
    assert "KisAccessToken" in r

    # save should write JSON using raw(); monkeypatch raw to known dict
    data = {
        "access_token": "abc123",
        "token_type": "Bearer",
        "access_token_token_expired": "2000-01-01 00:00:00",
        "expires_in": 3600,
    }

    def fake_raw(self):
        return data

    # attach temporarily
    KisAccessToken.raw = fake_raw  # simple assignment for test

    p = tmp_path / "tok.json"
    t.save(str(p))

    with open(p) as f:
        got = json.load(f)

    assert got == data


def test_kisaccess_token_load_calls_transform(monkeypatch, tmp_path):
    sample = {"a": 1}
    p = tmp_path / "in.json"
    p.write_text(json.dumps(sample))

    called = {}

    def fake_transform(obj, cls):
        called["obj"] = obj
        called["cls"] = cls
        return "LOADED"

    monkeypatch.setattr(tk.KisObject, "transform_", fake_transform)

    res = KisAccessToken.load(str(p))
    assert res == "LOADED"
    assert called["obj"] == sample
    assert called["cls"] is KisAccessToken


def test_token_issue_calls_fetch_and_returns_instance(monkeypatch):
    t = make_token_instance()

    class FakeKis:
        def __init__(self):
            self.last = None

        def fetch(self, *args, **kwargs):
            self.last = kwargs
            return t

    kis = FakeKis()

    res = token_issue(kis, domain="live")
    assert res is t
    assert kis.last is not None
    assert kis.last.get("domain") == "live"


def test_token_revoke_success_and_failure():
    class Good:
        def request(self, *a, **k):
            return types.SimpleNamespace(ok=True)

    class Bad:
        def request(self, *a, **k):
            return types.SimpleNamespace(ok=False, status_code=400, text="err")

    # success does not raise
    token_revoke(Good(), "tok")

    with pytest.raises(ValueError) as ei:
        token_revoke(Bad(), "tok")

    assert "토큰 폐기에 실패했습니다" in str(ei.value)
