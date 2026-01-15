from __future__ import annotations

from pathlib import Path

import yaml

from docsgen.parsers.master_headers import MasterStruct
from docsgen.parsers.master_sources import MasterSource
from docsgen.renderers.masters import (
    group_sources,
    render_master_index_yaml,
    render_master_readme,
    render_struct_markdown,
    render_struct_yaml,
)


def save_master_docs(
    *,
    output_dir: Path,
    sources: list[MasterSource],
    structs: list[MasterStruct],
    source_url: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    grouped, folder_map = group_sources(sources)
    structs_by_header: dict[str, list[MasterStruct]] = {}
    for struct in structs:
        structs_by_header.setdefault(struct.header_url, []).append(struct)

    readme_path = output_dir / "README.md"
    readme_path.write_text(render_master_readme(sources, source_url=source_url), encoding="utf-8")

    index_path = output_dir / "index.yaml"
    index_payload = render_master_index_yaml(sources)
    index_path.write_text(
        yaml.safe_dump(index_payload, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )

    expected_files: set[Path] = {readme_path, index_path}
    expected_dirs: set[Path] = {output_dir}

    for group, group_sources in grouped.items():
        folder = output_dir / folder_map[group]
        folder.mkdir(parents=True, exist_ok=True)
        expected_dirs.add(folder)

        group_structs: list[MasterStruct] = []
        seen: set[str] = set()
        for source in group_sources:
            for struct in structs_by_header.get(source.header_url, []):
                if struct.name in seen:
                    continue
                seen.add(struct.name)
                group_structs.append(struct)

        for struct in group_structs:
            md_path = folder / f"{struct.name}.md"
            md_path.write_text(render_struct_markdown(struct), encoding="utf-8")
            expected_files.add(md_path)

            yaml_path = folder / f"{struct.name}.yaml"
            yaml_payload = render_struct_yaml(struct)
            yaml_path.write_text(
                yaml.safe_dump(yaml_payload, allow_unicode=True, sort_keys=False, width=120),
                encoding="utf-8",
            )
            expected_files.add(yaml_path)

    for path in output_dir.rglob("*"):
        if path.is_file() and path not in expected_files:
            path.unlink()

    for path in sorted(output_dir.rglob("*"), reverse=True):
        if path.is_dir() and path not in expected_dirs:
            try:
                path.rmdir()
            except OSError:
                pass
