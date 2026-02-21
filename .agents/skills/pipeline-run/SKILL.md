# /pipeline-run

코드젠 파이프라인 전체 실행 + 검증 + 리포트 오케스트레이션 스킬.

## Description

코드젠 파이프라인을 실행하고, 결과를 분석하여 에러를 분류하며, context.md를 업데이트합니다.

## Workflow

### Phase 0: Pre-check

코드 품질 선행 검사.

```bash
.venv/bin/ruff check .
.venv/bin/ty check
```

실패 시 수정 후 재시도.

### Phase 1: Pipeline Execution

```bash
PYTHONPATH=src .venv/bin/python -c "from codegen.api.pipeline import run_pipeline; run_pipeline()"
```

### Phase 2: Analysis & Classification

리포트 파일 분석:

- `tmp/docs/reports/summary.json` — 전체 요약
- `tmp/docs/reports/smoke.json` — smoke 결과 (`errors`, `warnings`, status 분포)
- `tmp/docs/reports/validation.json` — validation 결과
- `tmp/docs/reports/augment.json` — augment 결과

에러 분류:
- `request_error` → augment_overrides.yaml 파라미터 수정 후보
- `server_nondeterminism` → warning 유지
- `doc_mismatch` → type_overrides.yaml override 후보
- `parser_false_positive` → codegen 로직 수정 후보

Override 후보 식별:
- `tmp/docs/reports/type_override_candidates_enum_priority.json`
- `tmp/docs/reports/manual_enum_review_candidates.json`

`context.md` 수치 업데이트.

### Phase 3: Quality Gate

```bash
.venv/bin/python -m pytest -q
```

확인 항목:
- `smoke.errors == 0`
- `validation.errors == 0`
- `augment.errors == 0`
- pytest 전체 통과

결과 요약 출력.

## Output

```
Pipeline Results:
- smoke: errors=0, warnings=N
- validation: errors=0
- augment: errors=0
- tests: N passed
- override candidates: ready=N, hold=N
```
