"""서버 토큰 동기화 예제에 개인 경로가 없는지 봅니다. (이슈 #121)

채워진 `scripts/sync_tokens_from_server.sh` 는 gitignore 합니다. 추적되는
것은 자리표시자만 있는 예제입니다. 예제에 서버 홈·저장소 경로가 들어가면
gitignore 가 소용 없습니다.
"""

from __future__ import annotations

import pathlib
import subprocess

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
EXAMPLE = REPO_ROOT / "scripts" / "sync_tokens_from_server.example.sh"
GITIGNORE = REPO_ROOT / ".gitignore"

#: 예제에 있으면 개인 서버 정보가 샌 것입니다.
_PERSONAL = ("ec2-user", "hybridma", "/home/ec2-user", "seo_demo", "seo_real", "withju")


def test_example_script_is_tracked_and_has_placeholders() -> None:
    text = EXAMPLE.read_text(encoding="utf-8")

    assert EXAMPLE.is_file(), f"예제가 없습니다: {EXAMPLE}"
    assert "/path/on/server/to/token" in text
    assert "stock-bot" in text
    assert "configs/token" in text


def test_example_script_does_not_name_a_personal_server_path() -> None:
    text = EXAMPLE.read_text(encoding="utf-8")
    hits = [word for word in _PERSONAL if word in text]

    assert not hits, f"예제에 개인 서버 정보가 있습니다: {hits}"


def test_filled_sync_script_is_gitignored() -> None:
    text = GITIGNORE.read_text(encoding="utf-8")

    assert "scripts/sync_tokens_from_server.sh" in text


def test_example_script_refuses_to_run_unfilled() -> None:
    """자리표시자 그대로 돌리면 복사에 들어가기 전에 멈추는지 봅니다."""
    result = subprocess.run(
        ["bash", str(EXAMPLE)],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2, result.stderr
    assert "REMOTE_TOKEN_DIR" in result.stderr
    assert "access_token" not in result.stdout
    assert "authorization" not in result.stdout


def test_example_script_does_not_print_token_files() -> None:
    """값을 흘릴 수 있는 명령을 예제가 쓰는지 봅니다."""
    text = EXAMPLE.read_text(encoding="utf-8")

    assert "cat " not in text
    assert "jq " not in text
