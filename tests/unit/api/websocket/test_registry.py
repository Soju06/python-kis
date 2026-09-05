"""이슈 #17 — 실시간 응답 레지스트리의 자기등록.

예전에는 `api/websocket/__init__.py` 가 dict 리터럴을 소유하고
`client/websocket.py` 가 그것을 import 했다. 통신 계층이 상위 계층에
의존하는 역방향 간선이었고, TR 하나를 추가할 때마다 client 까지 바뀌었다.

지금은 레지스트리가 `responses/` 에 있고 각 응답 클래스가 데코레이터로
자기등록한다. **등록이 안 되면 구독은 되지만 수신 이벤트가 조용히
버려지므로**, 아래 테스트들이 그 회귀를 잡는다.
"""

import ast
import pathlib
import subprocess
import sys

import pytest

from vmkis.responses.websocket import (
    ENCRYPTED_TR_IDS,
    WEBSOCKET_RESPONSES_MAP,
    register_websocket_response,
)


class TestRegistryIsPopulated:
    def test_registry_is_not_empty(self):
        """비어 있으면 모든 실시간 이벤트가 조용히 사라진다."""
        assert WEBSOCKET_RESPONSES_MAP, "레지스트리가 비었습니다. 자기등록이 동작하지 않습니다."

    @pytest.mark.parametrize(
        "tr_id",
        ["H0STCNT0", "HDFSCNT0", "H0STASP0", "HDFSASP1", "HDFSASP0", "H0STCNI0", "H0STCNI9", "H0GSCNI0", "H0GSCNI9"],
    )
    def test_known_tr_ids_are_registered(self, tr_id):
        assert tr_id in WEBSOCKET_RESPONSES_MAP

    def test_encrypted_tr_ids(self):
        """암호화 TR 목록도 선언에서 나온다. 예전에는 client 에 하드코딩돼 있었다."""
        assert ENCRYPTED_TR_IDS == {"H0STCNI0", "H0STCNI9", "H0GSCNI0", "H0GSCNI9"}

    def test_registry_populated_in_a_fresh_interpreter(self):
        """`import vmkis` 만으로 등록이 끝나야 한다.

        지금도 `VmKis` -> adapter -> api 경로로 우연히 로드되지만, 어댑터를
        리팩터링하면 그 경로가 끊길 수 있다. `vmkis/__init__.py` 의 명시적
        import 가 이것을 고정하며, 이 테스트가 그것을 지킨다.
        """
        code = "import vmkis;from vmkis.responses.websocket import WEBSOCKET_RESPONSES_MAP as m;print(len(m))"
        out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)

        assert out.returncode == 0, out.stderr
        assert int(out.stdout.strip()) > 0, "새 인터프리터에서 레지스트리가 비었습니다."


class TestNoReverseDependency:
    def test_client_websocket_does_not_import_api(self):
        """`client` 는 `api` 를 모듈 레벨에서 import 하지 않아야 한다."""
        source = pathlib.Path("src/vmkis/client/websocket.py").read_text(encoding="utf-8")
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

        assert not offenders, f"client/websocket.py 가 상위 계층을 import 합니다: {offenders}"


class TestDecorator:
    def test_registers_and_returns_class(self):
        sentinel = "TEST_TR_ID_DO_NOT_USE"

        try:

            @register_websocket_response(sentinel)
            class Dummy:
                pass

            assert WEBSOCKET_RESPONSES_MAP[sentinel] is Dummy
        finally:
            WEBSOCKET_RESPONSES_MAP.pop(sentinel, None)

    def test_multiple_tr_ids_and_encrypted_flag(self):
        ids = ("TEST_A_DO_NOT_USE", "TEST_B_DO_NOT_USE")

        try:

            @register_websocket_response(*ids, encrypted=True)
            class Dummy:
                pass

            assert all(WEBSOCKET_RESPONSES_MAP[i] is Dummy for i in ids)
            assert all(i in ENCRYPTED_TR_IDS for i in ids)
        finally:
            for i in ids:
                WEBSOCKET_RESPONSES_MAP.pop(i, None)
                ENCRYPTED_TR_IDS.discard(i)
