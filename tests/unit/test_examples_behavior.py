"""예제가 자격증명 없이 **동작의 겉면**을 지키는지 봅니다. (#154, #30)

네트워크와 키는 없습니다. 여기서 보는 것은

- 파일이 파이썬으로 열리는가
- `01_basic` 이 `create_client` 를 부르는가 (`hello_world` 스텁 금지)
- `--help` 가 0 으로 끝나는가 (argparse 가 먼저 죽지 않는가)
- 없는 설정으로 실행하면 경로가 보이는가

실제 시세·주문은 `tests/integration/test_examples_run_smoke.py` 입니다.
"""

from __future__ import annotations

import py_compile
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = REPO_ROOT / "examples"
BASIC = EXAMPLES / "01_basic"
MISSING_CONFIG = REPO_ROOT / "configs" / "does_not_exist_for_example_behavior.yaml"


def _basic_scripts() -> list[Path]:
    return sorted(p for p in BASIC.glob("*.py") if p.name != "__init__.py")


def _all_example_scripts() -> list[Path]:
    return sorted(p for p in EXAMPLES.rglob("*.py") if "__pycache__" not in p.parts)


@pytest.mark.parametrize("path", _all_example_scripts(), ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_example_module_compiles(path: Path) -> None:
    py_compile.compile(str(path), doraise=True)


@pytest.mark.parametrize("path", _basic_scripts(), ids=lambda p: p.name)
def test_basic_example_calls_create_client(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    assert "create_client(" in text, f"{path.name} 이 create_client 를 부르지 않습니다"


@pytest.mark.parametrize("path", _basic_scripts(), ids=lambda p: p.name)
def test_basic_example_help_exits_zero(path: Path) -> None:
    proc = subprocess.run(
        [sys.executable, str(path), "--help"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert proc.returncode == 0, f"{path.name} --help 가 {proc.returncode}:\n{proc.stderr}"
    assert "usage" in proc.stdout.lower()


@pytest.mark.parametrize("path", _basic_scripts(), ids=lambda p: p.name)
def test_basic_example_missing_config_names_the_path(path: Path) -> None:
    assert not MISSING_CONFIG.exists()

    proc = subprocess.run(
        [sys.executable, str(path), "--config", str(MISSING_CONFIG)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    combined = proc.stdout + proc.stderr

    assert proc.returncode != 0, f"{path.name} 가 없는 설정으로 0 을 냈습니다"
    assert MISSING_CONFIG.name in combined, f"{path.name} 가 없는 경로를 말하지 않습니다:\n{combined}"


def test_hello_world_stub_fails_create_client_check() -> None:
    stub = 'print("Hello from VM-Stock-KIS example")\n'

    assert "create_client(" not in stub


def test_basic_scripts_are_not_empty() -> None:
    found = _basic_scripts()

    assert len(found) >= 10, f"01_basic 이 {len(found)}개뿐입니다. 경로가 맞습니까?"


def test_integration_smoke_does_not_point_at_the_template() -> None:
    """#154. 옛 연기는 추적 템플릿을 `--config` 로 넘겼습니다."""
    smoke = REPO_ROOT / "tests" / "integration" / "test_examples_run_smoke.py"
    source = smoke.read_text(encoding="utf-8")

    assert '/ "template_account_profiles.yaml"' not in source
    assert "FILLED_CONFIG" in source


def test_old_template_smoke_path_is_caught() -> None:
    old = 'cfg = REPO_ROOT / "configs" / "template_account_profiles.yaml"\n'

    assert '/ "template_account_profiles.yaml"' in old


def test_comment_your_hts_id_is_not_a_template(tmp_path) -> None:
    """#157. 주석에 YOUR_HTS_ID 가 남아도 값이 채워져 있으면 템플릿이 아닙니다."""
    from tests.integration.test_examples_run_smoke import is_unfilled_template

    path = tmp_path / "account_profiles.yaml"
    path.write_text(
        """
version: 1
# 템플릿 안내는 YOUR_HTS_ID 입니다
apps:
  app_paper1:
    mode: "paper"
    hts_id: "filledid"
    app_key: "k123456789012345678901234567890123"
    app_secret: "s123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
accounts:
  acc_paper1:
    app: "app_paper1"
    account_no: "12345678"
    product_code: "01"
default_account: "acc_paper1"
""",
        encoding="utf-8",
    )

    assert "YOUR_HTS_ID" in path.read_text(encoding="utf-8")
    assert is_unfilled_template(path) is False


def test_hours_independent_smoke_excludes_account_reads() -> None:
    """#30. 잔고·계좌 조회는 자격증명 필수 연기가 아닙니다."""
    from tests.integration.test_examples_run_smoke import _HOURS_INDEPENDENT

    assert "get_balance.py" not in _HOURS_INDEPENDENT
    assert "account_lookups.py" not in _HOURS_INDEPENDENT


def test_placeholder_hts_id_is_a_template(tmp_path) -> None:
    from tests.integration.test_examples_run_smoke import is_unfilled_template

    path = tmp_path / "account_profiles.yaml"
    path.write_text(
        """
version: 1
apps:
  app_paper1:
    mode: "paper"
    hts_id: "YOUR_HTS_ID"
    app_key: "k123456789012345678901234567890123"
    app_secret: "s123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
accounts:
  acc_paper1:
    app: "app_paper1"
    account_no: "12345678"
    product_code: "01"
default_account: "acc_paper1"
""",
        encoding="utf-8",
    )

    assert is_unfilled_template(path) is True
