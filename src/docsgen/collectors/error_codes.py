from __future__ import annotations

from docsgen.portal import KisPortalClient


async def fetch_error_code_contents_body(client: KisPortalClient) -> str:
    return await client.fetch_error_code_contents_body()
