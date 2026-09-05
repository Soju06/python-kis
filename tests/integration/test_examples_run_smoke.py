"""채운 설정이 있을 때만 장중 무관 `01_basic` 조회 예제를 실행합니다. (#154, #157)

예전 검사는 파일 문자열에 `YOUR_HTS_ID` 가 있으면 skip 했습니다. 주석에
그 조각이 남은 채운 파일도 템플릿으로 봤습니다. 지금은 `load_kis_config` 가
읽은 `hts_id` / `app_key` 가 `YOUR_` 로 시작하는지만 봅니다.

주문·웹소켓은 장중 의존이라 넣지 않습니다.
잔고·계좌 조회(`get_balance` · `account_lookups`)는 `#30` 동작의
필수 연기가 아닙니다. 파일은 두고 이 목록에만 넣지 않습니다.
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys

import pytest

from vmkis.config import load_kis_config

pytestmark = [pytest.mark.integration, pytest.mark.requires_api]

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
FILLED_CONFIG = REPO_ROOT / "configs" / "account_profiles.yaml"

_HOURS_INDEPENDENT = (
    "hello_world.py",
    "keep_token.py",
    "get_quote.py",
    "get_chart.py",
    "get_orderbook.py",
    "trading_hours.py",
)


def is_unfilled_template(path: pathlib.Path) -> bool:
    """자리표시자인지는 파싱된 필드만 봅니다. 주석의 YOUR_HTS_ID 는 무시합니다."""
    try:
        cfg = load_kis_config(path)
        acc = cfg.account()
    except (OSError, ValueError):
        return True
    return acc.hts_id.startswith("YOUR_") or acc.app_key.startswith("YOUR_")


def _filled_config() -> pathlib.Path:
    if os.environ.get("RUN_INTEGRATION") != "1":
        pytest.skip("RUN_INTEGRATION=1 일 때만 예제 연기를 돌립니다")
    if not FILLED_CONFIG.is_file():
        pytest.skip(f"{FILLED_CONFIG} 가 없습니다. 템플릿을 복사해 채우세요")
    if is_unfilled_template(FILLED_CONFIG):
        pytest.skip(f"{FILLED_CONFIG} 가 아직 템플릿입니다")
    return FILLED_CONFIG


@pytest.mark.parametrize("name", _HOURS_INDEPENDENT)
def test_basic_read_example_runs_with_filled_config(name: str) -> None:
    cfg = _filled_config()
    script = REPO_ROOT / "examples" / "01_basic" / name
    env = os.environ.copy()
    env.setdefault("VMKIS_ACCOUNT", "acc_paper_1")
    proc = subprocess.run(
        [sys.executable, str(script), "--config", str(cfg)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )

    assert proc.returncode == 0, f"{name} 가 {proc.returncode}"
