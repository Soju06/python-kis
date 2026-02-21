# Pipeline Lifecycle

코드젠 파이프라인 HITL 라이프사이클 정책.

## Lifecycle (반복)

### 1. Observe

`tmp/docs/reports/` 리포트로 현재 오류/경고를 수치화.

- `summary.json` — 전체 요약
- `smoke.json` — smoke test (API 실호출)
- `validation.json` — 모델 검증
- `augment.json` — 응답 캐시 보강

### 2. Classify

원인 분류:

| Category | Description |
|----------|-------------|
| `request_error` | 파라미터 불일치/누락 |
| `server_nondeterminism` | KIS 서버 간헐적 에러 |
| `doc_mismatch` | 문서-실응답 불일치 |
| `parser_false_positive` | 파서/추론 오탐 |
| `policy_skip` | 정책적 스킵 (not_read_only 등) |

### 3. Decide

해결 수단 선택:

| Resolution | When to Use |
|-----------|-------------|
| 파라미터 안정화 | request_error: augment_overrides.yaml 수정 |
| 런타임 완화 | nonfatal 분류 + warning 유지 |
| 파서 수정 | parser_false_positive: codegen 로직 수정 |
| Override | doc_mismatch: type_overrides.yaml (HITL 필수) |

### 4. HITL Approval

`data/overrides/type_overrides.yaml` 변경은 사용자 승인 후에만 반영.
상세: `specs/governance/override-policy.md`

### 5. Implement

최소 변경으로 코드/오버라이드 반영. 필요 시 테스트 추가.

### 6. Verify

필수 검증 순서:

```bash
PYTHONPATH=src .venv/bin/python -c "from codegen.api.pipeline import run_pipeline; run_pipeline()"
.venv/bin/python -m pytest -q
.venv/bin/ruff check .
.venv/bin/ty check
```

### 7. Record

결과를 `context.md`에 수치 반영.

## Agent ↔ User 작업 방식

### Agent 책임

- 사실 기반으로 현재 상태를 수치/파일 경로로 보고
- 변경 전 옵션과 트레이드오프를 명시
- 승인 필요한 항목(특히 type override)은 먼저 승인 요청 후 실행
- 실행 후 반드시 재검증 결과를 공유

### User 책임

- 우선순위, 위험 선호도, override 승인 여부를 명확히 결정
- API 정책성 이슈에 대한 제품 결정을 제공
