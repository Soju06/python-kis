import json

import pytest

from vmkis.__env__ import APPKEY_LENGTH, SECRETKEY_LENGTH
from vmkis.client.account import KisAccountNumber
from vmkis.client.appkey import KisKey
from vmkis.client.auth import KisAuth


def make_key(length: int) -> str:
    return "K" * length


def make_auth(account: str = "00000000-01", paper: bool = False) -> KisAuth:
    return KisAuth(
        id="me",
        appkey=make_key(APPKEY_LENGTH),
        secretkey=make_key(SECRETKEY_LENGTH),
        account=account,
        paper=paper,
    )


def test_key_and_account_number_properties_return_expected_types():
    auth = make_auth()
    key = auth.key
    acct = auth.account_number

    assert isinstance(key, KisKey)
    assert key.id == "me"
    assert key.appkey == auth.appkey

    assert isinstance(acct, KisAccountNumber)
    assert str(acct) == auth.account


def test_save_writes_json_and_load_returns_equal_object(tmp_path):
    auth = make_auth(paper=True)
    p = tmp_path / "auth.json"

    auth.save(p)

    # file should contain expected keys
    with open(p) as f:
        d = json.load(f)

    assert d["id"] == auth.id
    assert d["appkey"] == auth.appkey
    assert d["secretkey"] == auth.secretkey
    assert d["account"] == auth.account
    assert d["paper"] == auth.paper

    loaded = KisAuth.load(p)
    assert loaded == auth


def test_load_invalid_json_raises_value_error(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("not json")

    with pytest.raises(ValueError):
        KisAuth.load(p)


def test_load_missing_file_raises_value_error(tmp_path):
    p = tmp_path / "missing.json"
    with pytest.raises(ValueError):
        KisAuth.load(p)


def test_load_with_incorrect_structure_raises_value_error(tmp_path):
    p = tmp_path / "wrong.json"
    # write JSON that does not map to KisAuth fields
    p.write_text(json.dumps({"foo": "bar"}))

    with pytest.raises(ValueError):
        KisAuth.load(p)


def test_repr_includes_account_and_virtual():
    auth = make_auth(account="99999999-99", paper=True)
    r = repr(auth)
    assert "KisAuth" in r
    assert "99999999-99" in r
    assert "paper=True" in r
