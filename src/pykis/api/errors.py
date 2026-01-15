from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from pykis.errors import PykisError


class KisApiError(PykisError):
    """Base exception for KIS API errors."""

    __slots__ = ()


@dataclass(frozen=True, slots=True)
class KisErrorContext:
    endpoint_id: str | None
    method: str | None
    path: str | None
    status_code: int | None
    message: str | None


class KisAuthError(KisApiError):
    """Authentication or token issuance errors."""

    __slots__ = ("context",)

    def __init__(self, message: str, *, context: KisErrorContext | None = None) -> None:
        super().__init__(message)
        self.context = context


class KisRateLimitError(KisApiError):
    """Rate limit errors."""

    __slots__ = ("context", "retry_after")

    def __init__(self, message: str, *, retry_after: float | None, context: KisErrorContext | None = None) -> None:
        super().__init__(message)
        self.context = context
        self.retry_after = retry_after


class KisTransportError(KisApiError):
    """Network or transport failures."""

    __slots__ = ("context", "original")

    def __init__(self, message: str, *, original: Exception, context: KisErrorContext | None = None) -> None:
        super().__init__(message)
        self.context = context
        self.original = original


class KisHttpError(KisApiError):
    """Non-OK HTTP responses."""

    __slots__ = ("context", "payload")

    def __init__(self, message: str, *, context: KisErrorContext | None = None, payload: str | None = None) -> None:
        super().__init__(message)
        self.context = context
        self.payload = payload


class KisResponseError(KisApiError):
    """Invalid or unexpected response payloads."""

    __slots__ = ("context", "payload")

    def __init__(
        self,
        message: str,
        *,
        context: KisErrorContext | None = None,
        payload: Mapping[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.context = context
        self.payload = payload


class KisUnsupportedEndpointError(KisApiError):
    """Endpoint not supported in the current domain."""

    __slots__ = ("context",)

    def __init__(self, message: str, *, context: KisErrorContext | None = None) -> None:
        super().__init__(message)
        self.context = context
