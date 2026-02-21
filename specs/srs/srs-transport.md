# SRS: Transport & Authentication Requirements

## 3.1 Authentication

SyRS-T001: The SDK shall implement automatic token refresh using KIS `/oauth2/tokenP` endpoint.
- Traces to: SR-T001
- Technology: httpx async client
- Constraint: Token cache must be thread-safe; refresh within 5s of expiry
- Verification: Test with expired token scenario

SyRS-T002: The SDK shall support both demo and real trading environments via environment configuration.
- Traces to: SR-T002
- Constraint: Same API surface, different base URLs and TR IDs
- Verification: Unit test with environment switching

## 3.2 HTTP Transport

SyRS-T003: The SDK shall enforce rate limits per KIS API specifications.
- Traces to: SR-T003
- Constraint: real 20 req/sec, demo 2 req/sec
- Technology: Token bucket rate limiter
- Verification: Concurrent request test

SyRS-T004: The SDK shall set explicit timeouts on all HTTP requests.
- Traces to: SR-D003
- Constraint: Configurable timeout with reasonable default
- Verification: Timeout test with slow server mock

SyRS-T005: The SDK shall handle HTTP 429 (rate limit) with Retry-After header backoff.
- Traces to: SR-T003
- Constraint: Retry is opt-in and conservative; never retry non-idempotent operations by default
- Verification: 429 response handling test

## 3.3 WebSocket Transport

SyRS-T006: The SDK shall maintain one WebSocket session per (app_key, domain) pair.
- Traces to: SR-M001
- Technology: SessionPool with reference counting
- Constraint: Max 41 subscriptions per session
- Verification: Session sharing test

SyRS-T007: The SDK shall implement AES-CBC decryption for encrypted WebSocket payloads.
- Traces to: SR-M001
- Constraint: Key store updated on control messages
- Verification: Encrypted payload decryption test

## 3.4 Error Classification

SyRS-T008: The SDK shall classify transport errors into SDK-specific exception types.
- Traces to: SR-D003
- Exception hierarchy:
  - `KisAuthError` — 인증/토큰 오류
  - `KisRateLimitError` — Rate limit (429)
  - `KisTransportError` — 네트워크/전송 오류
  - `KisHttpError` — Non-OK HTTP 응답
  - `KisResponseError` — rt_cd 체크 실패
  - `KisUnsupportedEndpointError` — 도메인 미지원
- Verification: Each error type raised in appropriate scenario
