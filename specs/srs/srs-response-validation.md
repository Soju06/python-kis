# SRS: Response Validation Requirements

KIS API 응답 검증 시스템 요구사항. (원본: `docs/prd/kis-response-validator-prd.md`)

## Problem Statement

KIS API는 HTTP 200과 `rt_cd`/`msg_cd`가 정상이어도 실제로는 무효한 payload를 반환하는 경우가 있다:
- 필수 필드에 빈 문자열, `"0"`, `"0.0"`, `"00000000"` 등 sentinel 값
- 일부 필드 키 자체가 누락
- output 배열이 비어 있거나 모든 row가 sentinel

현재 SDK는 이런 경우 nullable 처리로 무효 응답을 silent하게 전달하여 사용자에게 원인 불명의 `None` 값을 노출한다.

## Requirements

### Functional

SyRS-V001: The SDK shall support per-endpoint response validation rules defined in `data/overrides/type_overrides.yaml`.
- Traces to: SR-D003
- Constraint: Rules are object-based (dataclass), not function-based
- Verification: Validator rule loading test

SyRS-V002: The SDK shall detect sentinel values (empty string, zero, zero-time/date) for fields declared as meaningful.
- Traces to: SR-D003
- Rule types: `AllFieldsSentinel`, `AnyFieldSentinel`
- Constraint: 명시적 필드 목록만 검사, 휴리스틱 없음 (runtime)
- Verification: Sentinel payload test

SyRS-V003: The SDK shall detect missing required fields (absent keys) in API responses.
- Traces to: SR-D003
- Rule types: `AllFieldsMissing`, `AnyFieldMissing`
- Verification: Missing field payload test

SyRS-V004: The SDK shall detect empty or absent output arrays when output is expected.
- Traces to: SR-D003
- Rule type: `OutputRequired`
- Verification: Empty output test

SyRS-V005: The SDK shall raise SDK-specific exceptions (`KisResponseUnavailableError`, `KisResponseSentinelError`) with endpoint context when validation fails.
- Traces to: SR-D003
- Context fields: `endpoint_id`, `domain`, `error_code`, `message`, `user_message`, `hint`
- Verification: Exception fields test

SyRS-V006: The SDK shall support configurable validation modes: `raise` (default), `warn`, `ignore`.
- Traces to: SR-D003
- Constraint: Client config flag `response_validation`
- Verification: Mode switching test

### Non-Functional

SyRS-V007: Validation rules shall be deterministically generated from YAML at build-time, with no runtime I/O.
- Traces to: SR-C001
- Verification: Pipeline re-run produces identical validators

SyRS-V008: Validation shall execute before raw model parsing for strict correctness.
- Traces to: SR-D003
- Verification: Validation runs on raw JSON before Pydantic parse

## Rule Types (Runtime)

| Type | Class | Trigger |
|------|-------|---------|
| `output_required` | `OutputRequired` | output 없거나 빈 배열 |
| `all_fields_sentinel` | `AllFieldsSentinel` | 명시된 모든 필드가 sentinel |
| `any_field_sentinel` | `AnyFieldSentinel` | 하나라도 sentinel |
| `all_fields_missing` | `AllFieldsMissing` | 모든 필드 키 없음 |
| `any_field_missing` | `AnyFieldMissing` | 하나라도 키 없음 |

## Scope Options

| Scope | Description |
|-------|-------------|
| `first_row` | 첫 번째 row만 검사 |
| `all_rows` | 모든 row가 조건 충족 시 invalid |

## Error Hierarchy

```
PykisError
└── KisApiError
    └── KisResponseError
        ├── KisResponseUnavailableError   # 알려진 "데이터 미제공" 케이스
        ├── KisResponseSentinelError      # Sentinel 값 감지
        ├── KisResponseIncompleteError    # 필드 누락
        └── KisInvalidResponseError       # 기타 무효 응답
```

## Discovery vs Runtime 분리

| Stage | Uses | Purpose |
|-------|------|---------|
| Codegen Discovery | thresholds, min_ratio | 후보 필드 자동 탐지 |
| Human Review | validation_hints.json | 후보 필드 검토/승인 |
| type_overrides.yaml | 명시적 필드 목록 | 승인된 필드만 등록 |
| Runtime Validator | 명시적 필드 목록 | 정확히 명시된 필드만 검사 |

## YAML Schema

```yaml
# data/overrides/type_overrides.yaml
overrides:
  - id: "<endpoint-uuid>"
    changes:
      validator:
        rules:
          - id: <rule_id>
            type: all_fields_sentinel
            output: output
            scope: first_row
            fields: [field1, field2, ...]
            sentinel_values: ["", "0", "0.0"]
            error:
              code: KIS_RESPONSE_UNAVAILABLE
              message: "..."
              user_message: "..."
              hint: "..."
              exception: KisResponseUnavailableError
```

## Migration Priority

| Priority | Endpoints | Pattern |
|----------|-----------|---------|
| P0 | `e27baf2f` (inquire_investor) | Sentinel masking |
| P1 | `a87c0275`, `1d150774`, `5613b629` | 888888 sentinel time |
| P2 | `77de2a74`, `86194480` | KOSPI200 conditional fields |
| P3 | 기타 `required: false` 항목들 | 점진적 전환 |
