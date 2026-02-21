from __future__ import annotations

from docsgen.portal import KisPortalClient


async def fetch_pinned_post_details(
    client: KisPortalClient,
    *,
    forum_id: str,
    page: int = 0,
    size: int = 500,
    sort: str = "fixOnTop,desc",
) -> list[dict[str, object]]:
    posts, _total = await client.fetch_forum_posts(
        forum_id=forum_id,
        page=page,
        size=size,
        sort=sort,
    )
    pinned_ids = [p.get("id") for p in posts if isinstance(p, dict) and p.get("fixOnTop") is True and p.get("id")]
    details: list[dict[str, object]] = []
    for post_id in pinned_ids:
        detail = await client.fetch_forum_post_detail(forum_id=forum_id, post_id=str(post_id))
        details.append(detail)
    return details
