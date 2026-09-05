# 2026-08-28 - Issue #17 WebSocket 레지스트리 자기등록 개발 일지

**대상 이슈**: [#17](https://github.com/visualmoney/vm-stock-kis/issues/17)

---

## 요약

```text
990 passed, 7 skipped / TOTAL 90.83%
런타임 모듈레벨 역방향 의존: 11건 -> 10건
client -> api 간선 제거 (ARCHITECTURE.md 의 "정리 대상" 2건 모두 해소)
```

---

## 착수 전 크기 비교 — #43 보다 #17 을 먼저 한 이유

| | #43 남은 작업 | #17 |
|---|---|---|
| 수정 지점 | 10곳 / 5개 파일 | **3곳 / 2개 파일** |
| 영향 테스트 | `test_info.py` 30 · `test_daily_chart.py` 48 = **78곳** | `monkeypatch.setitem` 6곳 |
| 테스트 위험 | 🔴 높음 | 🟢 낮음 |

**시세 계열은 `fake_kis = Mock()` 을 씁니다.** `Mock` 은 속성을 자동 생성하므로
`self.call(...)` 이 조용히 Mock 을 반환합니다 — **테스트가 아무것도 검증하지
않으면서 통과**할 수 있습니다. 계좌 계열은 `FakeKis` 가 `fetch` 를 명시적으로
정의해 즉시 깨졌기에 바로 알아챘지만, 여기서는 실패조차 나지 않습니다.

---

## 설계 — 레지스트리를 `responses/` 에 두었다

이슈는 "레지스트리 소유권을 client 로 옮기고 api 가 자기등록"을 제안했습니다.
**한 단계 더 내렸습니다.**

| 위치 | client 에서 | api 에서 |
|---|---|---|
| `api/websocket/` (이전) | ❌ 역방향 | 정방향 |
| `client/websocket.py` (이슈 제안) | 정방향 | 정방향 |
| **`responses/websocket.py` (채택)** | **정방향** | **정방향** |

`client/websocket.py` 는 **이미** `from vmkis.responses.websocket import
KisWebsocketResponse` 를 하고 있었습니다. 즉 **새 import 간선이 하나도 생기지
않습니다.** 그리고 "TR ID → 응답 클래스" 는 응답 도메인 지식이므로 의미상으로도
`responses/` 가 맞습니다.

## 하드코딩 튜플도 함께 없앴다

```python
# 이전 — client/websocket.py
if tr.id in ("H0STCNI0", "H0STCNI9", "H0GSCNI0", "H0GSCNI9"):
```

암호화 TR 을 추가할 때 이 파일도 함께 고쳐야 했습니다. 이제 응답 클래스가
`encrypted=True` 로 선언하고 `ENCRYPTED_TR_IDS` 가 자동으로 채워집니다.

---

## 가장 위험했던 지점 — 등록 시점

`client/websocket.py:19` 가 **`vmkis.api.websocket` 을 import 하는 유일한
곳**이었습니다. 그냥 지우면 응답 클래스가 로드되지 않아 레지스트리가 비고,
**모든 실시간 이벤트가 조용히 사라집니다.** 이 이슈가 없애려던 바로 그 실패
모드입니다.

지우고 나서 확인해 보니 여전히 동작했는데, **왜 동작하는지**를 추적했습니다.

```text
vmkis/__init__ -> vmkis.kis -> (클래스 본문 import) -> adapter/websocket/price
                                                    -> api/websocket/*
```

**우연이었습니다.** 어댑터를 리팩터링하면 이 경로가 끊기고 실시간이 죽습니다.
그래서 두 가지를 했습니다.

1. `vmkis/__init__.py` 에 **명시적 등록 import** 를 넣어 경로를 고정
2. **새 인터프리터에서 `import vmkis` 만으로 레지스트리가 채워지는지** 검증하는
   테스트 추가 (`subprocess` 로 격리 실행)

두 번째가 핵심입니다. 같은 프로세스 안에서는 다른 테스트가 이미 모듈을
적재해 놓아 **거짓 통과**가 나기 쉽습니다.

---

## 테스트

`tests/unit/api/websocket/test_registry.py` 신규 15개.

| 테스트 | 검증 |
|---|---|
| `test_registry_is_not_empty` | 비면 모든 이벤트가 사라진다 |
| `test_known_tr_ids_are_registered` (9) | TR 9종 |
| `test_encrypted_tr_ids` | 암호화 목록이 선언에서 나온다 |
| `test_registry_populated_in_a_fresh_interpreter` | **새 프로세스**에서 등록 확인 |
| `test_client_websocket_does_not_import_api` | AST 로 역방향 간선 회귀 차단 |
| 데코레이터 2건 | 다중 TR, `encrypted` 플래그 |

`test_client_websocket_does_not_import_api` 는 #18 의
`test_retry_module_imports_nothing_from_vmkis` 와 같은 발상입니다.
**import-linter 도입 전까지의 경량 대체재**입니다.

---

## 하위 호환

`from vmkis.api.websocket import WEBSOCKET_RESPONSES_MAP` 는 그대로 동작합니다
(재export). 기존 테스트 6곳의 `monkeypatch.setitem` 도 같은 dict 객체를
가리키므로 수정이 필요 없었습니다.

`api/websocket/__init__.py` 의 import 들은 **부수효과가 목적**이라 ruff 가
`F401` 로 잡았습니다. `__all__` 에 넣어 의도를 드러냈습니다 — `# noqa` 로
덮는 것보다 정직합니다.

---

## 변경 파일

- `src/vmkis/responses/websocket.py` — 레지스트리, `ENCRYPTED_TR_IDS`, 데코레이터
- `src/vmkis/api/websocket/*.py` — 응답 클래스 7개에 데코레이터
- `src/vmkis/api/websocket/__init__.py` — dict 리터럴 제거, 재export
- `src/vmkis/client/websocket.py` — 역방향 import 제거, 하드코딩 튜플 제거
- `src/vmkis/__init__.py` — 명시적 등록 import
- `tests/unit/api/websocket/test_registry.py` — 신규
- `docs/architecture/ARCHITECTURE.md`, `docs/user/EXTENDING_API.md`

## 다음 할 일

- [ ] **import-linter 도입** — 정리 대상 2건이 모두 끝났으므로 이제 계약을
      걸 수 있다. `utils → 상위 금지`, `client → api 금지`.
      지금은 AST 테스트 2개가 그 역할을 대신한다
- [ ] [#43](https://github.com/visualmoney/vm-stock-kis/issues/43) 시세 계열 —
      `Mock()` 의 자동 속성 생성 때문에 테스트가 조용히 통과할 수 있으니
      78곳을 하나씩 확인해야 한다
- [ ] 서드파티가 라이브러리 수정 없이 실시간 TR 을 추가할 수 있게 됐다.
      `EXTENDING_API.md` Level 3 에 반영했다
