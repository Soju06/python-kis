---
status: accepted
date: 2026-01-16
---

# ADR-009: Normalization Pipeline (Codeagent + Codex SDK)

## Context

국내/해외 API의 형상(필드명, 구조)이 크게 달라 SDK 사용자가 통합된 인터페이스를 사용하기 어렵다. 수동 매핑은 유지보수 비용이 높다.

## Decision

- **입력**: codegen으로 자동 생성된 Layer 0 raw 모델
- **방식**: codeagent에 codex SDK 기반 AI agent를 구축하고 프롬프트로 Layer 1 모델/매핑 생성
- **출력**: mapping 규칙 (py/yaml/json) + `Normalized*` 스키마 (빌드타임 산출물)
- **구현 위치**: `src/codeagent/` 패키지 (codegen 확장)

## Consequences

- 빌드타임에만 AI 사용, 런타임은 결정적 매핑만 수행
- 매핑 규칙은 versioned, reproducible
- Store의 `translate` 계층도 동일 매핑 정책으로 정렬
