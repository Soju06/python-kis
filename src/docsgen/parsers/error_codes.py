"""Error code parsing for KIS API Portal."""

from __future__ import annotations

from dataclasses import dataclass

from bs4 import BeautifulSoup


@dataclass(frozen=True, slots=True)
class ErrorCodeEntry:
    """A single error code entry from the portal FAQ page."""

    category: str  # e.g. "EGW서버"
    code: str  # e.g. "EGW00102"
    message: str  # e.g. "AppKey는 필수입니다."


def parse_error_code_contents_body(contents_body_html: str) -> list[ErrorCodeEntry]:
    """Parse KIS portal ERRORCODE contentsBody HTML into error code entries.

    The portal renders multiple sections; each section is a table that contains rows like:

        <tr>
          <th>CODE1</th><td>MESSAGE1</td>
          <th>CODE2</th><td>MESSAGE2</td>
        </tr>

    Returns:
        List of ErrorCodeEntry in document order.
    """

    soup = BeautifulSoup(contents_body_html, "html.parser")

    entries: list[ErrorCodeEntry] = []

    for item in soup.select("div.conts-area-item"):
        category_el = item.select_one("h2.cont-tit")
        category = category_el.get_text(" ", strip=True) if category_el else ""

        table = item.select_one("table")
        if table is None:
            continue

        for tr in table.select("tbody tr"):
            # rows alternate th (code) and td (message), repeated twice per row.
            cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
            if not cells:
                continue

            # Consume as (code, message) pairs; ignore incomplete tail.
            for i in range(0, len(cells) - 1, 2):
                code = cells[i].strip()
                message = cells[i + 1].strip()
                if not code or not message:
                    continue
                entries.append(ErrorCodeEntry(category=category, code=code, message=message))

    return entries
