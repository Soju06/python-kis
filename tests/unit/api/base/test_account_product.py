import types

from vmkis.api.base import account_product as apb


def test_account_product_inherits_and_properties_work():
    p = apb.KisAccountProductBase()
    p.kis = types.SimpleNamespace()
    p.account_number = "ACC"
    p.market = "KRX"
    p.symbol = "SYM"

    # account property comes from KisAccountBase
    class FakeKis:
        def account(self, account):
            return f"ACC-{account}"

    p.kis = FakeKis()
    assert p.account == "ACC-ACC"

    # name property comes from the info() call; monkeypatch the info function
    def fake_info(kis, symbol, market):
        return types.SimpleNamespace(name="N")

    import vmkis.api.stock.info as info_mod

    info_mod_info = info_mod.info
    try:
        info_mod.info = fake_info
        assert p.name == "N"
    finally:
        # restore
        info_mod.info = info_mod_info
