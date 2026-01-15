from __future__ import annotations

import logging
from typing import Iterable


DEFAULT_LOGGER_NAME = "pykis"


def get_logger(name: str | None = None) -> logging.Logger:
    if name is None:
        return logging.getLogger(DEFAULT_LOGGER_NAME)
    if name.startswith(DEFAULT_LOGGER_NAME):
        return logging.getLogger(name)
    return logging.getLogger(f"{DEFAULT_LOGGER_NAME}.{name}")


def configure_logging(
    *,
    level: int = logging.INFO,
    handlers: Iterable[logging.Handler] | None = None,
    fmt: str | None = None,
) -> None:
    if handlers is None:
        handlers = [logging.StreamHandler()]
    if fmt is None:
        fmt = "%(asctime)s %(levelname)s %(name)s: %(message)s"
    root = logging.getLogger(DEFAULT_LOGGER_NAME)
    root.setLevel(level)
    root.handlers.clear()
    for handler in handlers:
        handler.setFormatter(logging.Formatter(fmt))
        root.addHandler(handler)
