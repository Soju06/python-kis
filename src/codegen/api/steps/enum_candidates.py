from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from codegen.api.models import EndpointSpec, SpecField
from codegen.api.report_models import EnumDriftCandidate, EnumDriftCandidateReport
from codegen.core.types import JsonObject, JsonValue


def _as_object(value: JsonValue | None) -> JsonObject | None:
    if isinstance(value, dict):
        return {str(key): item for key, item in value.items()}
    return None


def _as_text_list(value: JsonValue | None) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    seen: set[str] = set()
    for item in value:
        text = str(item).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def _append_unique(target: list[str], values: list[str]) -> None:
    for value in values:
        if value not in target:
            target.append(value)


def _build_candidate(
    spec: EndpointSpec,
    field: SpecField,
    field_trace: JsonObject,
    *,
    location: str,
    output: str | None,
    augment_dir: Path,
) -> EnumDriftCandidate | None:
    decision = _as_object(field_trace.get("decision")) or {}
    decision_kind = str(decision.get("kind") or "").strip().lower()
    if decision_kind != "enum":
        return None

    enum_info = _as_object(field_trace.get("enum"))
    if enum_info is None:
        return None

    unknown_values = _as_text_list(enum_info.get("unknown_sample_values"))
    if not unknown_values:
        return None

    documented_values = _as_text_list(enum_info.get("documented_values"))
    if not documented_values:
        documented_values = _as_text_list(enum_info.get("values"))
    observed_values = _as_text_list(enum_info.get("sample_values"))
    proposed_values = list(documented_values)
    _append_unique(proposed_values, unknown_values)

    endpoint_dir = augment_dir / spec.id
    field_path = f"outputs.{output}.{field.code}" if output else f"{location}.{field.code}"
    evidence: JsonObject = {
        "field_path": field_path,
        "request_path": str(endpoint_dir / "request.json"),
        "raw_path": str(endpoint_dir / "raw.json"),
    }

    return EnumDriftCandidate(
        endpoint_id=spec.id,
        endpoint_name=spec.name,
        path=spec.path,
        source_path=spec.source_path,
        location=location,
        output=output,
        field_code=field.code,
        field_name=field.name or field.code,
        inference_kind=str(decision.get("kind")) if decision.get("kind") is not None else None,
        inference_reason=str(decision.get("reason")) if decision.get("reason") is not None else None,
        documented_values=documented_values,
        observed_values=observed_values,
        unknown_values=unknown_values,
        proposed_values=proposed_values,
        evidence=evidence,
    )


def build_enum_drift_candidates(
    specs: list[EndpointSpec],
    inference_trace: dict[str, JsonObject],
    augment_dir: Path,
) -> EnumDriftCandidateReport:
    candidates: list[EnumDriftCandidate] = []
    for spec in specs:
        trace_entry = _as_object(inference_trace.get(spec.id))
        if trace_entry is None:
            continue

        request_trace = _as_object(trace_entry.get("request")) or {}
        response_trace = _as_object(trace_entry.get("response")) or {}
        outputs_trace = _as_object(trace_entry.get("outputs")) or {}

        for field in spec.request.query:
            field_trace = _as_object(request_trace.get(field.code))
            if field_trace is None:
                continue
            candidate = _build_candidate(
                spec,
                field,
                field_trace,
                location="request.query",
                output=None,
                augment_dir=augment_dir,
            )
            if candidate is not None:
                candidates.append(candidate)

        for field in spec.request.body:
            field_trace = _as_object(request_trace.get(field.code))
            if field_trace is None:
                continue
            candidate = _build_candidate(
                spec,
                field,
                field_trace,
                location="request.body",
                output=None,
                augment_dir=augment_dir,
            )
            if candidate is not None:
                candidates.append(candidate)

        for field in spec.response.body:
            field_trace = _as_object(response_trace.get(field.code))
            if field_trace is None:
                continue
            candidate = _build_candidate(
                spec,
                field,
                field_trace,
                location="response.body",
                output=None,
                augment_dir=augment_dir,
            )
            if candidate is not None:
                candidates.append(candidate)

        for output in spec.response.outputs:
            output_trace = _as_object(outputs_trace.get(output.code)) or {}
            for field in output.fields:
                field_trace = _as_object(output_trace.get(field.code))
                if field_trace is None:
                    continue
                candidate = _build_candidate(
                    spec,
                    field,
                    field_trace,
                    location="response.output",
                    output=output.code,
                    augment_dir=augment_dir,
                )
                if candidate is not None:
                    candidates.append(candidate)

    candidates.sort(key=lambda item: (item.endpoint_id, item.location, item.output or "", item.field_code))
    by_location = dict(Counter(candidate.location for candidate in candidates))
    endpoint_count = len({candidate.endpoint_id for candidate in candidates})
    return EnumDriftCandidateReport(
        generated_at=datetime.now(timezone.utc).isoformat(),
        total=len(candidates),
        endpoints=endpoint_count,
        by_location=by_location,
        candidates=candidates,
    )


__all__ = ["build_enum_drift_candidates"]
