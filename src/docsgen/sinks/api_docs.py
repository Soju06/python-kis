from __future__ import annotations

from pathlib import Path

import yaml

from docsgen.portal.models import ApiDetail, Section
from docsgen.renderers.api_docs import (
    generate_markdown,
    generate_yaml,
    normalize_filename,
    normalize_section_folder,
)


def save_api_docs(api: ApiDetail, section: Section, base_dir: Path) -> tuple[Path, Path]:
    """Save API documentation as markdown and YAML files."""
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
