from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from codegen.core.types import JsonObject

HintStatus = Literal["pending_review", "no_candidates", "too_few_fields"]


class FieldDiff(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    field: str
    success_value: str | None
    empty_value: str | None
    sentinel_type: str


class ComparisonResult(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    diffs: list[FieldDiff] = Field(default_factory=list)
    sentinel_ratio: float = 0.0
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


class ValidationHint(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    endpoint_id: str
    generated_at: str
    status: HintStatus
    discovery: DiscoverySummary | None = None
    candidate_fields: list[str] = Field(default_factory=list)
    evidence: ValidationEvidence | None = None
    suggested_yaml: str | None = None

    @classmethod
    def now(cls, endpoint_id: str, status: HintStatus) -> ValidationHint:
        return cls(
            endpoint_id=endpoint_id,
            generated_at=datetime.now(timezone.utc).isoformat(),
            status=status,
        )


__all__ = [
    "ComparisonResult",
    "DiscoveryHeuristics",
    "DiscoverySummary",
    "FieldDiff",
    "HintStatus",
    "ValidationEvidence",
    "ValidationHint",
]
