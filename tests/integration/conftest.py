"""`tests/integration/` 아래 모든 테스트에 `integration` 마커를 자동으로 붙인다.

`tests/performance/conftest.py` 와 같은 방식이고, 같은 이유다. 그쪽은 30개 중
8개만 마커를 갖고 있었다. 여기도 이미 어긋나 있었다.

    tests/integration  전체 29개 수집 / integration 마커 9개

29개 중 20개가 마커 없이 이 디렉터리에 있었다. 이슈 #41 이 네트워크 테스트
2파일(17개)을 여기로 옮기면서 마커 없는 파일이 더 늘어날 참이었다.

디렉터리와 마커가 서로 다른 말을 하면 어느 쪽을 믿어야 할지 알 수 없다.
디렉터리 규칙으로 두면 새 파일이 마커 없이 추가돼도 같은 일이 반복되지 않는다.

**게이팅은 바뀌지 않는다.** CI 의 게이팅 잡은 `-m 'not requires_api and not
performance'` 라 `integration` 을 제외하지 않는다. 이 마커는 사람이 고르기
위한 것이지 머지를 막는 장치가 아니다.
"""

from pathlib import Path

import pytest

_HERE = Path(__file__).parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    # 주의: 하위 디렉터리의 conftest 라도 이 훅은 **수집된 전체 목록**을 받는다.
    # 경로로 거르지 않으면 저장소의 모든 테스트가 integration 으로 표시된다.
    for item in items:
        if _HERE in item.path.parents:
            item.add_marker(pytest.mark.integration)
