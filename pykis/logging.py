import logging
import sys
from colorlog import ColoredFormatter

logging.addLevelName(logging.DEBUG, "DEBG")
logging.addLevelName(logging.INFO, "INFO")
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.ERROR, "EROR")
logging.addLevelName(logging.CRITICAL, "CRIT")


def _create_logger(name: str, level) -> logging.Logger:
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(
        ColoredFormatter(
            "%(log_color)s[%(asctime)s] %(levelname)s %(message)s",
            datefmt="%m/%d %H:%M:%S",
            reset=True,
            log_colors={
                "DEBUG": "white",
                "INFO": "white,bold",
                "INFOV": "white,bold",
                "WARNING": "yellow",
                "ERROR": "red,bold",
                "CRITICAL": "red,bold",
            },
            secondary_log_colors={},
            style="%",
        )
    )
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


logger = _create_logger("pykis", logging.INFO)
