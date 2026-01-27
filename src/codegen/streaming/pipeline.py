from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from codegen.core.issues import IssueLevel, IssueReport, SpecIssue
from codegen.core.paths import project_root
from codegen.core.report_models import IssueItem, ParseError
from codegen.streaming.steps.generate import generate_streaming_raw
from codegen.streaming.steps.io import SpecError, load_streaming_spec
from codegen.streaming.steps.validate import validate_spec

ROOT = project_root()
REPORT_DIR = ROOT / "tmp" / "docs" / "reports"
DEFAULT_SPEC_PATH = REPORT_DIR / "streaming_fieldspec_draft.yaml"
DEFAULT_OUTPUT_DIR = ROOT / "src" / "pykis" / "streaming" / "raw" / "structs"


def run_pipeline(
    spec_path: Path | None = None,
    output_dir: Path | None = None,
) -> int:
    target_spec = spec_path or DEFAULT_SPEC_PATH
    target_output = output_dir or DEFAULT_OUTPUT_DIR
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    issues: list[SpecIssue] = []
    parse_errors: list[dict[str, str]] = []
    try:
        spec = load_streaming_spec(target_spec)
    except (SpecError, OSError) as exc:
        parse_errors.append({"path": str(target_spec), "error": str(exc)})
        issues.append(
            SpecIssue(
                IssueLevel.ERROR,
                "parse.error",
                f"Failed to parse streaming spec: {exc}",
                str(target_spec),
                None,
            )
        )
        spec = None

    if spec is not None:
        issues.extend(validate_spec(spec))

    report_path = REPORT_DIR / "streaming_codegen_report.json"
    _write_report(report_path, issues, parse_errors)

    report = IssueReport()
    report.extend(issues)
    if report.has_errors():
        raise SystemExit(f"Streaming spec validation failed. See {report_path}.")

    if spec is None:
        raise SystemExit(f"Streaming spec missing. See {report_path}.")

    return generate_streaming_raw(spec, target_output)


def _write_report(path: Path, issues: list[SpecIssue], parse_errors: list[dict[str, str]]) -> None:
    report = IssueReport()
    report.extend(issues)
    counts = report.counts()
    issue_items = [IssueItem.model_validate(asdict(issue)) for issue in issues]
    error_items = [ParseError.model_validate(item) for item in parse_errors]
    payload = {
        "total_issues": len(issues),
        "errors": counts[IssueLevel.ERROR.value],
        "warnings": counts[IssueLevel.WARN.value],
        "issues": [item.model_dump() for item in issue_items],
        "parse_errors": [item.model_dump() for item in error_items],
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
