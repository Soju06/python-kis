# /override-review

Override 후보 검토 및 HITL 승인 프로세스 스킬.

## Description

Override 후보를 분석하고, 거버넌스 정책 기준으로 검증하여, 사용자 승인 프로세스를 진행합니다.

## Workflow

### Phase 0: Discovery

후보 파일 읽기:

- `tmp/docs/reports/type_override_candidates_enum_priority.json` — enum override 후보
- `tmp/docs/reports/manual_enum_review_candidates.json` — 수동 검토 후보
- `data/overrides/type_overrides.yaml` — 현재 적용된 override

### Phase 1: Analysis

각 후보별:
1. 근거 분석 (smoke/augment 데이터, 문서 스펙)
2. `specs/governance/override-policy.md` 기준 검증
3. 트레이드오프 평가 (override vs 코드 수정 vs 정책 유지)

### Phase 2: HITL Presentation

사용자에게 제시:

```
Override Candidate: [endpoint-name]
- Endpoint: [UUID]
- Type: [enum_extension / output_kind / optional_field]
- Reason: [근거 요약]
- Evidence: [리포트 경로]
- Trade-off: [override 시 영향 vs 미적용 시 영향]
- Recommendation: [approve / hold / reject]
```

사용자 승인/거부 대기.

### Phase 3: Application (승인 시)

1. `data/overrides/type_overrides.yaml` 업데이트
   - 승인 메타데이터 포함: `approved_by`, `approved_at`, `reason`, `evidence`
2. `/pipeline-run` 실행 (파이프라인 재실행)
3. quality gate 통과 확인

## Override Types

| Type | YAML Key | Description |
|------|----------|-------------|
| enum_extension | `changes.enums` | 문서 미등록 enum 값 추가 |
| output_kind | `changes.output_kinds` | output 모델 kind 변경 (single→array) |
| optional_field | `changes.optional_fields` | required → optional 완화 |
