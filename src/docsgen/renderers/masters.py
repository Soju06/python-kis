"""Render master file docs into markdown/YAML outputs."""

from __future__ import annotations

import re
from dataclasses import asdict

from docsgen.parsers.master_headers import MasterStruct
from docsgen.parsers.master_sources import MasterSource
from docsgen.renderers.jinja_env import render_template


def _escape_markdown(value: str) -> str:
    return value.replace("|", "\\|")


def _format_description(text: str) -> str:
    if not text:
        return ""
    return _escape_markdown(text).replace("\n", "<br>")


def _normalize_group_folder(name: str) -> str:
    cleaned = re.sub(r"[^\w가-힣]+", "-", name.strip()).strip("-")
    return cleaned or "unknown"


def _group_sources(sources: list[MasterSource]) -> dict[str, list[MasterSource]]:
    grouped: dict[str, list[MasterSource]] = {}
    for source in sources:
        grouped.setdefault(source.group, []).append(source)
    return grouped


def _group_folders(groups: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    used: dict[str, str] = {}
    for group in groups:
        folder = _normalize_group_folder(group)
        if folder in used and used[folder] != group:
            suffix = 2
            candidate = f"{folder}-{suffix}"
            while candidate in used:
                suffix += 1
                candidate = f"{folder}-{suffix}"
            folder = candidate
        used[folder] = group
        mapping[group] = folder
    return mapping


def render_master_readme(sources: list[MasterSource], *, source_url: str) -> str:
    rows = [
        {
            "group": _escape_markdown(source.group),
            "label": _escape_markdown(source.label),
            "download_url": source.download_url,
            "header_url": source.header_url,
        }
        for source in sources
    ]
    return render_template("master_readme.md.jinja", source_url=source_url, sources=rows)


def render_master_index_yaml(sources: list[MasterSource]) -> dict:
    return {
        "version": "1",
        "sources": [
            {
                "source_id": source.source_id,
                "group": source.group,
                "label": source.label,
                "download_url": source.download_url,
                "header_url": source.header_url,
                **({"sample_code_url": source.sample_code_url} if source.sample_code_url else {}),
            }
            for source in sources
        ],
    }


def render_struct_markdown(struct: MasterStruct) -> str:
    fields = [
        {
            "name": field.name,
            "type_code": field.type_code,
            "length": field.length,
            "description": _format_description(field.description),
        }
        for field in struct.fields
    ]
    return render_template("master_struct.md.jinja", struct=struct, fields=fields)


def render_struct_yaml(struct: MasterStruct) -> dict:
    return {
        "name": struct.name,
        "header_url": struct.header_url,
        "record_length": struct.record_length,
        "fields": [asdict(field) for field in struct.fields],
    }


def group_sources(sources: list[MasterSource]) -> tuple[dict[str, list[MasterSource]], dict[str, str]]:
    grouped = _group_sources(sources)
    folder_map = _group_folders(list(grouped.keys()))
    return grouped, folder_map
