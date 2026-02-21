---
status: accepted
date: 2026-01-27
---

# ADR-008: Endpoint-Integrated Object-Based Response Validators

## Context

KIS API는 HTTP 200에 `rt_cd=0`이어도 무효한 payload를 반환하는 경우가 있다 (sentinel 값, 필드 누락). 기존 대응은 nullable override로 무효 응답을 silent하게 수용하는 방식이었으나, 사용자에게 원인 불명의 `None`을 노출하는 문제가 있었다.

## Decision

**Endpoint 정의에 validator를 직접 통합**하고, **object-based rules**로 검증한다.

### 폐기된 대안

| 접근 | 이유 |
|------|------|
| 별도 validator registry | lookup 복잡도, endpoint과 분리된 관리 |
| 함수 기반 validator | 템플릿 렌더링 복잡, 디버깅 어려움 |
| 자동 적용 (휴리스틱) | 오탐 위험, 사용자 제어 불가 |

### 채택된 접근

- Validator rules를 `dataclass(frozen=True, slots=True)` 객체로 정의
- `Endpoint.validators: tuple[ValidatorRule, ...]`에 직접 포함
- `evaluate_validators()`가 객체를 해석하여 검증 실행
- 규칙은 `type_overrides.yaml`에서만 로드 (HITL 승인 필수)

### 코드젠 통합

```
Codegen Discovery (휴리스틱)
  → validation_hints.json (후보)
  → Human Review
  → type_overrides.yaml (명시적 등록)
  → Generate (객체 생성 코드)
  → Runtime (결정적 검증)
```

### Runtime Flow

```
HTTP Response → Raw JSON → evaluate_validators() → [pass] → Pydantic parse
                                                  → [fail] → SDK Error
```

## Consequences

- Validator가 endpoint과 함께 관리되어 추적성 우수
- Object-based라 함수 템플릿 불필요, 조합/직렬화/디버깅 용이
- 자동 적용 없음 — 모든 규칙은 HITL 승인 후 등록 (ADR-006)
- 새 규칙 타입 추가 시 Rule 클래스만 추가하면 됨
- Discovery 휴리스틱은 코드젠에서만, runtime은 명시적 필드 목록만 사용
