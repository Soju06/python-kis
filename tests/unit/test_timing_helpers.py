"""`tests/timing.py` 자체를 검사합니다.

이 파일이 필요한 이유는 하나입니다. **여기 있는 것이 조용히 죽으면 레이트리밋
구간 단언 세 개가 전부 초록이 됩니다.** #92 를 고치면서 원래 `all(제너레이터)`
였던 단언을 `assert_band` 로 바꿨는데, 그 교체 자체가 그런 사고를 낼 수 있습니다.

되돌려 확인했습니다 — `out` 을 빈 리스트로 고정하면 3건이 빨개집니다
(`docs/dev_logs/2026-08-30_10_issue92_flake.md`).
"""

import pytest
from tests.timing import SCHEDULING_SLACK, assert_band


class TestAssertBand:
    def test_passes_when_every_value_is_inside(self):
        assert_band([1.0, 1.5, 2.0], lo=1.0, hi=2.0, label="구간")

    def test_catches_a_value_above_the_band(self):
        """검사기가 죽었는지를 본다. 이것이 통과하면 구간 단언 3개가 무의미하다."""
        with pytest.raises(AssertionError):
            assert_band([1.0, 9.9], lo=1.0, hi=2.0, label="구간")

    def test_catches_a_value_below_the_band(self):
        """하한이 유량 제한기의 성질이다. 아래로 새는 것을 반드시 잡아야 한다."""
        with pytest.raises(AssertionError):
            assert_band([0.01], lo=1.0, hi=2.0, label="구간")

    def test_message_names_every_offender_with_its_time(self):
        """`all(제너레이터)` 가 못 하던 것 — 번호와 실제 시각.

        #92 의 원래 실패 메시지는 `assert False` 한 줄이었고, 그래서 어느 요청이
        얼마나 늦었는지 알 방법이 없었다.
        """
        with pytest.raises(AssertionError) as caught:
            assert_band([1.0, 3.3, 1.5, 4.4], lo=1.0, hi=2.0, offset=10, label="11-20번째")

        message = str(caught.value)

        assert "11-20번째" in message
        assert "2/4건" in message
        # 잘라 낸 구간의 번호가 아니라 **원래 번호**로 찍혀야 한다.
        assert "11번=3.300s" in message
        assert "13번=4.400s" in message
        # 통과한 것은 범인 목록에 없어야 한다.
        assert "10번=" not in message
        assert "12번=" not in message


class TestSlackDoesNotCostTheCheck:
    """상한을 넓힌 대가를 못 박습니다.

    **여유를 키우는 수정은 검사를 지우는 가장 흔한 방법**입니다. 넓힌 뒤에도
    무엇을 여전히 잡는지를 여기 고정해 둡니다.
    """

    def test_absorbs_a_scheduler_stall_that_broke_the_old_bound(self):
        """#92 의 실패 형태 — 요청 하나가 스케줄러 때문에 늦는 것.

        실측(CPU 16배 과부하)에서 11-20번째의 최대가 1.062초였으므로, 옛 상한
        2.5 가 터지려면 **1.44초 지연**이 필요했다. 새 상한은 1.94초까지 견딘다.
        """
        stalled = [1.06] * 9 + [2.60]

        assert_band(stalled, lo=1.0, hi=1.0 + SCHEDULING_SLACK, offset=10, label="11-20번째")

        # 같은 값이 옛 상한에서는 빨갛다. 넓힌 것이 실제로 이 실패를 없앤다.
        with pytest.raises(AssertionError):
            assert_band(stalled, lo=1.0, hi=2.5, offset=10, label="11-20번째")

    def test_still_catches_a_rate_limit_that_stopped_working(self):
        """넓힌 상한이 사 오지 **않은** 것.

        유량 제한이 통째로 사라지면 값이 0 근처로 내려앉는다. 그것은 상한이
        아니라 하한이 잡고, 하한은 건드리지 않았다. 과소 대기는 API 차단을
        부르므로 이쪽이 이 테스트가 지키는 성질이다.
        """
        no_throttle = [0.001 * i for i in range(10)]

        with pytest.raises(AssertionError):
            assert_band(no_throttle, lo=1.0, hi=1.0 + SCHEDULING_SLACK, offset=10, label="11-20번째")

    def test_slack_is_wider_than_one_period(self):
        """이 여유가 무엇을 못 잡는지를 코드로 남깁니다.

        2.0 > 1.0 이므로 **과대 대기 한 주기는 상한이 못 잡습니다.**
        `tests/timing.py` 의 주석이 그렇게 적혀 있는지 이 단언이 감시합니다 —
        누군가 여유를 0.5 로 줄이면 그 주석이 틀리게 되고 이것이 빨개집니다.
        """
        assert SCHEDULING_SLACK > 1.0
