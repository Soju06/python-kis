# 2026-08-29 - #42 `__del__` 무력화 패치 제거 개발 일지

**이슈**: [#42](https://github.com/visualmoney/vm-stock-kis/issues/42)
`test: __del__ 무력화 패치 3곳이 이제 불필요합니다`
**프롬프트**: [`2026-08-29_02_issue42_del_patches.md`](../prompts/2026-08-29_02_issue42_del_patches.md)

## 걸린 것 — 패치만 지우면 **목적을 절반만 달성합니다**

이슈의 목적은 "패치 3줄 삭제"가 아니라 이것입니다.

> 소멸자를 무력화한 상태로 테스트하면 소멸자의 회귀를 못 잡습니다.
> 패치를 지우면 그 회귀가 `PytestUnraisableExceptionWarning` 으로 드러납니다.

지우고 나서 실제로 회귀를 되살려 봤습니다. `VmKis.close()` 의
`getattr(self, "_sessions", {})` 가드([#38](https://github.com/visualmoney/vm-stock-kis/issues/38))를
걷어낸 상태입니다.

```console
$ uv run pytest tests/unit/test_kis.py -q
  AttributeError: 'VmKis' object has no attribute '_sessions'
    warnings.warn(pytest.PytestUnraisableExceptionWarning(msg))
42 passed, 3 warnings in 0.24s
```

**42 passed 입니다. 초록입니다.** 회귀가 로그에 보이기는 하지만 CI 를 막지
않습니다. 경고는 원래 그렇습니다.

패치를 지운 결과가 "회귀를 못 잡는다"에서 "회귀를 잡지만 아무도 안 본다"로
바뀐 것뿐입니다. 이슈가 **"(선택)"** 으로 남긴 항목이 사실은 이 작업의 절반이었습니다.

```toml
# pyproject.toml [tool.pytest.ini_options]
filterwarnings = [
    "error::pytest.PytestUnraisableExceptionWarning",
]
```

같은 조작을 다시 하면:

```console
FAILED tests/unit/test_kis.py::test_init_value_errors
FAILED tests/unit/test_kis.py::test_init_with_virtual_auth_validation
FAILED tests/unit/test_kis.py::test_init_with_auth_virtual_error
3 failed, 39 passed in 0.54s
```

**패치가 붙어 있던 바로 그 3건이 실패합니다.** 이제서야 이슈가 말한
"회귀 탐지력"이 실재합니다.

## 되돌려 확인 (완료 기준)

| 조작 | 패치 제거만 | 패치 제거 + `filterwarnings` |
|---|---|---|
| `close()` 의 `getattr` 가드 제거 | ❌ 42 passed, 3 warnings | ✅ **3 failed**, 39 passed |
| 조작 없음 | ✅ 42 passed | ✅ 42 passed |

이슈의 완료 기준도 충족합니다.

```console
$ git grep -c 'VmKis.__del__' tests/     # 출력 없음 (0건)
$ uv run pytest -q tests/unit/test_kis.py
42 passed in 0.45s
```

## 확인한 함정 — GC 시점

`__del__` 은 GC 시점에 불리므로, 경고가 **한참 뒤의 다른 테스트**에서 터질
수 있다고 보고 단독 실행만으로 판정하지 않았습니다.

- `tests/unit/test_kis.py` 단독 — 경고 0
- 전체 스위트(`performance` 포함, 1052건) — `unraisable`·`__del__`·`AttributeError`
  문자열 0건

회귀를 되살렸을 때도 경고가 **정확히 그 3건에** 귀속됐습니다. CPython 의 참조
카운팅이 `pytest.raises` 블록을 벗어나는 즉시 회수하므로 지연이 없습니다.
전역 `filterwarnings` 를 켜도 다른 테스트가 말려들지 않는 이유입니다.

## 판단한 것

- **`error::pytest.PytestUnraisableExceptionWarning` 하나만 좁혔습니다.**
  전역 `filterwarnings = ["error"]` 는 서드파티 `DeprecationWarning` 까지 전부
  실패로 만들어 우리 코드와 무관한 이유로 red 가 됩니다. 실제로 이 스위트에는
  경고 9건이 남아 있고(전부 무해), 전역으로 켜면 그 9건이 전부 터집니다.
- **`kis.py` 의 가드에 역참조 주석을 달았습니다.** 가드를 지우면 무엇이
  깨지는지가 가드 옆에 없으면, 다음 사람은 그것을 "불필요한 방어"로 읽습니다.
  `close()` 는 이제 어느 테스트가 자기를 지키는지 말합니다.

## 변경 파일

- `tests/unit/test_kis.py` — `@patch("vmkis.kis.VmKis.__del__", ...)` 3곳 제거,
  docstring 을 "왜 무력화하는가"에서 "왜 무력화하지 않는가"로 교체
- `pyproject.toml` — `[tool.pytest.ini_options] filterwarnings` 추가
- `src/vmkis/kis.py` — `close()` 가드에 역참조 주석 (동작 변경 없음)

## 테스트 결과

```text
uv run pytest -m 'not requires_api'                     1052 passed, 8 skipped
uv run pytest -m 'not requires_api and not performance' 1023 passed, 7 skipped
coverage                                                92%  (게이트 90)
ruff check / format · lint-imports · uv lock --check    통과
git grep -c 'VmKis.__del__' tests/                      0
```

## 남은 것

없습니다. 이슈의 "할 일" 3항목(선택 항목 포함)을 전부 처리했습니다.
