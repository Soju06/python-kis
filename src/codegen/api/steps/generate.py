from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from codegen.api.models import EndpointSpec, SpecField
from codegen.api.types import EndpointHints, FieldHint, TypeOverrides
from codegen.core.render import render_template

__all__ = ["generate_raw", "normalize_filename", "section_path"]


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
class ModelField:
    name: str
    type: str
    alias: str
    required: bool
    desc: str
    field_args: list[str]


@dataclass(slots=True)
class ModelDef:
    name: str
    fields: list[ModelField]


@dataclass(slots=True)
class TypedDictField:
    code: str
    type: str
    required: bool
    desc: str
    doc_type: str


@dataclass(slots=True)
class TypedDictDef:
    name: str
    fields: list[TypedDictField]


@dataclass(slots=True)
class DocFieldInfo:
    code: str
    type: str
    required: bool
    desc: str


@dataclass(slots=True)
class EndpointContext:
    id: str
    name: str
    method: str
    path: str
    description: str | None
    real_tr_id: str | None
    demo_tr_id: str | None
    auth_required: bool
    hashkey_required: bool
    request_name: str
    response_name: str
    request_dict_name: str
    call_doc_lines: list[str]


def normalize_filename(name: str) -> str:
    name = re.sub(r"^\[[^\]]+\]\s*", "", name)
    name = re.sub(r"\[v\d+_[^\]]+\]", "", name).strip()
    name = re.sub(r"\([^)]*\)", "", name).strip()
    name = re.sub(r"[^\w가-힣]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    if not name:
        name = "unnamed"
    if name[0].isdigit():
        name = f"_{name}"
    return name.lower()


def _spec_basename(spec: EndpointSpec) -> str:
    source = (spec.source_path or "").strip()
    if source:
        stem = Path(source).stem
        if stem:
            return normalize_filename(stem)
    return normalize_filename(spec.name)


def section_path(category: str | None, subcategory: str | None) -> Path:
    def _slug(value: str) -> str:
        value = re.sub(r"[^\w가-힣]+", "_", value).strip("_")
        if not value:
            value = "misc"
        if value[0].isdigit():
            value = f"_{value}"
        return value

    if category:
        return Path(_slug(category)) / _slug(subcategory or "misc")
    return Path(_slug(subcategory or "misc"))


def _class_name(name: str, suffix: str) -> str:
    base = re.sub(r"\[v\d+_[^\]]+\]", "", name).strip()
    base = re.sub(r"\([^)]*\)", "", base).strip()
    base = re.sub(r"[^0-9A-Za-z가-힣_]", "_", base)
    base = re.sub(r"_+", "_", base).strip("_")
    if not base:
        base = "Endpoint"
    if base[0].isdigit():
        base = f"_{base}"
    return f"{base}{suffix}"


def _field_name(code: str) -> str:
    name = re.sub(r"[^0-9A-Za-z_]", "_", code)
    name = re.sub(r"_+", "_", name).strip("_")
    if not name:
        name = "field"
    if name[0].isdigit():
        name = f"field_{name}"
    return name


def _enum_class_name(code: str) -> str:
    parts = _field_name(code).split("_")
    return "".join(part.capitalize() for part in parts if part) + "Enum"


def _enum_member_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value).upper().strip("_")
    if not cleaned:
        cleaned = "VALUE"
    if cleaned[0].isdigit():
        cleaned = f"VALUE_{cleaned}"
    return cleaned


def _register_enum(
    enum_defs: dict[str, EnumDef],
    enum_name: str,
    values: list[str],
    enum_desc: dict[str, str] | None,
) -> None:
    enum_def = enum_defs.get(enum_name)
    if enum_def is None:
        enum_def = EnumDef(name=enum_name, members=[])
        enum_defs[enum_name] = enum_def
    members = enum_def.members
    existing = {member.value for member in members}
    seen_names = {member.name for member in members}
    for value in values:
        value_str = str(value)
        if value_str in existing:
            continue
        name = _enum_member_name(value_str)
        if name in seen_names:
            suffix = 2
            candidate = f"{name}_{suffix}"
            while candidate in seen_names:
                suffix += 1
                candidate = f"{name}_{suffix}"
            name = candidate
        seen_names.add(name)
        members.append(EnumMember(name=name, value=value_str, desc=str(enum_desc.get(value_str, "")) if enum_desc else ""))


def _field_type(field: SpecField, hint: FieldHint | None) -> tuple[str, set[str], list[str]]:
    field_args: list[str] = []
    if hint:
        if hint.enum:
            enum_name = _enum_class_name(field.code)
            return f"{enum_name} | str", set(), field_args
        kind = hint.kind
        if kind == "int":
            return "int", set(), field_args
        if kind == "decimal":
            max_digits = hint.max_digits
            decimal_places = hint.decimal_places
            if isinstance(max_digits, int) and max_digits > 0:
                field_args.append(f"max_digits={max_digits}")
            if isinstance(decimal_places, int) and decimal_places > 0:
                field_args.append(f"decimal_places={decimal_places}")
            return "Decimal", {"Decimal"}, field_args
        if kind == "date":
            return "KisDate", {"KisDate"}, field_args
        if kind == "time":
            return "KisTime", {"KisTime"}, field_args
        if kind == "datetime":
            return "KisDateTime", {"KisDateTime"}, field_args
        if kind == "bool":
            return "KisBool", {"KisBool"}, field_args

    if field.code.lower().startswith(("output", "outblock")):
        return "object", set(), field_args
    type_name = (field.type_name or "").lower()
    if type_name == "number":
        return "Decimal", {"Decimal"}, field_args
    if type_name == "object":
        return "dict[str, object]", set(), field_args
    if type_name == "array":
        return "list[object]", set(), field_args
    return "str", set(), field_args


def _optional_type(py_type: str, imports: set[str]) -> str:
    if py_type == "KisDate":
        imports.add("KisDateOptional")
        return "KisDateOptional"
    if py_type == "KisTime":
        imports.add("KisTimeOptional")
        return "KisTimeOptional"
    if py_type == "KisDateTime":
        imports.add("KisDateTimeOptional")
        return "KisDateTimeOptional"
    return f"{py_type} | None"


def _inline_doc(text: str) -> str:
    text = (text or "").replace('"""', "\\\"\\\"\\\"")
    return " ".join(text.split()).strip()


def _enum_hint(hint: FieldHint | None) -> tuple[list[str] | None, dict[str, str] | None]:
    if not hint or hint.kind != "enum" or not hint.enum:
        return None, None
    return [str(value) for value in hint.enum], hint.enum_desc or None


def _collect_enums(
    fields: list[SpecField],
    hints: dict[str, FieldHint],
    enum_defs: dict[str, EnumDef],
) -> None:
    for field in fields:
        hint = hints.get(field.code)
        enum_values, enum_desc = _enum_hint(hint)
        if not enum_values:
            continue
        enum_name = _enum_class_name(field.code)
        _register_enum(enum_defs, enum_name, enum_values, enum_desc)


def _clean_doc_lines(text: str) -> list[str]:
    text = (text or "").replace('"""', "\\\"\\\"\\\"")
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def _build_model_fields(
    fields: list[SpecField],
    hints: dict[str, FieldHint] | None = None,
) -> list[ModelField]:
    if not fields:
        return []

    items: list[ModelField] = []
    used_names: set[str] = set()
    for field in fields:
        name = _field_name(field.code)
        if name in used_names:
            name = f"{name}_field"
        used_names.add(name)
        hint = hints.get(field.code) if hints else None
        base_type, _, field_args = _field_type(field, hint)
        required = field.required
        if hint and hint.required is not None:
            required = hint.required
        py_type = base_type if required else _optional_type(base_type, set())
        desc = _inline_doc(field.description or field.name or "")
        items.append(
            ModelField(
                name=name,
                type=py_type,
                alias=field.code,
                required=required,
                desc=desc,
                field_args=field_args,
            )
        )
    return items


def _build_typed_dict_fields(
    fields: list[SpecField],
    hints: dict[str, FieldHint] | None = None,
) -> list[TypedDictField]:
    if not fields:
        return []

    items: list[TypedDictField] = []
    for field in fields:
        hint = hints.get(field.code) if hints else None
        required = field.required
        if hint and hint.required is not None:
            required = hint.required
        base_type, _, _ = _field_type(field, hint)
        py_type = base_type if required else _optional_type(base_type, set())
        desc = _inline_doc(field.description or field.name or "")
        if desc:
            py_type = f"Annotated[{py_type}, {desc!r}]"
        items.append(
            TypedDictField(
                code=field.code,
                type=py_type,
                required=required,
                desc=desc,
                doc_type=base_type,
            )
        )
    return items


def _build_doc_fields(
    fields: list[SpecField],
    hints: dict[str, FieldHint] | None = None,
) -> list[DocFieldInfo]:
    items: list[DocFieldInfo] = []
    for field in fields:
        hint = hints.get(field.code) if hints else None
        required = field.required
        if hint and hint.required is not None:
            required = hint.required
        base_type, _, _ = _field_type(field, hint)
        desc = _inline_doc(field.description or field.name or "")
        items.append(
            DocFieldInfo(code=field.code, type=base_type, required=required, desc=desc)
        )
    return items


def _format_doc_field_line(field: DocFieldInfo, indent: str) -> str:
    code = field.code
    type_name = field.type
    desc = field.desc or ""
    optional = "" if field.required else " optional"
    if desc:
        return f"{indent}{code} ({type_name}): {desc}{optional}"
    return f"{indent}{code} ({type_name}){optional}"


def _build_request_doc_lines(description_lines: list[str], doc_fields: list[DocFieldInfo]) -> list[str]:
    header = ["Request fields:"] if doc_fields else []
    field_lines = [_format_doc_field_line(field, "    ") for field in doc_fields]
    if description_lines and header:
        return [*description_lines, "", *header, *field_lines]
    return [*description_lines, *header, *field_lines]


def _build_call_doc_lines(
    description_lines: list[str],
    doc_fields: list[DocFieldInfo],
    request_model_name: str,
    request_dict_name: str,
    response_name: str,
) -> list[str]:
    lines = [*description_lines, ""] if description_lines else []
    lines += [
        "Args:",
        "    client (SyncKisRawClient): API client.",
        (
            f"    request ({request_model_name} | {request_dict_name} | None): "
            "요청 파라미터. request 또는 kwargs 중 하나만 사용하세요."
        ),
        f"    **kwargs ({request_dict_name}): 요청 파라미터 키워드 입력.",
        "    headers (Mapping[str, str] | None): 추가 헤더.",
    ]
    if doc_fields:
        field_lines = [_format_doc_field_line(field, "            ") for field in doc_fields]
        lines += ["        Request fields:", *field_lines]
    lines += ["", "Returns:", f"    tuple[{response_name}, KisResponse]: 응답 모델과 원시 응답"]
    return lines


def generate_raw(specs: list[EndpointSpec], out_dir: Path, type_overrides: TypeOverrides | None = None) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    keep_files = {"base.py", "types.py", "registry.py", "__init__.py"}
    for child in out_dir.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        elif child.is_file() and child.name not in keep_files:
            child.unlink()

    static_files: list[str] = ["base.py", "types.py", "__init__.py"]
    for filename in static_files:
        if not (out_dir / filename).exists():
            raise RuntimeError(f"Static raw api file missing: {out_dir / filename}")

    registry_entries: list[str] = []
    used_names: dict[Path, dict[str, int]] = {}

    for spec in specs:
        folder = out_dir / section_path(spec.category, spec.subcategory)
        folder.mkdir(parents=True, exist_ok=True)
        _ensure_package_dirs(folder, out_dir)

        base_name = _spec_basename(spec)
        folder_names = used_names.setdefault(folder, {})
        count = folder_names.get(base_name, 0) + 1
        folder_names[base_name] = count
        suffix = f"_{count}" if count > 1 else ""
        filename = f"{base_name}{suffix}.py"
        module_path = folder / filename

        req_name = _class_name(spec.name, "Request")
        res_name = _class_name(spec.name, "Response")

        endpoint_hint = type_overrides.endpoints.get(spec.id) if type_overrides else None
        hints = endpoint_hint or EndpointHints()

        request_hint = hints.request
        response_hint = hints.response
        output_hint = hints.outputs
        output_kinds = hints.output_kinds
        output_aliases = hints.output_aliases
        extra_fields = hints.extra_fields

        request_fields = spec.request.query + spec.request.body
        response_fields = list(spec.response.body)
        for extra in extra_fields.response:
            response_fields.append(extra)

        enum_defs: dict[str, EnumDef] = {}

        description_lines = _clean_doc_lines(spec.description or spec.name or "")
        request_doc_fields = _build_doc_fields(request_fields, request_hint)
        request_doc_lines = _build_request_doc_lines(description_lines, request_doc_fields)
        _collect_enums(request_fields, request_hint, enum_defs)
        request_model = ModelDef(name=req_name, fields=_build_model_fields(request_fields, request_hint))

        request_dict_name = f"{req_name}Dict"
        request_dict = TypedDictDef(name=request_dict_name, fields=_build_typed_dict_fields(request_fields, request_hint))
        output_models: list[ModelDef] = []
        output_class_names: list[str] = []
        output_fields: list[ModelField] = []
        for output in spec.response.outputs:
            output_code = output.code
            class_suffix = re.sub(r"[^0-9A-Za-z]+", "_", output_code).title().replace("_", "")
            output_class = _class_name(spec.name, class_suffix)
            output_class_names.append(output_class)
            field_hints = output_hint.get(output_code, {})
            output_fields_list = list(output.fields)
            for extra in extra_fields.outputs.get(output_code, []):
                output_fields_list.append(extra)
            _collect_enums(output_fields_list, field_hints, enum_defs)
            output_models.append(
                ModelDef(name=output_class, fields=_build_model_fields(output_fields_list, field_hints))
            )

            kind = output_kinds.get(output_code) or output.kind
            if kind == "array":
                field_type = f"list[{output_class}]"
            else:
                field_type = output_class
            alias = output_aliases.get(output_code)
            output_desc = (output.name or "").strip()
            output_fields.append(
                ModelField(
                    name=output_code,
                    type=field_type,
                    alias=alias if isinstance(alias, str) and alias != output_code else output_code,
                    required=True,
                    desc=output_desc,
                    field_args=[],
                )
            )

        _collect_enums(response_fields, response_hint, enum_defs)
        envelope_fields = _build_model_fields(response_fields, response_hint)
        response_model = ModelDef(name=res_name, fields=[*envelope_fields, *output_fields])

        enum_list = list(enum_defs.values())
        all_names = [
            "ENDPOINT",
            req_name,
            request_dict_name,
            res_name,
            *output_class_names,
            *[enum_def.name for enum_def in enum_list],
        ]
        import_lines = [
            "from typing import Annotated, Mapping, NotRequired, Protocol, TYPE_CHECKING, TypedDict, Unpack, overload",
            "from decimal import Decimal",
            "",
            "from pydantic import Field",
            "",
            "from pykis.api.raw.base import RawModel, KisBool, KisDate, KisTime, KisDateTime, KisDateOptional, KisTimeOptional, KisDateTimeOptional",
            "from pykis.api.raw.types import Endpoint, KisResponse",
            "",
        ]
        if enum_list:
            import_lines.insert(3, "from pykis.common.enums import KisStrEnum")
        import_lines += [
            "if TYPE_CHECKING:",
            "    from pykis.api.client import SyncKisRawClient",
        ]
        endpoint_ctx = EndpointContext(
            id=spec.id,
            name=spec.name,
            method=spec.method,
            path=spec.path,
            description=spec.description,
            real_tr_id=spec.real_tr_id,
            demo_tr_id=spec.demo_tr_id,
            auth_required=_has_header(spec.request.headers, "authorization"),
            hashkey_required=_has_header(spec.request.headers, "hashkey"),
            request_name=req_name,
            response_name=res_name,
            request_dict_name=request_dict_name,
            call_doc_lines=_build_call_doc_lines(
                description_lines,
                request_doc_fields,
                req_name,
                request_dict_name,
                res_name,
            ),
        )
        module_text = render_template(
            "api/raw_module.py.jinja",
            imports=import_lines,
            request_model=request_model,
            request_dict=request_dict,
            request_doc_lines=request_doc_lines,
            output_models=output_models,
            response_model=response_model,
            endpoint=endpoint_ctx,
            enum_defs=enum_list,
            all_names=all_names,
        )
        module_path.write_text(module_text, encoding="utf-8")

        module_import = _module_import(out_dir, module_path)
        registry_entries.append(f"from {module_import} import ENDPOINT as ENDPOINT_{spec.id.replace('-', '_')}")
        registry_entries.append(f"ENDPOINTS[{spec.id!r}] = ENDPOINT_{spec.id.replace('-', '_')}")
        registry_entries.append("")

    registry_text = render_template("api/registry.py.jinja", registry_entries=registry_entries)
    (out_dir / "registry.py").write_text(registry_text, encoding="utf-8")


def _module_import(root: Path, module_path: Path) -> str:
    rel = module_path.relative_to(root).with_suffix("")
    parts = ["pykis", "api", "raw", *rel.parts]
    return ".".join(parts)


def _has_header(headers: list[SpecField], code: str) -> bool:
    target = code.lower()
    return any(field.code.lower() == target for field in headers)


def _ensure_package_dirs(folder: Path, root: Path) -> None:
    current = folder
    while True:
        init_path = current / "__init__.py"
        if not init_path.exists():
            init_path.write_text("", encoding="utf-8")
        if current == root:
            break
        if current.parent == current:
            break
        current = current.parent
