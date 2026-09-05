"""`docs/README.md` 가 다시 두 번째 인덱스가 되지 않게 합니다. (이슈 #103)

## 왜 이 검사가 필요한가

GitHub 은 디렉터리를 열면 그 안의 `README.md` 를 렌더링합니다. `docs/` 를 누른
사람이 가장 먼저 보는 자리라 **비워 둘 수 없습니다.** 그런데 거기에 문서 목록을
적으면 `docs/INDEX.md` 와 목적이 같아지고, **인덱스가 둘이면 둘 다 낡습니다.**

실제로 그렇게 됐던 파일이 `archive/docs/2024-12_DOCS_INDEX.md` 입니다. 20개월
동안 살아 있는 문서 행세를 했고, 안에는 CLAUDE.md 가 적지 말라고 한 값이
가득했습니다 — *"총 문서 6개"*, *"5,800+ 줄"*, *"커버리지 90%"*.

## 왜 사람의 검토로는 부족한가

`#103` 의 완료 기준 셋 중 하나가 **"포인터에는 숫자를 적지 않습니다"** 였습니다.
그것을 무엇도 감시하지 않으면 다음에 한 줄 덧붙이는 사람이 *"현재 문서 32개"*
를 적어도 아무 일이 일어나지 않습니다. **판정 기준을 적어 두는 것과 판정하는
것은 다릅니다.**

HTML 주석은 검사 대상에서 뺍니다 — 렌더링되지 않고, 유지보수자에게 주는
지시라서 `#103` 같은 참조가 들어갑니다.
"""

from __future__ import annotations

import pathlib
import re

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS_README = REPO_ROOT / "docs" / "README.md"
DOCS_INDEX = REPO_ROOT / "docs" / "INDEX.md"
ARCHIVED = REPO_ROOT / "archive" / "docs" / "2024-12_DOCS_INDEX.md"

#: 렌더링되는 부분만 남깁니다.
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


@pytest.fixture(scope="module")
def rendered() -> str:
    return _COMMENT.sub("", DOCS_README.read_text(encoding="utf-8")).strip()


def test_it_points_at_the_index(rendered: str) -> None:
    """포인터가 실제로 가리키는지 봅니다."""
    assert "INDEX.md" in rendered, "docs/README.md 가 INDEX.md 를 가리키지 않습니다"
    assert DOCS_INDEX.exists(), f"가리키는 대상이 없습니다: {DOCS_INDEX}"


def test_it_writes_no_numbers(rendered: str) -> None:
    """#103 의 완료 기준 — **포인터에는 숫자를 적지 않습니다.**

    문서 개수·줄 수·커버리지·버전은 적는 순간 낡습니다(CLAUDE.md). 포인터에
    필요한 숫자는 없으므로 전부 금지해도 잃는 것이 없습니다.
    """
    digits = [line.strip() for line in rendered.splitlines() if re.search(r"\d", line)]

    assert not digits, "포인터에 숫자를 적었습니다. 값은 코드나 INDEX 에서 뽑으세요:\n  " + "\n  ".join(digits)


def test_it_stays_a_pointer_not_a_second_index(rendered: str) -> None:
    """목록으로 자라는 것을 막습니다.

    표가 생기거나 링크가 여럿이 되는 순간 두 번째 인덱스입니다. 옛 파일은
    440줄이었습니다.
    """
    links = re.findall(r"\[[^\]]+\]\([^)]+\)", rendered)

    assert len(links) <= 2, f"링크가 {len(links)}개입니다. 목록이 되어 가고 있습니까?\n  {links}"
    assert "|" not in rendered, "표가 생겼습니다. 목록은 INDEX.md 가 답니다"
    assert len(rendered.splitlines()) <= 10, f"{len(rendered.splitlines())}줄입니다. 포인터는 몇 줄이면 됩니다"


def test_the_old_index_is_archived_with_a_notice() -> None:
    """옮긴 원본이 `archive/README.md` 의 규칙대로 있는지 봅니다.

    > 2. **맨 위에 동결 안내를 답니다.** 왜 보관됐는지, 언제 것인지, 지금은
    >    무엇을 봐야 하는지 한 문단이면 충분합니다.
    """
    assert ARCHIVED.exists(), f"옮긴 원본이 없습니다: {ARCHIVED}"

    head = ARCHIVED.read_text(encoding="utf-8").lstrip().splitlines()[0]

    assert head.startswith("> "), f"동결 안내가 맨 위에 없습니다: {head!r}"
    assert "동결" in head, f"동결 안내로 시작하지 않습니다: {head!r}"


def test_the_index_does_not_list_the_pointer() -> None:
    """INDEX 가 포인터를 문서로 세지 않는지 봅니다.

    옛 `docs/README.md` 는 INDEX 의 "그 밖에" 표에 *`docs/` 자체 소개* 로
    올라 있었습니다. 포인터는 문서가 아니라 이정표이므로 목록에 넣으면
    다시 "여기에도 뭔가 적어야 할 것 같은" 자리가 됩니다.
    """
    index = DOCS_INDEX.read_text(encoding="utf-8")

    assert "](README.md)" not in index, "INDEX 가 포인터를 목록에 올려 두고 있습니다"


def test_the_checker_actually_reads_the_file(rendered: str) -> None:
    """빈 문자열을 검사하고 있지 않은지 봅니다.

    경로가 틀리면 위 검사들이 전부 조용히 통과합니다 — 숫자도 없고 링크도
    없고 표도 없기 때문입니다. **가장 위험한 통과가 이것입니다.**
    """
    assert DOCS_README.exists(), f"docs/README.md 가 없습니다: {DOCS_README}"
    assert rendered, "렌더링되는 내용이 비었습니다. GitHub 이 빈 화면을 보여 줍니다"
