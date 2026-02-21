from __future__ import annotations

import json
import logging
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal, cast

from codegen.api.models import EndpointSpec
from codegen.api.overrides import load_doc_overrides, load_type_overrides, load_validator_overrides
from codegen.api.report_models import (
    ApiPipelineReport,
    AugmentQualityReport,
    AugmentSummary,
    ScanReport,
)
from codegen.api.reporting import write_api_report
from codegen.api.scenarios import load_scenarios
from codegen.api.steps.augment import run_multi_scenario_augmentation, summarize_scenarios
from codegen.api.steps.enum_candidates import build_enum_drift_candidates
from codegen.api.steps.generate import RAW_KEEP_FILES, generate_raw, normalize_filename, section_path
from codegen.api.steps.infer import infer_types, validate_samples
from codegen.api.steps.io import (
    iter_yaml_files,
    load_yaml_doc,
    write_report,
    write_spec,
)
from codegen.api.steps.manual_candidates import (
    build_enum_manual_review_candidates,
    build_enum_manual_review_priority,
    render_enum_manual_review_candidates_markdown,
    render_enum_manual_review_priority_markdown,
)
from codegen.api.steps.normalize import normalize_doc
from codegen.api.steps.override_candidates import (
    build_enum_type_override_candidates,
    build_enum_type_override_priority,
    render_enum_type_override_candidates_markdown,
    render_enum_type_override_priority_markdown,
)
from codegen.api.steps.smoke import run_smoke
from codegen.api.steps.validate import validate_doc
from codegen.api.steps.validators import build_validation_candidates, discover_validators
from codegen.api.types import TypeOverrides
from codegen.core.cleanup import clean_dir_keep_files
from codegen.core.issues import IssueLevel, IssueReport, SpecIssue
from codegen.core.paths import docs_root, project_root
from codegen.core.report_models import IssueItem, ParseError
from codegen.core.reports import write_docs_summary
from codegen.core.types import JsonObject
from pykis.api.auth import KisAuth
from pykis.api.client import SyncKisRawClient
from pykis.api.raw.types import Endpoint

ROOT = project_root()
DOCS_BASE = ROOT / "data"
DOCS_ROOT = docs_root(ROOT)
ARTIFACTS_ROOT = ROOT / "tmp" / "docs"
NORMALIZED_DIR = ARTIFACTS_ROOT / "normalized"
REPORT_DIR = ARTIFACTS_ROOT / "reports"
GENERATED_API_RAW_DIR = ROOT / "src" / "pykis" / "api" / "raw"
RAW_REGISTRY_PREFIX = "pykis.api.raw"
AUGMENT_DIR = ARTIFACTS_ROOT / "augment"
OVERRIDES_PATH = DOCS_BASE / "overrides" / "augment_overrides.yaml"
TYPE_OVERRIDES_PATH = DOCS_BASE / "overrides" / "type_overrides.yaml"
VALIDATOR_OVERRIDES_PATH = DOCS_BASE / "overrides" / "validators.yaml"
DOC_OVERRIDES_PATH = DOCS_BASE / "overrides" / "doc_overrides.yaml"
AUGMENT_SCENARIOS_PATH = ROOT / "src" / "codegen" / "config" / "augment_scenarios.yaml"
DEMO_SECRET = ROOT / "demo_secret.json"
REAL_SECRET = ROOT / "real_secret.json"
TARGET_SECTIONS: tuple[str, ...] | None = None
SAMPLE_COUNT = 5
DEMO_RATE_LIMIT = 0.5
REAL_RATE_LIMIT = 0.2
CODEGEN_API_TIMEOUT_SECONDS = float(os.environ.get("CODEGEN_API_TIMEOUT_SECONDS", "20"))
OAUTH_SECTIONS = {"OAuth인증"}
OAUTH_SUBCATEGORIES = {"OAuth인증"}
REALTIME_SUBCATEGORIES = {"실시간시세"}
EXCLUDED_PATH_PREFIXES = ("/oauth2",)

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


def _normalize_label(value: str | None) -> str:
    return (value or "").strip()


def _is_oauth_spec(spec: EndpointSpec) -> bool:
    section = _normalize_label(spec.section)
    category = _normalize_label(spec.category)
    subcategory = _normalize_label(spec.subcategory)
    path = (spec.path or "").strip()
    if section in OAUTH_SECTIONS:
        return True
    if category in OAUTH_SECTIONS:
        return True
    if subcategory in OAUTH_SUBCATEGORIES:
        return True
    return any(path.startswith(prefix) for prefix in EXCLUDED_PATH_PREFIXES)


def _is_realtime_spec(spec: EndpointSpec) -> bool:
    section = _normalize_label(spec.section)
    category = _normalize_label(spec.category)
    subcategory = _normalize_label(spec.subcategory)
    if "실시간시세" in section:
        return True
    if "실시간시세" in category:
        return True
    return subcategory in REALTIME_SUBCATEGORIES


def _filter_api_raw_specs(specs: list[EndpointSpec]) -> tuple[list[EndpointSpec], list[EndpointSpec]]:
    kept: list[EndpointSpec] = []
    dropped: list[EndpointSpec] = []
    for spec in specs:
        if _is_oauth_spec(spec) or _is_realtime_spec(spec):
            dropped.append(spec)
        else:
            kept.append(spec)
    return kept, dropped


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
    client = SyncKisRawClient(
        auth,
        domain=domain,
        rate_limit=rate_limit,
        keep_token=keep_token,
        timeout=CODEGEN_API_TIMEOUT_SECONDS,
    )
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
    validator_overrides = load_validator_overrides(VALIDATOR_OVERRIDES_PATH)
    type_overrides = type_overrides.merge(validator_overrides)

    if TARGET_SECTIONS:
        section_specs = [spec for spec in specs if spec.section in TARGET_SECTIONS]
        logger.info(
            "scope target_sections=%s endpoints=%s",
            ", ".join(TARGET_SECTIONS),
            len(section_specs),
        )
    else:
        section_specs = specs
        logger.info("scope target_sections=ALL endpoints=%s", len(section_specs))
    section_specs, excluded_specs = _filter_api_raw_specs(section_specs)
    if excluded_specs:
        oauth_count = sum(1 for spec in excluded_specs if _is_oauth_spec(spec))
        realtime_count = len(excluded_specs) - oauth_count
        logger.info(
            "exclude api_raw oauth=%s realtime=%s kept=%s",
            oauth_count,
            realtime_count,
            len(section_specs),
        )

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

    scenario_config = load_scenarios(AUGMENT_SCENARIOS_PATH)
    scenarios = scenario_config.scenarios
    ENDPOINTS = _reload_registry()

    sample_multi = run_multi_scenario_augmentation(
        specs=sample_specs,
        registry=ENDPOINTS,
        demo_client=demo_client,
        real_client=real_client,
        overrides_path=OVERRIDES_PATH,
        out_dir=AUGMENT_DIR,
        scenarios=scenarios,
        request_templates=scenario_config.request_templates,
    )
    sample_summary = summarize_scenarios(sample_multi, "success")

    write_report(REPORT_DIR / "augment_sample.json", sample_summary)
    write_report(REPORT_DIR / "augment_multi_sample.json", sample_multi)
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

    FULL_ENDPOINTS = _reload_registry()

    augment_multi = run_multi_scenario_augmentation(
        specs=section_specs,
        registry=FULL_ENDPOINTS,
        demo_client=demo_client,
        real_client=real_client,
        overrides_path=OVERRIDES_PATH,
        out_dir=AUGMENT_DIR,
        scenarios=scenarios,
        request_templates=scenario_config.request_templates,
    )
    augment_summary = summarize_scenarios(augment_multi, "success")

    write_report(REPORT_DIR / "augment.json", augment_summary)
    write_report(REPORT_DIR / "augment_multi.json", augment_multi)
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

    validator_hints = discover_validators(section_specs, AUGMENT_DIR)
    write_report(
        REPORT_DIR / "validation_hints.json",
        {endpoint_id: hint.model_dump() for endpoint_id, hint in validator_hints.items()},
    )
    logger.info("validator hints generated=%s", len(validator_hints))

    validation_candidates = build_validation_candidates(section_specs, AUGMENT_DIR, validator_hints)
    write_report(
        REPORT_DIR / "validation_hints_candidates.json",
        {"candidates": [candidate.model_dump() for candidate in validation_candidates]},
    )
    logger.info("validator candidates generated=%s", len(validation_candidates))

    inference_trace: dict[str, JsonObject] = {}
    inference_base = infer_types(section_specs, AUGMENT_DIR, trace_out=inference_trace)
    write_report(REPORT_DIR / "inference_base.json", inference_base)
    (REPORT_DIR / "inference_trace.json").write_text(
        json.dumps(inference_trace, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    enum_drift_candidates = build_enum_drift_candidates(section_specs, inference_trace, AUGMENT_DIR)
    write_report(REPORT_DIR / "enum_drift_candidates.json", enum_drift_candidates)
    logger.info("enum drift candidates generated=%s", enum_drift_candidates.total)
    enum_override_candidates = build_enum_type_override_candidates(
        enum_drift_candidates,
        source_report_path=str(REPORT_DIR / "enum_drift_candidates.json"),
        applied_overrides=type_overrides,
    )
    write_report(REPORT_DIR / "type_override_candidates_enum.json", enum_override_candidates)
    (REPORT_DIR / "type_override_candidates_enum.md").write_text(
        render_enum_type_override_candidates_markdown(enum_override_candidates),
        encoding="utf-8",
    )
    enum_override_priority = build_enum_type_override_priority(enum_override_candidates)
    write_report(REPORT_DIR / "type_override_candidates_enum_priority.json", enum_override_priority)
    (REPORT_DIR / "type_override_candidates_enum_priority.md").write_text(
        render_enum_type_override_priority_markdown(enum_override_priority),
        encoding="utf-8",
    )
    override_entries = enum_override_candidates.get("overrides")
    override_count = len(override_entries) if isinstance(override_entries, list) else 0
    priority_summary = enum_override_priority.get("summary")
    ready_count = (
        int(priority_summary.get("ready_overrides", 0))
        if isinstance(priority_summary, dict)
        else 0
    )
    logger.info(
        "enum override draft candidates generated=%s ready=%s",
        override_count,
        ready_count,
    )
    inference = _apply_type_overrides(inference_base, type_overrides)
    write_report(REPORT_DIR / "inference.json", inference)
    generate_raw(section_specs, GENERATED_API_RAW_DIR, inference, module_prefix="pykis.api.raw")

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
    manual_enum_review = build_enum_manual_review_candidates(
        section_specs,
        inference_base,
        smoke,
        augment_dir=AUGMENT_DIR,
    )
    write_report(REPORT_DIR / "manual_enum_review_candidates.json", manual_enum_review)
    (REPORT_DIR / "manual_enum_review_candidates.md").write_text(
        render_enum_manual_review_candidates_markdown(manual_enum_review),
        encoding="utf-8",
    )
    manual_enum_priority = build_enum_manual_review_priority(
        manual_enum_review,
        source_report_path=str(REPORT_DIR / "manual_enum_review_candidates.json"),
    )
    write_report(REPORT_DIR / "manual_enum_review_priority.json", manual_enum_priority)
    (REPORT_DIR / "manual_enum_review_priority.md").write_text(
        render_enum_manual_review_priority_markdown(manual_enum_priority),
        encoding="utf-8",
    )
    priority_summary = manual_enum_priority.get("summary")
    ready_endpoints = (
        int(priority_summary.get("ready_endpoints", 0))
        if isinstance(priority_summary, dict)
        else 0
    )
    hold_endpoints = (
        int(priority_summary.get("hold_endpoints", 0))
        if isinstance(priority_summary, dict)
        else 0
    )
    logger.info(
        "manual enum review candidates fields=%s endpoints=%s ready=%s hold=%s",
        manual_enum_review.total_fields,
        manual_enum_review.endpoints,
        ready_endpoints,
        hold_endpoints,
    )

    pipeline_report = ApiPipelineReport(
        scan=scan_report,
        normalize=normalize_report,
        sample=sample_summary,
        augment=augment_summary,
        augment_multi_sample=sample_multi,
        augment_multi=augment_multi,
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
    write_api_report(ROOT)

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

    clean_dir_keep_files(GENERATED_API_RAW_DIR, RAW_KEEP_FILES)


def _reload_registry() -> dict[str, Endpoint]:
    to_delete = [name for name in sys.modules if name.startswith(RAW_REGISTRY_PREFIX)]
    for name in to_delete:
        sys.modules.pop(name, None)
    import importlib

    import pykis.api.raw.registry as registry

    importlib.reload(registry)
    return cast(dict[str, Endpoint], registry.ENDPOINTS)
