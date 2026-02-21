from __future__ import annotations

import shutil
from pathlib import Path

RUFF_CONFIG_NAME = "ruff.toml"
DEFAULT_GROUP_KEEP_FILES = frozenset({"__init__.py"})


def raw_keep_files(*names: str) -> set[str]:
    return {RUFF_CONFIG_NAME, *names}


def clean_dir_keep_files(root: Path, keep_files: set[str]) -> None:
    if not root.exists():
        return
    for child in root.iterdir():
        if child.is_file():
            if child.name in keep_files:
                continue
            child.unlink()
        elif child.is_dir():
            shutil.rmtree(child)


def clean_structs_dir(
    structs_dir: Path,
    *,
    root_keep_files: set[str],
    keep_dirs: set[str],
    group_keep_files: set[str] | None = None,
) -> None:
    structs_dir.mkdir(parents=True, exist_ok=True)
    for path in structs_dir.glob("*.py"):
        if path.name not in root_keep_files:
            path.unlink()
    for path in structs_dir.iterdir():
        if not path.is_dir():
            continue
        if path.name not in keep_dirs:
            shutil.rmtree(path)
            continue
        keep_group_files = group_keep_files or set(DEFAULT_GROUP_KEEP_FILES)
        for module_path in path.glob("*.py"):
            if module_path.name not in keep_group_files:
                module_path.unlink()
