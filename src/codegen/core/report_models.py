from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from codegen.core.issues import IssueLevel


class IssueItem(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    level: IssueLevel
    code: str
    message: str
    path: str
    endpoint_id: str | None = None


class ParseError(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    path: str
    error: str


class ScanCounts(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    total_issues: int = 0
    errors: int = 0
    warnings: int = 0


class AugmentCounts(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    total: int = 0
    processed: int = 0
    ok: int = 0
    cached: int = 0
    skipped: int = 0
    errors: int = 0


class AugmentQualityCounts(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    total_calls: int = 0
    http_ok: int = 0


class SimpleCounts(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    total: int = 0
    errors: int = 0


class DocsSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    timestamp: str
    generated: int = 0
    scan: ScanCounts
    normalize: ScanCounts
    augment: AugmentCounts
    augment_quality: AugmentQualityCounts
    validation: SimpleCounts
    smoke: SimpleCounts


class StoreValidationSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    total_errors: int = 0
    sources: int = 0
    records: int = 0
    enum_mismatches: int = 0


class StoreSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    timestamp: str
    scan: ScanCounts
    validation: StoreValidationSummary


__all__ = [
    "AugmentCounts",
    "AugmentQualityCounts",
    "DocsSummary",
    "IssueItem",
    "ParseError",
    "ScanCounts",
    "SimpleCounts",
    "StoreSummary",
    "StoreValidationSummary",
]
