from __future__ import annotations

import asyncio
import importlib
import io
import os
import time
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

fcntl_module: ModuleType | None
try:
    fcntl_module = importlib.import_module("fcntl")
except ImportError:  # pragma: no cover - non-POSIX fallback
    fcntl_module = None

fcntl: ModuleType | None = fcntl_module


@dataclass(slots=True)
class FileLock:
    path: Path
    timeout_sec: float = 900.0
    poll_sec: float = 0.2

    _handle: io.TextIOWrapper | None = None

    def acquire(self) -> None:
        start = time.monotonic()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        handle = self.path.open("a+")
        try:
            while True:
                if fcntl is None:
                    raise RuntimeError("fcntl is not available for file locking on this platform")
                try:
                    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if self.timeout_sec and (time.monotonic() - start) >= self.timeout_sec:
                        raise TimeoutError(f"Timed out waiting for lock: {self.path}")
                    time.sleep(self.poll_sec)
            handle.seek(0)
            handle.truncate()
            handle.write(f"pid={os.getpid()}\n")
            handle.write(f"acquired_at={time.time():.6f}\n")
            handle.flush()
            self._handle = handle
        except Exception:
            handle.close()
            raise

    def release(self) -> None:
        handle = self._handle
        if handle is None:
            return
        try:
            if fcntl is not None:
                fcntl.flock(handle, fcntl.LOCK_UN)
        finally:
            handle.close()
            self._handle = None

    def __enter__(self) -> "FileLock":
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.release()


@dataclass(slots=True)
class AsyncFileLock:
    path: Path
    timeout_sec: float = 900.0
    poll_sec: float = 0.2

    _lock: FileLock | None = None

    async def acquire(self) -> None:
        if self._lock is None:
            self._lock = FileLock(self.path, timeout_sec=self.timeout_sec, poll_sec=self.poll_sec)
        await asyncio.to_thread(self._lock.acquire)

    async def release(self) -> None:
        lock = self._lock
        if lock is None:
            return
        await asyncio.to_thread(lock.release)

    async def __aenter__(self) -> "AsyncFileLock":
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.release()
