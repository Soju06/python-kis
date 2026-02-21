# python-kis Project Definition

## Overview

python-kis는 한국투자증권(KIS) Open API를 Python에서 사용하기 위한 SDK이다.
KIS API의 REST/WebSocket 인터페이스를 타입 안전하고 직관적인 Python API로 제공한다.

## Goals

1. **타입 안전한 API 제공**: KIS API의 모든 endpoint를 Pydantic 기반 타입 모델로 제공
2. **코드젠 기반 자동화**: API 문서에서 모델/endpoint를 자동 생성하여 유지보수 비용 최소화
3. **Async-first**: async 기본 구현, unasync로 sync 자동 생성
4. **국내/해외 통합**: 국내주식, 해외주식, 선물옵션, 채권을 단일 SDK로 통합

## Scope

### In-Scope

- KIS Open API REST 호출 (국내주식, 해외주식, 선물옵션, 장내채권)
- KIS WebSocket 실시간 스트리밍 (시세, 체결)
- OAuth 인증/토큰 관리
- 코드젠 파이프라인 (API 문서 → Raw 모델 자동 생성)
- 종목정보파일(마스터 데이터) 파싱/인덱싱

### Out-of-Scope

- 트레이딩 전략/알고리즘
- 백테스팅 엔진
- KIS 이외 증권사 API

## Architecture Summary

3-layer architecture (see `specs/architecture/layered-model.md`):

- **Layer 0 (Raw)**: 코드젠으로 생성된 Pydantic 모델, API 원형 보존
- **Layer 1 (Normalize)**: 국내/해외 형상 통합, 표준 영어 필드명 정규화
- **Layer 2 (System)**: 도메인 객체, Decimal/UTC 강제, 다중 API 병합

## Technology Stack

- Python 3.13+
- Pydantic (public API 모델링)
- httpx (async HTTP client)
- asyncio (async runtime)
- unasync (sync code generation)
- uv (package management)
- ruff (linting/formatting)
- ty (type checking)

## Standards

- ISO/IEC/IEEE 29148 경량 적용 (요구사항)
- IEEE 42010 / C4 경량 적용 (아키텍처)
- ADR (Architecture Decision Records)
