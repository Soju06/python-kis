from __future__ import annotations

from codegen.api.report_models import EnumDriftCandidate, EnumDriftCandidateReport
from codegen.api.steps.override_candidates import (
    build_enum_type_override_candidates,
    build_enum_type_override_priority,
    render_enum_type_override_candidates_markdown,
    render_enum_type_override_priority_markdown,
)
from codegen.api.types import EndpointHints, FieldHint, TypeOverrides


def _candidate(
    *,
    endpoint_id: str,
    endpoint_name: str,
    path: str,
    source_path: str,
    location: str,
    output: str | None,
    field_code: str,
    proposed_values: list[str],
    unknown_values: list[str],
) -> EnumDriftCandidate:
    return EnumDriftCandidate(
        endpoint_id=endpoint_id,
        endpoint_name=endpoint_name,
        path=path,
        source_path=source_path,
        location=location,
        output=output,
        field_code=field_code,
        field_name=field_code,
        inference_kind="enum",
        inference_reason="enum_preferred",
        documented_values=proposed_values[:-1] if len(proposed_values) > 1 else proposed_values,
        observed_values=proposed_values,
        unknown_values=unknown_values,
        proposed_values=proposed_values,
        evidence={
            "field_path": f"{location}.{field_code}",
            "raw_path": f"tmp/docs/augment/{endpoint_id}/raw.json",
            "request_path": f"tmp/docs/augment/{endpoint_id}/request.json",
        },
    )


def test_build_enum_type_override_candidates_merges_endpoint_changes() -> None:
    report = EnumDriftCandidateReport(
        generated_at="2026-02-12T00:00:00+00:00",
        total=4,
        endpoints=2,
        by_location={"response.output": 3, "request.query": 1},
        candidates=[
            _candidate(
                endpoint_id="endpoint-a",
                endpoint_name="endpoint A",
                path="/uapi/a",
                source_path="docs/a.yaml",
                location="response.output",
                output="output",
                field_code="news_code",
                proposed_values=["01", "02", "03"],
                unknown_values=["03"],
            ),
            _candidate(
                endpoint_id="endpoint-a",
                endpoint_name="endpoint A",
                path="/uapi/a",
                source_path="docs/a.yaml",
                location="response.output",
                output="output",
                field_code="news_code",
                proposed_values=["01", "02", "03", "04"],
                unknown_values=["04"],
            ),
            _candidate(
                endpoint_id="endpoint-a",
                endpoint_name="endpoint A",
                path="/uapi/a",
                source_path="docs/a.yaml",
                location="request.query",
                output=None,
                field_code="FID_COND_MRKT_DIV_CODE",
                proposed_values=["KRX", "NXT", "J"],
                unknown_values=["J"],
            ),
            _candidate(
                endpoint_id="endpoint-b",
                endpoint_name="endpoint B",
                path="/uapi/b",
                source_path="docs/b.yaml",
                location="response.output",
                output="output1",
                field_code="country_code",
                proposed_values=["US", "JP", "GB"],
                unknown_values=["GB"],
            ),
        ],
    )

    payload = build_enum_type_override_candidates(
        report,
        source_report_path="tmp/docs/reports/enum_drift_candidates.json",
    )

    summary_value = payload.get("summary")
    assert isinstance(summary_value, dict)
    summary = summary_value
    assert summary["draft_overrides"] == 2
    overrides_value = payload.get("overrides")
    assert isinstance(overrides_value, list)
    overrides = [item for item in overrides_value if isinstance(item, dict)]
    assert len(overrides) == 2

    endpoint_a = next(item for item in overrides if item.get("id") == "endpoint-a")
    changes_value = endpoint_a.get("changes")
    assert isinstance(changes_value, dict)
    outputs_value = changes_value.get("outputs")
    request_value = changes_value.get("request")
    assert isinstance(outputs_value, dict)
    assert isinstance(request_value, dict)
    output_value = outputs_value.get("output")
    request_field_value = request_value.get("FID_COND_MRKT_DIV_CODE")
    assert isinstance(output_value, dict)
    assert isinstance(request_field_value, dict)
    news_code_value = output_value.get("news_code")
    assert isinstance(news_code_value, dict)
    assert news_code_value.get("enum") == ["01", "02", "03", "04"]
    assert request_field_value.get("enum") == ["KRX", "NXT", "J"]
    review_value = endpoint_a.get("review")
    assert isinstance(review_value, list)
    assert len(review_value) == 3

    markdown = render_enum_type_override_candidates_markdown(payload)
    assert "# Enum Type Override Draft Candidates" in markdown
    assert "## endpoint-a" in markdown


def test_build_enum_type_override_priority_splits_ready_and_hold() -> None:
    report = EnumDriftCandidateReport(
        generated_at="2026-02-12T00:00:00+00:00",
        total=3,
        endpoints=3,
        by_location={"response.output": 2, "request.query": 1},
        candidates=[
            _candidate(
                endpoint_id="ready-endpoint",
                endpoint_name="ready endpoint",
                path="/uapi/ready",
                source_path="docs/ready.yaml",
                location="response.output",
                output="output",
                field_code="flng_cls_code",
                proposed_values=["01", "02", "00"],
                unknown_values=["00"],
            ),
            _candidate(
                endpoint_id="hold-request",
                endpoint_name="hold request endpoint",
                path="/uapi/hold-request",
                source_path="docs/hold-request.yaml",
                location="request.query",
                output=None,
                field_code="FID_COND_MRKT_DIV_CODE",
                proposed_values=["KRX", "NXT", "J"],
                unknown_values=["J"],
            ),
            _candidate(
                endpoint_id="hold-parser",
                endpoint_name="hold parser endpoint",
                path="/uapi/hold-parser",
                source_path="docs/hold-parser.yaml",
                location="response.output",
                output="output1",
                field_code="price_value",
                proposed_values=["4", "16", "0.00"],
                unknown_values=["0.00"],
            ),
        ],
    )
    draft = build_enum_type_override_candidates(
        report,
        source_report_path="tmp/docs/reports/enum_drift_candidates.json",
    )
    priority = build_enum_type_override_priority(draft)

    summary_value = priority.get("summary")
    assert isinstance(summary_value, dict)
    assert summary_value.get("ready_overrides") == 1
    assert summary_value.get("hold_overrides") == 2

    ready_value = priority.get("ready")
    hold_value = priority.get("hold")
    assert isinstance(ready_value, list)
    assert isinstance(hold_value, list)
    assert any(isinstance(item, dict) and item.get("id") == "ready-endpoint" for item in ready_value)
    assert any(isinstance(item, dict) and item.get("id") == "hold-request" for item in hold_value)
    assert any(isinstance(item, dict) and item.get("id") == "hold-parser" for item in hold_value)

    markdown = render_enum_type_override_priority_markdown(priority)
    assert "# Enum Override Priority Review" in markdown
    assert "## Ready (승인 우선)" in markdown
    assert "## Hold (추가 검토)" in markdown


def test_build_enum_type_override_candidates_skips_covered_candidates() -> None:
    report = EnumDriftCandidateReport(
        generated_at="2026-02-12T00:00:00+00:00",
        total=2,
        endpoints=2,
        by_location={"response.output": 2},
        candidates=[
            _candidate(
                endpoint_id="endpoint-a",
                endpoint_name="endpoint A",
                path="/uapi/a",
                source_path="docs/a.yaml",
                location="response.output",
                output="output",
                field_code="news_code",
                proposed_values=["01", "02", "03", "04"],
                unknown_values=["04"],
            ),
            _candidate(
                endpoint_id="endpoint-b",
                endpoint_name="endpoint B",
                path="/uapi/b",
                source_path="docs/b.yaml",
                location="response.output",
                output="output1",
                field_code="country_code",
                proposed_values=["US", "JP", "GB"],
                unknown_values=["GB"],
            ),
        ],
    )
    applied_overrides = TypeOverrides(
        endpoints={
            "endpoint-a": EndpointHints(
                outputs={
                    "output": {
                        "news_code": FieldHint(enum=["01", "02", "03", "04"]),
                    }
                }
            )
        }
    )

    payload = build_enum_type_override_candidates(
        report,
        source_report_path="tmp/docs/reports/enum_drift_candidates.json",
        applied_overrides=applied_overrides,
    )

    summary_value = payload.get("summary")
    assert isinstance(summary_value, dict)
    assert summary_value.get("covered_by_existing_overrides") == 1
    assert summary_value.get("pending_candidates") == 1
    assert summary_value.get("draft_overrides") == 1

    overrides_value = payload.get("overrides")
    assert isinstance(overrides_value, list)
    overrides = [item for item in overrides_value if isinstance(item, dict)]
    assert len(overrides) == 1
    assert overrides[0].get("id") == "endpoint-b"
