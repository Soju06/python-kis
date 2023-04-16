import requests
from typing import TYPE_CHECKING, Iterable, Literal
from datetime import datetime, time

from ..account import KisAccount
from ..client import KisPage, KisLongPage, KisDynamicPagingAPIResponse, KisDynamicLongPagingAPIResponse, KisDynamic, KisDynamicAPIResponse
from .base import KisScopeBase

if TYPE_CHECKING:
    from ..kis import PyKis
