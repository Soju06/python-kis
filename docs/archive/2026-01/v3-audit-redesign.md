# python-kis v3 설계 메모 (v2 Audit + v3 Redesign)

작성일: 2026-01-07 (업데이트: 2026-01-15)

이 문서는 `python-kis-v2`의 구조를 분석하고, v3에서 **“설치 즉시 직관적으로 사용하는 SDK”**를 목표로 한 재설계 방향을 정리한다.
분석 대상은 v2 소스와 위키 문서이며, v3에서는 문서 기반 자동 생성과 표준화 레이어가 핵심이다.

## 0) 2026-01-15 현재 구현 스냅샷

- **Docs Ingestion**: `docsgen`이 포털 문서를 수집해 `docs/kis/**`에 저장 (API/오류코드/FAQ/종목정보파일).
- **API Codegen**: `scan → normalize → augment → infer → generate → validate → smoke` 파이프라인이 동작하며, 결과는 `src/pykis/api/raw/**`와 `tmp/docs/**`로 산출.
- **Raw Runtime**: `KisRawClient`/`SyncKisRawClient` + `Endpoint.call/acall` 기반의 타입 안전 Raw 호출이 구현됨.
- **Store Codegen**: `docs/kis/종목정보파일` 기반 raw structs/registry 생성 + 타입 추론/검증 리포트 (`tmp/store_codegen`).
- **Store Runtime**: 마스터 파일 스냅샷 다운로드/SQLite 적재/인덱싱 + `MasterStore` 조회 API 구현.
- **미구현**: 도메인 API(고수준 클라이언트), 표준화 모델/네이밍 레이어, 이벤트/스트리밍, v2 compat.

## 1) v2 핵심 구조 요약 (추론)

```
PyKis (pykis/kis.py)
 ├─ auth: KisAuth / KisKey / KisAccountNumber
 ├─ http: request()/fetch() -> KisObject.transform_
 ├─ cache/rate/thread: KisCacheStorage, RateLimiter, thread_safe
 ├─ scope: account() -> KisAccountScope, stock() -> KisStockScope
 │   ├─ mixins/adapters -> api/* 함수 바인딩
 └─ websocket: KisWebsocketClient
     ├─ event: KisEventHandler/KisEventTicket
     └─ GC 참조카운터: ReferenceStore/ReferenceTicket

Data 모델 계층
 ├─ KisDynamic + KisType 계열
 └─ API 응답: KisResponse/KisAPIResponse/KisPaginationAPIResponse
```

## 2) User Journey (import → 주문)

```python
from pykis import PyKis

# 1) 인증/세션
kis = PyKis("secret.json", keep_token=True)

# 2) 종목 스코프
stock = kis.stock("005930")
quote = stock.quote()

# 3-A) 종목 스코프 기반 주문
order = stock.buy(price=70000, qty=1)

# 3-B) 계좌 스코프 기반 주문
account = kis.account()
order2 = account.buy(
    market=stock.market,
    symbol=stock.symbol,
    price=70000,
    qty=1,
)
```

## 3) “불필요하게 복잡하다” Top 5

1. `pykis/responses/dynamic.py`  
   - Pydantic이 이미 해결하는 모델 변환/검증/필드 매핑을 자체 구현.
2. `pykis/responses/types.py`  
   - 타입 변환 규칙이 분산되어 유지보수 비용이 큼.
3. `pykis/client/websocket.py`  
   - 연결/복구/구독/암호화/이벤트가 단일 클래스에 결합.
4. `pykis/event/handler.py` + `pykis/utils/reference.py`  
   - GC 기반 해지 방식이 비결정적이고 디버깅 난이도 증가.
5. `pykis/kis.py` (+ rate/thread utils)  
   - 요청/토큰/레이트리밋/락이 커스텀 구현이라 수정 비용 큼.

## 4) 데이터 모델 확장성 문제 (기여자 입장)

```python
class KisDomesticQuote(KisQuoteBase, KisAPIResponse):
    price: Decimal = KisDecimal["stck_prpr"]
    indicator: KisDomesticIndicator = KisTransform(
        lambda x: KisObject.transform_(x, KisDomesticIndicator, ignore_missing=True)
    )()

class KisDomesticIndicator(KisDynamic):
    eps: Decimal = KisDecimal["eps"]
```

- 신규 API 추가 시 다음을 모두 이해해야 한다:
  - KisDynamic/KisType 규칙
  - __path__/scope/transform 규칙
  - API 함수 작성과 mixin 바인딩
  - 내보내기 및 문서화
- 결과적으로 “라이브러리 내부 프레임워크” 학습 비용이 커서 기여 장벽이 높다.

## 5) DX 및 Naming 평가

- 장점: `kis.stock().quote()` 같은 기본 경로는 직관적.
- 단점: 조건/체결/시장 값이 코드 기반이며 내부 맵핑 이해 필요.
- mixin 분산 구조로 메서드 정의 추적 비용이 큼.
- Naming은 표준화 의도는 좋지만 도메인 용어와 일치하지 않는 항목 존재:
  - 예: `orderable_amount` → `buying_power`, `market` → `exchange`

---

## 6) v3 아키텍처 (현 구현 + 업데이트된 방향)

### 6.1 Raw Data Layer (구현)

- Pydantic v2 기반 `RawModel` + KIS 전용 타입(`KisDate`, `KisTime`, `KisDateTime`, `KisBool`) 사용.
- Layer 0 enum은 `KisStrEnum`만 사용하며 Literal/TypeAlias 편의 타입은 제공하지 않는다 (정확성/안정성 우선).
- 응답/출력 모델과 요청 TypedDict가 codegen으로 생성됨. (`src/pykis/api/raw/**`)
- `extra="ignore"` + alias 매핑으로 스펙 변경에 내성 확보.

### 6.2 Runtime Transport (구현)

- `KisRawClient`/`SyncKisRawClient`가 인증/해시키/레이트리밋/재시도/에러 컨텍스트를 관리.
- `Endpoint.call/acall()`로 타입 안정 Raw 호출 제공.

### 6.3 Spec → Codegen 자동화 (구현)

- `docsgen`이 포털 문서를 수집해 `docs/kis/**`에 저장.
- `codegen/api/pipeline.py`가 `scan → normalize → augment → infer → generate → validate → smoke` 순서로 실행.
- 산출물: `src/pykis/api/raw/**`, 리포트 `tmp/docs/**`.
- API 모델 클래스명은 스펙 파일명 정규화 규칙과 동일한 방식으로 생성 (파일명과 1:1 대응).
- Override: `docs/overrides/{doc,type,augment}_overrides.yaml`.

### 6.4 Master Store (구현)

- `docs/kis/종목정보파일` 기반으로 `pykis/store/raw/structs`와 `SOURCE_DEFS` 생성.
- Store raw structs도 enum은 `KisStrEnum`만 제공하며 Literal 기반 편의 타입은 생성하지 않는다.
- 스냅샷/SQLite 적재/인덱싱 파이프라인 제공 (`pykis/store/service`).
- 공개 API: `MasterStore` (async 원본 + unasync로 sync 생성).

### 6.5 Domain/Normalization Layer (미구현)

- 사용자 친화 API (`KisClient`/`KisAsyncClient`)와 도메인 모델/표준화 네이밍은 아직 없음.
- “표준화 레이어 + 편의 필드”는 다음 단계에서 설계/구현.

### 6.6 Event/Streaming (미구현)

- Websocket/stream 구독 API는 아직 설계/구현 전.
- Realtime도 Layer 0/1/2 아키텍처를 적용

---

## 7) 업데이트된 레이어링 전략

1) **Docs Ingestion (build-time)**  
   - `docsgen/*` → `docs/kis/**` (포털 기반, 온라인 전제)

2) **Spec Normalization + Codegen (build-time)**  
   - `codegen/api/*`, `codegen/store/*` → raw 모델 생성 + 리포트

3) **Raw Runtime**  
   - `pykis/api/raw` + `pykis/api/_async/_sync`  
   - `pykis/store/raw` + `pykis/store/_async/_sync`

4) **Service Layer**  
   - Store snapshot/SQLite 파이프라인 (`pykis/store/service`)

5) **Store Layering (to-do)**  
   - Layer 0: RawStore (raw models/structs + parsers)  
   - Layer 1: NormalizedStore (표준 필드명/형상)  
   - Layer 2: MasterStore — 국내+해외 통합 정규화/시스템 기본 반환  

6) **Domain Layer (to-do)**  
   - 사용자 친화 API, 정규화된 모델, 도메인 용어 통일
7) **Streaming Layering (to-do)**  
   - Layer 0: websocket transport + decrypt (raw는 명시적 Layer 0 경로로만 제공)  
   - Layer 1: 이벤트 정규화/표준 필드명  
   - Layer 2: 도메인 이벤트/파생 필드

운영 원칙:
- build-time 자동화, runtime은 생성된 아티팩트만 사용해 결정적 동작.
- override는 명시적이고 리뷰 가능한 형태로 관리.
- 기본 사용자 경로는 Layer 2/1이며, raw 접근은 명시적 Layer 0 경로로만 제공.
- 필요 시 Layer 2 응답에 raw payload를 첨부하는 debug/inspect 옵션을 제공하되 기본값은 off.

---

## 8) 최신 스택 (현 사용 기준)

- Python 3.13, `uv` 기반 환경
- Pydantic v2, httpx(+httpx-retries), aiopath
- 품질: `ruff`, `ty`, `pytest`
- Sync는 `unasync`로 자동 생성 (수동 수정 금지)

---

## 9) Async/Sync 분리 (현 상태)

- 원본 구현: `pykis/api/_async`, `pykis/store/_async`
- Sync 생성: `scripts/build_unasync.py` → `pykis/api/_sync`, `pykis/store/_sync`
- Sync 코드는 생성물이며 수동 수정 금지.

---

## 10) 마이그레이션/공개 API 전략 (업데이트)

- 현재 공개 가능 범위: Raw Client + Raw Models + MasterStore
- 목표 공개 API: `KisClient`/`KisAsyncClient` + 도메인 모델 (sync-first naming, async-first implementation)
- v2 호환 레이어는 아직 미설계 (필요 시 `compat.v2`로 최소 호환)

---

## 11) 결정 사항 (2026-01-16 확정)

1) **정규화 파이프라인**  
   - 입력: codegen으로 자동 생성된 Layer 0 raw 모델  
   - 방식: `codeagent`에 codex sdk 기반 AI agent를 구축하고 프롬프트로 Layer 1 모델/매핑 생성  
   - 출력: mapping 규칙(py/yaml/json)과 `Normalized*` 스키마 (빌드‑타임 산출물)  
   - 구현 위치: `codeagent`/`src/codegen` 확장

2) **Public entrypoint/naming**  
   - 기본 사용자 경로: `KisClient`(sync) / `KisAsyncClient`(async)  
   - 코드 구현은 async-first, sync는 unasync로 생성

3) **Store ingestion canonical path**  
   - sqlite snapshot 파이프라인을 기본으로 사용  
   - 백엔드 스위칭으로 in-memory 구조도 호환  
   - `MasterStore`는 RawStore 위에서 국내+해외 통합 정규화/시스템 레이어를 기본 반환

4) **Streaming lifecycle 정책**  
   - 구독 핸들은 명시적 해지(`aclose`) 중심, GC 기반 해지는 지양  
   - 잠재적 버그를 방지하는 안정적 설계를 우선  
   - 41 subscription 제한 상수는 `src/pykis/streaming/constants.py`에 정의 (Layer 0 제약)

5) **Error model layering**  
   - pykis 전용 에러 시스템으로 명확한 메시지와 디버깅 컨텍스트 제공  
   - rate limit/retry는 transport(http adaptor)에서 안정성 확보

---

## 다음 단계 (현실 기준 우선순위)

1) docsgen → codegen 전체 섹션 확장 (현재 일부 섹션만 타깃)  
2) 도메인 모델/네이밍 표준화 레이어 설계 및 최소 API 도입  
3) 이벤트/스트리밍 설계 (웹소켓 스펙 정리 후)  
4) Store Normalizer 확장 + 검색/조회 API 정리  
5) CI 게이트: ruff/ty/pytest + smoke 리포트 기준 확정
6) Public entrypoint/naming 문서화 및 정책 정합화  
7) Override 승인 정책 문서화 + 후보 기록 경로 합의
