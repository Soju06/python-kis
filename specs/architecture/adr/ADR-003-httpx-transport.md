---
status: accepted
date: 2026-01-15
---

# ADR-003: httpx as HTTP Transport

## Context

async HTTP client가 필요. requests는 sync-only, aiohttp는 API가 다르고 유지보수 우려.

## Decision

httpx를 HTTP transport로 사용한다.

## Consequences

- async/sync 모두 동일 API로 지원
- HTTP/2 지원 가능
- 타임아웃, 재시도, 인증 등 내장 기능 활용
