from __future__ import annotations

import unicodedata

_NULL_DESCRIPTION_PHRASES = ("null 값 설정", "null값 설정")
_BLANK_FORBIDDEN_PHRASES = (
    "공백 불가",
    "공란 불가",
    "공백불가",
    "공란불가",
    "공란으로 비우지 않음",
    "공백으로 비우지 않음",
)


def is_blank_description(description: str | None) -> bool:
    if not description:
        return False
    desc = description.strip()
    if not desc:
        return False
    if any(phrase in desc for phrase in _BLANK_FORBIDDEN_PHRASES):
        return False
    lowered = desc.lower()
    if "blank" in lowered:
        return True
    if '""' in desc:
        return True
    if "공백" in desc or "공란" in desc:
        return True
    return False


def is_demo_unavailable(value: str | None) -> bool:
    if not value:
        return False
    text = value.strip()
    if not text:
        return False
    if text in {"미지원", "미지", "제공 안함", "제공안함"}:
        return True
    if "모의투자" in text and ("미지원" in text or "불가" in text or "미제공" in text):
        return True
    return "모의투자 미지원" in text


def is_forced_null_description(description: str | None) -> bool:
    if not description:
        return False
    desc = description.strip()
    if not desc:
        return False
    lowered = desc.lower()
    if "null" in lowered and "설정" in desc:
        return True
    return any(phrase in desc for phrase in _NULL_DESCRIPTION_PHRASES)


def _display_width(text: str) -> int:
    width = 0
    for ch in text:
        width += 2 if unicodedata.east_asian_width(ch) in {"F", "W"} else 1
    return width


def _split_long_word(word: str, width: int) -> list[str]:
    if width <= 0:
        return [word]
    parts: list[str] = []
    current = []
    current_width = 0
    for ch in word:
        ch_width = 2 if unicodedata.east_asian_width(ch) in {"F", "W"} else 1
        if current and current_width + ch_width > width:
            parts.append("".join(current))
            current = [ch]
            current_width = ch_width
            continue
        current.append(ch)
        current_width += ch_width
        if current_width >= width:
            parts.append("".join(current))
            current = []
            current_width = 0
    if current:
        parts.append("".join(current))
    return parts or [word]


def wrap_display_lines(value: str, width: int = 100) -> list[str]:
    if not value:
        return [value]
    lines = value.splitlines() or [value]
    wrapped_lines: list[str] = []
    for line in lines:
        if not line.strip():
            wrapped_lines.append("")
            continue
        prefix_len = len(line) - len(line.lstrip())
        prefix = line[:prefix_len]
        content = line.strip()
        max_width = max(1, width - _display_width(prefix))
        words = content.split()
        if not words:
            wrapped_lines.append(prefix)
            continue
        current = ""
        for word in words:
            if not current:
                if _display_width(word) <= max_width:
                    current = word
                    continue
                for part in _split_long_word(word, max_width):
                    wrapped_lines.append(f"{prefix}{part}")
                current = ""
                continue
            candidate = f"{current} {word}"
            if _display_width(candidate) <= max_width:
                current = candidate
                continue
            wrapped_lines.append(f"{prefix}{current}")
            if _display_width(word) <= max_width:
                current = word
                continue
            for part in _split_long_word(word, max_width):
                wrapped_lines.append(f"{prefix}{part}")
            current = ""
        if current:
            wrapped_lines.append(f"{prefix}{current}")
    return wrapped_lines


def wrap_display_text(value: str, width: int = 100) -> str:
    return "\n".join(wrap_display_lines(value, width=width))


__all__ = [
    "is_blank_description",
    "is_demo_unavailable",
    "is_forced_null_description",
    "wrap_display_lines",
    "wrap_display_text",
]
