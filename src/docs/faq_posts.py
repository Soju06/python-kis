"""FAQ forum posts ingestion for KIS API Portal.

This targets the '자주 묻는 질문' forum (a fixed forumId) and documents *pinned* posts.

Design:
- Fetching stays in `KisPortalClient` (network I/O).
- Parsing/transform is pure and typed.
"""

from __future__ import annotations

from dataclasses import dataclass

from bs4 import BeautifulSoup


FAQ_FORUM_ID = "10000000-0000-0011-0000-000000000002"


@dataclass(frozen=True, slots=True)
class ForumAttachment:
    """Attachment metadata (best-effort; shape depends on portal)."""

    name: str
    url: str


@dataclass(frozen=True, slots=True)
class ForumPost:
    """A forum post as used for documentation output."""

    forum_id: str
    post_id: str
    title: str
    created_date: str
    fix_on_top: bool
    title_highlight: bool
    content_html: str
    attachments: tuple[ForumAttachment, ...] = ()

    @property
    def source_url(self) -> str:
        return f"https://apiportal.koreainvestment.com/community/{self.forum_id}/post/{self.post_id}"


def rewrite_portal_relative_urls(html: str, *, base_url: str) -> str:
    """Rewrite relative URLs (starting with '/') to absolute portal URLs."""

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup.find_all(True):
        for attr in ("src", "href"):
            val = tag.get(attr)
            if not isinstance(val, str):
                continue
            val = val.strip()
            if val.startswith("/"):
                tag[attr] = base_url.rstrip("/") + val

    # Preserve HTML as-is; markdown renderers can handle inline HTML blocks.
    return str(soup)


def _collapse_whitespace(text: str) -> str:
    return " ".join(text.split())


def html_to_markdown(html: str) -> str:
    """Best-effort HTML -> Markdown conversion for forum post bodies.

    We keep this dependency-free (other than BeautifulSoup) so it works in offline builds.
    """

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
            return f"```\\n{inner}\\n```\\n\\n"

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
            lines = []
            lines.append("| " + " | ".join(header) + " |")
            lines.append("| " + " | ".join(["---"] * len(header)) + " |")
            for r in body:
                # pad/truncate to header length
                if len(r) < len(header):
                    r = r + [""] * (len(header) - len(r))
                lines.append("| " + " | ".join(r[: len(header)]) + " |")
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


def forum_post_from_detail_json(detail: dict[str, object], *, forum_id: str, base_url: str) -> ForumPost:
    """Build a ForumPost from the portal's post-detail JSON."""

    post_id = str(detail.get("id", "") or "")
    title = str(detail.get("title", "") or "")
    created_date = str(detail.get("createdDate", "") or "")
    fix_on_top = bool(detail.get("fixOnTop", False))
    title_highlight = bool(detail.get("titleHighlight", False))
    content_html_raw = str(detail.get("content", "") or "")

    content_html = rewrite_portal_relative_urls(content_html_raw, base_url=base_url)

    attachments_raw = detail.get("attachFileList") or []
    attachments: list[ForumAttachment] = []
    if isinstance(attachments_raw, list):
        for item in attachments_raw:
            if not isinstance(item, dict):
                continue
            name = (
                str(item.get("originalFileName", "") or "")
                or str(item.get("fileName", "") or "")
                or str(item.get("id", "") or "")
            ).strip()
            url = (
                str(item.get("downloadUrl", "") or "")
                or str(item.get("fileUrl", "") or "")
                or str(item.get("url", "") or "")
            ).strip()
            if url.startswith("/"):
                url = base_url.rstrip("/") + url
            if name and url:
                attachments.append(ForumAttachment(name=name, url=url))

    return ForumPost(
        forum_id=forum_id,
        post_id=post_id,
        title=title,
        created_date=created_date,
        fix_on_top=fix_on_top,
        title_highlight=title_highlight,
        content_html=content_html,
        attachments=tuple(attachments),
    )


