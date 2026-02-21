---
status: accepted
date: 2026-01-16
---

# ADR-007: Layer 0/1/2 Separation

## Context

KIS API는 국내/해외 형상이 크게 달라 단일 SDK 형상이 없고, raw 필드명이 한국어 축약어이며, 금융 값이 문자열로 전달됨.

## Decision

3-layer 아키텍처를 적용:

- **Layer 0 (Raw)**: API 원형 보존, codegen 산출물
- **Layer 1 (Normalize)**: 국내/해외 통합, 표준 영어 필드명
- **Layer 2 (System)**: Decimal/UTC 강제, 도메인 객체

## Consequences

- 각 레이어는 단일 책임 — Raw는 원형, Normalize는 통합, System은 편의
- 사용자는 필요한 레이어를 선택적으로 접근 가능
- 레이어 간 역방향 의존 금지 (L2 → L1 → L0만 허용)
- REST, Streaming, Store 모두 동일 레이어 원칙 적용
