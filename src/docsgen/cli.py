"""CLI entry point for KIS API documentation downloader."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from docsgen.config import DocsGenConfig
from docsgen.paths import project_root as resolve_project_root
from docsgen.pipeline import run_pipeline
from pykis.logging import configure_logging, get_logger


def get_project_root() -> Path:
    return resolve_project_root()


async def run(project_root: Path) -> int:
    """Async entry point for CLI."""
    config = DocsGenConfig.from_project_root(project_root)

    configure_logging()
    logger = get_logger(__name__)
    logger.info("KIS API Documentation Downloader")
    logger.info("Output directory: %s", config.output_dir)

    report = await run_pipeline(config, logger=logger)

    if report.failed_master:
        return 1
    return 0 if report.failed_apis == 0 else 1


def main() -> int:
    """Main entry point for CLI."""
    root = get_project_root()
    return asyncio.run(run(root))


if __name__ == "__main__":
    sys.exit(main())
