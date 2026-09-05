import yaml


def test_create_client_and_simple(monkeypatch, tmp_path):
    # prepare temporary config (#75 스키마)
    cfg = {
        "version": 1,
        "apps": {
            "app_paper1": {
                "mode": "paper",
                "hts_id": "testid",
                "app_key": "appkey",
                "app_secret": "secret",
            },
            # 모의 계좌도 시세는 실전 도메인으로 나가므로 실전 앱이 필요합니다. (#87)
            "app_live1": {
                "mode": "live",
                "hts_id": "testid",
                "app_key": "liveappkey",
                "app_secret": "livesecret",
            },
        },
        "accounts": {
            "acc_paper1": {"app": "app_paper1", "account_no": "00000000", "product_code": "01"},
            "acc_live1": {"app": "app_live1", "account_no": "11111111", "product_code": "01"},
        },
        "default_account": "acc_paper1",
    }
    p = tmp_path / "account_profiles.yaml"
    p.write_text(yaml.dump(cfg, sort_keys=False), encoding="utf-8")

    # Dummy VmKis to avoid network calls
    class DummyVmKis:
        def __init__(self, *args, **kwargs):
            self.inited = True

        def stock(self, symbol):
            class S:
                def quote(self_inner):
                    return {"symbol": symbol}

                def buy(self_inner, price=None, qty=None):
                    return {"bought": symbol, "qty": qty, "price": price}

            return S()

        def account(self):
            class A:
                def balance(self_inner):
                    return {"cash": 100}

            return A()

    # import helpers and monkeypatch VmKis used there
    import vmkis.helpers as helpers

    monkeypatch.setattr(helpers, "VmKis", DummyVmKis, raising=False)

    kis = helpers.create_client(str(p))
    assert isinstance(kis, DummyVmKis)

    from vmkis.simple import SimpleKIS

    sk = SimpleKIS.from_client(kis)
    assert sk.get_price("005930")["symbol"] == "005930"
    assert sk.get_balance()["cash"] == 100
    assert sk.place_order("005930", qty=1)["bought"] == "005930"
