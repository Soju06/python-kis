import logging
import pathlib
import shutil
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

import unasync

if TYPE_CHECKING:
    from hatchling.builders.hooks.plugin.interface import BuildHookInterface
else:
    try:
        from hatchling.builders.hooks.plugin.interface import BuildHookInterface
    except ImportError:  # pragma: no cover - optional for local script runs
        class BuildHookInterface:
            pass


logger = logging.getLogger(__name__)


PostProcessor = Callable[[pathlib.Path], None]


@dataclass(frozen=True, slots=True)
class UnasyncTarget:
    name: str
    async_dir: pathlib.Path
    sync_dir: pathlib.Path
    replacements: dict[str, str]
    postprocess: PostProcessor | None = None


def _build_target(target: UnasyncTarget) -> None:
    if not target.async_dir.exists():
        logger.warning("unasync target missing: %s (%s)", target.name, target.async_dir)
        return

    if target.sync_dir.exists():
        shutil.rmtree(target.sync_dir)

    rules = [
        unasync.Rule(
            fromdir=str(target.async_dir),
            todir=str(target.sync_dir),
            additional_replacements=target.replacements,
        ),
    ]

    filepaths = [str(path) for path in target.async_dir.rglob("*.py")]
    if not filepaths:
        logger.warning("unasync target empty: %s (%s)", target.name, target.async_dir)
        return

    unasync.unasync_files(filepaths, rules)
    if target.postprocess:
        target.postprocess(target.sync_dir)
    logger.info("unasync target complete: %s", target.name)


def _postprocess_api_sync(sync_dir: pathlib.Path) -> None:
    replacements = {
        "httpx.SyncClient": "httpx.Client",
        "asyncio.sleep": "time.sleep",
        "asyncio.run(self.close())": "self.close()",
        "KisRawClient still open; call aclose() explicitly.": "SyncKisRawClient still open; call close() explicitly.",
    }
    for path in sync_dir.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        updated = text
        for before, after in replacements.items():
            updated = updated.replace(before, after)
        if "time.sleep" in updated and "import time" not in updated:
            updated = updated.replace("import asyncio", "import asyncio\nimport time")
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def _targets(root: pathlib.Path) -> list[UnasyncTarget]:
    store_root = root / "src" / "pykis" / "store"
    api_root = root / "src" / "pykis" / "api"
    return [
        UnasyncTarget(
            name="store",
            async_dir=store_root / "_async",
            sync_dir=store_root / "_sync",
            replacements={
                "_async": "_sync",
                "aiopath": "pathlib",
                "AsyncPath": "Path",
                "ensure_daily_snapshot_async": "ensure_daily_snapshot",
                "build_snapshot_async": "build_snapshot",
                "aiosqlite": "sqlite3",
                "MasterStore": "SyncMasterStore",
                "aclose": "close",
            },
        ),
        UnasyncTarget(
            name="api",
            async_dir=api_root / "_async",
            sync_dir=api_root / "_sync",
            replacements={
                "_async": "_sync",
                "KisRawClient": "SyncKisRawClient",
                "aclose": "close",
                "httpx.AsyncClient": "httpx.Client",
            },
            postprocess=_postprocess_api_sync,
        ),
    ]


def build_sync_code() -> None:
    root = pathlib.Path(__file__).resolve().parent.parent
    for target in _targets(root):
        _build_target(target)
    logger.info("Async to sync transformation complete.")


class UnasyncBuildHook(BuildHookInterface):
    def initialize(self, version, build_data) -> None:
        build_sync_code()


if __name__ == "__main__":
    build_sync_code()
