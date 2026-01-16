from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from docsgen.parsers.faq_posts import FAQ_FORUM_ID
from docsgen.paths import docs_root


@dataclass(frozen=True, slots=True)
class DocsGenConfig:
    project_root: Path
    output_dir: Path
    portal_base_url: str = "https://apiportal.koreainvestment.com"
    portal_delay: float = 0.2
    header_concurrency: int = 4
    header_timeout: float = 10.0
    faq_forum_id: str = FAQ_FORUM_ID
    master_reference_path: Path | None = None
    master_source_url: str = "https://apiportal.koreainvestment.com/api/contents/kind?title=CATEGORY&kind=CONTENTS"

    @classmethod
    def from_project_root(cls, project_root: Path) -> DocsGenConfig:
        return cls(
            project_root=project_root,
            output_dir=docs_root(project_root),
            master_reference_path=project_root / "docs" / "종목정보파일_주소_헤더.md",
        )
