"""Documentation ingestion and generation tooling."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from docsgen.config import DocsGenConfig
    from docsgen.pipeline import DocsGenReport, run_pipeline

__all__ = ["DocsGenConfig", "DocsGenReport", "run_pipeline"]


def __getattr__(name: str):
    if name == "DocsGenConfig":
        from docsgen.config import DocsGenConfig

        return DocsGenConfig
    if name == "DocsGenReport":
        from docsgen.pipeline import DocsGenReport

        return DocsGenReport
    if name == "run_pipeline":
        from docsgen.pipeline import run_pipeline

        return run_pipeline
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(__all__)
