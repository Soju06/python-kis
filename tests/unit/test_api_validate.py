from __future__ import annotations

from codegen.api.models import DocEndpoint
from codegen.api.steps.validate import validate_doc


def _field(code: str, *, description: str = "") -> dict[str, object]:
    return {
        "code": code,
        "name": code,
        "type": "A0001",
        "type_name": "String",
        "length": "10",
        "required": True,
        "description": description,
    }


def _doc_with_fields(*, request_body: list[dict[str, object]], response_body: list[dict[str, object]]) -> DocEndpoint:
    return DocEndpoint.model_validate(
        {
            "id": "validate-agg-test",
            "name": "validate aggregation endpoint",
            "section": "test",
            "category": "test",
            "subcategory": "test",
            "method": "POST",
            "url": "/uapi/test/v1/validate",
            "content_type": "application/json",
            "req_format": "JSON",
            "domains": {"real": "https://example.com", "demo": None},
            "request": {
                "headers": [],
                "params": [],
                "body": request_body,
                "example": None,
            },
            "response": {
                "headers": [],
                "body": response_body,
                "example": None,
            },
            "errors": [],
        }
    )


def test_validate_doc_aggregates_missing_description_warnings() -> None:
    doc = _doc_with_fields(
        request_body=[_field("REQ1"), _field("REQ2"), _field("REQ_OK", description="ok")],
        response_body=[_field("RES1"), _field("RES2"), _field("RES3")],
    )

    issues = validate_doc(doc)
    request_issues = [issue for issue in issues if issue.code == "request.body.description.missing"]
    response_issues = [issue for issue in issues if issue.code == "response.body.description.missing"]

    assert len(request_issues) == 1
    assert request_issues[0].path == "request.body"
    assert "2 fields" in request_issues[0].message
    assert "REQ1, REQ2" in request_issues[0].message

    assert len(response_issues) == 1
    assert response_issues[0].path == "response.body"
    assert "3 fields" in response_issues[0].message
    assert "RES1, RES2, RES3" in response_issues[0].message


def test_validate_doc_missing_description_preview_is_truncated() -> None:
    missing_fields = [_field(f"RES{i}") for i in range(1, 8)]
    doc = _doc_with_fields(request_body=[], response_body=missing_fields)

    issues = validate_doc(doc)
    response_issue = next(issue for issue in issues if issue.code == "response.body.description.missing")

    assert "7 fields" in response_issue.message
    assert "RES1, RES2, RES3, RES4, RES5, … (+2)" in response_issue.message
