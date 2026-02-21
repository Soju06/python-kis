from __future__ import annotations

import re
from pathlib import Path

from docsgen.parsers.faq_posts import ForumPost
from docsgen.renderers.api_docs import normalize_filename
from docsgen.renderers.faq_posts import generate_faq_post_markdown


def save_faq_pinned_posts_docs(posts: list[ForumPost], base_dir: Path) -> list[Path]:
    """Save one markdown file per pinned FAQ post."""
    faq_dir = base_dir / "FAQ" / "자주묻는질문"
    faq_dir.mkdir(parents=True, exist_ok=True)

    expected_names: set[str] = set()
    written: list[Path] = []
    for post in posts:
        slug = normalize_filename(post.title)
        expected_name = f"{slug}-{post.post_id[:8]}.md"
        expected_names.add(expected_name)
        md_path = faq_dir / expected_name
        md_path.write_text(generate_faq_post_markdown(post), encoding="utf-8")
        written.append(md_path)

    # Cleanup: delete previously generated pinned-post docs that are no longer present.
    # We only manage files that match our naming convention `*-{8hex}.md` OR contain our marker.
    managed_name_re = re.compile(r".+-[0-9a-f]{8}\\.md$")
    for existing in faq_dir.glob("*.md"):
        if existing.name in expected_names:
            continue
        should_manage = bool(managed_name_re.match(existing.name))
        if not should_manage:
            try:
                content = existing.read_text(encoding="utf-8", errors="ignore")
                if "<!-- generated: kis-docs-fetch -->" in content:
                    should_manage = True
            except OSError:
                continue
        if should_manage:
            existing.unlink()

    return written
