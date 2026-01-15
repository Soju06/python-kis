from __future__ import annotations

import re

from codegen.api.models import DocEndpoint, DocField
from codegen.core.issues import IssueLevel, SpecIssue
from codegen.core.text import is_demo_unavailable

URL_RE = re.compile(r"^(https?|wss?)://", re.IGNORECASE)


def _is_url(value: str | None) -> bool:
    if not value:
        return False
    return bool(URL_RE.match(value.strip()))


def _field_has_description(field: DocField) -> bool:
    return bool((field.description or "").strip())


def validate_doc(doc: DocEndpoint) -> list[SpecIssue]:
    issues: list[SpecIssue] = []
    endpoint_id = doc.id

    method = (doc.method or "").upper()
    if method not in {"GET", "POST"}:
        issues.append(
            SpecIssue(
                IssueLevel.ERROR,
                "method.invalid",
                f"Unsupported HTTP method: {doc.method!r}",
                "method",
                endpoint_id,
            )
        )

    if not doc.url.startswith("/"):
        issues.append(
            SpecIssue(
                IssueLevel.ERROR,
                "url.invalid",
                f"URL must start with '/': {doc.url!r}",
                "url",
                endpoint_id,
            )
        )

    if doc.domains.demo and not _is_url(doc.domains.demo):
        if not is_demo_unavailable(doc.domains.demo):
            issues.append(
                SpecIssue(
                    IssueLevel.WARN,
                    "domain.demo.non_url",
                    f"Demo domain is non-URL placeholder: {doc.domains.demo!r}",
                    "domains.demo",
                    endpoint_id,
                )
            )

    if not (doc.content_type or "").strip():
        issues.append(
            SpecIssue(
                IssueLevel.WARN,
                "content_type.missing",
                "content_type is empty.",
                "content_type",
                endpoint_id,
            )
        )

    if not (doc.req_format or "").strip():
        issues.append(
            SpecIssue(
                IssueLevel.WARN,
                "req_format.missing",
                "req_format is empty.",
                "req_format",
                endpoint_id,
            )
        )

    for field in doc.request.headers:
        if not _field_has_description(field):
            issues.append(
                SpecIssue(
                    IssueLevel.WARN,
                    "request.header.description.missing",
                    f"Missing header description: {field.code}",
                    "request.headers",
                    endpoint_id,
                )
            )

    for field in doc.request.params:
        if not _field_has_description(field):
            issues.append(
                SpecIssue(
                    IssueLevel.WARN,
                    "request.params.description.missing",
                    f"Missing param description: {field.code}",
                    "request.params",
                    endpoint_id,
                )
            )

    for field in doc.request.body:
        if not _field_has_description(field):
            issues.append(
                SpecIssue(
                    IssueLevel.WARN,
                    "request.body.description.missing",
                    f"Missing body description: {field.code}",
                    "request.body",
                    endpoint_id,
                )
            )

    for field in doc.response.body:
        if not _field_has_description(field):
            issues.append(
                SpecIssue(
                    IssueLevel.WARN,
                    "response.body.description.missing",
                    f"Missing response description: {field.code}",
                    "response.body",
                    endpoint_id,
                )
            )

    return issues
