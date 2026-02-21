# Override Policy

Override 승인 및 반영에 관한 거버넌스 정책.

## Principles

1. Override는 **자동 반영 금지** — 반드시 사용자 승인 필요
2. 최소 변경 원칙 — 필요 최소한의 override만 적용
3. 근거 기반 — 모든 override에 evidence 첨부 필수

## Override Types

### Type Overrides (`data/overrides/type_overrides.yaml`)

KIS API 문서와 실응답 간 불일치를 보정.

적용 대상:
- `output_kinds`: output 모델 kind 변경 (single → array)
- `enums`: 문서 미등록 enum 값 추가
- `optional_fields`: required → optional 완화
- `validator`: 응답 검증 규칙

### Augment Overrides (`data/overrides/augment_overrides.yaml`)

Smoke test 파라미터 안정화.

적용 대상:
- 종목코드, 날짜, 시장코드 등 smoke test 입력값 고정

## Required Metadata

모든 type override 항목에 필수:

```yaml
- id: "<endpoint-uuid>"
  changes: { ... }
  approved_by: "<reviewer>"
  approved_at: "YYYY-MM-DD"
  reason: "<why override is needed>"
  evidence: "<report path or payload sample>"
```

## Approval Process

1. **후보 식별**: 파이프라인 리포트에서 자동 추출
2. **분석**: 근거 + 트레이드오프 + 대안 검토
3. **HITL 제시**: 사용자에게 후보 목록 + 추천 제시
4. **승인/거부**: 사용자 결정
5. **반영**: 승인 시 YAML 업데이트 + 메타데이터 기록
6. **검증**: 파이프라인 재실행 + quality gate 통과

## Quality Gate (반영 후 완료 조건)

- 파이프라인 정상 종료
- `smoke.errors == 0`
- `validation.errors == 0`
- `augment.errors == 0`
- `.venv/bin/python -m pytest -q` 통과
- `.venv/bin/ruff check .` 통과
- `.venv/bin/ty check` 통과

## Priority Classification

Override 후보 자동 분류 기준:

| Classification | Criteria | Action |
|---------------|----------|--------|
| `ready` | response 위치, 소수 값, 명확한 enum drift | 승인 우선 |
| `hold` | request 위치, 고카디널리티, 시간형, 소수점형 | 파서/추론 보정 후 재검토 |
| `reject` | 파서 오탐, 설명 문구 오인 | codegen 수정으로 해결 |

## Decision Principles

1. **실응답이 문서보다 우선** — 단, 파서 오탐 가능성 먼저 배제
2. **enum이 폐쇄 집합이 아니면 str 완화 우선** — 무리한 enum 강제 회피
3. **파서/추론 품질 개선이 override보다 우선** — 근본 원인 해결 우선
