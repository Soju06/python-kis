from __future__ import annotations

from codegen.core.issues import IssueLevel, SpecIssue
from codegen.store.models import MasterCatalog


def validate_catalog(catalog: MasterCatalog, path: str) -> list[SpecIssue]:
    issues: list[SpecIssue] = []

    struct_map: dict[str, str] = {}
    for struct in catalog.structs:
        if struct.name in struct_map:
            issues.append(
                SpecIssue(
                    IssueLevel.ERROR,
                    "store.struct.duplicate",
                    f"Duplicate struct name: {struct.name}",
                    path,
                    struct.name,
                )
            )
            continue
        struct_map[struct.name] = struct.header_url
        if not struct.fields:
            issues.append(
                SpecIssue(
                    IssueLevel.ERROR,
                    "store.struct.empty",
                    f"Struct has no fields: {struct.name}",
                    path,
                    struct.name,
                )
            )
            continue

        field_names: set[str] = set()
        total_length = 0
        for field in struct.fields:
            if field.name in field_names:
                issues.append(
                    SpecIssue(
                        IssueLevel.ERROR,
                        "store.field.duplicate",
                        f"Duplicate field in {struct.name}: {field.name}",
                        path,
                        struct.name,
                    )
                )
            field_names.add(field.name)
            if field.length <= 0:
                issues.append(
                    SpecIssue(
                        IssueLevel.ERROR,
                        "store.field.length",
                        f"Invalid length for {struct.name}.{field.name}: {field.length}",
                        path,
                        struct.name,
                    )
                )
            total_length += field.length

        if struct.record_length is not None and struct.record_length != total_length:
            issues.append(
                SpecIssue(
                    IssueLevel.ERROR,
                    "store.struct.length",
                    f"Record length mismatch for {struct.name}: {struct.record_length} != {total_length}",
                    path,
                    struct.name,
                )
            )

    source_ids: set[str] = set()
    for source in catalog.sources:
        if source.source_id in source_ids:
            issues.append(
                SpecIssue(
                    IssueLevel.ERROR,
                    "store.source.duplicate",
                    f"Duplicate source id: {source.source_id}",
                    path,
                    source.source_id,
                )
            )
        source_ids.add(source.source_id)
        header_url = struct_map.get(source.struct_name)
        if header_url is None:
            issues.append(
                SpecIssue(
                    IssueLevel.ERROR,
                    "store.source.struct_missing",
                    f"Unknown struct for source {source.source_id}: {source.struct_name}",
                    path,
                    source.source_id,
                )
            )
            continue
        if source.header_url != header_url:
            issues.append(
                SpecIssue(
                    IssueLevel.ERROR,
                    "store.source.header_mismatch",
                    f"Header URL mismatch for {source.source_id}: {source.header_url}",
                    path,
                    source.source_id,
                )
            )

    return issues
