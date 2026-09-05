"""Exception 클래스 및 retry 메커니즘 테스트."""

import time
from unittest.mock import MagicMock

import pytest

from vmkis.client.exceptions import (
    KisAuthenticationError,
    KisConnectionError,
    KisHTTPNotFoundError,
    KisRateLimitError,
    KisServerError,
    KisTimeoutError,
    KisValidationError,
)
from vmkis.utils.retry import RetryConfig, with_async_retry, with_retry


def _make_response(status_code: int) -> MagicMock:
    """예외 생성에 필요한 최소한의 Response 목."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.reason = "Test"
    resp.text = "body"
    resp.request.headers = {}
    resp.request.method = "GET"
    resp.request.url = "https://api.example.com/test"
    resp.request.body = None
    return resp


class TestExceptionHierarchy:
    """Exception 클래스 계층 구조 테스트."""

    def test_kis_authentication_error_is_http_error(self):
        """KisAuthenticationError는 KisHTTPError 하위 클래스."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.reason = "Unauthorized"
        mock_response.text = "Invalid appkey"
        mock_response.request.headers = {}
        mock_response.request.method = "GET"
        mock_response.request.url = "https://api.example.com/test"
        mock_response.request.body = None

        exc = KisAuthenticationError(mock_response)
        assert isinstance(exc, KisAuthenticationError)
        assert exc.status_code == 401

    def test_kis_rate_limit_error_is_http_error(self):
        """KisRateLimitError는 KisHTTPError 하위 클래스."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.reason = "Too Many Requests"
        mock_response.text = "Rate limit exceeded"
        mock_response.request.headers = {}
        mock_response.request.method = "GET"
        mock_response.request.url = "https://api.example.com/test"
        mock_response.request.body = None

        exc = KisRateLimitError(mock_response)
        assert exc.status_code == 429

    def test_kis_server_error_is_http_error(self):
        """KisServerError는 KisHTTPError 하위 클래스 (5xx)"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.reason = "Internal Server Error"
        mock_response.text = "Server error"
        mock_response.request.headers = {}
        mock_response.request.method = "GET"
        mock_response.request.url = "https://api.example.com/test"
        mock_response.request.body = None

        exc = KisServerError(mock_response)
        assert exc.status_code == 500

    def test_kis_timeout_error_is_retryable(self):
        """KisTimeoutError는 재시도 가능."""
        mock_response = MagicMock()
        mock_response.status_code = 0  # 연결 타임아웃
        mock_response.reason = "Timeout"
        mock_response.text = "Request timeout"
        mock_response.request.headers = {}
        mock_response.request.method = "GET"
        mock_response.request.url = "https://api.example.com/test"
        mock_response.request.body = None

        exc = KisTimeoutError(mock_response)
        assert isinstance(exc, KisTimeoutError)


class TestRetryConfig:
    """RetryConfig 설정 테스트."""

    def test_default_retry_config(self):
        """기본 retry 설정 검증."""
        config = RetryConfig()
        assert config.max_retries == 3
        assert config.initial_delay == 1.0
        assert config.max_delay == 60.0
        assert config.exponential_base == 2.0
        assert config.jitter is True

    def test_calculate_delay_exponential_backoff(self):
        """Exponential backoff 계산 검증."""
        config = RetryConfig(
            initial_delay=1.0,
            exponential_base=2.0,
            jitter=False,
        )
        assert config.calculate_delay(0) == 1.0  # 1 * 2^0
        assert config.calculate_delay(1) == 2.0  # 1 * 2^1
        assert config.calculate_delay(2) == 4.0  # 1 * 2^2
        assert config.calculate_delay(3) == 8.0  # 1 * 2^3

    def test_calculate_delay_max_delay_limit(self):
        """최대 대기 시간 초과 방지."""
        config = RetryConfig(
            initial_delay=30.0,
            max_delay=60.0,
            exponential_base=2.0,
            jitter=False,
        )
        delay = config.calculate_delay(2)  # 30 * 2^2 = 120
        assert delay == 60.0  # max_delay로 제한

    def test_calculate_delay_with_jitter(self):
        """Jitter 추가 검증 (범위 검사)"""
        config = RetryConfig(
            initial_delay=10.0,
            exponential_base=2.0,
            jitter=True,
        )
        delays = [config.calculate_delay(1) for _ in range(10)]
        # 기본값: 20 * (1 - 0.1) ~ 20 * (1 + 0.1) = 18 ~ 22
        assert all(17 < d < 23 for d in delays), f"Jitter delays out of range: {delays}"


class TestWithRetryDecorator:
    """@with_retry 데코레이터 테스트"""

    def test_successful_call_no_retry(self):
        """성공한 호출은 재시도하지 않음."""
        call_count = 0

        @with_retry(max_retries=3, initial_delay=0.1)
        def successful_func():
            nonlocal call_count
            call_count += 1
            return "success"

        result = successful_func()
        assert result == "success"
        assert call_count == 1

    def test_retryable_exception_retry_success(self):
        """재시도 가능한 예외 발생 후 성공."""
        call_count = 0
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.reason = "Too Many Requests"
        mock_response.text = "Rate limit"
        mock_response.request.headers = {}
        mock_response.request.method = "GET"
        mock_response.request.url = "https://api.example.com/test"
        mock_response.request.body = None

        @with_retry(max_retries=3, initial_delay=0.05)
        def eventually_successful():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise KisRateLimitError(mock_response)
            return "success"

        result = eventually_successful()
        assert result == "success"
        assert call_count == 3

    def test_max_retries_exceeded(self):
        """최대 재시도 횟수 초과."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.reason = "Internal Server Error"
        mock_response.text = "Server error"
        mock_response.request.headers = {}
        mock_response.request.method = "GET"
        mock_response.request.url = "https://api.example.com/test"
        mock_response.request.body = None

        @with_retry(max_retries=2, initial_delay=0.05)
        def always_fails():
            raise KisServerError(mock_response)

        with pytest.raises(KisServerError):
            always_fails()

    def test_non_retryable_exception_not_retried(self):
        """재시도 불가능한 예외는 즉시 발생."""
        call_count = 0

        @with_retry(max_retries=3, initial_delay=0.1)
        def fail_non_retryable():
            nonlocal call_count
            call_count += 1
            # Mock response with proper attributes
            mock_response = MagicMock()
            mock_response.status_code = 400
            mock_response.text = "Bad Request"
            mock_response.headers = {}
            mock_request = MagicMock()
            mock_request.url = "https://test.com/api"
            mock_request.method = "POST"
            mock_request.headers = {}
            mock_request.body = b""
            mock_response.request = mock_request
            raise KisValidationError(mock_response)

        with pytest.raises(KisValidationError):
            fail_non_retryable()

        # 재시도하지 않으므로 호출 횟수는 1
        assert call_count == 1

    def test_retry_multiple_exception_types(self):
        """다양한 재시도 가능 예외 처리."""
        call_count = 0
        mock_response_429 = MagicMock()
        mock_response_429.status_code = 429
        mock_response_429.reason = "Too Many Requests"
        mock_response_429.text = "Rate limit"
        mock_response_429.request.headers = {}
        mock_response_429.request.method = "GET"
        mock_response_429.request.url = "https://api.example.com/test"
        mock_response_429.request.body = None

        mock_response_500 = MagicMock()
        mock_response_500.status_code = 500
        mock_response_500.reason = "Server Error"
        mock_response_500.text = "Error"
        mock_response_500.request.headers = {}
        mock_response_500.request.method = "GET"
        mock_response_500.request.url = "https://api.example.com/test"
        mock_response_500.request.body = None

        @with_retry(max_retries=3, initial_delay=0.05)
        def fail_different_exceptions():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise KisRateLimitError(mock_response_429)
            elif call_count == 2:
                raise KisServerError(mock_response_500)
            return "success"

        result = fail_different_exceptions()
        assert result == "success"
        assert call_count == 3


class TestWithAsyncRetryDecorator:
    """@with_async_retry 데코레이터 테스트"""

    @pytest.mark.asyncio
    async def test_async_successful_call_no_retry(self):
        """비동기 성공한 호출은 재시도하지 않음."""
        call_count = 0

        @with_async_retry(max_retries=3, initial_delay=0.05)
        async def async_successful():
            nonlocal call_count
            call_count += 1
            return "success"

        result = await async_successful()
        assert result == "success"
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_async_retryable_exception_retry_success(self):
        """비동기 재시도 가능한 예외 발생 후 성공."""
        call_count = 0
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.reason = "Too Many Requests"
        mock_response.text = "Rate limit"
        mock_response.request.headers = {}
        mock_response.request.method = "GET"
        mock_response.request.url = "https://api.example.com/test"
        mock_response.request.body = None

        @with_async_retry(max_retries=3, initial_delay=0.05)
        async def async_eventually_successful():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise KisRateLimitError(mock_response)
            return "success"

        result = await async_eventually_successful()
        assert result == "success"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_async_max_retries_exceeded(self):
        """비동기 최대 재시도 횟수 초과."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.reason = "Internal Server Error"
        mock_response.text = "Server error"
        mock_response.request.headers = {}
        mock_response.request.method = "GET"
        mock_response.request.url = "https://api.example.com/test"
        mock_response.request.body = None

        @with_async_retry(max_retries=2, initial_delay=0.05)
        async def async_always_fails():
            raise KisServerError(mock_response)

        with pytest.raises(KisServerError):
            await async_always_fails()

    @pytest.mark.asyncio
    async def test_async_timing_between_retries(self):
        """비동기 재시도 간 대기 시간 검증."""
        call_count = 0
        start_time = time.time()
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.reason = "Too Many Requests"
        mock_response.text = "Rate limit"
        mock_response.request.headers = {}
        mock_response.request.method = "GET"
        mock_response.request.url = "https://api.example.com/test"
        mock_response.request.body = None

        @with_async_retry(max_retries=2, initial_delay=0.1)
        async def async_eventually_successful():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise KisRateLimitError(mock_response)
            return "success"

        result = await async_eventually_successful()
        elapsed_time = time.time() - start_time

        assert result == "success"
        # 2 retries with delays: 0.1s (jitter 포함)
        # 최소 0.2초 이상 소요
        assert elapsed_time >= 0.15


# ---------------------------------------------------------------------------
# 이슈 #18 — 전역 retry_config 변형 버그와 계층 위반
#
# `with_retry` 가 전역 싱글턴을 제자리에서 변형해, 한 번 인자를 준 뒤로는
# 인자 없는 `@with_retry()` 까지 그 값을 물려받았다. 호출 순서에 따라 동작이
# 달라져 재현이 어려웠고, 커버리지 95%인데도 잡히지 않았다 —
# 어떤 테스트도 `with_retry()` 를 인자 없이 부른 적이 없었기 때문이다.
# ---------------------------------------------------------------------------


class TestRetryConfigIsolation:
    """데코레이터는 전역 설정을 읽기만 해야 한다"""

    def test_with_retry_does_not_mutate_global_config(self):
        from vmkis.utils.retry import retry_config

        before = (retry_config.max_retries, retry_config.initial_delay)

        @with_retry(max_retries=7, initial_delay=9.0)
        def f():
            return "ok"

        f()

        assert (retry_config.max_retries, retry_config.initial_delay) == before

    def test_with_async_retry_does_not_mutate_global_config(self):
        from vmkis.utils.retry import retry_config

        before = (retry_config.max_retries, retry_config.initial_delay)

        @with_async_retry(max_retries=11, initial_delay=3.0)
        async def f():
            return "ok"

        assert (retry_config.max_retries, retry_config.initial_delay) == before

    def test_default_decorator_is_not_polluted_by_another(self):
        """이 버그의 실제 피해 지점.

        인자를 준 데코레이터가 전역을 바꾸면, **기본값을 의도한** 다른
        데코레이터가 그 값을 물려받는다. 시세 조회 하나가 9초씩 기다리게 된다.
        """
        from vmkis.utils.retry import retry_config

        @with_retry(max_retries=7, initial_delay=9.0)
        def polluter():
            return "ok"

        polluter()

        attempts = []

        @with_retry(initial_delay=0.001)  # max_retries 는 기본값을 의도
        def default_user():
            attempts.append(1)
            raise KisServerError(_make_response(500))

        with pytest.raises(KisServerError):
            default_user()

        # 기본값 3회 재시도 + 최초 1회 = 4. 오염됐다면 8이 된다.
        assert len(attempts) == retry_config.max_retries + 1


class TestRetryableMarker:
    """재시도 판단은 예외가 들고 있는 `retryable` 표식으로 한다.

    예외 **종류 목록**을 utils 에 두면 `utils -> client` 역방향 의존이 생긴다.
    """

    def test_retry_module_imports_nothing_from_vmkis(self):
        """`utils/retry.py` 는 상위 계층을 import 하지 않아야 한다."""
        import ast
        import pathlib

        source = pathlib.Path("src/vmkis/utils/retry.py").read_text(encoding="utf-8")
        imported = {
            node.module for node in ast.walk(ast.parse(source)) if isinstance(node, ast.ImportFrom) and node.module
        }

        assert not [m for m in imported if m.startswith("vmkis")], (
            f"utils/retry.py 가 상위 계층을 import 합니다: {imported}"
        )

    @pytest.mark.parametrize(
        "exc_type, expected",
        [
            (KisRateLimitError, True),
            (KisServerError, True),
            (KisTimeoutError, True),
            (KisConnectionError, True),
            (KisHTTPNotFoundError, False),
            (KisAuthenticationError, False),
        ],
    )
    def test_retryable_marker(self, exc_type, expected):
        from vmkis.utils.retry import is_retryable

        assert is_retryable(exc_type(_make_response(500))) is expected

    def test_unknown_exception_is_not_retryable(self):
        from vmkis.utils.retry import is_retryable

        assert is_retryable(ValueError("표식 없음")) is False

    def test_non_retryable_exception_is_reraised_immediately(self):
        attempts = []

        @with_retry(max_retries=3, initial_delay=0.001)
        def f():
            attempts.append(1)
            raise ValueError("재시도 대상 아님")

        with pytest.raises(ValueError):
            f()

        assert len(attempts) == 1
