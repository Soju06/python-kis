# python-kis v3 설계 메모 (v2 Audit + v3 Redesign)

작성일: 2026-01-07

이 문서는 `python-kis-v2`의 구조를 분석하고, v3에서 **“설치 즉시 직관적으로 사용하는 SDK”**를 목표로 한 재설계 방향을 정리한다.
분석 대상은 v2 소스와 위키 문서이며, v3에서는 문서 기반 자동 생성과 표준화 레이어가 핵심이다.

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

## 6) v3 아키텍처 제안 (핵심 방향)

### 6.1 Data Layer: Pydantic v2 기반 모델

- `Field(alias=...)`로 매핑하고, `@computed_field`로 편의 필드를 제공.
- `extra="ignore"` 기본으로 스펙 변화에 강하게 설계.

```python
from pydantic import BaseModel, Field, ConfigDict, computed_field
from decimal import Decimal

class Quote(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")
    price: Decimal = Field(alias="stck_prpr")
    change: Decimal = Field(alias="prdy_vrss")

    @computed_field
    @property
    def rate(self) -> Decimal:
        return self.change / self.price * 100
```

### 6.2 Interface: 계층적 + 짧은 호출

- 메인: `kis.domestic.stock.quote("005930")`
- 보조: `kis.stock("005930").quote()` shortcut 유지
- 주문: `kis.account().orders.buy(symbol="005930", qty=1, price=70000, exchange="KRX")`

### 6.3 Event System: 단순 구독 모델

- GC 해지 제거. 명시적 `Subscription` + `close()`/`aclose()` 제공.
- Async Generator 우선, Sync는 브리지 제공.

```python
async with kis.streams.price.subscribe("005930") as stream:
    async for tick in stream:
        ...

for tick in kis.streams.price.iter("005930"):
    ...
```

### 6.4 AI Automation: 스키마 기반 자동 생성

```
JSON/Excel Spec → Normalizer → Pydantic Model + Endpoint Stub 생성
→ 타입체크(mypy) → 테스트/스냅샷 → 패키징
```

- 자동 생성 결과는 `kis/_generated/*`에 두고, 수동 수정은 `kis/overrides/*`로 분리.
- 스펙 변경 시 CI에서 재생성 + diff 검토.

---

## 7) v3 레이어링 전략 (문서 기반 + 완화 레이어)

### 7.1 계층 구분

1) **Spec Ingestion Layer**  
   - 문서/스키마를 구조화하여 “정규화된 API 스펙” 생성.

2) **Raw API Layer (자동 생성)**  
   - 요청/응답 타입 + 엔드포인트 정의만 포함하는 얇은 레이어.
   - 명시적 필드 매핑과 최소한의 변환.

3) **Normalization/AI Layer (표준화 레이어)**  
   - AI 기반 네이밍 제안 + 수동 승인 워크플로우.
   - 국내/해외 불일치 필드를 정규 스키마로 통합.
   - 편의 필드(수익률, 총액, 평가손익 등) 제공.

4) **pykis System Layer**  
   - 사용자-facing API, 캐시/스트림/세션 관리.
   - 국내/해외 공통 인터페이스와 직관적 경로 제공.

### 7.2 운영 원칙

- AI는 “런타임”이 아니라 “빌드 타임”에만 사용해 결정성을 확보.
- 표준화 매핑은 “명시적 registry”로 관리하고 리뷰 가능하게 유지.

---

## 8) 최신 스택 도입 방향

- Python 3.13 기준으로 설계  
- 패키징/환경: `uv` (빠른 설치/락)
- 품질 도구: `ruff`, `mypy`, `pytest`
- 타입 안정성 강화로 IDE 자동완성을 극대화

---

## 9) Async/Sync API 분리 + 오버헤드 최소화

### 9.1 기본 원칙

- Async가 “원본”이고 Sync는 브리지 방식으로 제공.
- 공통 로직은 `Endpoint`/`Transport` 계층으로 공유.

### 9.2 구조 예시

```
EndpointSpec (auto-generated)
  └─ BaseClient._call(endpoint, transport)
      ├─ SyncTransport (httpx.Client)
      └─ AsyncTransport (httpx.AsyncClient)
```

- Sync/Async를 같은 스펙에서 생성해 중복 코드 최소화.
- Websocket도 동일: Async 스트림 원본 + Sync wrapper 제공.

### 9.3 코드 오버헤드 축소 아이디어

- **단일 EndpointSpec**: 요청/응답 변환을 한 곳에 정의하고 Sync/Async 클라이언트가 이를 호출.
- **Transport 인터페이스 분리**: `send()`/`asend()`만 다르고 나머지는 동일 로직.
- **Sync는 Async 얇은 래퍼**: 블로킹 환경에서는 `anyio.from_thread`로 async 실행 (단, 이벤트 루프 중첩 방지).
- **Codegen 템플릿 공유**: 동일 템플릿에서 sync/async 두 파일 생성해 변경 비용 최소화.
- **Stream 처리 분리**: 스트리밍/웹소켓은 async 원본 유지, sync는 `iter()` 제공.

---

## 10) 마이그레이션 전략 (Breaking Changes)

- `PyKis` → `KisClient`/`KisAsyncClient`
- `KisDynamic/KisType` 제거, Pydantic 모델로 전환
- API 경로: `kis.stock().quote()` → `kis.domestic.stock.quote()`
- 이벤트: `websocket.on(...)` → `streams.*.subscribe(...)`
- Naming 정비: `market` → `exchange`, `orderable_amount` → `buying_power`

완화책:
- `kis.compat.v2` 모듈 제공 (deprecated warnings + 자동 라우팅)
- v2 객체 → v3 모델 변환 어댑터 제공

---

## 다음 단계

1) 스펙 자동화 파이프라인 설계 및 프로토타입  
2) Raw API 레이어 스켈레톤 생성  
3) 표준화/편의 필드 매핑 레지스트리 설계  
4) System Layer의 사용자 API 설계 초안
