from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Callable

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.table import Table

from codegen.api.pipeline import run_pipeline as run_api_codegen
from codegen.core.paths import project_root
from codegen.store.pipeline import run_pipeline as run_store_codegen
from docsgen.cli import run as run_docs_sync
from pykis.logging import configure_logging


@dataclass(frozen=True, slots=True)
class Action:
    key: str
    label: str
    runner: Callable[[], int]


def _run_docs() -> int:
    root = project_root()
    return asyncio.run(run_docs_sync(root))


def _run_api() -> int:
    run_api_codegen()
    return 0


def _run_store() -> int:
    run_store_codegen(infer=True, refresh=True)
    return 0


def _build_actions() -> list[Action]:
    return [
        Action("1", "Docs sync (API docs + master docs)", _run_docs),
        Action("2", "API codegen (raw models)", _run_api),
        Action("3", "Store codegen (masters/raw structs)", _run_store),
    ]


def _render_menu(console: Console, actions: list[Action]) -> None:
    table = Table(title="pykis codegen", show_lines=True)
    table.add_column("Key", justify="right", style="bold")
    table.add_column("Action")
    for action in actions:
        table.add_row(action.key, action.label)
    console.print(table)
    console.print(Panel("Enter comma-separated keys (e.g. 1,3).", title="Select"))


def _parse_choice(choice: str, actions: list[Action]) -> list[Action]:
    lookup = {action.key: action for action in actions}
    selected: list[Action] = []
    for token in [part.strip() for part in choice.split(",") if part.strip()]:
        action = lookup.get(token)
        if action and action not in selected:
            selected.append(action)
    return selected


def main() -> None:
    configure_logging()
    console = Console()
    actions = _build_actions()
    _render_menu(console, actions)
    choice = Prompt.ask("Run", default="1")
    selected = _parse_choice(choice, actions)
    if not selected:
        console.print("[yellow]No valid selection. Exiting.[/yellow]")
        return

    results: list[tuple[str, int]] = []
    for action in selected:
        with Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            task_id = progress.add_task(f"{action.label}...", total=None)
            code = action.runner()
            progress.update(task_id, completed=1)
        results.append((action.label, code))

    summary = Table(title="Results")
    summary.add_column("Action")
    summary.add_column("Status", justify="right")
    for label, code in results:
        status = "OK" if code == 0 else f"ERR({code})"
        summary.add_row(label, status)
    console.print(summary)


if __name__ == "__main__":
    main()
