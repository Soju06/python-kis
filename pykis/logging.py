import logging
import sys
from typing import Literal

from colorlog import ColoredFormatter

__all__ = [
    "logger",
    "setLevel",
]


def _create_logger(name: str, level) -> logging.Logger:
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(
        ColoredFormatter(
            "%(log_color)s[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%m/%d %H:%M:%S",
            reset=True,
            log_colors={
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


logger = _create_logger("pykis", logging.INFO)


def setLevel(level: int | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]) -> None:
    """PyKis 로거의 로깅 레벨을 설정합니다."""
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

    logger.setLevel(level)
