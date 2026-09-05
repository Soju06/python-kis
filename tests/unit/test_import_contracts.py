"""import-linter 계약이 실제로 무언가를 검사하고 있는지 확인합니다.

계약의 **내용**은 `lint-imports` 가 검사합니다(CI 의 lint 잡, 규칙은
`pyproject.toml` 의 `[tool.importlinter]`). 여기서 보는 것은 계약이 놓치는 두 가지
— 계약이 **아무것도 못 보는 상태**와 계약이 **볼 수 없는 위반**입니다.
"""

from __future__ import annotations

import ast
import pathlib
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = REPO_ROOT / "src"
PACKAGE_DIR = SRC / "vmkis"


def _load_pyproject() -> dict:
    if sys.version_info >= (3, 11):
        import tomllib
    else:  # import-linter 가 3.11 미만에서 tomli 를 함께 설치합니다.
        tomllib = pytest.importorskip("tomli", reason="tomli 는 import-linter 의 의존성입니다")

    with (REPO_ROOT / "pyproject.toml").open("rb") as fp:
        return tomllib.load(fp)


def _module_name(path: pathlib.Path) -> str:
    parts = list(path.relative_to(SRC).with_suffix("").parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _source_modules() -> set[str]:
    return {_module_name(p) for p in PACKAGE_DIR.rglob("*.py") if "__pycache__" not in p.parts}


def test_contract_graph_covers_every_source_module() -> None:
    """설정된 루트가 `src/vmkis` 의 모든 모듈을 그래프에 담아야 합니다.

    grimp 은 루트 패키지를 스캔할 때 `__init__.py` 가 없는 디렉터리(암묵적
    네임스페이스 패키지)를 **건너뜁니다.** 이슈 #50 당시 `src/vmkis` 의 디렉터리
    18개 중 13개가 그 상태여서, 루트 하나만 주면 모듈 92개 중 20개만 잡히고
    `utils` · `client` · `responses` · `api` · `adapter` 가 통째로 사라졌습니다.

    빠진 것이 계약의 `source_modules` 면 import-linter 가
    `Module 'vmkis.utils' does not exist.` 로 죽어 소리를 냅니다. 그러나 빠진 것이
    `forbidden_modules` 쪽이거나 계약에 아직 안 걸린 서브패키지면 **조용히 통과**합니다.

    이슈 #64 에서 `__init__.py` 를 채워 원인을 없앴습니다. 이 테스트는 그것이
    유지되는지를 봅니다 — `__init__.py` 없는 디렉터리가 새로 생기면 여기서 잡힙니다.
    """
    # grimp 은 lint 그룹(import-linter)이 끌고 옵니다. `--group test` 만 설치한
    # 환경에서는 이 검사를 건너뜁니다. 아래 AST 검사는 그런 환경에서도 돕니다.
    grimp = pytest.importorskip("grimp", reason="import-linter(lint 그룹)가 설치되어야 합니다")

    # `root_package`(단수) / `root_packages`(복수) 둘 다 import-linter 의 유효한
    # 설정입니다. 어느 쪽으로 적혀 있든 같은 성질을 검사합니다.
    session = _load_pyproject()["tool"]["importlinter"]
    roots = session.get("root_packages") or [session["root_package"]]
    graph = grimp.build_graph(*roots)

    missing = sorted(_source_modules() - set(graph.modules))

    assert not missing, (
        "다음 모듈이 import-linter 그래프에 없습니다. 계약이 이들을 검사하지 않습니다.\n"
        "해당 디렉터리에 __init__.py 가 있는지 확인하세요(이슈 #64).\n  " + "\n  ".join(missing)
    )


def test_messaging_keeps_api_import_lazy() -> None:
    """`client/messaging.py` 의 `api` import 는 함수 안에 있어야 합니다.

    이 한 줄은 "client 는 api 를 import 하지 않는다" 계약의 `ignore_imports` 에
    면제로 등록되어 있습니다. **면제는 모듈 쌍 단위**라서 위치를 보지 않습니다 —
    이 import 를 파일 상단으로 올려도 `lint-imports` 는 초록으로 통과합니다(실측).

    모듈 레벨로 올라가면 패키지가 로드 불능이 되므로(ARCHITECTURE.md 불변식 3번)
    계약이 못 보는 이 구멍을 여기서 막습니다.
    """
    source = (PACKAGE_DIR / "client" / "messaging.py").read_text(encoding="utf-8")
    tree = ast.parse(source)

    lazy = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            lazy |= {id(x) for x in ast.walk(node) if isinstance(x, (ast.Import, ast.ImportFrom))}

    offenders = [
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.module
        and node.module.startswith("vmkis.api")
        and id(node) not in lazy
    ]

    assert not offenders, f"client/messaging.py 가 api 를 모듈 레벨에서 import 합니다: {offenders}"
