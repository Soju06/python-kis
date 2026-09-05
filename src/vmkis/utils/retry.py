"""Exponential backoff retry 메커니즘

VmKis API 호출 시 일시적 오류(429, 5xx)에 대한 자동 재시도 기능을 제공합니다.

이 모듈은 **아무것도 import 하지 않습니다**(표준 라이브러리 제외).
`utils` 는 최하층이고, 상위 계층을 참조하면 아키텍처 불변식을 깨뜨립니다
(`docs/architecture/ARCHITECTURE.md` 의 "지켜야 할 불변식" 참고).

예전에는 `vmkis.client.exceptions` 에서 재시도 대상 예외 4종을 import 했습니다.
지금은 **예외 자신이 `retryable` 표식을 들고 있고**, 이 모듈은 그 표식만 봅니다.
"""

import asyncio
import logging
import random
import time
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, TypeVar

__all__ = [
    "with_retry",
    "with_async_retry",
    "retry_config",
    "is_retryable",
]

_logger = logging.getLogger(__name__)

T = TypeVar("T")
P = TypeVar("P")


class RetryConfig:
    """재시도 설정"""

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
    ):
        """재시도 설정 초기화

        Args:
            max_retries: 최대 재시도 횟수 (기본값: 3)
            initial_delay: 초기 대기 시간(초) (기본값: 1.0)
            max_delay: 최대 대기 시간(초) (기본값: 60.0)
            exponential_base: 지수 기반값 (기본값: 2.0, 1초 → 2초 → 4초 → 8초)
            jitter: 대기 시간에 무작위 값 추가 여부 (기본값: True)
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

    def calculate_delay(self, attempt: int) -> float:
        """재시도 대기 시간 계산

        Args:
            attempt: 현재 시도 횟수 (0부터 시작)

        Returns:
            대기 시간(초)
        """
        # exponential backoff: initial_delay * (base ^ attempt)
        delay = self.initial_delay * (self.exponential_base**attempt)
        delay = min(delay, self.max_delay)

        # jitter: 대기 시간에 ±10% 무작위 값 추가
        if self.jitter:
            jitter_amount = delay * 0.1
            delay += random.uniform(-jitter_amount, jitter_amount)

        return max(0, delay)


# 기본 재시도 설정
retry_config = RetryConfig(
    max_retries=3,
    initial_delay=1.0,
    max_delay=60.0,
    exponential_base=2.0,
    jitter=True,
)


def _resolve_config(max_retries: int | None, initial_delay: float | None) -> RetryConfig:
    """전역 기본값 위에 인자를 얹은 **새 설정**을 만듭니다.

    예전에는 이렇게 되어 있었습니다.

        config = retry_config              # 사본이 아니라 전역 객체 그 자체
        if max_retries is not None:
            config.max_retries = max_retries

    `@with_retry(max_retries=7)` 를 한 번 쓰면 전역이 7로 바뀌고, 그 뒤로는
    인자 없는 `@with_retry()` 까지 7회 재시도했습니다. 호출 순서에 따라 동작이
    달라져 재현도 어려웠습니다.

    전역은 **읽기만** 합니다.
    """
    return RetryConfig(
        max_retries=retry_config.max_retries if max_retries is None else max_retries,
        initial_delay=retry_config.initial_delay if initial_delay is None else initial_delay,
        max_delay=retry_config.max_delay,
        exponential_base=retry_config.exponential_base,
        jitter=retry_config.jitter,
    )


def is_retryable(exc: BaseException) -> bool:
    """예외가 재시도 대상인지 판단합니다.

    예외 **종류 목록**을 여기 두면 이 모듈이 `vmkis.client.exceptions` 를
    import 해야 합니다. 대신 예외가 스스로 `retryable = True` 를 선언하게 하고
    여기서는 그 표식만 봅니다.

    표식이 없는 임의의 예외(표준 라이브러리 등)는 재시도하지 않습니다.
    """
    return getattr(exc, "retryable", False) is True


def with_retry(
    max_retries: int | None = None,
    initial_delay: float | None = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """동기 함수에 재시도 메커니즘을 추가하는 데코레이터

    Args:
        max_retries: 최대 재시도 횟수 (None이면 기본값 사용)
        initial_delay: 초기 대기 시간(초) (None이면 기본값 사용)

    Returns:
        데코레이터 함수

    Example:
        ```python
        @with_retry(max_retries=5, initial_delay=2.0)
        def fetch_data(symbol: str) -> Quote:
            return kis_client.get_quote(symbol)

        # 호출 시 429/5xx 에러 발생 시 자동 재시도
        data = fetch_data("005930")
        ```
    """

    config = _resolve_config(max_retries, initial_delay)

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            for attempt in range(config.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if not is_retryable(e):
                        raise
                    last_exception = e
                    if attempt < config.max_retries:
                        delay = config.calculate_delay(attempt)
                        _logger.warning(
                            f"재시도 가능한 오류 발생: {type(e).__name__}. "
                            f"{delay:.1f}초 후 재시도 ({attempt + 1}/{config.max_retries})"
                        )
                        time.sleep(delay)
                    else:
                        _logger.error(f"최대 재시도 횟수 초과: {type(e).__name__}")

            raise last_exception or RuntimeError("Unknown error")

        return wrapper

    return decorator


def with_async_retry(
    max_retries: int | None = None,
    initial_delay: float | None = None,
) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]:
    """비동기 함수에 재시도 메커니즘을 추가하는 데코레이터

    Args:
        max_retries: 최대 재시도 횟수 (None이면 기본값 사용)
        initial_delay: 초기 대기 시간(초) (None이면 기본값 사용)

    Returns:
        데코레이터 함수

    Example:
        ```python
        @with_async_retry(max_retries=5, initial_delay=2.0)
        async def fetch_data(symbol: str) -> Quote:
            return await kis_client.get_quote_async(symbol)

        # 호출 시 429/5xx 에러 발생 시 자동 재시도
        data = await fetch_data("005930")
        ```
    """

    config = _resolve_config(max_retries, initial_delay)

    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            for attempt in range(config.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if not is_retryable(e):
                        raise
                    last_exception = e
                    if attempt < config.max_retries:
                        delay = config.calculate_delay(attempt)
                        _logger.warning(
                            f"재시도 가능한 오류 발생: {type(e).__name__}. "
                            f"{delay:.1f}초 후 재시도 ({attempt + 1}/{config.max_retries})"
                        )
                        await asyncio.sleep(delay)
                    else:
                        _logger.error(f"최대 재시도 횟수 초과: {type(e).__name__}")

            raise last_exception or RuntimeError("Unknown error")

        return wrapper

    return decorator
