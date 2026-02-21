# Quality Gates

파이프라인 및 코드 변경의 품질 게이트 정의.

## Pipeline Quality Gate

파이프라인 실행 후 반드시 통과해야 하는 조건:

| Gate | Condition | Severity |
|------|-----------|----------|
| Smoke errors | `smoke.errors == 0` | Blocking |
| Validation errors | `validation.errors == 0` | Blocking |
| Augment errors | `augment.errors == 0` | Blocking |
| Unit tests | `pytest -q` 전체 통과 | Blocking |
| Lint | `ruff check .` 통과 | Blocking |
| Type check | `ty check` 통과 | Blocking |

## Warning Thresholds

Warning은 blocking이 아니나 추적:

| Metric | Current | Target |
|--------|---------|--------|
| `smoke.warnings` (runtime) | 0 | 0 유지 |
| `smoke.skipped` (not_read_only) | 76 | 비안전 endpoint 수와 동일 |
| `scan.warnings` | ~390 | 모니터링 |
| `normalize.warnings` | ~405 | 모니터링 |

## Code Change Quality Gate

코드 변경(PR/commit) 시:

1. **Lint**: `ruff check .` 통과
2. **Type**: `ty check` 통과
3. **Tests**: `pytest -q` 전체 통과
4. **Pipeline**: codegen 관련 변경 시 파이프라인 재실행

## Override Quality Gate

Override 반영 시 추가 조건:

1. 승인 메타데이터 포함 (`approved_by`, `approved_at`, `reason`, `evidence`)
2. 파이프라인 재실행 후 전체 quality gate 통과
3. 이전 상태 대비 regression 없음
