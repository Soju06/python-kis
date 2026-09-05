"""`self.fetch(...)` 호출부가 `VmKis.fetch` 시그니처를 지키는지 정적 검사 (이슈 #43).

**왜 필요한가.** `daily_order.py` 와 `pending_order.py` 가 `self.fetch(..., page=page)`
를 호출하고 있었습니다. `fetch()` 에는 `page` 인자가 없으므로 **첫 호출에서
`TypeError` 로 죽습니다.** 국내 일별 체결내역 조회와 국내 미체결 주문 조회가
그 상태였습니다.

테스트가 이것을 잡지 못한 이유는 가짜 `fetch` 가 `**kwargs` 를 받았기
때문입니다. 목은 시그니처를 검사하지 않습니다. 그래서 소스를 직접 봅니다.

`call()` 은 스펙에서 `page_size` 를 읽어 커서 길이를 맞추므로 페이징이 있는
엔드포인트는 `call(ep, page=...)` 로 가야 합니다.
"""

import ast
import inspect
import pathlib

import pytest

from vmkis.kis import VmKis

SRC = pathlib.Path(inspect.getfile(VmKis)).parent
FETCH_PARAMS = set(inspect.signature(VmKis.fetch).parameters) - {"self"}
CALL_PARAMS = set(inspect.signature(VmKis.call).parameters) - {"self", "endpoint"}


def _method_calls(name: str):
    """`self.<name>(...)` 호출부를 (파일, 행, 키워드집합) 으로 모읍니다."""
    for path in sorted(SRC.rglob("*.py")):
        tree = ast.parse(path.read_text(), filename=str(path))

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            func = node.func

            if (
                isinstance(func, ast.Attribute)
                and func.attr == name
                and isinstance(func.value, ast.Name)
                and func.value.id == "self"
            ):
                keywords = {kw.arg for kw in node.keywords if kw.arg is not None}
                yield path.relative_to(SRC.parent), node.lineno, keywords


@pytest.mark.parametrize(
    ("method", "allowed"),
    [("fetch", FETCH_PARAMS), ("call", CALL_PARAMS)],
)
def test_call_sites_match_signature(method, allowed):
    """받지 않는 키워드를 넘기는 호출부가 없어야 합니다."""
    violations = [
        f"{path}:{lineno} — {method}() 가 받지 않는 인자 {sorted(keywords - allowed)}"
        for path, lineno, keywords in _method_calls(method)
        if keywords - allowed
    ]

    assert not violations, "\n".join(violations)


def test_fetch_never_receives_page():
    """`page` 는 `call()` 의 인자입니다.

    `fetch()` 에 넘기면 죽고, 넘기지 않으면 커서 길이와 `continuous` 를 손으로
    맞춰야 합니다. 페이징이 있는 엔드포인트는 `call()` 로 가야 합니다.
    """
    offenders = [f"{path}:{lineno}" for path, lineno, keywords in _method_calls("fetch") if "page" in keywords]

    assert not offenders, "fetch() 에 page 를 넘기는 곳: " + ", ".join(offenders)
