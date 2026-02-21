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


def _missing_description_codes(fields: list[DocField]) -> list[str]:
    missing: list[str] = []
    for field in fields:
        if _field_has_description(field):
            continue
        code = field.code.strip()
        if not code:
            continue
        missing.append(code)
    return missing


def _append_missing_description_issue(
    issues: list[SpecIssue],
    *,
    endpoint_id: str,
    code: str,
    path: str,
    label: str,
    missing_codes: list[str],
) -> None:
    if not missing_codes:
        return
    preview = ", ".join(missing_codes[:5])
    tail = f", … (+{len(missing_codes) - 5})" if len(missing_codes) > 5 else ""
    issues.append(
        SpecIssue(
            IssueLevel.WARN,
            code,
            f"Missing {label} descriptions: {len(missing_codes)} fields ({preview}{tail})",
            path,
            endpoint_id,
        )
    )


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

    _append_missing_description_issue(
        issues,
        endpoint_id=endpoint_id,
        code="request.header.description.missing",
        path="request.headers",
        label="header",
        missing_codes=_missing_description_codes(doc.request.headers),
    )
    _append_missing_description_issue(
        issues,
        endpoint_id=endpoint_id,
        code="request.params.description.missing",
        path="request.params",
        label="param",
        missing_codes=_missing_description_codes(doc.request.params),
    )
    _append_missing_description_issue(
        issues,
        endpoint_id=endpoint_id,
        code="request.body.description.missing",
        path="request.body",
        label="request body",
        missing_codes=_missing_description_codes(doc.request.body),
    )
    _append_missing_description_issue(
        issues,
        endpoint_id=endpoint_id,
        code="response.body.description.missing",
        path="response.body",
        label="response body",
        missing_codes=_missing_description_codes(doc.response.body),
    )

    return issues
