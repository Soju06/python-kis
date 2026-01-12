"""CLI entry point for KIS API documentation downloader."""

from __future__ import annotations

import sys
from pathlib import Path

from .client import KisPortalClient
from .error_codes import parse_error_code_contents_body
from .faq_posts import FAQ_FORUM_ID, forum_post_from_detail_json
from .generator import normalize_section_folder, save_api_docs, save_error_codes_docs, save_faq_pinned_posts_docs


def get_project_root() -> Path:
    """Get the project root directory.

    Returns:
        Path to project root.
    """
    # Start from this file's directory and go up until we find pyproject.toml
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent

    # Fallback to current working directory
    return Path.cwd()


def main() -> int:
    """Main entry point for CLI.

    Downloads KIS API documentation and saves as markdown/yaml files.

    Returns:
        Exit code (0 for success).
    """
    project_root = get_project_root()
    docs_dir = project_root / "docs" / "kis"

    print(f"🚀 KIS API Documentation Downloader")
    print(f"📁 Output directory: {docs_dir}")
    print()

    # Initialize client
    client = KisPortalClient(delay=0.2)

    # Fetch all sections
    print("📋 Fetching API sections...")
    sections = client.fetch_sections()
    print(f"   Found {len(sections)} sections")

    total_apis = 0
    failed_apis = 0

    for section in sections:
        section_folder = normalize_section_folder(section)
        print(f"\n📂 {section.name}")
        print(f"   → {section_folder}")

        # Fetch APIs in this section
        try:
            apis = client.fetch_api_list(section.id)
        except Exception as e:
            print(f"   ❌ Failed to fetch API list: {e}")
            continue

        print(f"   Found {len(apis)} APIs")

        for api_info in apis:
            try:
                # Fetch complete API details
                api_detail = client.fetch_complete_api(api_info)

                # Save documentation
                md_path, yaml_path = save_api_docs(api_detail, section, docs_dir)

                total_apis += 1
                print(f"   ✅ {api_info.name}")
                print(f"      → {md_path.relative_to(project_root)}")

            except Exception as e:
                failed_apis += 1
                print(f"   ❌ {api_info.name}: {e}")

    # Fetch + generate portal-wide error codes doc (no additional CLI options).
    try:
        print("\n📋 Fetching FAQ error codes...")
        contents_body = client.fetch_error_code_contents_body()
        error_entries = parse_error_code_contents_body(contents_body)
        md_path = save_error_codes_docs(error_entries, docs_dir)
        print(f"   ✅ 오류코드")
        print(f"      → {md_path.relative_to(project_root)}")
    except Exception as e:
        print(f"   ❌ Failed to fetch/save 오류코드: {e}")

    # Fetch + generate pinned FAQ posts (자주 묻는 질문) (no additional CLI options).
    try:
        print("\n📋 Fetching pinned FAQ posts...")
        posts, _total = client.fetch_forum_posts(
            forum_id=FAQ_FORUM_ID,
            page=0,
            size=500,
            sort="fixOnTop,desc",
        )
        pinned_ids = [p.get("id") for p in posts if isinstance(p, dict) and p.get("fixOnTop") is True and p.get("id")]
        faq_posts = []
        for pid in pinned_ids:
            detail = client.fetch_forum_post_detail(forum_id=FAQ_FORUM_ID, post_id=str(pid))
            faq_posts.append(forum_post_from_detail_json(detail, forum_id=FAQ_FORUM_ID, base_url="https://apiportal.koreainvestment.com"))

        written = save_faq_pinned_posts_docs(faq_posts, docs_dir)
        print(f"   ✅ 자주 묻는 질문(상단고정) {len(written)}건")
        if written:
            print(f"      → {written[0].parent.relative_to(project_root)}/")
    except Exception as e:
        print(f"   ❌ Failed to fetch/save 자주 묻는 질문(상단고정): {e}")

    print()
    print("=" * 60)
    print(f"✨ Done! Downloaded {total_apis} APIs")
    if failed_apis > 0:
        print(f"⚠️  Failed: {failed_apis} APIs")
    print(f"📁 Output: {docs_dir}")

    return 0 if failed_apis == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

