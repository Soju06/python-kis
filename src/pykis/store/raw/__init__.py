"""Raw layer for master-data ingestion.

Raw layer handles bytes, fixed-width parsing, and source metadata. It must not
import translation or service layers.
"""

from pykis.store.raw.base import (
    StoreBool,
    StoreBoolOptional,
    StoreDate,
    StoreDateOptional,
    StoreDateTime,
    StoreDateTimeOptional,
    StoreDecimal,
    StoreDecimalOptional,
    StoreInt,
    StoreIntOptional,
    StoreModel,
    StoreTime,
    StoreTimeOptional,
)
from pykis.store.raw.io import iter_fixed_width_blocks
from pykis.store.raw.models import RawRecord, RawSource
from pykis.store.raw.parser import FixedWidthParser
from pykis.store.raw.reader import DelimitedReader, FixedWidthReader, RecordReader, is_delimited_file, is_line_fixed_file
from pykis.store.raw.spec import FieldSpec, RecordSpec

__all__ = [
    "FieldSpec",
    "FixedWidthParser",
    "DelimitedReader",
    "FixedWidthReader",
    "RawRecord",
    "RawSource",
    "RecordSpec",
    "RecordReader",
    "StoreBool",
    "StoreBoolOptional",
    "StoreDate",
    "StoreDateOptional",
    "StoreDateTime",
    "StoreDateTimeOptional",
    "StoreDecimal",
    "StoreDecimalOptional",
    "StoreInt",
    "StoreIntOptional",
    "StoreModel",
    "StoreTime",
    "StoreTimeOptional",
    "iter_fixed_width_blocks",
    "is_delimited_file",
    "is_line_fixed_file",
]
