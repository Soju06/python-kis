## Environment
1. Python: .venv/bin/python (uv, CPython 3.13.3)

## Project Vocabulary
1. **Demo trading**: Use "demo" for simulated/paper trading environments
2. **Real trading**: Use "real" for live trading with actual money
3. **Endpoints**: API endpoints are identified by UUID and have both demo and real variants
4. **Raw models**: Generated Pydantic models that mirror the exact API response structure
5. **Domain models**: Hand-written business logic models that provide ergonomic interfaces

## Code Conventions (Python Library / SDK)
1. **Architecture & Design**
   1. Prefer **small, stable, well-typed** public APIs. Avoid “internal frameworks” and heavy magic.
   2. Keep boundaries explicit: **pure transforms** vs **I/O** (HTTP/WebSocket/files). I/O should be injectable for testability.
   3. Treat **spec/doc ingestion** and **code generation** as build-time concerns; runtime must remain deterministic and offline.
2. **Coding Style**
   1. Use **absolute imports** only to avoid circular dependency issues and improve readability.
   2. **Naming & Visibility**: Use `_leading_underscore` for private members. Use `snake_case` for public members, and `@property` for fields requiring validation or logic. Avoid abbreviations (e.g., use `request` instead of `req`, `response` instead of `res`).
3. **Maintenance & Policy**
   1. **Code Hygiene**: Aggressively remove legacy, unused, orphan code, and models. Do not leave dead code in the codebase.
   2. **Refactoring Policy**: Do not prioritize legacy structure or backward compatibility during refactoring. Embrace breaking changes to maximize impact and improvement.
   3. **Network Assumption**: Do not consider environments without internet access; assume connectivity is available.
   4. **Quality Assurance**: Upon task completion, run `ruff` and `ty` for formatting and type checking. Never use `type: ignore` (or `ty: ignore`) without explicit user approval.
   5. **No Meta-Comments**: Do not add comments about user requests or conversation history (e.g., "Reflecting user requirements..."). Comments must focus strictly on technical context and code logic.
   6. **Enforcement**: If you encounter code that violates these conventions, **do not ignore it**; you must fix it to align with the standards.

## Responsibility & Layering
1. Each module/class should have **one reason to change** and a narrow public surface.
2. Keep a clear layering boundary:
   - **API surface**: user-facing clients, convenience helpers, stable exports.
   - **Domain contracts**: typed models/enums + pure transformations (no network, no filesystem).
   - **Transport**: request building, sending, retries/timeouts, response decoding (no domain-specific business rules).
   - **Tooling**: docs/spec ingestion and code generation (build-time only; never required at runtime).
3. Avoid bidirectional dependencies between layers; depend “downwards” only.

## Typing & Data Contracts
1. **Modeling & Typing Strategy**
   1. **Prioritize Modeling**: When data can be structured, modeled, or formalized, prioritize modeling to ensure type safety and reduce bugs. Minimize passing raw `dict`/`mapping` structures.
   2. **Modeling Tooling**:
      - **Pydantic**: Use for **Public API** (request/response modeling), validation, and serialization.
      - **dataclass**: Use for **Internal System** logic and complex type parameters.
      - **TypedDict**: Use sparingly for **Public API** input options where convenience is paramount.
   3. **Strict Typing**: Prefer strict typing end-to-end. Avoid `Any`, `object`, `dict`, and `Mapping` when the shape is known.
2. **Implementation Patterns**
   1. **Class Structure**: Define instance variables with type annotations in the class body and ensure all of them are initialized in `__init__`.
      ```python
      class MyClass:
          name: str
          _private: int | None
          def __init__(self, name: str):
              self.name = name
              self._private = None
      ```
   2. **Enforce `slots=True` (or `__slots__`)** for predictable data models to optimize memory and prevent attribute sprawl.
   3. **Boundary Conversion**: Convert boundary payloads (JSON/dicts) into typed models early; do not leak raw payloads across layers.
   4. **Compatibility**: Be forward-compatible with external APIs: prefer explicit aliases and tolerate unknown fields (e.g., `extra="ignore"` in models).
3. **Domain Types**
   1. **Time Values**: use timezone-aware `datetime` (UTC) in the public surface and serialize as ISO 8601 strings.
   2. **Financial Values**: (prices, amounts, fees, P/L, rates): **always use `Decimal`** in public data contracts (never `float`).

## Public API Design
1. Public surface should be discoverable and minimal; add convenience shortcuts sparingly.
2. Avoid side effects at import time (network calls, reading secrets, global singletons).
3. Keep `__init__` exports intentional; do not re-export large dependency graphs by default.

## Async / Sync Strategy
1. **Async Default**: The primary implementation is **async**. Sync clients must be prefixed with `Sync` (e.g. `SyncClient`).
2. **Automated Generation**: Use `unasync` to generate synchronous wrappers automatically.
3. **Directory Structure**: Separate implementations into `/_async` (source) and `/_sync` (generated).
4. **Immutable Sync Code**: **Never manually edit sync code**. All logic resides in async source; sync code is a build artifact.
5. Never block the event loop; do not use blocking I/O inside async code paths.
6. Resource lifecycle must be explicit (`close()` / `aclose()`); avoid GC-based cleanup.

## Transport, Errors, and Retries
1. Always set timeouts and provide actionable errors. Never swallow exceptions silently.
2. Raise SDK-specific exception types that preserve root cause and include context (endpoint, request id, etc.).
3. Retries/backoff must be opt-in and conservative; never retry non-idempotent operations by default.

## Code Generation & Automation
1. Generated files must be deterministic and reproducible; **do not hand-edit generated code**.
2. Keep templates small and composable; keep naming/normalization logic in handwritten layers.
3. When the contract changes (field names/types/defaults), update tests and snapshots to match the new typed schema.

## Override Approval
1. Overrides are **never** applied automatically; they require explicit approval before updating `docs/overrides/type_overrides.yaml`.
2. Use the list format and include approval metadata on each entry:
   ```yaml
   overrides:
     - id: "<endpoint-uuid>"
       changes: { ... }
       approved_by: "<reviewer>"
       approved_at: "YYYY-MM-DD"
       reason: "<why override is needed>"
       evidence: "<report path or payload sample>"
   ```
3. Until approved, keep candidates out of `type_overrides.yaml` (record them in review notes or a separate draft file).
4. After approval, rerun the full codegen pipeline and pytest, and confirm `tmp/docs/reports/smoke.json` has zero errors.

## Testing
1. Unit tests: fast, isolated, deterministic (fixed timestamps, explicit payloads).
2. Integration tests: can exercise multiple layers but must not hit real external services by default; use stubs/fixtures.
3. Tests should assert public behavior (SDK outputs/exceptions), not internal implementation details.

## Security & Secrets
1. Never commit secrets/tokens. Load credentials from environment variables or local secret files excluded from VCS.
2. Scrub secrets from logs and exception messages.

## Git Workflow & Contribution
1. **Important**: Create branches, commits, or PRs **only upon explicit user request**. Implicit actions are not allowed.
2. **Branch Naming**: Use prefixes like `feature/`, `fix/`, `chore/` (e.g., `feature/add-login`).
3. **Commit Messages**: Follow [Conventional Commits](https://www.conventionalcommits.org/).
   - Format: `<type>(<scope>): <description>`
   - Types: `feat`, `fix`, `docs`, `refactor`, `chore`, `test`
   - Example: `feat(api): add auth endpoint`
4. **Workflow**:
   ```bash
   git checkout -b feature/add-login
   git commit -m "feat(api): add auth endpoint"
   # Only on explicit request:
   git push -u origin feature/add-login
   gh pr create --title "feat(api): add auth" --body "..."
   ```
5. **Best Practices**: Commit often in small units. Do not commit directly to `main`. Always check `git diff` before pushing.
