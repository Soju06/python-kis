"""살아 있는 문서가 허브-스포크와 다른 그림을 가르치지 않는지 봅니다. (#146)

동결 문서(reports · dev_logs · prompts · archive)는 당시 서술입니다.
SECURITY 의 virtual_secret.json 은 막는 옛 이름이라 허용합니다.
"""

from __future__ import annotations

import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
SKIP_PARTS = {"reports", "dev_logs", "prompts", "archive", "generated", "examples"}
SECURITY_NAMES = {"SECURITY.md", "SECURITY.en.md"}

_LIES = (
    "_KisMarketInfo",
    'period="D"',
    "period='D'",
    "end_date=",
    '.chart("D")',
    ".chart('D')",
    "vmkis._internal",
    'VmKis("config.yaml")',
    "VmKis('config.yaml')",
    "Scope Layer",
    "Adapter Layer",
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


def _hits(text: str, needles: tuple[str, ...]) -> list[str]:
    return [needle for needle in needles if needle in text]


def test_living_docs_do_not_teach_the_old_picture() -> None:
    hits: list[str] = []
    for path in _living_markdown():
        text = path.read_text(encoding="utf-8")
        origin = path.relative_to(REPO_ROOT)
        found = _hits(text, _LIES)
        if found:
            hits.append(f"{origin}: {found}")

    assert not hits, "살아 있는 문서가 옛 계층·호출을 가르칩니다:\n  " + "\n  ".join(hits)


def test_developer_guide_does_not_keep_virtual_secret_filename() -> None:
    text = (REPO_ROOT / "docs" / "developer" / "DEVELOPER_GUIDE.md").read_text(encoding="utf-8")

    assert "virtual_secret.json" not in text
    assert "paper_secret.json" in text


def test_security_may_name_virtual_secret_as_blocked() -> None:
    for name in SECURITY_NAMES:
        text = (REPO_ROOT / name).read_text(encoding="utf-8")
        assert "virtual_secret.json" in text, f"{name} 이 막는 옛 이름을 잃었습니다"


def test_event_to_api_is_not_called_undecided() -> None:
    architecture = (REPO_ROOT / "docs" / "architecture" / "ARCHITECTURE.md").read_text(encoding="utf-8")
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert "아직 판정되지" not in architecture
    assert "아직 판정되지" not in pyproject
    assert "#63" in architecture
    assert "#63" in pyproject


def test_architecture_flow_is_hub_and_spoke() -> None:
    text = (REPO_ROOT / "docs" / "architecture" / "ARCHITECTURE.md").read_text(encoding="utf-8")

    assert "VmKis (kis.py)" in text
    assert 'stock.on("price"' in text
    assert "create_client" in text
    assert "MarketType" in text


def test_old_picture_lies_are_caught() -> None:
    stale = (
        "MarketInfo: TypeAlias = _KisMarketInfo\n"
        'daily_chart = stock.chart(period="D", end_date=date(2024, 12, 10))\n'
        "stock.chart(period='D')\n"
        'charts = kis.stock("005930").chart("D")\n'
        "kis.stock('005930').chart('D')\n"
        "- 내부 구현 (vmkis._internal)\n"
        'kis = VmKis("config.yaml")\n'
        "kis = VmKis('config.yaml')\n"
        "│  Scope Layer (API 진입점) │\n"
        "│  Adapter Layer (기능 추가)   │\n"
    )

    assert set(_hits(stale, _LIES)) == set(_LIES)
