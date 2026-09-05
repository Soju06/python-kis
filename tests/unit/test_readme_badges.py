"""README 배지가 배포 메타데이터와 어긋나지 않는지 봅니다.

배지는 **깨져도 아무도 안 알려 줍니다.** 404 는 회색 이미지로 렌더링되고,
잘못된 값은 그냥 잘못된 값으로 렌더링됩니다. CI 는 README 를 보지 않습니다.

CLAUDE.md 가 정한 것과 같은 이유입니다.

> **손으로 적지 않는 것** — 이슈 목록, 테스트 통과 수, 커버리지, PyPI 버전 …
> **적는 순간 낡습니다.**

그래서 배지 안에 값을 적지 않습니다. 버전·지원 파이썬·라이선스는 shields.io 가
PyPI 에서 직접 읽습니다. 손으로 적은 것은 **패키지 이름 하나**뿐이고, 그것이
틀리면 배지 셋이 동시에 404 가 됩니다.

라이선스 배지를 처음에는 `badge/license-MIT-blue` 로 박으려 했습니다. 재 보니
`pypi/l/vm-stock-kis` 가 실제로 `license: MIT` 를 돌려주므로 그쪽을 씁니다 —
`pyproject.toml` 이 `license = "MIT"` 를 `License-Expression` 으로 내보내고
있기 때문입니다. **적을 값이 없으면 어긋날 일도 없습니다.**

네트워크를 쓰지 않습니다. URL 이 살아 있는지가 아니라 **저장소가 스스로 아는
사실과 맞는지**만 봅니다.
"""

from __future__ import annotations

import pathlib
from importlib.metadata import metadata

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
README = REPO_ROOT / "README.md"

#: 배포 메타데이터. `pyproject.toml` 을 직접 읽지 않는 이유는 `tomllib` 이
#: 3.11+ 이고 이 프로젝트가 3.10 을 지원하기 때문입니다. 게다가 배지가 읽는
#: 것은 **빌드된 메타데이터**이므로 이쪽이 대조 대상으로도 더 정확합니다.
DIST = metadata("vm-stock-kis")


@pytest.fixture(scope="module")
def readme() -> str:
    return README.read_text(encoding="utf-8")


def test_badges_use_the_real_package_name(readme: str) -> None:
    """배지 URL 이 실제 배포 이름을 가리키는지 봅니다.

    이름이 바뀌면 shields.io 가 404 를 회색 이미지로 돌려주고, README 는
    조용히 깨진 채로 남습니다. **손으로 적은 값이 이것 하나뿐**이라 여기만
    지키면 됩니다.
    """
    name = DIST["Name"]
    missing = [
        path
        for path in (
            f"img.shields.io/pypi/v/{name}",
            f"img.shields.io/pypi/pyversions/{name}",
            f"img.shields.io/pypi/l/{name}",
            f"pypi.org/project/{name}/",
        )
        if path not in readme
    ]

    assert not missing, f"배포 이름은 {name!r} 입니다. README 가 가리키지 않는 것:\n  " + "\n  ".join(missing)


def test_no_badge_hard_codes_a_value_pypi_already_knows(readme: str) -> None:
    """값을 박은 배지가 다시 생기지 않게 합니다.

    `img.shields.io/badge/...` 는 문자열을 URL 에 박는 형태입니다. 라이선스나
    버전을 그렇게 적으면 `pyproject.toml` 만 바뀐 날 배지가 **거짓말**을
    시작하고, 아무 검사도 걸리지 않습니다.
    """
    hard_coded = [
        line.strip()
        for line in readme.splitlines()
        if "img.shields.io/badge/" in line and any(k in line.lower() for k in ("license", "version", "python"))
    ]

    assert not hard_coded, (
        "PyPI 가 이미 아는 값을 배지에 박았습니다. pypi/v · pypi/pyversions · pypi/l 을 쓰세요:\n  "
        + "\n  ".join(hard_coded)
    )


def test_the_license_link_points_at_the_file_that_exists(readme: str) -> None:
    """라이선스 배지가 가리키는 파일이 실제로 있는지 봅니다.

    이 저장소의 파일명은 `LICENCE` 입니다 — `LICENSE` 가 아닙니다. 철자를
    틀리면 링크가 404 이고, 그것도 아무도 안 알려 줍니다.
    """
    declared = DIST.get_all("License-File") or []

    assert declared, "배포 메타데이터에 License-File 이 없습니다"

    for relative in declared:
        assert (REPO_ROOT / relative).exists(), f"메타데이터가 가리키는 {relative} 가 없습니다"
        assert f"](./{relative})" in readme, f"README 라이선스 배지가 ./{relative} 를 가리키지 않습니다"


def test_the_checker_actually_reads_the_readme(readme: str) -> None:
    """README 를 못 읽는 상태를 막습니다.

    경로가 틀리면 `readme` 가 빈 문자열이 되고 위 검사들이 전부 조용히
    통과합니다 — `in` 은 빈 문자열에 대해서도 예외를 내지 않습니다.
    """
    assert len(readme) > 1000, f"README 가 {len(readme)}자뿐입니다. 경로가 맞습니까? {README}"
    assert "actions/workflows/ci.yml/badge.svg" in readme, "CI 배지가 사라졌습니다"
