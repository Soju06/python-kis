---
status: accepted
date: 2026-01-16
---

# ADR-004: Appkey-Shared WebSocket Sessions

## Context

KIS는 계좌(앱키)당 1개 WebSocket 세션만 허용하고, 실시간 구독 총합 41건으로 제한. 여러 구독을 1 세션에서 관리해야 함.

## Decision

- `SessionPool`: `(app_key, domain)` 키로 1 세션만 유지
- `SubscriptionRegistry`: 한 세션당 41개 cap 강제
- 명시적 `aclose()` 기반 구독 해지 (GC 의존 없음)

## Consequences

- 동일 앱키로 여러 구독 시 자동으로 세션 공유
- 41개 제한 초과 시 즉시 에러 (silent drop 없음)
- 재연결 시 active subscriptions deterministic replay
