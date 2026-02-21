from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field

from codegen.store.models import MasterCatalog, MasterSourceSpec, MasterStructSpec


class _DocsSourceSpec(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    source_id: str
    group: str
    label: str
    download_url: str
    header_url: str
    sample_code_url: str | None = None


class _DocsIndex(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    version: str | None = None
    sources: list[_DocsSourceSpec] = Field(default_factory=list)


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML root: {path}")
    return data


def _resolve_docs_paths(path: Path) -> tuple[Path, Path]:
    if path.is_dir():
        docs_root = path
        index_path = docs_root / "index.yaml"
    else:
        docs_root = path.parent
        index_path = path
    return docs_root, index_path


def _load_structs(docs_root: Path) -> dict[str, MasterStructSpec]:
    structs: dict[str, MasterStructSpec] = {}
    for path in sorted(docs_root.rglob("*.yaml")):
        if path.name == "index.yaml":
            continue
        data = _load_yaml(path)
        struct = MasterStructSpec.model_validate(data)
        existing = structs.get(struct.name)
        if existing is None:
            structs[struct.name] = struct
            continue
        if existing.model_dump() != struct.model_dump():
            raise ValueError(f"Conflicting struct definition: {struct.name}")
    return structs


def _build_sources(index: _DocsIndex, structs: dict[str, MasterStructSpec]) -> list[MasterSourceSpec]:
    header_to_struct: dict[str, str] = {}
    for struct in structs.values():
        existing = header_to_struct.setdefault(struct.header_url, struct.name)
        if existing != struct.name:
            raise ValueError(f"Multiple structs for header URL: {struct.header_url}")

    sources: list[MasterSourceSpec] = []
    for source in index.sources:
        struct_name = header_to_struct.get(source.header_url)
        if struct_name is None:
            raise ValueError(f"Missing struct for header URL: {source.header_url}")
        sources.append(
            MasterSourceSpec(
                source_id=source.source_id,
                group=source.group,
                label=source.label,
                download_url=source.download_url,
                header_url=source.header_url,
                struct=struct_name,
            )
        )
    return sources


def load_catalog(path: Path) -> MasterCatalog:
    docs_root, index_path = _resolve_docs_paths(path)
    index = _DocsIndex.model_validate(_load_yaml(index_path))
    structs = _load_structs(docs_root)
    sources = _build_sources(index, structs)
    return MasterCatalog(version=index.version, sources=sources, structs=list(structs.values()))


def write_catalog(path: Path, catalog: MasterCatalog) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = catalog.model_dump(by_alias=True, exclude_none=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, allow_unicode=True, sort_keys=False)
