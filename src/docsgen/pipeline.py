from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from docsgen.collectors.api_docs import fetch_api_list, fetch_complete_api, fetch_sections
from docsgen.collectors.error_codes import fetch_error_code_contents_body
from docsgen.collectors.faq_posts import fetch_pinned_post_details
from docsgen.collectors.masters import fetch_header_payloads, fetch_master_contents_body
from docsgen.config import DocsGenConfig
from docsgen.parsers.error_codes import parse_error_code_contents_body
from docsgen.parsers.faq_posts import forum_post_from_detail_json
from docsgen.parsers.master_headers import decode_header_bytes, merge_structs, parse_header_structs
from docsgen.parsers.master_sources import compare_sources, parse_master_contents_body, parse_reference_markdown
from docsgen.portal import KisPortalClient
from docsgen.renderers.api_docs import normalize_section_folder
from docsgen.sinks.api_docs import save_api_docs
from docsgen.sinks.error_codes import save_error_codes_docs
from docsgen.sinks.faq_posts import save_faq_pinned_posts_docs
from docsgen.sinks.masters import save_master_docs


@dataclass(frozen=True, slots=True)
class DocsGenReport:
    total_apis: int
    failed_apis: int
    failed_master: bool
    error_codes_written: bool
    faq_posts_written: int
    master_docs_written: bool


async def run_pipeline(config: DocsGenConfig, *, logger: logging.Logger | None = None) -> DocsGenReport:
    log = logger or logging.getLogger(__name__)
    total_apis = 0
    failed_apis = 0
    failed_master = False
    error_codes_written = False
    faq_posts_written = 0
    master_docs_written = False

    async with KisPortalClient(delay=config.portal_delay, base_url=config.portal_base_url) as client:
        log.info("Fetching API sections...")
        sections = await fetch_sections(client)
        log.info("Found %s sections", len(sections))

        for section in sections:
            section_folder = normalize_section_folder(section)
            log.info("Section %s -> %s", section.name, section_folder)

            try:
                apis = await fetch_api_list(client, section.id)
            except Exception as exc:
                log.error("Failed to fetch API list: %s", exc)
                continue

            log.info("Found %s APIs", len(apis))

            for api_info in apis:
                try:
                    api_detail = await fetch_complete_api(client, api_info)
                    md_path, _yaml_path = await asyncio.to_thread(
                        save_api_docs, api_detail, section, config.output_dir
                    )
                    total_apis += 1
                    log.info("Saved %s -> %s", api_info.name, md_path.relative_to(config.project_root))
                except Exception as exc:
                    failed_apis += 1
                    log.error("Failed to save %s: %s", api_info.name, exc)

        try:
            log.info("Fetching FAQ error codes...")
            contents_body = await fetch_error_code_contents_body(client)
            error_entries = parse_error_code_contents_body(contents_body)
            md_path = await asyncio.to_thread(save_error_codes_docs, error_entries, config.output_dir)
            error_codes_written = True
            log.info("Saved 오류코드 -> %s", md_path.relative_to(config.project_root))
        except Exception as exc:
            log.error("Failed to fetch/save 오류코드: %s", exc)

        try:
            log.info("Fetching master file contents...")
            contents_body = await fetch_master_contents_body(client)
            sources = parse_master_contents_body(contents_body)

            if config.master_reference_path and config.master_reference_path.exists():
                reference_sources = parse_reference_markdown(config.master_reference_path)
                mismatches = compare_sources(reference_sources, sources)
                if mismatches:
                    for mismatch in mismatches:
                        log.error("Master sources mismatch: %s", mismatch)
                    raise RuntimeError("Master sources mismatch against reference markdown.")

            unique_headers = sorted({source.header_url for source in sources})
            header_results = await fetch_header_payloads(
                unique_headers,
                timeout=config.header_timeout,
                concurrency=config.header_concurrency,
            )

            struct_list = []
            for header_url, payload in header_results:
                header_text = decode_header_bytes(payload)
                struct_list.extend(parse_header_structs(header_text, header_url))

            structs = merge_structs(struct_list)

            master_dir = config.output_dir / "종목정보파일"
            await asyncio.to_thread(
                save_master_docs,
                output_dir=master_dir,
                sources=sources,
                structs=structs,
                source_url=config.master_source_url,
            )
            master_docs_written = True
            log.info("Saved master file docs -> %s", master_dir.relative_to(config.project_root))
        except Exception as exc:
            failed_master = True
            log.error("Failed to fetch/save master file docs: %s", exc)

        try:
            log.info("Fetching pinned FAQ posts...")
            details = await fetch_pinned_post_details(client, forum_id=config.faq_forum_id)
            faq_posts = [
                forum_post_from_detail_json(
                    detail,
                    forum_id=config.faq_forum_id,
                    base_url=config.portal_base_url,
                )
                for detail in details
            ]
            written = await asyncio.to_thread(save_faq_pinned_posts_docs, faq_posts, config.output_dir)
            faq_posts_written = len(written)
            log.info("Saved pinned FAQ posts: %s", len(written))
            if written:
                log.info("Pinned FAQ output -> %s/", written[0].parent.relative_to(config.project_root))
        except Exception as exc:
            log.error("Failed to fetch/save 자주 묻는 질문(상단고정): %s", exc)

    log.info("Done. Downloaded %s APIs", total_apis)
    if failed_apis > 0:
        log.warning("Failed: %s APIs", failed_apis)
    log.info("Output: %s", config.output_dir)

    return DocsGenReport(
        total_apis=total_apis,
        failed_apis=failed_apis,
        failed_master=failed_master,
        error_codes_written=error_codes_written,
        faq_posts_written=faq_posts_written,
        master_docs_written=master_docs_written,
    )
