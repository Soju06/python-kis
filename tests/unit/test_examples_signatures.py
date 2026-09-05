"""`examples/` 가 공개 API 와 어긋나지 않는지 봅니다. (이슈 #84, #95)

## 왜 이 검사가 필요한가

#75 가 `create_client` 의 `profile` 을 `account` 로 바꾸면서 `examples/01_basic/`
3개만 고치고 **7개를 놓쳤습니다.** 그 7개는 실행하면 이렇게 죽습니다.

```text
TypeError: create_client() got an unexpected keyword argument 'profile'
```

## 왜 기존 검사가 못 잡았나

`tests/integration/test_examples_run_smoke.py` 가 예제를 실제로 **실행**합니다.
그런데

1. `RUN_INTEGRATION=1` 없이는 통째로 skip 이고, CI 는 그 변수를 주지 않습니다
2. 실행 방식이라 **자격증명과 네트워크가 필요**합니다

**이 결함은 둘 다 필요 없습니다.** `create_client` 는 호출되는 순간 죽으므로
서버에 닿을 일이 없습니다. `--help` 로 돌리는 것도 답이 아닙니다 — argparse 가
`create_client` 보다 먼저 끝나 인자 오류가 드러나지 않습니다.

그래서 **AST 로 호출부를 읽어 실제 시그니처와 대조**합니다. 자격증명도
네트워크도 없이 돌고, 다음 개명도 같은 자리에서 잡힙니다.

## `--config` 기본값 (이슈 #95)

같은 누락이 한 번 더 났습니다. #75 가 `01_basic/` 4개의 기본값을
`configs/account_profiles.yaml` 로 고치고 **7개를 놓쳤습니다.** 놓친 쪽은
`config.yaml` 을 가리키는데 그 파일은 저장소에 없고 `.gitignore` 에 있습니다.
크래시가 아니라 친절한 안내로 끝나서 조용히 오래갔습니다.

이슈는 *"기본값이 전부 같은지"* 를 제안했습니다. **그 검사는 11개가 똑같이
틀려도 통과합니다.** 그래서 서로 대조하지 않고 **`create_client` 자신의
기본값과 대조**합니다. 라이브러리가 경로를 바꾸면 검사가 따라옵니다.
"""

from __future__ import annotations

import ast
import inspect
import pathlib
from collections.abc import Callable
from typing import Any

import pytest

from vmkis import KisAuth, SimpleKIS, VmKis, create_client, save_config_interactive

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
EXAMPLES = REPO_ROOT / "examples"

#: 예제가 부르는 공개 진입점. 이름은 **예제가 쓰는 이름**입니다.
CHECKED: dict[str, Callable[..., Any]] = {
    "create_client": create_client,
    "save_config_interactive": save_config_interactive,
    "KisAuth": KisAuth,
    "SimpleKIS": SimpleKIS,
    "VmKis": VmKis,
}


#: 예제의 `--config` 기본값이 맞춰야 하는 값.
#:
#: 손으로 적지 않고 **`create_client` 의 기본값에서 꺼냅니다.** 여기에 문자열을
#: 박으면 라이브러리가 경로를 바꾼 날 검사가 조용히 거짓이 됩니다. 비공개
#: `helpers.DEFAULT_CONFIG_PATH` 를 import 하지 않는 이유도 같습니다 — 예제가
#: 쓰는 것은 공개 API 이고, 검사도 같은 것을 봐야 합니다.
EXPECTED_CONFIG_DEFAULT = inspect.signature(create_client).parameters["config_path"].default


def _example_files() -> list[pathlib.Path]:
    return sorted(p for p in EXAMPLES.rglob("*.py") if "__pycache__" not in p.parts)


def _example_docs() -> list[pathlib.Path]:
    """예제가 딸고 있는 README 와 노트북.

    `#111` 이전에는 `.ipynb` 를 뺐습니다. 노트북이 폐기된 평면 스키마를
    가르치고 있어서, 경로 검사만 넣으면 틀린 것을 최신처럼 보이게 만들었기
    때문입니다. 스키마를 고친 뒤에는 빼면 안 됩니다 — 빼는 순간 같은 결함이
    검사 밖으로 나갑니다.
    """
    return sorted(
        p for p in (*EXAMPLES.rglob("README.md"), *EXAMPLES.rglob("*.ipynb")) if ".ipynb_checkpoints" not in p.parts
    )


#: 폐기된 평면 설정 스키마. YAML 키 형태(`id: "…"`)만 봅니다.
#: `KisAuth(id="…")` 생성자 인자와 구별됩니다. (#111)
_FLAT_CONFIG_MARKERS = ('id: "YOUR_ID"', 'appkey: "YOUR_APPKEY"')


def _flat_config_schema_hits(text: str, origin: str) -> list[str]:
    return [f"{origin} — {marker}" for marker in _FLAT_CONFIG_MARKERS if marker in text]


def _callee_name(node: ast.Call) -> str | None:
    """`f(...)` 와 `mod.f(...)` 에서 마지막 이름을 꺼냅니다."""
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _violations(source: str, origin: str) -> list[str]:
    problems: list[str] = []

    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call):
            continue

        name = _callee_name(node)
        target = CHECKED.get(name or "")
        if target is None:
            continue

        params = inspect.signature(target).parameters
        accepts_var_kw = any(p.kind is p.VAR_KEYWORD for p in params.values())
        keyword_ok = {n for n, p in params.items() if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)}

        for kw in node.keywords:
            if kw.arg is None:  # `**something` — 정적으로는 알 수 없습니다
                continue
            if kw.arg not in keyword_ok and not accepts_var_kw:
                problems.append(
                    f"{origin}:{node.lineno} — {name}(...) 에 `{kw.arg}=` 를 넘깁니다. "
                    f"받는 이름은 {sorted(keyword_ok)} 입니다"
                )

        positional_ok = sum(1 for p in params.values() if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD))
        given = sum(1 for a in node.args if not isinstance(a, ast.Starred))
        if given > positional_ok and not any(p.kind is p.VAR_POSITIONAL for p in params.values()):
            problems.append(
                f"{origin}:{node.lineno} — {name}(...) 에 위치 인자 {given}개를 넘깁니다. "
                f"받는 것은 {positional_ok}개입니다"
            )

    return problems


@pytest.mark.parametrize("path", _example_files(), ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_example_calls_match_public_signatures(path: pathlib.Path) -> None:
    problems = _violations(path.read_text(encoding="utf-8"), str(path.relative_to(REPO_ROOT)))
    assert not problems, "예제가 존재하지 않는 인자를 넘깁니다:\n  " + "\n  ".join(problems)


def test_checker_actually_sees_the_examples() -> None:
    """검사기가 **아무것도 안 보는 상태**를 막습니다.

    경로가 틀리거나 예제가 `create_client` 를 그만 쓰면, 위 테스트는 위반이
    0건이라 조용히 통과합니다. 그때는 검사가 아니라 장식입니다.
    """
    files = _example_files()
    assert len(files) >= 10, f"예제 파일이 {len(files)}개뿐입니다. 경로가 맞습니까? {EXAMPLES}"

    seen = {
        _callee_name(node)
        for path in files
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
        if isinstance(node, ast.Call)
    }
    assert "create_client" in seen, "예제 어디에도 create_client 호출이 없습니다"


def test_checker_catches_the_original_defect() -> None:
    """#84 의 결함을 그대로 먹여 실제로 잡히는지 봅니다.

    회귀 테스트를 되돌려 확인하는 대신, **결함을 문자열로 박아** 둡니다.
    예제가 다시 고쳐져도 이 검사기 자체의 성능은 계속 검증됩니다.
    """
    defect = "create_client(config_path, profile=profile)\n"
    problems = _violations(defect, "<결함 재현>")

    assert problems, "검사기가 #84 의 원래 결함을 못 잡습니다"
    assert "profile" in problems[0]
    assert "account" in problems[0]


def _config_defaults(source: str) -> list[tuple[int, Any]]:
    """예제가 argparse 로 선언한 `--config` 의 기본값을 `(행, 값)` 으로 꺼냅니다."""
    found: list[tuple[int, Any]] = []

    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call) or _callee_name(node) != "add_argument":
            continue
        if not node.args or not isinstance(node.args[0], ast.Constant) or node.args[0].value != "--config":
            continue

        for kw in node.keywords:
            if kw.arg == "default" and isinstance(kw.value, ast.Constant):
                found.append((node.lineno, kw.value.value))

    return found


@pytest.mark.parametrize("path", _example_files(), ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_example_config_default_matches_the_library(path: pathlib.Path) -> None:
    """`--config` 기본값이 `create_client` 의 기본값과 같은지 봅니다. (#95)"""
    origin = str(path.relative_to(REPO_ROOT))
    wrong = [
        f"{origin}:{lineno} — --config 기본값이 {value!r} 입니다"
        for lineno, value in _config_defaults(path.read_text(encoding="utf-8"))
        if value != EXPECTED_CONFIG_DEFAULT
    ]

    assert not wrong, f"create_client 의 기본값은 {EXPECTED_CONFIG_DEFAULT!r} 입니다:\n  " + "\n  ".join(wrong)


@pytest.mark.parametrize("path", _example_files() + _example_docs(), ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_example_does_not_name_a_path_that_does_not_exist(path: pathlib.Path) -> None:
    """`config.yaml` 이라는 이름이 남아 있는지 봅니다. (#95)

    기본값만 보면 부족합니다. #95 의 28곳 중 **21곳이 argparse 바깥**이었습니다
    — docstring 의 실행 조건, `os.getcwd()` 폴백, 그리고 파일을 못 찾았을 때의
    안내 문구. 사용자는 그 문구를 읽고 없는 파일을 만들려 합니다.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    origin = str(path.relative_to(REPO_ROOT))
    hits = [f"{origin}:{i} — {line.strip()}" for i, line in enumerate(lines, 1) if "config.yaml" in line]

    assert not hits, (
        "저장소에 `config.yaml` 은 없습니다(.gitignore 에 있습니다). "
        f"{EXPECTED_CONFIG_DEFAULT} 로 적으세요:\n  " + "\n  ".join(hits)
    )


def test_config_default_checker_actually_sees_the_flags() -> None:
    """검사기가 **아무것도 안 보는 상태**를 막습니다.

    `--config` 를 못 찾으면 위 검사는 위반 0건으로 조용히 통과합니다. #95 를
    고칠 때 예제 11개가 이 플래그를 선언하고 있었습니다.
    """
    seen = [
        (path, lineno, value)
        for path in _example_files()
        for lineno, value in _config_defaults(path.read_text(encoding="utf-8"))
    ]

    assert len(seen) >= 10, f"--config 기본값을 {len(seen)}개만 찾았습니다. 추출기가 눈이 멀었습니까?"


def test_config_default_checker_catches_the_original_defect() -> None:
    """#95 의 결함을 그대로 먹여 실제로 잡히는지 봅니다."""
    defect = 'parser.add_argument("--config", default="config.yaml", help="path to config file")\n'
    found = _config_defaults(defect)

    assert found == [(1, "config.yaml")], f"검사기가 #95 의 원래 결함을 못 잡습니다: {found}"
    assert found[0][1] != EXPECTED_CONFIG_DEFAULT


def test_the_expected_default_is_a_path_the_docs_can_create() -> None:
    """기본값이 **실제로 만들 수 있는 자리**인지 봅니다.

    #95 의 결함은 "기본값이 갈라진 것"이 아니라 **"없는 파일을 가리킨 것"**
    입니다. 서로 같은지만 보면 전부 똑같이 없는 경로를 가리켜도 통과합니다.

    문서가 안내하는 것은 이 한 줄입니다.

        cp configs/template_account_profiles.yaml configs/account_profiles.yaml
    """
    template = REPO_ROOT / "configs" / "template_account_profiles.yaml"
    assert template.exists(), f"템플릿이 없습니다: {template}"

    expected = REPO_ROOT / EXPECTED_CONFIG_DEFAULT
    assert expected.parent == template.parent, (
        f"기본값 {EXPECTED_CONFIG_DEFAULT} 가 템플릿({template.parent.name}/)과 다른 자리를 가리킵니다"
    )


def test_the_name_check_also_reads_the_readmes() -> None:
    """검사가 `.py` 만 보고 있지 않은지 봅니다.

    #95 의 28곳은 전부 `.py` 였지만, 같은 문자열이 README 에도 있었고
    사용자는 그쪽을 먼저 읽습니다. `_example_docs()` 가 빈 목록이 되면
    조용히 검사 밖으로 나갑니다. `#155` 이후 예제 README 는 둘입니다
    (`examples/` · `01_basic/`).
    """
    docs = _example_docs()
    readmes = [p for p in docs if p.name == "README.md"]

    assert len(readmes) == 2, f"예제 README 가 {len(readmes)}개입니다: {readmes}"


def test_the_name_check_also_reads_the_tutorial_notebook() -> None:
    """#111 의 닫힘 조건입니다. 노트북이 목록에서 빠지면 검사가 눈을 감습니다."""
    notebooks = [p for p in _example_docs() if p.suffix == ".ipynb"]

    assert any(p.name == "tutorial_basic.ipynb" for p in notebooks), (
        f"tutorial_basic.ipynb 이 검사 밖으로 빠졌습니다: {notebooks}"
    )


def test_tutorial_notebook_does_not_teach_the_flat_config_schema() -> None:
    """경로만 고치고 평면 스키마를 남기면 안 됩니다. (#111, #70 함정)"""
    path = EXAMPLES / "tutorial_basic.ipynb"
    hits = _flat_config_schema_hits(path.read_text(encoding="utf-8"), path.name)

    assert not hits, (
        "노트북이 폐기된 평면 설정 스키마를 가르칩니다. "
        "스키마 정본은 configs/template_account_profiles.yaml 입니다:\n  " + "\n  ".join(hits)
    )


def test_flat_schema_checker_catches_the_original_defect() -> None:
    """#111 의 결함을 그대로 먹여 실제로 잡히는지 봅니다."""
    defect = 'id: "YOUR_ID"\naccount: "YOUR_ACCOUNT"\nappkey: "YOUR_APPKEY"\nsecretkey: "YOUR_SECRETKEY"\n'
    hits = _flat_config_schema_hits(defect, "<결함 재현>")

    assert hits, "검사기가 #111 의 원래 결함을 못 잡습니다"
    assert 'id: "YOUR_ID"' in hits[0]


def test_hello_world_calls_create_client() -> None:
    """#152. 첫 연결 예제가 스텁으로 되돌아가면 실패합니다."""
    text = (EXAMPLES / "01_basic" / "hello_world.py").read_text(encoding="utf-8")

    assert "create_client(" in text
    assert "Hello from VM-Stock-KIS example" not in text


def test_hello_world_stub_is_caught() -> None:
    stub = 'print("Hello from VM-Stock-KIS example")\n'

    assert "create_client(" not in stub
    assert "Hello from VM-Stock-KIS example" in stub
