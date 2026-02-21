---
status: accepted
date: 2026-01-15
---

# ADR-002: Pydantic for Public API, dataclass for Internal

## Context

SDK에서 데이터 모델링에 사용할 도구를 선택해야 함. 외부 사용자에게는 validation과 serialization이 중요하고, 내부적으로는 경량 구조가 필요.

## Decision

- **Pydantic**: Public API (request/response 모델), validation, serialization
- **dataclass**: Internal system 로직, complex type parameters
- **TypedDict**: Public API input options (편의성이 중요한 경우)

## Consequences

- Public surface는 Pydantic 모델로 통일되어 IDE 지원/문서화 우수
- 내부 로직은 dataclass로 가벼움
- Generated raw models은 Pydantic 기반 (`extra="ignore"`, alias 지원)
