from vmkis.api.base import account as ab


def test_account_property_calls_kis_account():
    class FakeKis:
        def __init__(self):
            self.called = None

        def account(self, account):
            self.called = account
            return "ACCOUNT-OBJ"

    a = ab.KisAccountBase()
    a.kis = FakeKis()
    a.account_number = "ACC123"

    res = a.account
    assert res == "ACCOUNT-OBJ"
    assert a.kis.called == "ACC123"
