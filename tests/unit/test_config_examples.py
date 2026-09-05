"""저장소가 배포하는 템플릿이 실제로 읽히는지 확인합니다.

템플릿은 사용자가 처음 만나는 파일입니다. 여기가 깨져 있으면 첫걸음에서 막힙니다.
스키마를 고치면서 템플릿 갱신을 잊는 것이 가장 흔한 드리프트라, 규칙 검사를
그대로 통과하는지를 테스트로 묶어 둡니다.

원래 이 파일은 `examples/01_basic/get_quote.py` 안의 **복사본** `load_config` 를
importlib 로 끌어와 테스트했습니다. 그 복사본이 5벌 중 하나였고, 테스트가 중복을
고착시키고 있었습니다 (#69).
"""

import pathlib
import shutil

import pytest

from vmkis.config import load_kis_config

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
TEMPLATE = REPO_ROOT / "configs" / "template_account_profiles.yaml"


def test_template_exists():
    assert TEMPLATE.is_file(), "템플릿이 없으면 사용자가 시작할 방법이 없습니다"


def test_template_passes_validation(tmp_path):
    """템플릿을 그대로 복사해도 R1~R9 를 통과해야 합니다."""
    copied = tmp_path / "account_profiles.yaml"
    shutil.copy(TEMPLATE, copied)

    cfg = load_kis_config(copied)
    account = cfg.account()

    assert account.mode == "paper", "템플릿의 기본값은 모의투자여야 합니다"
    assert account.is_paper is True
    assert account.account == "00000000-01"


def test_template_defaults_to_paper():
    """실전이 기본인 템플릿은 사고의 시작입니다.

    #87 이후 템플릿에는 앱이 **둘** 있습니다 — 모의 계좌도 시세 조회는 실전
    도메인으로 나가므로 실전 앱이 필요하기 때문입니다. 그래서 "mode 가 paper
    하나뿐"이 아니라 **`default_account` 가 가리키는 계좌의 앱이 모의인가**를
    봅니다. 그것이 원래 지키려던 성질입니다.
    """
    config = load_kis_config(TEMPLATE)

    assert config.account().is_paper, (
        f"템플릿의 default_account '{config.default_account}' 가 실전입니다. "
        "실수로 실전에 붙는 것이 기본값이 되면 안 됩니다."
    )


def test_template_token_path_stays_inside_configs(tmp_path):
    """토큰은 설정 파일 옆에 떨어져야 합니다 — `configs/` 는 무시 대상입니다."""
    configs = tmp_path / "configs"
    configs.mkdir()
    copied = configs / "account_profiles.yaml"
    shutil.copy(TEMPLATE, copied)

    assert load_kis_config(copied).account().token_path.parent == configs / "token"


@pytest.mark.parametrize("quoted", ["hts_id", "app_key", "app_secret", "account_no", "product_code"])
def test_template_quotes_every_string(quoted):
    """따옴표가 빠지면 YAML 이 값을 바꿔 버립니다 (R9).

    템플릿은 사용자가 흉내 내는 본보기라, 여기서 따옴표를 빼면 사용자도 뺍니다.
    """
    for line in TEMPLATE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()

        if stripped.startswith(f"{quoted}:") and not stripped.startswith("#"):
            value = stripped.split(":", 1)[1].split("#")[0].strip()
            assert value.startswith('"') and value.endswith('"'), f"{quoted} 에 따옴표가 없습니다: {line}"
