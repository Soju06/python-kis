"""살아 있는 문서의 '현재 버전' 주장이 최신 태그와 맞는지 봅니다. (#94)

릴리스가 진실을 바꾸는데 문서가 안 따라오면, API_REFERENCE 가 낡는 것과
같은 뿌리입니다. 생성기는 그쪽을, 이 파일은 버전 표기를 봅니다.

`지난 판` 줄은 위반이 아닙니다 — API_STABILITY_POLICY 의 0.0.x 행이
#30 의 근거입니다.
"""

from __future__ import annotations

import pathlib
import re
import subprocess

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
SKIP_PARTS = {"reports", "dev_logs", "prompts", "archive", "generated"}

#: 배포판 계열. Python 3.10 · 스키마 `1` 은 잡지 않습니다.
_PKG_VER = re.compile(r"\b([01](?:\.\d+|\.x)(?:\.\d+|\.x)?)\b")
_HARDCODED_PROJECT = re.compile(r"\*\*버전\*\*:\s*\d+\.\d+")
_HARDCODED_PRINT = re.compile(r"출력:.*VmKis 버전:\s*\d+\.\d+")


def _latest_series() -> tuple[int, int]:
    tag = (
        subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=REPO_ROOT,
            text=True,
        )
        .strip()
        .lstrip("v")
    )
    major, minor, *_ = tag.split(".")
    return int(major), int(minor)


def _claimed_matches(ver: str, current: tuple[int, int]) -> bool:
    if ver.endswith(".x") and ver.count(".") == 1:
        return int(ver[0]) == current[0]
    parts = ver.replace(".x", "").split(".")
    major = int(parts[0])
    minor = int(parts[1]) if len(parts) > 1 else None
    if major != current[0]:
        return False
    if minor is None:
        return True
    return minor == current[1]


def _current_version_hits(text: str, origin: str, current: tuple[int, int]) -> list[str]:
    hits: list[str] = []
    for i, line in enumerate(text.splitlines(), 1):
        if _HARDCODED_PROJECT.search(line) or _HARDCODED_PRINT.search(line):
            hits.append(f"{origin}:{i} — {line.strip()}")
            continue
        if "현재" not in line or "지난" in line:
            continue
        for match in _PKG_VER.finditer(line):
            ver = match.group(1)
            if not _claimed_matches(ver, current):
                hits.append(f"{origin}:{i} — {line.strip()}  (최신 태그 계열 {current[0]}.{current[1]})")
    return hits


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


def test_living_docs_current_version_matches_latest_tag() -> None:
    current = _latest_series()
    hits: list[str] = []
    for path in _living_markdown():
        hits.extend(
            _current_version_hits(
                path.read_text(encoding="utf-8"),
                str(path.relative_to(REPO_ROOT)),
                current,
            )
        )

    assert not hits, (
        "살아 있는 문서가 낡은 계열을 현재라고 적습니다. "
        "git 태그를 보거나, 지난 판이면 '지난'을 적으세요:\n  " + "\n  ".join(hits)
    )


def test_stale_current_series_is_caught() -> None:
    """#94 코멘트의 결함을 그대로 먹여 봅니다."""
    hits = _current_version_hits("| 0.0.x | 🟢 **현재** |", "<결함>", (0, 1))

    assert hits, "검사기가 '0.0.x 가 현재'를 못 잡습니다"


def test_historical_past_series_is_not_caught() -> None:
    hits = _current_version_hits(
        "| 0.0.x | ⚪ 지난 판 (2026-08-28 ~ 08-29) |",
        "<근거>",
        (0, 1),
    )

    assert not hits, f"#30 근거 줄을 위반으로 잡았습니다: {hits}"


def test_current_series_line_is_ok() -> None:
    hits = _current_version_hits(
        "| **0.1.x** | 🟢 **현재** (2026-08-29 이후) |",
        "<현재>",
        (0, 1),
    )

    assert not hits, f"맞는 현재 계열을 잡았습니다: {hits}"


def test_hardcoded_project_version_is_caught() -> None:
    hits = _current_version_hits(
        "- **버전**: 0.0.1 (이 배포명의 첫 릴리스)",
        "<결함>",
        (0, 1),
    )

    assert hits, "검사기가 '버전: 0.0.1' 칸을 못 잡습니다"


def test_hardcoded_print_example_is_caught() -> None:
    hits = _current_version_hits("# 출력: VmKis 버전: 0.0.1", "<결함>", (0, 1))

    assert hits, "검사기가 출력 예제의 고정 버전을 못 잡습니다"


def test_the_version_checker_reads_architecture() -> None:
    names = {p.name for p in _living_markdown()}

    assert "ARCHITECTURE.md" in names
    assert "API_STABILITY_POLICY.md" in names
