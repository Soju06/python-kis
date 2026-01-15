"""Markdown rendering for portal error codes."""

from __future__ import annotations

from docsgen.parsers.error_codes import ErrorCodeEntry
from docsgen.renderers.jinja_env import render_template


def generate_error_codes_markdown(entries: list[ErrorCodeEntry], *, source_url: str) -> str:
    """Generate markdown for the portal-wide error codes list."""

    # Keep stable ordering: category order as encountered, then code ascending within.
    categories: dict[str, list[ErrorCodeEntry]] = {}
    for e in entries:
        categories.setdefault(e.category, []).append(e)
    for cat_entries in categories.values():
        cat_entries.sort(key=lambda x: x.code)

    category_rows = [
        {
            "name": category,
            "entries": [
                {"code": entry.code, "message": entry.message.replace("|", "\\|")}
                for entry in cat_entries
            ],
        }
        for category, cat_entries in categories.items()
    ]

    return render_template("error_codes.md.jinja", source_url=source_url, categories=category_rows)
