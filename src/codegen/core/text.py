from __future__ import annotations

_NULL_DESCRIPTION_PHRASES = ('""', "null 값 설정", "null값 설정")


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
    if '""' in desc:
        return True
    if "null" in lowered and "설정" in desc:
        return True
    return any(phrase in desc for phrase in _NULL_DESCRIPTION_PHRASES)


__all__ = ["is_demo_unavailable", "is_forced_null_description"]
