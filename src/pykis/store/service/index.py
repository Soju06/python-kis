from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Protocol

from pykis.store.translate.models import Instrument, InstrumentKey


class Index(Protocol):
    def lookup(self, key: InstrumentKey) -> Instrument | None: ...

    def search_name(self, query: str, limit: int = 50) -> Sequence[Instrument]: ...


class InMemoryIndex:
    """Reference index implementation (fast for small datasets)."""

    _by_key: dict[InstrumentKey, Instrument]
    _by_name: dict[str, list[Instrument]]

    __slots__ = ("_by_key", "_by_name")

    def __init__(self, instruments: Iterable[Instrument]) -> None:
        self._by_key: dict[InstrumentKey, Instrument] = {}
        self._by_name: dict[str, list[Instrument]] = {}
        for inst in instruments:
            self._by_key[inst.key] = inst
            if inst.name:
                key = inst.name.casefold()
                self._by_name.setdefault(key, []).append(inst)

    def lookup(self, key: InstrumentKey) -> Instrument | None:
        return self._by_key.get(key)

    def search_name(self, query: str, limit: int = 50) -> Sequence[Instrument]:
        if not query:
            return []
        needle = query.casefold()
        results: list[Instrument] = []
        for name_key, items in self._by_name.items():
            if needle in name_key:
                results.extend(items)
                if len(results) >= limit:
                    break
        return results[:limit]
