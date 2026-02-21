from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from codegen.core.types import JsonObject

HintStatus = Literal["pending_review", "no_candidates", "too_few_fields"]
InvalidHintStatus = Literal[
    "pending_review",
    "no_candidates",
    "rt_cd_error",
    "missing_success",
    "missing_probe",
    "message_error",
]


class FieldDiff(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    field: str
    success_value: str | None
    empty_value: str | None
    sentinel_type: str


class MissingFieldDiff(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    field: str
    success_value: str | None


class ComparisonResult(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    diffs: list[FieldDiff] = Field(default_factory=list)
    sentinel_ratio: float = 0.0
    total_fields: int = 0


class MissingComparisonResult(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    diffs: list[MissingFieldDiff] = Field(default_factory=list)
    missing_ratio: float = 0.0
    total_fields: int = 0


class DiscoveryHeuristics(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    min_sentinel_ratio: float
    min_fields_differ: int


class DiscoverySummary(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    heuristics_used: DiscoveryHeuristics
    results: ComparisonResult


class ValidationEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    success_sample: JsonObject = Field(default_factory=dict)
    empty_sample: JsonObject = Field(default_factory=dict)


class InvalidProbeEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    success_sample: JsonObject = Field(default_factory=dict)
    probe_sample: JsonObject = Field(default_factory=dict)


class ResponseMeta(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    rt_cd: str | None = None
    msg_cd: str | None = None
    msg1: str | None = None


class OutputSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    output: str
    present: bool
    empty: bool
    kind: str | None = None
    length: int | None = None


class MessageSignal(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    error: bool = False
    empty: bool = False
    msg_cd_matches: list[str] = Field(default_factory=list)
    msg1_error_matches: list[str] = Field(default_factory=list)
    msg1_empty_matches: list[str] = Field(default_factory=list)


class InvalidProbeHint(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    status: InvalidHintStatus
    rt_cd: str | None = None
    msg_cd: str | None = None
    msg1: str | None = None
    message_signal: MessageSignal | None = None
    rule_type: str | None = None
    output_key: str | None = None
    output_missing: bool = False
    output_empty: bool = False
    sentinel: ComparisonResult | None = None
    missing: MissingComparisonResult | None = None
    candidate_fields: list[str] = Field(default_factory=list)
    evidence: InvalidProbeEvidence | None = None


class ValidationHint(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    endpoint_id: str
    generated_at: str
    status: HintStatus
    discovery: DiscoverySummary | None = None
    candidate_fields: list[str] = Field(default_factory=list)
    evidence: ValidationEvidence | None = None
    invalid_probe: InvalidProbeHint | None = None

    @classmethod
    def now(cls, endpoint_id: str, status: HintStatus) -> ValidationHint:
        return cls(
            endpoint_id=endpoint_id,
            generated_at=datetime.now(timezone.utc).isoformat(),
            status=status,
        )


class ValidationCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    endpoint_id: str
    rule_type: str | None = None
    output: str | None = None
    status: InvalidHintStatus | None = None
    rt_cd: str | None = None
    msg_cd: str | None = None
    msg1: str | None = None
    candidate_fields: list[str] = Field(default_factory=list)
    reason: str | None = None
    output_state: OutputSnapshot | None = None
    success_meta: ResponseMeta | None = None
    probe_meta: ResponseMeta | None = None
    evidence: InvalidProbeEvidence | None = None
    invalid_template: JsonObject | None = None


__all__ = [
    "ComparisonResult",
    "DiscoveryHeuristics",
    "DiscoverySummary",
    "FieldDiff",
    "HintStatus",
    "InvalidHintStatus",
    "InvalidProbeEvidence",
    "InvalidProbeHint",
    "MissingComparisonResult",
    "MissingFieldDiff",
    "OutputSnapshot",
    "ResponseMeta",
    "MessageSignal",
    "ValidationCandidate",
    "ValidationEvidence",
    "ValidationHint",
]
