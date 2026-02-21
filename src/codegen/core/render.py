from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from codegen.core.text import format_annotated_type, format_inline_literal, format_string_literal, wrap_display_text


def _template_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "templates"


@lru_cache(maxsize=1)
def _env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(_template_dir()),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        undefined=StrictUndefined,
    )
    env.filters["repr"] = repr
    env.filters["inline_literal"] = format_inline_literal
    env.filters["string_literal"] = format_string_literal
    env.filters["annotated_type"] = format_annotated_type
    env.filters["wrap_text"] = _wrap_text
    return env


def _wrap_text(value: str, width: int = 100) -> str:
    return wrap_display_text(value, width=width)


def render_template(name: str, **context: Any) -> str:
    template = _env().get_template(name)
    return template.render(**context)
