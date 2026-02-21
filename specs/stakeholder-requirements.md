# Stakeholder Requirements (StRS)

ISO/IEC/IEEE 29148 경량 적용. SDK 사용자 관점 요구사항.

## Transport & Authentication

SR-T001: The SDK shall authenticate with KIS API using OAuth token management.
- Priority: Critical
- Verification: Integration test with demo credentials
- Acceptance: Token auto-refresh within 5s of expiry

SR-T002: The SDK shall support both demo and real trading environments.
- Priority: Critical
- Verification: Unit test with environment switching
- Acceptance: Same API surface, different endpoints

SR-T003: The SDK shall provide rate-limiting to comply with KIS API limits.
- Priority: High
- Verification: Concurrent request test
- Acceptance: real 20 req/sec, demo 2 req/sec

## Market Data

SR-M001: The SDK shall provide real-time market data via WebSocket streaming.
- Priority: High
- Verification: Integration test with live WebSocket
- Acceptance: Normalized event delivery within 100ms of receipt

SR-M002: The SDK shall provide historical price data (daily/weekly/monthly candles).
- Priority: High
- Verification: API call with date range
- Acceptance: Correct OHLCV data in typed model

SR-M003: The SDK shall unify domestic and overseas market data under a single interface.
- Priority: Medium
- Verification: Same API call pattern for KRX and NYSE
- Acceptance: Normalized field names across markets

## Trading

SR-O001: The SDK shall support order placement (buy/sell) for domestic stocks.
- Priority: Critical
- Verification: Demo order execution
- Acceptance: Order confirmation with order number

SR-O002: The SDK shall support order placement for overseas stocks.
- Priority: High
- Verification: Demo order execution
- Acceptance: Exchange-aware order routing

SR-O003: The SDK shall support order modification and cancellation.
- Priority: High
- Verification: Order → modify → cancel flow
- Acceptance: Each step returns confirmation

## Account

SR-A001: The SDK shall provide account balance and position inquiries.
- Priority: Critical
- Verification: API call with demo account
- Acceptance: Typed balance/position models

SR-A002: The SDK shall provide order history and execution details.
- Priority: High
- Verification: API call with date range
- Acceptance: Complete execution records

## Developer Experience

SR-D001: The SDK shall provide full type annotations for IDE auto-completion.
- Priority: Critical
- Verification: ty check passes
- Acceptance: All public APIs have type hints

SR-D002: The SDK shall provide both async and sync interfaces.
- Priority: Critical
- Verification: Same operations work in async and sync
- Acceptance: Sync generated from async via unasync

SR-D003: The SDK shall raise clear, actionable errors with context.
- Priority: High
- Verification: Error message includes endpoint, request context
- Acceptance: Users can diagnose issues from error alone

SR-D004: The SDK shall use Decimal for all financial values.
- Priority: High
- Verification: Price/amount fields are Decimal
- Acceptance: No float precision issues

## Code Generation

SR-C001: The SDK shall auto-generate API models from KIS documentation.
- Priority: Critical
- Verification: Pipeline run produces models
- Acceptance: Generated models match API responses

SR-C002: The SDK shall validate generated models against live API responses.
- Priority: High
- Verification: Smoke test against real API
- Acceptance: smoke.errors == 0, validation.errors == 0
