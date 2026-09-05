# 2026-08-28 - 세션 종료 요약

**성격**: 이날 세션 전체의 종합. 개별 작업은 같은 날짜의 다른 일지를 보세요.
**파일명**: 이 문서부터 [새 명명 규칙](../../CLAUDE.md#파일명-규칙)(`_nn_`)을 적용합니다.

---

## 한 줄

**`vm-stock-kis 0.0.1` 을 PyPI 에 첫 배포**하고, 그 전후로 PR 12건을 머지해 이슈 13건을 닫았습니다.

```text
PyPI      vm-stock-kis 0.0.1  (2026-08-28T04:05 업로드)
태그      v2.1.6 · v3.0.0rc1 · v3.0.0rc2 · v0.0.1rc1 · v0.0.1
테스트    990 passed, 7 skipped / TOTAL 90.83%  (게이트 90)
이슈      닫힘 13 / 열림 12
```

---

## 이 세션에서 배포까지 간 경로

이슈 [#2](https://github.com/visualmoney/vm-stock-kis/issues/2)(이름 변경)의 마무리가 출발점이었는데, **배포 직전 재검토에서 배포를 막아야 하는 결함이 나왔습니다.**

| 단계 | PR | 핵심 |
|---|---|---|
| 기록물 정리 | [#22](https://github.com/visualmoney/vm-stock-kis/pull/22) | `archive/` 신설. 죽은 링크 19곳 |
| 태그 규칙 | [#24](https://github.com/visualmoney/vm-stock-kis/pull/24) | `publish.yml` 이 PEP 440 정규형과 **문자열 비교**한다는 함정 |
| **배포 전 재검토** | [#26](https://github.com/visualmoney/vm-stock-kis/pull/26) | `pip install vmkis` 11곳 — **미등록·선점 가능한 이름** |
| core metadata | [#28](https://github.com/visualmoney/vm-stock-kis/pull/28) | 고정의 근거를 갱신하고 게시 전 검사 추가 |
| **배포** | — | `v0.0.1rc1` → TestPyPI → `v0.0.1` → PyPI |

### 버전을 `3.0.0` → `0.0.1` 로 바꾼 판단

업스트림 2.1.6 을 이어받는 대신 **이 배포명의 첫 릴리스**로 다시 시작했습니다. 배포명이 다르면 pip 이 두 버전을 비교하지 않으므로 이어받을 이유가 없고, 첫 릴리스가 3.0.0 인 것은 실제보다 성숙해 보이게 만듭니다. `Development Status` 도 `4 - Beta` 로 함께 내렸습니다.

---

## 반복해서 드러난 것

### 1. 이름 스윕이 만든 결함을 세 번에 걸쳐 고쳤습니다

이슈 #2 의 `\bpykis\b → vmkis` 규칙은 import 문에서는 옳지만 다른 문맥에서는 틀립니다.

| 발견 | 내용 |
|---|---|
| [#22](https://github.com/visualmoney/vm-stock-kis/pull/22) | `QuantumOmega`·`yourusername` — 존재하지 않는 저장소 19곳 |
| [#26](https://github.com/visualmoney/vm-stock-kis/pull/26) | `pip install vmkis` — 스윕이 **틀린 것을 그럴듯하게** 만듦 |
| [#26](https://github.com/visualmoney/vm-stock-kis/pull/26) | 마이그레이션 문서의 v2.x 예제가 새 이름으로 덮여 **문서가 스스로를 반박** |

### 2. "문서가 코드에 대해 사실이 아닌 것을 말한다"

[#39](https://github.com/visualmoney/vm-stock-kis/pull/39) 에서 드리프트 7건을 고치며 **암묵적 불변식을 처음 명문화**했습니다. 특히 *"`vmkis.kis` 를 모듈 레벨에서 import 하지 않는다"* — 전체 패키지가 정상 로드되는 **유일한 이유**인데 어디에도 없었습니다.

### 3. 테스트가 프로덕션 결함을 우회하고 있었습니다

`test_kis.py:96` 이 `__del__` 을 무력화하는 패치로 증상만 덮고 있었습니다([#38](https://github.com/visualmoney/vm-stock-kis/issues/38)에서 근본 원인 수정, 잔여 패치는 [#42](https://github.com/visualmoney/vm-stock-kis/issues/42)).

### 4. 역방향 의존 2건을 같은 발상으로 없앴습니다

**목록을 옮기는 대신 판단 근거를 당사자에게 넘겼습니다.**

| 간선 | 방법 |
|---|---|
| `utils → client` ([#18](https://github.com/visualmoney/vm-stock-kis/issues/18)) | 예외가 `retryable` 표식을 들고, 유틸은 `getattr` 로 확인 |
| `client → api` ([#17](https://github.com/visualmoney/vm-stock-kis/issues/17)) | 응답 클래스가 `@register_websocket_response` 로 자기등록 |

런타임 모듈레벨 역방향 **12건 → 10건**. 남은 것은 전부 의도적입니다.

---

## 검증에서 배운 것 — 되돌려 확인하기

회귀 테스트를 넣은 뒤 **버그를 일부러 되살려 실패하는지** 확인하는 습관이 두 번 값을 했습니다.

- [#18](https://github.com/visualmoney/vm-stock-kis/issues/18) — 전역 변형 코드를 되돌리니 예상대로 실패, 복원 후 통과
- [#17](https://github.com/visualmoney/vm-stock-kis/issues/17) — 레지스트리 등록이 **우연히** 동작하는 것을 발견. `import` 경로를 추적해 `adapter → api` 체인에 기대고 있음을 확인하고, `vmkis/__init__.py` 에 명시적으로 고정한 뒤 **새 인터프리터에서** `subprocess` 로 검증

두 번째가 특히 중요했습니다. 같은 프로세스 안에서는 다른 테스트가 모듈을 이미 적재해 **거짓 통과**가 납니다.

---

## 남긴 미완

### [#43](https://github.com/visualmoney/vm-stock-kis/issues/43) 이 중간 상태입니다 — 유일한 블로커성 항목

`KisEndpoint` 가 **계좌 계열에만** 적용됐습니다. 같은 코드베이스에 두 방식이 공존합니다.

```python
self.call(_DOMESTIC_BALANCE, ...)                          # 계좌 (이관됨)
self.fetch(path, api="FHKST01010100", domain="real", ...)  # 시세 (미이관)
```

남은 10곳의 이관 자체는 단순하지만 **테스트가 위험합니다.** 시세 계열은 `fake_kis = Mock()` 을 쓰는데, `Mock` 은 속성을 자동 생성하므로 `self.call(...)` 이 조용히 Mock 을 반환합니다 — **테스트가 아무것도 검증하지 않으면서 통과**할 수 있습니다. 78곳을 하나씩 확인해야 합니다.

착수 조사는 [이슈 코멘트](https://github.com/visualmoney/vm-stock-kis/issues/43#issuecomment-5450601767)와 [일지](2026-08-28_issue43_endpoint_spec.md)에 있습니다.

### 사용자에게 물어봐 두고 결론 나지 않은 것

**`real`/`virtual` → `live`/`paper` 명칭 통일.** 이슈로 등록하지 않았습니다.

- `virtual` 은 KIS 도메인(`openapi**vts**`)에서 온 이름이라 근거가 있음
- `real` 은 벤더 표기가 아니고, 코드베이스의 `Realtime*` **236곳**과 시각적으로 충돌
- 사용자가 사실상 0명인 지금이 가장 싼 시점
- 위험은 `config.yaml` 키 변경 — 안 고치면 **조용히 실전 계좌로 붙을 수 있음**

---

## 다음 세션에서 볼 것

[To-Do List](../../archive/docs/reports/2026-08-28_TODO_LIST.md) 에 우선순위와 블로커를
정리했습니다. (이 문서는 이후 `archive/` 로 옮겨졌습니다. **작업 목록은 이슈 트래커가
유일한 출처입니다** — `gh issue list`.)

## 테스트 결과

```text
uv run pytest -q -m 'not requires_api and not performance' --cov
990 passed, 7 skipped, 47 deselected
TOTAL 90.83%   (게이트 90)

uv run ruff check . && uv run ruff format --check .
All checks passed! / 188 files
```
