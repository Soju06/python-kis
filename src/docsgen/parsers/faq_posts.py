"""FAQ forum posts ingestion for KIS API Portal."""

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
            item_map = {str(key): value for key, value in item.items()}
            name = (
                str(item_map.get("originalFileName", "") or "")
                or str(item_map.get("fileName", "") or "")
                or str(item_map.get("id", "") or "")
            ).strip()
            url = (
                str(item_map.get("downloadUrl", "") or "")
                or str(item_map.get("fileUrl", "") or "")
                or str(item_map.get("url", "") or "")
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
