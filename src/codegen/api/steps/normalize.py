from __future__ import annotations

from typing import Iterable

from codegen.api.models import (
    DocEndpoint,
    EndpointSpec,
    SpecDomains,
    SpecField,
    SpecOutput,
    SpecRequest,
    SpecResponse,
)
from codegen.api.steps.validate import URL_RE, validate_doc
from codegen.core.issues import IssueLevel, IssueReport, SpecIssue
from codegen.core.text import is_demo_unavailable, is_forced_null_description

HTTP_REAL_DOMAIN = "https://openapi.koreainvestment.com:9443"
HTTP_DEMO_DOMAIN = "https://openapivts.koreainvestment.com:29443"


def _normalize_domains(doc: DocEndpoint, report: IssueReport) -> SpecDomains:
    real = doc.domains.real
    demo = doc.domains.demo

    if not real or not URL_RE.match(real.strip()):
        real = HTTP_REAL_DOMAIN

    if demo and not URL_RE.match(demo.strip()):
        if is_demo_unavailable(demo):
            demo = None
        else:
            report.add(
                SpecIssue(
                    IssueLevel.WARN,
                    "domain.demo.placeholder",
                    f"Demo domain placeholder mapped to None: {demo!r}",
                    "domains.demo",
                    doc.id,
                )
            )
            demo = None

    if not demo and not _demo_disabled(doc):
        demo = HTTP_DEMO_DOMAIN

    return SpecDomains(real=real, demo=demo)


def _demo_disabled(doc: DocEndpoint) -> bool:
    if is_demo_unavailable(doc.demo_tr_id):
        return True
    for tr_id in doc.tr_ids:
        if isinstance(tr_id, str) and is_demo_unavailable(tr_id):
            return True
    if is_demo_unavailable(doc.domains.demo):
        return True
    return False


def _clean_tr_id(value: str | None) -> str | None:
    if not value:
        return None
    if is_demo_unavailable(value):
        return None
    return value


def _infer_content_type(doc: DocEndpoint) -> str | None:
    if doc.content_type and doc.content_type.strip():
        return doc.content_type
    for header in doc.request.headers:
        if header.code.lower() == "content-type" and header.description:
            return header.description.strip()
    return doc.content_type


def _infer_req_format(doc: DocEndpoint, content_type: str | None) -> str | None:
    if doc.req_format and doc.req_format.strip():
        return doc.req_format
    if content_type and "json" in content_type.lower():
        return "JSON"
    if content_type and "form" in content_type.lower():
        return "FORM"
    return doc.req_format


_RELAX_REQUIRED_PHRASES = ("특정 경우에만 데이터 출력", "데이터 미회신")


def _should_relax_required(field: SpecField) -> bool:
    if not field.required:
        return False
    desc = (field.description or "").strip()
    if not desc:
        return False
    return any(phrase in desc for phrase in _RELAX_REQUIRED_PHRASES)


def _normalize_summary_description(doc: DocEndpoint, report: IssueReport) -> tuple[str | None, str | None]:
    summary = (doc.summary or "").strip()
    description = (doc.description or "").strip()
    if summary:
        if description and summary != description:
            return None, f"{summary}\n{description}".strip()
        return None, summary

    return None, description


def normalize_doc(doc: DocEndpoint, source_path: str) -> tuple[EndpointSpec | None, IssueReport]:
    report = IssueReport()
    report.extend(validate_doc(doc))

    if report.has_errors():
        return None, report

    method = doc.method.upper()
    content_type = _infer_content_type(doc)
    req_format = _infer_req_format(doc, content_type)
    _, description = _normalize_summary_description(doc, report)

    query_fields = list(doc.request.params)
    body_fields = list(doc.request.body)

    def _filter_invalid(fields: list[SpecField] | list) -> list:
        filtered = []
        for field in fields:
            code = getattr(field, "code", "")
            if "…" in code or "..." in code:
                report.add(
                    SpecIssue(
                        IssueLevel.WARN,
                        "field.code.invalid",
                        f"Dropping templated field code: {code}",
                        "request",
                        doc.id,
                    )
                )
                continue
            filtered.append(field)
        return filtered

    query_fields = _filter_invalid(query_fields)
    body_fields = _filter_invalid(body_fields)

    if method == "GET" and body_fields:
        query_fields = query_fields + body_fields
        body_fields = []

    def _apply_null_required(fields: list[SpecField]) -> list[SpecField]:
        updated: list[SpecField] = []
        for field in fields:
            if field.required and is_forced_null_description(field.description):
                report.add(
                    SpecIssue(
                        IssueLevel.WARN,
                        "field.required.null_description",
                        "Field marked required but description enforces null; relaxing required flag.",
                        "request",
                        doc.id,
                    )
                )
                updated.append(SpecField.model_validate({**field.model_dump(), "required": False}))
            else:
                updated.append(field)
        return updated

    query_fields = _apply_null_required(query_fields)
    body_fields = _apply_null_required(body_fields)

    response_fields = [SpecField.model_validate(field.model_dump()) for field in doc.response.body]
    envelope_fields: list[SpecField] = []
    outputs: list[SpecOutput] = []
    current_output: SpecOutput | None = None
    output_markers = {"output", "output1", "output2", "output3"}

    for field in response_fields:
        code = field.code.lower()
        if code in output_markers:
            desc = (field.description or "").lower()
            type_name = (field.type_name or "").lower()
            field_name = (field.name or "").lower()
            if "array" in desc or "배열" in desc or "array" in type_name or "list" in type_name or "배열" in field_name:
                kind = "array"
            elif "single" in desc:
                if code.endswith(("2", "3")):
                    kind = "array"
                else:
                    kind = "single"
            else:
                if code.endswith("1") or code == "output":
                    kind = "single"
                elif code.endswith(("2", "3")):
                    kind = "array"
                else:
                    kind = "unknown"
            current_output = SpecOutput(code=field.code, name=field.name, kind=kind, fields=[])
            outputs.append(current_output)
            continue

        if _should_relax_required(field):
            report.add(
                SpecIssue(
                    IssueLevel.WARN,
                    "field.required.relaxed_by_description",
                    "Field marked required but description indicates optional output; relaxing required flag.",
                    "response",
                    doc.id,
                )
            )
            field = SpecField.model_validate({**field.model_dump(), "required": False})

        if current_output is None:
            envelope_fields.append(field)
        else:
            current_output.fields.append(field)

    spec = EndpointSpec(
        id=doc.id,
        name=doc.name,
        section=doc.section,
        category=doc.category,
        subcategory=doc.subcategory,
        method=method,  # type: ignore[arg-type]
        path=doc.url,
        content_type=content_type,
        req_format=req_format,
        domains=_normalize_domains(doc, report),
        tr_ids=doc.tr_ids,
        real_tr_id=_clean_tr_id(doc.real_tr_id),
        demo_tr_id=_clean_tr_id(doc.demo_tr_id),
        description=description,
        metadata=doc.metadata,
        request=SpecRequest(
            headers=[SpecField.model_validate(field.model_dump()) for field in doc.request.headers],
            query=[SpecField.model_validate(field.model_dump()) for field in query_fields],
            body=[SpecField.model_validate(field.model_dump()) for field in body_fields],
            example=doc.request.example,
        ),
        response=SpecResponse(
            headers=[SpecField.model_validate(field.model_dump()) for field in doc.response.headers],
            body=envelope_fields,
            outputs=outputs,
            example=doc.response.example,
        ),
        errors=doc.errors,
        source_path=source_path,
    )

    return spec, report


def normalize_all(
    docs: Iterable[tuple[DocEndpoint, str]]
) -> tuple[list[EndpointSpec], IssueReport]:
    report = IssueReport()
    specs: list[EndpointSpec] = []
    for doc, source_path in docs:
        spec, doc_report = normalize_doc(doc, source_path)
        report.extend(doc_report.issues)
        if spec is not None:
            specs.append(spec)
    return specs, report
