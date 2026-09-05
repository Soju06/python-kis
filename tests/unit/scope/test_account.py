import vmkis.scope.account as account_mod


class FakeAcc:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, FakeAcc) and self.value == other.value

    def __repr__(self):
        return f"FakeAcc({self.value!r})"


class FakeScope:
    def __init__(self, kis, account):
        # mimic KisAccountScope expected attributes
        self.kis = kis
        self.account_number = account


class DummyKis:
    def __init__(self, primary=None):
        self.primary = primary
        self.primary_account = None


def test_account_with_string_creates_kisaccountnumber_and_passes_to_scope(monkeypatch):
    # arrange: replace KisAccountNumber and KisAccountScope with fakes
    monkeypatch.setattr(account_mod, "KisAccountNumber", FakeAcc)
    monkeypatch.setattr(account_mod, "KisAccountScope", FakeScope)

    kis = DummyKis()
    result = account_mod.account(kis, "12345")

    assert isinstance(result, FakeScope)
    # account string should have been converted to FakeAcc with same value
    assert isinstance(result.account_number, FakeAcc)
    assert result.account_number == FakeAcc("12345")
    # kis passed through to scope ctor
    assert result.kis is kis


def test_account_with_kisaccountnumber_passes_through(monkeypatch):
    monkeypatch.setattr(account_mod, "KisAccountScope", FakeScope)

    kis = DummyKis()
    existing = FakeAcc("acct-xyz")
    res = account_mod.account(kis, existing)

    assert isinstance(res, FakeScope)
    assert res.account_number is existing  # same object passed through
    assert res.kis is kis


def test_account_with_none_uses_self_primary(monkeypatch):
    monkeypatch.setattr(account_mod, "KisAccountScope", FakeScope)

    primary_acc = FakeAcc("primary-1")
    kis = DummyKis(primary=primary_acc)

    res = account_mod.account(kis, None)
    assert isinstance(res, FakeScope)
    assert res.account_number is primary_acc


def test_account_primary_flag_sets_primary_account_and_returns_scope(monkeypatch):
    monkeypatch.setattr(account_mod, "KisAccountNumber", FakeAcc)
    monkeypatch.setattr(account_mod, "KisAccountScope", FakeScope)

    kis = DummyKis(primary=None)
    res = account_mod.account(kis, "000-11", primary=True)

    # returned object's account_number created from string
    assert res.account_number == FakeAcc("000-11")
    # primary_account on kis should be set to the created KisAccountNumber
    assert kis.primary_account == FakeAcc("000-11")
