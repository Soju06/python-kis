---
status: accepted
date: 2026-01-16
---

# ADR-011: SDK Error Model Contracts

## Context

SDK 사용자에게 명확하고 디버깅 가능한 에러를 제공해야 한다. KIS API는 다양한 에러 형태를 반환하며, SDK 내부에서도 인증/전송/파싱 에러가 발생할 수 있다.

## Decision

pykis 전용 에러 계층 구조를 정의한다.

```
PykisError (base)
└── KisApiError
    ├── KisAuthError               # 인증/토큰 오류
    ├── KisRateLimitError          # Rate limit (429)
    ├── KisTransportError          # 네트워크/전송 오류
    ├── KisHttpError               # Non-OK HTTP 응답
    ├── KisResponseError           # rt_cd 체크 실패
    │   ├── KisResponseUnavailableError  # 데이터 미제공
    │   ├── KisResponseSentinelError     # Sentinel 값 감지
    │   ├── KisResponseIncompleteError   # 필드 누락
    │   └── KisInvalidResponseError      # 기타 무효 응답
    └── KisUnsupportedEndpointError  # 도메인 미지원
```

필수 context 필드: `endpoint_id`, `domain`, `request_id`, `method`, `path`.

## Consequences

- 사용자가 에러 타입으로 catch/handle 가능
- context 필드로 디버깅 가능
- rate limit/retry는 transport에서 처리 (ADR-003)
- response validation 에러는 KisResponseError 하위로 통합 (ADR-008)
