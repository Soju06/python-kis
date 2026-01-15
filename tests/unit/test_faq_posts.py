from __future__ import annotations

from docsgen.parsers.faq_posts import forum_post_from_detail_json, rewrite_portal_relative_urls
from docsgen.renderers.faq_posts import html_to_markdown


def test_rewrite_portal_relative_urls() -> None:
    html = '<p><img src=\"/files/download/public/image/abc\" /></p><a href=\"/community/x\">x</a>'
    out = rewrite_portal_relative_urls(html, base_url="https://apiportal.koreainvestment.com")
    assert "https://apiportal.koreainvestment.com/files/download/public/image/abc" in out
    assert "https://apiportal.koreainvestment.com/community/x" in out


def test_forum_post_from_detail_json_rewrites_content_and_attachments() -> None:
    detail = {
        "id": "post-123",
        "title": "테스트",
        "createdDate": "2026-01-01T00:00:00.000+0900",
        "fixOnTop": True,
        "titleHighlight": False,
        "content": '<p><img src=\"/files/download/public/image/abc\" /></p>',
        "attachFileList": [
            {"originalFileName": "a.txt", "downloadUrl": "/files/download/public/file/def"},
        ],
    }
    post = forum_post_from_detail_json(detail, forum_id="forum-1", base_url="https://apiportal.koreainvestment.com")
    assert post.post_id == "post-123"
    assert post.fix_on_top is True
    assert "https://apiportal.koreainvestment.com/files/download/public/image/abc" in post.content_html
    assert post.attachments[0].url == "https://apiportal.koreainvestment.com/files/download/public/file/def"


def test_html_to_markdown_basic_tags() -> None:
    md = html_to_markdown(
        '<p>Hello <b>World</b></p>'
        '<p><a href=\"https://example.com\">link</a></p>'
        '<p><img alt=\"a\" src=\"https://img\"/></p>'
        '<ul><li>one</li><li>two</li></ul>'
    )
    assert "Hello **World**" in md
    assert "[link](https://example.com)" in md
    assert "![a](https://img)" in md
    assert "- one" in md
    assert "- two" in md


