from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .paths import default_store_root, read_text, StorePaths

@dataclass(frozen=True, slots=True)
class StoreConfig:
    root: Path = field(default_factory=default_store_root)
    snapshot: str | None = None
    auto_refresh: bool = True

    def resolve_snapshot(self) -> Path:
        if self.snapshot:
            return self.root / "snapshots" / self.snapshot
        paths = StorePaths(self.root)
        latest = read_text(paths.latest_file)
        if latest:
            return paths.snapshot_date_dir(latest)
        return self.root / "snapshots" / "latest"
