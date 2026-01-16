"""Markdown/YAML rendering for API documentation."""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING

from docsgen.renderers.jinja_env import render_template

if TYPE_CHECKING:
    from docsgen.portal.models import ApiDetail, ApiError, ApiProperty, Section


def normalize_filename(name: str) -> str:
    """Normalize API name to valid filename."""
    # Remove [category] prefix if present
    name = re.sub(r"^\[[^\]]+\]\s*", "", name)

    # Remove version/code suffix like [v1_국내주식-001]
    name = re.sub(r"\[v\d+_[^\]]+\]", "", name).strip()

    # Remove parentheses content for simplicity
    name = re.sub(r"\([^)]*\)", "", name).strip()

    # Replace spaces and special chars with hyphens
    name = re.sub(r"[^\w가-힣]+", "-", name)
    name = re.sub(r"-+", "-", name)
    name = name.strip("-")

    # Convert to lowercase
    return name.lower() if name else "unnamed"


def normalize_section_folder(section: Section) -> str:
    """Get normalized folder name for section."""
    # Create folder structure like: 국내주식/주문-계좌
    if section.category:
        category = re.sub(r"[^\w가-힣]+", "-", section.category).strip("-")
        subcategory = re.sub(r"[^\w가-힣]+", "-", section.subcategory).strip("-")
        return f"{category}/{subcategory}"
    return re.sub(r"[^\w가-힣]+", "-", section.subcategory).strip("-")


def html_to_text(html: str) -> str:
    """Convert HTML to plain text."""
    if not html:
        return ""

    # Replace <br/> and <br> with newlines
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)

    # Remove all other HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Decode HTML entities
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&amp;", "&")
    text = text.replace("&quot;", '"')
    text = text.replace("&#39;", "'")
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    return text.strip()


def get_type_name(property_type: str) -> str:
    """Convert property type code to readable name."""
    type_map = {
        "A0001": "String",
        "A0002": "String",
        "A0003": "String",
        "A0004": "Number",
        "A0005": "Object",
        "A0006": "Array",
    }
    return type_map.get(property_type, property_type)


def generate_property_table(properties: list[ApiProperty], title: str) -> str:
    """Generate markdown table for properties."""
    if not properties:
        return ""

    rows = []
    for prop in properties:
        desc = html_to_text(prop.description)
        # Escape pipe characters in description
        desc = desc.replace("|", "\\|").replace("\n", " ")
        # Truncate long descriptions
        if len(desc) > 100:
            desc = desc[:97] + "..."

        rows.append(
            {
                "code": prop.code,
                "name": prop.name,
                "type_name": get_type_name(prop.property_type),
                "length": prop.length,
                "required": "Y" if prop.required else "N",
                "desc": desc,
            }
        )

    return render_template("property_table.md.jinja", title=title, rows=rows)


def format_json_example(json_str: str) -> str:
    """Format JSON string for display."""
    if not json_str:
        return ""

    try:
        # Parse and re-format with indentation
        data = json.loads(json_str)
        return json.dumps(data, indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        # Return as-is if not valid JSON
        return json_str.strip()


def _normalize_tr_id(value: str | None) -> str | None:
    if not value:
        return None
    text = value.strip()
    return text or None


def generate_markdown(api: ApiDetail, section: Section) -> str:
    """Generate markdown documentation for an API."""
    summary_text = html_to_text(api.summary) if api.summary else ""
    description_text = ""
    if api.description and api.description != api.summary:
        description_text = html_to_text(api.description)

    metadata_items: list[dict[str, str]] = []
    if api.organization:
        metadata_items.append({"label": "제공 기관", "value": api.organization})
    if api.billing_policy:
        metadata_items.append({"label": "과금 정책", "value": api.billing_policy})
    if api.status:
        metadata_items.append({"label": "상태", "value": api.status})
    if api.created_date:
        date_str = api.created_date[:10] if len(api.created_date) >= 10 else api.created_date
        metadata_items.append({"label": "생성일", "value": date_str})
    if api.last_modified_date:
        date_str = api.last_modified_date[:10] if len(api.last_modified_date) >= 10 else api.last_modified_date
        metadata_items.append({"label": "최종 수정일", "value": date_str})

    real_tr_id = _normalize_tr_id(api.real_tr_id)
    demo_tr_id = _normalize_tr_id(api.demo_tr_id)

    request_tables = [
        generate_property_table(api.request_headers, "Headers"),
        generate_property_table(api.request_params, "Query Parameters"),
        generate_property_table(api.request_body, "Body"),
    ]
    request_tables = [table.rstrip() for table in request_tables if table]

    response_tables = [
        generate_property_table(api.response_headers, "Headers"),
        generate_property_table(api.response_body, "Body"),
    ]
    response_tables = [table.rstrip() for table in response_tables if table]

    errors = [
        {
            "code": err.code,
            "message": err.message,
            "description": html_to_text(err.description).replace("|", "\\|").replace("\n", " "),
        }
        for err in api.errors
    ]

    return render_template(
        "api_doc.md.jinja",
        api=api,
        section=section,
        summary=summary_text,
        description=description_text,
        real_tr_id=real_tr_id,
        demo_tr_id=demo_tr_id,
        metadata_items=metadata_items,
        request_tables=request_tables,
        response_tables=response_tables,
        request_example=format_json_example(api.request_example) if api.request_example else "",
        response_example=format_json_example(api.response_example) if api.response_example else "",
        errors=errors,
    )


def generate_yaml(api: ApiDetail, section: Section) -> dict:
    """Generate YAML-compatible dict for an API."""

    def prop_to_dict(prop: ApiProperty) -> dict:
        return {
            "code": prop.code,
            "name": prop.name,
            "type": prop.property_type,
            "type_name": get_type_name(prop.property_type),
            "length": prop.length,
            "required": prop.required,
            "description": html_to_text(prop.description),
        }

    def error_to_dict(err: ApiError) -> dict:
        return {
            "code": err.code,
            "message": err.message,
            "description": html_to_text(err.description),
        }

    # Parse examples as JSON if possible
    req_example_data = None
    if api.request_example:
        try:
            req_example_data = json.loads(api.request_example)
        except json.JSONDecodeError:
            req_example_data = api.request_example

    res_example_data = None
    if api.response_example:
        try:
            res_example_data = json.loads(api.response_example)
        except json.JSONDecodeError:
            res_example_data = api.response_example

    return {
        # 기본 정보
        "id": api.id,
        "name": api.name,
        "section": section.name,
        "category": section.category,
        "subcategory": section.subcategory,
        # HTTP 정보
        "method": api.http_method,
        "url": api.access_url,
        "content_type": api.content_type,
        "req_format": api.req_format,
        # 도메인
        "domains": {
            "real": api.real_domain,
            "demo": api.demo_domain,
        },
        "real_tr_id": api.real_tr_id,
        "demo_tr_id": api.demo_tr_id,
        # 설명
        "summary": html_to_text(api.summary),
        "description": html_to_text(api.description),
        # 메타데이터
        "metadata": {
            "organization": api.organization,
            "billing_policy": api.billing_policy,
            "status": api.status,
            "created_date": api.created_date,
            "last_modified_date": api.last_modified_date,
        },
        # 요청
        "request": {
            "headers": [prop_to_dict(p) for p in api.request_headers],
            "params": [prop_to_dict(p) for p in api.request_params],
            "body": [prop_to_dict(p) for p in api.request_body],
            "example": req_example_data,
        },
        # 응답
        "response": {
            "headers": [prop_to_dict(p) for p in api.response_headers],
            "body": [prop_to_dict(p) for p in api.response_body],
            "example": res_example_data,
        },
        # 오류 코드
        "errors": [error_to_dict(e) for e in api.errors],
    }
