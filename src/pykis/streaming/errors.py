from __future__ import annotations

from pykis.errors import PykisError


class StreamingLimitError(PykisError):
    __slots__ = ("message",)

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
