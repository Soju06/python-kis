from __future__ import annotations

from docsgen.parsers.faq_posts import ForumPost
from docsgen.sinks.faq_posts import save_faq_pinned_posts_docs


def test_save_faq_pinned_posts_docs_deletes_stale_files(tmp_path) -> None:
    base_dir = tmp_path / "docs" / "kis"
    faq_dir = base_dir / "FAQ" / "자주묻는질문"
    faq_dir.mkdir(parents=True)

    # Existing generated files (one stale, one will be replaced/kept)
    stale = faq_dir / "old-title-deadbeef.md"
    stale.write_text("<!-- generated: kis-docs-fetch -->\n# old\n", encoding="utf-8")
    keep_old_name = faq_dir / "same-title-aaaaaaaa.md"
    keep_old_name.write_text("<!-- generated: kis-docs-fetch -->\n# old\n", encoding="utf-8")

    posts = [
        ForumPost(
            forum_id="forum",
            post_id="aaaaaaaa-0000-0000-0000-000000000000",
            title="Same Title",
            created_date="",
            fix_on_top=True,
            title_highlight=False,
            content_html="<p>hi</p>",
            attachments=(),
        )
    ]

    written = save_faq_pinned_posts_docs(posts, base_dir)
    assert len(written) == 1
    assert written[0].exists()
    assert not stale.exists()
