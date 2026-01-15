from __future__ import annotations

from pathlib import Path

import pytest

from pykis.store.raw.models import RawSource
from pykis.store.raw.reader import RecordReader, is_delimited_file
from pykis.store.raw.spec import RecordSpec

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
