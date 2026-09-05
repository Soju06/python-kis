"""설정 스키마 검증 (#75).

`docs/guidelines/CONFIG_SCHEMA.md` 의 R1~R9 와 1:1 로 대응합니다. 규칙을 지웠는데
테스트가 남아 있으면 어느 쪽이 사양인지 알 수 없으므로, 규칙 번호를 이름에 답니다.

이 모듈이 지키는 것은 하나입니다 — **조용히 넘어가지 않는다.** 이전 스키마에서는
`virtaul: true` 오타가 기본값 `False`(실전)로 떨어져 모의투자 의도가 실전 주문이
됐습니다 (#69).
"""

import pytest
import yaml

from vmkis.config import load_kis_config


def write(tmp_path, data, name="account_profiles.yaml"):
    path = tmp_path / name
    path.write_text(yaml.dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def config(**overrides):
    """통과하는 최소 설정. 각 테스트는 여기서 한 가지만 망가뜨립니다."""
    base = {
        "version": 1,
        "apps": {
            "app_paper1": {
                "mode": "paper",
                "hts_id": "testid",
                "app_key": "a" * 36,
                "app_secret": "s" * 180,
            }
        },
        "accounts": {
            "acc_paper1": {
                "app": "app_paper1",
                "account_no": "00000000",
                "product_code": "01",
            }
        },
        "default_account": "acc_paper1",
    }
    return {**base, **overrides}


class TestHappyPath:
    def test_minimal_config_loads(self, tmp_path):
        cfg = load_kis_config(write(tmp_path, config()))
        account = cfg.account()

        assert account.name == "acc_paper1"
        assert account.app == "app_paper1"
        assert account.mode == "paper"
        assert account.is_paper is True
        assert account.account == "00000000-01", "KisAuth 가 받는 형식이어야 한다"

    def test_single_account_needs_no_default(self, tmp_path):
        """계좌가 하나뿐이면 `default_account` 를 요구하지 않습니다 (R7 의 이면)."""
        data = config()
        del data["default_account"]

        assert load_kis_config(write(tmp_path, data)).account().name == "acc_paper1"

    def test_token_path_derives_from_app_name(self, tmp_path):
        """토큰 파일은 앱 이름에서 나옵니다. 사용자가 적지 않으므로 충돌할 수 없습니다."""
        cfg = load_kis_config(write(tmp_path, config()))

        assert cfg.account().token_path == tmp_path / "token" / "app_paper1.json"

    def test_token_dir_is_relative_to_config_file(self, tmp_path):
        """cwd 가 아니라 설정 파일 기준입니다.

        cwd 기준이면 다른 디렉터리에서 실행할 때마다 새 토큰 파일이 생깁니다.
        """
        nested = tmp_path / "configs"
        nested.mkdir()
        path = write(nested, config(token_dir="secrets"))

        assert load_kis_config(path).account().token_path == nested / "secrets" / "app_paper1.json"

    def test_two_accounts_can_share_one_app(self, tmp_path):
        """한 앱키로 계좌 N개 — 이 스키마가 앱과 계좌를 나눈 이유입니다."""
        data = config()
        data["accounts"]["acc_paper2"] = {"app": "app_paper1", "account_no": "11111111", "product_code": "22"}
        cfg = load_kis_config(write(tmp_path, data))

        assert cfg.account("acc_paper1").token_path == cfg.account("acc_paper2").token_path


class TestRules:
    def test_r1_missing_version_names_the_old_format(self, tmp_path):
        """옛 형식은 `version` 이 없습니다. 조용히 오독되지 않아야 합니다."""
        data = config()
        del data["version"]

        with pytest.raises(ValueError, match="0.0.x 형식으로 보입니다"):
            load_kis_config(write(tmp_path, data))

    def test_r1_unknown_version(self, tmp_path):
        with pytest.raises(ValueError, match="아는 판"):
            load_kis_config(write(tmp_path, config(version=99)))

    def test_r1_rejects_actual_old_config(self, tmp_path):
        """#69 이전 형식을 통째로 넣어도 R1 에서 걸립니다."""
        old = {
            "default": "paper",
            "configs": {"paper": {"id": "x", "account": "00000000-01", "paper": True}},
        }

        with pytest.raises(ValueError, match="`version` 이 없습니다"):
            load_kis_config(write(tmp_path, old))

    def test_r2_unknown_key_in_app(self, tmp_path):
        data = config()
        data["apps"]["app_paper1"]["nickname"] = "주계좌"

        with pytest.raises(ValueError, match="모르는 키가 있습니다: nickname"):
            load_kis_config(write(tmp_path, data))

    def test_r2_typo_is_not_silently_ignored(self, tmp_path):
        """`mode` 를 `mdoe` 로 잘못 쓰면 R2 가 잡습니다.

        조용히 무시되면 R3 이 "mode 가 없다"고만 말해 원인이 안 보입니다.
        """
        data = config()
        data["apps"]["app_paper1"]["mdoe"] = "paper"
        del data["apps"]["app_paper1"]["mode"]

        with pytest.raises(ValueError, match="모르는 키가 있습니다: mdoe"):
            load_kis_config(write(tmp_path, data))

    def test_r3_missing_required_key(self, tmp_path):
        data = config()
        del data["apps"]["app_paper1"]["app_secret"]

        with pytest.raises(ValueError, match="필수 키가 없습니다: app_secret"):
            load_kis_config(write(tmp_path, data))

    def test_r4_bad_mode_value(self, tmp_path):
        """값 오타 — 키는 맞고 값이 틀린 경우. R2 가 못 잡는 종류입니다."""
        data = config()
        data["apps"]["app_paper1"]["mode"] = "papr"

        with pytest.raises(ValueError, match="live | paper"):
            load_kis_config(write(tmp_path, data))

    def test_r5_account_points_at_missing_app(self, tmp_path):
        data = config()
        data["accounts"]["acc_paper1"]["app"] = "app_nope"

        with pytest.raises(ValueError, match="apps 에 없습니다"):
            load_kis_config(write(tmp_path, data))

    def test_r6_orphan_app_is_rejected(self, tmp_path):
        """아무 계좌도 쓰지 않는 앱 — 자격증명이 든 블록이 방치되는 것을 막습니다."""
        data = config()
        data["apps"]["app_live1"] = {
            "mode": "live",
            "hts_id": "x",
            "app_key": "b" * 36,
            "app_secret": "t" * 180,
        }

        with pytest.raises(ValueError, match="아무 계좌도 쓰지 않는 것이 있습니다: app_live1"):
            load_kis_config(write(tmp_path, data))

    def test_r7_two_accounts_without_default(self, tmp_path):
        data = config()
        data["accounts"]["acc_paper2"] = {"app": "app_paper1", "account_no": "11111111", "product_code": "01"}
        del data["default_account"]

        with pytest.raises(ValueError, match="default_account 가 없습니다"):
            load_kis_config(write(tmp_path, data))

    def test_r8_default_account_points_nowhere(self, tmp_path):
        """초안 템플릿이 실제로 갖고 있던 결함입니다."""
        with pytest.raises(ValueError, match="accounts 에 없습니다"):
            load_kis_config(write(tmp_path, config(default_account="acc_nope")))

    def test_r9_unquoted_account_no_becomes_int(self, tmp_path):
        """`account_no: 00000000` 은 따옴표가 없으면 정수 `0` 입니다.

        사용자 오타가 아니라 YAML 의 함정이라, 오류 메시지가 원인을 말해야 합니다.
        """
        path = tmp_path / "account_profiles.yaml"
        path.write_text(
            "version: 1\n"
            "apps:\n"
            "  app_paper1:\n"
            '    mode: "paper"\n'
            '    hts_id: "x"\n'
            '    app_key: "k"\n'
            '    app_secret: "s"\n'
            "accounts:\n"
            "  acc_paper1:\n"
            '    app: "app_paper1"\n'
            "    account_no: 00000000\n"
            '    product_code: "01"\n',
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match='따옴표를 씌우세요: account_no: "0"'):
            load_kis_config(path)

    def test_r9_unquoted_mode_off_becomes_bool(self, tmp_path):
        """YAML 1.1 의 `no`/`off` 는 불리언입니다."""
        data = config()
        data["apps"]["app_paper1"]["mode"] = False

        with pytest.raises(ValueError, match="따옴표를 씌우세요"):
            load_kis_config(write(tmp_path, data))


class TestOptionalBlocks:
    def test_user_agent_defaults_to_none(self, tmp_path):
        assert load_kis_config(write(tmp_path, config())).user_agent is None

    def test_user_agent_is_read(self, tmp_path):
        cfg = load_kis_config(write(tmp_path, config(user_agent="Mozilla/5.0")))

        assert cfg.user_agent == "Mozilla/5.0"

    def test_endpoints_partial_override(self, tmp_path):
        """웹소켓 포트만 바뀌는 일이 흔해서 부분 지정을 허용합니다."""
        cfg = load_kis_config(write(tmp_path, config(endpoints={"paper": {"ws_url": "ws://x:1"}})))

        assert cfg.endpoint("paper").ws_url == "ws://x:1"
        assert cfg.endpoint("paper").base_url is None, "적지 않은 것은 기본값을 씁니다"
        assert cfg.endpoint("live").ws_url is None

    def test_endpoints_unknown_mode(self, tmp_path):
        with pytest.raises(ValueError, match="모르는 키가 있습니다: staging"):
            load_kis_config(write(tmp_path, config(endpoints={"staging": {"ws_url": "ws://x:1"}})))

    def test_endpoints_unknown_topic(self, tmp_path):
        with pytest.raises(ValueError, match="모르는 키가 있습니다: rest_url"):
            load_kis_config(write(tmp_path, config(endpoints={"paper": {"rest_url": "https://x"}})))


class TestMalformedShapes:
    """모양이 아예 틀린 입력.

    이 모듈의 본업이 거부이므로, 거부 경로가 검사되지 않으면 안 됩니다.
    사용자가 들여쓰기를 잘못하면 여기로 옵니다 — `AttributeError` 대신 설명이
    나와야 합니다.
    """

    def test_file_is_not_a_mapping(self, tmp_path):
        path = tmp_path / "account_profiles.yaml"
        path.write_text("- 목록입니다\n", encoding="utf-8")

        with pytest.raises(ValueError, match="매핑이 아닙니다: list"):
            load_kis_config(path)

    def test_apps_is_not_a_mapping(self, tmp_path):
        with pytest.raises(ValueError, match="apps 가 비어 있거나 매핑이 아닙니다"):
            load_kis_config(write(tmp_path, config(apps=["app_paper1"])))

    def test_apps_is_empty(self, tmp_path):
        with pytest.raises(ValueError, match="apps 가 비어 있거나"):
            load_kis_config(write(tmp_path, config(apps={})))

    def test_accounts_is_empty(self, tmp_path):
        with pytest.raises(ValueError, match="accounts 가 비어 있거나"):
            load_kis_config(write(tmp_path, config(accounts={})))

    def test_app_block_is_not_a_mapping(self, tmp_path):
        with pytest.raises(ValueError, match="apps.app_paper1 이\\(가\\) 매핑이 아닙니다: str"):
            load_kis_config(write(tmp_path, config(apps={"app_paper1": "oops"})))

    def test_account_block_is_not_a_mapping(self, tmp_path):
        with pytest.raises(ValueError, match="accounts.acc_paper1 이\\(가\\) 매핑이 아닙니다: str"):
            load_kis_config(write(tmp_path, config(accounts={"acc_paper1": "oops"})))

    def test_endpoints_is_not_a_mapping(self, tmp_path):
        with pytest.raises(ValueError, match="endpoints 이\\(가\\) 매핑이 아닙니다: list"):
            load_kis_config(write(tmp_path, config(endpoints=["live"])))

    def test_endpoint_block_is_not_a_mapping(self, tmp_path):
        with pytest.raises(ValueError, match="endpoints.live 이\\(가\\) 매핑이 아닙니다: str"):
            load_kis_config(write(tmp_path, config(endpoints={"live": "https://x"})))

    def test_token_dir_is_not_a_string(self, tmp_path):
        with pytest.raises(ValueError, match="token_dir 이 문자열이 아닙니다"):
            load_kis_config(write(tmp_path, config(token_dir=1)))

    def test_absolute_token_dir_is_used_as_is(self, tmp_path):
        """절대경로는 설정 파일 기준으로 붙이지 않습니다."""
        elsewhere = tmp_path / "elsewhere"
        cfg = load_kis_config(write(tmp_path, config(token_dir=str(elsewhere))))

        assert cfg.account().token_path == elsewhere / "app_paper1.json"


class TestAccountSelection:
    def test_unknown_account_name(self, tmp_path):
        cfg = load_kis_config(write(tmp_path, config()))

        with pytest.raises(ValueError, match="계좌 'nope' 가 없습니다"):
            cfg.account("nope")
