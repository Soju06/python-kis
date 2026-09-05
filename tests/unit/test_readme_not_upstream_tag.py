"""README 가 업스트림 태그를 이 배포판처럼 읽히게 하지 않는지 봅니다. (#135)

Wiki Tutorial 앵커는 스텁이라 404 입니다. 검사는 README 와 이슈 템플릿만
봅니다. 위키 git 은 이 저장소 밖입니다.
"""

from __future__ import annotations

import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
README = REPO_ROOT / "README.md"
TEMPLATES = REPO_ROOT / ".github" / "ISSUE_TEMPLATE"

_CONFUSING = (
    "2.0.0 버전 이전",
    "wiki/Tutorial#",
    "3.11을 기준으로",
)


def _confusing_hits(text: str) -> list[str]:
    return [needle for needle in _CONFUSING if needle in text]


def test_readme_does_not_imply_this_project_is_2_0_0() -> None:
    text = README.read_text(encoding="utf-8")

    assert not _confusing_hits(text), (
        f"README 가 업스트림 태그나 빈 Wiki 를 이 배포판처럼 읽히게 합니다: {_confusing_hits(text)}"
    )
    assert "업스트림" in text
    assert "python-kis" in text


def test_issue_templates_do_not_call_wiki_docs() -> None:
    hits: list[str] = []
    for path in sorted(TEMPLATES.iterdir()):
        if path.suffix not in {".yml", ".yaml"}:
            continue
        if "vm-stock-kis/wiki" in path.read_text(encoding="utf-8"):
            hits.append(str(path.relative_to(REPO_ROOT)))

    assert not hits, "이슈 템플릿이 빈 Wiki 를 Docs 라고 부릅니다:\n  " + "\n  ".join(hits)


def test_readme_does_not_keep_virtual_secret_filename() -> None:
    """#141. Home 의 virtual_ 파일명을 이 배포판처럼 두지 않습니다."""
    text = README.read_text(encoding="utf-8")

    assert "virtual_secret.json" not in text
    assert "paper_secret.json" in text
    assert "hynix = kis.stock(" in text
    assert "account = kis.account()" in text


def test_virtual_secret_filename_is_caught() -> None:
    assert "virtual_secret.json" in 'kis = VmKis("secret.json", "virtual_secret.json")\n'


_UPSTREAM_VER_HEADING = "### ver "


def test_readme_does_not_paste_upstream_changelog_entries() -> None:
    """#143. 업스트림 항목별 이력은 Releases 로 둡니다."""
    text = README.read_text(encoding="utf-8")

    assert _UPSTREAM_VER_HEADING not in text
    assert "CHANGELOG.md" in text
    assert "## License" in text
    assert "[MIT](./LICENCE)" in text


def test_pasted_upstream_ver_heading_is_caught() -> None:
    assert _UPSTREAM_VER_HEADING in "### ver 2.1.3\n"


def test_stale_readme_sentence_is_caught() -> None:
    """#135 이전의 혼동 문장을 그대로 먹여 봅니다."""
    stale = (
        "**2.0.0 버전 이전의 라이브러리는 여기**\n"
        "라이브러리는 파이썬 3.11을 기준으로 작성되었습니다.\n"
        "[인증](https://github.com/visualmoney/vm-stock-kis/wiki/Tutorial#1-인증)\n"
    )

    assert _confusing_hits(stale) == list(_CONFUSING)
