from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class IssueLevel(str, Enum):
    ERROR = "error"
    WARN = "warn"


@dataclass(frozen=True, slots=True)
class SpecIssue:
    level: IssueLevel
    code: str
    message: str
    path: str
    endpoint_id: str | None = None


class IssueReport:
    issues: list[SpecIssue]

    __slots__ = ("issues",)

    def __init__(self) -> None:
        self.issues: list[SpecIssue] = []

    def add(self, issue: SpecIssue) -> None:
        self.issues.append(issue)

    def extend(self, issues: Iterable[SpecIssue]) -> None:
        self.issues.extend(issues)

    def has_errors(self) -> bool:
        return any(issue.level == IssueLevel.ERROR for issue in self.issues)

    def counts(self) -> dict[str, int]:
        counts = {IssueLevel.ERROR.value: 0, IssueLevel.WARN.value: 0}
        for issue in self.issues:
            counts[issue.level.value] += 1
        return counts
