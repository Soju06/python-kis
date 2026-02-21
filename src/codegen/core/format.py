from __future__ import annotations

import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

from codegen.core.paths import project_root


def run_ruff_fix(paths: Iterable[Path], *, select: str = "F401,I") -> None:
    targets = [str(path) for path in paths if path.exists()]
    if not targets:
        return
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            "--fix",
            "--select",
            select,
            *targets,
        ],
        cwd=project_root(),
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    output = "\n".join(chunk for chunk in (stdout, stderr) if chunk)
    message = "ruff check --fix failed"
    if output:
        message = f"{message}:\n{output}"
    raise RuntimeError(message)


def run_ruff_format(paths: Iterable[Path]) -> None:
    targets = [str(path) for path in paths if path.exists()]
    if not targets:
        return
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "format", *targets],
        cwd=project_root(),
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    output = "\n".join(chunk for chunk in (stdout, stderr) if chunk)
    message = "ruff format failed"
    if output:
        message = f"{message}:\n{output}"
    raise RuntimeError(message)
