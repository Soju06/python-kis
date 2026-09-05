"""VmKis 로깅 시스템

기본 텍스트 로깅과 JSON 구조 로깅을 지원합니다.
- 개발 환경: 컬러가 지정된 텍스트 로그
- 프로덕션 환경: JSON 구조 로그 (파싱 용이)
"""

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Literal

from colorlog import ColoredFormatter

__all__ = [
    "logger",
    "setLevel",
    "JsonFormatter",
    "get_logger",
    "enable_json_logging",
    "disable_json_logging",
]


class JsonFormatter(logging.Formatter):
    """JSON 구조 로깅 포매터

    로그 레코드를 JSON 형식으로 변환합니다.
    ELK, Datadog 등의 로그 수집 서비스에 호환됩니다.
    """

    def format(self, record: logging.LogRecord) -> str:
        """로그 레코드를 JSON 문자열로 변환

        Args:
            record: 로깅 레코드

        Returns:
            JSON 형식의 로그 문자열
        """
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # 예외 정보 포함
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
            }

        # 추가 컨텍스트 데이터
        if hasattr(record, "context"):
            log_data["context"] = record.context

        try:
            return json.dumps(log_data, ensure_ascii=False, default=str)
        except (TypeError, ValueError):
            # JSON 직렬화 실패 시 기본 형식으로 폴백
            return f"{log_data['timestamp']} {log_data['level']} {log_data['message']}"


def _create_logger(
    name: str,
    level: int = logging.INFO,
    use_json: bool = False,
) -> logging.Logger:
    """로거 생성

    Args:
        name: 로거 이름
        level: 로깅 레벨
        use_json: JSON 포매터 사용 여부

    Returns:
        설정된 로거
    """
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(stream=sys.stdout)

    if use_json:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            ColoredFormatter(
                "%(log_color)s[%(asctime)s] %(levelname)s: %(message)s",
                datefmt="%m/%d %H:%M:%S",
                reset=True,
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "white",
                    "WARNING": "bold_yellow",
                    "ERROR": "bold_red",
                    "CRITICAL": "bold_red",
                },
                secondary_log_colors={},
                style="%",
            )
        )

    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


# 기본 로거
logger = _create_logger("vmkis", logging.INFO, use_json=False)


def get_logger(name: str) -> logging.Logger:
    """서브 로거 획득

    Args:
        name: 로거 이름 (e.g., "vmkis.api", "vmkis.client")

    Returns:
        로거 인스턴스
    """
    return logging.getLogger(name)


def setLevel(level: int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]) -> None:
    """VmKis 로거의 로깅 레벨을 설정합니다

    Args:
        level: 로깅 레벨 (정수 또는 문자열)

    Example:
        ```python
        from vmkis import setLevel

        setLevel("DEBUG")  # 디버그 레벨로 설정
        setLevel(logging.WARNING)  # 경고 레벨로 설정
        ```
    """
    if isinstance(level, str):
        match level:
            case "DEBUG":
                level = logging.DEBUG
            case "INFO":
                level = logging.INFO
            case "WARNING":
                level = logging.WARNING
            case "ERROR":
                level = logging.ERROR
            case "CRITICAL":
                level = logging.CRITICAL
            case _:
                raise ValueError(f"Invalid log level: {level}")

    logger.setLevel(level)
    # 모든 자식 로거도 함께 설정
    for handler in logger.handlers:
        handler.setLevel(level)


def enable_json_logging() -> None:
    """JSON 구조 로깅 활성화

    프로덕션 환경에서 로그 수집 서비스를 사용할 때 호출합니다.

    Example:
        ```python
        from vmkis.logging import enable_json_logging

        enable_json_logging()  # JSON 포매팅 활성화
        ```
    """
    global logger
    logger.handlers.clear()
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)


def disable_json_logging() -> None:
    """JSON 구조 로깅 비활성화

    텍스트 로깅으로 복구합니다.

    Example:
        ```python
        from vmkis.logging import disable_json_logging

        disable_json_logging()  # 텍스트 포매팅으로 복구
        ```
    """
    global logger
    logger.handlers.clear()
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(
        ColoredFormatter(
            "%(log_color)s[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%m/%d %H:%M:%S",
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "white",
                "WARNING": "bold_yellow",
                "ERROR": "bold_red",
                "CRITICAL": "bold_red",
            },
            secondary_log_colors={},
            style="%",
        )
    )
    logger.addHandler(handler)
