from __future__ import annotations

import re
from dataclasses import dataclass

_ENUM_LIST_RE = re.compile(r"(?:[A-Z0-9]{1,4}\s*,\s*)+[A-Z0-9]{1,4}")
_ENUM_PAIR_RE = re.compile(
    r"(?P<code>[A-Za-z0-9]{1,8})\s*[:=]\s*(?P<desc>.*?)(?=(?:\b[A-Za-z0-9]{1,8}\s*[:=])|$)",
    re.S,
)
_ENUM_PAIR_DASH_RE = re.compile(
    r"(?P<code>[A-Za-z0-9]{1,8})\s*[-–]\s*(?P<desc>.*?)(?=(?:\b[A-Za-z0-9]{1,8}\s*[-–])|$)",
    re.S,
)
_ENUM_PAIR_DOT_RE = re.compile(
    r"(?<![A-Za-z0-9가-힣_])(?P<code>[A-Za-z0-9]{1,5})\s*[.)]\s*(?P<desc>.*?)(?=(?:\b[A-Za-z0-9]{1,5}\s*[.)])|$)",
    re.S,
)
_ENUM_PAREN_CODE_RE = re.compile(r"(?P<desc>[^()\n,;/]+?)\s*\((?P<code>[A-Za-z0-9]{1,5})\)")
_ENUM_PAREN_DESC_RE = re.compile(r"(?<![A-Za-z0-9_])(?P<code>[A-Za-z0-9]{1,5})\s*\((?P<desc>[^()\n,;/]+?)\)")
_ENUM_EXAMPLE_RE = re.compile(r"(?i)\bex\b|e\.g\.|예시|예\)|예:")
_ENUM_EXAMPLE_LIST_HINT_RE = re.compile(r"(?i)\bticker\b|티커")
_UNIQUE_KEY_HINT_RE = re.compile(r"(?i)\bunique\s*key\b")
_BIT_SECTION_HEADER_RE = re.compile(r"^\(\s*(?P<index>\d+)\s*\)\s*(?P<title>.*)$")
_BIT_HINT_RE = re.compile(r"(?i)\bbit\b|비트")
_HIERARCHICAL_LINE_RE = re.compile(
    r"^\s*(?P<level>\d+)\s*:\s*(?P<code>[A-Za-z0-9]{1,8})\s*:\s*(?P<desc>.+?)\s*$"
)


@dataclass(frozen=True, slots=True)
class EnumEntry:
    code: str
    desc: str


_CLEAN_CODE_RE = re.compile(r"[^A-Za-z0-9]+")


def _normalize_description(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = normalized.replace("<br/>", "\n").replace("<br />", "\n").replace("<br>", "\n")
    normalized = normalized.replace("''", "'")
    normalized = normalized.replace("：", ":").replace("／", "/").replace("，", ",")
    normalized = normalized.replace("—", "-").replace("–", "-")
    normalized = re.sub(r"\b\d{4}[./]\d{1,2}[./]\d{1,2}\b", " ", normalized)
    normalized = re.sub(r"\b\d{4}[./]\d{1,2}\b", " ", normalized)
    normalized = re.sub(r"[\"']\s*([A-Za-z0-9]{1,8})\s*[\"']", r"\1", normalized)
    return normalized


def _clean_desc(text: str) -> str:
    cleaned = " ".join(text.split())
    cleaned = cleaned.strip(" ,;")
    cleaned = _strip_unbalanced_trailing_paren(cleaned)
    cleaned = cleaned.strip(" ,;")
    return cleaned


def _strip_unbalanced_trailing_paren(text: str) -> str:
    if not text or not text.endswith(")"):
        return text
    open_count = text.count("(")
    close_count = text.count(")")
    if close_count <= open_count:
        return text
    extra = close_count - open_count
    trimmed = text
    while extra > 0 and trimmed.endswith(")"):
        trimmed = trimmed[:-1].rstrip()
        extra -= 1
    return trimmed


def _clean_code(token: str) -> str:
    cleaned = token.strip().strip("()[]{}<>.,;")
    return cleaned


def _is_code_token(token: str) -> bool:
    if any(char in token for char in ("(", ")", "/")):
        return False
    cleaned = _clean_code(token)
    if not cleaned:
        return False
    if len(cleaned) > 8:
        return False
    return _CLEAN_CODE_RE.sub("", cleaned) == cleaned


def _parse_pairs(normalized: str) -> list[EnumEntry]:
    entries: list[EnumEntry] = []
    segments = [line.strip() for line in normalized.splitlines() if line.strip()]
    if not segments:
        segments = [normalized]
    for segment in segments:
        for match in _ENUM_PAIR_RE.finditer(segment):
            code = match.group("code").strip()
            desc = _clean_desc(match.group("desc") or "")
            if not code or not desc:
                continue
            entries.append(EnumEntry(code=code, desc=desc))
        for match in _ENUM_PAIR_DASH_RE.finditer(segment):
            code = match.group("code").strip()
            desc = _clean_desc(match.group("desc") or "")
            if not code or not desc:
                continue
            entries.append(EnumEntry(code=code, desc=desc))
    return entries


def _parse_dot_pairs(normalized: str) -> list[EnumEntry]:
    entries: list[EnumEntry] = []
    for line in normalized.splitlines():
        for match in _ENUM_PAIR_DOT_RE.finditer(line):
            code = match.group("code").strip()
            desc = _clean_desc(match.group("desc") or "")
            if not code or not desc:
                continue
            if code.lower() in {"ex", "eg"}:
                continue
            if desc.startswith("※") or "FID_" in desc:
                continue
            entries.append(EnumEntry(code=code, desc=desc))
    return entries


def _parse_paren_pairs(normalized: str) -> list[EnumEntry]:
    entries: list[EnumEntry] = []
    for match in _ENUM_PAREN_CODE_RE.finditer(normalized):
        code = match.group("code").strip()
        desc = _clean_desc(match.group("desc") or "")
        if not code or not desc:
            continue
        entries.append(EnumEntry(code=code, desc=desc))
    for match in _ENUM_PAREN_DESC_RE.finditer(normalized):
        code = match.group("code").strip()
        desc = _clean_desc(match.group("desc") or "")
        if not code or not desc:
            continue
        entries.append(EnumEntry(code=code, desc=desc))
    return entries


def _parse_colonless(normalized: str) -> list[EnumEntry]:
    entries: list[EnumEntry] = []
    for line in normalized.splitlines():
        line = line.strip()
        if not line:
            continue
        for segment in re.split(r"[,/]+", line):
            segment = segment.strip()
            if not segment or ":" in segment or "=" in segment:
                continue
            tokens = segment.split()
            if not tokens:
                continue
            code_indexes = [idx for idx, token in enumerate(tokens) if _is_code_token(token)]
            if not code_indexes:
                continue
            if len(code_indexes) == 1:
                code_index = code_indexes[0]
                if code_index != 0:
                    continue
                if len(tokens) < 2:
                    continue
                code = _clean_code(tokens[0])
                desc = _clean_desc(" ".join(tokens[1:]))
                if code and desc:
                    entries.append(EnumEntry(code=code, desc=desc))
                continue
            if code_indexes[0] != 0:
                continue
            if code_indexes[-1] == len(tokens) - 1:
                continue
            segment_entries: list[EnumEntry] = []
            invalid = False
            for idx, code_index in enumerate(code_indexes):
                end = code_indexes[idx + 1] if idx + 1 < len(code_indexes) else len(tokens)
                desc_tokens = tokens[code_index + 1 : end]
                if not desc_tokens:
                    invalid = True
                    break
                code = _clean_code(tokens[code_index])
                desc = _clean_desc(" ".join(desc_tokens))
                if not code or not desc:
                    invalid = True
                    break
                segment_entries.append(EnumEntry(code=code, desc=desc))
            if invalid:
                continue
            entries.extend(segment_entries)
    return entries


def _is_bit_component_code(code: str) -> bool:
    return len(code) == 1 and code.isalnum() and (code.isdigit() or code.isupper())


def _parse_bitwise_combinations(normalized: str) -> tuple[list[EnumEntry], set[str]]:
    sections: list[list[EnumEntry]] = []
    current: list[EnumEntry] | None = None

    for raw_line in normalized.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        header_match = _BIT_SECTION_HEADER_RE.match(line)
        if header_match:
            title = _clean_desc(header_match.group("title") or "")
            if _BIT_HINT_RE.search(title):
                current = []
                sections.append(current)
                continue
            if sections:
                current = None

        if current is None:
            continue

        for match in _ENUM_PAIR_RE.finditer(line):
            code = match.group("code").strip()
            desc = _clean_desc(match.group("desc") or "")
            if not code or not desc:
                continue
            current.append(EnumEntry(code=code, desc=desc))

    if len(sections) < 2:
        return [], set()

    first_raw, second_raw = sections[0], sections[1]
    if len(first_raw) < 2 or len(second_raw) < 2:
        return [], set()

    first: list[EnumEntry] = []
    second: list[EnumEntry] = []
    first_seen: set[str] = set()
    second_seen: set[str] = set()

    for entry in first_raw:
        if entry.code in first_seen:
            continue
        first_seen.add(entry.code)
        first.append(entry)
    for entry in second_raw:
        if entry.code in second_seen:
            continue
        second_seen.add(entry.code)
        second.append(entry)

    if not all(_is_bit_component_code(entry.code) for entry in first + second):
        return [], set()

    if len(first) * len(second) > 100:
        return [], set()

    combined: list[EnumEntry] = []
    for left in first:
        for right in second:
            desc = _clean_desc(f"{left.desc} / {right.desc}")
            combined.append(EnumEntry(code=f"{left.code}{right.code}", desc=desc))

    component_codes = {entry.code for entry in first + second}
    return combined, component_codes


def _parse_prefixed_subcodes(normalized: str) -> list[EnumEntry]:
    entries: list[EnumEntry] = []
    current_prefix: str | None = None

    for raw_line in normalized.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        match = _HIERARCHICAL_LINE_RE.match(line)
        if not match:
            continue

        level = int(match.group("level"))
        code = match.group("code").strip()
        desc = _clean_desc(match.group("desc") or "")

        if level == 1:
            current_prefix = code if len(code) == 1 and code.isalpha() else None
            continue

        if level != 3 or current_prefix is None:
            continue
        if len(code) != 2 or not code.isdigit():
            continue
        if not desc:
            continue

        entries.append(EnumEntry(code=f"{current_prefix}{code}", desc=desc))

    return entries


def parse_enum_entries(description: str | None) -> list[EnumEntry]:
    desc = (description or "").strip()
    if not desc:
        return []

    if _UNIQUE_KEY_HINT_RE.search(desc):
        return []

    normalized = _normalize_description(desc)
    candidates: list[EnumEntry] = []
    bitwise_combinations, bit_component_codes = _parse_bitwise_combinations(normalized)
    prefixed_subcodes = _parse_prefixed_subcodes(normalized)

    candidates.extend(_parse_pairs(normalized))
    candidates.extend(_parse_colonless(normalized))
    candidates.extend(_parse_dot_pairs(normalized))
    candidates.extend(_parse_paren_pairs(normalized))
    candidates.extend(bitwise_combinations)
    candidates.extend(prefixed_subcodes)

    if not candidates:
        if _ENUM_EXAMPLE_RE.search(normalized) or _ENUM_EXAMPLE_LIST_HINT_RE.search(normalized):
            return []
        for chunk in _ENUM_LIST_RE.findall(normalized):
            for token in chunk.split(","):
                token = token.strip()
                if token:
                    candidates.append(EnumEntry(code=token, desc=""))

    if not candidates:
        return []

    unique: dict[str, EnumEntry] = {}
    for entry in candidates:
        code = entry.code
        if bitwise_combinations:
            if code in bit_component_codes:
                continue
            if any(char.islower() for char in code):
                continue
        if code in unique:
            if not unique[code].desc and entry.desc:
                unique[code] = entry
            continue
        unique[code] = entry

    entries = list(unique.values())
    if len(entries) < 2:
        return []
    return entries


def parse_enum_values(description: str | None) -> list[str]:
    entries = parse_enum_entries(description)
    if not entries:
        return []
    values = [entry.code for entry in entries]
    if set(values).issubset({"Y", "N"}):
        values = [value for value in values if value in {"Y", "N"}]
    unique: list[str] = []
    for value in values:
        if value not in unique:
            unique.append(value)
    return unique if len(unique) >= 2 else []
