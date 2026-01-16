from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import yaml

from codegen.core.format import run_ruff_fix, run_ruff_format
from codegen.core.render import render_template
from codegen.core.text import wrap_display_lines
from codegen.core.types import JsonObject
from codegen.store.models import MasterCatalog, MasterField, MasterStructSpec
from codegen.store.steps.infer import CatalogInference, FieldInference


def _snake(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", name).lower()


def _const(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]+", "_", name).upper()


def _group_dir(name: str) -> str:
    cleaned = name.strip()
    cleaned = cleaned.replace("/", "_").replace("\\", "_")
    cleaned = re.sub(r"\s+", "_", cleaned)
    return cleaned or "unknown"


def _enum_class_name(field_name: str) -> str:
    parts = re.split(r"[^a-zA-Z0-9]+", field_name)
    return "".join(part.capitalize() for part in parts if part) + "Enum"


def _enum_member_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value).upper().strip("_")
    if not cleaned:
        cleaned = "VALUE"
    if cleaned in {"I", "O", "L"}:
        cleaned = f"VALUE_{cleaned}"
    if cleaned[0].isdigit():
        cleaned = f"VALUE_{cleaned}"
    return cleaned


@dataclass(slots=True)
class EnumMember:
    name: str
    value: str
    desc: str


@dataclass(slots=True)
class EnumDef:
    name: str
    members: list[EnumMember]


@dataclass(slots=True)
class StoreFieldDef:
    name: str
    type: str
    extra: JsonObject
    nullable: bool
    desc_lines: list[str]

    @property
    def init_args(self) -> list[str]:
        args: list[str] = []
        if self.nullable:
            args.append("default=None")
        args.append(f"json_schema_extra={self.extra!r}")
        return args


@dataclass(slots=True)
class FieldSpecDef:
    name: str
    start: int
    end: int


@dataclass(slots=True)
class SourceDefContext:
    alias: str
    source_id: str
    group: str
    label: str
    download_url: str
    header_url: str
    struct_name: str


@dataclass(slots=True)
class StructInitEntry:
    struct_name: str
    module_name: str
    group: str


@dataclass(slots=True)
class ExportItem:
    name: str
    alias: str | None = None


@dataclass(slots=True)
class StructModuleExport:
    module_name: str
    items: list[ExportItem]


@dataclass(slots=True)
class EnumMemberSource:
    group: str
    desc: str
    struct_name: str
    field_name: str


@dataclass(slots=True)
class EnumConflict:
    enum_name: str
    value: str
    existing_desc: str
    existing_group: str
    existing_struct: str
    existing_field: str
    new_desc: str
    new_group: str
    new_struct: str
    new_field: str


@dataclass(slots=True)
class EnumOverride:
    canonical_desc: str
    variants: set[str]


def _build_enum_def(enum_name: str, enum_values: list[str], enum_desc: dict[str, str] | None) -> EnumDef:
    seen: set[str] = set()
    members: list[EnumMember] = []
    for value in enum_values:
        name = _enum_member_name(str(value))
        if name in seen:
            suffix = 2
            candidate = f"{name}_{suffix}"
            while candidate in seen:
                suffix += 1
                candidate = f"{name}_{suffix}"
            name = candidate
        seen.add(name)
        desc = str(enum_desc.get(str(value), "")) if enum_desc else ""
        members.append(
            EnumMember(
                name=name,
                value=str(value),
                desc=desc.strip(),
            )
        )
    return EnumDef(
        name=enum_name,
        members=members,
    )


def _record_length(struct: MasterStructSpec) -> int:
    total = sum(field.length for field in struct.fields)
    return struct.record_length if struct.record_length is not None else total


def _desc_lines(text: str) -> list[str]:
    if not text:
        return []
    lines = wrap_display_lines(text, width=96)
    if len(lines) <= 1:
        return lines
    return [f"{line} " for line in lines[:-1]] + [lines[-1]]


def _ensure_unique_member_name(name: str, used: set[str]) -> str:
    if name not in used:
        used.add(name)
        return name
    suffix = 2
    candidate = f"{name}_{suffix}"
    while candidate in used:
        suffix += 1
        candidate = f"{name}_{suffix}"
    used.add(candidate)
    return candidate


def _apply_override_desc(override: EnumOverride | None, desc: str) -> str:
    cleaned = (desc or "").strip()
    if override is None:
        return cleaned
    canonical = (override.canonical_desc or "").strip()
    variants = {value.strip() for value in override.variants if value is not None}
    if canonical:
        variants.add(canonical)
    if not cleaned:
        return canonical
    if cleaned in variants:
        return canonical or cleaned
    return cleaned


def _load_enum_overrides(path: Path | None) -> dict[tuple[str, str], EnumOverride]:
    if path is None or not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    overrides = payload.get("overrides") if isinstance(payload, dict) else None
    if not isinstance(overrides, list):
        return {}
    result: dict[tuple[str, str], EnumOverride] = {}
    for entry in overrides:
        if not isinstance(entry, dict):
            continue
        enum_name = entry.get("enum") or entry.get("enum_name")
        value = entry.get("value")
        if not enum_name or value is None:
            continue
        canonical = str(entry.get("canonical_desc") or "")
        variants: set[str] = set()
        for variant in entry.get("variants") or []:
            if isinstance(variant, dict):
                desc = variant.get("desc")
            else:
                desc = variant
            if desc is None:
                continue
            variants.add(str(desc))
        if canonical:
            variants.add(canonical)
        result[(str(enum_name), str(value))] = EnumOverride(canonical_desc=canonical, variants=variants)
    return result


def _merge_global_enum(
    *,
    group: str,
    enum_name: str,
    enum_values: list[str],
    enum_desc: dict[str, str] | None,
    struct_name: str,
    field_name: str,
    enum_defs: dict[str, EnumDef],
    enum_sources: dict[str, dict[str, EnumMemberSource]],
    overrides: dict[tuple[str, str], EnumOverride],
    conflicts: list[EnumConflict],
) -> None:
    new_def = _build_enum_def(enum_name, enum_values, enum_desc)
    existing_def = enum_defs.get(enum_name)
    if existing_def is None:
        for member in new_def.members:
            override = overrides.get((enum_name, member.value))
            member.desc = _apply_override_desc(override, member.desc)
        enum_defs[enum_name] = new_def
        enum_sources[enum_name] = {
            member.value: EnumMemberSource(
                group=group,
                desc=member.desc,
                struct_name=struct_name,
                field_name=field_name,
            )
            for member in new_def.members
        }
        return

    value_map = {member.value: member for member in existing_def.members}
    name_set = {member.name for member in existing_def.members}
    source_map = enum_sources.setdefault(enum_name, {})

    for member in new_def.members:
        override = overrides.get((enum_name, member.value))
        member.desc = _apply_override_desc(override, member.desc)
        existing_member = value_map.get(member.value)
        if existing_member:
            existing_member.desc = _apply_override_desc(override, existing_member.desc)
            existing_source = source_map.get(
                member.value,
                EnumMemberSource(
                    group=group,
                    desc=existing_member.desc,
                    struct_name=struct_name,
                    field_name=field_name,
                ),
            )
            existing_desc = existing_member.desc
            new_desc = member.desc
            if existing_desc != new_desc:
                conflicts.append(
                    EnumConflict(
                        enum_name=enum_name,
                        value=member.value,
                        existing_desc=existing_member.desc,
                        existing_group=existing_source.group,
                        existing_struct=existing_source.struct_name,
                        existing_field=existing_source.field_name,
                        new_desc=member.desc,
                        new_group=group,
                        new_struct=struct_name,
                        new_field=field_name,
                    )
                )
                if not existing_desc and new_desc:
                    existing_member.desc = member.desc
                    source_map[member.value] = EnumMemberSource(
                        group=group,
                        desc=member.desc,
                        struct_name=struct_name,
                        field_name=field_name,
                    )
            continue

        unique_name = _ensure_unique_member_name(member.name, name_set)
        existing_def.members.append(
            EnumMember(
                name=unique_name,
                value=member.value,
                desc=member.desc,
            )
        )
        value_map[member.value] = existing_def.members[-1]
        source_map[member.value] = EnumMemberSource(
            group=group,
            desc=member.desc,
            struct_name=struct_name,
            field_name=field_name,
        )


def generate_structs(
    catalog: MasterCatalog,
    raw_dir: Path,
    inference: CatalogInference | None = None,
    enum_overrides: dict[tuple[str, str], EnumOverride] | None = None,
) -> list[EnumConflict]:
    structs_dir = raw_dir / "structs"
    structs_dir.mkdir(parents=True, exist_ok=True)

    struct_groups: dict[str, set[str]] = {}
    for source in catalog.sources:
        struct_groups.setdefault(source.struct_name, set()).add(_group_dir(source.group))
    for struct in catalog.structs:
        struct_groups.setdefault(struct.name, {"unknown"})

    target_groups = {group for groups in struct_groups.values() for group in groups}
    for path in structs_dir.glob("*.py"):
        if path.name not in {"__init__.py", "_enums.py"}:
            path.unlink()
    for path in structs_dir.iterdir():
        if path.is_dir() and path.name not in target_groups:
            shutil.rmtree(path)
    for group in target_groups:
        group_dir = structs_dir / group
        group_dir.mkdir(parents=True, exist_ok=True)
        for path in group_dir.glob("*.py"):
            if path.name != "__init__.py":
                path.unlink()

    struct_inference = inference.structs if inference else {}
    struct_entries: list[StructInitEntry] = []
    group_exports: dict[str, list[StructModuleExport]] = {}
    enum_defs: dict[str, EnumDef] = {}
    enum_sources: dict[str, dict[str, EnumMemberSource]] = {}
    conflicts: list[EnumConflict] = []
    overrides = enum_overrides or {}

    for struct in sorted(catalog.structs, key=lambda item: item.name):
        module_name = _snake(struct.name)
        groups = sorted(struct_groups.get(struct.name, {"unknown"}))
        for group in groups:
            module_path = structs_dir / group / f"{module_name}.py"
            struct_hint = struct_inference.get(struct.name)
            field_hints = struct_hint.fields if struct_hint else {}
            typing_imports: set[str] = set()
            enum_names: set[str] = set()
            fields_payload: list[StoreFieldDef] = []
            offset = 0
            field_specs: list[FieldSpecDef] = []
            for field in struct.fields:
                hint = field_hints.get(field.name)
                py_type, needed_imports, enum_values, enum_desc, nullable = _field_type(field, hint)
                typing_imports.update(needed_imports)
                enum_pool_values = hint.enum if hint and hint.enum else None
                enum_pool_desc = hint.enum_desc if hint and hint.enum_desc else None
                if enum_pool_values:
                    enum_name = _enum_class_name(field.name)
                    _merge_global_enum(
                        group=group,
                        enum_name=enum_name,
                        enum_values=enum_pool_values,
                        enum_desc=enum_pool_desc or {},
                        struct_name=struct.name,
                        field_name=field.name,
                        enum_defs=enum_defs,
                        enum_sources=enum_sources,
                        overrides=overrides,
                        conflicts=conflicts,
                    )
                    if py_type == "enum" and enum_values:
                        enum_names.add(enum_name)
                        py_type = f"{enum_name} | None" if nullable else enum_name
                extra: JsonObject = {"length": field.length}
                if enum_values:
                    extra["enum"] = enum_values
                if enum_desc:
                    extra["enum_desc"] = enum_desc
                fields_payload.append(
                    StoreFieldDef(
                        name=field.name,
                        type=py_type,
                        extra=extra,
                        nullable=nullable,
                        desc_lines=_desc_lines(field.description or ""),
                    )
                )
                start = offset
                end = offset + field.length
                field_specs.append(FieldSpecDef(name=field.name, start=start, end=end))
                offset = end

            export_names = [struct.name, "STRUCT_DEF"]
            group_exports.setdefault(group, []).append(
                StructModuleExport(
                    module_name=module_name,
                    items=[
                        ExportItem(name=struct.name),
                        ExportItem(name="STRUCT_DEF", alias=f"{struct.name}_DEF"),
                    ],
                )
            )

            content = render_template(
                "store/struct_module.py.jinja",
                struct_name=struct.name,
                header_url=struct.header_url,
                record_length=_record_length(struct),
                fields=fields_payload,
                field_specs=field_specs,
                typing_imports=sorted(typing_imports),
                enum_imports=sorted(enum_names),
                export_names=export_names,
            )
            module_path.write_text(content, encoding="utf-8")

        primary_group = groups[0]
        struct_entries.append(StructInitEntry(struct_name=struct.name, module_name=module_name, group=primary_group))

    init_content = render_template("store/structs_init.py.jinja", struct_entries=struct_entries)
    (structs_dir / "__init__.py").write_text(init_content, encoding="utf-8")

    enums_path = structs_dir / "_enums.py"
    if enum_defs:
        enum_content = render_template(
            "store/enums_module.py.jinja",
            enum_defs=[enum_defs[name] for name in sorted(enum_defs)],
        )
        enums_path.write_text(enum_content, encoding="utf-8")
    elif enums_path.exists():
        enums_path.unlink()

    for group in target_groups:
        group_dir = structs_dir / group
        module_exports = group_exports.get(group, [])
        if not module_exports:
            module_names = [path.stem for path in sorted(group_dir.glob("*.py")) if path.name != "__init__.py"]
            module_exports = [
                StructModuleExport(
                    module_name=name,
                    items=[ExportItem(name="STRUCT_DEF", alias=f"{name.upper()}_DEF")],
                )
                for name in module_names
            ]
        group_init_content = render_template(
            "store/structs_group_init.py.jinja",
            group=group,
            module_exports=module_exports,
        )
        (structs_dir / group / "__init__.py").write_text(group_init_content, encoding="utf-8")
    return conflicts


def generate_masters(catalog: MasterCatalog, raw_dir: Path) -> None:
    masters_dir = raw_dir / "masters"
    if masters_dir.exists():
        shutil.rmtree(masters_dir)

    module_path = raw_dir / "masters.py"
    sources: list[SourceDefContext] = []
    for source in sorted(catalog.sources, key=lambda item: item.source_id):
        sources.append(
            SourceDefContext(
                alias=f"{_const(source.source_id)}_SOURCE",
                source_id=source.source_id,
                group=source.group,
                label=source.label,
                download_url=source.download_url,
                header_url=source.header_url,
                struct_name=source.struct_name,
            )
        )
    content = render_template("store/masters.py.jinja", sources=sources)
    module_path.write_text(content, encoding="utf-8")


def generate_store(
    catalog: MasterCatalog,
    raw_dir: Path,
    inference: CatalogInference | None = None,
    enum_override_path: Path | None = None,
) -> list[EnumConflict]:
    overrides = _load_enum_overrides(enum_override_path)
    conflicts = generate_structs(catalog, raw_dir, inference, enum_overrides=overrides)
    generate_masters(catalog, raw_dir)
    run_ruff_fix([raw_dir / "structs", raw_dir / "masters.py"])
    run_ruff_format([raw_dir / "structs", raw_dir / "masters.py"])
    return conflicts


def _field_type(
    field: MasterField,
    hint: FieldInference | None,
) -> tuple[str, set[str], list[str] | None, dict[str, str] | None, bool]:
    kind = hint.kind if hint else "str"
    nullable = hint.nullable if hint else False
    enum_values = hint.enum if hint and kind == "enum" else None
    enum_desc = hint.enum_desc if hint and kind == "enum" else None

    if kind == "bool":
        return ("StoreBoolOptional" if nullable else "StoreBool"), set(), None, None, nullable
    if kind == "date":
        return ("StoreDateOptional" if nullable else "StoreDate"), set(), None, None, nullable
    if kind == "time":
        return ("StoreTimeOptional" if nullable else "StoreTime"), set(), None, None, nullable
    if kind == "datetime":
        return ("StoreDateTimeOptional" if nullable else "StoreDateTime"), set(), None, None, nullable
    if kind == "decimal":
        return ("StoreDecimalOptional" if nullable else "StoreDecimal"), set(), None, None, nullable
    if kind == "int":
        return ("StoreIntOptional" if nullable else "StoreInt"), set(), None, None, nullable
    if kind == "enum" and isinstance(enum_values, list) and enum_values:
        return (
            "enum",
            set(),
            [str(value) for value in enum_values],
            enum_desc,
            nullable,
        )
    return ("str | None" if nullable else "str"), set(), None, None, nullable
