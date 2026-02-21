from __future__ import annotations

from codegen.core.text import is_blank_description, is_forced_null_description


def test_blank_description_accepts_quotes_and_korean() -> None:
    assert is_blank_description('""(공란) 입력') is True
    assert is_blank_description("공백으로 입력") is True
    assert is_blank_description("공란(Default)") is True
    assert is_blank_description('"" 공백으로 입력') is True


def test_blank_description_rejects_forbidden_phrases() -> None:
    assert is_blank_description("공백 불가") is False
    assert is_blank_description("공란으로 비우지 않음") is False


def test_forced_null_description_ignores_blank_quotes() -> None:
    assert is_forced_null_description('""(공란) 입력') is False
    assert is_forced_null_description("null 값 설정") is True
    assert is_forced_null_description("null값 설정") is True
