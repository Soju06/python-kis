"""`import vmkis` 가 helpers/simple 의 결함을 가리지 않아야 합니다. (이슈 #73)

`vmkis/__init__.py` 에는 이런 폴백이 있었습니다.

```python
try:
    from vmkis.helpers import create_client, save_config_interactive
except ImportError:
    create_client = None
    save_config_interactive = None
```

이게 걸리면 `import vmkis` 는 **성공**하고, 사용자는 한참 뒤 호출 지점에서
`TypeError: 'NoneType' object is not callable` 을 받습니다. 원인 모듈 이름이
어디에도 나오지 않습니다. 예제 9개가 `from vmkis import create_client` 를
쓰므로 그 비용은 가장 디버깅을 못 하는 사용자에게 갑니다.

**결함을 되살려 확인했습니다** — `try/except` 를 되돌리면 이 파일의
`test_broken_*` 두 건이 `SWALLOWED None` 로 실패합니다.
"""

from __future__ import annotations

import subprocess
import sys
import textwrap

import pytest

#: 루트가 조용한 None 으로 만들던 이름들.
FALLBACK_NAMES = ("create_client", "save_config_interactive", "SimpleKIS")


def _import_vmkis_with_broken(module: str) -> str:
    """`module` 의 import 를 고장 낸 하위 프로세스에서 `import vmkis` 를 합니다.

    `sys.modules[name] = None` 은 CPython 이 그 이름의 import 를 ImportError 로
    중단시키는 표준 동작입니다. 실제 파일을 건드리지 않고 "helpers 안에 버그가
    있다"와 같은 상태를 만들 수 있습니다.

    하위 프로세스를 쓰는 이유는 `vmkis` 가 이미 import 된 테스트 세션에서는
    `sys.modules` 캐시 때문에 이 경로가 아예 실행되지 않기 때문입니다.
    """
    code = textwrap.dedent(
        f"""
        import sys

        sys.modules[{module!r}] = None  # import 를 ImportError 로 중단시킵니다

        try:
            import vmkis
        except ImportError as exc:
            print("RAISED", type(exc).__name__)
        else:
            print("SWALLOWED", *(getattr(vmkis, n, "<없음>") for n in {FALLBACK_NAMES!r}))
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"하위 프로세스가 죽었습니다:\n{result.stderr}"
    return result.stdout.strip()


@pytest.mark.parametrize("module", ["vmkis.helpers", "vmkis.simple"])
def test_broken_submodule_is_not_swallowed(module: str) -> None:
    """helpers/simple 이 import 에 실패하면 `import vmkis` 도 실패해야 합니다."""
    output = _import_vmkis_with_broken(module)

    assert output.startswith("RAISED"), (
        f"`{module}` 이 고장 났는데 `import vmkis` 가 통과했습니다. 공개 이름이 조용히 None 이 됩니다: {output}"
    )


def test_public_helper_names_are_usable() -> None:
    """정상 설치에서 세 이름은 None 이 아니라 호출 가능한 객체여야 합니다.

    위 두 건은 "실패가 안 보인다"를 막습니다. 이 건은 그 반대편 —
    폴백을 지우면서 이름 자체를 떨어뜨리지 않았는지를 봅니다.
    """
    import vmkis

    for name in FALLBACK_NAMES:
        obj = getattr(vmkis, name, None)
        assert obj is not None, f"`vmkis.{name}` 이 None 입니다"
        assert callable(obj), f"`vmkis.{name}` 이 호출 가능하지 않습니다: {obj!r}"

    assert set(FALLBACK_NAMES) <= set(vmkis.__all__)
