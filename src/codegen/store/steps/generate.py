from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from codegen.core.render import render_template
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
    desc: str


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
        members.append(
            EnumMember(
                name=name,
                value=str(value),
                desc=str(enum_desc.get(str(value), "")) if enum_desc else "",
            )
        )
    return EnumDef(name=enum_name, members=members)


def _record_length(struct: MasterStructSpec) -> int:
    total = sum(field.length for field in struct.fields)
    return struct.record_length if struct.record_length is not None else total


def generate_structs(catalog: MasterCatalog, raw_dir: Path, inference: CatalogInference | None = None) -> None:
    structs_dir = raw_dir / "structs"
    structs_dir.mkdir(parents=True, exist_ok=True)

    struct_groups: dict[str, set[str]] = {}
    for source in catalog.sources:
        struct_groups.setdefault(source.struct_name, set()).add(_group_dir(source.group))
    for struct in catalog.structs:
        struct_groups.setdefault(struct.name, {"unknown"})

    target_groups = {group for groups in struct_groups.values() for group in groups}
    for path in structs_dir.glob("*.py"):
        if path.name != "__init__.py":
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

    for struct in sorted(catalog.structs, key=lambda item: item.name):
        module_name = _snake(struct.name)
        groups = sorted(struct_groups.get(struct.name, {"unknown"}))
        for group in groups:
            module_path = structs_dir / group / f"{module_name}.py"
            struct_hint = struct_inference.get(struct.name)
            field_hints = struct_hint.fields if struct_hint else {}
            typing_imports: set[str] = set()
            enum_defs: list[EnumDef] = []
            enum_names: set[str] = set()
            fields_payload: list[StoreFieldDef] = []
            offset = 0
            field_specs: list[FieldSpecDef] = []
            for field in struct.fields:
                hint = field_hints.get(field.name)
                py_type, needed_imports, enum_values, enum_desc, nullable = _field_type(field, hint)
                typing_imports.update(needed_imports)
                if py_type == "enum" and enum_values:
                    enum_name = _enum_class_name(field.name)
                    if enum_name not in enum_names:
                        enum_defs.append(_build_enum_def(enum_name, enum_values, enum_desc or {}))
                        enum_names.add(enum_name)
                    enum_type = f"{enum_name} | str"
                    py_type = f"{enum_type} | None" if nullable else enum_type
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
                        desc=field.description or "",
                    )
                )
                start = offset
                end = offset + field.length
                field_specs.append(FieldSpecDef(name=field.name, start=start, end=end))
                offset = end

            content = render_template(
                "store/struct_module.py.jinja",
                struct_name=struct.name,
                header_url=struct.header_url,
                record_length=_record_length(struct),
                fields=fields_payload,
                field_specs=field_specs,
                typing_imports=sorted(typing_imports),
                enum_defs=enum_defs,
            )
            module_path.write_text(content, encoding="utf-8")

        primary_group = groups[0]
        struct_entries.append(
            StructInitEntry(struct_name=struct.name, module_name=module_name, group=primary_group)
        )

    init_content = render_template("store/structs_init.py.jinja", struct_entries=struct_entries)
    (structs_dir / "__init__.py").write_text(init_content, encoding="utf-8")

    for group in target_groups:
        group_dir = structs_dir / group
        module_names = [
            path.stem for path in sorted(group_dir.glob("*.py")) if path.name != "__init__.py"
        ]
        group_init_content = render_template(
            "store/structs_group_init.py.jinja",
            group=group,
            module_names=module_names,
        )
        (structs_dir / group / "__init__.py").write_text(group_init_content, encoding="utf-8")


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
) -> None:
    generate_structs(catalog, raw_dir, inference)
    generate_masters(catalog, raw_dir)


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
