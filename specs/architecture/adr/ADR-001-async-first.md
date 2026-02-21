---
status: accepted
date: 2026-01-15
---

# ADR-001: Async-First with unasync Generation

## Context

SDK는 async와 sync 모두 지원해야 함. 두 구현을 별도로 유지하면 로직 중복과 동기화 부담이 발생.

## Decision

async를 기본 구현으로, unasync로 sync 코드를 자동 생성한다.

- `/_async/`가 source of truth
- `/_sync/`는 build artifact
- `KisAsyncClient` (async), `KisClient` (sync via unasync)

## Consequences

- sync 코드를 직접 수정하면 안 됨 — 다음 빌드에서 덮어씀
- async 구현에만 집중하면 sync도 자동 반영
- unasync 변환에 적합하도록 코드 패턴을 맞춰야 함
