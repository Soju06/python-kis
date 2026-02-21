from __future__ import annotations

from pykis.store.service.index import Index
from pykis.store.translate.models import Instrument, InstrumentKey


class Store:
    """Lookup/search facade backed by an index implementation."""

    _index: Index

    __slots__ = ("_index",)

    def __init__(self, index: Index) -> None:
        self._index = index

    def lookup(self, *, asset_class: str, market: str, symbol: str) -> Instrument | None:
        key = InstrumentKey(
            asset_class=asset_class.strip().upper(),
            market=market.strip().upper(),
            symbol=symbol.strip().upper(),
        )
        return self._index.lookup(key)

    def search_name(self, query: str, limit: int = 50) -> list[Instrument]:
        return list(self._index.search_name(query, limit=limit))
