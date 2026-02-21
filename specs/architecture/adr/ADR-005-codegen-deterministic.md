---
status: accepted
date: 2026-01-15
---

# ADR-005: Deterministic Code Generation

## Context

코드젠 파이프라인이 동일 입력에 대해 동일 출력을 보장해야 함. Non-deterministic 생성은 불필요한 diff와 review 부담을 유발.

## Decision

- Generated files는 deterministic하고 reproducible
- Hand-edit 금지 — 수정 필요 시 override 또는 codegen 로직 변경
- 템플릿은 small, composable — naming/normalization 로직은 handwritten layers에 보관

## Consequences

- 동일 문서 + 동일 override → 동일 코드 생성
- override가 유일한 커스텀 수단 (HITL 승인 필수)
- codegen 로직 변경 시 전체 regeneration 필요
