"""`tests/performance/` 아래 모든 테스트에 `performance` 마커를 자동으로 붙인다.

파일마다 손으로 붙이지 않는 이유가 있다. 실제로 그렇게 하다가 어긋났다.

    test_benchmark.py            마커 0개 / 테스트 7개
    test_memory.py               마커 0개 / 테스트 7개
    test_websocket_stress.py     마커 0개 / 테스트 8개
    test_performance_advanced.py 마커 3개 / 테스트 7개
    test_perf_dummy.py           마커 1개 / 테스트 1개

30개 중 8개만 마커를 갖고 있었다. 나머지 22개는 `tests/performance/` 에 있으면서도
CI의 게이팅 잡(`-m 'not requires_api'`)에 그대로 수집됐다.

그중 `test_benchmark.py` 는 `time.time()` 의 시계 해상도에 걸려 실행마다 무작위로
실패한다(이슈 #23). 측정 구간이 Windows 시계 눈금(~15.6ms)보다 빨리 끝나면 경과가
0.000s 로 찍히고 ops/s 가 0 이 된다. **기계가 빠를수록 실패한다.** CI가 초록이었던
것은 러너가 느렸기 때문이고, 러너 세대가 바뀌면 main 이 red 가 될 상태였다.

디렉터리 규칙으로 두면 새 파일이 마커 없이 추가돼도 같은 일이 반복되지 않는다.
"""

from pathlib import Path

import pytest

_HERE = Path(__file__).parent


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    # 주의: 하위 디렉터리의 conftest 라도 이 훅은 **수집된 전체 목록**을 받는다.
    # 경로로 거르지 않으면 저장소의 모든 테스트가 performance 로 표시되어
    # 게이팅 잡이 아무것도 실행하지 않게 된다.
    for item in items:
        if _HERE in item.path.parents:
            item.add_marker(pytest.mark.performance)
