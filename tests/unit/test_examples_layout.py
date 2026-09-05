"""초·중·고 폴더가 돌아오면 실패합니다. (#155)"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = REPO_ROOT / "examples"

_LIVING = (
    REPO_ROOT / "README.md",
    REPO_ROOT / "QUICKSTART.md",
    REPO_ROOT / "docs" / "SIMPLEKIS_GUIDE.md",
    EXAMPLES / "README.md",
)


def test_curriculum_folders_are_gone() -> None:
    assert not (EXAMPLES / "02_intermediate").exists()
    assert not (EXAMPLES / "03_advanced").exists()
    assert (EXAMPLES / "01_basic").is_dir()


def test_living_docs_do_not_point_at_curriculum() -> None:
    for path in _LIVING:
        text = path.read_text(encoding="utf-8")
        assert "02_intermediate" not in text, f"{path} 가 02_intermediate 를 가리킵니다"
        assert "03_advanced" not in text, f"{path} 가 03_advanced 를 가리킵니다"


def test_curriculum_path_in_living_doc_is_caught() -> None:
    """결함을 되넣으면 문서 검사가 실패합니다."""
    stale = "see examples/02_intermediate/ and examples/03_advanced/\n"

    assert "02_intermediate" in stale
    assert "03_advanced" in stale
