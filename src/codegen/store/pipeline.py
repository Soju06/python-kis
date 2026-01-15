from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Mapping

import httpx
from pydantic import ValidationError

from codegen.core.issues import IssueLevel, IssueReport, SpecIssue
from codegen.core.paths import project_root, store_docs_root
from codegen.core.report_models import IssueItem
from codegen.core.reports import write_store_summary
from codegen.store.models import MasterCatalog, MasterSourceSpec
from codegen.store.report_models import StoreScanReport
from codegen.store.steps.generate import generate_store
from codegen.store.steps.infer import (
    CatalogInference,
    InferConfig,
    infer_catalog_types,
    write_inference,
)
from codegen.store.steps.io import load_catalog
from codegen.store.steps.validate import validate_catalog
from codegen.store.validation_models import (
    EnumMismatchMap,
    StoreValidationReport,
    ValidationErrorEntry,
    ValidationErrorRecord,
    ValidationSourceSummary,
    ValidationSplitResult,
)
from pykis.store.raw.definitions import SourceDef

ROOT = project_root()
DOCS_ROOT = store_docs_root(ROOT)
SPEC_PATH = DOCS_ROOT
RAW_DIR = ROOT / "src" / "pykis" / "store" / "raw"
REPORT_DIR = ROOT / "tmp" / "store_codegen"
CACHE_DIR = REPORT_DIR / "cache"


@dataclass(frozen=True, slots=True)
class StorePipelineResult:
    scan_report: StoreScanReport
    structs: int
    sources: int
    inference_path: Path | None


def _build_report(issues: list[SpecIssue], path: Path) -> StoreScanReport:
    report = IssueReport()
    report.extend(issues)
    counts = report.counts()
    issue_items = [IssueItem.model_validate(asdict(issue)) for issue in issues]
    return StoreScanReport(
        path=str(path),
        total_issues=len(issues),
        errors=counts[IssueLevel.ERROR.value],
        warnings=counts[IssueLevel.WARN.value],
        issues=issue_items,
    )


def _scan_spec(path: Path) -> tuple[MasterCatalog, StoreScanReport]:
    catalog = load_catalog(path)
    issues = validate_catalog(catalog, str(path))
    report = _build_report(issues, path)
    return catalog, report


def run_pipeline(
    spec_path: Path | None = None,
    raw_dir: Path | None = None,
    *,
    infer: bool = False,
    refresh: bool = False,
    workers: int = 4,
    infer_config: InferConfig | None = None,
    cache_dir: Path | None = None,
    validate_models: bool = True,
) -> StorePipelineResult:
    target_spec = spec_path or SPEC_PATH
    target_raw = raw_dir or RAW_DIR

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    catalog, scan_report = _scan_spec(target_spec)
    report_path = REPORT_DIR / "scan.json"
    with report_path.open("w", encoding="utf-8") as handle:
        json.dump(scan_report.model_dump(), handle, ensure_ascii=False, indent=2)

    if scan_report.errors:
        raise SystemExit("Store spec validation failed. See tmp/store_codegen/scan.json.")

    inference: CatalogInference | None = None
    inference_path: Path | None = None
    data_paths: dict[str, Path] | None = None
    if infer:
        cache_root = cache_dir or CACHE_DIR
        inference, data_paths = _build_inference(
            catalog,
            cache_root,
            refresh=refresh,
            workers=workers,
            config=infer_config,
        )
        inference_path = REPORT_DIR / "inference.json"
        write_inference(inference_path, inference)

    generate_store(catalog, target_raw, inference)

    if infer and validate_models and data_paths and inference:
        max_loops = 2
        enum_fields = _enum_field_map(inference)
        enum_values = _enum_value_map(inference)
        for attempt in range(max_loops):
            result = _validate_generated_models(
                catalog,
                data_paths,
                iteration=attempt,
                enum_fields=enum_fields,
                enum_values=enum_values,
            )
            if result.total_errors == 0:
                break
            if attempt >= max_loops - 1:
                raise SystemExit(f"Validation failed. See {result.report_path}.")
            _downgrade_inference(inference, result.invalid_fields)
            generate_store(catalog, target_raw, inference)
        if inference_path:
            write_inference(inference_path, inference)

    write_store_summary(REPORT_DIR)

    return StorePipelineResult(
        scan_report=scan_report,
        structs=len(catalog.structs),
        sources=len(catalog.sources),
        inference_path=inference_path,
    )


@dataclass(frozen=True, slots=True)
class DownloadResult:
    source_id: str
    download_path: Path


@dataclass(frozen=True, slots=True)
class ExtractResult:
    source_id: str
    data_path: Path


def _build_inference(
    catalog: MasterCatalog,
    cache_dir: Path,
    *,
    refresh: bool,
    workers: int,
    config: InferConfig | None,
) -> tuple[CatalogInference, dict[str, Path]]:
    sources = [_source_def(source) for source in catalog.sources]
    downloads_dir = cache_dir / "downloads"
    extracted_dir = cache_dir / "extracted"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    extracted_dir.mkdir(parents=True, exist_ok=True)

    download_results = _download_sources(sources, downloads_dir, workers=workers, refresh=refresh)
    extract_results = _extract_sources(
        sources,
        download_results,
        extracted_dir,
        workers=workers,
        refresh=refresh,
    )
    data_paths = {result.source_id: result.data_path for result in extract_results}
    inference = infer_catalog_types(catalog, data_paths, config=config)
    return inference, data_paths


@dataclass(frozen=True, slots=True)
class ValidationResult:
    total_errors: int
    invalid_fields: dict[str, set[str]]
    report_path: Path


def _validate_generated_models(
    catalog: MasterCatalog,
    data_paths: dict[str, Path],
    *,
    iteration: int = 0,
    enum_fields: dict[str, set[str]] | None = None,
    enum_values: dict[str, dict[str, list[str]]] | None = None,
) -> ValidationResult:
    import importlib
    import sys

    from pykis.store.raw.models import RawSource
    from pykis.store.raw.reader import RecordReader

    for name in list(sys.modules):
        if name == "pykis.store.raw.structs" or name.startswith("pykis.store.raw.structs."):
            sys.modules.pop(name, None)
    structs_module = importlib.import_module("pykis.store.raw.structs")
    STRUCT_DEFS = structs_module.STRUCT_DEFS
    STRUCT_MODELS = structs_module.STRUCT_MODELS

    report = StoreValidationReport()
    max_errors = 50
    invalid_fields: dict[str, set[str]] = {}

    for source in catalog.sources:
        path = data_paths.get(source.source_id)
        if path is None:
            continue
        struct_def = STRUCT_DEFS.get(source.struct_name)
        model = STRUCT_MODELS.get(source.struct_name)
        if struct_def is None or model is None:
            continue
        raw_source = RawSource(
            source_id=source.source_id,
            kind=source.struct_name,
            path=path,
            spec=struct_def.record_spec,
        )
        reader = RecordReader(raw_source)
        source_errors = 0
        total_records = 0
        with path.open("rb") as handle:
            for record in reader.iter_records(handle):
                total_records += 1
                fields = record.fields
                _collect_enum_mismatches(report, source.struct_name, fields, enum_values)
                try:
                    model.model_validate(fields)
                except ValidationError as exc:
                    split = _split_validation_errors(
                        exc,
                        struct_name=source.struct_name,
                        enum_fields=enum_fields,
                    )
                    if split.mismatches.root:
                        _merge_enum_mismatches(report, split.mismatches)
                    if split.hard_errors:
                        source_errors += 1
                        invalid_fields.setdefault(source.struct_name, set()).update(
                            _extract_error_fields(split.hard_errors)
                        )
                        if len(report.errors) < max_errors:
                            report.errors.append(
                                ValidationErrorRecord(
                                    source_id=source.source_id,
                                    struct=source.struct_name,
                                    line_no=record.line_no,
                                    error=str(exc),
                                )
                            )
        report.sources[source.source_id] = ValidationSourceSummary(
            struct=source.struct_name,
            records=total_records,
            errors=source_errors,
        )
        report.total_errors += source_errors
    report_path = REPORT_DIR / ("validation.json" if iteration == 0 else f"validation_{iteration}.json")
    report_path.write_text(
        json.dumps(report.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return ValidationResult(
        total_errors=report.total_errors,
        invalid_fields=invalid_fields,
        report_path=report_path,
    )


def _extract_error_fields(errors: list[ValidationErrorEntry]) -> set[str]:
    fields: set[str] = set()
    for error in errors:
        loc = error.loc
        if isinstance(loc, (list, tuple)) and loc:
            field = loc[0]
            if isinstance(field, str):
                fields.add(field)
    return fields


def _enum_field_map(inference: CatalogInference) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for struct_name, struct in inference.structs.items():
        enum_fields = {name for name, field in struct.fields.items() if field.kind == "enum"}
        if enum_fields:
            result[struct_name] = enum_fields
    return result


def _enum_value_map(inference: CatalogInference) -> dict[str, dict[str, list[str]]]:
    result: dict[str, dict[str, list[str]]] = {}
    for struct_name, struct in inference.structs.items():
        enum_map = {
            field_name: list(field.enum)
            for field_name, field in struct.fields.items()
            if field.kind == "enum" and field.enum
        }
        if enum_map:
            result[struct_name] = enum_map
    return result


def _collect_enum_mismatches(
    report: StoreValidationReport,
    struct_name: str,
    fields: Mapping[str, str],
    enum_values: dict[str, dict[str, list[str]]] | None,
) -> None:
    if not enum_values:
        return
    struct_enums = enum_values.get(struct_name)
    if not struct_enums:
        return
    for field_name, allowed in struct_enums.items():
        raw = fields.get(field_name)
        if raw is None:
            continue
        value = str(raw).strip()
        if not value or value in allowed:
            continue
        report.enum_mismatches.increment(struct_name, field_name, value)


def _split_validation_errors(
    exc: ValidationError,
    *,
    struct_name: str,
    enum_fields: dict[str, set[str]] | None,
) -> ValidationSplitResult:
    result = ValidationSplitResult()
    enum_field_set = (enum_fields or {}).get(struct_name, set())
    for error in exc.errors():
        loc = error.get("loc")
        field = loc[0] if isinstance(loc, (list, tuple)) and loc else None
        if error.get("type") == "literal_error" and isinstance(field, str) and field in enum_field_set:
            value = error.get("input")
            value_str = "" if value is None else str(value)
            result.mismatches.increment(struct_name, field, value_str)
            continue
        result.hard_errors.append(ValidationErrorEntry.model_validate(error))
    return result


def _merge_enum_mismatches(report: StoreValidationReport, mismatches: EnumMismatchMap) -> None:
    report.enum_mismatches.merge(mismatches)


def _downgrade_inference(inference: CatalogInference, invalid_fields: dict[str, set[str]]) -> None:
    for struct_name, fields in invalid_fields.items():
        struct = inference.structs.get(struct_name)
        if struct is None:
            continue
        for field_name in fields:
            field = struct.fields.get(field_name)
            if field is None:
                continue
            field.kind = "str"
            field.enum = None
            field.enum_desc = None


def _download_sources(
    sources: list[SourceDef],
    downloads_dir: Path,
    *,
    workers: int,
    refresh: bool,
) -> list[DownloadResult]:
    if not sources:
        return []
    if workers <= 1:
        return [_download_source(source, downloads_dir, refresh=refresh) for source in sources]
    from concurrent.futures import ThreadPoolExecutor, as_completed

    results: list[DownloadResult] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_download_source, source, downloads_dir, refresh=refresh): source
            for source in sources
        }
        for future in as_completed(futures):
            results.append(future.result())
    result_map = {result.source_id: result for result in results}
    return [result_map[source.source_id] for source in sources]


def _download_source(source: SourceDef, downloads_dir: Path, *, refresh: bool) -> DownloadResult:
    file_name = Path(source.download_url).name
    dest = downloads_dir / file_name
    if dest.exists() and not refresh:
        return DownloadResult(source_id=source.source_id, download_path=dest)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        with client.stream("GET", source.download_url) as response:
            response.raise_for_status()
            with tmp.open("wb") as handle:
                for chunk in response.iter_bytes(chunk_size=1024 * 1024):
                    if chunk:
                        handle.write(chunk)
    tmp.replace(dest)
    return DownloadResult(source_id=source.source_id, download_path=dest)


def _extract_sources(
    sources: list[SourceDef],
    downloads: list[DownloadResult],
    extracted_dir: Path,
    *,
    workers: int,
    refresh: bool,
) -> list[ExtractResult]:
    if len(sources) != len(downloads):
        raise ValueError("sources and downloads must be aligned")
    if workers <= 1:
        results = [
            _extract_source(source, download.download_path, extracted_dir, refresh=refresh)
            for source, download in zip(sources, downloads)
        ]
        result_map = {result.source_id: result for result in results}
        return [result_map[source.source_id] for source in sources]
    from concurrent.futures import ThreadPoolExecutor, as_completed

    results: list[ExtractResult] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_extract_source, source, download.download_path, extracted_dir, refresh=refresh): source
            for source, download in zip(sources, downloads)
        }
        for future in as_completed(futures):
            results.append(future.result())
    result_map = {result.source_id: result for result in results}
    return [result_map[source.source_id] for source in sources]


def _extract_source(
    source: SourceDef,
    download_path: Path,
    extracted_dir: Path,
    *,
    refresh: bool,
) -> ExtractResult:
    if download_path.suffix.lower() == ".zip":
        target = _resolve_extracted_path(extracted_dir, source)
        if target.exists() and not refresh:
            return ExtractResult(source_id=source.source_id, data_path=target)
        target = _extract_single_file(download_path, target)
        return ExtractResult(source_id=source.source_id, data_path=target)
    return ExtractResult(source_id=source.source_id, data_path=download_path)


def _resolve_extracted_path(extracted_dir: Path, source: SourceDef) -> Path:
    return extracted_dir / f"{source.source_id}.mst"


def _extract_single_file(zip_path: Path, out_path: Path) -> Path:
    import zipfile

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zipf:
        members = [name for name in zipf.namelist() if name.lower().endswith((".mst", ".cod"))]
        if not members:
            raise RuntimeError(f"No .mst/.cod file found in {zip_path}")
        member = members[0]
        suffix = Path(member).suffix.lower()
        final_path = out_path.with_suffix(suffix if suffix else out_path.suffix)
        if final_path != out_path:
            out_path = final_path
        with zipf.open(member) as src, out_path.open("wb") as dst:
            import shutil

            shutil.copyfileobj(src, dst, length=1024 * 1024)
    return out_path


def _source_def(source: MasterSourceSpec) -> SourceDef:
    return SourceDef(
        source_id=source.source_id,
        group=source.group,
        label=source.label,
        download_url=source.download_url,
        header_url=source.header_url,
        struct_name=source.struct_name,
    )
