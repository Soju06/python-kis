"""`vmkis.helpers` 테스트.

이 모듈은 오랫동안 커버리지 27%에 머물러 있었다. 원인은 테스트 부족이 아니라
`save_config_interactive()` 본문에 모듈 전체 복사본이 통째로 중첩되어 있었기
때문이다. 바깥 함수는 그 중첩 정의들을 호출하지도 반환하지도 않아
`None`을 반환했고, 선언된 반환 타입 `dict[str, Any]`와 어긋나 있었다.
https://github.com/visualmoney/vm-stock-kis/issues/3

**스키마 검증은 여기 없습니다** — `tests/unit/test_config.py` 로 옮겼습니다 (#75).
helpers 가 하는 일은 설정을 `KisAuth`/`VmKis` 로 **번역**하는 것뿐이라, 이 파일은
그 번역만 봅니다.
"""

import getpass

import pytest
import yaml

from vmkis import helpers

APP = {
    "mode": "paper",
    "hts_id": "testid",
    "app_key": "a" * 36,
    "app_secret": "s" * 180,
}

#: 실전 앱. **모의 계좌만 쓸 때도 설정에 있어야 합니다** — 시세 TR 이
#: 모의도메인에 없어서 모의 계좌도 실전 도메인으로 나갑니다. (이슈 #87)
LIVE_APP = {
    "mode": "live",
    "hts_id": "testid",
    "app_key": "b" * 36,
    "app_secret": "t" * 180,
}

ACCOUNT = {"app": "app_paper1", "account_no": "00000000", "product_code": "01"}
LIVE_ACCOUNT = {"app": "app_live1", "account_no": "11111111", "product_code": "01"}


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """계좌/확인 관련 환경변수가 테스트 사이로 새지 않게 합니다."""
    for name in ("VMKIS_ACCOUNT", "PYKIS_ACCOUNT", "VMKIS_CONFIRM_SKIP"):
        monkeypatch.delenv(name, raising=False)


def write_config(tmp_path, **overrides):
    data = {
        "version": 1,
        "apps": {"app_paper1": dict(APP), "app_live1": dict(LIVE_APP)},
        "accounts": {"acc_paper1": dict(ACCOUNT), "acc_live1": dict(LIVE_ACCOUNT)},
        "default_account": "acc_paper1",
    }
    data.update(overrides)
    path = tmp_path / "account_profiles.yaml"
    path.write_text(yaml.dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


class TestCreateClient:
    """`create_client` 테스트."""

    @pytest.fixture
    def dummy_vmkis(self, monkeypatch):
        """네트워크 호출을 피하기 위해 `VmKis`를 대체합니다."""
        calls = []

        class DummyVmKis:
            def __init__(self, *args, **kwargs):
                calls.append((args, kwargs))

        monkeypatch.setattr(helpers, "VmKis", DummyVmKis)
        return calls

    def test_paper_account_passed_as_second_auth(self, tmp_path, dummy_vmkis):
        """모의 자격증명은 **두 번째** 인자로 가고, 첫 번째는 실전이어야 한다.

        #87 이전에는 이 테스트가 `args[0] is None` 을 단언했습니다. 그런데
        `VmKis` 가 그 형태를 받지 않아 **실제로는 항상 ValueError 였습니다.**
        `dummy_vmkis` 가 생성자를 통째로 대체하고 있어서 테스트가 그 사실을
        보지 못하고 **버그를 박제하고 있었습니다.**

        모의도메인 전용 인증 정보를 실전 인증 정보로 잘못 다루지 않는다는
        원래 의도는 두 번째 인자 검사로 그대로 지켜집니다.
        """
        helpers.create_client(write_config(tmp_path))

        (args, _) = dummy_vmkis[0]
        assert args[0].paper is False, "첫 인자는 실전 인증이어야 합니다"
        assert args[1].paper is True
        assert args[1].account == "00000000-01"

    def test_paper_only_config_says_what_to_add(self, tmp_path, dummy_vmkis):
        """실전 앱이 없는 설정은 **무엇을 추가해야 하는지** 말하고 멈춰야 한다.

        #87 이전 메시지는 `id를 입력해야 합니다` 였습니다. 사용자는 id 를
        빠뜨린 적이 없으므로 그 메시지로는 원인에 닿을 수 없었습니다.
        """
        path = write_config(
            tmp_path,
            apps={"app_paper1": dict(APP)},
            accounts={"acc_paper1": dict(ACCOUNT)},
        )

        with pytest.raises(ValueError) as exc:
            helpers.create_client(path)

        message = str(exc.value)
        assert "실전 계좌가 하나도 없습니다" in message
        assert 'mode: "live"' in message, "무엇을 추가해야 하는지 말해야 합니다"

    def test_live_account_passed_as_positional_auth(self, tmp_path, dummy_vmkis):
        """실전 자격증명은 첫 인자로 전달된다."""
        path = write_config(
            tmp_path,
            apps={"app_paper1": dict(APP, mode="live")},
            accounts={"acc_paper1": dict(ACCOUNT)},
        )

        helpers.create_client(path)

        (args, _) = dummy_vmkis[0]
        assert args[0].paper is False

    def test_account_argument_selects(self, tmp_path, dummy_vmkis):
        path = write_config(
            tmp_path,
            accounts={
                "acc_paper1": dict(ACCOUNT),
                "acc_paper2": dict(ACCOUNT, account_no="11111111", product_code="02"),
                "acc_live1": dict(LIVE_ACCOUNT),
            },
        )

        helpers.create_client(path, account="acc_paper2")

        (args, _) = dummy_vmkis[0]
        assert args[1].account == "11111111-02"

    def test_real_vmkis_is_actually_constructed(self, tmp_path):
        """**`VmKis` 를 모킹하지 않고** 끝까지 만듭니다. (이슈 #87)

        이 클래스의 다른 테스트는 `dummy_vmkis` 로 생성자를 대체합니다. 호출
        형태를 보기에는 그게 맞지만, **그래서 #87 을 놓쳤습니다** — `create_client`
        가 `VmKis(None, auth)` 를 부르고 있었고 진짜 생성자는 그것을 거부하는데,
        대역은 무엇이든 받았습니다. 테스트는 초록이고 사용자는 `ValueError` 를
        받는 상태가 8개월 갔습니다.

        자격증명은 **형식만** 맞으면 되고 네트워크는 타지 않습니다. 토큰 발급이
        지연되기 때문입니다(`VmKis.token` 은 프로퍼티입니다).
        """
        path = write_config(
            tmp_path,
            apps={
                "app_paper1": dict(APP, app_key="P" + "A" * 35, app_secret="S" * 180),
                "app_live1": dict(LIVE_APP, app_key="P" + "B" * 35, app_secret="T" * 180),
            },
        )

        kis = helpers.create_client(path, keep_token=False)

        assert kis.paper is True, "모의 계좌를 골랐으므로 모의 클라이언트여야 합니다"
        assert kis.appkey.appkey.endswith("B" * 35), "실전 앱키가 실려야 합니다"
        assert kis.paper_appkey.appkey.endswith("A" * 35), "모의 앱키가 실려야 합니다"

    def test_token_path_comes_from_config(self, tmp_path, dummy_vmkis):
        """토큰 경로는 설정이 정합니다 — 앱 이름에서 파생됩니다."""
        path = write_config(tmp_path)

        helpers.create_client(path)

        (_, kwargs) = dummy_vmkis[0]
        assert kwargs["keep_token"] == tmp_path / "token" / "app_paper1.json"
        assert (tmp_path / "token").is_dir(), "저장 폴더를 미리 만들어야 한다"

    def test_keep_token_false_disables_saving(self, tmp_path, dummy_vmkis):
        helpers.create_client(write_config(tmp_path), keep_token=False)

        (_, kwargs) = dummy_vmkis[0]
        assert kwargs["keep_token"] is False
        assert not (tmp_path / "token").exists(), "저장하지 않는데 폴더를 만들면 안 된다"

    def test_user_agent_is_forwarded(self, tmp_path, dummy_vmkis):
        helpers.create_client(write_config(tmp_path, user_agent="Mozilla/5.0"))

        (_, kwargs) = dummy_vmkis[0]
        assert kwargs["user_agent"] == "Mozilla/5.0"

    def test_endpoints_are_translated_to_domain_vocabulary(self, tmp_path, dummy_vmkis):
        """설정은 live/paper, `VmKis` 는 live/paper 로 말합니다.

        #70 이 코드 쪽을 개명하면 이 번역은 사라집니다. 그때 이 테스트도 함께
        지워야 하므로 이유를 남겨 둡니다.
        """
        path = write_config(tmp_path, endpoints={"paper": {"ws_url": "ws://x:1"}})

        helpers.create_client(path)

        (_, kwargs) = dummy_vmkis[0]
        assert set(kwargs["endpoints"]) == {"paper"}
        assert kwargs["endpoints"]["paper"].ws_url == "ws://x:1"

    def test_invalid_config_fails_before_client_is_made(self, tmp_path, dummy_vmkis):
        """검증 실패면 클라이언트가 만들어지면 안 됩니다."""
        path = write_config(tmp_path, default_account="acc_nope")

        with pytest.raises(ValueError, match="accounts 에 없습니다"):
            helpers.create_client(path)

        assert not dummy_vmkis, "실패해야 하는데 클라이언트가 만들어졌다"


class TestSaveConfigInteractive:
    """`save_config_interactive` 테스트."""

    @pytest.fixture
    def answers(self, monkeypatch):
        """`input`/`getpass`를 대본으로 대체합니다."""
        script = []

        def fake_input(prompt=""):
            assert script, f"입력 대본이 소진되었습니다. 프롬프트: {prompt!r}"
            return script.pop(0)

        monkeypatch.setattr("builtins.input", fake_input)
        monkeypatch.setattr(getpass, "getpass", lambda prompt="": "s" * 180)
        return script

    def test_writes_yaml_and_returns_data(self, tmp_path, answers, monkeypatch):
        """확인을 건너뛰면 파일을 쓰고 저장한 값을 반환한다."""
        monkeypatch.setenv("VMKIS_CONFIRM_SKIP", "1")
        answers.extend(["myid", "00000000", "01", "myappkey", "y"])
        path = tmp_path / "configs" / "account_profiles.yaml"

        result = helpers.save_config_interactive(str(path))

        assert result["version"] == 1
        assert result["apps"]["app_paper1"]["hts_id"] == "myid"
        assert result["apps"]["app_paper1"]["app_key"] == "myappkey"
        assert result["apps"]["app_paper1"]["app_secret"] == "s" * 180
        assert result["apps"]["app_paper1"]["mode"] == "paper"
        assert result["accounts"]["acc_paper1"]["account_no"] == "00000000"
        assert result["default_account"] == "acc_paper1"

        # 반환값이 실제로 파일에 쓰인 내용과 일치해야 한다.
        assert yaml.safe_load(path.read_text(encoding="utf-8")) == result

    def test_written_file_passes_its_own_validation(self, tmp_path, answers, monkeypatch):
        """스스로 만든 파일이 스키마를 통과해야 합니다.

        쓰는 쪽과 읽는 쪽이 어긋나면 사용자는 "방금 만든 파일이 안 읽힌다"를
        만납니다. 이전 스키마에서 실제로 두 곳이 키 문자열을 따로 적고 있었습니다.
        """
        from vmkis.config import load_kis_config

        monkeypatch.setenv("VMKIS_CONFIRM_SKIP", "1")
        answers.extend(["myid", "00000000", "01", "myappkey", "n"])
        path = tmp_path / "configs" / "account_profiles.yaml"

        helpers.save_config_interactive(str(path))

        assert load_kis_config(path).account().mode == "live"

    @pytest.mark.parametrize(
        ("answer", "expected"),
        [("y", "paper"), ("yes", "paper"), ("true", "paper"), ("1", "paper"), ("n", "live"), ("", "live")],
    )
    def test_paper_answer_parsing(self, tmp_path, answers, monkeypatch, answer, expected):
        monkeypatch.setenv("VMKIS_CONFIRM_SKIP", "1")
        answers.extend(["myid", "00000000", "01", "myappkey", answer])

        result = helpers.save_config_interactive(str(tmp_path / "account_profiles.yaml"))

        assert next(iter(result["apps"].values()))["mode"] == expected

    def test_product_code_defaults_to_01(self, tmp_path, answers, monkeypatch):
        monkeypatch.setenv("VMKIS_CONFIRM_SKIP", "1")
        answers.extend(["myid", "00000000", "", "myappkey", "y"])

        result = helpers.save_config_interactive(str(tmp_path / "account_profiles.yaml"))

        assert result["accounts"]["acc_paper1"]["product_code"] == "01"

    def test_confirm_prompt_accepts_write(self, tmp_path, answers):
        """확인 프롬프트에 y로 답하면 기록한다."""
        answers.extend(["myid", "00000000", "01", "myappkey", "n", "y"])
        path = tmp_path / "account_profiles.yaml"

        helpers.save_config_interactive(str(path))

        assert path.exists()

    def test_declining_aborts_without_writing(self, tmp_path, answers):
        """확인 프롬프트를 거절하면 파일을 쓰지 않고 SystemExit."""
        answers.extend(["myid", "00000000", "01", "myappkey", "n", "N"])
        path = tmp_path / "account_profiles.yaml"

        with pytest.raises(SystemExit, match="Aborted by user"):
            helpers.save_config_interactive(str(path))

        assert not path.exists()
