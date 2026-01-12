"""Raw layer for master-data ingestion.

Raw layer handles bytes, fixed-width parsing, and source metadata. It must not
import translation or service layers.
"""

from .io import iter_fixed_width_blocks
from .models import RawRecord, RawSource
from .parser import FixedWidthParser
from .reader import FixedWidthReader
from .spec import FieldSpec, RecordSpec

__all__ = [
    "FieldSpec",
    "FixedWidthParser",
    "FixedWidthReader",
    "RawRecord",
    "RawSource",
    "RecordSpec",
    "iter_fixed_width_blocks",
]
