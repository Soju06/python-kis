"""examples/README 가 배포 버전을 바닥에 박지 않는지 봅니다. (#136)

살아 있는 문서 검사기는 `docs/` 와 저장소 루트만 봅니다. 예제 안내가
`1.0.0` 을 현재처럼 읽히게 해도 거기로는 안 잡힙니다.
"""

from __future__ import annotations

import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
EXAMPLES_README = REPO_ROOT / "examples" / "README.md"

_PINNED_VERSION = re.compile(r"\*\*버전\*\*:\s*\d+\.\d+")
_STALE_DATE = "2025-12-19"


def _pin_hits(text: str) -> list[str]:
    hits: list[str] = []
    if _PINNED_VERSION.search(text):
        hits.append("버전")
    if _STALE_DATE in text:
        hits.append(_STALE_DATE)
    return hits


def test_examples_readme_does_not_pin_a_version() -> None:
    text = EXAMPLES_README.read_text(encoding="utf-8")

    assert not _pin_hits(text), f"examples/README.md 가 배포 버전이나 낡은 날짜를 박습니다: {_pin_hits(text)}"


def test_pinned_footer_is_caught() -> None:
    """#136 이전의 바닥 줄을 그대로 먹여 봅니다."""
    stale = "**마지막 업데이트**: 2025-12-19\n**버전**: 1.0.0\n**상태**: 모든 예제 작동 확인 완료\n"

    assert _pin_hits(stale) == ["버전", _STALE_DATE]
