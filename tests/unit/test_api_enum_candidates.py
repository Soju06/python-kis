from __future__ import annotations

import json

from codegen.api.models import EndpointSpec
from codegen.api.steps.enum_candidates import build_enum_drift_candidates
from codegen.api.steps.infer import infer_types
from codegen.core.types import JsonObject


def _build_spec() -> EndpointSpec:
    return EndpointSpec.model_validate(
        {
            "id": "enum-candidate-test",
            "name": "enum candidate endpoint",
            "section": "test",
            "category": "test",
            "subcategory": "test",
            "method": "GET",
            "path": "/uapi/test/v1/example",
            "domains": {"real": "Y", "demo": "Y"},
            "request": {
                "headers": [],
                "query": [
                    {
                        "code": "FID_COND_MRKT_DIV_CODE",
                        "name": "조건 시장 분류 코드",
                        "type": "A0001",
                        "type_name": "String",
                        "required": True,
                        "description": "KRX:한국거래소, NXT:넥스트트레이드",
                    }
                ],
                "body": [],
            },
            "response": {"headers": [], "body": [], "outputs": []},
            "errors": [],
            "source_path": "docs/kis/test/example.yaml",
        }
    )


def test_enum_unknown_value_keeps_enum_and_generates_candidate(tmp_path) -> None:
    spec = _build_spec()
    endpoint_dir = tmp_path / spec.id
    endpoint_dir.mkdir(parents=True)
    (endpoint_dir / "request.json").write_text(
        json.dumps({"query": {"FID_COND_MRKT_DIV_CODE": "J"}, "body": {}}, ensure_ascii=False),
        encoding="utf-8",
    )

    trace_out: dict[str, JsonObject] = {}
    inferred = infer_types([spec], tmp_path, trace_out=trace_out)
    request_hint = inferred.endpoints[spec.id].request["FID_COND_MRKT_DIV_CODE"]
    assert request_hint.kind == "enum"
    assert request_hint.enum is not None
    assert "J" in request_hint.enum

    report = build_enum_drift_candidates([spec], trace_out, tmp_path)
    assert report.total == 1
    candidate = report.candidates[0]
    assert candidate.endpoint_id == spec.id
    assert candidate.location == "request.query"
    assert candidate.field_code == "FID_COND_MRKT_DIV_CODE"
    assert candidate.unknown_values == ["J"]
    assert "J" in candidate.proposed_values
