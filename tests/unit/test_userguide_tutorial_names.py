"""USER_GUIDE·FAQ 가 Tutorial 과 다른 이름을 가르치지 않는지 봅니다. (#139)"""

from __future__ import annotations

import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
GUIDES = (
    REPO_ROOT / "docs" / "user" / "USER_GUIDE.md",
    REPO_ROOT / "docs" / "FAQ.md",
)

_STALE_PLAIN = (
    "sellable()",
    "daily_executions",
    "is_market_open",
    "is_open_now",
    ").trading_hours()",
    "trading_hours()",
)
_PROFIT = re.compile(r"\.profit\(")


def _stale_hits(text: str) -> list[str]:
    hits = [needle for needle in _STALE_PLAIN if needle in text]
    if _PROFIT.search(text):
        hits.append(".profit(")
    return hits


def test_living_guides_use_tutorial_names() -> None:
    hits: list[str] = []
    for path in GUIDES:
        found = _stale_hits(path.read_text(encoding="utf-8"))
        if found:
            hits.append(f"{path.relative_to(REPO_ROOT)}: {found}")

    assert not hits, "살아 있는 가이드가 Tutorial 과 다른 이름을 가르칩니다:\n  " + "\n  ".join(hits)


def test_guides_call_the_real_names() -> None:
    user_guide = (REPO_ROOT / "docs" / "user" / "USER_GUIDE.md").read_text(encoding="utf-8")
    faq = (REPO_ROOT / "docs" / "FAQ.md").read_text(encoding="utf-8")

    assert "account.profits(" in user_guide
    assert "account.daily_orders(" in user_guide
    assert "stock.orderable" in user_guide
    assert 'kis.trading_hours("KR")' in user_guide
    assert 'kis.trading_hours("KR")' in faq


def test_stale_guide_names_are_caught() -> None:
    stale = (
        "sellable = stock.sellable()\n"
        "account.profit(start_date=date(2024, 1, 1))\n"
        "account.daily_executions(date=date(2024, 12, 10))\n"
        'hours = kis.stock("005930").trading_hours()\n'
        "print(hours.is_open_now)\n"
        "print(hours.is_market_open)\n"
        "kis.trading_hours()\n"
    )

    assert set(_stale_hits(stale)) == set(_STALE_PLAIN) | {".profit("}
