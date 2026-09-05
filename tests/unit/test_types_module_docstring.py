"""`vmkis.types` 모듈 docstring 이 배포 계열을 현재라고 박지 않는지 봅니다. (#126)

#94 는 살아 있는 마크다운만 봤습니다. 이 파일은 생성기 대상도 아니라서
`API_REFERENCE` 재생성이 고쳐 주지 않습니다.

`현재(0.1.0)` 으로 바꾸면 #100 뒤에 예정된 0.2.0 태그에서 또 낡습니다.
"""

from __future__ import annotations

import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
TYPES = REPO_ROOT / "src" / "vmkis" / "types.py"

#: `현재(0.0.1)` · `현재(0.1.0)` 같이 배포 숫자를 현재에 붙인 것.
_STALE_CURRENT = re.compile(r"현재\s*\(\s*[01]\.\d+")


def _stale_current_hits(text: str, origin: str) -> list[str]:
    return [
        f"{origin}:{i} — {line.strip()}" for i, line in enumerate(text.splitlines(), 1) if _STALE_CURRENT.search(line)
    ]


def test_types_docstring_does_not_name_a_release_as_current() -> None:
    hits = _stale_current_hits(TYPES.read_text(encoding="utf-8"), "src/vmkis/types.py")

    assert not hits, (
        "모듈 docstring 이 배포 계열을 현재라고 적습니다. 태그는 git describe 가 정합니다:\n  " + "\n  ".join(hits)
    )


def test_compat_table_says_root_path_is_gone() -> None:
    text = TYPES.read_text(encoding="utf-8")

    assert re.search(r"1\.0\.0\+\s*\|\s*✅\s*적용", text), "1.0.0+ 적용 행이 없습니다"
    assert not re.search(r"0\.0\.x\s*\|\s*✅\s*활성", text), "0.0.x 활성 행이 아직 있습니다"


def test_stale_current_line_is_caught() -> None:
    """#126 의 결함을 그대로 먹여 봅니다."""
    hits = _stale_current_hits("- 현재(0.0.1): 기존 코드가 경고와 함께 계속 동작", "<결함>")

    assert hits, "검사기가 '현재(0.0.1)' 을 못 잡습니다"


def test_next_tag_as_current_is_also_caught() -> None:
    hits = _stale_current_hits("- 현재(0.1.0): 기존 코드가 경고와 함께 계속 동작", "<결함>")

    assert hits, "검사기가 '현재(0.1.0)' 을 못 잡습니다"
