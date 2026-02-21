---
status: accepted
date: 2026-02-12
---

# ADR-006: HITL Override Approval

## Context

코드젠이 문서와 실응답 간 불일치를 감지하면 override로 보정할 수 있으나, 자동 적용은 오탐 위험이 있음.

## Decision

- Override는 자동 반영 금지
- 모든 type override에 승인 메타데이터 필수 (`approved_by`, `approved_at`, `reason`, `evidence`)
- 파이프라인이 후보를 자동 생성하되, 적용은 사용자 승인 후에만

## Consequences

- 안전성 확보 — 오탐에 의한 타입 손상 방지
- 승인 프로세스 오버헤드 존재하나 SDK 안정성이 우선
- 후보 생성 → 분석 → HITL 제시 → 승인 → 반영 → 검증 워크플로우
