---
status: accepted
date: 2026-01-16
---

# ADR-010: Store Ingestion Canonical Path (SQLite Snapshot)

## Context

Store(종목정보) ingestion에 sqlite snapshot 파이프라인과 in-memory 인덱스 빌더 두 경로가 존재. 정규화 경로가 다르고 Layer 1 정책과 연결되지 않음.

## Decision

- **기본 경로**: SQLite snapshot 파이프라인
- **백엔드 스위칭**으로 in-memory 구조도 호환
- `MasterStore` 기본 반환은 국내+해외 통합 정규화/시스템 레이어
- Raw 접근은 명시적 raw 경로로 제공

## Consequences

- 단일 canonical ingestion path로 일관성 확보
- Store raw 계층에서 생성 코드와 런타임 유틸 분리 필요
- MasterStore는 optional 서브시스템으로 제공
