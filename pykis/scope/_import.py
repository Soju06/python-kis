import requests
from typing import TYPE_CHECKING, Iterable, Literal
from datetime import datetime, date, time

from ..account import KisAccount
from ..client import (
    KisPage,
    KisLongPage,
    KisZeroPage,
    KisDynamicPagingAPIResponse,
    KisDynamic,
    KisDynamicAPIResponse,
    KisDynamicLongPagingAPIResponse,
    KisDynamicZeroPagingAPIResponse,
)
from .base import KisScopeBase

if TYPE_CHECKING:
    from ..kis import PyKis
