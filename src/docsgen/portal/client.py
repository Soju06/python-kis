from __future__ import annotations

import asyncio
import json
import re
from typing import Mapping

import httpx

from docsgen.portal.models import ApiDetail, ApiError, ApiInfo, ApiProperty, Section

BASE_URL = "https://apiportal.koreainvestment.com"
SUMMARY_PATH = "/apiservice-summary"
CONTENTS_KIND_PATH = "/api/contents/kind"
FORUMS_PATH_PREFIX = "/api/forums"

DEFAULT_HEADERS: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json, text/html, */*",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
}
DEFAULT_TIMEOUT = 8.0


class KisPortalClient:
    """Async client for KIS API Portal (docsgen only)."""

    base_url: str
    delay: float
    _client: httpx.AsyncClient
    _owns_client: bool
    _closed: bool

    __slots__ = ("base_url", "delay", "_client", "_owns_client", "_closed")

    def __init__(
        self,
        *,
        base_url: str | None = None,
        delay: float = 0.3,
        client: httpx.AsyncClient | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: float | None = None,
    ) -> None:
        """Initialize client.

        Args:
            base_url: Base portal URL (defaults to KIS API Portal).
            delay: Delay between requests in seconds to avoid rate limiting.
            client: Optional pre-configured httpx.AsyncClient.
            headers: Additional headers to merge with defaults.
            timeout: Timeout in seconds for new clients.
        """
        self.base_url = base_url or BASE_URL
        self.delay = delay
        self._closed = False
        if client is None:
            merged_headers = dict(DEFAULT_HEADERS)
            if headers:
                merged_headers.update(headers)
            self._client = httpx.AsyncClient(timeout=timeout or DEFAULT_TIMEOUT, headers=merged_headers)
            self._owns_client = True
        else:
            self._client = client
            self._owns_client = False

    async def __aenter__(self) -> KisPortalClient:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._closed:
            return
        self._closed = True
        if self._owns_client:
            await self._client.aclose()

    async def _sleep(self) -> None:
        if self.delay > 0:
            await asyncio.sleep(self.delay)

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    async def _get(
        self,
        url: str,
        *,
        params: Mapping[str, str | int | float | None] | None = None,
    ) -> httpx.Response:
        """Make GET request with delay."""
        if self._closed:
            raise RuntimeError("KisPortalClient is closed")
        await self._sleep()
        response = await self._client.get(url, params=params)
        response.raise_for_status()
        return response

    async def fetch_sections(self) -> list[Section]:
        """Fetch all API sections/categories from the summary page."""
        response = await self._get(self._url(SUMMARY_PATH))
        html = response.text

        pattern = r'<option\s+value="([^"]+)">\s*([^<]+)\s*</option>'
        matches = re.findall(pattern, html)

        sections: list[Section] = []
        for section_id, name in matches:
            name = name.strip()
            if not name or not section_id:
                continue

            category_match = re.match(r"\[([^\]]+)\]\s*(.+)", name)
            if category_match:
                category = category_match.group(1)
                subcategory = category_match.group(2).strip()
            else:
                category = ""
                subcategory = name

            sections.append(
                Section(
                    id=section_id,
                    name=name,
                    category=category,
                    subcategory=subcategory,
                )
            )

        return sections

    async def fetch_api_list(self, section_id: str) -> list[ApiInfo]:
        """Fetch list of APIs in a section."""
        url = self._url(f"/api/apis/public/api-list/{section_id}")
        response = await self._get(url)
        data = response.json()

        apis: list[ApiInfo] = []
        for item in data:
            apis.append(
                ApiInfo(
                    id=item.get("id", ""),
                    name=item.get("name", ""),
                    access_url=item.get("accessUrl", ""),
                    description=item.get("description", ""),
                    real_domain=item.get("realDomain", ""),
                    demo_domain=item.get("virtualDomain", ""),
                )
            )

        return apis

    async def fetch_api_detail(self, access_url: str) -> dict[str, object]:
        """Fetch API detail by access URL."""
        url = self._url("/api/apis/public/detail")
        response = await self._get(url, params={"accessUrl": access_url})
        return response.json()

    async def fetch_api_properties(self, api_id: str) -> list[dict[str, object]]:
        """Fetch API properties (request/response fields)."""
        url = self._url(f"/api/apis/guide/property/{api_id}")
        response = await self._get(url)
        return response.json()

    async def fetch_contents_body(self, *, title: str, kind: str = "CONTENTS") -> str:
        """Fetch a contents body by title/kind from the portal."""
        response = await self._get(self._url(CONTENTS_KIND_PATH), params={"title": title, "kind": kind})
        data = response.json()
        return str(data.get("contentsBody", "") or "")

    async def fetch_error_code_contents_body(self) -> str:
        """Fetch the FAQ error-code page contents body (HTML)."""
        return await self.fetch_contents_body(title="ERRORCODE")

    async def fetch_category_contents_body(self) -> str:
        """Fetch the CATEGORY contents body (HTML)."""
        return await self.fetch_contents_body(title="CATEGORY")

    async def fetch_forum_posts(
        self,
        *,
        forum_id: str,
        page: int = 0,
        size: int = 50,
        sort: str = "fixOnTop,desc",
        extra_params: dict[str, str] | None = None,
    ) -> tuple[list[dict[str, object]], int]:
        """Fetch forum post list."""
        url = self._url(f"{FORUMS_PATH_PREFIX}/{forum_id}/posts")
        params: dict[str, str | int] = {"page": page, "size": size, "sort": sort}
        if extra_params:
            params.update(extra_params)

        response = await self._get(url, params=params)
        total = int(response.headers.get("X-Total-Count", "0") or "0")
        data = response.json()
        if not isinstance(data, list):
            raise TypeError(f"Expected list response from {url}, got {type(data).__name__}")
        return data, total

    async def fetch_forum_post_detail(self, *, forum_id: str, post_id: str) -> dict[str, object]:
        """Fetch forum post detail (includes HTML content)."""
        url = self._url(f"{FORUMS_PATH_PREFIX}/{forum_id}/posts/{post_id}")
        response = await self._get(url)
        data = response.json()
        if not isinstance(data, dict):
            raise TypeError(f"Expected object response from {url}, got {type(data).__name__}")
        return data

    def _parse_http_method(self, detail: dict[str, object]) -> str:
        """Parse HTTP method from detail response."""
        if detail.get("httpMethod"):
            return str(detail["httpMethod"])

        children_str = detail.get("children")
        if not isinstance(children_str, str):
            children_str = "[]"
        if children_str:
            try:
                children = json.loads(children_str)
                if isinstance(children, list):
                    for child in children:
                        if not isinstance(child, dict):
                            continue
                        param_list = child.get("paramList", [])
                        if not isinstance(param_list, list):
                            continue
                        for param in param_list:
                            if not isinstance(param, dict):
                                continue
                            if param.get("name") == "methodList":
                                methods = param.get("value", [])
                                if isinstance(methods, list) and methods:
                                    return str(methods[0])
            except (json.JSONDecodeError, TypeError):
                pass

        return "GET"

    def _infer_real_tr_id(self, name: str, description: str) -> str:
        """Infer real TR ID from name/description when missing."""
        tr_pattern = r"([A-Z]{4}\d{4}[A-Z])"
        match = re.search(tr_pattern, f"{description} {name}")
        return match.group(1) if match else ""

    def _parse_properties(
        self, raw_props: list[dict[str, object]]
    ) -> tuple[
        list[ApiProperty],
        list[ApiProperty],
        list[ApiProperty],
        list[ApiProperty],
        list[ApiProperty],
        list[ApiProperty],
    ]:
        """Parse and organize properties by type."""
        properties: list[ApiProperty] = []
        request_headers: list[ApiProperty] = []
        request_params: list[ApiProperty] = []
        request_body: list[ApiProperty] = []
        response_headers: list[ApiProperty] = []
        response_body: list[ApiProperty] = []

        def _normalize_property_code(code: str) -> str:
            normalized = code.strip()
            if normalized.startswith("-") and len(normalized) > 1 and normalized[1].isalnum():
                normalized = normalized.lstrip("-").strip()
            return normalized

        for prop in raw_props:
            raw_code = str(prop.get("propertyCd", "") or "")
            api_prop = ApiProperty(
                code=_normalize_property_code(raw_code),
                name=str(prop.get("propertyNm", "") or ""),
                body_type=str(prop.get("bodyType", "") or ""),
                property_type=str(prop.get("propertyType", "") or ""),
                length=str(prop.get("propertyLength", "") or ""),
                order=str(prop.get("propertyOrder", "") or ""),
                required=prop.get("requireYn", "N") == "Y",
                description=str(prop.get("description", "") or ""),
            )
            properties.append(api_prop)

            body_type = api_prop.body_type
            if body_type == "req_h":
                request_headers.append(api_prop)
            elif body_type == "req_p":
                request_params.append(api_prop)
            elif body_type == "req_b":
                request_body.append(api_prop)
            elif body_type == "res_h":
                response_headers.append(api_prop)
            elif body_type == "res_b":
                response_body.append(api_prop)

        for prop_list in [request_headers, request_params, request_body, response_headers, response_body]:
            prop_list.sort(key=lambda p: p.order)

        return properties, request_headers, request_params, request_body, response_headers, response_body

    def _parse_errors(self, api_errors: list[dict[str, object]]) -> list[ApiError]:
        """Parse API error codes."""
        errors: list[ApiError] = []
        for err in api_errors:
            errors.append(
                ApiError(
                    code=str(err.get("errorCode", "") or ""),
                    message=str(err.get("errorMessage", "") or ""),
                    description=str(err.get("description", "") or ""),
                )
            )
        return errors

    async def fetch_complete_api(self, api_info: ApiInfo) -> ApiDetail:
        """Fetch complete API details including properties."""
        detail = await self.fetch_api_detail(api_info.access_url)

        name = str(detail.get("name", api_info.name) or "")
        description = str(detail.get("description", "") or api_info.description or "")
        summary = str(detail.get("apiSummary", "") or "")

        http_method = self._parse_http_method(detail)
        content_type = str(detail.get("contentType", "application/json") or "application/json")
        req_format = str(detail.get("reqFormat", "JSON") or "JSON")

        real_tr_id = str(detail.get("realTrId", "") or "")
        demo_tr_id = str(detail.get("virtualTrId", "") or "")
        if not real_tr_id:
            real_tr_id = self._infer_real_tr_id(name, description)

        request_example = str(detail.get("reqExample", "") or "")
        response_example = str(detail.get("resAuth", "") or detail.get("resNoAuth", "") or "")

        organization = ""
        organization_payload = detail.get("organization")
        if isinstance(organization_payload, dict):
            organization_map = {str(key): value for key, value in organization_payload.items()}
            organization = str(organization_map.get("name", "") or "")

        billing_policy = ""
        billing_payload = detail.get("billingPolicy")
        if isinstance(billing_payload, dict):
            billing_map = {str(key): value for key, value in billing_payload.items()}
            billing_policy = str(billing_map.get("name", "") or "")

        status = str(detail.get("status", "") or "")
        created_date = str(detail.get("createdDate", "") or "")
        last_modified_date = str(detail.get("lastModifiedDate", "") or "")

        raw_props = detail.get("apiPropertys")
        if not isinstance(raw_props, list) or not raw_props:
            raw_props = await self.fetch_api_properties(api_info.id)
        raw_props = [{str(key): value for key, value in item.items()} for item in raw_props if isinstance(item, dict)]

        (
            properties,
            request_headers,
            request_params,
            request_body,
            response_headers,
            response_body,
        ) = self._parse_properties(raw_props)

        api_errors = detail.get("apiErrors")
        error_list = (
            [{str(key): value for key, value in item.items()} for item in api_errors if isinstance(item, dict)]
            if isinstance(api_errors, list)
            else []
        )
        errors = self._parse_errors(error_list)

        return ApiDetail(
            id=api_info.id,
            name=name,
            access_url=api_info.access_url,
            description=description,
            summary=summary,
            real_domain=str(detail.get("realDomain", api_info.real_domain) or ""),
            demo_domain=str(detail.get("virtualDomain", api_info.demo_domain) or ""),
            http_method=http_method,
            content_type=content_type,
            req_format=req_format,
            real_tr_id=real_tr_id,
            demo_tr_id=demo_tr_id,
            request_example=request_example,
            response_example=response_example,
            organization=organization,
            billing_policy=billing_policy,
            status=status,
            created_date=created_date,
            last_modified_date=last_modified_date,
            properties=properties,
            request_headers=request_headers,
            request_params=request_params,
            request_body=request_body,
            response_headers=response_headers,
            response_body=response_body,
            errors=errors,
        )
