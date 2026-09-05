import pytest

from vmkis.__env__ import APPKEY_LENGTH, SECRETKEY_LENGTH
from vmkis.client.appkey import KisKey


def make_key(length: int) -> str:
    return "A" * length


def test_valid_kiskey_sets_attributes_and_builds_dict():
    appkey = make_key(APPKEY_LENGTH)
    secret = make_key(SECRETKEY_LENGTH)
    k = KisKey("myid", appkey, secret)

    assert k.id == "myid"
    assert k.appkey == appkey
    assert k.secretkey == secret

    # build without existing dict returns expected mapping
    result = k.build()
    assert result["appkey"] == appkey
    assert result["appsecret"] == secret


def test_build_merges_into_given_dict_and_returns_same_object():
    appkey = make_key(APPKEY_LENGTH)
    secret = make_key(SECRETKEY_LENGTH)
    k = KisKey("x", appkey, secret)

    d = {"existing": 1}
    ret = k.build(d)
    # same dict object returned
    assert ret is d
    assert d["existing"] == 1
    assert d["appkey"] == appkey
    assert d["appsecret"] == secret


def test_repr_masks_secret_and_shows_id_and_appkey():
    appkey = make_key(APPKEY_LENGTH)
    secret = make_key(SECRETKEY_LENGTH)
    k = KisKey("user", appkey, secret)

    r = repr(k)
    assert "KisKey(" in r
    assert "user" in r
    assert appkey in r
    # secret should not be visible
    assert secret not in r
    assert "***" in r


def test_missing_id_raises_value_error():
    appkey = make_key(APPKEY_LENGTH)
    secret = make_key(SECRETKEY_LENGTH)
    with pytest.raises(ValueError):
        KisKey("", appkey, secret)


def test_invalid_appkey_length_raises():
    secret = make_key(SECRETKEY_LENGTH)
    with pytest.raises(ValueError):
        KisKey("id", make_key(APPKEY_LENGTH - 1), secret)

    with pytest.raises(ValueError):
        KisKey("id", make_key(APPKEY_LENGTH + 1), secret)


def test_invalid_secretkey_length_raises():
    appkey = make_key(APPKEY_LENGTH)
    with pytest.raises(ValueError):
        KisKey("id", appkey, make_key(SECRETKEY_LENGTH - 1))

    with pytest.raises(ValueError):
        KisKey("id", appkey, make_key(SECRETKEY_LENGTH + 1))
