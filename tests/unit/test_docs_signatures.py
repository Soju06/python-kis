"""문서와 노트북의 python 예제가 실제 API 와 맞는지 봅니다. (이슈 #78)

## 왜 필요한가

#78 은 "사용자 문서가 존재하지 않는 `VmKis` 시그니처를 적고 있다"로 열렸고,
그 완료 기준 2번이 **"문서의 파이썬 예제가 실제로 import 되고 시그니처가
맞는지 검사하는 방법"** 이었습니다. 이 파일이 그 답입니다.

이 검사를 처음 돌렸을 때 이슈 본문이 적어 둔 3곳 말고 **7곳이 더** 나왔습니다
(`from vmkis import setLevel`, `vmkis.mock`, `VmKis(paper=...)` 등). 사람이 512줄
문서를 눈으로 훑어서는 안 나오는 것들입니다.

## 검사하는 것과 안 하는 것

| | |
|---|---|
| ✅ `from vmkis... import X` 의 `X` 가 그 모듈에 있는가 | 삭제된 이름을 잡습니다 |
| ✅ 공개 진입점 호출의 키워드/위치 인자 | 바뀐 시그니처를 잡습니다 |
| ❌ 예제가 **실행되는가** | 자격증명·네트워크가 필요합니다. 별개 성질입니다 |
| ❌ import 할 수 없는 모듈 | `vmkis.api.my_api` 처럼 **의도된 자리표시자**가 있습니다 |

마지막 줄이 중요합니다. "모듈이 없다"는 틀렸다는 뜻이 아니라 **확인할 수 없다**는
뜻입니다. `DEVELOPER_GUIDE` 의 확장 가이드가 `my_api`·`my_adapter` 같은 이름을
일부러 씁니다. 그래서 **import 되는 모듈 안에서만** 이름을 검증합니다.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import json
import pathlib
import re
import warnings
from collections.abc import Callable, Iterator
from typing import Any

import pytest

from vmkis import KisAuth, SimpleKIS, VmKis, create_client, save_config_interactive

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]

#: 동결 문서. 손으로 고치는 대상이 아닙니다.
#: `generated/API_REFERENCE.md` 는 생성기가 맞추므로 검사 대상입니다.
SKIP_PARTS = {"reports", "dev_logs", "prompts", "archive"}

CHECKED: dict[str, Callable[..., Any]] = {
    "create_client": create_client,
    "save_config_interactive": save_config_interactive,
    "KisAuth": KisAuth,
    "SimpleKIS": SimpleKIS,
    "VmKis": VmKis,
}

_FENCE = re.compile(r"```(?:python|py)\n(.*?)```", re.S)


def _doc_files() -> list[pathlib.Path]:
    roots = [REPO_ROOT / "docs", REPO_ROOT / "examples", REPO_ROOT]
    found: set[pathlib.Path] = set()
    for root in roots:
        for pattern in ("*.md", "*.ipynb"):
            for p in root.rglob(pattern) if root != REPO_ROOT else root.glob(pattern):
                if SKIP_PARTS & set(p.relative_to(REPO_ROOT).parts):
                    continue
                if ".venv" in p.parts or "node_modules" in p.parts:
                    continue
                found.add(p)
    return sorted(found)


def _blocks(path: pathlib.Path) -> Iterator[tuple[str, int]]:
    """`(코드, 파일 내 시작 행)` 을 냅니다."""
    text = path.read_text(encoding="utf-8")

    if path.suffix == ".ipynb":
        # 노트북은 셀 단위. 행 번호는 셀 안 기준이라 0 으로 둡니다.
        for cell in json.loads(text).get("cells", []):
            if cell.get("cell_type") == "code":
                yield "".join(cell.get("source", [])), 0
        return

    for m in _FENCE.finditer(text):
        yield m.group(1), text[: m.start()].count("\n") + 2


def _callee(node: ast.Call) -> str | None:
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return None


def _check_block(code: str, origin: str, line0: int) -> list[str]:
    problems: list[str] = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        # 문서에는 `...` 나 발췌가 섞입니다. 파싱 안 되는 블록은 검사 대상이
        # 아닙니다 — 여기서 실패시키면 문서 쓰는 사람이 검사를 꺼 버립니다.
        return problems

    def where_of(node: ast.AST) -> str:
        # `ast.walk` 은 `lineno` 가 없는 Module 도 냅니다. 위치는 실제로 쓸 때만
        # 계산합니다.
        return f"{origin}:{line0 + node.lineno - 1}" if line0 else origin  # type: ignore[attr-defined]

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and (node.module or "").startswith("vmkis"):
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", DeprecationWarning)
                    module = importlib.import_module(node.module)
            except ImportError:
                continue  # 자리표시자일 수 있습니다. 확인 불가 ≠ 틀림
            for alias in node.names:
                if alias.name == "*":
                    continue
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", DeprecationWarning)
                    exists = hasattr(module, alias.name)
                if not exists:
                    problems.append(f"{where_of(node)} — `{node.module}` 에 `{alias.name}` 이(가) 없습니다")

        if isinstance(node, ast.Call):
            target = CHECKED.get(_callee(node) or "")
            if target is None:
                continue
            params = inspect.signature(target).parameters
            if any(p.kind is p.VAR_KEYWORD for p in params.values()):
                continue
            allowed = {n for n, p in params.items() if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)}
            for kw in node.keywords:
                if kw.arg and kw.arg not in allowed:
                    problems.append(
                        f"{where_of(node)} — {_callee(node)}(...) 에 `{kw.arg}=` 를 넘깁니다. "
                        f"받는 이름은 {sorted(allowed)} 입니다"
                    )

    return problems


@pytest.mark.parametrize("path", _doc_files(), ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_doc_examples_match_public_api(path: pathlib.Path) -> None:
    origin = str(path.relative_to(REPO_ROOT))
    problems = [p for code, line0 in _blocks(path) for p in _check_block(code, origin, line0)]
    assert not problems, "문서 예제가 실제 API 와 다릅니다:\n  " + "\n  ".join(problems)


def test_generated_api_reference_is_signature_checked() -> None:
    """#94: 생성물을 SKIP 하면 다시 눈이 멀었습니다."""
    paths = {p.relative_to(REPO_ROOT).as_posix() for p in _doc_files()}

    assert "docs/generated/API_REFERENCE.md" in paths, f"API_REFERENCE 가 시그니처 검사 밖입니다: {sorted(paths)}"


def test_checker_actually_reads_documents() -> None:
    """검사기가 **아무것도 안 보는 상태**를 막습니다.

    경로나 코드펜스 정규식이 틀리면 블록이 0개라 전부 조용히 통과합니다.
    """
    files = _doc_files()
    assert len(files) >= 20, f"문서가 {len(files)}개뿐입니다. 경로가 맞습니까?"

    blocks = sum(1 for f in files for _ in _blocks(f))
    assert blocks >= 100, f"python 코드블록이 {blocks}개뿐입니다. 코드펜스를 못 읽고 있습니까?"


@pytest.mark.parametrize(
    "code, needle",
    [
        ("from vmkis.helpers import load_config\n", "load_config"),  # #75 에서 삭제
        ("from vmkis import setLevel\n", "setLevel"),  # 루트에 없음
        ('VmKis(app_key="x", app_secret="y")\n', "app_key"),  # 옛 이름
        ("KisAuth(virtual=True)\n", "virtual"),  # #70 이전 이름
        ("VmKis(paper=True)\n", "paper"),  # KisAuth 의 인자를 VmKis 에 준 것
    ],
)
def test_checker_catches_known_defects(code: str, needle: str) -> None:
    """#78 이 실제로 잡은 결함들을 그대로 먹여 봅니다.

    문서가 앞으로 어떻게 바뀌든 **검사기 자체의 성능**이 계속 검증됩니다.
    """
    problems = _check_block(code, "<결함 재현>", 0)
    assert problems, f"검사기가 {needle!r} 결함을 못 잡습니다"
    assert needle in problems[0]
