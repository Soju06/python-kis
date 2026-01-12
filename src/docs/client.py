"""HTTP client for KIS API Portal."""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field

import requests


BASE_URL = "https://apiportal.koreainvestment.com"
SUMMARY_URL = f"{BASE_URL}/apiservice-summary"
ERROR_CODE_CONTENTS_URL = f"{BASE_URL}/api/contents/kind"
FORUMS_URL_PREFIX = f"{BASE_URL}/api/forums"


@dataclass(slots=True)
class Section:
    """API section/category information."""

    id: str
    name: str
    category: str  # e.g., "국내주식", "해외주식"
    subcategory: str  # e.g., "주문/계좌", "기본시세"


@dataclass(slots=True)
class ApiInfo:
    """Basic API information from list."""

    id: str
    name: str
    access_url: str
    description: str
    real_domain: str
    virtual_domain: str


@dataclass(slots=True)
class ApiProperty:
    """API request/response property."""

    code: str
    name: str
    body_type: str  # req_h, req_b, req_p, res_h, res_b
    property_type: str
    length: str
    order: str
    required: bool
    description: str


@dataclass(slots=True)
class ApiError:
    """API error code information."""

    code: str
    message: str
    description: str


@dataclass(slots=True)
class ApiDetail:
    """Complete API detail information."""

    # 기본 정보
    id: str
    name: str
    access_url: str
    description: str
    summary: str  # apiSummary
    real_domain: str
    virtual_domain: str

    # HTTP 정보
    http_method: str
    content_type: str
    req_format: str

    # TR ID
    tr_ids: dict[str, list[str]] = field(default_factory=dict)  # {"real": [...], "virtual": [...]}
    real_tr_id: str = ""
    virtual_tr_id: str = ""

    # 요청/응답 예시
    request_example: str = ""
    response_example: str = ""

    # 메타데이터
    organization: str = ""
    billing_policy: str = ""
    status: str = ""
    created_date: str = ""
    last_modified_date: str = ""

    # Properties
    properties: list[ApiProperty] = field(default_factory=list)
    request_headers: list[ApiProperty] = field(default_factory=list)
    request_params: list[ApiProperty] = field(default_factory=list)
    request_body: list[ApiProperty] = field(default_factory=list)
    response_headers: list[ApiProperty] = field(default_factory=list)
    response_body: list[ApiProperty] = field(default_factory=list)

    # Errors
    errors: list[ApiError] = field(default_factory=list)


class KisPortalClient:
    """Client for KIS API Portal."""

    __slots__ = ("session", "delay")

    def __init__(self, delay: float = 0.3) -> None:
        """Initialize client.

        Args:
            delay: Delay between requests in seconds to avoid rate limiting.
        """
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "application/json, text/html, */*",
                "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            }
        )
        self.delay = delay

    def _get(self, url: str, **kwargs: object) -> requests.Response:
        """Make GET request with delay."""
        time.sleep(self.delay)
        response = self.session.get(url, **kwargs)
        response.raise_for_status()
        return response

    def fetch_sections(self) -> list[Section]:
        """Fetch all API sections/categories from the summary page.

        Returns:
            List of Section objects.
        """
        response = self._get(SUMMARY_URL)
        html = response.text

        # Parse <option value="uuid">섹션명</option>
        pattern = r'<option\s+value="([^"]+)">\s*([^<]+)\s*</option>'
        matches = re.findall(pattern, html)

        sections: list[Section] = []
        for section_id, name in matches:
            name = name.strip()
            if not name or not section_id:
                continue

            # Parse category and subcategory from name
            # e.g., "[국내주식] 주문/계좌" -> category="국내주식", subcategory="주문/계좌"
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

    def fetch_api_list(self, section_id: str) -> list[ApiInfo]:
        """Fetch list of APIs in a section.

        Args:
            section_id: Section UUID.

        Returns:
            List of ApiInfo objects.
        """
        url = f"{BASE_URL}/api/apis/public/api-list/{section_id}"
        response = self._get(url)
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
                    virtual_domain=item.get("virtualDomain", ""),
                )
            )

        return apis

    def fetch_api_detail(self, access_url: str) -> dict[str, object]:
        """Fetch API detail by access URL.

        Args:
            access_url: API access URL path (e.g., "/uapi/domestic-stock/v1/trading/order-cash").

        Returns:
            Raw API detail response.
        """
        url = f"{BASE_URL}/api/apis/public/detail"
        response = self._get(url, params={"accessUrl": access_url})
        return response.json()

    def fetch_api_properties(self, api_id: str) -> list[dict[str, object]]:
        """Fetch API properties (request/response fields).

        Args:
            api_id: API UUID.

        Returns:
            List of property dictionaries.
        """
        url = f"{BASE_URL}/api/apis/guide/property/{api_id}"
        response = self._get(url)
        return response.json()

    def fetch_error_code_contents_body(self) -> str:
        """Fetch the FAQ error-code page contents body (HTML).

        The portal page (`/faq-error-code`) loads its content via:
            GET /api/contents/kind?title=ERRORCODE&kind=CONTENTS

        Returns:
            HTML string contained in `contentsBody`.
        """
        response = self._get(ERROR_CODE_CONTENTS_URL, params={"title": "ERRORCODE", "kind": "CONTENTS"})
        data = response.json()
        return str(data.get("contentsBody", "") or "")

    def fetch_forum_posts(
        self,
        *,
        forum_id: str,
        page: int = 0,
        size: int = 50,
        sort: str = "fixOnTop,desc",
        extra_params: dict[str, str] | None = None,
    ) -> tuple[list[dict[str, object]], int]:
        """Fetch forum post list.

        The portal uses headers for total count:
          - X-Total-Count: total rows

        Returns:
            (posts, total_count)
        """
        url = f"{FORUMS_URL_PREFIX}/{forum_id}/posts"
        params: dict[str, str | int] = {"page": page, "size": size, "sort": sort}
        if extra_params:
            params.update(extra_params)

        response = self._get(url, params=params)
        total = int(response.headers.get("X-Total-Count", "0") or "0")
        data = response.json()
        if not isinstance(data, list):
            raise TypeError(f"Expected list response from {url}, got {type(data).__name__}")
        return data, total

    def fetch_forum_post_detail(self, *, forum_id: str, post_id: str) -> dict[str, object]:
        """Fetch forum post detail (includes HTML content)."""
        url = f"{FORUMS_URL_PREFIX}/{forum_id}/posts/{post_id}"
        response = self._get(url)
        data = response.json()
        if not isinstance(data, dict):
            raise TypeError(f"Expected object response from {url}, got {type(data).__name__}")
        return data

    def _parse_http_method(self, detail: dict[str, object]) -> str:
        """Parse HTTP method from detail response."""
        # First try direct httpMethod field
        if detail.get("httpMethod"):
            return detail["httpMethod"]

        # Fallback to parsing from children
        children_str = detail.get("children", "[]")
        if children_str:
            try:
                children = json.loads(children_str)
                for child in children:
                    param_list = child.get("paramList", [])
                    for param in param_list:
                        if param.get("name") == "methodList":
                            methods = param.get("value", [])
                            if methods:
                                return methods[0]
            except (json.JSONDecodeError, TypeError):
                pass

        return "GET"

    def _parse_tr_ids(self, detail: dict[str, object], name: str, desc: str) -> dict[str, list[str]]:
        """Parse TR IDs from detail response."""
        tr_ids: dict[str, list[str]] = {"real": [], "virtual": []}

        # Direct fields
        if detail.get("realTrId"):
            tr_ids["real"].append(detail["realTrId"])
        if detail.get("virtualTrId"):
            tr_ids["virtual"].append(detail["virtualTrId"])

        # Extract from name/description
        tr_pattern = r"([A-Z]{4}\d{4}[A-Z])"
        tr_matches = re.findall(tr_pattern, desc + " " + name)
        for tr_id in tr_matches:
            if tr_id not in tr_ids["real"]:
                tr_ids["real"].append(tr_id)

        return tr_ids

    def _parse_properties(self, raw_props: list[dict[str, object]]) -> tuple[
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

        for prop in raw_props:
            api_prop = ApiProperty(
                code=prop.get("propertyCd", ""),
                name=prop.get("propertyNm", ""),
                body_type=prop.get("bodyType", ""),
                property_type=prop.get("propertyType", ""),
                length=prop.get("propertyLength", ""),
                order=prop.get("propertyOrder", ""),
                required=prop.get("requireYn", "N") == "Y",
                description=prop.get("description", ""),
            )
            properties.append(api_prop)

            # Organize by type
            bt = api_prop.body_type
            if bt == "req_h":
                request_headers.append(api_prop)
            elif bt == "req_p":
                request_params.append(api_prop)
            elif bt == "req_b":
                request_body.append(api_prop)
            elif bt == "res_h":
                response_headers.append(api_prop)
            elif bt == "res_b":
                response_body.append(api_prop)

        # Sort by order
        for prop_list in [request_headers, request_params, request_body, response_headers, response_body]:
            prop_list.sort(key=lambda p: p.order)

        return properties, request_headers, request_params, request_body, response_headers, response_body

    def _parse_errors(self, api_errors: list[dict[str, object]]) -> list[ApiError]:
        """Parse API error codes."""
        errors: list[ApiError] = []
        for err in api_errors:
            errors.append(
                ApiError(
                    code=err.get("errorCode", ""),
                    message=err.get("errorMessage", ""),
                    description=err.get("description", ""),
                )
            )
        return errors

    def fetch_complete_api(self, api_info: ApiInfo) -> ApiDetail:
        """Fetch complete API details including properties.

        Args:
            api_info: Basic API information.

        Returns:
            Complete ApiDetail object.
        """
        # Get detail
        detail = self.fetch_api_detail(api_info.access_url)

        # Basic info
        name = detail.get("name", api_info.name)
        desc = detail.get("description", "") or api_info.description or ""
        summary = detail.get("apiSummary", "") or ""

        # HTTP info
        http_method = self._parse_http_method(detail)
        content_type = detail.get("contentType", "application/json")
        req_format = detail.get("reqFormat", "JSON")

        # TR IDs
        tr_ids = self._parse_tr_ids(detail, name, desc)
        real_tr_id = detail.get("realTrId", "")
        virtual_tr_id = detail.get("virtualTrId", "")

        # Examples
        request_example = detail.get("reqExample", "") or ""
        response_example = detail.get("resAuth", "") or detail.get("resNoAuth", "") or ""

        # Metadata
        organization = ""
        if detail.get("organization"):
            organization = detail["organization"].get("name", "")

        billing_policy = ""
        if detail.get("billingPolicy"):
            billing_policy = detail["billingPolicy"].get("name", "")

        status = detail.get("status", "")
        created_date = detail.get("createdDate", "")
        last_modified_date = detail.get("lastModifiedDate", "")

        # Properties - prefer apiPropertys from detail, fallback to separate API call
        raw_props = detail.get("apiPropertys", [])
        if not raw_props:
            raw_props = self.fetch_api_properties(api_info.id)

        (
            properties,
            request_headers,
            request_params,
            request_body,
            response_headers,
            response_body,
        ) = self._parse_properties(raw_props)

        # Errors
        errors = self._parse_errors(detail.get("apiErrors", []))

        return ApiDetail(
            id=api_info.id,
            name=name,
            access_url=api_info.access_url,
            description=desc,
            summary=summary,
            real_domain=detail.get("realDomain", api_info.real_domain),
            virtual_domain=detail.get("virtualDomain", api_info.virtual_domain),
            http_method=http_method,
            content_type=content_type,
            req_format=req_format,
            tr_ids=tr_ids,
            real_tr_id=real_tr_id,
            virtual_tr_id=virtual_tr_id,
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
