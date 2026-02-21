from __future__ import annotations

from dataclasses import dataclass

from pykis.store.parser.spec import RecordSpec


@dataclass(frozen=True, slots=True)
class StructDef:
    name: str
    header_url: str
    record_spec: RecordSpec


@dataclass(frozen=True, slots=True)
class SourceDef:
    source_id: str
    group: str
    label: str
    download_url: str
    header_url: str
    struct_name: str
