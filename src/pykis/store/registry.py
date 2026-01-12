from __future__ import annotations

from typing import Type

from pydantic import BaseModel

from pathlib import Path

from .generated import SOURCE_DEFS, STRUCT_DEFS
from .raw.models import RawSource
from .generated import models as _models


def list_sources():
    return list(SOURCE_DEFS.values())


def list_structs():
    return list(STRUCT_DEFS.values())


def get_source(source_id: str):
    return SOURCE_DEFS.get(source_id)


def get_struct(struct_name: str):
    return STRUCT_DEFS.get(struct_name)


def get_model(struct_name: str) -> Type[BaseModel]:
    model = getattr(_models, struct_name, None)
    if model is None:
        raise KeyError(f"model not found: {struct_name}")
    return model


def build_raw_source(*, source_id: str, file_path: Path) -> RawSource:
    source = get_source(source_id)
    if source is None:
        raise KeyError(f"source not found: {source_id}")
    struct = get_struct(source.struct_name)
    if struct is None:
        raise KeyError(f"struct not found: {source.struct_name}")
    return RawSource(source_id=source.source_id, kind=source.struct_name, path=file_path, spec=struct.record_spec)
