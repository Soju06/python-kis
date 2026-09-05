# 2026-08-29 - #50 import-linter 계약 도입

## 사용자 요청

> #50 착수해줘

([#50](https://github.com/visualmoney/vm-stock-kis/issues/50)
`ci: import-linter 계약으로 아키텍처 역방향 의존 회귀 차단`)

## 분석

### 작업 범위

[#17](https://github.com/visualmoney/vm-stock-kis/issues/17) ·
[#18](https://github.com/visualmoney/vm-stock-kis/issues/18) 이 해소한 역방향
간선 2건(`client → api`, `utils → client`)이 다시 생기지 않도록 계약으로
고정합니다. 현재는 파일 하나씩만 보는 AST 테스트 2건이 그 역할을 대신합니다.

- `[dependency-groups] lint` 에 `import-linter` 추가
- 계약 2개 정의 (`utils` 최하위 · `client` 는 `api` 를 모름)
- `client/messaging.py:52` 지연 import 예외 처리 + 사유 주석
- `ci.yml` 의 `lint` 잡에 `lint-imports` 스텝 추가
- 아키텍처 문서 갱신

### 제외 (이슈 본문 명시)

- `event → api` 판정 — 별건
- `responses → client`, `api ↔ adapter` — 의도적으로 동결된 간선
- 기존 AST 테스트 제거 — import-linter 는 CI 전용, AST 테스트는 `pytest` 만으로 돎

### 착수 전 실측

이슈 본문의 전제를 코드에 대고 확인했습니다(AST 전수 스캔).

| 전제 | 실측 |
|---|---|
| `utils` 가 상위를 import 하지 않는다 | ✅ `utils` 의 vmkis 내부 import **0건** |
| `client → api` 는 지연 import 1건뿐 | ✅ `client/messaging.py:52` 단 1건 |
| 그 지연 import 에 사유 주석이 있다 | ❌ **없습니다** — 불변식 3번 위반 |

`client → api` 계약을 걸면 이 1건이 유일한 위반이 됩니다.

### 이슈 본문의 오류 1건

> `ARCHITECTURE.md` 불변식 4번("import-linter 도입 권장")을 완료로 갱신

`ARCHITECTURE.md` 불변식 4번은 **"`event/` 는 이 그림에 포함됩니다"** 입니다.
"import-linter 도입 권장"은
`docs/reports/2026-08-27_ARCHITECTURE_COMPARISON_OPEN_TRADING_API_KR.md:428`
의 **권장사항 4번**이고, 보고서는 동결 문서라 고치지 않습니다.

기계화되는 것은 **불변식 2번**("새로운 모듈-레벨 역방향 간선을 만들지 않습니다")
이므로 갱신 대상은 그쪽입니다.

## 계획

1. `import-linter` 를 `lint` 의존성 그룹에 추가하고 `uv lock`
2. `pyproject.toml` 에 `[tool.importlinter]` 계약 2개 정의
3. `messaging.py:52` 에 사유 주석 + `ignore_imports` 에 사유와 함께 등록
4. **위반을 일부러 만들어 계약이 실패하는지 확인** (완료 기준)
5. `ci.yml` `lint` 잡에 스텝 추가
6. `ARCHITECTURE.md` 불변식 2번 갱신
7. 개발 일지 작성

## 결과

완료. 개발 일지: [`2026-08-29_01_issue50_import_linter.md`](../dev_logs/2026-08-29_01_issue50_import_linter.md)

계획 대비 늘어난 것 2건 — 둘 다 계약을 넣지 않으면 보이지 않던 것입니다.

1. **`root_packages` 복수 나열 + 그래프 커버리지 가드 테스트.**
   `__init__.py` 없는 디렉터리 13개 때문에 `root_package = "vmkis"` 로는 모듈
   92개 중 20개만 잡혔습니다.
2. **`utils/diagnosis.py` 의 `import vmkis` 제거.**
   착수 전 실측이 "utils 의 vmkis 내부 import 0건"이라 했던 것이 틀렸습니다.
   루트 파사드 import 는 그룹 대 그룹으로 보는 스캔에 잡히지 않습니다.
