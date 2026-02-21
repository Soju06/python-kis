from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from codegen.store.steps.io import load_catalog


def _write_yaml(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8")


def _index_payload(header_url: str) -> dict:
    return {
        "version": "1",
        "sources": [
            {
                "source_id": "alpha",
                "group": "Group",
                "label": "Label",
                "download_url": "https://example.com/alpha.mst.zip",
                "header_url": header_url,
            }
        ],
    }


def _struct_payload(name: str, header_url: str) -> dict:
    return {
        "name": name,
        "header_url": header_url,
        "record_length": 2,
        "fields": [
            {
                "name": "field_one",
                "type": "char",
                "length": 2,
                "description": "Field One",
            }
        ],
    }


def test_load_catalog_from_docs_dir_builds_sources(tmp_path: Path) -> None:
    docs_root = tmp_path / "docs"
    header_url = "https://example.com/header.h"
    _write_yaml(docs_root / "index.yaml", _index_payload(header_url))
    _write_yaml(docs_root / "Group" / "ST_ALPHA.yaml", _struct_payload("ST_ALPHA", header_url))

    catalog = load_catalog(docs_root)

    assert len(catalog.sources) == 1
    assert catalog.sources[0].struct_name == "ST_ALPHA"
    assert len(catalog.structs) == 1
    assert catalog.structs[0].name == "ST_ALPHA"


def test_load_catalog_dedup_structs(tmp_path: Path) -> None:
    docs_root = tmp_path / "docs"
    header_url = "https://example.com/header.h"
    _write_yaml(docs_root / "index.yaml", _index_payload(header_url))
    struct_payload = _struct_payload("ST_ALPHA", header_url)
    _write_yaml(docs_root / "GroupA" / "ST_ALPHA.yaml", struct_payload)
    _write_yaml(docs_root / "GroupB" / "ST_ALPHA.yaml", struct_payload)

    catalog = load_catalog(docs_root)

    assert len(catalog.structs) == 1
    assert catalog.structs[0].name == "ST_ALPHA"


def test_load_catalog_rejects_conflicting_structs(tmp_path: Path) -> None:
    docs_root = tmp_path / "docs"
    _write_yaml(docs_root / "index.yaml", _index_payload("https://example.com/one.h"))
    _write_yaml(docs_root / "GroupA" / "ST_ALPHA.yaml", _struct_payload("ST_ALPHA", "https://example.com/one.h"))
    _write_yaml(docs_root / "GroupB" / "ST_ALPHA.yaml", _struct_payload("ST_ALPHA", "https://example.com/two.h"))

    with pytest.raises(ValueError, match="Conflicting struct definition"):
        load_catalog(docs_root)


def test_load_catalog_missing_struct_header(tmp_path: Path) -> None:
    docs_root = tmp_path / "docs"
    _write_yaml(docs_root / "index.yaml", _index_payload("https://example.com/missing.h"))

    with pytest.raises(ValueError, match="Missing struct for header URL"):
        load_catalog(docs_root)
