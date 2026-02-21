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
            "source_path": "data/kis/test/example.yaml",
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


def test_enum_candidate_requires_enum_decision_kind(tmp_path) -> None:
    spec = _build_spec()
    endpoint_dir = tmp_path / spec.id
    endpoint_dir.mkdir(parents=True)
    (endpoint_dir / "request.json").write_text(
        json.dumps({"query": {"FID_COND_MRKT_DIV_CODE": "J"}, "body": {}}, ensure_ascii=False),
        encoding="utf-8",
    )

    trace_out: dict[str, JsonObject] = {
        spec.id: {
            "request": {
                "FID_COND_MRKT_DIV_CODE": {
                    "enum": {
                        "values": ["KRX", "NXT"],
                        "documented_values": ["KRX", "NXT"],
                        "sample_values": ["J"],
                        "unknown_sample_values": ["J"],
                    },
                    "decision": {"kind": "decimal", "reason": "sample_decimal_str"},
                }
            },
            "response": {},
            "outputs": {},
        }
    }

    report = build_enum_drift_candidates([spec], trace_out, tmp_path)
    assert report.total == 0


def test_infer_enum_ignores_length_exceeding_description_tokens(tmp_path) -> None:
    spec = EndpointSpec.model_validate(
        {
            "id": "enum-candidate-length-filter",
            "name": "enum length filter endpoint",
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
                        "code": "ORD_GNO_BRNO",
                        "name": "주문채번지점번호",
                        "type": "A0001",
                        "type_name": "String",
                        "length": "5",
                        "required": True,
                        "description": "TTS6058R 조회 시 해당 주문번호(odno)의 ord_gno_brno 입력",
                    }
                ],
                "body": [],
            },
            "response": {"headers": [], "body": [], "outputs": []},
            "errors": [],
            "source_path": "data/kis/test/example.yaml",
        }
    )
    endpoint_dir = tmp_path / spec.id
    endpoint_dir.mkdir(parents=True)
    (endpoint_dir / "request.json").write_text(
        json.dumps({"query": {"ORD_GNO_BRNO": ""}, "body": {}}, ensure_ascii=False),
        encoding="utf-8",
    )

    inferred = infer_types([spec], tmp_path)
    request_hint = inferred.endpoints[spec.id].request["ORD_GNO_BRNO"]
    assert request_hint.kind == "str"
    assert request_hint.enum is None


def test_infer_binary_mask_request_field_stays_str_and_skips_drift(tmp_path) -> None:
    spec = EndpointSpec.model_validate(
        {
            "id": "enum-candidate-binary-mask",
            "name": "enum binary mask endpoint",
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
                        "code": "FID_TRGT_CLS_CODE",
                        "name": "대상 구분 코드",
                        "type": "A0001",
                        "type_name": "String",
                        "length": "32",
                        "required": True,
                        "description": (
                            "1 or 0 9자리 (차례대로 증거금 30% 40% 50% 60% 100% 신용보증금 30% 40% 50% 60%)\n"
                            'ex) "111111111"'
                        ),
                    }
                ],
                "body": [],
            },
            "response": {"headers": [], "body": [], "outputs": []},
            "errors": [],
            "source_path": "data/kis/test/example.yaml",
        }
    )
    endpoint_dir = tmp_path / spec.id
    endpoint_dir.mkdir(parents=True)
    (endpoint_dir / "request.json").write_text(
        json.dumps({"query": {"FID_TRGT_CLS_CODE": "111111111"}, "body": {}}, ensure_ascii=False),
        encoding="utf-8",
    )

    trace_out: dict[str, JsonObject] = {}
    inferred = infer_types([spec], tmp_path, trace_out=trace_out)
    request_hint = inferred.endpoints[spec.id].request["FID_TRGT_CLS_CODE"]
    assert request_hint.kind == "str"
    assert request_hint.enum is None

    report = build_enum_drift_candidates([spec], trace_out, tmp_path)
    assert report.total == 0
