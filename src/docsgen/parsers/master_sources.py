"""Parse KIS portal master-file contents tables."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote, urlparse, urlunparse

from bs4 import BeautifulSoup


@dataclass(frozen=True, slots=True)
class MasterSource:
    """Master file source entry from the portal contents page."""

    source_id: str
    group: str
    label: str
    download_url: str
    header_url: str
    sample_code_url: str | None = None


_URL_RE = re.compile(r"`(https?://[^`]+)`")


def normalize_header_url(url: str) -> str:
    """Normalize GitHub blob URL to raw URL."""

    url = url.strip()
    if "github.com" in url and "/blob/" in url:
        prefix, rest = url.split("/blob/", 1)
        prefix = prefix.replace("https://github.com", "https://raw.githubusercontent.com")
        url = f"{prefix}/{rest}"

    parsed = urlparse(url)
    if not parsed.path:
        return url
    normalized_path = quote(unquote(parsed.path), safe="/")
    return urlunparse(parsed._replace(path=normalized_path))


def source_id_from_url(url: str) -> str:
    name = url.split("/")[-1]
    for suffix in (".mst.zip", ".cod.zip", ".mst", ".cod", ".zip"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    name = re.sub(r"[^a-zA-Z0-9_]+", "_", name)
    return name.strip("_")


def parse_master_contents_body(contents_body_html: str) -> list[MasterSource]:
    """Parse CATEGORY contentsBody HTML into master sources."""

    soup = BeautifulSoup(contents_body_html, "html.parser")
    sources: list[MasterSource] = []

    for section in soup.select("div.conts-area-item"):
        group_title = ""
        title_el = section.select_one("h2.cont-tit")
        if title_el:
            group_title = title_el.get_text(" ", strip=True)

        table = section.select_one("table")
        if table is None:
            continue

        current_group = group_title
        current_header_url: str | None = None
        current_sample_url: str | None = None
        for row in table.select("tbody tr"):
            cells = row.find_all(["th", "td"], recursive=False)
            if not cells:
                continue

            if row.find("th", scope="row"):
                current_group = cells[0].get_text(" ", strip=True) or current_group
                current_header_url = None
                current_sample_url = None
                label_cell = cells[1]
                action_cell = cells[2] if len(cells) > 2 else None
            else:
                label_cell = cells[0]
                action_cell = cells[1] if len(cells) > 1 else None

            download_link = label_cell.find("a") if label_cell else None
            if download_link is None:
                continue

            download_url = (download_link.get("href") or "").strip()
            label = download_link.get_text(" ", strip=True)

            header_url = ""
            sample_code_url: str | None = None
            if action_cell:
                for link in action_cell.find_all("a"):
                    text = link.get_text(" ", strip=True)
                    href = (link.get("href") or "").strip()
                    if not href or href == "#":
                        continue
                    if "헤더" in text:
                        header_url = href
                    elif "샘플" in text:
                        sample_code_url = href

            if header_url:
                current_header_url = header_url
            if sample_code_url:
                current_sample_url = sample_code_url

            if not header_url and current_header_url:
                header_url = current_header_url
            if sample_code_url is None and current_sample_url:
                sample_code_url = current_sample_url

            if not header_url:
                raise ValueError(f"Missing header URL for {label} ({download_url})")

            normalized_header = normalize_header_url(header_url)
            source_id = source_id_from_url(download_url)
            sources.append(
                MasterSource(
                    source_id=source_id,
                    group=current_group,
                    label=label,
                    download_url=download_url,
                    header_url=normalized_header,
                    sample_code_url=sample_code_url,
                )
            )

    return sources


def parse_reference_markdown(path: Path) -> list[MasterSource]:
    """Parse reference markdown table into master sources."""

    lines = path.read_text(encoding="utf-8").splitlines()
    sources: list[MasterSource] = []
    idx = 0
    current_group = ""
    while idx < len(lines):
        line = lines[idx]
        if line.startswith("### "):
            header = line[4:].strip()
            if header in {"국내", "해외"}:
                current_group = header
        if "| 구분 |" in line and "| 종목 |" in line:
            idx += 1
            while idx < len(lines) and not lines[idx].startswith("|---"):
                idx += 1
            idx += 1
            while idx < len(lines):
                row = lines[idx]
                if not row.strip().startswith("|") or row.startswith("### "):
                    break
                parts = [p.strip() for p in row.strip().strip("|").split("|")]
                if len(parts) < 4:
                    idx += 1
                    continue
                group = parts[0] or current_group
                label = parts[1]
                urls = _URL_RE.findall(row)
                if len(urls) >= 2:
                    download_url, header_url = urls[0], urls[1]
                    header_url = normalize_header_url(header_url)
                    sources.append(
                        MasterSource(
                            source_id=source_id_from_url(download_url),
                            group=group,
                            label=label,
                            download_url=download_url,
                            header_url=header_url,
                        )
                    )
                idx += 1
            continue
        idx += 1
    return sources


def compare_sources(expected: list[MasterSource], actual: list[MasterSource]) -> list[str]:
    """Compare expected vs actual sources and return mismatch messages."""

    errors: list[str] = []
    expected_map = {entry.source_id: entry for entry in expected}
    actual_map = {entry.source_id: entry for entry in actual}

    missing = sorted(set(expected_map) - set(actual_map))
    extra = sorted(set(actual_map) - set(expected_map))
    for source_id in missing:
        errors.append(f"Missing source in contents API: {source_id}")
    for source_id in extra:
        errors.append(f"Unexpected source from contents API: {source_id}")

    for source_id, expected_entry in expected_map.items():
        actual_entry = actual_map.get(source_id)
        if actual_entry is None:
            continue
        if expected_entry.group != actual_entry.group:
            errors.append(f"Group mismatch for {source_id}: {expected_entry.group} != {actual_entry.group}")
        if expected_entry.label != actual_entry.label:
            errors.append(f"Label mismatch for {source_id}: {expected_entry.label} != {actual_entry.label}")
        if expected_entry.download_url != actual_entry.download_url:
            errors.append(
                f"Download URL mismatch for {source_id}: {expected_entry.download_url} != {actual_entry.download_url}"
            )
        if expected_entry.header_url != actual_entry.header_url:
            errors.append(
                f"Header URL mismatch for {source_id}: {expected_entry.header_url} != {actual_entry.header_url}"
            )

    return errors
