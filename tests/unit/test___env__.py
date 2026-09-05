import importlib
import sys
from importlib.metadata import PackageNotFoundError
from unittest.mock import patch

import pytest

from vmkis.__env__ import (
    APPKEY_LENGTH,
    LIVE_API_REQUEST_PER_SECOND,
    LIVE_DOMAIN,
    PAPER_API_REQUEST_PER_SECOND,
    PAPER_DOMAIN,
    SECRETKEY_LENGTH,
    USER_AGENT,
    WEBSOCKET_LIVE_DOMAIN,
    WEBSOCKET_MAX_SUBSCRIPTIONS,
    WEBSOCKET_PAPER_DOMAIN,
    __author__,
    __author_email__,
    __authors__,
    __license__,
    __maintainers__,
    __package_name__,
    __upstream_author__,
    __upstream_url__,
    __url__,
    __version__,
)


def test_sys_version_info():
    """Python 버전에 따른 RuntimeError 발생을 테스트합니다."""
    # Python 3.10 미만일 경우 RuntimeError 발생
    with patch.object(sys, "version_info", (3, 9, 0)):
        with pytest.raises(RuntimeError, match="VmKis에는 Python 3.10 이상이 필요합니다."):
            importlib.reload(sys.modules["vmkis.__env__"])

    # Python 3.10 이상일 경우 정상 실행
    with patch.object(sys, "version_info", (3, 10, 0)):
        importlib.reload(sys.modules["vmkis.__env__"])


def test_version_placeholder():
    assert __version__ != "{{VERSION_PLACEHOLDER}}"


def test_constants_and_metadata():
    """__env__.py의 상수와 메타데이터를 테스트합니다."""
    assert APPKEY_LENGTH == 36
    assert SECRETKEY_LENGTH == 180
    assert LIVE_DOMAIN == "https://openapi.koreainvestment.com:9443"
    assert PAPER_DOMAIN == "https://openapivts.koreainvestment.com:29443"
    assert WEBSOCKET_LIVE_DOMAIN == "ws://ops.koreainvestment.com:21000"
    assert WEBSOCKET_PAPER_DOMAIN == "ws://ops.koreainvestment.com:31000"
    assert WEBSOCKET_MAX_SUBSCRIPTIONS == 40
    assert LIVE_API_REQUEST_PER_SECOND == 19
    assert PAPER_API_REQUEST_PER_SECOND == 2

    assert USER_AGENT == f"VmKis/{__version__}"

    assert __license__ == "MIT"
    assert __version__ is not None
    assert len(__version__) > 0

    # 저자와 원저자는 구분되어야 한다.
    # 이 프로젝트는 Soju06/python-kis 의 포크이며, 배포판을 내는 주체는 포크
    # 관리자다. 예전에는 __author__ 가 업스트림 저자로 하드코딩되어 있어
    # pyproject.toml 과 어긋나 있었다.
    assert __author__ == "visualmoney"
    assert __author_email__ == "visualmoney2@gmail.com"
    assert __upstream_author__ == "Soju06"
    assert __author__ != __upstream_author__

    # 원저자 크레딧은 저자 목록과 URL 양쪽에 남아 있어야 한다.
    assert ("Soju06", "qlskssk@gmail.com") in __authors__
    assert __upstream_url__ == "https://github.com/Soju06/python-kis"
    assert __url__ == "https://github.com/visualmoney/vm-stock-kis"


# ---------------------------------------------------------------------------
# 저자 정보는 배포 메타데이터에서 파생됩니다.
#
# 예전에는 __env__.py 에 하드코딩되어 있었고, 포크 이후에도 업스트림 저자만 담고
# 있어 pyproject.toml(두 저자 + visualmoney 관리자)과 어긋난 상태였습니다.
# 아래 테스트들은 두 곳이 다시 갈라지면 실패합니다.
# ---------------------------------------------------------------------------


def test_authors_match_distribution_metadata():
    """__authors__ 는 pyproject.toml 의 [project] authors 를 그대로 반영한다"""
    from email.utils import getaddresses
    from importlib.metadata import metadata

    expected = getaddresses([metadata(__package_name__).get("Author-email") or ""])

    assert __authors__ == expected
    assert len(__authors__) >= 1


def test_maintainers_match_distribution_metadata():
    from email.utils import getaddresses
    from importlib.metadata import metadata

    expected = getaddresses([metadata(__package_name__).get("Maintainer-email") or ""])

    assert __maintainers__ == expected


def test_author_is_the_primary_maintainer():
    """__author__ 는 관리자가 있으면 관리자, 없으면 첫 저자다"""
    primary = (__maintainers__ or __authors__)[0]

    assert (__author__, __author_email__) == primary


def test_author_is_not_hardcoded_upstream():
    """포크 이후 __author__ 가 업스트림 저자로 남아 있으면 안 된다"""
    assert __author__ != __upstream_author__


def test_upstream_credit_is_kept():
    """업스트림 크레딧은 별도 필드로 보존한다"""
    assert __upstream_author__ == "Soju06"
    assert __upstream_url__ == "https://github.com/Soju06/python-kis"
    assert __url__ != __upstream_url__
    # 업스트림 저자는 여전히 저자 목록에 남아 있어야 한다.
    assert any(name == __upstream_author__ for name, _ in __authors__)


def test_upstream_url_matches_project_urls():
    """__upstream_url__ 은 pyproject.toml 의 [project.urls] "Original Project" 와 같아야 한다.

    PEP 621 에는 "원저자"를 담을 표준 필드가 없다. 그래서 원저자 정보는
    __env__.py 의 상수와 [project.urls] 두 곳에 나뉘어 있다. 이 테스트가
    둘이 갈라지는 것을 막는다.
    """
    from importlib.metadata import metadata

    urls = dict(line.split(", ", 1) for line in metadata(__package_name__).get_all("Project-URL") or [])

    assert urls["Original Project"] == __upstream_url__
    assert urls["Repository"] == __url__


def test_falls_back_when_distribution_is_missing():
    """설치되지 않은 소스 트리에서도 import가 실패하지 않는다"""
    import importlib.metadata

    module = sys.modules["vmkis.__env__"]

    try:
        with (
            patch.object(importlib.metadata, "metadata", side_effect=PackageNotFoundError),
            patch.object(importlib.metadata, "version", side_effect=PackageNotFoundError),
        ):
            reloaded = importlib.reload(module)

            assert reloaded.__version__ == "0.0.0+unknown"
            assert reloaded.__authors__ == []
            assert reloaded.__maintainers__ == []
            assert reloaded.__author__ == ""
            assert reloaded.__author_email__ == ""
            # 업스트림 크레딧은 메타데이터와 무관하므로 그대로 남는다.
            assert reloaded.__upstream_author__ == "Soju06"
    finally:
        importlib.reload(module)
