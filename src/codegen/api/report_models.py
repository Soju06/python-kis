from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from codegen.api.types import TypeOverrides
from codegen.core.report_models import IssueItem, ParseError
from codegen.core.types import JsonObject

AugmentStatus = Literal["ok", "cached", "skipped", "error"]


class ScanReport(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    total_issues: int = 0
    errors: int = 0
    warnings: int = 0
    issues: list[IssueItem] = Field(default_factory=list)
    parse_errors: list[ParseError] = Field(default_factory=list)


class AugmentRequestPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    method: str
    url: str
    headers: dict[str, str]
    query: JsonObject
    body: JsonObject


class AugmentMeta(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    status_code: int
    ok: bool
    domain: str
    endpoint: str
    missing_required: list[str] = Field(default_factory=list)
    fingerprint: str
    empty: bool | None = None
    scenario: str | None = None
    request_template: str | None = None
    expected: str | None = None


class AugmentEndpointResult(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str
    status: AugmentStatus
    status_code: int | None = None
    reason: str | None = None
    note: str | None = None
    scenario: str | None = None


class AugmentSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    total: int = 0
    processed: int = 0
    ok: int = 0
    cached: int = 0
    skipped: int = 0
    errors: int = 0
    results: list[AugmentEndpointResult] = Field(default_factory=list)


class ScenarioResult(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    endpoint_id: str
    scenario: str
    status: AugmentStatus
    status_code: int | None = None
    reason: str | None = None
    note: str | None = None


class MultiScenarioReport(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    total: int = 0
    processed: int = 0
    ok: int = 0
    cached: int = 0
    skipped: int = 0
    errors: int = 0
    results: list[ScenarioResult] = Field(default_factory=list)


class AugmentQualityReport(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    total_calls: int = 0
    http_ok: int = 0
    status_codes_top: list[tuple[str, int]] = Field(default_factory=list)
    rt_cd_top: list[tuple[str, int]] = Field(default_factory=list)
    msg_cd_top: list[tuple[str, int]] = Field(default_factory=list)
    missing_required_top: list[tuple[str, int]] = Field(default_factory=list)


class ValidationSampleResult(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str
    status: str
    domain: str | None = None
    reason: str | None = None


class ValidationReport(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    total: int = 0
    errors: int = 0
    results: list[ValidationSampleResult] = Field(default_factory=list)


class SmokeResult(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str
    status: str
    domain: str | None = None
    attempt: int | None = None
    reason: str | None = None
    status_code: int | None = None


class SmokeReport(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    total: int = 0
    errors: int = 0
    results: list[SmokeResult] = Field(default_factory=list)


class ApiPipelineReport(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    scan: ScanReport
    normalize: ScanReport
    sample: AugmentSummary
    augment: AugmentSummary
    augment_multi_sample: MultiScenarioReport | None = None
    augment_multi: MultiScenarioReport | None = None
    augment_quality_sample: AugmentQualityReport
    augment_quality: AugmentQualityReport
    inference_sample: TypeOverrides
    inference: TypeOverrides
    validation: ValidationReport
    smoke: SmokeReport
    generated: int = 0


__all__ = [
    "ApiPipelineReport",
    "AugmentEndpointResult",
    "AugmentMeta",
    "AugmentQualityReport",
    "AugmentRequestPayload",
    "AugmentSummary",
    "MultiScenarioReport",
    "ScanReport",
    "ScenarioResult",
    "SmokeReport",
    "SmokeResult",
    "ValidationReport",
    "ValidationSampleResult",
]
