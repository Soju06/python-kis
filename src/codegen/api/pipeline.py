from __future__ import annotations

import json
import logging
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal, cast

from codegen.api.models import EndpointSpec
from codegen.api.overrides import load_doc_overrides, load_type_overrides
from codegen.api.report_models import (
    ApiPipelineReport,
    AugmentQualityReport,
    AugmentSummary,
    ScanReport,
)
from codegen.api.steps.augment import run_augmentation
from codegen.api.steps.generate import generate_raw, normalize_filename, section_path
from codegen.api.steps.infer import infer_types, validate_samples
from codegen.api.steps.io import (
    iter_yaml_files,
    load_yaml_doc,
    write_report,
    write_spec,
)
from codegen.api.steps.normalize import normalize_doc
from codegen.api.steps.smoke import run_smoke
from codegen.api.steps.validate import validate_doc
from codegen.api.types import TypeOverrides
from codegen.core.issues import IssueLevel, IssueReport, SpecIssue
from codegen.core.paths import docs_root, project_root
from codegen.core.report_models import IssueItem, ParseError
from codegen.core.reports import write_docs_summary
from codegen.core.types import JsonObject
from pykis.api.auth import KisAuth
from pykis.api.client import SyncKisRawClient
from pykis.raw.types import Endpoint

ROOT = project_root()
DOCS_BASE = ROOT / "docs"
DOCS_ROOT = docs_root(ROOT)
ARTIFACTS_ROOT = ROOT / "tmp" / "docs"
NORMALIZED_DIR = ARTIFACTS_ROOT / "normalized"
REPORT_DIR = ARTIFACTS_ROOT / "reports"
GENERATED_API_RAW_DIR = ROOT / "src" / "pykis" / "api" / "raw"
GENERATED_RAW_DIR = ROOT / "src" / "pykis" / "raw"
RAW_REGISTRY_PREFIX = "pykis.api.raw"
AUGMENT_DIR = ARTIFACTS_ROOT / "augment"
OVERRIDES_PATH = DOCS_BASE / "overrides" / "augment_overrides.yaml"
TYPE_OVERRIDES_PATH = DOCS_BASE / "overrides" / "type_overrides.yaml"
DOC_OVERRIDES_PATH = DOCS_BASE / "overrides" / "doc_overrides.yaml"
DEMO_SECRET = ROOT / "demo_secret.json"
REAL_SECRET = ROOT / "real_secret.json"
TARGET_SECTIONS = ("[국내주식] 기본시세", "[해외주식] 기본시세")
SAMPLE_COUNT = 5
DEMO_RATE_LIMIT = 0.5
REAL_RATE_LIMIT = 0.2

logger = logging.getLogger("pykis.codegen.pipeline")


@dataclass(frozen=True, slots=True)
class PipelineResult:
    scan_report: ScanReport
    normalize_report: ScanReport
    augment_summary: AugmentSummary
    augment_quality: AugmentQualityReport
    generated: int


def _spec_basename(spec: EndpointSpec) -> str:
    source = (spec.source_path or "").strip()
    if source:
        stem = Path(source).stem
        if stem:
            return normalize_filename(stem)
    return normalize_filename(spec.name)


def _build_report(issues: list[SpecIssue], parse_errors: list[JsonObject]) -> ScanReport:
    report = IssueReport()
    report.extend(issues)
    counts = report.counts()
    issue_items = [IssueItem.model_validate(asdict(issue)) for issue in issues]
    error_items = [ParseError.model_validate(item) for item in parse_errors]
    return ScanReport(
        total_issues=len(issues),
        errors=counts[IssueLevel.ERROR.value],
        warnings=counts[IssueLevel.WARN.value],
        issues=issue_items,
        parse_errors=error_items,
    )


def _scan_docs() -> ScanReport:
    issues: list[SpecIssue] = []
    parse_errors: list[JsonObject] = []
    doc_overrides = load_doc_overrides(DOC_OVERRIDES_PATH)
    for path in iter_yaml_files(DOCS_ROOT):
        try:
            doc = load_yaml_doc(path, doc_overrides)
        except Exception as exc:
            parse_errors.append({"path": str(path), "error": str(exc)})
            issues.append(
                SpecIssue(
                    IssueLevel.ERROR,
                    "parse.error",
                    f"Failed to parse YAML: {exc}",
                    str(path),
                    None,
                )
            )
            continue
        issues.extend(validate_doc(doc))
    return _build_report(issues, parse_errors)


def _apply_type_overrides(inference: TypeOverrides, overrides: TypeOverrides) -> TypeOverrides:
    if not overrides.endpoints:
        return inference
    return inference.merge(overrides)


def _normalize_docs() -> tuple[list[EndpointSpec], ScanReport]:
    issues: list[SpecIssue] = []
    parse_errors: list[JsonObject] = []
    specs: list[EndpointSpec] = []
    doc_overrides = load_doc_overrides(DOC_OVERRIDES_PATH)

    for path in iter_yaml_files(DOCS_ROOT):
        try:
            doc = load_yaml_doc(path, doc_overrides)
        except Exception as exc:
            parse_errors.append({"path": str(path), "error": str(exc)})
            issues.append(
                SpecIssue(
                    IssueLevel.ERROR,
                    "parse.error",
                    f"Failed to parse YAML: {exc}",
                    str(path),
                    None,
                )
            )
            continue

        spec, report = normalize_doc(doc, str(path))
        issues.extend(report.issues)
        if spec is None:
            continue
        specs.append(spec)

    report = _build_report(issues, parse_errors)
    if report.errors:
        return [], report

    for spec in specs:
        folder = NORMALIZED_DIR / section_path(spec.category, spec.subcategory)
        folder.mkdir(parents=True, exist_ok=True)
        filename = f"{_spec_basename(spec)}__{spec.id}.json"
        write_spec(folder / filename, spec)
    return specs, report


def _load_auth(path: Path) -> KisAuth:
    return KisAuth.load(path)


def _prepare_client(
    auth: KisAuth, domain: Literal["demo", "real"], rate_limit: float, keep_token: bool | str
) -> tuple[SyncKisRawClient | None, Exception | None]:
    client = SyncKisRawClient(auth, domain=domain, rate_limit=rate_limit, keep_token=keep_token)
    try:
        client.ensure_token()
        return client, None
    except Exception as exc:  # pragma: no cover - runtime auth dependent
        return None, exc


def _evaluate_augmentation(out_dir: Path, spec_ids: set[str]) -> AugmentQualityReport:
    meta_files = [out_dir / spec_id / "meta.json" for spec_id in spec_ids]
    meta_files = [path for path in meta_files if path.exists()]
    total = len(meta_files)
    http_ok = 0
    status_codes: dict[int, int] = {}
    rt_cd_counts: dict[str, int] = {}
    msg_cd_counts: dict[str, int] = {}
    missing_counts: dict[str, int] = {}

    for meta_file in meta_files:
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        status_codes[meta["status_code"]] = status_codes.get(meta["status_code"], 0) + 1
        if meta.get("ok"):
            http_ok += 1

        for missing in meta.get("missing_required") or []:
            missing_counts[missing] = missing_counts.get(missing, 0) + 1

        success_path = meta_file.parent / "success.json"
        if not success_path.exists():
            continue
        payload = json.loads(success_path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            rt_cd = payload.get("rt_cd")
            msg_cd = payload.get("msg_cd")
            if rt_cd is not None:
                rt_cd_counts[str(rt_cd)] = rt_cd_counts.get(str(rt_cd), 0) + 1
            if msg_cd is not None:
                msg_cd_counts[str(msg_cd)] = msg_cd_counts.get(str(msg_cd), 0) + 1

    def _top(items: dict[str, int], limit: int = 10) -> list[tuple[str, int]]:
        return sorted(items.items(), key=lambda x: -x[1])[:limit]

    return AugmentQualityReport(
        total_calls=total,
        http_ok=http_ok,
        status_codes_top=_top({str(k): v for k, v in status_codes.items()}),
        rt_cd_top=_top(rt_cd_counts),
        msg_cd_top=_top(msg_cd_counts),
        missing_required_top=_top(missing_counts),
    )


def run_pipeline() -> PipelineResult:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    _clean_generated_dirs()

    scan_report = _scan_docs()
    write_report(REPORT_DIR / "scan.json", scan_report)
    logger.info(
        "scan issues=%s errors=%s warnings=%s",
        scan_report.total_issues,
        scan_report.errors,
        scan_report.warnings,
    )
    if scan_report.errors:
        raise SystemExit("Scan failed with errors. See report.")

    specs, normalize_report = _normalize_docs()
    write_report(REPORT_DIR / "normalize.json", normalize_report)
    logger.info(
        "normalize endpoints=%s issues=%s errors=%s warnings=%s",
        len(specs),
        normalize_report.total_issues,
        normalize_report.errors,
        normalize_report.warnings,
    )

    if normalize_report.errors:
        raise SystemExit("Normalization failed with errors. See report.")

    type_overrides = load_type_overrides(TYPE_OVERRIDES_PATH)

    section_specs = [spec for spec in specs if spec.section in TARGET_SECTIONS]
    logger.info("scope target_sections=%s endpoints=%s", ", ".join(TARGET_SECTIONS), len(section_specs))

    def _sort_key(item: EndpointSpec) -> str:
        return item.id

    demo_specs = [spec for spec in section_specs if spec.domains.demo]
    sample_specs = sorted(demo_specs, key=_sort_key)[:SAMPLE_COUNT]
    if len(sample_specs) < SAMPLE_COUNT:
        remaining = [spec for spec in section_specs if spec not in sample_specs]
        sample_specs += sorted(remaining, key=_sort_key)[: max(0, SAMPLE_COUNT - len(sample_specs))]

    logger.info("sample endpoints=%s", len(sample_specs))

    # Generate raw models/registry for sample
    generate_raw(sample_specs, GENERATED_API_RAW_DIR, type_overrides, module_prefix="pykis.api.raw")
    generate_raw(sample_specs, GENERATED_RAW_DIR, type_overrides, module_prefix="pykis.raw")

    if not DEMO_SECRET.exists():
        raise SystemExit("Missing demo_secret.json required for demo augmentation.")
    if not REAL_SECRET.exists():
        raise SystemExit("Missing real_secret.json required for real smoke tests.")

    demo_auth = _load_auth(DEMO_SECRET)
    real_auth = _load_auth(REAL_SECRET)

    demo_client, demo_error = _prepare_client(demo_auth, "demo", DEMO_RATE_LIMIT, True)
    if demo_client is None:
        raise SystemExit(f"Unable to obtain demo token: {demo_error}")
    real_client, real_error = _prepare_client(real_auth, "real", REAL_RATE_LIMIT, True)
    if real_client is None:
        raise SystemExit(f"Unable to obtain real token: {real_error}")

    ENDPOINTS = _reload_registry()

    sample_summary = run_augmentation(
        specs=sample_specs,
        registry=ENDPOINTS,
        demo_client=demo_client,
        real_client=real_client,
        overrides_path=OVERRIDES_PATH,
        out_dir=AUGMENT_DIR,
    )

    write_report(REPORT_DIR / "augment_sample.json", sample_summary)
    logger.info(
        "augment-sample processed=%s ok=%s cached=%s skipped=%s errors=%s",
        sample_summary.processed,
        sample_summary.ok,
        sample_summary.cached,
        sample_summary.skipped,
        sample_summary.errors,
    )
    augment_quality_sample = _evaluate_augmentation(AUGMENT_DIR, {spec.id for spec in sample_specs})
    write_report(REPORT_DIR / "augment_quality_sample.json", augment_quality_sample)
    logger.info(
        "quality-sample rt_cd_top=%s msg_cd_top=%s",
        augment_quality_sample.rt_cd_top,
        augment_quality_sample.msg_cd_top,
    )

    inference_sample = _apply_type_overrides(infer_types(sample_specs, AUGMENT_DIR), type_overrides)
    write_report(REPORT_DIR / "inference_sample.json", inference_sample)
    generate_raw(section_specs, GENERATED_API_RAW_DIR, inference_sample, module_prefix="pykis.api.raw")
    generate_raw(section_specs, GENERATED_RAW_DIR, inference_sample, module_prefix="pykis.raw")

    FULL_ENDPOINTS = _reload_registry()

    augment_summary = run_augmentation(
        specs=section_specs,
        registry=FULL_ENDPOINTS,
        demo_client=demo_client,
        real_client=real_client,
        overrides_path=OVERRIDES_PATH,
        out_dir=AUGMENT_DIR,
    )

    write_report(REPORT_DIR / "augment.json", augment_summary)
    logger.info(
        "augment processed=%s ok=%s cached=%s skipped=%s errors=%s",
        augment_summary.processed,
        augment_summary.ok,
        augment_summary.cached,
        augment_summary.skipped,
        augment_summary.errors,
    )

    augment_quality = _evaluate_augmentation(AUGMENT_DIR, {spec.id for spec in section_specs})
    write_report(REPORT_DIR / "augment_quality.json", augment_quality)
    logger.info(
        "quality rt_cd_top=%s msg_cd_top=%s",
        augment_quality.rt_cd_top,
        augment_quality.msg_cd_top,
    )

    inference = _apply_type_overrides(infer_types(section_specs, AUGMENT_DIR), type_overrides)
    write_report(REPORT_DIR / "inference.json", inference)
    generate_raw(section_specs, GENERATED_API_RAW_DIR, inference, module_prefix="pykis.api.raw")
    generate_raw(section_specs, GENERATED_RAW_DIR, inference, module_prefix="pykis.raw")

    validation = validate_samples(section_specs, AUGMENT_DIR, _reload_registry())
    write_report(REPORT_DIR / "validation.json", validation)
    logger.info("validate total=%s errors=%s", validation.total, validation.errors)

    smoke = run_smoke(
        section_specs,
        _reload_registry(),
        demo_client,
        real_client,
        OVERRIDES_PATH,
        REPORT_DIR / "smoke.json",
    )
    logger.info("smoke total=%s errors=%s", smoke.total, smoke.errors)

    pipeline_report = ApiPipelineReport(
        scan=scan_report,
        normalize=normalize_report,
        sample=sample_summary,
        augment=augment_summary,
        augment_quality_sample=augment_quality_sample,
        augment_quality=augment_quality,
        inference_sample=inference_sample,
        inference=inference,
        validation=validation,
        smoke=smoke,
        generated=len(section_specs),
    )
    (REPORT_DIR / "pipeline.json").write_text(
        json.dumps(pipeline_report.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_docs_summary(REPORT_DIR)

    if validation.errors:
        raise SystemExit("Validation finished with errors. See reports.")
    if smoke.errors:
        raise SystemExit("Smoke tests finished with errors. See reports.")

    return PipelineResult(
        scan_report=scan_report,
        normalize_report=normalize_report,
        augment_summary=augment_summary,
        augment_quality=augment_quality,
        generated=len(section_specs),
    )


def _clean_generated_dirs() -> None:
    for path in REPORT_DIR.glob("*.json"):
        path.unlink()

    if NORMALIZED_DIR.exists():
        for child in NORMALIZED_DIR.rglob("*.json"):
            child.unlink()
        for sub in sorted(NORMALIZED_DIR.rglob("*"), reverse=True):
            if sub.is_dir():
                sub.rmdir()

    keep_files = {"base.py", "registry.py", "types.py", "__init__.py"}
    for raw_dir in (GENERATED_API_RAW_DIR, GENERATED_RAW_DIR):
        if not raw_dir.exists():
            continue
        for child in raw_dir.iterdir():
            if child.is_file() and child.name in keep_files:
                continue
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                for sub in child.rglob("*"):
                    if sub.is_file():
                        sub.unlink()
                for sub in sorted(child.rglob("*"), reverse=True):
                    if sub.is_dir():
                        sub.rmdir()
                child.rmdir()


def _reload_registry() -> dict[str, Endpoint]:
    to_delete = [name for name in sys.modules if name.startswith(RAW_REGISTRY_PREFIX)]
    for name in to_delete:
        sys.modules.pop(name, None)
    import importlib

    import pykis.api.raw.registry as registry

    importlib.reload(registry)
    return cast(dict[str, Endpoint], registry.ENDPOINTS)
