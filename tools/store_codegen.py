from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DOC_PATH = Path("docs/종목정보파일_주소_헤더.md")
OUT_DIR = Path("src/pykis/store/generated")

HEADER_URL_RE = re.compile(r"^### `(?P<url>https?://[^`]+)`")
STRUCT_RE = re.compile(r"^#### `(?P<name>[^`]+)`")
TABLE_HEADER_RE = re.compile(r"^\|\s*필드명\s*\|\s*타입\s*\|\s*길이\s*\|\s*설명")
MACRO_RE = re.compile(r"([A-Z_]+)\s*=\s*(\d+)")
URL_RE = re.compile(r"`(https?://[^`]+)`")


@dataclass(frozen=True, slots=True)
class FieldDef:
    name: str
    raw_type: str
    length: int
    description: str


@dataclass(frozen=True, slots=True)
class StructDef:
    name: str
    header_url: str
    fields: tuple[FieldDef, ...]

    @property
    def record_length(self) -> int:
        return sum(field.length for field in self.fields)


@dataclass(frozen=True, slots=True)
class SourceDef:
    source_id: str
    group: str
    label: str
    download_url: str
    header_url: str
    struct_name: str


@dataclass(slots=True)
class ParsedSpec:
    structs: dict[str, StructDef]
    sources: list[SourceDef]


def _strip_ticks(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def _split_row(line: str) -> list[str]:
    parts = [part.strip() for part in line.strip().strip("|").split("|")]
    return parts


def _resolve_length(raw: str, desc: str, macros: dict[str, int]) -> int:
    token = _strip_ticks(raw)
    if token.isdigit():
        return int(token)
    for name, value in MACRO_RE.findall(desc):
        macros[name] = int(value)
    if token in macros:
        return macros[token]
    if token.startswith("SZ_"):
        suffix = re.search(r"(\d+)$", token)
        if suffix:
            return int(suffix.group(1))
        raise ValueError(f"Unknown macro length: {token}")
    match = re.search(r"\d+", token)
    if match:
        return int(match.group(0))
    raise ValueError(f"Unable to resolve length: {raw}")


def parse_structs(lines: list[str]) -> dict[str, StructDef]:
    structs: dict[str, StructDef] = {}
    macros: dict[str, int] = {
        "SZ_SHRNCODE": 9,
        "SZ_STNDCODE": 12,
        "SZ_KORNAME": 40,
    }
    idx = 0
    current_header_url: str | None = None
    while idx < len(lines):
        line = lines[idx]
        header_match = HEADER_URL_RE.match(line)
        if header_match:
            current_header_url = header_match.group("url")
            idx += 1
            continue
        struct_match = STRUCT_RE.match(line)
        if struct_match and current_header_url:
            struct_name = struct_match.group("name")
            idx += 1
            while idx < len(lines) and not TABLE_HEADER_RE.match(lines[idx]):
                if lines[idx].startswith("### ") or lines[idx].startswith("#### "):
                    break
                idx += 1
            if idx >= len(lines) or not TABLE_HEADER_RE.match(lines[idx]):
                continue
            idx += 1
            if idx < len(lines) and lines[idx].startswith("|---"):
                idx += 1
            fields: list[FieldDef] = []
            while idx < len(lines):
                row = lines[idx]
                if row.startswith("### ") or row.startswith("#### "):
                    break
                if not row.strip() or not row.strip().startswith("|"):
                    idx += 1
                    continue
                parts = _split_row(row)
                if len(parts) >= 4 and parts[0] != "필드명":
                    name = _strip_ticks(parts[0])
                    raw_type = _strip_ticks(parts[1])
                    length = _resolve_length(parts[2], parts[3], macros)
                    desc = _strip_ticks(parts[3])
                    fields.append(FieldDef(name=name, raw_type=raw_type, length=length, description=desc))
                idx += 1
            structs[struct_name] = StructDef(
                name=struct_name,
                header_url=current_header_url,
                fields=tuple(fields),
            )
            continue
        idx += 1
    return structs


def parse_sources(lines: list[str], struct_map: dict[str, StructDef]) -> list[SourceDef]:
    header_url_to_struct: dict[str, str] = {struct.header_url: struct.name for struct in struct_map.values()}

    def _parse_table(start: int) -> tuple[list[SourceDef], int]:
        sources: list[SourceDef] = []
        idx = start
        while idx < len(lines) and "| 구분 |" not in lines[idx]:
            idx += 1
        if idx >= len(lines):
            return sources, idx
        idx += 2
        while idx < len(lines):
            line = lines[idx]
            if not line.strip() or line.startswith("### "):
                break
            if not line.strip().startswith("|"):
                idx += 1
                continue
            parts = _split_row(line)
            if len(parts) < 4:
                idx += 1
                continue
            group = parts[0]
            label = parts[1]
            urls = URL_RE.findall(line)
            if len(urls) >= 2:
                download_url, header_url = urls[0], urls[1]
                source_id = _source_id_from_url(download_url)
                struct_name = header_url_to_struct.get(header_url)
                if struct_name is None:
                    raise ValueError(f"Missing struct for header URL: {header_url}")
                sources.append(
                    SourceDef(
                        source_id=source_id,
                        group=group,
                        label=label,
                        download_url=download_url,
                        header_url=header_url,
                        struct_name=struct_name,
                    )
                )
            idx += 1
        return sources, idx

    sources: list[SourceDef] = []
    idx = 0
    while idx < len(lines):
        if lines[idx].startswith("### 국내"):
            domestic, idx = _parse_table(idx)
            sources.extend(domestic)
            continue
        if lines[idx].startswith("### 해외"):
            foreign, idx = _parse_table(idx)
            sources.extend(foreign)
            continue
        idx += 1
    return sources


def _source_id_from_url(url: str) -> str:
    name = url.split("/")[-1]
    for suffix in (".mst.zip", ".cod.zip", ".mst", ".cod", ".zip"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    name = re.sub(r"[^a-zA-Z0-9_]+", "_", name)
    return name.strip("_")


def load_specs() -> ParsedSpec:
    text = DOC_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    structs = parse_structs(lines)
    sources = parse_sources(lines, structs)
    return ParsedSpec(structs=structs, sources=sources)


def _snake(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", name).lower()


def write_models(spec: ParsedSpec) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / "models.py"
    lines: list[str] = [
        "# Generated by tools/store_codegen.py. DO NOT EDIT.",
        "# ruff: noqa",
        "from __future__ import annotations",
        "",
        "from pydantic import BaseModel, ConfigDict, Field",
        "",
    ]
    for struct in sorted(spec.structs.values(), key=lambda s: s.name):
        lines.append(f"class {struct.name}(BaseModel):")
        lines.append("    model_config = ConfigDict(extra=\"ignore\", slots=True)")
        for field in struct.fields:
            description = field.description.replace("\"", "\\\"")
            lines.append(
                f"    {field.name}: str = Field(description=\"{description}\", json_schema_extra={{\"length\": {field.length}}})"
            )
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_specs(spec: ParsedSpec) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / "specs.py"
    lines: list[str] = [
        "# Generated by tools/store_codegen.py. DO NOT EDIT.",
        "# ruff: noqa",
        "from __future__ import annotations",
        "",
        "from dataclasses import dataclass",
        "",
        "from pykis.store.raw.spec import FieldSpec, RecordSpec",
        "",
    ]
    lines.append("@dataclass(frozen=True, slots=True)")
    lines.append("class StructDef:")
    lines.append("    name: str")
    lines.append("    header_url: str")
    lines.append("    record_spec: RecordSpec")
    lines.append("")
    lines.append("@dataclass(frozen=True, slots=True)")
    lines.append("class SourceDef:")
    lines.append("    source_id: str")
    lines.append("    group: str")
    lines.append("    label: str")
    lines.append("    download_url: str")
    lines.append("    header_url: str")
    lines.append("    struct_name: str")
    lines.append("")
    lines.append("STRUCT_DEFS: dict[str, StructDef] = {}")
    for struct in sorted(spec.structs.values(), key=lambda s: s.name):
        lines.append(
            f"STRUCT_DEFS['{struct.name}'] = StructDef(name='{struct.name}', header_url='{struct.header_url}', record_spec=RecordSpec(record_length={struct.record_length}, fields=("
        )
        offset = 0
        for field in struct.fields:
            start = offset
            end = offset + field.length
            lines.append(f"    FieldSpec(name='{field.name}', start={start}, end={end}),")
            offset = end
        lines.append(")))")
    lines.append("")
    lines.append("SOURCE_DEFS: dict[str, SourceDef] = {}")
    for source in spec.sources:
        lines.append(
            "SOURCE_DEFS['{source_id}'] = SourceDef(source_id='{source_id}', group='{group}', label='{label}', download_url='{download_url}', header_url='{header_url}', struct_name='{struct_name}')".format(
                source_id=source.source_id,
                group=source.group,
                label=source.label,
                download_url=source.download_url,
                header_url=source.header_url,
                struct_name=source.struct_name,
            )
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    spec = load_specs()
    write_models(spec)
    write_specs(spec)


if __name__ == "__main__":
    main()
