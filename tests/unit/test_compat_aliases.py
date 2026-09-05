"""1.0.0 에서 이름 호환 폴백이 사라졌는지 봅니다. (#33)

예전에는 DeprecationWarning 과 함께 살아 있었습니다. 지금은 AttributeError /
무시입니다.
"""

from __future__ import annotations

import pytest

import vmkis
from vmkis import helpers


class TestPyKisAliasRemoved:
    def test_pykis_is_gone(self):
        with pytest.raises(AttributeError):
            _ = vmkis.PyKis

    def test_vmkis_still_exported(self):
        assert "VmKis" in vmkis.__all__
        assert "PyKis" not in vmkis.__all__


class TestEnvironmentVariableFallbackRemoved:
    @pytest.fixture(autouse=True)
    def clean_env(self, monkeypatch):
        for name in ("VMKIS_ACCOUNT", "PYKIS_ACCOUNT", "VMKIS_PROFILE", "PYKIS_PROFILE"):
            monkeypatch.delenv(name, raising=False)

    def test_returns_none_when_only_legacy_is_set(self, monkeypatch):
        monkeypatch.setenv("PYKIS_PROFILE", "legacy")

        assert helpers._env("PROFILE") is None

    def test_reads_new_prefix(self, monkeypatch):
        monkeypatch.setenv("VMKIS_PROFILE", "new")

        assert helpers._env("PROFILE") == "new"

    def test_create_client_ignores_legacy_account_variable(self, tmp_path, monkeypatch):
        import yaml

        config = {
            "version": 1,
            "apps": {
                "app_paper1": {
                    "mode": "paper",
                    "hts_id": "x",
                    "app_key": "k",
                    "app_secret": "s",
                },
                "app_live1": {
                    "mode": "live",
                    "hts_id": "x",
                    "app_key": "K",
                    "app_secret": "S",
                },
            },
            "accounts": {
                "acc_a": {"app": "app_paper1", "account_no": "00000000", "product_code": "01"},
                "acc_b": {"app": "app_paper1", "account_no": "11111111", "product_code": "02"},
                "acc_live": {"app": "app_live1", "account_no": "22222222", "product_code": "01"},
            },
            "default_account": "acc_a",
        }
        path = tmp_path / "account_profiles.yaml"
        path.write_text(yaml.dump(config), encoding="utf-8")

        captured: dict = {}
        monkeypatch.setattr(helpers, "VmKis", lambda *a, **kw: captured.update(auth=a[1]) or object())
        monkeypatch.setenv("PYKIS_ACCOUNT", "acc_b")

        helpers.create_client(path, keep_token=False)

        assert captured["auth"].account == "00000000-01", "PYKIS_* 는 더 이상 읽히지 않습니다"


class TestUserAgentAndPackageName:
    def test_package_name_is_the_distribution_name(self):
        from vmkis.__env__ import __package_name__

        assert __package_name__ == "vm-stock-kis"

    def test_user_agent_uses_class_name(self):
        from vmkis.__env__ import USER_AGENT, __version__

        assert USER_AGENT == f"VmKis/{__version__}"

    def test_version_is_not_the_unknown_fallback(self):
        from vmkis.__env__ import __version__

        assert not __version__.startswith("0.0.0")
