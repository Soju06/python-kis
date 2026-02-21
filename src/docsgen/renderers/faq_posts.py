"""Markdown rendering for FAQ posts."""

from __future__ import annotations

from bs4 import BeautifulSoup

from docsgen.parsers.faq_posts import ForumPost
from docsgen.renderers.jinja_env import render_template


def _collapse_whitespace(text: str) -> str:
    return " ".join(text.split())


def html_to_markdown(html: str) -> str:
    """Best-effort HTML -> Markdown conversion for forum post bodies."""

    soup = BeautifulSoup(html, "html.parser")

    # Drop non-content tags early
    for tag in soup.select("script, style"):
        tag.decompose()

    # Convert <br> to newline
    for br in soup.find_all("br"):
        br.replace_with("\n")

    def render(node, *, indent: str = "") -> str:
        from bs4 import NavigableString, Tag

        if isinstance(node, NavigableString):
            return str(node)
        if not isinstance(node, Tag):
            return ""

        name = node.name.lower()

        if name in {"p", "div"}:
            inner = "".join(render(c, indent=indent) for c in node.children).strip()
            inner = inner.replace("\u00a0", " ")
            inner = inner.strip()
            if not inner:
                return ""
            return f"{inner}\n\n"

        if name in {"strong", "b"}:
            inner = _collapse_whitespace("".join(render(c, indent=indent) for c in node.children))
            return f"**{inner}**" if inner else ""

        if name in {"em", "i"}:
            inner = _collapse_whitespace("".join(render(c, indent=indent) for c in node.children))
            return f"*{inner}*" if inner else ""

        if name == "code":
            inner = _collapse_whitespace("".join(render(c, indent=indent) for c in node.children))
            return f"`{inner}`" if inner else ""

        if name == "pre":
            inner = "".join(render(c, indent=indent) for c in node.children).strip("\n")
            if not inner:
                return ""
            return f"```\n{inner}\n```\n\n"

        if name == "a":
            href = (node.get("href") or "").strip()
            text = _collapse_whitespace(node.get_text(" ", strip=True)) or href
            if not href:
                return text
            return f"[{text}]({href})"

        if name == "img":
            src = (node.get("src") or "").strip()
            alt = (node.get("alt") or "").strip()
            if not src:
                return ""
            return f"![{alt}]({src})"

        if name in {"ul", "ol"}:
            is_ordered = name == "ol"
            out_lines: list[str] = []
            idx = 1
            for li in node.find_all("li", recursive=False):
                li_text = render(li, indent=indent + "  ").strip()
                if not li_text:
                    continue
                prefix = f"{idx}. " if is_ordered else "- "
                out_lines.append(f"{indent}{prefix}{li_text}")
                idx += 1
            return ("\n".join(out_lines) + "\n\n") if out_lines else ""

        if name == "li":
            inner = "".join(render(c, indent=indent) for c in node.children)
            inner = inner.replace("\n\n", "\n").strip()
            return _collapse_whitespace(inner)

        if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(name[1])
            hashes = "#" * level
            text = _collapse_whitespace(node.get_text(" ", strip=True))
            return f"{hashes} {text}\n\n" if text else ""

        if name == "blockquote":
            text = _collapse_whitespace(node.get_text(" ", strip=True))
            if not text:
                return ""
            return "\n".join(f"> {line}" for line in text.splitlines()) + "\n\n"

        if name == "hr":
            return "---\n\n"

        if name == "table":
            rows = node.find_all("tr")
            if not rows:
                return ""
            rendered_rows: list[list[str]] = []
            for r in rows:
                cols = []
                for c in r.find_all(["th", "td"]):
                    cols.append(_collapse_whitespace(c.get_text(" ", strip=True)).replace("|", "\\|"))
                if cols:
                    rendered_rows.append(cols)
            if not rendered_rows:
                return ""
            header = rendered_rows[0]
            body = rendered_rows[1:] or []
            column_count = max(len(row) for row in rendered_rows)
            if len(header) < column_count:
                header = header + [""] * (column_count - len(header))
            lines = []
            lines.append("| " + " | ".join(header) + " |")
            lines.append("| " + " | ".join(["---"] * column_count) + " |")
            for r in body:
                if len(r) < column_count:
                    r = r + [""] * (column_count - len(r))
                lines.append("| " + " | ".join(r) + " |")
            return "\n".join(lines) + "\n\n"

        # Default: inline container
        return "".join(render(c, indent=indent) for c in node.children)

    out = "".join(render(c) for c in soup.contents)
    # Normalize excessive blank lines
    lines = out.splitlines()
    cleaned: list[str] = []
    blank_run = 0
    for ln in lines:
        if not ln.strip():
            blank_run += 1
            if blank_run <= 1:
                cleaned.append("")
            continue
        blank_run = 0
        cleaned.append(ln.rstrip())
    return "\n".join(cleaned).strip() + "\n"


def generate_faq_post_markdown(post: ForumPost) -> str:
    content = html_to_markdown(post.content_html).rstrip()
    return render_template("faq_post.md.jinja", post=post, content=content)
