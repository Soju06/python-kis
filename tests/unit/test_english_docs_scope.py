"""영문 문서가 다시 갈라지지 않게 합니다. (이슈 #104)

## 무엇을 정했나

`docs/user/en/` 을 **README 한 장**으로 줄였습니다. 번역본 3개가 한국어 원본을
못 따라와 **틀린 안내**를 하고 있었기 때문입니다.

- 옛 영문 `QUICKSTART` 는 `#87`("모의 계좌도 실전 앱이 필요하다")이 없어, 그대로
  따라간 사용자가 `create_client()` 에서 막혔습니다
- 옛 영문 `FAQ` 는 `#70` 이 없앤 `virtual`/`sandbox` 를 가르쳤습니다

**아무도 갱신하지 않는 번역은 번역이 없는 것보다 나쁩니다.** 읽는 사람이 낡은
것을 알 방법이 없기 때문입니다.

## 왜 검사가 필요한가

`docs/guidelines/MULTILINGUAL_SUPPORT.md` 가 356줄로 번역 유지 절차를 적어
두었는데도 위 드리프트가 났습니다. **정책 문서는 검사가 아닙니다.**

영문을 다시 늘리는 것 자체는 막지 않습니다 — `#104` 가 **단계별 범위**를 적어
두었습니다. **조건은 없습니다. 옮길지는 그때 판단합니다.** 이 검사가 막는 것은
**아무도 모르게 늘어나는 것**입니다. 파일을 추가하면 여기가 빨개지고, 그때
`#104` 의 단계를 다시 읽게 됩니다.
"""

from __future__ import annotations

import pathlib
import re

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
EN = REPO_ROOT / "docs" / "user" / "en"

#: 이 디렉터리에서 유지하기로 한 것. 늘리려면 `#104` 의 단계 범위를 먼저 보세요.
KEPT = {"README.md"}


@pytest.fixture(scope="module")
def page() -> str:
    return (EN / "README.md").read_text(encoding="utf-8")


def test_the_english_branch_stays_closed() -> None:
    """`docs/user/en/` 이 조용히 다시 늘어나는 것을 막습니다."""
    found = {p.name for p in EN.iterdir() if p.is_file()}
    extra = sorted(found - KEPT)

    assert not extra, (
        "영문 문서가 늘었습니다. #104 가 단계별 범위를 적어 뒀습니다 — "
        f"단계를 옮기기로 정했으면 이 목록(KEPT)에 넣고 근거를 남기세요:\n  {extra}"
    )
    assert KEPT <= found, f"유지하기로 한 것이 사라졌습니다: {sorted(KEPT - found)}"


def test_every_link_on_the_page_resolves(page: str) -> None:
    """한 장뿐이므로 그 한 장은 죽은 링크가 없어야 합니다.

    옛 `en/README.md` 는 `./CONFIGURATION.md`(없는 파일)와
    `../ko/README.md`(존재한 적 없는 디렉터리)를 가리키고 있었습니다.
    """
    dead = [
        f"{label} -> {target}"
        for label, target in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", page)
        if not target.startswith(("http", "#")) and not (EN / target.split("#")[0]).exists()
    ]

    assert not dead, "영문 페이지에 죽은 링크가 있습니다:\n  " + "\n  ".join(dead)


def test_it_carries_the_requirement_that_broke_the_old_translation(page: str) -> None:
    """`#87` 의 실전 앱 요건이 영문에 있는지 봅니다.

    `#104` 의 완료 기준 중 **선택과 무관하게 필요한** 항목입니다. 옛 영문
    QUICKSTART 가 이것을 빠뜨려 사용자가 `create_client()` 에서 막혔습니다.
    영문이 한 장으로 줄었으므로 그 한 장이 이것을 져야 합니다.
    """
    paragraph = next((b for b in page.split("\n\n") if "live app" in b.lower()), "")

    assert paragraph, "실전 앱 요건(#87)이 영문 페이지에 없습니다"

    # `"live app"` 만 보면 안 됩니다. 뒤쪽 설명 문장("uses the live app key")에도
    # 그 말이 나오므로, **요건 문장을 통째로 지워도 통과**합니다. 처음 이 검사를
    # 그렇게 썼고 되돌리기 확인에서 초록이 나와 잡았습니다.
    missing = [word for word in ("required", "paper", "create_client") if word not in paragraph.lower()]

    assert not missing, (
        f"실전 앱 요건이 요건으로 읽히지 않습니다. 빠진 것: {missing}\n해당 문단: {paragraph.strip()[:200]}"
    )


def test_it_writes_no_hand_kept_numbers(page: str) -> None:
    """손으로 적은 값을 막습니다.

    옛 `en/README.md` 는 `badge/coverage-92%25` 를 박아 두고 있었습니다.
    CLAUDE.md 가 금지한 것이고, 배지가 아니어도 같은 문제입니다.
    """
    banned = [
        line.strip()
        for line in page.splitlines()
        if re.search(r"badge/(coverage|version|license)-", line) or re.search(r"\b\d+(\.\d+)?%", line)
    ]

    assert not banned, "손으로 적은 값이 있습니다. 값은 코드나 PyPI 에서 뽑으세요:\n  " + "\n  ".join(banned)


def test_the_checker_actually_reads_the_directory(page: str) -> None:
    """빈 디렉터리·빈 파일을 검사하고 있지 않은지 봅니다.

    `EN` 경로가 틀리면 위 검사들이 조용히 통과합니다 — 늘어난 파일도 없고
    죽은 링크도 없기 때문입니다.
    """
    assert EN.is_dir(), f"영문 문서 디렉터리가 없습니다: {EN}"
    assert len(page) > 500, f"영문 페이지가 {len(page)}자뿐입니다. 경로가 맞습니까?"
