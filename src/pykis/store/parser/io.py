from __future__ import annotations

from collections.abc import Iterator
from typing import BinaryIO


def iter_fixed_width_blocks(
    stream: BinaryIO,
    record_length: int,
    *,
    buffer_size: int = 1024 * 1024,
) -> Iterator[memoryview]:
    if record_length <= 0:
        raise ValueError("record_length must be positive")
    if buffer_size < record_length:
        buffer_size = record_length

    remainder = b""
    while True:
        chunk = stream.read(buffer_size)
        if not chunk:
            break
        data = remainder + chunk
        total = (len(data) // record_length) * record_length
        if total:
            view = memoryview(data)
            for offset in range(0, total, record_length):
                yield view[offset : offset + record_length]
        remainder = data[total:]

    # ignore trailing incomplete record, if any
