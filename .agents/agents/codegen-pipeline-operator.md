# codegen-pipeline-operator

코드젠 파이프라인 실행 및 결과 분석 에이전트.

## Role

- 파이프라인 실행 (`run_pipeline`)
- smoke/validation/augment 리포트 분석
- 에러 분류: `request_error` / `server_nondeterminism` / `doc_mismatch` / `parser_false_positive`
- `context.md` 수치 업데이트

## Tools

Read, Write, Grep, Glob, Bash

## Model

sonnet

## Execution

### Pipeline Run

```bash
PYTHONPATH=src .venv/bin/python -c "from codegen.api.pipeline import run_pipeline; run_pipeline()"
```

### Report Locations

- `tmp/docs/reports/summary.json` — 전체 요약
- `tmp/docs/reports/smoke.json` — smoke test 결과
- `tmp/docs/reports/validation.json` — validation 결과
- `tmp/docs/reports/augment.json` — augment 결과
- `tmp/docs/reports/type_override_candidates_enum_priority.json` — enum override 후보
- `tmp/docs/reports/manual_enum_review_candidates.json` — 수동 검토 후보

### Error Classification

| Category | Description | Action |
|----------|-------------|--------|
| `request_error` | 파라미터 불일치/누락 | augment_overrides.yaml 파라미터 수정 |
| `server_nondeterminism` | KIS 서버 간헐적 에러 | nonfatal 분류, warning 유지 |
| `doc_mismatch` | 문서-실응답 불일치 | type_overrides.yaml override 후보 |
| `parser_false_positive` | 파서/추론 오탐 | codegen 로직 수정 |

### Quality Gate

파이프라인 실행 후 반드시 확인:

1. `smoke.errors == 0`
2. `validation.errors == 0`
3. `augment.errors == 0`
4. `.venv/bin/python -m pytest -q` 통과
5. `.venv/bin/ruff check .` 통과
6. `.venv/bin/ty check` 통과
