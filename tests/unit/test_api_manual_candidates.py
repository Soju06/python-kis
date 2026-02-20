from __future__ import annotations

from codegen.api.models import EndpointSpec
from codegen.api.report_models import SmokeReport, SmokeResult
from codegen.api.steps.manual_candidates import (
    build_enum_manual_review_candidates,
    build_enum_manual_review_priority,
    render_enum_manual_review_candidates_markdown,
    render_enum_manual_review_priority_markdown,
)
from codegen.api.types import EndpointHints, FieldHint, TypeOverrides


def _build_output_spec() -> EndpointSpec:
    return EndpointSpec.model_validate(
        {
            "id": "manual-candidate-output",
            "name": "manual candidate output endpoint",
            "section": "test",
            "category": "test",
            "subcategory": "test",
            "method": "GET",
            "path": "/uapi/test/v1/output",
            "domains": {"real": "Y", "demo": "Y"},
            "request": {"headers": [], "query": [], "body": []},
            "response": {
                "headers": [],
                "body": [],
                "outputs": [
                    {
                        "code": "output1",
                        "name": "output1",
                        "kind": "single",
                        "fields": [
                            {
                                "code": "new_mkop_cls_code",
                                "name": "신 장운영 구분 코드",
                                "type": "A0001",
                                "type_name": "String",
                                "length": "2",
                                "required": True,
                                "description": "(1) 첫 번째 비트 / (2) 두 번째 비트",
                            }
                        ],
                    }
                ],
            },
            "errors": [],
            "source_path": "tmp/docs/normalized/test/output.json",
        }
    )


def _build_request_spec() -> EndpointSpec:
    return EndpointSpec.model_validate(
        {
            "id": "manual-candidate-request",
            "name": "manual candidate request endpoint",
            "section": "test",
            "category": "test",
            "subcategory": "test",
            "method": "GET",
            "path": "/uapi/test/v1/request",
            "domains": {"real": "Y", "demo": "Y"},
            "request": {
                "headers": [],
                "query": [
                    {
                        "code": "fid_prc_cls_code",
                        "name": "가격 구분 코드",
                        "type": "A0001",
                        "type_name": "String",
                        "length": "2",
                        "required": True,
                        "description": "0 또는 1",
                    },
                    {
                        "code": "FM_EXCG_CD",
                        "name": "해외거래소코드",
                        "type": "A0001",
                        "type_name": "String",
                        "length": "10",
                        "required": True,
                        "description": "CME, EUREX, HKEx",
                    },
                ],
                "body": [],
            },
            "response": {"headers": [], "body": [], "outputs": []},
            "errors": [],
            "source_path": "tmp/docs/normalized/test/request.json",
        }
    )


def test_manual_candidates_detect_output_parser_token(tmp_path) -> None:
    spec = _build_output_spec()
    inference = TypeOverrides(
        endpoints={
            spec.id: EndpointHints(
                outputs={
                    "output1": {
                        "new_mkop_cls_code": FieldHint(kind="enum", enum=["00", "49", "Buy", "in", "20"])
                    }
                }
            )
        }
    )
    smoke = SmokeReport(total=2, errors=2, results=[SmokeResult(id=spec.id, status="error", domain="real", attempt=1)])

    report = build_enum_manual_review_candidates([spec], inference, smoke, augment_dir=tmp_path)

    assert report.endpoints == 1
    assert report.total_fields == 1
    candidate = report.candidates[0]
    assert candidate.endpoint_id == spec.id
    assert candidate.smoke_status == "error"
    field = candidate.fields[0]
    assert field.field_code == "new_mkop_cls_code"
    assert field.suspicious_values == ["Buy", "in"]
    assert field.confidence == "high"


def test_manual_candidates_keep_whitelisted_mixed_case_values(tmp_path) -> None:
    spec = _build_request_spec()
    inference = TypeOverrides(
        endpoints={
            spec.id: EndpointHints(
                request={
                    "fid_prc_cls_code": FieldHint(kind="enum", enum=["0", "1", "code"]),
                    "FM_EXCG_CD": FieldHint(kind="enum", enum=["CME", "EUREX", "HKEx"]),
                }
            )
        }
    )
    smoke = SmokeReport(total=2, errors=0, results=[SmokeResult(id=spec.id, status="ok", domain="real", attempt=1)])

    report = build_enum_manual_review_candidates([spec], inference, smoke, augment_dir=tmp_path)

    assert report.endpoints == 1
    assert report.total_fields == 1
    field = report.candidates[0].fields[0]
    assert field.field_code == "fid_prc_cls_code"
    assert field.suspicious_values == ["code"]
    assert field.confidence == "high"

    markdown = render_enum_manual_review_candidates_markdown(report)
    assert "# Enum Parser Manual Review Candidates" in markdown
    assert "manual-candidate-request" in markdown


def test_manual_priority_splits_parser_fix_and_override_review(tmp_path) -> None:
    spec = _build_request_spec()
    inference = TypeOverrides(
        endpoints={
            spec.id: EndpointHints(
                request={
                    "fid_prc_cls_code": FieldHint(kind="enum", enum=["0", "1", "code"]),
                    "FM_EXCG_CD": FieldHint(kind="enum", enum=["CME", "LONGVALUE11"]),
                }
            )
        }
    )
    smoke = SmokeReport(total=2, errors=0, results=[SmokeResult(id=spec.id, status="ok", domain="real", attempt=1)])

    report = build_enum_manual_review_candidates([spec], inference, smoke, augment_dir=tmp_path)
    priority = build_enum_manual_review_priority(
        report,
        source_report_path="tmp/docs/reports/manual_enum_review_candidates.json",
    )

    summary_value = priority.get("summary")
    assert isinstance(summary_value, dict)
    assert summary_value.get("ready_endpoints") == 0
    assert summary_value.get("hold_endpoints") == 1
    assert summary_value.get("parser_fix_fields") == 1
    assert summary_value.get("override_review_fields") == 1

    hold_value = priority.get("hold")
    assert isinstance(hold_value, list)
    assert len(hold_value) == 1
    hold_item = hold_value[0]
    assert isinstance(hold_item, dict)
    ready_fields_value = hold_item.get("ready_fields")
    hold_fields_value = hold_item.get("hold_fields")
    assert isinstance(ready_fields_value, list)
    assert isinstance(hold_fields_value, list)
    assert len(ready_fields_value) == 1
    assert len(hold_fields_value) == 1
    assert ready_fields_value[0].get("decision") == "parser_fix"
    assert hold_fields_value[0].get("decision") == "override_review"

    markdown = render_enum_manual_review_priority_markdown(priority)
    assert "# Enum Parser Review Priority" in markdown
    assert "## Hold (override 검토)" in markdown
