"""CI 끝단이 분류기 최신과 맞는지 봅니다. (#127)

정책 문서에 3.10~3.13 을 나열하면, CI 는 끝단만 도는데도 거짓말이 됩니다.
끝단은 `ci.yml` 과 분류기에서 읽고, 여기에 숫자를 박지 않습니다.
"""

from __future__ import annotations

import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
PYPROJECT = REPO_ROOT / "pyproject.toml"
CI = REPO_ROOT / ".github" / "workflows" / "ci.yml"
POLICY = REPO_ROOT / "docs" / "guidelines" / "API_STABILITY_POLICY.md"

_CLASSIFIER = re.compile(r'"Programming Language :: Python :: (3\.\d+)"')
_MATRIX = re.compile(r"python-version:\s*\[([^\]]+)\]")


def _classifier_series(text: str) -> list[str]:
    return _CLASSIFIER.findall(text)


def _ci_ends(text: str) -> list[str]:
    match = _MATRIX.search(text)
    if match is None:
        return []
    return re.findall(r"'(\d+\.\d+)'", match.group(1))


def _ends_match(pyproject: str, ci: str) -> bool:
    series = _classifier_series(pyproject)
    if not series:
        return False
    return _ci_ends(ci) == [series[0], series[-1]]


def test_ci_ends_match_requires_min_and_latest_classifier() -> None:
    pyproject = PYPROJECT.read_text(encoding="utf-8")
    ci = CI.read_text(encoding="utf-8")

    assert 'requires-python = ">=3.10"' in pyproject
    assert _ends_match(pyproject, ci), (
        f"CI 끝단이 분류기 최신과 다릅니다. 분류기={_classifier_series(pyproject)} CI={_ci_ends(ci)}"
    )


def test_policy_does_not_enumerate_middle_python_versions() -> None:
    text = POLICY.read_text(encoding="utf-8")

    assert "3.10 / 3.11 / 3.12 / 3.13" not in text
    assert "최대 지원" not in text
    assert "중간 버전을 여기 나열하지" in text


def test_stale_ci_upper_end_is_caught() -> None:
    """#127 이전의 3.13 끝단을 그대로 먹여 봅니다."""
    pyproject = PYPROJECT.read_text(encoding="utf-8")
    stale_ci = "        python-version: ['3.10', '3.13']\n"

    assert not _ends_match(pyproject, stale_ci), "검사기가 낡은 CI 끝단을 통과시킵니다"
