"""살아 있는 문서가 없는 `config.yaml` 을 복사하라고 하지 않는지 봅니다. (#112)

`examples/` 이름 검사를 `docs/` 에 그대로 확장하면 안 됩니다.
마이그레이션 문서와 안정성 정책은 **옛 이름을 일부러** 보여 줍니다.
그래서 막는 것은 따라 하면 파일이 없는 호출뿐입니다.

    create_client("config.yaml")
    save_config_interactive("config.yaml")
"""

from __future__ import annotations

import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
SKIP_PARTS = {"reports", "dev_logs", "prompts", "archive", "generated", "examples"}

_FORBIDDEN_CALLS = (
    'create_client("config.yaml")',
    "create_client('config.yaml')",
    'save_config_interactive("config.yaml")',
    "save_config_interactive('config.yaml')",
)


def _living_markdown() -> list[pathlib.Path]:
    found: set[pathlib.Path] = set()
    for root in (REPO_ROOT / "docs", REPO_ROOT):
        iterator = root.rglob("*.md") if root != REPO_ROOT else root.glob("*.md")
        for path in iterator:
            if SKIP_PARTS & set(path.relative_to(REPO_ROOT).parts):
                continue
            if ".venv" in path.parts:
                continue
            found.add(path)
    return sorted(found)


def test_living_docs_do_not_tell_you_to_call_create_client_on_config_yaml() -> None:
    hits: list[str] = []
    for path in _living_markdown():
        text = path.read_text(encoding="utf-8")
        origin = path.relative_to(REPO_ROOT)
        for i, line in enumerate(text.splitlines(), 1):
            if any(call in line for call in _FORBIDDEN_CALLS):
                hits.append(f"{origin}:{i} — {line.strip()}")

    assert not hits, (
        "살아 있는 문서가 없는 config.yaml 을 읽으라고 합니다. "
        "configs/account_profiles.yaml 로 적으세요:\n  " + "\n  ".join(hits)
    )


def test_config_schema_quote_uses_the_real_error_shape() -> None:
    """R1 메시지는 파일 경로를 앞에 붙입니다. `config.yaml 에` 로 시작하면 가짜입니다."""
    text = (REPO_ROOT / "docs" / "guidelines" / "CONFIG_SCHEMA.md").read_text(encoding="utf-8")

    assert "config.yaml 에 `version` 이 없습니다" not in text
    assert "에 `version` 이 없습니다" in text


def test_the_living_docs_checker_sees_simplekis_guide() -> None:
    paths = {p.name for p in _living_markdown()}

    assert "SIMPLEKIS_GUIDE.md" in paths, f"SIMPLEKIS_GUIDE 가 검사 밖입니다: {sorted(paths)}"


def test_quote_redistribution_is_stated_without_copying_the_terms() -> None:
    """#96: 요지와 원문 링크는 있고, 약관 전문은 없습니다."""
    guide = (REPO_ROOT / "docs" / "user" / "USER_GUIDE.md").read_text(encoding="utf-8")
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    english = (REPO_ROOT / "docs" / "user" / "en" / "README.md").read_text(encoding="utf-8")

    assert "제5조" in guide and "apiportal.koreainvestment.com" in guide
    assert "시세 재배포" in readme and "apiportal.koreainvestment.com" in readme
    assert "your own use only" in english.lower()
    assert "제 5 조 (이용 신청)" not in guide
    assert "제 5 조 (이용 신청)" not in readme
