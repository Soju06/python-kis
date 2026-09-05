import os

import pytest

pytestmark = pytest.mark.performance


@pytest.mark.skipif(os.environ.get("RUN_PERF") != "1", reason="Set RUN_PERF=1 to run performance tests")
def test_math_speed_baseline(benchmark):
    def compute():
        s = 0
        for i in range(10000):
            s += (i * i) % 97
        return s

    res = benchmark(compute)
    assert res >= 0
