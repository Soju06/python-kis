"""`docs/generated/API_REFERENCE.md` 가 생성기와 같은지 봅니다. (#94)

검사가 없으면 생성기를 안 돌립니다. 0.1.0 이 `live`/`paper` 로 개명한 뒤에도
레퍼런스는 `virtual` 을 13곳 싣고 있었습니다.
"""

from __future__ import annotations

import importlib.util
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "scripts" / "generate_api_reference.py"
OUTPUT = REPO_ROOT / "docs" / "generated" / "API_REFERENCE.md"


def _generator():
    spec = importlib.util.spec_from_file_location("generate_api_reference", GENERATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_api_reference_matches_the_generator() -> None:
    committed = OUTPUT.read_text(encoding="utf-8")
    generated = _generator().render()

    assert committed == generated, (
        "docs/generated/API_REFERENCE.md 가 생성기와 다릅니다. "
        "`uv run python scripts/generate_api_reference.py` 를 돌리세요."
    )


def test_generated_directory_only_has_the_reference() -> None:
    names = sorted(p.name for p in OUTPUT.parent.iterdir() if p.is_file())

    assert names == ["API_REFERENCE.md"], (
        "docs/generated/ 에 생성기가 만들지 않는 파일이 있습니다. "
        "일회성 산출물은 archive/docs/generated/ 로 가세요:\n  " + ", ".join(names)
    )


def test_regenerated_reference_dropped_removed_names() -> None:
    text = OUTPUT.read_text(encoding="utf-8")

    assert "virtual" not in text
    assert "real_auth" not in text
    assert "PyKis" not in text
    assert "pykis." not in text


def test_stale_reference_fails_the_check() -> None:
    """#94 의 결함을 그대로 먹여 봅니다. 파일을 건드리지 않습니다."""
    stale = "# API Reference\n\n>>> KisAuth(virtual=False)\n"

    assert stale != _generator().render(), "검사기가 낡은 레퍼런스를 최신으로 착각합니다"


def test_index_does_not_call_generated_a_folder_of_generators() -> None:
    index = (REPO_ROOT / "docs" / "INDEX.md").read_text(encoding="utf-8")

    assert "자동 생성물 (API 레퍼런스 등)" not in index
    assert "generated/API_REFERENCE.md" in index
