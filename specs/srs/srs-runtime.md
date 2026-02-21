# SRS: Runtime SDK Requirements

## 3.1 Async/Sync Architecture

SyRS-R001: The SDK shall implement all public APIs as async-first, with synchronous wrappers auto-generated via unasync.
- Traces to: SR-D002
- Technology: asyncio, unasync
- Constraint: `/_async/` is source of truth, `/_sync/` is build artifact
- Verification: Same test suite passes for both async and sync paths

SyRS-R002: The SDK shall provide full type annotations on all public APIs for IDE auto-completion support.
- Traces to: SR-D001
- Technology: Pydantic (public models), dataclass (internal)
- Constraint: No `Any` in public surface; `ty check` must pass
- Verification: `ty check` clean, IDE completion test

## 3.2 Data Models

SyRS-R003: The SDK shall use `Decimal` for all financial values (prices, amounts, fees, P/L, rates) in Layer 2 public surface.
- Traces to: SR-D004
- Constraint: Never use `float` for financial values in public contracts
- Verification: Type check + unit test with precision edge cases

SyRS-R004: The SDK shall provide Layer 0 Raw models that mirror exact API response structure with Pydantic.
- Traces to: SR-C001
- Technology: Pydantic with `extra="ignore"`, alias support
- Constraint: Generated, not hand-edited
- Verification: `validation.errors == 0` in pipeline

SyRS-R005: The SDK shall use timezone-aware `datetime` (UTC) for all time values in Layer 2 public surface.
- Traces to: SR-D004
- Constraint: ISO 8601 serialization
- Verification: Unit test with timezone conversion

## 3.3 Streaming

SyRS-R006: The SDK shall support WebSocket-based real-time market data streaming with async-first interface.
- Traces to: SR-M001
- Technology: websockets, asyncio
- Constraint: appkey-shared session pool, 41-subscription cap
- Verification: Integration test with live WebSocket

SyRS-R007: The SDK shall implement explicit subscription lifecycle with `aclose()`/`close()`.
- Traces to: SR-M001
- Constraint: No GC-based cleanup
- Verification: Subscription create → receive → close test

SyRS-R008: The SDK shall implement reconnect/resubscribe flow with deterministic replay on connection loss.
- Traces to: SR-M001
- Constraint: Active subscriptions replayed in deterministic order
- Verification: Simulated disconnect test

## 3.4 Error Handling

SyRS-R009: The SDK shall raise SDK-specific exceptions with context (endpoint, request_id, domain).
- Traces to: SR-D003
- Constraint: Never swallow exceptions silently
- Verification: Error messages include actionable context

SyRS-R010: The SDK shall support per-endpoint response validation with deterministic rules.
- Traces to: SR-D003
- Technology: Validator rule objects in Endpoint definition
- Constraint: Rules defined in `data/overrides/type_overrides.yaml`
- Verification: Unit test with sentinel payloads

## 3.5 Store (Master Data)

SyRS-R011: The SDK shall provide master data (stock info files) via MasterStore service.
- Traces to: SR-A001
- Technology: SQLite snapshot backend
- Constraint: Optional subsystem, lazy initialization
- Verification: Symbol lookup test
