from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import yaml

from .models import DocEndpoint, EndpointSpec


def iter_yaml_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.yaml") if p.is_file())


def load_yaml_doc(path: Path) -> DocEndpoint:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML root: {path}")
    return DocEndpoint.model_validate(data)


def load_spec(path: Path) -> EndpointSpec:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return EndpointSpec.model_validate(data)


def write_spec(path: Path, spec: EndpointSpec) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(spec.model_dump(by_alias=True), handle, ensure_ascii=False, indent=2)


def write_report(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)


def iter_spec_files(root: Path) -> Iterable[Path]:
    return sorted(p for p in root.rglob("*.json") if p.is_file())

