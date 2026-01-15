"""Parse master header files into structured fields."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class MasterField:
    name: str
    type_code: str
    length: int
    description: str
    length_source: str | None = None


@dataclass(frozen=True, slots=True)
class MasterStruct:
    name: str
    header_url: str
    fields: tuple[MasterField, ...]
    record_length: int


_FIELD_RE = re.compile(
    r"^\s*(?P<type>[A-Za-z_][\w\s\*]*?)\s+(?P<name>[A-Za-z_]\w*)\s*\[(?P<size>[^\]]+)\]\s*;"
)

_STRUCT_START_RE = re.compile(r"^\s*typedef\s+struct\b")
_STRUCT_NAMED_RE = re.compile(r"^\s*struct\s+(?P<name>[A-Za-z_]\w*)\b")
_STRUCT_END_RE = re.compile(r"\}\s*(?P<name>[A-Za-z_]\w*)?\s*;")


_DEFAULT_MACROS: dict[str, int] = {
    "SZ_SHRNCODE": 9,
    "SZ_STNDCODE": 12,
    "SZ_KORNAME": 40,
    "SZ_KORNAME20": 20,
}


def decode_header_bytes(payload: bytes) -> str:
    for encoding in ("euc-kr", "cp949", "utf-8"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    return payload.decode("utf-8", errors="replace")


def _clean_type(type_code: str) -> str:
    return " ".join(type_code.strip().split())


def _normalize_description(text: str) -> str:
    cleaned = " ".join(text.strip().split())
    return cleaned


def _tokenize_expr(expr: str) -> list[str]:
    return re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+|[()+\-*/]", expr)


def _eval_expr(expr: str, macros: dict[str, int]) -> int:
    tokens = []
    for token in _tokenize_expr(expr):
        if token.isdigit() or token in {"+", "-", "*", "/", "(", ")"}:
            tokens.append(token)
            continue
        if token in macros:
            tokens.append(str(macros[token]))
            continue
        if token.startswith("SZ_"):
            digits = re.search(r"(\d+)$", token)
            if digits:
                tokens.append(digits.group(1))
                continue
        raise ValueError(f"Unknown macro: {token}")

    parsed = ast.parse("".join(tokens), mode="eval")
    if not isinstance(parsed, ast.Expression):
        raise ValueError("Invalid expression")

    def _eval(node: ast.AST) -> int:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return int(node.value)
            raise ValueError("Invalid constant")
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, (ast.Div, ast.FloorDiv)):
                return left // right
            raise ValueError("Invalid operator")
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            if isinstance(node.op, ast.UAdd):
                return operand
            if isinstance(node.op, ast.USub):
                return -operand
            raise ValueError("Invalid unary operator")
        raise ValueError("Invalid expression")

    value = _eval(parsed)
    if value < 0:
        raise ValueError("Negative length")
    return value


def _parse_length(raw: str, macros: dict[str, int]) -> tuple[int, str | None]:
    raw = raw.strip()
    if raw.isdigit():
        return int(raw), None
    value = _eval_expr(raw, macros)
    return value, raw


def _split_code_comment(line: str, in_block: bool) -> tuple[str, list[str], bool]:
    code_parts: list[str] = []
    comments: list[str] = []
    i = 0
    while i < len(line):
        if in_block:
            end = line.find("*/", i)
            if end == -1:
                comments.append(line[i:].strip())
                return "".join(code_parts), comments, True
            comments.append(line[i:end].strip())
            i = end + 2
            in_block = False
            continue

        idx_line = line.find("//", i)
        idx_block = line.find("/*", i)

        if idx_line == -1 and idx_block == -1:
            code_parts.append(line[i:])
            break

        if idx_line != -1 and (idx_block == -1 or idx_line < idx_block):
            code_parts.append(line[i:idx_line])
            comments.append(line[idx_line + 2 :].strip())
            break

        code_parts.append(line[i:idx_block])
        i = idx_block + 2
        in_block = True

    return "".join(code_parts), comments, in_block


def parse_header_structs(
    header_text: str,
    header_url: str,
    macros: dict[str, int] | None = None,
) -> list[MasterStruct]:
    """Parse header text into struct definitions."""

    macro_map = dict(_DEFAULT_MACROS)
    if macros:
        macro_map.update(macros)

    structs: list[MasterStruct] = []
    lines = header_text.splitlines()

    inside_struct = False
    pending_typedef = False
    struct_name: str | None = None
    fields: list[MasterField] = []

    in_block_comment = False
    block_owner: int | None = None

    def _append_comment(target_index: int | None, text: str) -> None:
        if target_index is None:
            return
        if not text:
            return
        field = fields[target_index]
        desc = field.description
        combined = f"{desc}\n{text}" if desc else text
        fields[target_index] = MasterField(
            name=field.name,
            type_code=field.type_code,
            length=field.length,
            description=combined,
            length_source=field.length_source,
        )

    for line in lines:
        stripped = line.strip()
        if not inside_struct:
            if _STRUCT_START_RE.search(stripped):
                pending_typedef = True
                if "{" in stripped:
                    inside_struct = True
                continue
            named_match = _STRUCT_NAMED_RE.search(stripped)
            if named_match and "{" in stripped:
                inside_struct = True
                struct_name = named_match.group("name")
                continue
            if named_match and not inside_struct:
                struct_name = named_match.group("name")
                continue
            if pending_typedef and "{" in stripped:
                inside_struct = True
                continue
            continue

        end_match = _STRUCT_END_RE.search(stripped)
        if end_match:
            name_from_end = end_match.group("name")
            final_name = struct_name or name_from_end
            if final_name and fields:
                record_length = sum(field.length for field in fields)
                structs.append(
                    MasterStruct(
                        name=final_name,
                        header_url=header_url,
                        fields=tuple(fields),
                        record_length=record_length,
                    )
                )
            inside_struct = False
            pending_typedef = False
            struct_name = None
            fields = []
            in_block_comment = False
            block_owner = None
            continue

        code, comments, in_block_comment = _split_code_comment(line, in_block_comment)
        code = code.strip()
        comment_text = "\n".join(filter(None, (_normalize_description(c) for c in comments)))

        if code:
            field_match = _FIELD_RE.match(code)
            if field_match:
                type_code = _clean_type(field_match.group("type"))
                name = field_match.group("name")
                size_expr = field_match.group("size").strip()
                length, length_source = _parse_length(size_expr, macro_map)
                description = comment_text
                fields.append(
                    MasterField(
                        name=name,
                        type_code=type_code,
                        length=length,
                        description=description,
                        length_source=length_source,
                    )
                )
                if in_block_comment:
                    block_owner = len(fields) - 1
                continue

        if comment_text:
            target = block_owner if block_owner is not None else (len(fields) - 1 if fields else None)
            _append_comment(target, comment_text)

        if not in_block_comment:
            block_owner = None

    return structs


def merge_structs(structs: Iterable[MasterStruct]) -> list[MasterStruct]:
    merged: dict[str, MasterStruct] = {}
    for struct in structs:
        if struct.name in merged:
            raise ValueError(f"Duplicate struct name: {struct.name}")
        merged[struct.name] = struct
    return list(merged.values())
