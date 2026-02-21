# SRS: Codegen Pipeline Requirements

## 3.1 Pipeline Architecture

SyRS-C001: The codegen pipeline shall generate Pydantic raw models from KIS API documentation YAML files.
- Traces to: SR-C001
- Input: `data/kis/**/*.yaml`
- Output: `src/pykis/api/raw/**/*.py`
- Constraint: Deterministic, reproducible output
- Verification: Pipeline run produces identical output for same input

SyRS-C002: The codegen pipeline shall validate generated models against live API responses (smoke test).
- Traces to: SR-C002
- Constraint: `smoke.errors == 0` for release
- Verification: Pipeline smoke stage with real API calls

SyRS-C003: The codegen pipeline shall support type overrides for documented-vs-actual API mismatches.
- Traces to: SR-C001
- Input: `data/overrides/type_overrides.yaml`
- Constraint: Override requires HITL approval (see `specs/governance/override-policy.md`)
- Verification: Override application + pipeline re-run

## 3.2 Pipeline Stages

SyRS-C004: The pipeline shall execute stages in order: scan → normalize → filter → generate → augment → infer → generate → validate → smoke.
- Traces to: SR-C001
- Constraint: Each stage is idempotent
- Verification: Re-run produces same results

SyRS-C005: The augment stage shall collect live API responses for type inference and model validation.
- Traces to: SR-C002
- Constraint: Cache responses for reproducibility; probe errors are non-fatal
- Verification: Augment report with `errors == 0`

SyRS-C006: The infer stage shall determine field types from both documentation and live response samples.
- Traces to: SR-C001
- Constraint: Documentation-based type takes precedence unless overridden
- Verification: Inferred types match API behavior

## 3.3 Override System

SyRS-C007: The override system shall support enum extension, output kind change, and optional field relaxation.
- Traces to: SR-C003
- Constraint: Each override entry requires approval metadata
- Verification: Override candidates generated with evidence

SyRS-C008: The pipeline shall generate override candidates automatically but never apply them without approval.
- Traces to: SR-C003
- Output: `tmp/docs/reports/type_override_candidates_enum_priority.json`
- Constraint: `ready_overrides` are suggestions, not auto-applied
- Verification: Candidate report accuracy

## 3.4 Reporting

SyRS-C009: The pipeline shall generate structured reports for all stages.
- Traces to: SR-C002
- Output: `tmp/docs/reports/summary.json`, `smoke.json`, `validation.json`, `augment.json`
- Constraint: Reports include error counts, classifications, and evidence
- Verification: Report completeness check
