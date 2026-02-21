# Session State

## Pipeline Status

- smoke.errors: 0 | validation.errors: 0 | augment.errors: 0
- scan.warnings: 390 | normalize.warnings: 405
- smoke.skipped: 76 (not_read_only)
- enum candidates: ready=0, hold=0
- manual review: total_fields=0, endpoints=0
- tests: 140 passed
- last_run: 2026-02-20

## Active Work

- 문서화 시스템 구축 완료 (specs/, .agents/, openspec/)
- L1 Service Layer 구축 진행 중 (ADR-012)
  - ✅ Infrastructure: enums, enum_map, types, convert
  - ✅ Drift detection: scripts/check_l0_drift.py + manifest + pre-commit hook
  - ✅ Quote domain: models, service, domestic/overseas mappers, 32 tests
  - ✅ /service-build skill 정의
  - ⬜ Chart domain (multi-call)
  - ⬜ Order + Balance domains

## Quick Commands

- Pipeline: `PYTHONPATH=src .venv/bin/python -c "from codegen.api.pipeline import run_pipeline; run_pipeline()"`
- Test: `.venv/bin/python -m pytest -q`
- Lint: `.venv/bin/ruff check . && .venv/bin/ty check`

## References

- Governance: `specs/governance/`
- Architecture: `specs/architecture/`
- Archive: `docs/archive/` (resolved history: `context_solved.md`)
