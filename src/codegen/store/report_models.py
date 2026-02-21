from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from codegen.core.report_models import IssueItem


class StoreScanReport(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    path: str
    total_issues: int = 0
    errors: int = 0
    warnings: int = 0
    issues: list[IssueItem] = Field(default_factory=list)


__all__ = ["StoreScanReport"]
