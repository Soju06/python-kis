from __future__ import annotations

from docsgen.portal import KisPortalClient
from docsgen.portal.models import ApiDetail, ApiInfo, Section


async def fetch_sections(client: KisPortalClient) -> list[Section]:
    return await client.fetch_sections()


async def fetch_api_list(client: KisPortalClient, section_id: str) -> list[ApiInfo]:
    return await client.fetch_api_list(section_id)


async def fetch_complete_api(client: KisPortalClient, api_info: ApiInfo) -> ApiDetail:
    return await client.fetch_complete_api(api_info)
