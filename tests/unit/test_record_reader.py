from __future__ import annotations

from pathlib import Path

import pytest

from pykis.store.parser.models import RawSource
from pykis.store.parser.reader import RecordReader, is_delimited_file
from pykis.store.parser.spec import RecordSpec

pytestmark = pytest.mark.unit


def test_record_reader_parses_delimited(tmp_path: Path) -> None:
    path = tmp_path / "sample.mst"
    path.write_bytes(b"1|ABC|ALPHA\n2|DEF|BETA\n")

    spec = RecordSpec.from_lengths(["code", "id", "name"], [1, 3, 5], record_length=9)
    source = RawSource(source_id="sample", kind="sample", path=path, spec=spec)

    assert is_delimited_file(path, len(spec.fields))

    reader = RecordReader(source)
    with path.open("rb") as stream:
        records = list(reader.iter_records(stream))

    assert records[0].fields["code"] == "1"
    assert records[0].fields["id"] == "ABC"
    assert records[1].fields["name"] == "BETA"


def test_record_reader_parses_tab_delimited(tmp_path: Path) -> None:
    path = tmp_path / "sample.cod"
    path.write_bytes(b"1\tABC\tALPHA\t\n2\tDEF\tBETA\t\n")

    spec = RecordSpec.from_lengths(["code", "id", "name", "extra"], [1, 3, 5, 1], record_length=10)
    source = RawSource(source_id="sample", kind="sample", path=path, spec=spec)

    assert is_delimited_file(path, len(spec.fields))

    reader = RecordReader(source)
    with path.open("rb") as stream:
        records = list(reader.iter_records(stream))

    assert records[0].fields["code"] == "1"
    assert records[0].fields["id"] == "ABC"
    assert records[1].fields["name"] == "BETA"
    assert records[1].fields["extra"] == ""
