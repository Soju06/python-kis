"""Markdown and YAML generator for API documentation."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from .client import ApiDetail, ApiError, ApiProperty, Section
    from .error_codes import ErrorCodeEntry
    from .faq_posts import ForumPost


def normalize_filename(name: str) -> str:
    """Normalize API name to valid filename.

    Args:
        name: Original API name.

    Returns:
        Normalized filename (without extension).
    """
    # Remove [category] prefix if present
    name = re.sub(r"^\[[^\]]+\]\s*", "", name)

    # Extract core name and code if present
    # e.g., "주식주문(현금)[v1_국내주식-001]" -> "order-cash"
    # or just use the Korean name normalized

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
    """Get normalized folder name for section.

    Args:
        section: Section object.

    Returns:
        Folder name.
    """
    # Create folder structure like: 국내주식/주문-계좌
    if section.category:
        category = re.sub(r"[^\w가-힣]+", "-", section.category).strip("-")
        subcategory = re.sub(r"[^\w가-힣]+", "-", section.subcategory).strip("-")
        return f"{category}/{subcategory}"
    else:
        return re.sub(r"[^\w가-힣]+", "-", section.subcategory).strip("-")


def html_to_text(html: str) -> str:
    """Convert HTML to plain text.

    Args:
        html: HTML string.

    Returns:
        Plain text.
    """
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
    """Convert property type code to readable name.

    Args:
        property_type: Property type code (e.g., "A0001").

    Returns:
        Readable type name.
    """
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
    """Generate markdown table for properties.

    Args:
        properties: List of ApiProperty objects.
        title: Table title.

    Returns:
        Markdown table string.
    """
    if not properties:
        return ""

    lines = [
        f"### {title}",
        "",
        "| 필드명 | 한글명 | 타입 | 길이 | 필수 | 설명 |",
        "|--------|--------|------|------|------|------|",
    ]

    for prop in properties:
        desc = html_to_text(prop.description)
        # Escape pipe characters in description
        desc = desc.replace("|", "\\|").replace("\n", " ")
        # Truncate long descriptions
        if len(desc) > 100:
            desc = desc[:97] + "..."

        required = "Y" if prop.required else "N"
        type_name = get_type_name(prop.property_type)
        lines.append(
            f"| `{prop.code}` | {prop.name} | {type_name} | {prop.length} | {required} | {desc} |"
        )

    lines.append("")
    return "\n".join(lines)


def format_json_example(json_str: str) -> str:
    """Format JSON string for display.

    Args:
        json_str: Raw JSON string.

    Returns:
        Formatted JSON string.
    """
    if not json_str:
        return ""

    try:
        # Parse and re-format with indentation
        data = json.loads(json_str)
        return json.dumps(data, indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        # Return as-is if not valid JSON
        return json_str.strip()


def generate_markdown(api: ApiDetail, section: Section) -> str:
    """Generate markdown documentation for an API.

    Args:
        api: ApiDetail object.
        section: Section this API belongs to.

    Returns:
        Markdown content.
    """
    lines = [
        f"# {api.name}",
        "",
        f"> {section.name}",
        "",
    ]

    # Summary (apiSummary)
    if api.summary:
        summary_text = html_to_text(api.summary)
        lines.extend([summary_text, ""])

    # Description
    if api.description and api.description != api.summary:
        desc_text = html_to_text(api.description)
        if desc_text:
            lines.extend([desc_text, ""])

    # Basic info table
    lines.extend(
        [
            "## 기본 정보",
            "",
            "| 항목 | 상세 내용 |",
            "| :--- | :--- |",
            f"| **API ID** | `{api.id}` |",
            f"| **HTTP Method** | `{api.http_method}` |",
            f"| **URL** | `{api.access_url}` |",
            f"| **Content-Type** | `{api.content_type}` |",
            f"| **요청 포맷** | `{api.req_format}` |",
            f"| **실전 도메인** | `{api.real_domain}` |",
            f"| **모의 도메인** | `{api.virtual_domain}` |",
        ]
    )

    # TR IDs in table
    all_tr_ids = list(set(api.tr_ids.get("real", []) + api.tr_ids.get("virtual", [])))
    if api.real_tr_id and api.real_tr_id not in all_tr_ids:
        all_tr_ids.append(api.real_tr_id)
    if api.virtual_tr_id and api.virtual_tr_id not in all_tr_ids:
        all_tr_ids.append(api.virtual_tr_id)

    if all_tr_ids:
        tr_str = ", ".join(f"`{tr}`" for tr in all_tr_ids)
        lines.append(f"| **TR ID** | {tr_str} |")

    lines.append("")

    # Metadata section
    if api.organization or api.billing_policy or api.status or api.created_date or api.last_modified_date:
        lines.extend(["## 메타 정보", ""])
        if api.organization:
            lines.append(f"- **제공 기관**: {api.organization}")
        if api.billing_policy:
            lines.append(f"- **과금 정책**: {api.billing_policy}")
        if api.status:
            lines.append(f"- **상태**: {api.status}")
        if api.created_date:
            date_str = api.created_date[:10] if len(api.created_date) >= 10 else api.created_date
            lines.append(f"- **생성일**: {date_str}")
        if api.last_modified_date:
            date_str = api.last_modified_date[:10] if len(api.last_modified_date) >= 10 else api.last_modified_date
            lines.append(f"- **최종 수정일**: {date_str}")
        lines.append("")

    # Request
    lines.extend(["## 요청 (Request)", ""])

    if api.request_headers:
        lines.append(generate_property_table(api.request_headers, "Headers"))

    if api.request_params:
        lines.append(generate_property_table(api.request_params, "Query Parameters"))

    if api.request_body:
        lines.append(generate_property_table(api.request_body, "Body"))

    if not api.request_headers and not api.request_params and not api.request_body:
        lines.extend(["(요청 명세 없음)", ""])

    # Request example
    if api.request_example:
        formatted_req = format_json_example(api.request_example)
        lines.extend(
            [
                "### 요청 예시",
                "",
                "```json",
                formatted_req,
                "```",
                "",
            ]
        )

    # Response
    lines.extend(["## 응답 (Response)", ""])

    if api.response_headers:
        lines.append(generate_property_table(api.response_headers, "Headers"))

    if api.response_body:
        lines.append(generate_property_table(api.response_body, "Body"))

    if not api.response_headers and not api.response_body:
        lines.extend(["(응답 명세 없음)", ""])

    # Response example
    if api.response_example:
        formatted_res = format_json_example(api.response_example)
        lines.extend(
            [
                "### 응답 예시",
                "",
                "```json",
                formatted_res,
                "```",
                "",
            ]
        )

    # Error codes
    if api.errors:
        lines.extend(
            [
                "## 오류 코드",
                "",
                "| 코드 | 메시지 | 설명 |",
                "|------|--------|------|",
            ]
        )
        for err in api.errors:
            err_desc = html_to_text(err.description).replace("|", "\\|").replace("\n", " ")
            lines.append(f"| `{err.code}` | {err.message} | {err_desc} |")
        lines.append("")

    return "\n".join(lines)


def generate_yaml(api: ApiDetail, section: Section) -> dict:
    """Generate YAML-compatible dict for an API.

    Args:
        api: ApiDetail object.
        section: Section this API belongs to.

    Returns:
        Dictionary suitable for YAML export.
    """

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

    # Collect all TR IDs
    all_tr_ids = list(set(api.tr_ids.get("real", []) + api.tr_ids.get("virtual", [])))
    if api.real_tr_id and api.real_tr_id not in all_tr_ids:
        all_tr_ids.append(api.real_tr_id)
    if api.virtual_tr_id and api.virtual_tr_id not in all_tr_ids:
        all_tr_ids.append(api.virtual_tr_id)

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
            "virtual": api.virtual_domain,
        },
        # TR ID
        "tr_ids": all_tr_ids,
        "real_tr_id": api.real_tr_id,
        "virtual_tr_id": api.virtual_tr_id,
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


def save_api_docs(api: ApiDetail, section: Section, base_dir: Path) -> tuple[Path, Path]:
    """Save API documentation as markdown and YAML files.

    Args:
        api: ApiDetail object.
        section: Section this API belongs to.
        base_dir: Base directory for docs (e.g., docs/kis).

    Returns:
        Tuple of (markdown_path, yaml_path).
    """
    # Create folder structure
    folder_name = normalize_section_folder(section)
    folder_path = base_dir / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)

    # Generate filename from access_url
    # e.g., "/uapi/domestic-stock/v1/trading/order-cash" -> "order-cash"
    url_parts = api.access_url.rstrip("/").split("/")
    filename = url_parts[-1] if url_parts else normalize_filename(api.name)

    # Save markdown
    md_path = folder_path / f"{filename}.md"
    md_content = generate_markdown(api, section)
    md_path.write_text(md_content, encoding="utf-8")

    # Save YAML
    yaml_path = folder_path / f"{filename}.yaml"
    yaml_content = generate_yaml(api, section)
    yaml_str = yaml.dump(
        yaml_content,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=120,
    )
    yaml_path.write_text(yaml_str, encoding="utf-8")

    return md_path, yaml_path


def generate_error_codes_markdown(entries: list["ErrorCodeEntry"], *, source_url: str) -> str:
    """Generate markdown for the portal-wide error codes list."""

    # Keep stable ordering: category order as encountered, then code ascending within.
    categories: dict[str, list["ErrorCodeEntry"]] = {}
    for e in entries:
        categories.setdefault(e.category, []).append(e)
    for cat_entries in categories.values():
        cat_entries.sort(key=lambda x: x.code)

    lines: list[str] = []
    lines.append("# 오류코드")
    lines.append("")
    lines.append(f"- 출처: [{source_url}]({source_url})")
    lines.append("")
    lines.append("이 문서는 KIS Developers FAQ 오류코드 페이지에서 자동 수집/생성되었습니다.")

    for category, cat_entries in categories.items():
        lines.append("")
        lines.append(f"## {category}")
        lines.append("")
        lines.append("| 코드 | 메시지 |")
        lines.append("|---|---|")
        for e in cat_entries:
            msg = e.message.replace("|", "\\|")
            lines.append(f"| `{e.code}` | {msg} |")

    lines.append("")
    return "\n".join(lines)


def save_error_codes_docs(entries: list["ErrorCodeEntry"], base_dir: Path) -> Path:
    """Save portal error codes markdown under docs/kis."""

    # New canonical location requested: docs/kis/오류코드.md
    # Clean up legacy location if it exists.
    legacy = base_dir / "FAQ" / "오류코드.md"
    if legacy.exists():
        legacy.unlink()

    md_path = base_dir / "오류코드.md"
    md_path.write_text(
        generate_error_codes_markdown(entries, source_url="https://apiportal.koreainvestment.com/faq-error-code"),
        encoding="utf-8",
    )
    return md_path


def generate_faq_post_markdown(post: "ForumPost") -> str:
    from .faq_posts import html_to_markdown

    lines: list[str] = []
    lines.append("<!-- generated: kis-docs-fetch -->")
    lines.append(f"# {post.title}")
    lines.append("")
    lines.append(f"- 출처: [{post.source_url}]({post.source_url})")
    lines.append(f"- 작성일: `{post.created_date}`")
    lines.append("")
    lines.append("## 내용")
    lines.append("")
    lines.append(html_to_markdown(post.content_html))

    if post.attachments:
        lines.append("")
        lines.append("## 첨부파일")
        lines.append("")
        for a in post.attachments:
            lines.append(f"- [{a.name}]({a.url})")

    lines.append("")
    return "\n".join(lines)


def save_faq_pinned_posts_docs(posts: list["ForumPost"], base_dir: Path) -> list[Path]:
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
                head = existing.read_text(encoding="utf-8", errors="ignore")[:200]
                if "<!-- generated: kis-docs-fetch -->" in head:
                    should_manage = True
            except OSError:
                continue
        if should_manage:
            existing.unlink()

    return written
