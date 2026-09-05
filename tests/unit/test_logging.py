"""로깅 시스템 테스트."""

import json
import logging
from io import StringIO

import pytest

from vmkis import logging as vmkis_logging
from vmkis.logging import (
    JsonFormatter,
    disable_json_logging,
    enable_json_logging,
    get_logger,
    logger,
    setLevel,
)


class TestLoggingLevel:
    """로깅 레벨 설정 테스트."""

    def test_set_level_with_string(self):
        """문자열 로그 레벨 설정."""
        setLevel("DEBUG")
        assert logger.level == logging.DEBUG

        setLevel("INFO")
        assert logger.level == logging.INFO

        setLevel("WARNING")
        assert logger.level == logging.WARNING

        setLevel("ERROR")
        assert logger.level == logging.ERROR

        setLevel("CRITICAL")
        assert logger.level == logging.CRITICAL

    def test_set_level_with_int(self):
        """정수 로그 레벨 설정."""
        setLevel(logging.DEBUG)
        assert logger.level == logging.DEBUG

        setLevel(logging.INFO)
        assert logger.level == logging.INFO

    def test_set_level_invalid_string(self):
        """유효하지 않은 로그 레벨 문자열."""
        with pytest.raises(ValueError):
            setLevel("INVALID")  # type: ignore


class TestJsonFormatter:
    """JSON 포매터 테스트."""

    def test_format_basic_record(self):
        """기본 로그 레코드 JSON 포매팅."""
        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="vmkis.test",
            level=logging.INFO,
            pathname="test.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)
        data = json.loads(result)

        assert data["level"] == "INFO"
        assert data["logger"] == "vmkis.test"
        assert data["message"] == "Test message"
        assert data["line"] == 42
        assert "timestamp" in data
        assert "module" in data

    def test_format_record_with_exception(self):
        """예외 정보를 포함한 로그 레코드."""
        formatter = JsonFormatter()

        try:
            raise ValueError("Test error")
        except ValueError:
            import sys

            record = logging.LogRecord(
                name="vmkis.test",
                level=logging.ERROR,
                pathname="test.py",
                lineno=50,
                msg="Error occurred",
                args=(),
                exc_info=sys.exc_info(),
            )

            result = formatter.format(record)
            data = json.loads(result)

            assert data["level"] == "ERROR"
            assert "exception" in data
            assert data["exception"]["type"] == "ValueError"
            assert "Test error" in data["exception"]["message"]

    def test_format_record_with_context(self):
        """추가 컨텍스트 데이터를 포함한 로그 레코드."""
        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="vmkis.api",
            level=logging.WARNING,
            pathname="api.py",
            lineno=100,
            msg="Rate limit warning",
            args=(),
            exc_info=None,
        )
        record.context = {  # type: ignore
            "transaction_id": "TR123456",
            "retry_count": 2,
        }

        result = formatter.format(record)
        data = json.loads(result)

        assert data["level"] == "WARNING"
        assert data["context"]["transaction_id"] == "TR123456"
        assert data["context"]["retry_count"] == 2


class TestGetLogger:
    """서브 로거 획득 테스트."""

    def test_get_child_logger(self):
        """자식 로거 획득."""
        child_logger = get_logger("vmkis.api")
        assert child_logger.name == "vmkis.api"

    def test_get_multiple_child_loggers(self):
        """여러 자식 로거 획득."""
        api_logger = get_logger("vmkis.api")
        client_logger = get_logger("vmkis.client")

        assert api_logger.name == "vmkis.api"
        assert client_logger.name == "vmkis.client"
        assert api_logger is not client_logger


class TestJsonLoggingToggle:
    """JSON 로깅 활성화/비활성화 테스트."""

    def test_enable_json_logging(self):
        """JSON 로깅 활성화."""
        enable_json_logging()

        # 핸들러가 JsonFormatter를 사용하는지 확인
        assert len(logger.handlers) > 0
        handler = logger.handlers[0]
        assert isinstance(handler.formatter, JsonFormatter)

    def test_disable_json_logging(self):
        """JSON 로깅 비활성화."""
        enable_json_logging()
        disable_json_logging()

        # 핸들러가 ColoredFormatter를 사용하는지 확인
        assert len(logger.handlers) > 0
        handler = logger.handlers[0]
        # ColoredFormatter는 logging.Formatter의 서브클래스
        assert handler.formatter is not None

    def test_toggle_json_logging_multiple_times(self):
        """JSON 로깅 활성화/비활성화 반복."""
        for _ in range(3):
            enable_json_logging()
            assert isinstance(logger.handlers[0].formatter, JsonFormatter)

            disable_json_logging()
            assert logger.handlers[0].formatter is not None


@pytest.fixture
def restore_log_level():
    """테스트가 바꾼 전역 로거 레벨을 원복합니다.

    `logger`는 모듈 수준 싱글턴이라 레벨 변경이 다른 테스트로 샙니다.
    """
    initial = logger.level
    initial_handler_levels = [handler.level for handler in logger.handlers]

    yield

    logger.setLevel(initial)
    for handler, level in zip(logger.handlers, initial_handler_levels, strict=False):
        handler.setLevel(level)


class LogCapture:
    """`vmkis.logging.logger`의 핸들러 출력을 `StringIO`로 돌려 관측합니다."""

    def __init__(self) -> None:
        self.stream = StringIO()
        self._restores: list[tuple[logging.StreamHandler, object]] = []

    def bind(self) -> None:
        """현재 `logger.handlers`의 출력 스트림을 캡처 스트림으로 교체합니다.

        핸들러를 교체하는 `enable_json_logging()` 등을 호출한 뒤에는 새 핸들러를 붙잡기 위해 다시 호출해야 합니다.
        """
        for handler in logger.handlers:
            self._restores.append((handler, handler.stream))
            handler.setStream(self.stream)

    def restore(self) -> None:
        for handler, original in reversed(self._restores):
            handler.setStream(original)
        self._restores.clear()

    @property
    def value(self) -> str:
        return self.stream.getvalue()


@pytest.fixture
def log_output():
    """로거 출력 캡처 픽스처.

    `capsys`/`capfd`를 쓰지 않는 이유:

    `vmkis.logging`의 기본 핸들러는 **모듈 import 시점**에
    `logging.StreamHandler(stream=sys.stdout)`으로 만들어지며 그 시점의
    `sys.stdout` 객체를 붙잡는다. pytest 실행 중에는 그 객체가 pytest가 세션
    시작 시 설치한 전역 캡처 스트림이다. 따라서

    * `capsys`는 나중에 `sys.stdout`을 교체하므로 이미 붙잡힌 스트림을 보지 못하고,
    * `capfd`도 fd 1을 새로 리다이렉트할 뿐이라 전역 캡처 스트림으로 나가는
      출력을 보지 못한다.

    핸들러가 import 시점의 스트림을 붙잡는 것은 `logging.StreamHandler`의 정상
    동작이지 라이브러리 버그가 아니다. 그래서 pytest의 캡처 계층에 기대는 대신
    핸들러의 스트림을 직접 교체해 포매팅과 레벨 필터링을 결정적으로 검증한다.

    참고: https://github.com/visualmoney/vm-stock-kis/issues/3
    """
    capture = LogCapture()
    capture.bind()

    try:
        yield capture
    finally:
        capture.restore()


class TestLoggingIntegration:
    """로깅 통합 테스트."""

    def test_logger_output_format(self, log_output, restore_log_level):
        """로거 출력 형식 검증."""
        setLevel("INFO")

        logger.info("Test info message")

        assert "Test info message" in log_output.value
        assert "INFO" in log_output.value

    def test_json_logger_output_format(self, log_output, restore_log_level):
        """JSON 로거 출력 형식 검증."""
        enable_json_logging()
        # enable_json_logging()이 핸들러를 새로 만들므로 다시 붙잡는다.
        log_output.bind()

        try:
            setLevel("INFO")
            logger.info("Test JSON message")

            data = json.loads(log_output.value.strip())
            assert data["message"] == "Test JSON message"
            assert data["level"] == "INFO"
        finally:
            disable_json_logging()

    def test_logger_filtering_by_level(self, log_output, restore_log_level):
        """로깅 레벨에 따른 필터링."""
        setLevel("WARNING")

        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")

        assert "Debug message" not in log_output.value
        assert "Info message" not in log_output.value
        assert "Warning message" in log_output.value


@pytest.mark.parametrize(
    ("level_input", "expected_level"),
    [
        ("DEBUG", logging.DEBUG),
        ("INFO", logging.INFO),
        ("WARNING", logging.WARNING),
        ("ERROR", logging.ERROR),
        ("CRITICAL", logging.CRITICAL),
        (logging.DEBUG, logging.DEBUG),
        (logging.INFO, logging.INFO),
        (logging.WARNING, logging.WARNING),
        (logging.ERROR, logging.ERROR),
        (logging.CRITICAL, logging.CRITICAL),
    ],
)
def test_set_level(level_input, expected_level):
    """SetLevel 함수가 로거 레벨을 올바르게 설정하는지 테스트합니다."""
    initial_level = vmkis_logging.logger.level

    try:
        vmkis_logging.setLevel(level_input)
        assert vmkis_logging.logger.level == expected_level
    finally:
        # 테스트 후 원래 레벨로 복원
        vmkis_logging.logger.setLevel(initial_level)
