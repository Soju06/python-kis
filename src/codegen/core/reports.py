from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel

from codegen.core.render import render_template
from codegen.core.report_models import (
    AugmentCounts,
    AugmentQualityCounts,
    DocsSummary,
    ScanCounts,
    SimpleCounts,
    StoreSummary,
    StoreValidationSummary,
)


def _load_json(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def _as_str_object_map(value: object | None) -> dict[str, object] | None:
    if not isinstance(value, dict):
        return None
    return {str(key): item for key, item in value.items()}


def _iso_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _pick(report: dict[str, object] | None, keys: tuple[str, ...]) -> dict[str, int]:
    if not isinstance(report, dict):
        return {key: 0 for key in keys}
    result: dict[str, int] = {}
    for key in keys:
        value = report.get(key, 0)
        result[key] = int(value) if isinstance(value, (int, float, str)) and str(value).strip() else 0
    return result


def _write_summary(
    report_dir: Path,
    report: BaseModel | dict[str, object],
    template_name: str,
    **context: object,
) -> None:
    payload = report.model_dump() if isinstance(report, BaseModel) else report
    (report_dir / "summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    markdown = render_template(template_name, **context)
    (report_dir / "summary.md").write_text(markdown, encoding="utf-8")


def write_docs_summary(report_dir: Path) -> DocsSummary | dict[str, object]:
    pipeline = _load_json(report_dir / "pipeline.json")
    if not pipeline:
        return {}

    scan = _as_str_object_map(pipeline.get("scan"))
    normalize = _as_str_object_map(pipeline.get("normalize"))
    augment = _as_str_object_map(pipeline.get("augment"))
    augment_quality = _as_str_object_map(pipeline.get("augment_quality"))
    validation = _as_str_object_map(pipeline.get("validation"))
    smoke = _as_str_object_map(pipeline.get("smoke"))

    scan_counts = ScanCounts(**_pick(scan, ("total_issues", "errors", "warnings")))
    normalize_counts = ScanCounts(**_pick(normalize, ("total_issues", "errors", "warnings")))
    augment_counts = AugmentCounts(**_pick(augment, ("total", "processed", "ok", "cached", "skipped", "errors")))
    augment_quality_counts = AugmentQualityCounts(**_pick(augment_quality, ("total_calls", "http_ok")))
    validation_counts = SimpleCounts(**_pick(validation, ("total", "errors")))
    smoke_counts = SimpleCounts(**_pick(smoke, ("total", "errors")))

    summary = DocsSummary(
        timestamp=_iso_timestamp(),
        generated=int(pipeline.get("generated", 0)),
        scan=scan_counts,
        normalize=normalize_counts,
        augment=augment_counts,
        augment_quality=augment_quality_counts,
        validation=validation_counts,
        smoke=smoke_counts,
    )

    _write_summary(
        report_dir,
        summary,
        "summary_docs.md.jinja",
        summary=summary,
        scan_counts=scan_counts,
        normalize_counts=normalize_counts,
        augment_counts=augment_counts,
        augment_quality_counts=augment_quality_counts,
        validation_counts=validation_counts,
        smoke_counts=smoke_counts,
    )
    return summary


def _latest_validation_path(report_dir: Path) -> Path | None:
    candidates = list(report_dir.glob("validation*.json"))
    if not candidates:
        return None

    def _score(path: Path) -> int:
        stem = path.stem
        if stem == "validation":
            return 0
        if "_" in stem:
            suffix = stem.split("_", 1)[1]
            if suffix.isdigit():
                return int(suffix)
        return 0

    return max(candidates, key=_score)


def write_store_summary(report_dir: Path) -> StoreSummary | dict[str, object]:
    scan = _load_json(report_dir / "scan.json")
    validation_path = _latest_validation_path(report_dir)
    validation = _load_json(validation_path) if validation_path else None

    sources = validation.get("sources", {}) if isinstance(validation, dict) else {}
    total_sources = len(sources) if isinstance(sources, dict) else 0
    total_records = 0
    if isinstance(sources, dict):
        for item in sources.values():
            if isinstance(item, dict):
                item_map = {str(key): value for key, value in item.items()}
                value = item_map.get("records", 0)
                total_records += int(value) if isinstance(value, (int, float, str)) and str(value).strip() else 0
    enum_mismatches = validation.get("enum_mismatches", {}) if isinstance(validation, dict) else {}
    enum_mismatch_count = len(enum_mismatches) if isinstance(enum_mismatches, dict) else 0

    scan_counts = ScanCounts(**_pick(scan, ("total_issues", "errors", "warnings")))
    validation_summary = StoreValidationSummary(
        total_errors=int(validation.get("total_errors", 0)) if isinstance(validation, dict) else 0,
        sources=total_sources,
        records=total_records,
        enum_mismatches=enum_mismatch_count,
    )
    summary = StoreSummary(
        timestamp=_iso_timestamp(),
        scan=scan_counts,
        validation=validation_summary,
    )

    _write_summary(
        report_dir,
        summary,
        "summary_store.md.jinja",
        summary=summary,
        scan_counts=scan_counts,
        validation_summary=validation_summary,
    )
    return summary
