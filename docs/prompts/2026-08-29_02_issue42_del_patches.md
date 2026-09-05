# 2026-08-29 - #42 `__del__` 무력화 패치 제거

## 사용자 요청

> pr #62 merge, issue #42 착수

([#42](https://github.com/visualmoney/vm-stock-kis/issues/42)
`test: __del__ 무력화 패치 3곳이 이제 불필요합니다`)

## 분석

### 배경

[#38](https://github.com/visualmoney/vm-stock-kis/issues/38) 이 `VmKis.close()` 에
`getattr(self, "_sessions", {})` 가드를 넣어 근본 원인을 고쳤습니다.
그것을 우회하던 테스트 패치 3곳이 남아 있습니다.

```text
tests/unit/test_kis.py:96   @patch("vmkis.kis.VmKis.__del__", new=lambda self: None)
tests/unit/test_kis.py:498  with patch(...)
tests/unit/test_kis.py:511  with patch(...)
```

### 왜 지우는가 — 이것이 이 작업의 전부입니다

**소멸자를 무력화한 상태로 테스트하면 소멸자의 회귀를 못 잡습니다.**
누가 `close()` 의 `getattr` 가드를 걷어내도 이 테스트들은 통과합니다.

즉 작업의 성패는 "패치를 지웠다"가 아니라 **"지운 뒤 그 회귀가 실제로
잡히는가"** 입니다. 가드를 일부러 되돌려 실패를 확인해야 합니다.

### 영향 받는 모듈

- `tests/unit/test_kis.py` — 패치 3곳 + docstring
- `pyproject.toml` — (선택) `filterwarnings` 검토

### 선택 항목의 쟁점

이슈가 "(선택)"으로 남긴 `filterwarnings` 는 사실 **핵심**일 수 있습니다.
경고는 기본적으로 CI 를 빨갛게 만들지 않습니다. 패치만 지우고 경고를 오류로
올리지 않으면, 회귀가 생겨도 로그에 줄 하나가 늘 뿐 **테스트는 통과합니다.**
그러면 "회귀 탐지력을 되찾는다"는 이슈의 목적이 절반만 달성됩니다.

전역 `filterwarnings = ["error"]` 는 범위가 너무 넓으므로
`error::pytest.PytestUnraisableExceptionWarning` 하나만 좁혀서 검토합니다.

### 예상되는 함정

`__del__` 은 **GC 시점**에 불립니다. 패치를 지운 뒤 경고가 나온다면 그것이
해당 테스트가 아니라 **한참 뒤의 다른 테스트**에서 터질 수 있습니다.
`tests/unit/test_kis.py` 단독 실행만으로 판정하면 안 되고 전체 스위트로
확인해야 합니다.

## 계획

1. 패치 3곳과 관련 docstring 제거
2. `tests/unit/test_kis.py` 단독 · 전체 스위트 양쪽에서 경고 0 확인
3. `filterwarnings` 좁힌 항목 추가 여부 판단 (근거를 일지에 기록)
4. **`close()` 의 `getattr` 가드를 일부러 되돌려** 테스트가 실패하는지 확인
5. 개발 일지 작성

## 결과

완료. 개발 일지:
[`2026-08-29_02_issue42_del_patches.md`](../dev_logs/2026-08-29_02_issue42_del_patches.md)

착수 전 예측이 둘 다 맞았습니다.

1. **"(선택)" 항목이 사실은 핵심이었습니다.** 패치만 지운 상태에서 가드를
   되돌리면 `42 passed, 3 warnings` — 초록입니다. `filterwarnings` 를 넣고서야
   `3 failed` 가 됩니다.
2. **GC 시점은 문제가 되지 않았습니다.** 참조 카운팅이 `pytest.raises` 블록을
   벗어나는 즉시 회수해, 경고가 정확히 해당 3건에 귀속됐습니다.
