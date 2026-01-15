from __future__ import annotations

from dataclasses import dataclass, field


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
    demo_domain: str


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
    demo_domain: str

    # HTTP 정보
    http_method: str
    content_type: str
    req_format: str

    # TR ID
    tr_ids: dict[str, list[str]] = field(default_factory=dict)  # {"real": [...], "demo": [...]}
    real_tr_id: str = ""
    demo_tr_id: str = ""

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
