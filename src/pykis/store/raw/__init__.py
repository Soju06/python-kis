"""Raw layer for master-data ingestion.

Raw layer handles bytes, fixed-width parsing, and source metadata. It must not
import translation or service layers.
"""

from pykis.store.parser.base import (
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
from pykis.store.parser.io import iter_fixed_width_blocks
from pykis.store.parser.models import RawRecord, RawSource
from pykis.store.parser.parser import FixedWidthParser
from pykis.store.parser.reader import (
    DelimitedReader,
    FixedWidthReader,
    RecordReader,
    is_delimited_file,
    is_line_fixed_file,
)
from pykis.store.parser.spec import FieldSpec, RecordSpec

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
