---
name: realtime streaming spec
overview: Define a concrete, runnable plan to standardize streaming realtime parsing for domestic and overseas stocks, including L0 Decimal/UTC parsing, local-time business date inference, and override logging workflows.
todos:
  - id: rt-scope-inventory
    content: "[P0] Inventory target TRs (domestic/overseas realtime) and extract response field order from docs"
    status: completed
  - id: rt-time-policy
    content: "[P0] Specify business_date inference using local NTP-synced time and market timezone rules"
    status: completed
  - id: rt-fieldspec
    content: "[P1] Draft FieldSpec set per TR (field order, types, Decimal rules, datetime rules)"
    status: completed
  - id: rt-parse-context
    content: "[P1] Define StreamingParseContext contract and lifecycle for date/time inference"
    status: completed
  - id: rt-override-report
    content: "[P1] Design override candidate report format and logging hooks for edge cases"
    status: completed
  - id: rt-codegen-ready
    content: "[P2] Prepare codegen input schema (streaming spec + FieldSpec + rules) for implementation"
    status: completed
---

# Realtime Streaming Standardization Plan (Domestic + Overseas)

## Goals
- Standardize realtime event parsing for **domestic/overseas stocks** only.
- Enforce **Decimal + UTC parsing at Layer 0**.
- Handle **non-JSON delimited payloads** (`|` + `^`) deterministically.
- Provide **robust edge-case logging** and a **manual override workflow**.

## Scope
- **Domestic realtime TRs**: all `*.yaml` under [`/var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/docs/kis/국내주식/실시간시세`](file:///var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/docs/kis/국내주식/실시간시세)
- **Overseas realtime TRs**: all `*.yaml` under [`/var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/docs/kis/해외주식/실시간시세`](file:///var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/docs/kis/해외주식/실시간시세)

## Parsing Architecture (Layer 0 Only)
- **Frame split**:
  - JSON frames: subscription success/errors and AES key/iv.
  - delimited frames: `encrypted_flag|tr_id|count|payload`.
- **Payload split**: `payload` uses `^` as field delimiter, ordered by `response.body` in YAML.
- **Multi-row payloads**: `count` indicates how many rows; split in fixed-size chunks (`len(field_order)`).
- **Decrypt**: if `encrypted_flag == 1`, AES decrypt using key/iv from subscription response.

## Business Date & UTC Policy (Local-Time Based)
- **Core idea**: realtime frames are assumed to be **“today” in market timezone** unless explicit date fields exist.
- **Local time source**: **system clock (NTP-synced)** is the default reference.
  - Use a `TimeProvider` that reads local time; optionally capture a startup offset for observability.
- **Date inference rules**:
  1. If payload contains `*DATE` or `*YMD` fields → use that date.
  2. Else, derive **business_date** from local time in the **market timezone**.
  3. If inferred date changes (local midnight boundary), update business_date.
- **Timezone rules**:
  - Domestic: `Asia/Seoul`.
  - Overseas: map market code (from `tr_key` or payload symbol) to timezone (NY, HK, JP, CN, VN).
- **UTC output**:
  - Combine `business_date + time` (or `XYMD/XHMS`, `KYMD/KHMS`) to a timezone-aware `datetime`.
  - Convert to **UTC** before exposing in L0 models.

## Decimal Parsing Rules (L0)
- **Rule-first typing**:
  - `CODE/TYPE/SIGN/YN` → `str`.
  - Price, volume, amount, rate, diff → `Decimal`.
- **Heuristic fallback**:
  - Numeric-like values parse as `Decimal` when not covered by rule list.
  - Apply **ZDIV scaling** for overseas price fields (`Decimal(value) / 10**ZDIV`).
- **Edge-case logging**:
  - Any ambiguity or parsing failure emits a structured record:
    - `endpoint_uuid`, `tr_id`, `field`, `raw_value`, `rule`, `decision`, `confidence`.

## Override Workflow (No auto-apply)
- Candidate logs are collected into a report file (example path):
  - `/var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/tmp/docs/reports/streaming_type_candidates.json`
- **Manual approval only**:
  - Candidates are reviewed and then applied to `docs/overrides/type_overrides.yaml` **only after explicit approval**.

## Work Plan

### 1) Inventory and Field Order Extraction
- Extract TR list and `response.body` order from:
  - [`/var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/docs/kis/국내주식/실시간시세`](file:///var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/docs/kis/국내주식/실시간시세)
  - [`/var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/docs/kis/해외주식/실시간시세`](file:///var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/docs/kis/해외주식/실시간시세)
- Produce a TR inventory list with:
  - `endpoint_uuid`, `tr_id`, `field_count`, field order.
- Output:
  - [`/var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/tmp/docs/reports/streaming_tr_inventory.json`](file:///var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/tmp/docs/reports/streaming_tr_inventory.json)
- Notes:
  - Found duplicate field codes in overseas `HDFSASP0` (PBID3/PASK3/VBID3/VASK3/DBID3/DASK3 repeated).

### 2) Business Date Inference Policy
- Specify `TimeProvider` behavior:
  - Uses system time in market timezone.
  - Provides monotonic updates at midnight boundary.
- Define a rule matrix for:
  - Domestic TRs missing date fields.
  - Overseas TRs with `XYMD/XHMS` and `KYMD/KHMS` precedence.
- Output:
  - [`/var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/tmp/docs/reports/streaming_parse_context_spec.yaml`](file:///var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/tmp/docs/reports/streaming_parse_context_spec.yaml)
- Decisions:
  - **Local-time (NTP-synced) policy**: business_date defaults to `now_utc().astimezone(market_tz).date()` when payload lacks a date field.
  - **Explicit date wins**: BSOP_DATE / XYMD / KYMD / TYMD / DEBT_DATE override local inference.
  - **Clock regression**: keep last inferred date and emit anomaly log.
  - **YYMMDD policy**: infer century from local date in the field timezone (`year_policy: century_from_local`).

### 3) TR-level FieldSpec Draft (L0)
- For each TR:
  - Declare `field_order`.
  - Assign `field_type` (`Decimal`, `str`, `datetime`).
  - Specify `datetime_rule` (field pair + timezone).
  - Specify `decimal_rule` (ZDIV scaling or direct).
- Output format designed for codegen input (see “Codegen Readiness”).
- Output:
  - [`/var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/tmp/docs/reports/streaming_fieldspec_draft.yaml`](file:///var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/tmp/docs/reports/streaming_fieldspec_draft.yaml)
- Decisions:
  - Duplicate fields are preserved in order and **aliased by index** (suffix `_2`).
  - Overseas `ZDIV` is parsed as int; price fields with scale apply `Decimal(value) / 10**ZDIV`.
  - `XYMD/KYMD` length 6 uses `year_policy: century_from_local`.

### 4) StreamingParseContext Contract
- Define inputs:
  - `market_timezone`
  - `business_date` (optional but required for date-less payloads)
  - `time_provider`
  - `zdiv` (overseas price scaling)
- Define update rules:
  - Update `business_date` on explicit date field.
  - Otherwise use local date in market timezone.
- Output:
  - [`/var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/tmp/docs/reports/streaming_parse_context_spec.yaml`](file:///var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/tmp/docs/reports/streaming_parse_context_spec.yaml)

### 5) Override Candidate Report
- Define JSON schema for override candidates.
- Define log hooks for:
  - parsing errors
  - heuristic-only decisions
  - ZDIV anomalies
- Ensure report is deterministic and reproducible for review.
- Output:
  - [`/var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/tmp/docs/reports/streaming_override_report_schema.json`](file:///var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/tmp/docs/reports/streaming_override_report_schema.json)

### 6) Codegen Readiness
- Draft a unified “Streaming Spec” schema:
  - `endpoint_uuid`, `tr_id`, `field_order`, `field_types`, `datetime_rules`, `decimal_rules`, `market_timezone_hint`.
- Validate that the schema supports:
  - Domestic + overseas differences
  - Date inference
  - Edge-case overrides
- Output:
  - [`/var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/tmp/docs/reports/streaming_codegen_input_schema.yaml`](file:///var/folders/k3/zdqbl1mj297_19vj6rrb9ch00000gn/T/vibe-kanban/worktrees/daf3-/python-kis/tmp/docs/reports/streaming_codegen_input_schema.yaml)
