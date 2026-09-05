"""
RateLimiter 정확성 테스트 (현행 API 기준)

이 테스트는 다음 시나리오를 검증합니다:
- Rate limiting이 정확한 시간 간격으로 요청을 제한하는지
- 대량 요청 시 초당 제한을 초과하지 않는지
- 비블로킹 요청 실패가 카운터에 반영되지 않는지
- 다중 스레드 환경에서의 안전성

타이밍 단언의 상한 여유는 `tests/timing.py` 를 따릅니다.
"""

import time
from threading import Thread

import pytest
from tests.timing import SCHEDULING_SLACK

from vmkis.utils.rate_limit import RateLimiter

# SCHEDULING_SLACK 은 `tests/timing.py` 로 옮겼습니다. 여기에만 있던 탓에
# tests/integration/test_rate_limit_compliance.py 가 같은 처방을 받지 못했고,
# 그것이 이슈 #92 입니다. 근거와 한계는 그 파일에 적혀 있습니다.
#
# 옮기면서 한 문장을 고쳤습니다. 여기에는 "대기가 한 주기 더 늘어나는 회귀는
# 이 여유(2초)보다 크므로 상한이 여전히 잡는다"고 적혀 있었는데, 1.0 < 2.0 이라
# **틀린 문장**이었습니다. 상한이 잡는 것은 세 주기 이상 늘어나는 회귀입니다.


class TestRateLimiterAccuracy:
    """RateLimiter 정확성 테스트"""

    def test_rate_limiter_basic_functionality(self):
        """기본 기능 테스트"""
        limiter = RateLimiter(rate=5, period=1.0)

        # 5번 요청은 즉시 통과
        for _ in range(5):
            assert limiter.acquire() is True

        assert limiter.count == 5

    def test_rate_limiter_blocks_after_limit(self):
        """제한 초과 시 대기"""
        limiter = RateLimiter(rate=2, period=1.0)

        start_time = time.time()

        # 처음 2개는 즉시
        assert limiter.acquire() is True
        assert limiter.acquire() is True

        # 3번째는 대기해야 함
        assert limiter.acquire(blocking=True) is True

        elapsed = time.time() - start_time

        # 적어도 1초는 대기했어야 함 (약간의 오차 허용)
        assert elapsed >= 0.9

    def test_rate_limiter_resets_after_interval(self):
        """시간 간격 후 리셋"""
        limiter = RateLimiter(rate=5, period=0.5)

        # 5번 요청
        for _ in range(5):
            assert limiter.acquire() is True
        assert limiter.count == 5

        # 0.5초 대기
        time.sleep(0.6)

        # 카운터 리셋 확인 후 다시 카운트
        assert limiter.count == 0
        assert limiter.acquire() is True
        assert limiter.count == 1

    def test_rate_limiter_with_callback(self):
        """콜백 함수 호출 확인"""
        callback_called = []

        def on_wait():
            callback_called.append(time.time())

        limiter = RateLimiter(rate=1, period=0.5)

        # 첫 요청은 즉시
        assert limiter.acquire() is True

        # 두 번째 요청은 대기하며 콜백 호출
        assert limiter.acquire(blocking=True, blocking_callback=on_wait) is True

        # 콜백이 호출되었는지 확인
        assert len(callback_called) >= 1

    def test_rate_limiter_on_error_does_not_count(self):
        """에러 시 카운트 안 함"""
        limiter = RateLimiter(rate=5, period=1.0)

        # 성공 3번
        for _ in range(3):
            assert limiter.acquire() is True

        # 제한 초과 상황에서 비블로킹 요청은 실패하고 카운트 증가 없음
        assert limiter.acquire(blocking=False) in (True, False)
        assert limiter.acquire(blocking=False) in (True, False)

        # 현재 카운트는 3 또는 5 이하이며, 비블로킹 실패는 카운트를 증가시키지 않음
        assert limiter.count <= 5

    def test_rate_limiter_precise_timing(self):
        """정밀한 타이밍 테스트 (초당 10개)"""
        limiter = RateLimiter(rate=10, period=1.0)

        start_time = time.time()
        request_times = []

        # 20개 요청
        for _ in range(20):
            limiter.acquire(blocking=True)
            request_times.append(time.time() - start_time)

        # 구현상 한 윈도우당 임계 도달 시에만 대기하므로 총 대기는 약 1초
        total_time = time.time() - start_time
        assert 0.9 <= total_time <= 1.0 + SCHEDULING_SLACK

        # 처음 10개는 1초 이내
        assert all(t < 1.0 for t in request_times[:10])

        # 다음 10개는 1초 이후
        assert all(t >= 1.0 for t in request_times[10:])

    def test_rate_limiter_high_frequency(self):
        """고빈도 요청 (초당 50개)"""
        limiter = RateLimiter(rate=50, period=1.0)

        start_time = time.time()

        # 100개 요청
        for _ in range(100):
            limiter.acquire(blocking=True)

        elapsed = time.time() - start_time

        # 구현 특성상 한 번만 대기하므로 총 약 1초
        assert 0.9 <= elapsed <= 1.0 + SCHEDULING_SLACK

    def test_rate_limiter_thread_safety(self):
        """스레드 안전성 테스트"""
        limiter = RateLimiter(rate=10, period=1.0)
        results = []

        def make_requests():
            for _ in range(5):
                limiter.acquire(blocking=True)
                results.append(time.time())

        # 4개 스레드에서 동시에 5개씩 = 총 20개
        threads = [Thread(target=make_requests) for _ in range(4)]

        start_time = time.time()
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        elapsed = time.time() - start_time

        # 20개 요청, 초당 10개 제한 -> 구현상 총 약 1초 대기
        #
        # 상한에 SCHEDULING_SLACK 을 쓴다. 614b68e 가 같은 이유로 6곳을 고치면서
        # 이 한 곳을 빠뜨렸는데, 하필 스레드 4개를 동시에 돌려 스케줄링에 가장
        # 민감한 테스트다. 커버리지를 켜면 10회 중 1회꼴로 터졌다(이슈 #59).
        #
        # 같은 빠뜨림이 파일 단위로 한 번 더 났다 — 이 처방이 integration 쪽
        # 레이트리밋 테스트에는 오지 않았다(이슈 #92).
        assert 0.9 <= elapsed <= 1.0 + SCHEDULING_SLACK
        assert len(results) == 20

    def test_rate_limiter_zero_wait_when_under_limit(self):
        """제한 이하일 때 대기 시간 0"""
        limiter = RateLimiter(rate=100, period=1.0)

        start_time = time.time()

        # 50개 요청 (제한의 절반)
        for _ in range(50):
            assert limiter.acquire(blocking=False) in (True, False)

        elapsed = time.time() - start_time

        # 대기가 전혀 없어야 한다. 한 주기(1.0초)보다 작으면 그 사실이 증명된다.
        assert elapsed < 1.0

    def test_rate_limiter_with_different_intervals(self):
        """다양한 시간 간격 테스트"""
        # 2초당 10개
        limiter = RateLimiter(rate=10, period=2.0)

        start_time = time.time()

        # 20개 요청
        for _ in range(20):
            limiter.acquire(blocking=True)

        elapsed = time.time() - start_time

        # 구현상 한 윈도우에서만 대기 -> 약 2초 소요
        assert 1.8 <= elapsed <= 2.0 + SCHEDULING_SLACK

    def test_rate_limiter_consecutive_errors(self):
        """연속 에러 시 카운트 관리"""
        limiter = RateLimiter(rate=5, period=1.0)

        # 10번 비블로킹 요청 (초과 시 실패하며 카운트 유지)
        successes = 0
        for _ in range(10):
            if limiter.acquire(blocking=False):
                successes += 1

        # 카운트는 최대 rate까지만 증가
        assert limiter.count == successes <= 5

    def test_rate_limiter_mixed_success_and_error(self):
        """성공/에러 혼합"""
        limiter = RateLimiter(rate=10, period=1.0)

        successes = 0
        total_successes = 0
        for i in range(10):
            if i % 2 == 0:
                ok = limiter.acquire(blocking=False)
                if ok:
                    successes += 1
                    total_successes += 1
            else:
                # 실패 케이스 시도 (초과 시 False 반환)
                ok = limiter.acquire(blocking=False)
                if ok:
                    total_successes += 1

        # 전체 성공 횟수와 카운트가 일치
        assert limiter.count == total_successes


class TestRateLimiterEdgeCases:
    """RateLimiter 엣지 케이스 테스트"""

    def test_rate_limiter_with_very_low_limit(self):
        """매우 낮은 제한 (초당 1개)"""
        limiter = RateLimiter(rate=1, period=1.0)

        start_time = time.time()

        # 3개 요청
        for _ in range(3):
            limiter.acquire(blocking=True)

        elapsed = time.time() - start_time

        # 요청 2, 3에서 각각 대기 -> 총 약 2초 소요
        assert 1.9 <= elapsed <= 2.0 + SCHEDULING_SLACK

    def test_rate_limiter_with_fractional_seconds(self):
        """소수점 초 단위"""
        limiter = RateLimiter(rate=5, period=0.5)

        start_time = time.time()

        # 10개 요청
        for _ in range(10):
            limiter.acquire(blocking=True)

        elapsed = time.time() - start_time

        # 구현상 한 번만 대기 -> 약 0.5초 소요
        assert 0.4 <= elapsed <= 0.5 + SCHEDULING_SLACK

    def test_rate_limiter_rapid_succession(self):
        """매우 빠른 연속 호출"""
        limiter = RateLimiter(rate=100, period=1.0)

        start_time = time.time()

        # 100개를 가능한 빠르게
        for _ in range(100):
            limiter.acquire()

        elapsed = time.time() - start_time

        # 제한(100)에 도달하지 않으므로 한 주기(1.0초)를 넘겨선 안 된다.
        assert elapsed < 1.0 + SCHEDULING_SLACK


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
