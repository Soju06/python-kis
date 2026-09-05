import pytest

from vmkis.client.account import KisAccountNumber


def test_valid_8_digit_account():
    acc = KisAccountNumber("12345678")
    assert acc.number == "12345678"
    assert acc.code == "01"
    assert acc.build() == {"CANO": "12345678", "ACNT_PRDT_CD": "01"}


def test_valid_10_digit_account():
    acc = KisAccountNumber("8765432109")
    assert acc.number == "87654321"
    assert acc.code == "09"
    assert acc.build({}) == {"CANO": "87654321", "ACNT_PRDT_CD": "09"}


def test_valid_11_with_hyphen():
    acc = KisAccountNumber("00000000-12")
    assert acc.number == "00000000"
    assert acc.code == "12"
    assert acc.build({"existing": 1})["existing"] == 1


def test_invalid_format_short_or_long():
    with pytest.raises(ValueError):
        KisAccountNumber("")

    with pytest.raises(ValueError):
        KisAccountNumber("123456789012")


def test_invalid_11_without_hyphen_is_rejected():
    # length 11 but no hyphen at index 8 -> invalid
    with pytest.raises(ValueError):
        KisAccountNumber("12345678901")


def test_non_digit_characters_raise():
    with pytest.raises(ValueError):
        KisAccountNumber("12AB5678")

    with pytest.raises(ValueError):
        KisAccountNumber("12345678-0A")


def test_equality_and_hash_and_repr_and_str():
    a = KisAccountNumber("11111111")
    b = KisAccountNumber("11111111")
    c = KisAccountNumber("11111111-02")

    assert a == b
    assert not (a != b)
    assert hash(a) == hash(b)
    assert a != c

    assert str(a) == "11111111-01"
    assert "KisAccountNumber('11111111-01')" in repr(a)
