# Development Roadmap

Phased delivery plan. (원본: `.cursor/plans/pykis-layered-refactor_d66a42e7.plan.md`)

## Phase Dependencies

```
Phase 0 (Analysis) ✅
    │
    ▼
Phase 1 (Layer 0: Raw)
    │
    ├──────────────────┐
    ▼                  ▼
Phase 2 (Layer 1)   Phase 4 (Streaming) ✅
    │                  │
    ▼                  │
Phase 3 (Layer 2) ◄────┘
    │
    ▼
Phase 5 (Client Entrypoint)
    │
    ▼
Phase 6 (Polish)
```

Phase 2와 Phase 4는 병렬 진행 가능. Phase 3은 Phase 2 완료 필수. Phase 5는 Phase 3, 4 완료 필수.

## Phase 0: Preparation & Analysis ✅

설계/분석 단계. 완료됨.

| Task | Status |
|------|--------|
| Import graph 분석 | ✅ |
| Store 모듈 인벤토리 | ✅ |
| Canonical namespace 결정 (`pykis.api.raw`) | ✅ |
| L1/L2 스키마 계약 정의 | ✅ |
| Normalized Instrument 계약 | ✅ |
| Error 시스템 계약 | ✅ |
| Public entrypoint 네이밍 | ✅ |

## Phase 1: Layer 0 — Raw Infrastructure

Raw 계층 통합 및 codegen 타겟 정리.

| Task | Description | Status |
|------|-------------|--------|
| Raw 패키지 통합 | `pykis.api` + `pykis.raw` → `pykis.api.raw` | Pending |
| Generated/Hand-written 분리 | `pykis.api.raw/generated/` vs runtime | Pending |
| API Codegen 템플릿 업데이트 | 출력 경로 변경 | Pending |
| Store generated 분리 | `pykis.store.raw.generated/` | Pending |
| Store Codegen 업데이트 | 출력 경로 변경 | Pending |
| unasync 경로 업데이트 | `scripts/build_unasync.py` | Pending |
| RawClient 리팩터 | namespace 이동 | Pending |
| Shadow 패키지 제거 | 중복 삭제 | Pending |

## Phase 2: Layer 1 — Normalization

국내/해외 형상 통합, 표준 영어 필드명 정규화.

| Task | Description | Status |
|------|-------------|--------|
| Normalize 패키지 생성 | `pykis.normalize/` | Pending |
| Mapping registry 구현 | yaml/py 매핑 레지스트리 | Pending |
| Codeagent 파이프라인 셋업 | codex SDK 기반 | Pending |
| Codeagent 프롬프트 정의 | L0→L1 변환용 템플릿 | Pending |
| Runtime normalizer 구현 | 결정적 매핑 적용 | Pending |
| 국내/해외 통합 검증 | fixture payload 검증 | Pending |
| Store normalize 마이그레이션 | translate → normalize | Pending |
| Store mapping 자동 생성 | codeagent 활용 | Pending |

## Phase 3: Layer 2 — System Layer

단일 형상 + 데이터 품질 향상 + 도메인 객체 API.

| Task | Description | Status |
|------|-------------|--------|
| System 패키지 생성 | `pykis.system/` | Pending |
| Decimal/UTC 적용 | L2 금융/시간 필드 | Pending |
| Multi-endpoint merge 로직 | 응답 병합 | Pending |
| Computed fields 구현 | 수익률, 변동률 | Pending |
| Stock 도메인 객체 | symbol 검증, quote/order 바인딩 | Pending |
| Account 도메인 객체 | 계좌 정보, 잔고, 주문 | Pending |
| Portfolio 도메인 객체 | 포지션 집계, 자산 배분 | Pending |
| MasterStore L2 연동 | symbol/name/isin lookup | Pending |
| MasterStore 기본 출력 변경 | normalized/system 기본 | Pending |

## Phase 4: Streaming ✅

Async-first 스트리밍 완료.

| Task | Status |
|------|--------|
| Streaming 패키지 생성 | ✅ |
| WebSocket transport | ✅ |
| Market timezone mapping | ✅ |
| Override candidate logging | ✅ |
| SessionPool 구현 | ✅ |
| SubscriptionRegistry 구현 | ✅ |
| EventRouter 구현 | ✅ |
| Bounded StreamQueue | ✅ |
| Streaming L1 normalizer | ✅ |
| Streaming L2 system events | ✅ |
| Reconnect/Resubscribe | ✅ |
| Streaming sync facade (unasync) | ✅ |

## Phase 5: Client Entrypoint

통합 클라이언트 API, 선택적 서브시스템, 명시적 라이프사이클.

| Task | Description | Status |
|------|-------------|--------|
| KisAsyncClient 구현 | API + system 통합 | Pending |
| Streaming 선택적 활성화 | `enable_streaming` flag | Pending |
| Store 선택적 활성화 | `enable_store` flag | Pending |
| 명시적 라이프사이클 | `aclose()`/`close()` | Pending |
| Convenience factories | `client.stock()`, `client.account()` | Pending |
| Immutable 응답 객체 | `frozen=True` | Pending |
| GC 친화적 설계 | WeakValueDictionary | Pending |
| KisClient sync facade | unasync 생성 | Pending |

## Phase 6: Polish, Tests & Documentation

Access tiers 적용, 문서화, CI 자동화.

| Task | Description | Status |
|------|-------------|--------|
| Public exports 정리 | `__init__.py` access tiers | Pending |
| Boundary tests | upward import 금지 검증 | Pending |
| Layer 문서화 | L0/L1/L2 usage guide | Pending |
| Store 문서화 | access tiers 안내 | Pending |
| Override 정책 문서화 | ✅ (`specs/governance/override-policy.md`) |
| CI gates 설정 | ruff/ty/pytest + smoke | Pending |
| Test snapshot 갱신 | 새 스키마 구조 반영 | Pending |
