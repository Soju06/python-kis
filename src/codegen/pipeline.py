from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
import sys

from .augment import run_augmentation
from .errors import IssueLevel, IssueReport, SpecIssue
from .generate import generate_raw, _normalize_filename, _section_path
from .infer import infer_types, validate_samples
from .smoke import run_smoke
from .io import iter_yaml_files, load_yaml_doc, write_report, write_spec
from .models import EndpointSpec
from .normalize import normalize_doc
from .validate import validate_doc
from pykis.api.auth import KisAuth
from pykis.api.client import KisRawClient


ROOT = Path(".")
DOCS_ROOT = ROOT / "docs" / "kis"
ARTIFACTS_ROOT = ROOT / "tmp" / "docs"
NORMALIZED_DIR = ARTIFACTS_ROOT / "normalized"
REPORT_DIR = ARTIFACTS_ROOT / "reports"
GENERATED_RAW_DIR = ROOT / "src" / "pykis" / "api" / "raw"
AUGMENT_DIR = ARTIFACTS_ROOT / "augment"
OVERRIDES_PATH = AUGMENT_DIR / "overrides.yaml"
DEMO_SECRET = ROOT / "demo_secret.json"
REAL_SECRET = ROOT / "real_secret.json"
TARGET_SECTION = "[국내주식] 기본시세"
SAMPLE_COUNT = 5


@dataclass(frozen=True, slots=True)
class PipelineResult:
    scan_report: dict
    normalize_report: dict
    augment_summary: dict
    augment_quality: dict
    generated: int


def _build_report(issues: list[SpecIssue], parse_errors: list[dict]) -> dict:
    report = IssueReport()
    report.extend(issues)
    counts = report.counts()
    return {
        "total_issues": len(issues),
        "errors": counts[IssueLevel.ERROR.value],
        "warnings": counts[IssueLevel.WARN.value],
        "issues": [asdict(issue) for issue in issues],
        "parse_errors": parse_errors,
    }


def _scan_docs() -> dict:
    issues: list[SpecIssue] = []
    parse_errors: list[dict] = []
    for path in iter_yaml_files(DOCS_ROOT):
        try:
            doc = load_yaml_doc(path)
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


def _normalize_docs() -> tuple[list[EndpointSpec], dict]:
    issues: list[SpecIssue] = []
    parse_errors: list[dict] = []
    specs: list[EndpointSpec] = []

    for path in iter_yaml_files(DOCS_ROOT):
        try:
            doc = load_yaml_doc(path)
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
    if report["errors"]:
        return [], report

    for spec in specs:
        folder = NORMALIZED_DIR / _section_path(spec.category, spec.subcategory)
        folder.mkdir(parents=True, exist_ok=True)
        filename = f"{_normalize_filename(spec.name)}__{spec.id}.json"
        write_spec(folder / filename, spec)
    return specs, report


def _load_auth(path: Path) -> KisAuth:
    return KisAuth.load(path)


def _prepare_client(
    auth: KisAuth, domain: str, rate_limit: float, keep_token: bool | str
) -> tuple[KisRawClient | None, Exception | None]:
    client = KisRawClient(auth, domain=domain, rate_limit=rate_limit, keep_token=keep_token)
    try:
        client.ensure_token()
        return client, None
    except Exception as exc:  # pragma: no cover - runtime auth dependent
        return None, exc


def _evaluate_augmentation(out_dir: Path, spec_ids: set[str]) -> dict:
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

    return {
        "total_calls": total,
        "http_ok": http_ok,
        "status_codes_top": _top({str(k): v for k, v in status_codes.items()}),
        "rt_cd_top": _top(rt_cd_counts),
        "msg_cd_top": _top(msg_cd_counts),
        "missing_required_top": _top(missing_counts),
    }


def run_pipeline() -> PipelineResult:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    _clean_generated_dirs()

    scan_report = _scan_docs()
    write_report(REPORT_DIR / "scan.json", scan_report)
    print(f"[scan] issues={scan_report['total_issues']} errors={scan_report['errors']} warnings={scan_report['warnings']}")
    if scan_report["errors"]:
        raise SystemExit("Scan failed with errors. See report.")

    specs, normalize_report = _normalize_docs()
    write_report(REPORT_DIR / "normalize.json", normalize_report)
    print(
        f"[normalize] endpoints={len(specs)} issues={normalize_report['total_issues']} "
        f"errors={normalize_report['errors']} warnings={normalize_report['warnings']}"
    )

    if normalize_report["errors"]:
        raise SystemExit("Normalization failed with errors. See report.")

    section_specs = [spec for spec in specs if spec.section == TARGET_SECTION]
    print(f"[scope] target_section={TARGET_SECTION} endpoints={len(section_specs)}")

    def _sort_key(item: EndpointSpec) -> str:
        return item.id

    demo_specs = [spec for spec in section_specs if spec.domains.virtual]
    sample_specs = sorted(demo_specs, key=_sort_key)[:SAMPLE_COUNT]
    if len(sample_specs) < SAMPLE_COUNT:
        remaining = [spec for spec in section_specs if spec not in sample_specs]
        sample_specs += sorted(remaining, key=_sort_key)[: max(0, SAMPLE_COUNT - len(sample_specs))]

    print(f"[sample] endpoints={len(sample_specs)}")

    # Generate raw models/registry for sample
    generate_raw(sample_specs, GENERATED_RAW_DIR)

    if not DEMO_SECRET.exists():
        raise SystemExit("Missing demo_secret.json required for demo augmentation.")
    if not REAL_SECRET.exists():
        raise SystemExit("Missing real_secret.json required for real smoke tests.")

    demo_auth = _load_auth(DEMO_SECRET)
    real_auth = _load_auth(REAL_SECRET)

    demo_client, demo_error = _prepare_client(demo_auth, "demo", 0.2, True)
    if demo_client is None:
        raise SystemExit(f"Unable to obtain demo token: {demo_error}")
    real_client, real_error = _prepare_client(real_auth, "real", 0.05, True)
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
    print(
        f"[augment-sample] processed={sample_summary['processed']} ok={sample_summary['ok']} "
        f"cached={sample_summary.get('cached', 0)} skipped={sample_summary['skipped']} "
        f"errors={sample_summary['errors']}"
    )
    augment_quality_sample = _evaluate_augmentation(AUGMENT_DIR, {spec.id for spec in sample_specs})
    write_report(REPORT_DIR / "augment_quality_sample.json", augment_quality_sample)
    print(
        f"[quality-sample] rt_cd_top={augment_quality_sample['rt_cd_top']} "
        f"msg_cd_top={augment_quality_sample['msg_cd_top']}"
    )

    inference_sample = infer_types(sample_specs, AUGMENT_DIR)
    write_report(REPORT_DIR / "inference_sample.json", inference_sample)
    generate_raw(section_specs, GENERATED_RAW_DIR, inference_sample)

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
    print(
        f"[augment] processed={augment_summary['processed']} ok={augment_summary['ok']} "
        f"cached={augment_summary.get('cached', 0)} skipped={augment_summary['skipped']} "
        f"errors={augment_summary['errors']}"
    )

    augment_quality = _evaluate_augmentation(AUGMENT_DIR, {spec.id for spec in section_specs})
    write_report(REPORT_DIR / "augment_quality.json", augment_quality)
    print(f"[quality] rt_cd_top={augment_quality['rt_cd_top']} msg_cd_top={augment_quality['msg_cd_top']}")

    inference = infer_types(section_specs, AUGMENT_DIR)
    write_report(REPORT_DIR / "inference.json", inference)
    generate_raw(section_specs, GENERATED_RAW_DIR, inference)

    validation = validate_samples(section_specs, AUGMENT_DIR, _reload_registry())
    write_report(REPORT_DIR / "validation.json", validation)
    print(f"[validate] total={validation['total']} errors={validation['errors']}")

    smoke = run_smoke(
        section_specs,
        _reload_registry(),
        demo_client,
        real_client,
        OVERRIDES_PATH,
        REPORT_DIR / "smoke.json",
    )
    print(f"[smoke] total={smoke['total']} errors={smoke['errors']}")

    pipeline_report = {
        "scan": scan_report,
        "normalize": normalize_report,
        "sample": sample_summary,
        "augment": augment_summary,
        "augment_quality_sample": augment_quality_sample,
        "augment_quality": augment_quality,
        "inference_sample": inference_sample,
        "inference": inference,
        "validation": validation,
        "smoke": smoke,
        "generated": len(section_specs),
    }
    (REPORT_DIR / "pipeline.json").write_text(
        json.dumps(pipeline_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    if validation.get("errors"):
        raise SystemExit("Validation finished with errors. See reports.")
    if smoke.get("errors"):
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

    legacy_artifacts = [
        ROOT / "src" / "docs" / "normalized",
        ROOT / "src" / "docs" / "reports",
        ROOT / "src" / "docs" / "augment",
    ]
    for legacy in legacy_artifacts:
        if not legacy.exists():
            continue
        for child in legacy.rglob("*"):
            if child.is_file():
                child.unlink()
        for sub in sorted(legacy.rglob("*"), reverse=True):
            if sub.is_dir():
                sub.rmdir()
        legacy.rmdir()

    legacy_models = GENERATED_RAW_DIR / "models.py"
    if legacy_models.exists():
        legacy_models.unlink()

    if GENERATED_RAW_DIR.exists():
        keep_files = {"base.py", "registry.py", "types.py", "__init__.py"}
        for child in GENERATED_RAW_DIR.iterdir():
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

    legacy_raw_dir = ROOT / "src" / "pykis" / "raw" / "api"
    if legacy_raw_dir.exists():
        for child in legacy_raw_dir.rglob("*"):
            if child.is_file():
                child.unlink()
        for sub in sorted(legacy_raw_dir.rglob("*"), reverse=True):
            if sub.is_dir():
                sub.rmdir()
        legacy_raw_dir.rmdir()

    legacy_generated = ROOT / "src" / "pykis" / "_generated"
    if legacy_generated.exists():
        for child in legacy_generated.rglob("*"):
            if child.is_file():
                child.unlink()
        for sub in sorted(legacy_generated.rglob("*"), reverse=True):
            if sub.is_dir():
                sub.rmdir()
        legacy_generated.rmdir()


def _reload_registry() -> dict[str, object]:
    to_delete = [name for name in sys.modules if name.startswith("pykis.api.raw")]
    for name in to_delete:
        sys.modules.pop(name, None)
    import importlib
    import pykis.api.raw.registry as registry

    importlib.reload(registry)
    return registry.ENDPOINTS
