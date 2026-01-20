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


def _has_import_line(text: str, module: str) -> bool:
    return any(line.strip() == f"import {module}" for line in text.splitlines())


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
        if "time.sleep" in updated and not _has_import_line(updated, "time"):
            if "import atexit" in updated:
                updated = updated.replace("import atexit", "import atexit\nimport time")
            else:
                updated = updated.replace("import asyncio", "import asyncio\nimport time")
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def _postprocess_store_sync(sync_dir: pathlib.Path) -> None:
    block = "\n".join(
        [
            "from pathlib import Path",
            "from sqlite3 import Row",
            "",
            "import pathlib",
            "import sqlite3",
            "from pydantic import BaseModel",
        ]
    )
    replacement = "\n".join(
        [
            "import pathlib",
            "import sqlite3",
            "from pathlib import Path",
            "from sqlite3 import Row",
            "",
            "from pydantic import BaseModel",
        ]
    )
    for path in sync_dir.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if block not in text:
            continue
        updated = text.replace(block, replacement)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def _postprocess_streaming_sync(sync_dir: pathlib.Path) -> None:
    for path in sync_dir.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        updated = text
        updated = updated.replace("asyncio.QueueEmpty", "queue.Empty")
        updated = updated.replace("asyncio.Queue", "queue.Queue")
        updated = updated.replace("asyncio.Lock", "threading.Lock")
        updated = updated.replace("asyncio.Task[None]", "threading.Thread")
        updated = updated.replace("asyncio.sleep", "time.sleep")
        updated = updated.replace("asyncio.CancelledError", "Exception")
        updated = updated.replace("websockets.connect", "websockets.sync.client.connect")
        updated = updated.replace(
            "    def connect(self) -> None:\n"
            "        if self._task is not None:\n"
            "            return\n"
            "        self._task = asyncio.create_task(self._run_loop())\n",
            "    def connect(self) -> None:\n"
            "        if self._task is not None:\n"
            "            return\n"
            "        self._task = threading.Thread(target=self._run_loop, daemon=True)\n"
            "        self._task.start()\n",
        )
        updated = updated.replace(
            "    def close(self) -> None:\n"
            "        self.reconnect = False\n"
            "        if self._task is not None:\n"
            "            self._task.cancel()\n"
            "            self._task = None\n"
            "        self.transport.close()\n",
            "    def close(self) -> None:\n"
            "        self.reconnect = False\n"
            "        self.transport.close()\n"
            "        if self._task is not None:\n"
            "            self._task.join(timeout=1.0)\n"
            "            self._task = None\n",
        )
        updated = updated.replace(
            "            except Exception:\n"
            "                return\n"
            "            except Exception:\n"
            "                self.transport.close()\n",
            "            except Exception:\n"
            "                self.transport.close()\n",
        )
        updated = updated.replace(
            "from typing import Iterator, Callable, Protocol",
            "from typing import Callable, Iterator, Protocol",
        )
        updated = updated.replace(
            "Callable[[], Awaitable[None]]",
            "Callable[[], None]",
        )
        updated = updated.replace(
            "from typing import Awaitable, Callable, Literal, Protocol",
            "from typing import Callable, Literal, Protocol",
        )
        if "threading." in updated and not _has_import_line(updated, "threading"):
            if "import asyncio" in updated:
                updated = updated.replace("import asyncio", "import asyncio\nimport threading")
            else:
                updated = "import threading\n" + updated
        if "queue.Queue" in updated and not _has_import_line(updated, "queue"):
            if "import asyncio" in updated:
                updated = updated.replace("import asyncio", "import asyncio\nimport queue")
            else:
                updated = "import queue\n" + updated
        if "queue.Empty" in updated and not _has_import_line(updated, "queue"):
            if "import asyncio" in updated:
                updated = updated.replace("import asyncio", "import asyncio\nimport queue")
            else:
                updated = "import queue\n" + updated
        if "time.sleep" in updated and not _has_import_line(updated, "time"):
            if "import asyncio" in updated:
                updated = updated.replace("import asyncio", "import asyncio\nimport time")
            else:
                updated = "import time\n" + updated
        if "import asyncio" in updated and "asyncio." not in updated:
            updated = updated.replace("import asyncio\n", "")
        updated = updated.replace(
            "import time\nimport threading\nimport json\n",
            "import json\nimport threading\nimport time\n",
        )
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def _targets(root: pathlib.Path) -> list[UnasyncTarget]:
    store_root = root / "src" / "pykis" / "store"
    api_root = root / "src" / "pykis" / "api"
    streaming_root = root / "src" / "pykis" / "streaming"
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
            postprocess=_postprocess_store_sync,
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
        UnasyncTarget(
            name="streaming",
            async_dir=streaming_root / "_async",
            sync_dir=streaming_root / "_sync",
            replacements={
                "_async": "_sync",
                "StreamingSession": "SyncStreamingSession",
                "SessionPool": "SyncSessionPool",
                "SessionEntry": "SyncSessionEntry",
                "SessionKey": "SyncSessionKey",
                "SubscriptionStream": "SyncSubscriptionStream",
                "SubscriptionRegistry": "SyncSubscriptionRegistry",
                "SubscriptionKey": "SyncSubscriptionKey",
                "StreamingEventRouter": "SyncStreamingEventRouter",
                "StreamQueue": "SyncStreamQueue",
                "WebSocketTransport": "SyncWebSocketTransport",
                "WebSocketRunner": "SyncWebSocketRunner",
                "AesCbcDecryptor": "SyncAesCbcDecryptor",
                "StreamingKeyStore": "SyncStreamingKeyStore",
                "aclose": "close",
                "asyncio.Lock": "threading.Lock",
                "asyncio.Queue": "queue.Queue",
                "asyncio.sleep": "time.sleep",
            },
            postprocess=_postprocess_streaming_sync,
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
