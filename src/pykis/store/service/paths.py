from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


def default_store_root() -> Path:
    return Path("~/.pykis/store").expanduser()


def today_key() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def read_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip() or None


@dataclass(frozen=True, slots=True)
class StorePaths:
    root: Path

    @property
    def cache_dir(self) -> Path:
        return self.root / "cache"

    @property
    def snapshot_dir(self) -> Path:
        return self.root / "snapshots"

    @property
    def lock_dir(self) -> Path:
        return self.root / "locks"

    @property
    def latest_file(self) -> Path:
        return self.snapshot_dir / "latest.txt"

    def cache_date_dir(self, date_key: str) -> Path:
        return self.cache_dir / date_key

    def snapshot_date_dir(self, date_key: str) -> Path:
        return self.snapshot_dir / date_key

    def snapshot_db_path(self, date_key: str) -> Path:
        return self.snapshot_date_dir(date_key) / "store.sqlite"

    def snapshot_manifest_path(self, date_key: str) -> Path:
        return self.snapshot_date_dir(date_key) / "manifest.json"

    def snapshot_done_path(self, date_key: str) -> Path:
        return self.snapshot_date_dir(date_key) / "DONE"

    def snapshot_lock_path(self, date_key: str) -> Path:
        return self.lock_dir / f"snapshot-{date_key}.lock"
