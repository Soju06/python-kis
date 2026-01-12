# AGENTS

## Environment
- Python: .venv/bin/python (uv, CPython 3.13.3)

## Project Vocabulary
- **Demo trading**: Use "demo" for simulated/paper trading environments
- **Real trading**: Use "real" for live trading with actual money
- **Endpoints**: API endpoints are identified by UUID and have both demo and real variants
- **Raw models**: Generated Pydantic models that mirror the exact API response structure
- **Domain models**: Hand-written business logic models that provide ergonomic interfaces

## Code Conventions (Python Library / SDK)
- Prefer **small, stable, well-typed** public APIs. Avoid “internal frameworks” and heavy magic.
- Keep boundaries explicit: **pure transforms** vs **I/O** (HTTP/WebSocket/files). I/O should be injectable for testability.
- Treat **spec/doc ingestion** and **code generation** as build-time concerns; runtime must remain deterministic and offline.
- Use **absolute imports** only to avoid circular dependency issues and improve readability.
- **Enforcement**: If you encounter code that violates these conventions, **do not ignore it**; you must fix it to align with the standards.

## Responsibility & Layering
- Each module/class should have **one reason to change** and a narrow public surface.
- Keep a clear layering boundary:
  - **API surface**: user-facing clients, convenience helpers, stable exports.
  - **Domain contracts**: typed models/enums + pure transformations (no network, no filesystem).
  - **Transport**: request building, sending, retries/timeouts, response decoding (no domain-specific business rules).
  - **Tooling**: docs/spec ingestion and code generation (build-time only; never required at runtime).
- Avoid bidirectional dependencies between layers; depend “downwards” only.

## Typing & Data Contracts
- Prefer strict typing end-to-end. Avoid `Any`, untyped `dict`, and ad-hoc `Mapping[str, object]` when the shape is known.
- Use `dataclass`/`Enum` for internal domain values; use **Pydantic models** when you need validation, alias mapping, or ergonomic computed fields.
- **Enforce `slots=True` (or `__slots__`)** for predictable data models to optimize memory and prevent attribute sprawl.
- Convert boundary payloads (JSON/dicts) into typed models early; do not leak raw payloads across layers.
- Be forward-compatible with external APIs: prefer explicit aliases and tolerate unknown fields (e.g., `extra="ignore"` in models).
- Time values: use timezone-aware `datetime` (UTC) in the public surface and serialize as ISO 8601 strings.
- Financial numeric values (prices, amounts, fees, P/L, rates): **always use `Decimal`** in public data contracts (never `float`).

## Public API Design
- Public surface should be discoverable and minimal; add convenience shortcuts sparingly.
- Avoid side effects at import time (network calls, reading secrets, global singletons).
- Keep `__init__` exports intentional; do not re-export large dependency graphs by default.

## Sync / Async Strategy
- Pick a single source of truth (prefer **async** for network-bound SDKs) and implement sync wrappers as thin adapters.
- Never block the event loop; do not use blocking I/O inside async code paths.
- Resource lifecycle must be explicit (`close()` / `aclose()`); avoid GC-based cleanup.

## Transport, Errors, and Retries
- Always set timeouts and provide actionable errors. Never swallow exceptions silently.
- Raise SDK-specific exception types that preserve root cause and include context (endpoint, request id, etc.).
- Retries/backoff must be opt-in and conservative; never retry non-idempotent operations by default.

## Code Generation & Automation
- Generated files must be deterministic and reproducible; **do not hand-edit generated code**.
- Keep templates small and composable; keep naming/normalization logic in handwritten layers.
- When the contract changes (field names/types/defaults), update tests and snapshots to match the new typed schema.

## Testing
- Unit tests: fast, isolated, deterministic (fixed timestamps, explicit payloads).
- Integration tests: can exercise multiple layers but must not hit real external services by default; use stubs/fixtures.
- Tests should assert public behavior (SDK outputs/exceptions), not internal implementation details.

## Security & Secrets
- Never commit secrets/tokens. Load credentials from environment variables or local secret files excluded from VCS.
- Scrub secrets from logs and exception messages.
