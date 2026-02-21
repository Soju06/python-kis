from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from pykis.errors import PykisError


class KisError(PykisError):
    """Base exception for pykis errors."""

    __slots__ = ()


class KisApiError(KisError):
    """Base exception for KIS API errors."""

    __slots__ = ()


@dataclass(frozen=True, slots=True)
class KisErrorContext:
    endpoint_id: str | None
    method: str | None
    path: str | None
    status_code: int | None
    message: str | None
    domain: str | None = None
    request_id: str | None = None


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

    __slots__ = (
        "context",
        "payload",
        "error_code",
        "user_message",
        "hint",
        "rule_id",
        "rule_type",
        "details",
    )

    def __init__(
        self,
        message: str,
        *,
        context: KisErrorContext | None = None,
        payload: Mapping[str, object] | None = None,
        error_code: str | None = None,
        user_message: str | None = None,
        hint: str | None = None,
        rule_id: str | None = None,
        rule_type: str | None = None,
        details: object | None = None,
    ) -> None:
        super().__init__(message)
        self.context = context
        self.payload = payload
        self.error_code = error_code
        self.user_message = user_message
        self.hint = hint
        self.rule_id = rule_id
        self.rule_type = rule_type
        self.details = details


class KisResponseIncompleteError(KisResponseError):
    """Missing keys/fields in response payloads."""

    __slots__ = ()


class KisResponseUnavailableError(KisResponseError):
    """Known unavailable cases (market closed, not published yet)."""

    __slots__ = ()


class KisResponseSentinelError(KisResponseError):
    """Sentinel values indicate invalid payloads."""

    __slots__ = ()


class KisInvalidResponseError(KisResponseError):
    """Fallback error for invalid payloads."""

    __slots__ = ()


class KisUnsupportedEndpointError(KisApiError):
    """Endpoint not supported in the current domain."""

    __slots__ = ("context",)

    def __init__(self, message: str, *, context: KisErrorContext | None = None) -> None:
        super().__init__(message)
        self.context = context
