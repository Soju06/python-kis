from __future__ import annotations

from pathlib import Path


def project_root(start: Path | None = None) -> Path:
    current = (start or Path(__file__)).resolve()
    if current.is_file():
        current = current.parent
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    return Path.cwd()


def docs_root(root: Path | None = None) -> Path:
    return project_root(root) / "docs" / "kis"


def store_docs_root(root: Path | None = None) -> Path:
    return docs_root(root) / "종목정보파일"
