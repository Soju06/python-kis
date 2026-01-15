from __future__ import annotations

from pathlib import Path

from docsgen.parsers.error_codes import ErrorCodeEntry
from docsgen.renderers.error_codes import generate_error_codes_markdown


def save_error_codes_docs(entries: list[ErrorCodeEntry], base_dir: Path) -> Path:
    """Save portal error codes markdown under docs/kis."""

    md_path = base_dir / "오류코드.md"
    md_path.write_text(
        generate_error_codes_markdown(entries, source_url="https://apiportal.koreainvestment.com/faq-error-code"),
        encoding="utf-8",
    )
    return md_path
