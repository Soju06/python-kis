"""Tutorial 목차의 빈 칸이 examples/ 에 있는지 봅니다. (#140)"""

from __future__ import annotations

import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
EXAMPLES = REPO_ROOT / "examples"

_REQUIRED: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("keep_token", re.compile(r"keep_token\s*=")),
    ("stock.chart", re.compile(r"\.chart\(")),
    ("stock.orderbook", re.compile(r"\.orderbook\(")),
    ("kis.trading_hours", re.compile(r"\.trading_hours\(")),
    ("account.profits", re.compile(r"\.profits\(")),
    ("account.daily_orders", re.compile(r"\.daily_orders\(")),
    ("orderable_amount", re.compile(r"\.orderable_amount\(")),
    ("stock.orderable", re.compile(r"stock\.orderable\b(?!_)")),
    ("pending_orders", re.compile(r"\.pending_orders\(")),
    ("stock.sell", re.compile(r"\.sell\(")),
    ("order.modify", re.compile(r"\.modify\(")),
    ("order.cancel", re.compile(r"\.cancel\(")),
    ("on orderbook", re.compile(r'\.on\(\s*["\']orderbook["\']')),
    ("on execution", re.compile(r'\.on\(\s*["\']execution["\']')),
)


def _example_python() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(EXAMPLES.rglob("*.py")) if "__pycache__" not in path.parts
    )


def test_examples_call_tutorial_names() -> None:
    corpus = _example_python()
    missing = [label for label, pattern in _REQUIRED if not pattern.search(corpus)]

    assert not missing, "Tutorial 목차 이름이 examples/ 에 없습니다:\n  " + "\n  ".join(missing)


def test_order_examples_keep_the_live_guard() -> None:
    for name in ("place_sell.py", "modify_cancel_order.py"):
        text = (EXAMPLES / "01_basic" / name).read_text(encoding="utf-8")
        assert "ALLOW_LIVE_TRADES" in text, f"{name} 에 실계좌 가드가 없습니다"


def test_missing_chart_call_is_caught() -> None:
    assert not _REQUIRED[1][1].search("stock.quote()\n")
    assert _REQUIRED[1][1].search("stock.chart('7d')\n")
