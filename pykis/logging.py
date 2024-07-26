import logging
import sys

from colorlog import ColoredFormatter

__all__ = [
    "logger",
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
