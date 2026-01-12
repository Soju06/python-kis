from __future__ import annotations

from typing import Iterable

from .errors import IssueReport, IssueLevel, SpecIssue
from .models import DocEndpoint, EndpointSpec, SpecDomains, SpecField, SpecOutput, SpecRequest, SpecResponse
from .validate import URL_RE, validate_doc


HTTP_REAL_DOMAIN = "https://openapi.koreainvestment.com:9443"
HTTP_VIRTUAL_DOMAIN = "https://openapivts.koreainvestment.com:29443"


def _normalize_domains(doc: DocEndpoint, report: IssueReport) -> SpecDomains:
    real = doc.domains.real
    virtual = doc.domains.virtual

    if not real or not URL_RE.match(real.strip()):
        if doc.url.startswith(("/uapi", "/oauth2")):
            report.add(
                SpecIssue(
                    IssueLevel.WARN,
                    "domain.real.inferred",
                    "Real domain inferred to default HTTP base.",
                    "domains.real",
                    doc.id,
                )
            )
            real = HTTP_REAL_DOMAIN

    if virtual and not URL_RE.match(virtual.strip()):
        report.add(
            SpecIssue(
                IssueLevel.WARN,
                "domain.virtual.placeholder",
                f"Virtual domain placeholder mapped to None: {virtual!r}",
                "domains.virtual",
                doc.id,
            )
        )
        virtual = None

    if not virtual:
        if doc.url.startswith(("/uapi", "/oauth2")) and not _virtual_disabled(doc):
            report.add(
                SpecIssue(
                    IssueLevel.WARN,
                    "domain.virtual.inferred",
                    "Virtual domain inferred to default HTTP base.",
                    "domains.virtual",
                    doc.id,
                )
            )
            virtual = HTTP_VIRTUAL_DOMAIN

    return SpecDomains(real=real, virtual=virtual)


def _virtual_disabled(doc: DocEndpoint) -> bool:
    if doc.virtual_tr_id and "미지원" in doc.virtual_tr_id:
        return True
    for tr_id in doc.tr_ids:
        if isinstance(tr_id, str) and "미지원" in tr_id:
            return True
    if doc.domains.virtual and "미지원" in doc.domains.virtual:
        return True
    return False


def _clean_tr_id(value: str | None) -> str | None:
    if not value:
        return None
    if "미지원" in value:
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


def normalize_doc(doc: DocEndpoint, source_path: str) -> tuple[EndpointSpec | None, IssueReport]:
    report = IssueReport()
    report.extend(validate_doc(doc))

    if report.has_errors():
        return None, report

    method = doc.method.upper()
    content_type = _infer_content_type(doc)
    req_format = _infer_req_format(doc, content_type)

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
        virtual_tr_id=_clean_tr_id(doc.virtual_tr_id),
        summary=doc.summary,
        description=doc.description,
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
