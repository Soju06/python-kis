from __future__ import annotations

import asyncio
from collections.abc import Iterable

import httpx

from docsgen.portal import KisPortalClient


async def fetch_master_contents_body(client: KisPortalClient) -> str:
    return await client.fetch_category_contents_body()


async def fetch_header_payloads(
    header_urls: Iterable[str],
    *,
    timeout: float,
    concurrency: int,
) -> list[tuple[str, bytes]]:
    limiter = asyncio.Semaphore(concurrency)

    async def fetch_header(url: str, session: httpx.AsyncClient) -> tuple[str, bytes]:
        async with limiter:
            response = await session.get(url)
            response.raise_for_status()
            return url, response.content

    async with httpx.AsyncClient(timeout=timeout) as session:
        return await asyncio.gather(*(fetch_header(url, session) for url in header_urls))
