# VM-Stock-KIS vs 한국투자증권 공식 샘플(open-trading-api) 아키텍처 비교 보고서

**작성일**: 2026-08-27
**작성자**: Claude (software-architect 서브에이전트 3인 병렬 분석, model: fable 5)
**버전**: v1.0
**분석 대상**

- `/home/claude/github.com/vm-stock-kis` — `src/vmkis`, 78 py / 21,565 LOC
- `/home/claude/github.com/open-trading-api` — `koreainvestment/open-trading-api` 포크 (upstream 확인됨)

> **검증 원칙**: 본 보고서의 모든 수치와 구조 주장은 기존 문서를 인용하지 않고 **실제 소스 코드를 직접 읽어 검증**했습니다.
> 기존 문서(`docs/architecture/ARCHITECTURE.md`, `docs/reports/ARCHITECTURE_*_KR.md`)와 코드가 불일치하는 항목은 §11에 별도 정리했습니다.

---

## 1. 요약 (Executive Summary)

두 저장소는 **같은 API를 감싸지만 완전히 반대 방향의 설계 결정**을 내렸습니다.

| | **vm-stock-kis** | **open-trading-api (공식)** |
|---|---|---|
| 설계 목표 | 타입 안전한 **라이브러리** | 복붙 가능한 **레퍼런스 샘플** |
| 계층 수 | 8개 그룹 (허브-스포크) | **2개** (`kis_auth.py` + 함수 334개) |
| REST 엔드포인트 | **30 경로 / TR ID 74개** | **274 함수 / TR ID 377개** |
| 실시간(WS) 스트림 | **9 TR ID** (사용자 이벤트 3종) | **60 함수** |
| 시장 커버리지 | 국내주식 + 해외주식 9개 시장 **(현물만)** | 국내주식·해외주식·국내/해외 선물옵션·채권·ELW·ETF/ETN **전부** |
| 코드량 | 21,565 LOC | 39,008 LOC (examples_user 기준, 중복 포함) |
| 타입 | 전 객체 타입 힌트 + `Decimal`/`datetime` 정규화 | 전 파라미터 `str`, 반환 `DataFrame`(전 컬럼 object) |
| 오류 처리 | 예외 위계 12종 (`KisAPIError` 등) | 실패 시 **빈 DataFrame 반환**(예외 없음) |
| 멀티 계정/환경 | 실전+모의 **동시 인스턴스 가능** | 전역 상태 mutate로 **프로세스당 1계정 1환경** |
| 테스트 | 957개 (unit 897) | **0개** |
| 패키징 | pip 설치형 (`uv`+`hatchling`) | `sys.path.extend` 해킹, 설치 불가 |
| 미지원 API 호출 | `kis.fetch(api="TRID")` — **1급 escape hatch 존재** | `ka._url_fetch(url, tr_id, ...)` — 4~6줄 |

**핵심 결론 5줄**

1. **폭(breadth)은 공식 샘플의 압승** — 커버리지 격차가 REST 기준 **약 9배**(74 vs 377 TR ID). vm-stock-kis는 KIS OpenAPI 중 **주식 현물 도메인만** 구현했습니다.
2. **깊이(depth)·안전성은 vm-stock-kis의 압승** — 타입, 예외, 재연결 복구, 참조카운팅 구독 해지, 멀티환경 동시성은 공식 샘플에 **아예 없는 기능**입니다.
3. **vm-stock-kis의 계층 아키텍처는 문서가 주장하는 단방향 계층이 아닙니다.** 코드상 `client → api`, `responses → client`, `api → adapter`, `event → api` 역방향 의존이 실재하며(§4.3), 이것이 **신규 API 추가 비용을 250~800 LOC까지 끌어올리는 근본 원인**입니다(§10). 다만 *단방향이 아닌 것 자체가 결함인가*는 별도 판정이 필요하며, §5에서 다룹니다.
4. **단방향이 아닌 것 자체는 결함이 아닙니다** — 역방향 7건 중 3건(`responses→client`, `api↔adapter`, `api→scope`)은 rich domain object 설계의 필연이고, **반드시 고칠 것은 2건**(`client/websocket.py:19`, `utils/retry.py:14`)입니다. 진짜 문제는 순환을 끊는 지연 import 30곳에 **사유 주석이 0곳**이라는 것입니다 (§5).
5. **커버리지 격차는 손으로 메울 수 없고, codegen으로는 메울 수 있습니다** — 공식 샘플 벤더링은 **라이선스 부재(all rights reserved)로 기각**되지만, `examples_llm/`은 REST 274개 중 **271개(98.9%)가 AST 파싱되는 기계 판독 스펙**임을 실측으로 증명했습니다. 사실만 추출해 vmkis 네이티브 코드를 생성하는 전략이 유일한 현실적 경로입니다 (§13).

---

## 2. 비교 대상 확인

사용자가 지칭한 `../open-api-trading`은 실제 디렉토리 `../open-trading-api`(한국투자증권 공식 GitHub 샘플의 포크)입니다.

해당 저장소의 **공식** 구성요소와 **로컬 추가분**을 구분해 분석했습니다.

| 구분 | 디렉토리 | 내용 |
|---|---|---|
| 공식 | `examples_llm/` | API 1개 = 폴더 1개, 폴더당 2파일 (`<name>.py` + `chk_<name>.py`), 총 668 py |
| 공식 | `examples_user/` | 세그먼트별 통합본 4파일 세트 (최대 `domestic_stock_functions.py` **13,463줄 / 131함수**) |
| 공식 | `legacy/` | 구세대 샘플 (Python/C#/Delphi/VBA/Postman) |
| 공식 | `stocks_info/` | 종목마스터 정제 스크립트 16종 |
| 공식 | `llms.txt`, `docs/convention.md`, `kis_devlp.yaml` | LLM 내비게이션 인덱스, 공식 코딩 컨벤션, 설정 템플릿 |
| **로컬 추가** | `backtester/`, `strategy_builder/`, `MCP/` | 사용자가 붙인 백테스터·전략빌더·MCP 서버 (공식 아님) |

---

## 3. 소스 구조 상세

두 저장소의 소스를 **어디부터 읽어야 하는지** 기준으로 정리합니다. 이후 §4~§5의 계층 논의는 이 구조를 전제로 합니다.

### 3.1 vm-stock-kis — `src/vmkis` (78 py / 21,565 LOC)

```text
src/vmkis/
├── kis.py                    ★ 758줄. VmKis 파사드. 모든 것의 시작점
│                               · request()  :510  raw HTTP (appkey/토큰/리미터/재시도)
│                               · fetch()    :601  request + JSON + 타입 변환  ← 확장 진입점
│                               · token      :669  만료 10분 전 자동 재발급 (@thread_safe)
│                               · 클래스 본문 :756  stock/account/trading_hours 메서드 주입
├── __init__.py                 공개 표면 12개 + 구 경로 deprecation __getattr__
├── public_types.py             Quote/Balance/Order/Chart/Orderbook 등 8개 TypeAlias
├── types.py                    고급 사용자용 100개 re-export
├── __env__.py                  도메인 URL, WS 구독한도 40, Rate Limit(실전 19/s·모의 2/s)
├── simple.py / helpers.py      SimpleKIS(dict 반환), create_client, save_config_interactive
│
├── scope/                    ★ 조립 루트 (3파일) — "사용자가 손에 쥐는 객체"
│   ├── base.py                 KisScopeBase — kis 참조 보관만
│   ├── stock.py       :53-64   KisStockScope = Base + AccountProduct + Mixin 3종 + EventFilter
│   │                  :87      stock() 팩토리 — 생성 시 info() REST 조회 발생
│   └── account.py     :37-45   KisAccountScope 동일 패턴
│
├── adapter/                    기능 Mixin (7파일) — "Scope에 메서드를 붙이는 층"
│   ├── product/quote.py :161   class Mixin: from ...quote import product_quote as quote
│   ├── account/order.py :402   동일 바인딩 트릭
│   ├── account_product/        주문·정정·취소 (응답 객체가 상속하기도 함 → §4.3-d)
│   └── websocket/price.py      on()/once() 문자열 이벤트 디스패처 (331줄 중 ~280줄이 overload)
│
├── api/                      ★ 엔드포인트 + 응답 스키마 (24파일, 코드량 최대)
│   ├── base/                   KisMarketBase → KisProductBase → KisAccountProductBase
│   ├── auth/                   token_issue / token_revoke / websocket_approval_key
│   ├── stock/                  quote.py(761줄) chart 2종 order_book info trading_hours market
│   ├── account/                order.py(2,066줄) balance daily_order pending_order
│   │                           order_profit orderable_amount order_modify
│   └── websocket/__init__.py ★ WEBSOCKET_RESPONSES_MAP — TR ID → 응답 클래스 레지스트리
│                               (미등록 TR은 수신 이벤트가 조용히 drop됨)
│
├── client/                     통신 프리미티브 (10파일)
│   ├── websocket.py   ★ 593줄  KisWebsocketClient — 재접속·구독복원·AES keychain·모의 이중 클라이언트
│   ├── object.py      :65      kis_object_init — 모든 응답 객체에 kis를 지연 주입하는 핵심 훅
│   ├── auth.py appkey.py account.py   KisAuth / KisKey / KisAccountNumber(KisForm 구현)
│   ├── page.py        :47-58   KisPage — ctx_area_fk100/fk200 자동 감지 (그 외 형식은 미지원)
│   ├── form.py messaging.py cache.py exceptions.py(예외 12종)
│
├── responses/                ★ 동적 변환 엔진 (5파일)
│   ├── dynamic.py     :233    KisObject.transform_ — dir() 반사로 KisType 필드 순회
│   ├── types.py               KisString/KisInt/KisDecimal/KisBool/KisDate/KisAny 등 11종
│   ├── response.py    :69     KisResponse(rt_cd 검사) / :99 KisAPIResponse(__path__="output")
│   │                  :130    KisPaginationAPIResponse(page_status·next_page 자동)
│   └── websocket.py   :48     "^" 분할 + __fields__ 위치 기반 파싱 (REST와 별도 엔진)
│
├── event/                      pub-sub (5파일). KisEventHandler / KisEventTicket(GC 자동해지)
│   └── filters/                KisProductEventFilter(symbol+market), KisSubscriptionEventFilter(TR)
└── utils/                      RateLimiter, @thread_safe, ReferenceStore(구독 참조카운팅),
                                @kis_repr(489줄), timex/timezone/math/workspace
```

**읽는 순서 권장**: `kis.py`(fetch/request) → `api/stock/quote.py`(엔드포인트 표준 패턴) → `responses/dynamic.py`(변환 엔진) → `scope/stock.py` + `adapter/product/quote.py`(조립) → `client/websocket.py`(실시간).

**구조를 요약하는 한 문장**: *하나의 엔드포인트가 `api/`(스키마+호출) → `adapter/`(메서드 바인딩) → `scope/`(사용자 객체) 3곳에 흩어져 있고, 실행 시점에는 모두 `VmKis`로 되돌아온다.*

### 3.2 open-trading-api — 공식 샘플

```text
open-trading-api/
├── examples_llm/             ★ 정본. API 1개 = 폴더 1개, 폴더당 2파일 (668 py)
│   └── domestic_stock/
│       ├── inquire_price/
│       │   ├── inquire_price.py        한줄호출함수 (검증 → tr_id → params → fetch → DataFrame)
│       │   └── chk_inquire_price.py    체크함수 (ka.auth() → 호출 → COLUMN_MAPPING 한글화 → print)
│       ├── volume_rank/ fluctuation/ inquire_investor/ short_sale/ ... (156개 폴더)
│       └── ccnl_krx/ asking_price_krx/ ...                            (실시간 25개)
│
├── examples_user/              위 함수들을 세그먼트별 1파일로 물리적 연결 (중복본)
│   ├── kis_auth.py           ★ 799줄. 유일한 인프라 계층 (examples_llm/kis_auth.py와 완전 동일)
│   │                           :46-50   import 시 토큰파일 생성 + yaml 로드 (부수효과)
│   │                           :146,151 _smartSleep global 누락 버그
│   │                           :413-454 _url_fetch — 모든 REST의 단일 관문, T/J/C→V 자동 치환
│   │                           :461-799 KISWebSocket (asyncio) + 전역 open_map/data_map
│   └── domestic_stock/
│       ├── domestic_stock_functions.py      13,463줄 / 131함수
│       ├── domestic_stock_functions_ws.py    2,129줄 /  25함수
│       ├── domestic_stock_examples.py        import만 해도 전 API 즉시 실행
│       └── domestic_stock_examples_ws.py     kws.subscribe(...) 나열 후 kws.start()
│
├── legacy/                     구세대 샘플 (Python/C#/Delphi/VBA/Postman)
├── stocks_info/                종목마스터 정제 스크립트 16종
├── docs/convention.md          공식 컨벤션 112줄 ("1용어 1단어" 등 LLM 친화 규칙)
├── llms.txt                    LLM 내비게이션 인덱스 30줄
└── kis_devlp.yaml              설정 템플릿 (~/KIS/config/ 로 복사해야 동작)
   ※ backtester/ strategy_builder/ MCP/ 는 로컬 추가분 (공식 아님)
```

**읽는 순서 권장**: `llms.txt` → `docs/convention.md` → `examples_user/kis_auth.py`(전부가 여기에) → 필요한 `examples_llm/<세그먼트>/<API명>/`.

**구조를 요약하는 한 문장**: *하나의 엔드포인트가 정확히 한 폴더 안에 자기완결적으로 들어 있고, 공유되는 것은 `kis_auth.py` 하나뿐이다.*

### 3.3 구조가 만든 결과

| | vm-stock-kis | open-trading-api |
|---|---|---|
| 엔드포인트 1개의 물리적 위치 | **3~4개 디렉토리에 분산** | **1개 폴더에 자기완결** |
| 공유 인프라 | `kis.py` + `client/` + `responses/` (25파일) | `kis_auth.py` (1파일) |
| 한 API를 이해하는 데 읽을 파일 수 | 4~6개 | **1개** |
| 한 API를 수정할 때 건드릴 파일 수 | 4~6개 | 2개(llm) + 2개(user 중복본) |
| grep으로 "이 TR이 뭐하는지" 찾기 | TR ID → api/ 파일 → Protocol 추적 필요 | 폴더명이 곧 기능명 |
| 코드 재사용 | 높음 (변환·인증·페이징 공통화) | 없음 (전부 전개) |

> 이 표가 두 저장소의 성격을 압축합니다. 공식 샘플은 **읽기**에, vm-stock-kis는 **쓰기**에 최적화되어 있습니다.

---

## 4. 계층 아키텍처 비교

### 4.1 open-trading-api — 의도적으로 2계층

```text
┌───────────────────────────────────────────────────────────┐
│ L2: API 함수 334개 (한줄호출함수)                          │
│  inquire_price() / inquire_balance() / order_cash() ...    │
│  · 함수 간 수평 의존 0                                     │
│  · 각자 tr_id 분기 + params dict + DataFrame 변환을 반복    │
├───────────────────────────────────────────────────────────┤
│ L1: kis_auth.py (799줄) — 유일한 인프라                    │
│  설정 로드 / 토큰 / _url_fetch / APIResp / KISWebSocket    │
│  전역 가변 상태: _TRENV, _base_headers, open_map, data_map │
└───────────────────────────────────────────────────────────┘
                          ↓
                    KIS OpenAPI
```

- **도메인 모델 계층 없음**. 응답 스키마는 `chk_*.py`의 `COLUMN_MAPPING` dict와 WS 함수의 `columns` 리스트로만 존재합니다.
- 모든 L2 함수는 예외 없이 `ka._url_fetch()` 또는 `ka.data_fetch()` **단 한 지점**만 호출합니다.
- 이 단순함은 버그가 아니라 **의도된 설계**입니다. `docs/convention.md`는 "LLM이 혼란스럽지 않도록 1용어 1단어"까지 규정하고, `llms.txt`는 `examples_llm/`을 엔드포인트 구현의 정본으로 지정합니다.

### 4.2 vm-stock-kis — 8그룹 허브-스포크

문서의 다이어그램은 수직 6계층이지만, 코드에서 확인되는 실제 구조는 **`VmKis` 인스턴스를 허브로 한 방사형 + 함수 주입(method-injection) 조립**입니다.

```text
        ┌──────────────── scope/ (3) — 조립 루트 ─────────────────┐
        │  KisStockScope = KisScopeBase + KisAccountProductBase   │
        │                + 어댑터 Mixin 3종 + EventFilter          │
        │  MRO 14클래스 / 팩토리 stock()은 생성 시 REST 조회 수행   │
        └───────────────────────┬─────────────────────────────────┘
                                │ 6 edge
        ┌───────────────────────▼─────────────────────────────────┐
        │  adapter/ (7) — Protocol + Mixin 쌍                      │
        │  class KisQuotableProductMixin:                          │
        │      from vmkis.api.stock.quote import product_quote     │
        │                                    as quote   ← 바인딩 트릭│
        └───────────────────────┬─────────────────────────────────┘
                    55 edge     │        ▲ 6 edge (역방향!)
        ┌───────────────────────▼────────┴────────────────────────┐
        │  api/ (24, 코드량 최대) — 엔드포인트 + 응답 스키마         │
        │  Protocol → Repr → Base → 국내/해외 impl → 함수 3층       │
        │  api/stock/quote.py 761줄 / api/account/order.py 2,066줄 │
        └──┬──────────────┬──────────────┬────────────┬───────────┘
      18   │         47   │         43   │       12   │
    ┌──────▼─────┐ ┌──────▼──────┐ ┌─────▼────┐ ┌─────▼─────┐
    │  client/   │ │ responses/  │ │  utils/  │ │  event/   │
    │   (10)     │◄┤    (5)      │ │  (11)    │ │   (5)     │
    │ WS 엔진 593│4│ 동적 변환엔진 │ │RateLimit │ │ pub-sub   │
    └──────┬─────┘ └─────────────┘ └────┬─────┘ └─────┬─────┘
        2  │ (역방향! → api)          1 │(→client)  3 │(→api, 역방향!)
           └──────────────────────────────────────────┘

                    ┌─────────────────────────────┐
   전 계층이 self.kis│  VmKis (kis.py, 758줄)      │ fan-in: 36파일 / 29 import
   로 재진입 ───────►│  토큰·세션·RateLimit·캐시    │
                    │  ·WebSocket·request/fetch    │
                    └─────────────────────────────┘
```

**메서드 주입 패턴** — `VmKis`의 사용자 대면 메서드는 클래스 본문 끝의 import로 붙습니다:

```python
# src/vmkis/kis.py:756-758 (클래스 본문 내부)
from vmkis.api.stock.trading_hours import trading_hours
from vmkis.scope.account import account
from vmkis.scope.stock import stock
```

어댑터도 동일한 트릭을 씁니다:

```python
# src/vmkis/adapter/product/quote.py:161-164
class KisQuotableProductMixin:
    from vmkis.api.stock.daily_chart import product_daily_chart as daily_chart
    from vmkis.api.stock.day_chart import product_day_chart as day_chart
    from vmkis.api.stock.order_book import product_orderbook as orderbook
    from vmkis.api.stock.quote import product_quote as quote
```

### 4.3 의존성 방향 검증 — **단방향이 아님 (문서 주장 반증)**

AST로 전 파일 import를 런타임/TYPE_CHECKING으로 분류한 결과:

```text
정방향:  adapter → api: 55    api → responses: 47   api → utils: 43
         api → client: 18     api → event: 12       scope → adapter: 6
역방향:  api → adapter: 6     responses → client: 4  event → api: 3
         client → api: 2      event → client: 2      utils → client: 1
         api → scope: 1
```

**확인된 위반 (file:line, 직접 검증 완료)**

| # | 위반 | 위치 | 성격 |
|---|---|---|---|
| (a) | `client → api` | `src/vmkis/client/websocket.py:19`<br>`from vmkis.api.websocket import WEBSOCKET_RESPONSES_MAP` | **모듈 레벨**. 통신 계층이 상위 응답 스키마 레지스트리를 끌어옴 |
| (b) | `client → api` | `src/vmkis/client/messaging.py:52` (함수 내 지연 import) | 순환 회피용 |
| (c) | `responses → client` | `src/vmkis/responses/response.py:5-7`<br>`KisAPIError`, `KisObjectBase`, `KisPage` | **모듈 레벨**. 변환 계층이 통신 계층 타입에 결합 |
| (d) | `api → adapter` | `api/account/order.py:15,19`, `api/account/balance.py:6,10`, `api/account/pending_order.py:9,12` | **모듈 레벨**. 응답 객체가 Mixin을 상속(예: `KisOrder`가 정정/취소 가능해야 함) |
| (e) | `event → api` | `event/filters/product.py:3-4`, `event/filters/order.py:4-5` | 모듈 레벨 |
| (f) | `utils → client` | `utils/retry.py:14` | 유틸이 예외 타입에 결합 |
| (g) | `api → scope` | `api/base/product.py:93` (지연 import) | property 내부 |

**순환 봉합 기법 3종**: ① `VmKis` 클래스 본문 import, ② 함수/property 내부 지연 import, ③ Protocol 구조적 서브타이핑 + `TYPE_CHECKING` 문자열 어노테이션(`self: "VmKis"` — api 모듈 17개).

`import vmkis`는 정상 동작합니다. 즉 **로드 순서로는 순환이 깨져 있으나 논리적으로는 kis ↔ scope ↔ adapter ↔ api ↔ client ↔ responses가 서로를 알고 있는 상호결합 그래프**입니다.

> **판정**: vm-stock-kis는 "순수 계층 아키텍처"가 아니라 **"Protocol과 지연 import로 순환을 봉합한 허브-스포크 구조"**입니다. `ARCHITECTURE.md`의 `API → Client → Response Transform → Utility` 하향 단방향 다이어그램은 코드와 일치하지 않습니다.

### 4.4 계층 관점 정리

| 관점 | vm-stock-kis | open-trading-api |
|---|---|---|
| 계층 분리 | 8그룹으로 나뉘었으나 **경계가 새어 있음**(7건 역방향) | 2계층, 경계 위반 없음 (위반할 계층 자체가 없음) |
| 결합도 | `VmKis` 신 객체 fan-in 36파일 — 전 계층이 허브에 재진입 | `kis_auth` 모듈 전역에 전 함수가 결합 |
| 응집도 | 기능(quote/order/balance) 단위로 높음 | 파일 단위로 높음, 전체적으로는 복붙 중복 |
| 교체 가능성 | Protocol 기반이라 이론상 가능, 실제로는 `self.kis` 재진입으로 저해 | 없음 |
| **역설** | 계층이 많은 쪽이 오히려 순환에 시달림 | 계층이 없어서 순환도 없음 |

---

## 5. 단방향 의존이 아니어도 되는가 — 아키텍처 판정

**한 줄 결론: "단방향이 아니라는 것" 자체는 죄가 아니다. 죄는 두 가지다 — (1) 문서가 코드에 없는 단방향성을 주장하고 있다는 것, (2) 순환을 끊는 장치(지연 import 30곳, TYPE_CHECKING 35파일, 클래스 본문 import)가 어디에도 설명 없이 존재해서, 누구든 "정리"하는 순간 부서질 수 있다는 것.** 역방향 간선 7종 중 **2개는 반드시 수정**, **3개는 의도적 설계로 인정하고 문서화**, **2개는 저비용 정리 대상**입니다.

### 5.1 원칙 정리 — 계층 아키텍처가 실제로 요구하는 것

흔히 뭉뚱그려 "계층 위반"이라 부르지만 심각도가 전혀 다른 세 가지를 구분해야 합니다.

| 구분 | 정의 | 이 코드에서의 해당 사례 | 심각도 |
|---|---|---|---|
| (i) 상향 참조 | 하위 계층이 상위 계층의 이름을 앎 | `utils/retry.py:14` → client, `responses/response.py:5-7` → client | 그 자체로는 "문서의 화살표가 틀렸다"는 뜻일 수도 있음 |
| (ii) 순환 (cycle) | A→B→A. ADP 위반 | api↔adapter (`api/account/order.py:15,19` ↔ `adapter/account_product/order_modify.py:80,107`), client↔api | **진짜 비용 발생 지점.** 릴리스/테스트/이해의 단위가 융합됨 |
| (iii) 컴파일타임 vs 런타임 결합 | 모듈 로드 시점 vs 호출 시점 | 모듈 레벨 (a)(c)(e)(f) vs 지연 import (b)(g) 및 adapter 함수 내 12곳 | 모듈 레벨 순환만이 ImportError를 낳음. 지연 import는 순환을 **숨긴** 것이지 없앤 것이 아님 |

원칙을 이 코드에 적용하면:

- **ADP(Acyclic Dependencies Principle)**: 위반 확실. 다만 Python은 링커가 없어 벌금이 C++/Java보다 쌉니다. 벌금은 "import 순서 민감성"과 "부분 로드 불가"로 지불됩니다(§5.3).
- **SDP(Stable Dependencies Principle)**: 가장 많이 의존받는 모듈은 `client/`(responses·utils·event·api 전부가 참조)이므로 client가 가장 안정적이어야 합니다. 그런데 `client/websocket.py:19`가 api의 구체 타입 맵(`WEBSOCKET_RESPONSES_MAP`)을 import합니다 — **가장 안정적이어야 할 모듈이 신규 TR 추가마다 바뀌는 가장 변동성 큰 모듈에 의존**합니다. 이 코드베이스에서 원칙 위반이 실질 위험으로 직결되는 유일한 지점입니다.
- **DIP**: `adapter/`는 이미 DIP를 절반 수행 중입니다. `adapter/account_product/order_modify.py:25,38,64`에 `KisCancelableOrder`, `KisModifyableOrder` Protocol이 정의되어 있고 api가 Mixin을 상속합니다. 추상은 이미 있는데 문서가 이를 "계층"으로 잘못 서술할 뿐입니다.

**결정적 사실**: 이 코드의 실제 형상은 계층(layer)이 아니라 **허브-스포크**입니다. `kis.py:756-758`이 클래스 본문에서 scope를 import해 VmKis를 허브로 만들고, 17개 api 모듈이 `self: "VmKis"` 문자열 어노테이션(58곳)으로 허브를 역참조합니다. 허브-스포크에서 스포크 간 참조는 정의상 계층 위반이 아니라 **허브 설계의 자연스러운 귀결**입니다.

### 5.2 역방향 의존 7종 — 본질적 vs 우발적

| 간선 | 위치 | 분류 | 근거 |
|---|---|---|---|
| **(a)** client→api | `client/websocket.py:19` (모듈 레벨) | **우발적 — MUST FIX** | `WEBSOCKET_RESPONSES_MAP` 사용처는 `:546` dispatch 한 곳뿐. client는 "어떤 응답 타입이 존재하는가"를 알 필요 없고 "id로 찾을 수 있다"만 알면 됨. 전형적 DIP 미적용이며 역전 비용이 매우 낮음 |
| **(b)** client→api | `client/messaging.py:52` (지연) | **우발적 — FIX 권장** | WS 요청 빌더가 approval key를 스스로 조달하러 상위를 호출. 이미 kis 허브를 들고 있으므로 key 공급자를 주입받는 형태로 뒤집는 것이 자연스러움 |
| **(c)** responses→client | `responses/response.py:5-7` (모듈 레벨) | **본질적 — 코드가 아니라 문서가 틀림** | `KisResponse`가 `KisAPIError`를 던지고 `KisObjectBase`/`KisPage` 정체성을 갖는 건 응답 객체의 본질. 실제 방향은 일관되게 responses→client인데 `ARCHITECTURE.md:106-109`만 Client를 Response Transform **위에** 그려놓음. 고칠 대상은 문서 |
| **(d)** api↔adapter | `api/account/order.py:15,19` + `order.py:546`의 `KisOrderBase(KisOrderNumberBase, KisOrderableOrderMixin, KisRealtimeOrderableOrderMixin)` | **본질적 — KEEP + 문서화** | `order.cancel()`, `balance.stock.sell()`이 되는 rich domain object가 이 라이브러리의 상품성 자체. Mixin 쪽(`order_modify.py:80,107`)이 지연 import로 api를 역호출하므로 진짜 순환이지만 **"데이터와 행위의 결합"이라는 설계 의도의 필연**. 억지로 역전하면 사용자 API가 `kis.cancel(order)`로 퇴화 |
| **(e)** event→api | `event/filters/product.py:3-4`, `filters/order.py:4-5` | **우발적·저위험 — 재배치 권장** | `event/handler.py`는 순수 제네릭인데 `event/filters/`만 도메인 타입을 앎. 잘못 놓인 건 의존이 아니라 **디렉터리**. filters를 도메인 측으로 옮기면 event는 순수 하위 계층이 됨 |
| **(f)** utils→client | `utils/retry.py:14` | **우발적 — MUST FIX (5분)** | "유틸리티가 최하층"이라는 문서 주장과 정면충돌하는 유일한 utils 간선. 재시도 가능 예외 튜플을 파라미터로 받으면 끝 |
| **(g)** api→scope | `api/base/product.py:93` (property 내 지연) | **본질적 — KEEP** | `product.stock`으로 상위 scope로 항해하는 fluent API. 허브-스포크의 의도된 역방향 항해이며 지연 import로 로드 순서에서 격리됨 |

### 5.3 이미 지불한 비용 — 측정 결과

전부 이 저장소에서 직접 측정/실행한 값입니다.

1. **순환 우회 장치의 총량**: 함수/프로퍼티 내부의 `vmkis.*` 지연 import **30곳**(AST 계수). 순환 우회 목적이 명백한 것 — adapter→api 12곳(`adapter/websocket/execution.py:83,111,145,173`, `adapter/websocket/price.py:222,232,309,319`, `adapter/product/quote.py:220,232`, `adapter/account_product/order_modify.py:80,107`), client→api 1곳, api→scope 1곳, kis→api 3곳(`kis.py:674,698,716`). 여기에 `TYPE_CHECKING` 블록 보유 파일 **35개**, `self: "VmKis"` 문자열 어노테이션 **17파일 58곳**, `kis.py:756-758` 클래스 본문 import.

2. **부분 로드 불가 — 실측**: `import vmkis.responses.response` 하나만 해도 **vmkis 모듈 87개 전부**가 로드됩니다(실행 확인). `import vmkis.client.websocket`도 동일. `__init__.py`가 `VmKis`를 즉시 import하고 kis.py 클래스 본문이 scope→adapter→api→전체를 연쇄 로드하기 때문입니다. **retry 데코레이터 하나 쓰려 해도 웹소켓 클라이언트까지 로드됩니다.** `import vmkis` 소요 157~220ms(requests 단독 98ms 제외 시 vmkis 몫 약 60~120ms) — 치명적이진 않으나 구조적으로 줄일 수 없는 상태입니다.

3. **문서화되지 않은 load-bearing 불변식**: 전체가 ImportError 없이 로드되는 이유는 단 하나 — **어떤 모듈도 `vmkis.kis`를 모듈 레벨에서 import하지 않는다**(`scope/stock.py:27`, `scope/base.py:6`, `scope/account.py:14` 모두 TYPE_CHECKING 블록 안). 이 불변식은 어디에도 적혀 있지 않습니다. 결정적으로 **`grep -rn "circular\|순환" src/vmkis` 결과는 0건**이고 git 이력에도 순환 관련 커밋이 없습니다. 즉 지연 import 30곳 중 단 한 곳도 사유가 적혀 있지 않습니다. 선의의 리팩터러가 `adapter/websocket/execution.py:83`의 함수 내 import를 파일 상단으로 올리는 순간(린터가 흔히 권하는 바로 그 정리) 패키지가 로드 불능이 될 수 있는데, **그 지뢰의 위치가 코드 어디에도 표시돼 있지 않습니다.**

### 5.4 아직 지불하지 않은 비용 — 공정한 평가

고전적 순환 폐해 중 이 프로젝트에 **해당 없는** 것들:

- **빌드 실패 없음** — 순수 Python, 링커/컴파일 단계 부재. `import vmkis` 성공(실측).
- **테스트가 실제로 막혀 있지 않음** — 87개 모듈 전체 로드가 60~120ms이므로 "격리 불가"의 세금이 체감 속도에 거의 안 잡힘. responses를 client 없이 import할 수는 없지만 그래야 할 실무적 이유가 아직 없음.
- **배포 분리 요구 없음** — 단일 wheel 배포. ADP의 최대 벌금(순환된 컴포넌트는 함께 릴리스해야 함)은 컴포넌트를 쪼갤 계획이 없으면 부과되지 않음. api/adapter/responses/client를 별도 패키지로 나눌 로드맵이 없는 한 (c)(d)의 순환은 **요금이 청구되지 않음**.
- **런타임 정합성 문제 없음** — 지연 import는 호출 시점에 이미 전 모듈이 로드된 뒤 실행되므로 실행 중 ImportError 위험도 사실상 없음.

즉 현재 비용은 "장애"가 아니라 **"이해 비용 + 변경 취약성"**에 국한됩니다. 다만 **(a)만은 예외**입니다 — TR 추가마다 api와 client가 함께 변경되는 구조는 지금도 요금이 나가고 있습니다.

### 5.5 판정

> **질문에 대한 답**: 지금 당장은 문제가 터지지 않았고 대부분은 앞으로도 안 터집니다. 그러나 쟁점은 "단방향이 아니어도 되는가"가 아니라 **"어떤 역방향은 설계이고 어떤 역방향은 사고인가"**이며, 이 프로젝트는 그 둘을 구분해 둔 곳이 없다는 것이 진짜 문제입니다.

**Tier 1 — 반드시 수정** (모듈 레벨 상향 참조, 역전 비용 낮음)

- **(a)** `client/websocket.py:19` — client에 빈 레지스트리를 두고 api가 자기등록하도록 역전:

  ```python
  # client/websocket.py — 소유권 이전
  WEBSOCKET_RESPONSES_MAP: dict[str, type["KisWebsocketResponse"]] = {}

  def register_websocket_response(tr_id: str):
      def deco(cls):
          WEBSOCKET_RESPONSES_MAP[tr_id] = cls
          return cls
      return deco

  # api/websocket/price.py — 등록은 api 쪽 책임
  @register_websocket_response("H0STCNT0")
  class KisDomesticRealtimePrice(...): ...
  ```

  `client/websocket.py:546`의 dispatch는 그대로. **신규 TR 추가 시 client 무변경**이 됩니다. 단 등록이 api 모듈 로드에 의존하므로 `api/websocket/__init__.py`가 로드를 보장해야 하며, 현 허브 구조에서는 자동 충족됩니다.
- **(f)** `utils/retry.py:14` — `retry(..., on: tuple[type[Exception], ...])`로 예외를 파라미터화하거나 해당 예외 4종의 *정의*를 client 밖 하위 모듈로 이동.

**Tier 2 — 의도적 설계로 공인하고 문서화 (수정 금지)**

- **(c)** responses→client: 실제 방향이 맞고 문서의 화살표가 틀림 → 문서 수정.
- **(d)** api↔adapter: rich domain object 설계의 본질. "adapter는 계층이 아니라 api와 같은 링(ring)의 역할 분담"으로 재서술. adapter 내 지연 import 12곳에 `# 순환 방지: api가 이 Mixin을 상속하므로 모듈 레벨 불가` 주석 필수.
- **(g)** api→scope 항해 프로퍼티: 허브-스포크의 의도된 역방향. 지연 import 유지 + 주석.

**Tier 3 — 저비용 정리 (여유 있을 때)**

- **(b)** approval key 공급자 주입으로 역전.
- **(e)** `event/filters/`를 도메인 측(api 또는 adapter)으로 재배치. event 코어는 이미 깨끗함.

### 5.6 문서 처방 — ARCHITECTURE.md가 말해야 할 진실

`docs/architecture/ARCHITECTURE.md:97-112`의 4단 수직 다이어그램(API → Client → Response Transform → Utility)은 삭제하고 다음으로 교체할 것을 제안합니다.

```text
                         ┌──────────────────────────┐
                         │   VmKis (kis.py) — 허브   │
                         │  scope/adapter를 클래스   │
                         │  본문 import로 조립       │
                         └───────┬──────────────────┘
              조립(compose)      │        역참조: self: "VmKis"
        ┌───────────────┬────────┴────────┐   (TYPE_CHECKING 전용, 58곳)
        ▼               ▼                 ▼
   ┌─────────┐    ┌──────────┐      ┌──────────┐
   │  scope/ │───▶│ adapter/ │◀────▶│   api/   │  ◀─ api↔adapter 순환은
   └─────────┘    └──────────┘ 의도적└─┬───┬────┘     의도적(rich object)
                        순환(d)        │   │ ▲
                                       │   │ └─(a) client가 응답맵 참조
                                       ▼   ▼      [수정 대상: 자기등록으로 역전]
                                 ┌──────────┐   ┌────────────┐
                                 │responses/│──▶│  client/   │◀── event/ (subscription)
                                 └──────────┘(c)└─────┬──────┘
                                  의도적: 응답은        │(f) utils/retry가 참조
                                  client 기반 위에 있음  ▼   [수정 대상]
                                                 ┌──────────┐
                                                 │  utils/  │
                                                 └──────────┘
   실제 계층 순서(위가 상위): scope → adapter/api → event → responses → client → utils
```

그리고 다음 **불변식**을 문서에 명문화해야 합니다.

1. **`vmkis.kis`를 모듈 레벨에서 import 금지** (TYPE_CHECKING 블록만 허용). 현재 전체 패키지가 정상 로드되는 유일한 이유이며 지금은 암묵입니다.
2. **신규 모듈-레벨 역방향 간선 금지.** 하위→상위 지식이 필요하면 (a)처럼 등록을 역전하거나 주입받습니다. 기존 역방향은 (c)(d)(g) 셋으로 동결하고 각각 "의도적"으로 표기합니다.
3. **모든 순환 우회 지연 import에 사유 주석 필수.** 현재 30곳 중 0곳에 사유가 있습니다.
4. CI에 **import-linter** 도입 권장: `utils → 상위 금지`, `client → api 금지`(등록 역전 후) 두 계약만으로 Tier 1 회귀를 기계적으로 차단할 수 있습니다.

---

## 6. API 커버리지 비교 — 가장 중요한 격차

### 6.1 정량 비교

| 세그먼트 | open-trading-api | vm-stock-kis |
|---|---|---|
| 국내주식 | 156 함수 (REST 131 + WS 25) | 시세 5 TR + 주문/계좌 약 20 TR |
| 해외주식 | 50 함수 (REST 46 + WS 4) | 시세 5 TR + 주문/계좌 약 30 TR (9개 시장) |
| 국내 선물옵션 | 43 함수 | **0 (미지원)** |
| 해외 선물옵션 | 35 함수 | **0 (미지원)** |
| ELW | 24 함수 | **0 (미지원)** |
| 장내채권 | 18 함수 | **0 (미지원)** |
| ETF/ETN | 6 함수 | **전용 API 0** (일반 현재가 TR로 가격 조회만 가능) |
| 인증 | 2 함수 | 3 경로 (`tokenP`, `revokeP`, `Approval`) |
| **합계** | **334 함수 / 고유 TR ID 377** | **REST 경로 30 / 고유 TR ID 74 / WS TR ID 9** |

### 6.2 vm-stock-kis가 지원하는 것 (전수)

**국내 시세**: `FHKST01010100`(현재가) `FHKST01010200`(호가) `FHKST03010100`(기간봉) `FHKST03010200`(당일분봉) `CTPF1604R`(상품기본조회)

**해외 시세**: `HHDFS00000300`(현재가) `HHDFS76200100`(10호가) `HHDFS76200200`(현재가상세) `HHDFS76240000`(기간별) `HHDFS76950200`(분봉)

**국내 주문/계좌**: `TTTC0801U/0802U/0803U` + `VTTC*`(매도/매수/정정취소), `TTTC8001R`/`CTSC9115R`(+`VT*`, 일별체결), `TTTC8036R`(미체결, 모의 미지원), `TTTC8434R`/`VTTC8434R`(잔고), `TTTC8908R`/`VTTC8908R`(매수가능), `TTTC8715R`(기간손익, 모의 미지원), `CTRP6504R`/`VTRP6504R`(체결기준현재잔고)

**해외 주문/계좌**: 미국 `TTTT1002U/1006U/1004U`, 일본 `TTTS0308U/0307U/0309U`, 상하이 `TTTS0202U/1005U/0302U`, 홍콩 `TTTS1002U/1001U/1003U`, 심천 `TTTS0305U/0304U`, 베트남 `TTTS0311U/0310U/0312U` (+ 각 `VT*` 모의), 미국 주간거래 `TTTS6036U/6037U/6038U`, 조회 `TTTS3007R/3012R/3018R/3035R/3039R`

**WebSocket 9종** (`src/vmkis/api/websocket/__init__.py:13-23` 직접 확인):
`H0STCNT0`(국내체결) `HDFSCNT0`(해외체결) `H0STASP0`(국내호가) `HDFSASP0`(미국호가) `HDFSASP1`(아시아호가) `H0STCNI0/9`(국내 체결통보) `H0GSCNI0/9`(해외 체결통보)
→ 사용자 이벤트 표면은 `"price"` / `"orderbook"` / `"execution"` 3종

**해외 시장 9개**: NASDAQ, NYSE, AMEX, TYO, HKEX, SSE, SZSE, HNX, HSX (`api/stock/market.py:17-29`)

### 6.3 vm-stock-kis가 지원하지 않는 것

- **국내주식 심화**: 등락률/거래량 순위, 투자자별 매매동향, 업종/지수 시세, 프로그램매매, 조건검색(HTS 조건식), 시간외 단일가, 공매도 현황, 예탁원정보(`ksdinfo_*`)
- **파생**: 국내/해외 선물옵션 전부 (시세·주문·잔고)
- **채권**: 장내채권/일반채권 전부
- **ELW**: 전부
- **ETF/ETN 전용**: NAV 비교추이·괴리율 등
- **주문 심화**: 예약주문(`CTSC0008U`), 신용주문(`TTTC0852U` 계열), 퇴직연금(`TTTC2202R` 등)
- **실시간**: 예상체결, 지수, 회원사, 프로그램매매, 시간외 체결/호가 등 파생 실시간 전부

---

## 7. 같은 API, 두 저장소의 코드 비교

### 7.1 국내주식 현재가 (`FHKST01010100`)

**open-trading-api** — `examples_llm/domestic_stock/inquire_price/inquire_price.py`

```python
API_URL = "/uapi/domestic-stock/v1/quotations/inquire-price"

def inquire_price(env_dv: str, fid_cond_mrkt_div_code: str, fid_input_iscd: str) -> pd.DataFrame:
    if env_dv == "real":   tr_id = "FHKST01010100"
    elif env_dv == "demo": tr_id = "FHKST01010100"
    params = {"FID_COND_MRKT_DIV_CODE": fid_cond_mrkt_div_code, "FID_INPUT_ISCD": fid_input_iscd}
    res = ka._url_fetch(API_URL, tr_id, "", params)
    if res.isOK():
        return pd.DataFrame(res.getBody().output, index=[0])
    else:
        res.printError(url=API_URL)
        return pd.DataFrame()          # ← 실패해도 예외 없음
```

호출 측은 `df["stck_prpr"]`(문자열)로 접근. 짝 파일 `chk_inquire_price.py`가 약 90항목 `COLUMN_MAPPING`으로 한글명을 붙입니다.

**vm-stock-kis** — 동일 기능이 761줄에 걸쳐 5개 구성요소로 분해

```python
# src/vmkis/api/stock/quote.py
class KisQuote(KisProductProtocol, Protocol): ...        # :74-201  타입 계약
@kis_repr("symbol", "price", lines="multiple")
class KisQuoteRepr: ...                                   # :269-294 표시
class KisQuoteBase(KisQuoteRepr, KisProductBase): ...     # :297-373 파생 속성
class KisDomesticQuote(KisQuoteBase, KisAPIResponse):     # :398
    price: Decimal = KisDecimal["stck_prpr"]              # :408  선언적 필드
    def __pre_init__(self, data):                         # :478  빈 응답 → raise_not_found
        ...
def domestic_quote(self: "VmKis", symbol, market) -> KisDomesticQuote:   # :618
    result = KisDomesticQuote(symbol, "KRX")
    return self.fetch("/uapi/domestic-stock/v1/quotations/inquire-price",
                      api="FHKST01010100", params={...},
                      response_type=result, domain="real")
def quote(self: "VmKis", symbol, market): ...             # :705  국내/해외 분기
def product_quote(self: "KisProductProtocol", ...): ...   # :738  scope 바인딩
```

사용자는 `kis.stock("000660").quote().price` → `Decimal`. 오류는 `KisAPIError` 예외.

**차이의 본질**: 공식은 *한 파일 = 한 API*, vmkis는 *한 파일 = 한 개념(국내+해외 통합 시세)*. 후자가 사용성은 좋지만 **구성요소 5개를 모두 만들어야 API 하나가 완성**됩니다.

### 7.2 페이지네이션

| | open-trading-api | vm-stock-kis |
|---|---|---|
| 방식 | 함수 **재귀** (`depth`/`max_depth=10`) | `while` 루프 + `KisPage` 객체 |
| 커서 노출 | 함수 인자로 `FK100`/`NK100`/`tr_cont` 노출 | `KisPage.__pre_init__`이 `fk100`/`fk200` 자동 감지 (`client/page.py:47-58`) |
| 코드 | `inquire_balance.py` 참조 | `api/account/balance.py:934-967` |
| 중복 | API마다 재귀 보일러플레이트 재작성 | 4개 API가 동일 while 루프를 각자 구현 (**공통 헬퍼 없음**) |

### 7.3 인증·토큰·동시성

| | open-trading-api | vm-stock-kis |
|---|---|---|
| 토큰 저장 | `~/KIS/config/KIS{YYYYMMDD}` 파일 (하드코딩 경로) | `keep_token=True` 시 `~/.vmkis/` 평문 JSON |
| 토큰 주입 | 모듈 전역 `_base_headers["authorization"]` **제자리 mutate** | 인스턴스 `token` property (`kis.py:669-712`), 만료 10분 전 자동 재발급 |
| 실전+모의 동시 | **불가** (전역 `_isPaper` 단일값) | **가능** (`VmKis(auth, virtual_auth=...)`, 세션/리미터 도메인별 분리) |
| 스레드 안전 | 없음 | `@thread_safe` (토큰 발급 `kis.py:670`, 구독 변경 `websocket.py:219,253`) |
| 모의 TR 변환 | `_url_fetch`가 `T/J/C` 시작 TR을 자동 `V` 치환 | 각 API 함수가 명시적 분기 (`"VTTC..." if self.virtual else "TTTC..."`, 28곳 산재) |

### 7.4 Rate Limiting

| | open-trading-api | vm-stock-kis |
|---|---|---|
| 구현 | `smart_sleep()` = 고정 `time.sleep(0.1)` | `RateLimiter` 도메인별 락 기반 (`utils/rate_limit.py:54`) |
| 설정값 | 실전 0.05 / 모의 0.5로 설정하려 하나 **`global` 선언 누락으로 지역변수화** → 항상 0.1 고정 (버그) | `REAL_API_REQUEST_PER_SECOND = 20 - 1` = **19/s**, `VIRTUAL = 2`/s (`__env__.py:18-19` 직접 확인) |
| 적용 범위 | 페이지네이션 재귀·WS 구독 전송에만. **일반 단건 호출엔 미적용** | `request()` 전 항상 `acquire()` (`kis.py:561`) |
| 초과 시 | 없음 | `EGW00201` 수신 시 0.1s 후 재시도 (`kis.py:585-589`) — **단, 재시도 상한 없는 `while True`** |

### 7.5 WebSocket

| | open-trading-api | vm-stock-kis |
|---|---|---|
| 엔진 | `KISWebSocket` (asyncio, `kis_auth.py:461-799`) | `KisWebsocketClient` (threading + `run_forever`, `client/websocket.py` 593줄) |
| 스키마 | 함수가 `columns` 리스트를 **하드코딩 반환**, `pd.read_csv(sep="^")`로 씌움 | `__fields__` 위치 기반 `KisType` 변환 (`responses/websocket.py:48`) |
| 컬럼 오류 시 | **조용히 밀린 DataFrame** 생성 | 타입 변환 실패 → 예외 |
| 재접속 | `max_retries=3`, `sleep(1)` 고정. 성공 후 카운터 리셋 없음 → 3회 소진 시 영구 종료 | `_run_forever` 루프 + `_restore_subscriptions` (`:347`) + 세션 상태/암호키 리셋 (`:339-345`) |
| 구독 해지 | `unsubscribe()`가 코루틴을 **await 없이 호출** → 동작 안 함 | `KisEventTicket.__del__` GC 자동 해지 + `ReferenceStore` 참조카운팅 (`:287,334-337`) |
| 40 구독 한도 | **함수 종류 수**를 셈 → 실제 제한과 불일치 | `WEBSOCKET_MAX_SUBSCRIPTIONS=40` 정확히 강제 (`:246`) |
| 모의 체결통보 | 미지원 | 별도 실전 클라이언트 프록시 (`_ensure_primary_client:573`) |
| AES 복호화 | `aes_cbc_base64_dec` (pycryptodome) | keychain 자동 적재 (`:510-520`), `cryptography` 사용 |

---

## 8. 사용자 관점 사용 편의성 — 클래스 방식 vs 함수 방식

인용된 코드는 모두 실제 저장소에 존재하는 코드이며, 각 항목에 출처 파일을 명시했습니다.

- **vmkis**: `VmKis` 객체 → Scope(`kis.stock(...)`) → 타입 객체(`Decimal`, `datetime`) 반환
- **official**: `kis_auth.py` 전역 인증 → 개별 함수 호출 → 문자열 `pandas.DataFrame` 반환

### 8.1 첫 실행까지의 거리

**vmkis — 3단계** (`QUICKSTART.md` 기준)

```bash
pip install vm-stock-kis        # 1. 설치
# 2. config.yaml 작성 (id/account/appkey/secretkey/virtual 5개 키)
```

```python
# 3. 실행 (examples/01_basic/get_quote.py 축약)
from vmkis import KisAuth, VmKis

auth = KisAuth(id="...", account="00000000-01", appkey="...", secretkey="...", virtual=True)
kis = VmKis(auth, keep_token=True)          # 토큰 발급·캐시 자동 (~/.vmkis/)
print(kis.stock("005930").quote().price)    # Decimal('71000')
```

**official — 6단계** (`README.md` 3장 기준)

```bash
git clone https://github.com/koreainvestment/open-trading-api   # 1. pip 패키지 아님, clone 필수
uv sync    # 또는 pip install requests pandas websockets PyYAML pycryptodome   # 2. 의존성
mkdir -p ~/KIS/config && cp kis_devlp.yaml ~/KIS/config/         # 3. 홈 밑 고정 경로로 복사
# 4. kis_devlp.yaml 편집: my_app/my_sec/paper_app/paper_sec/my_htsid/my_acct_stock/my_prod/my_agent
```

```python
# 5~6. examples_llm/domestic_stock/inquire_price/chk_inquire_price.py 실제 코드
import sys
sys.path.extend(['../..', '.'])   # 5. 실행 디렉터리 의존적 sys.path 해킹 — 모든 예제 파일 상단에 존재
import kis_auth as ka

ka.auth()                          # 6. 명시적 인증 (전역 상태 _TRENV 설정)
result = inquire_price(env_dv="real", fid_cond_mrkt_div_code="J", fid_input_iscd="005930")
print(result)                      # DataFrame 1행, 90여 개 문자열 컬럼
```

정직하게 세면 **vmkis 3단계 vs official 6단계**입니다. 특히 official의 `sys.path.extend(['../..', '.'])`는 실행 위치가 예제 폴더가 아니면 import가 깨진다는 뜻이고, `kis_auth.py`는 import 시점에 `~/KIS/config/kis_devlp.yaml`을 무조건 읽으므로 설정 파일이 없으면 **import 자체가 실패**합니다. 반면 vmkis는 pip 설치형이라 어느 디렉터리에서든 동작합니다. 다만 official의 방식은 "내 프로젝트에 파일을 복사해 넣는" 전통적 스크립트 문화에 익숙한 사용자에겐 오히려 익숙할 수 있습니다.

### 8.2 단일 시세 조회

| | vmkis | official |
|---|---|---|
| 호출 | `kis.stock("005930").quote()` | `inquire_price("real", "J", "005930")` |
| 반환 | `KisQuote` 객체 | `pd.DataFrame` (1행, 전 컬럼 문자열) |
| 현재가 | `quote.price` → `Decimal` | `df["stck_prpr"][0]` → `"71000"` (str) |
| 등락률 | `quote.rate` → `Decimal` | `df["prdy_ctrt"][0]` → str, `float()` 변환 필요 |

```python
# vmkis — price/open/high/low 전부 Decimal로 선언 (api/stock/quote.py)
quote = kis.stock("005930").quote()
print(f"{quote.price:,.0f}원 ({quote.rate}%)")
```

```python
# official — 필드명이 KIS 전문 코드 그대로라 chk_inquire_price.py가
#            COLUMN_MAPPING 딕셔너리(90여 항목)를 따로 제공할 정도다
df = inquire_price(env_dv="real", fid_cond_mrkt_div_code="J", fid_input_iscd="005930")
price = int(df["stck_prpr"].iloc[0])       # 수동 형변환
rate = float(df["prdy_ctrt"].iloc[0])
print(f"{price:,}원 ({rate}%)")
```

official은 `fid_cond_mrkt_div_code="J"` 같은 전문 파라미터를 사용자가 알아야 하고(J=KRX, NX=NXT, UN=통합), `stck_prpr`가 현재가라는 것도 매핑 표를 봐야 압니다. vmkis는 `price`, `rate`처럼 도메인 언어로 번역했습니다. 단 **이 번역 자체가 "vmkis의 이름 체계를 새로 배워야 한다"는 뜻**이기도 합니다 — KIS 공식 문서와 필드명이 1:1로 대응하지 않습니다.

### 8.3 잔고 조회 + 보유종목 순회

```python
# vmkis — KisBalance.stocks는 list[KisBalanceStock], 모든 금액이 Decimal
balance = kis.account().balance()

for s in balance.stocks:
    print(f"{s.symbol}: {s.qty}주, 평단 {s.purchase_price:,.0f}, "
          f"손익 {s.profit:+,.0f}원 ({s.profit_rate:+.2f}%)")

total_profit = sum(s.profit for s in balance.stocks)   # Decimal 합산, 오차 없음
print(f"총 평가금액 {balance.current_amount:,.0f} / 손익 {total_profit:+,.0f}")
```

```python
# official — inquire_balance는 필수 문자열 파라미터 9개 + (df1, df2) 튜플 반환
df1, df2 = inquire_balance(
    env_dv="real", cano=trenv.my_acct, acnt_prdt_cd=trenv.my_prod,
    afhr_flpr_yn="N", inqr_dvsn="01", unpr_dvsn="01",
    fund_sttl_icld_yn="N", fncg_amt_auto_rdpt_yn="N", prcs_dvsn="00",
)
for _, row in df1.iterrows():
    profit = int(row["evlu_pfls_amt"])          # 문자열 → int 수동 변환
    rate = float(row["evlu_pfls_rt"])
    print(f"{row['pdno']}: {row['hldg_qty']}주, 손익 {profit:+,}원 ({rate:+.2f}%)")

total_profit = pd.to_numeric(df1["evlu_pfls_amt"]).sum()
```

두 가지가 눈에 띕니다. (1) official의 `inquire_balance`는 `afhr_flpr_yn="N"`, `fncg_amt_auto_rdpt_yn="N"`처럼 **의미를 모르는 채 외워 넣는 파라미터가 6개**이고 vmkis는 전부 기본값으로 흡수했습니다. (2) 연속조회를 official은 함수 내부 재귀로 처리하는데 그 재귀 관리 인자(`depth`, `max_depth`, `FK100`, `NK100`)가 시그니처에 그대로 노출됩니다.

다만 **집계만 한다면** `pd.to_numeric().sum()` 한 줄이면 되므로 DataFrame이 크게 불리하지 않습니다. 격차가 결정적인 건 개별 종목 단위 로직입니다 — vmkis는 `s.profit_rate < -5` 비교가 바로 되고, `KisBalanceStock`이 `KisOrderableAccountProduct`를 구현하므로 **보유종목 객체에서 곧바로 `s.sell(qty=s.orderable)`을 호출**할 수 있습니다.

### 8.4 주문 → 정정/취소 — 클래스 방식의 가장 강한 논거

코드로 검증한 결과 두 설계의 격차가 가장 큰 곳입니다.

```python
# vmkis — 주문 객체가 곧 정정/취소의 핸들 (active record 스타일)
order = kis.stock("005930").buy(price=70000, qty=10)

order = order.modify(price=69500)   # 가격만 변경 — 수량/조건은 자동 유지
order.cancel()                       # 취소 끝
```

가능한 이유가 코드에 명확히 있습니다.

- `api/account/order.py:340` — `KisOrderNumber`가 `branch`(=`KRX_FWDG_ORD_ORGNO` 지점코드)와 `number`(주문번호)를 **주문 응답 시점에 객체에 저장**합니다 (`branch: str = KisString["KRX_FWDG_ORD_ORGNO"]`).
- `adapter/account_product/order_modify.py` — `KisModifyableOrderMixin.modify()` / `KisCancelableOrderMixin.cancel()`이 `self`를 그대로 `modify_order(self.kis, order=self, ...)`에 넘깁니다.
- `api/account/order_modify.py:140~188` — `modify()`에 생략된 인자는 **미체결 주문 조회로 원주문 값을 자동으로 채웁니다.** 시장가 상한가 보정(`price_setting == "upper"`이면 `quote.high_limit` 사용)까지 내부 처리하고, 최종적으로 `KRX_FWDG_ORD_ORGNO: order.branch`, `ORGN_ODNO: order.number`를 라이브러리가 대신 넣습니다.

official에서 같은 일을 하려면:

```python
# 1. 주문 — 주문번호와 지점코드를 "사용자가 직접" 뽑아 보관해야 한다
df = order_cash(env_dv="demo", ord_dv="buy", cano=trenv.my_acct, acnt_prdt_cd=trenv.my_prod,
                pdno="005930", ord_dvsn="00", ord_qty="10", ord_unpr="70000", excg_id_dvsn_cd="KRX")
odno = df["ODNO"].iloc[0]                      # 주문번호
ord_orgno = df["KRX_FWDG_ORD_ORGNO"].iloc[0]   # 지점코드 — 이 둘을 잃으면 정정/취소 불가

# 2. 정정 — 필수 파라미터 12개, 전부 문자열. 원주문 수량도 사용자가 기억해서 다시 넣어야 함
df2 = order_rvsecncl(env_dv="demo", cano=trenv.my_acct, acnt_prdt_cd=trenv.my_prod,
                     krx_fwdg_ord_orgno=ord_orgno, orgn_odno=odno,
                     ord_dvsn="00", rvse_cncl_dvsn_cd="01",   # 01=정정, 02=취소 (코드 암기)
                     ord_qty="10", ord_unpr="69500", qty_all_ord_yn="N", excg_id_dvsn_cd="KRX")
```

게다가 `order_rvsecncl`의 docstring 자체가 *"호출 전에 반드시 주식정정취소가능주문조회(`inquire_psbl_rvsecncl`)를 통해 정정취소가능수량을 확인하신 후 주문 내시기 바랍니다"*라고 안내합니다 — 안전한 정정취소는 사실상 **함수 3개를 조합하고 상태(주문번호·지점코드·잔량)를 사용자 코드가 들고 다니는** 작업입니다.

vmkis는 이 상태 운반을 객체가 대신하며, 프로세스 재시작 후에도 `KisOrder.from_number(kis, symbol=..., market="KRX", account_number=..., branch=..., number=...)`로 핸들을 복원할 수 있고 `account.pending_orders()`가 반환하는 미체결 주문 객체들도 동일하게 `.cancel()` 가능합니다. **주문 관리가 핵심인 봇이라면 이 항목 하나만으로 클래스 방식을 선택할 이유가 됩니다.**

### 8.5 실시간 구독

```python
# vmkis (examples/01_basic/realtime_price.py 실제 코드)
stock = kis.stock("005930")

def on_price(sender, e):
    print(e.response)          # 타입 객체

ticket = stock.on("price", on_price)   # 구독 + 티켓 반환
input("Press Enter to stop...")
ticket.unsubscribe()
```

```python
# official (examples_llm/domestic_stock/ccnl_krx/chk_ccnl_krx.py 실제 코드)
ka.auth()
ka.auth_ws()                                        # REST와 별도로 웹소켓 인증
kws = ka.KISWebSocket(api_url="/tryitout")
kws.subscribe(request=ccnl_krx, data=["005930", "000660"])

def on_result(ws, tr_id: str, result: pd.DataFrame, data_map: dict):
    result.rename(columns=COLUMN_MAPPING, inplace=True)   # 컬럼이 MKSC_SHRN_ISCD 등 원코드
    print(result)

kws.start(on_result=on_result)   # 내부에서 asyncio.run() — 블로킹, 이 뒤 코드는 실행 안 됨
```

- **콜백 라우팅**: vmkis는 종목·이벤트 단위 콜백이라 콜백 안에서 분기할 필요가 없습니다. official은 모든 TR 데이터가 단일 `on_result`로 들어오므로 여러 종류를 구독하면 `tr_id`로 직접 분기해야 합니다.
- **수명 관리 함정 (vmkis)**: `KisEventTicket.__del__`(`event/handler.py:265`)이 GC 시점에 **자동으로 구독을 해지**합니다. 즉 `stock.on("price", cb)`를 변수에 담지 않으면 티켓이 즉시 GC되어 구독이 소리 없이 끊길 수 있습니다(2.1.1 이후 `UserWarning`으로 완화, `ticket.suppress()` 또는 `with ticket:`도 제공). 처음 쓰는 사람이 반드시 밟는 함정입니다.
- **구조적 제약 (official)**: `kws.start()`가 내부에서 `asyncio.run()`을 호출하는 블로킹 설계라 "구독하면서 다른 로직도 도는" 봇을 만들려면 스레드/태스크를 직접 구성해야 합니다. 구독 목록이 모듈 전역 `open_map`/`data_map`으로 관리되는 점도 멀티 인스턴스를 어렵게 합니다.

### 8.6 에러 처리

vmkis는 예외 계층이 있습니다 (`client/exceptions.py`): `KisException` → `KisHTTPError` → `KisConnectionError`/`KisAuthenticationError`/`KisRateLimitError`/`KisServerError`, 그리고 `KisAPIError`의 서브클래스로 도메인 예외 `KisMarketNotOpenedError`(`responses/exceptions.py:37`)까지.

```python
# vmkis — 실패는 예외로 전파되므로 잡지 않으면 봇이 멈추고, 잡으면 종류별 대응 가능
from vmkis import KisAPIError, KisMarketNotOpenedError

try:
    order = stock.buy(price=70000, qty=10)
except KisMarketNotOpenedError:
    schedule_for_next_open()
except KisAPIError as e:
    logger.error("주문 거부: %s", e)     # rt_cd/메시지 포함
```

```python
# official — 모든 호출 뒤에 빈 DF 체크를 스스로 넣어야 한다
df = order_cash(...)
if df.empty:
    # 왜 실패했는지는 반환값에 없음 — 콘솔 로그를 봐야 함
    handle_failure_somehow()
```

official은 API 실패 시 `printError()`로 stdout에 출력하고 **빈 DataFrame을 반환**합니다. 실질적 위험은 **실패가 조용히 지나간다**는 것입니다 — 주문 실패를 놓친 봇은 포지션 관리가 어긋납니다. 파라미터 누락은 official도 `ValueError`를 던지지만 API 레벨 실패는 반환값만 봐서는 원인을 알 수 없습니다. 트레이딩 봇 기준으로는 vmkis가 명백히 안전합니다. 단 **데이터 수집 스크립트처럼 "실패하면 건너뛰고 계속"이 기본인 워크로드에선 빈 DF 방식이 오히려 편하다는 반론도 성립**합니다.

### 8.7 IDE / 타입 경험

- vmkis는 `py.typed` 마커가 있는 정식 타입 패키지입니다. 사용자 표면이 Protocol로 선언되어 있어(`KisQuote.price -> Decimal`) `kis.stock("005930").`을 치는 순간 IDE가 `quote / chart / daily_chart / buy / sell / on ...`을 자동완성하고, pyright가 `quote.price + "원"` 같은 실수를 잡습니다.
- 정직하게 짚을 것: 내부 구현은 디스크립터 트릭 위에 서 있습니다. `responses/dynamic.py:81`에서 `KisType.__call__`은 `-> T`로 선언하고 실제로는 `return self  # type: ignore`를 합니다. 즉 `branch: str = KisString["KRX_FWDG_ORD_ORGNO"]`는 정적으로는 `str`이지만 그 자리에 실제로 놓이는 것은 디스크립터 객체이고, 런타임 `transform`이 진짜 `str`/`Decimal`로 바꿔 넣습니다. **사용자가 받는 값은 진짜 타입이 맞지만**, 라이브러리 내부를 디버깅하러 들어가면 정적 타입이 겉포장인 지점을 만납니다.
- official은 함수 시그니처가 전부 `str` 파라미터에 `-> pd.DataFrame`이라 타입 검사가 잡아주는 게 거의 없습니다. `df["stck_prpr"]` 오타는 런타임 `KeyError`로만 발견됩니다. 대신 각 함수 docstring이 파라미터 코드값(`"01 – 대출일별 | 02 – 종목별"` 등)을 상세히 담고 있어 **hover 문서로서의 가치는 높습니다.**

### 8.8 데이터 분석 친화성 — official의 진짜 강점

여기는 official이 이깁니다.

```python
# official — 모든 함수가 처음부터 DataFrame 반환
df = inquire_daily_itemchartprice(..., fid_input_iscd="005930", ...)
df.to_parquet("005930_daily.parquet")            # 저장 즉시 가능
df["stck_clpr"] = pd.to_numeric(df["stck_clpr"]) # 숫자 변환만 필요
```

vmkis에서 DataFrame으로 나가는 공식 통로는 **차트뿐**입니다 (`api/stock/chart.py:294`의 `KisChart.df()` — pandas 미설치 시 `ImportError` 안내, `Decimal`을 `float`로 변환해 time/open/high/low/close/volume 컬럼 생성):

```python
chart = kis.stock("005930").daily_chart(...)
df = chart.df()          # 이건 편하다 — 컬럼명도 표준적이고 숫자형이다
```

그러나 잔고·시세·주문 응답에는 `.df()`가 없습니다. 원본은 `KisDynamic.raw`(`responses/dynamic.py:150`)로 dict를 꺼낼 수 있지만 결국 이런 코드를 직접 짜야 합니다:

```python
df = pd.DataFrame([{
    "symbol": s.symbol, "qty": int(s.qty),
    "profit": float(s.profit), "rate": float(s.profit_rate),
} for s in balance.stocks])
```

커버리지 자체도 다릅니다. official의 `domestic_stock_functions.py` 한 파일에만 131개 함수(시세분석·순위·업종·공매도·프로그램매매 등)가 있습니다. **분석 파이프라인의 종착지가 DataFrame이라면 출발부터 DataFrame인 쪽이 마찰이 적습니다.**

### 8.9 학습 곡선 / 발견 가능성

- **vmkis**: 제대로 쓰려면 Scope → Adapter → Protocol 3층 구조를 이해해야 합니다. "`.buy()`가 대체 어디 정의돼 있지?"의 답이 `adapter/account_product/order.py`의 믹스인이라는 건 go-to-definition 없이는 찾기 어렵습니다. 대신 **런타임 발견 가능성**은 좋습니다 — `kis.stock("005930")` 이후 자동완성이 API 지도 역할을 합니다. 즉 **IDE가 있으면 배우기 쉽고, 소스만 읽으면 배우기 어렵습니다.**
- **official**: 아키텍처가 없다는 것이 곧 학습 모델입니다. "폴더 찾기 → `chk_*.py` 열기 → 복사"가 전부이고, 함수 하나가 URL·tr_id·파라미터·컬럼매핑까지 자기완결적으로 담습니다. 초보자가 **첫 결과를 얻는 속도**는 official이 빠릅니다(개념 학습이 0이므로). 다만 복사한 코드 20개가 쌓인 뒤의 유지보수는 온전히 사용자 몫입니다.
- **LLM 코드 생성**: official은 디렉터리 이름부터 `examples_llm`이고 루트에 `llms.txt`가 있습니다. 1함수·1폴더·자기완결 구조는 컨텍스트 주입과 패턴 모방에 최적화되어 있습니다. vmkis는 믹스인·디스크립터에 걸친 암묵 지식(티켓 보관, `modify`의 `...` 기본값 등)이 많아 LLM이 **그럴듯하지만 틀린 코드**를 만들 여지가 큽니다.

### 8.10 초보자용 SimpleKIS — 격차를 메우는가?

`src/vmkis/simple.py`의 실제 전체 API는 메서드 **4개**입니다.

```python
class SimpleKIS:
    def get_price(self, symbol: str) -> Any:                 # kis.stock(symbol).quote()
    def get_balance(self) -> Any:                            # kis.account().balance()
    def place_order(self, symbol, qty, price=None) -> Any:   # price 없으면 시장가 매수
    def cancel_order(self, order_obj) -> Any:                # order_obj.cancel() 위임
```

```python
from vmkis import create_client
from vmkis.simple import SimpleKIS

kis = create_client("config.yaml")     # config 로드 + KisAuth + VmKis 일괄 처리
simple = SimpleKIS(kis)
price = simple.get_price("005930")
print(f"삼성전자: {price.price:,}원")
```

**부분적으로만** 메웁니다. 좋은 점 — 진입 코드가 3줄로 줄고, `save_config_interactive()`(입력 마스킹 포함 대화형 설정 생성)까지 있어 official의 "yaml을 홈 폴더에 복사해 편집"보다 온보딩이 매끄럽습니다. 한계 — (1) **매도·정정·실시간·차트가 없어** 조금만 나아가면 `VmKis` 본체로 내려가야 하고, (2) 반환 타입이 전부 `Any`라 **vmkis 최대 장점인 타입 경험을 파사드 계층에서 스스로 버렸습니다.**

### 8.11 결론 표

| 시나리오 | 승자 | 이유 |
|---|---|---|
| 일회성 조회 스크립트 | official (근소) | 폴더에서 `chk_*.py` 복사가 가장 빠름 — 단 최초 환경 설정 6단계는 감수 |
| 실시간 봇 | **vmkis** | 종목 단위 `stock.on()` + 논블로킹 vs 전역 상태·블로킹 `kws.start()` |
| 백테스트 데이터 수집 | **official** | 전 API가 DataFrame 반환 + 시세분석·순위류 커버리지가 훨씬 넓음 |
| 주문 관리 (정정/취소) | **vmkis** | `order.modify()/cancel()`이 지점코드·주문번호·잔량 운반을 전부 대신함 — 가장 명확한 격차 |
| 멀티계정 운영 | **vmkis** | `VmKis` 인스턴스 격리 vs `kis_auth.py`의 모듈 전역 단일 상태 |
| 파생·채권 등 전 상품군 | **official** | 공식 저장소가 전 상품 예제 보유; vmkis는 주식 현물만 |
| LLM 코드 생성 | **official** | `examples_llm` + `llms.txt` + 자기완결 1함수 구조가 생성 오류율을 낮춤 |
| 팀 프로덕션 코드베이스 | **vmkis** | `py.typed` 타입 표면 + 예외 계층 + pip 배포·버전 관리 |

> **총평**: *"탐색·수집은 함수 방식, 운영·주문은 클래스 방식"*이 코드 근거상 정직한 결론입니다. 실제 봇 프로젝트라면 **vmkis를 골격으로 쓰되 커버리지가 부족한 조회성 API는 `fetch()`로 뚫는**(부록 A) 혼합 전략이 현실적입니다.

---

## 9. 항목별 장단점 종합

### 9.1 vm-stock-kis

**장점 (코드 근거 확인)**

1. **국내/해외 응답 정규화가 실재** — `KisQuote` Protocol 하나로 `KisDomesticQuote`/`KisForeignQuote` 통합. 환율(`exchange_rate`)·소수점(`decimal_places`)·호가단위까지 정규화(`quote.py:512-588`). 주문도 시장별 TR 매핑 테이블(`FOREIGN_ORDER_API_CODES`, `order.py:1123-1161`)로 단일 인터페이스.
2. **테스트 가능한 설계** — 엔드포인트가 전부 `def f(self: "VmKis", ...)` 모듈 함수(56개)라 `fetch`만 mock하면 단독 테스트 가능. 실제 테스트 **957개**.
3. **WebSocket 수명주기 관리가 견고** — 재접속+구독 복원, 참조카운팅 자동 해지, 모의 이중 서버 프록시, 구독 한도 강제.
4. **스레드 안전성 일관** — 토큰·구독·리미터 전부 락 보호.
5. **공개 API 다이어트 실제 완료** — `__init__.py __all__` 12개 + `public_types.py` 8개 별칭, 구 경로는 `__getattr__` 경고 후 `vmkis.types`(100개)로 위임.
6. **범용 escape hatch 존재** — `kis.fetch(api="TRID", response_type=...)` (§10)

**단점 (코드 근거 확인)**

1. **`VmKis` 신 객체** — fan-in 36파일 / 29 import. 인증+토큰+세션+리미터+캐시+WS+범용 HTTP가 한 클래스(758줄). 모든 계층이 `self.kis`로 허브 재진입 → **계층 격리 사실상 없음**.
2. **추상화 누수** — `kis_object_init`이 응답 객체에 `kis`를 주입해야 `KisForeignQuote.indicator`(`quote.py:557` — **속성 접근이 추가 REST 호출 유발**)가 동작. 데이터 객체가 통신 능력을 가짐. 또 `stock()` 팩토리가 **네트워크 없이는 Scope 생성 불가**(`scope/stock.py:107`) → 오프라인 테스트 저해.
3. **신규 엔드포인트 보일러플레이트** — §10 참조. quote=761줄, order=2,066줄. **동일 docstring이 Protocol / Mixin / api 함수 3곳에 복제**.
4. **동적 타입 시스템의 대가** — `KisType.__call__`이 `-> T`로 거짓 선언하고 실제로는 `self`를 반환(`dynamic.py:81`, `# type: ignore`). `transform_` 실행 전 속성 접근은 `Decimal`이 아닌 `KisType` 인스턴스 → 정적 검사기가 못 잡는 런타임 지뢰. 한 필드가 Protocol+Base+국내+해외 **4중 선언**.
5. **이름 충돌** — `KisNotFoundError`가 `client/exceptions.py:202`(HTTP 404 계열)와 `responses/exceptions.py:13`(조회결과 없음)에 **동명 별개 클래스**로 존재 (직접 확인). catch 시 혼동 유발.
6. **`request()` 무한 루프 가능** — `kis.py:560-599`의 `while True`에 재시도 상한 없음. 서버가 `EGW00201`을 계속 반환하면 무한 대기.
7. **커버리지 협소** — KIS OpenAPI 중 주식 현물만. 파생/채권/ELW 사용자는 이 라이브러리를 쓸 수 없음.
8. **문서-코드 드리프트** — §11.

### 9.2 open-trading-api

**장점**

1. **폭이 절대적** — 334함수 / 377 TR ID. 국내 증권 API 래퍼 중 이 커버리지를 가진 서드파티는 없습니다.
2. **KIS 공식 문서와 1:1 매핑** — 함수 헤더마다 문서 ID 주석(`[v1_국내주식-008]`, `[실시간-003]`), 폴더명은 URL 경로에서 기계적 파생. 문서↔코드 왕복이 즉시 가능.
3. **공식 저장소 = 신규 시장 대응이 빠름** — NXT/대체거래소 대응이 `ccnl_krx` / `ccnl_nxt` / `ccnl_total` 3종 분리로 이미 반영.
4. **LLM 친화가 명시적 설계 목표** — `llms.txt`, 폴더당 원자적 2파일, `docs/convention.md`의 "1용어 1단어" 규칙. 모든 파라미터에 한국어 설명+예시값 인라인 주석. `COLUMN_MAPPING`이 필드 사전 역할.
5. **실무 디테일 내장** — 토큰 파일 캐시(발급 제한/알림톡 회피), 모의 TR 자동 V-치환, 연속조회 depth 가드, AES 복호화, PINGPONG.

**단점**

1. **대규모 복붙** — `examples_llm` ↔ `examples_user` 완전 중복, `kis_auth.py`가 저장소에 **6벌**. 단일 파일 13,463줄.
2. **패키징 부재** — `pyproject.toml`에 패키지 구조 없음, 전 파일이 `sys.path.extend(['../..','.'])` + `from ... import *`. pip 설치 불가, 설정 경로 `~/KIS/config/` 하드코딩.
3. **테스트 0개** — `chk_*.py`는 실계좌 필요한 수동 스크립트.
4. **전역 가변 상태** — `_base_headers`/`_TRENV`/`open_map`/`data_map` mutate → 멀티계정·멀티환경·스레드 안전성 없음.
5. **타입 계약 부실** — 파라미터 전부 `str`(수량·가격 포함), 반환은 `DataFrame` 또는 1~4-tuple 제각각(274 함수 중 `Optional[DataFrame]` 108 / `DataFrame` 72 / 2-tuple 86 / 3-tuple 6 / 4-tuple 1). **실패도 빈 DataFrame** → 성공한 빈 결과와 구분 불가.
6. **확인된 버그들** — `_smartSleep` global 누락(레이트리밋 설정 무효), `reAuth`의 `.seconds` vs `.total_seconds()`, `unsubscribe` await 누락, WS 구독 상한 검사 부정확, `amx_retries` 오타 필드.
7. **`*_examples.py`가 import만 해도 실전 주문까지 즉시 실행** — 모듈 최상위 레벨 호출.

### 9.3 언제 무엇을 쓸 것인가

| 상황 | 권장 |
|---|---|
| 국내/해외 **주식 현물** 자동매매 봇, 실시간 스트리밍, 장기 운영 | **vm-stock-kis** |
| 선물옵션·채권·ELW·조건검색·순위분석 필요 | **open-trading-api** (vmkis에 없음) |
| 프로덕션 서비스, 멀티계정, 타입 안전성, CI 테스트 | **vm-stock-kis** |
| API 스펙 확인·프로토타이핑·LLM 코드 생성 소스 | **open-trading-api** |
| 둘 다 필요 | vm-stock-kis 사용 + 미커버 TR은 `kis.fetch()` escape hatch(§10)로 호출 |

---

## 10. 미지원 API를 추가/호출하는 방법

vm-stock-kis에는 **3단계 확장 경로**가 있습니다. 대부분의 사용자는 Level 0~1로 충분합니다.

### Level 0 — 라이브러리 수정 없이 임의 TR 호출 (5줄)

`VmKis.fetch()`가 1급 escape hatch입니다 (`src/vmkis/kis.py:601-618`, 시그니처 직접 확인):

```python
def fetch(self, path, *, method="GET", params=None, body=None, form=None,
          headers=None, domain=None,               # "real" | "virtual"
          appkey_location="header", form_location=None, auth=True,
          api: str | None = None,                  # ← TR_ID → headers["tr_id"] (kis.py:623)
          continuous: bool = False,                # ← tr_cont="N" (kis.py:629)
          response_type=KisDynamicDict,            # ← 기본: 동적 dict
          verbose: bool = True) -> TDynamic
```

**바로 쓸 수 있는 예제 — 미커버 TR `HHDFS00000300`:**

```python
from vmkis import VmKis

kis = VmKis("vmkis_auth.json", keep_token=True)

res = kis.fetch(
    "/uapi/overseas-price/v1/quotations/price",
    api="HHDFS00000300",
    params={"AUTH": "", "EXCD": "NAS", "SYMB": "AAPL"},
    domain="real",            # 시세 TR은 모의 서버에 없음 → 명시 필수
)

print(res.rt_cd, res.msg1)    # ⚠ 자동 예외 없음 — 직접 확인 필요
print(res.output.last)        # 현재가 (문자열 그대로)
raw: dict = res.raw()         # 순수 dict (responses/dynamic.py:174-182)
```

**이 방식으로 자동으로 얻는 것**: appkey/토큰 주입·자동 갱신, 도메인 라우팅, Rate Limiting, `EGW00201`/`EGW00123` 자동 재시도, HTTP 오류 → `KisHTTPError`.

**주의 3가지**

- `KisDynamicDict`는 `__transform__` 단축 경로를 타서 `KisResponse.__pre_init__`의 `rt_cd` 검사(`responses/response.py:80-86`)를 **건너뜁니다.** 업무 오류를 직접 확인해야 합니다.
- 값이 전부 문자열 → `Decimal(...)` 수동 캐스팅 필요.
- 페이지네이션은 `continuous=True`(`tr_cont: "N"`)와 커서를 직접 관리해야 합니다.

한 단계 낮은 seam인 `VmKis.request()`(`kis.py:510`)는 raw `requests.Response`를 반환합니다.

**참고**: 라이브러리 내부도 정확히 이 패턴을 씁니다 — `api/stock/info.py:311-320`이 `HHDFS00000300`을 `response_type` 없이 호출합니다.

### Level 1 — 타입드 응답만 정의 (30~60 LOC, 라이브러리 밖 사용자 코드)

```python
from decimal import Decimal
from vmkis import VmKis
from vmkis.responses.response import KisAPIResponse      # __path__="output" 포함
from vmkis.responses.types import KisDecimal, KisInt, KisString


class KisForeignPrice(KisAPIResponse):
    """해외주식 현재체결가 [v1_해외주식-009] (HHDFS00000300)"""
    __ignore_missing__ = True          # KIS가 필드를 추가/누락해도 안전

    symbol: str = KisString["rsym"]
    decimal_places: int = KisInt["zdiv"]
    prev_price: Decimal = KisDecimal["base"]
    price: Decimal = KisDecimal["last"]
    change: Decimal = KisDecimal["diff"]
    rate: Decimal = KisDecimal["rate"]
    volume: int = KisInt["tvol"]
    orderable: str | None = KisString["ordy", None]      # 기본값 지정


def foreign_price(kis: VmKis, exchange: str, symbol: str) -> KisForeignPrice:
    return kis.fetch("/uapi/overseas-price/v1/quotations/price",
                     api="HHDFS00000300",
                     params={"AUTH": "", "EXCD": exchange, "SYMB": symbol},
                     response_type=KisForeignPrice,
                     domain="real")

p = foreign_price(VmKis("vmkis_auth.json"), "NAS", "AAPL")
print(p.price, p.rate)     # Decimal, Decimal
```

**사용 가능한 재료** (전부 실존 확인)

- 베이스: `KisResponse`(`response.py:69`, rt_cd 검사) / `KisAPIResponse`(`:99`, `__path__="output"`) / `KisPaginationAPIResponse`(`:130`, `page_status`·`next_page` 자동)
- 필드 디스크립터(`responses/types.py`): `KisString`(:69) `KisInt`(:79) `KisDecimal`(:110) `KisBool`(:123) `KisDate`(:144) `KisTime`(:167) `KisDatetime`(:190) `KisAny(fn)`(:58) — 금액에 `KisFloat` 사용 금지(:92 주석)
- 컨테이너: `KisList(ItemType)["output2"]`(`dynamic.py:204`), `KisTransform(...)`(`:193`)
- 문법: `KisDecimal["field"]` / `KisString["field", None]`(기본값) / `KisString()("field", absolute=True)`(`__path__` 무시)
- 클래스 옵션: `__path__`, `__ignore_missing__`

**Level 1에서 자동으로 얻는 것**: `rt_cd` → `KisAPIError`, 타입 변환·`Decimal` 정규화, 빈값 → nullable이면 `None`, `.raw()`, `__message__`.

생성자 인자가 필요하면 **인스턴스**를 넘깁니다 — `response_type=KisForeignPrice(symbol=...)` (`quote.py:641-651`의 `KisDomesticQuote(symbol, "KRX")` 패턴).

### Level 2 — 라이브러리 1급 시민으로 통합 (250~800 LOC)

이 코드베이스는 **Protocol(추상) / impl(구체) 분리**를 일관되게 씁니다:
`KisQuote`(Protocol) ↔ `KisQuoteBase`(공통) ↔ `KisDomesticQuote`/`KisForeignQuote`(TR별) ↔ `KisQuoteResponse`(Protocol+응답).

| Step | 파일 | 작업 | LOC |
|---|---|---|---|
| 1 | `src/vmkis/api/{stock,account}/<feature>.py` 신설 | Protocol → `@kis_repr` 클래스 → Base → 국내/해외 impl(`KisType` 필드) → `domestic_*`/`foreign_*`/`*` 함수 3층 → `product_*`/`account_*` scope 바인딩 wrapper | **150~800** |
| 2 | `src/vmkis/adapter/{product,account,account_product}/<feature>.py` | Protocol(docstring 통째 복제) + Mixin(`from ... import product_x as x` 1줄) | 50~240 |
| 3 | `src/vmkis/scope/{stock,account}.py` | Protocol 합성 클래스와 구현 클래스 MRO에 각각 추가 | 2~3 |
| 4 | `public_types.py` + `__init__.py` | `Foo: TypeAlias = _KisFooResponse` + `__all__` 2곳 | 4~6 |
| 5 | `tests/unit/...` | hermetic 단위 테스트(`test_info_quote.py` 패턴) + `VMKIS_RUN_REAL=1` 게이트 통합 테스트(`test_product_quote.py:20-40` 패턴) | 50~150 |
| 6 | docstring + `scripts/generate_api_reference.py` 재생성 + `CHANGELOG.md` | `국내주식시세 -> XXX[v1_국내주식-NNN]` + `(업데이트 날짜:)` 표기 관례 | — |

**실측 견적**: 단일 시장 신규 TR 1개 → **250~400 LOC**. 국내+해외 통합 → **500~800 LOC**. 그중 절반 이상이 Protocol/overload/docstring 중복입니다.

페이지네이션 API면 `KisPaginationAPIResponse` 상속 + `form=[account, page]`, `continuous=not page.is_first`, `result.is_last`/`next_page` while 루프 — `balance.py:934-967`이 정본.

### Level 3 — WebSocket 신규 실시간 이벤트

수신 경로: `_on_message`(`client/websocket.py:434`) → `_handle_event`(`:522`, `암호화|TRID|건수|본문` 파싱 + AES 복호화 `:533-544`) → **`WEBSOCKET_RESPONSES_MAP[tr_id]` 조회(`:546`)** → `KisWebsocketResponse.parse`(`^` 분할, `__fields__` 위치 매핑) → `kis_object_init` → 이벤트 필터 체인 → 콜백.

1. **응답 클래스** — `src/vmkis/api/websocket/<feature>.py`:

   ```python
   class KisDomesticRealtimeExpectedPrice(KisWebsocketResponse, KisRealtimeXxxBase):
       __fields__ = [                 # "^" 분리 순서 그대로, 미사용 필드는 None
           KisString["symbol"],       # 0 MKSC_SHRN_ISCD
           None,                      # 1 미사용
           KisDecimal["price"],       # 2 ...
       ]
       symbol: str
       price: Decimal
       def __pre_init__(self, data: list[str]): ...   # 복합 필드 조합 (price.py:577-587)
   ```

2. **레지스트리 등록 (필수 1줄)** — `src/vmkis/api/websocket/__init__.py`의 `WEBSOCKET_RESPONSES_MAP`에 추가.
   ⚠ **이게 없으면 구독 메시지는 전송되지만 수신 이벤트가 조용히 버려집니다** (`client/websocket.py:546-548`, `"RTC No response type"` 경고만). 직접 확인 완료.
3. **`on_xxx` / `on_product_xxx` 함수** — `KisProductEventFilter` + `client.on(id=TR, key=symbol, ...)` (`price.py:743-782` 패턴)
4. **adapter 확장** — `adapter/websocket/price.py:203-244`의 `on()` 문자열 분기에 `elif event == "...":` 추가 + Protocol/Mixin 양쪽 `@overload` (여기가 보일러플레이트 최대 지점 — 331줄 중 ~280줄이 overload/docstring)
5. **암호화 TR인 경우** — `client/websocket.py:513`의 하드코딩된 튜플 `("H0STCNI0","H0STCNI9","H0GSCNI0","H0GSCNI9")`도 수정 필요할 수 있음.

**Level 0 우회**: `WEBSOCKET_RESPONSES_MAP`은 dict 객체 자체가 import되므로 제자리 mutation(monkeypatch)이 유효합니다. 공식 API는 아니지만 라이브러리 수정 없이 신규 실시간 TR을 붙일 수 있는 유일한 경로입니다.

### 함정과 제약 (실무 체크리스트)

| # | 함정 | 상세 |
|---|---|---|
| 1 | **도메인 라우팅 기본값** | `fetch(domain=None)`은 `kis.virtual`이면 **모의 도메인**으로 감(`kis.py:535-536`). 시세 TR은 모의 서버에 없어 라이브러리 내 모든 시세 호출이 `domain="real"` 명시(`quote.py:651,701`). 빠뜨리면 **모의 계정에서만 터지는 버그** |
| 2 | **모의 미지원 TR** | `TTTC8715R`(기간손익), `TTTS3039R`(해외 기간손익), `TTTC8036R`(국내 미체결)은 V-변형 없음. 반대로 잔고/주문류는 `"VT..." if virtual else "TT..."` 분기 필수 |
| 3 | **빈 값 → `KisNoneValueError`** | KIS는 값 없으면 `""` → `KisInt/KisDecimal/KisDate`가 `KisNoneValueError`(`types.py:87,118`) → 어노테이션이 `\| None`이면 `None`, 아니면 `ValueError`(`dynamic.py:326-340`) |
| 4 | **필드 자체 누락 → `KeyError`** | `dynamic.py:311-315`. 해결책은 `KisString["field", None]` 또는 `__ignore_missing__ = True`. 실사례: 종목 `002170`의 `bstp_kor_isnm` 누락(`tests/unit/test_product_quote.py:46-48`) |
| 5 | **`KisDynamicDict`는 rt_cd 검사 안 함** | Level 0에서 업무 오류가 조용히 통과 |
| 6 | **페이지 커서 길이** | API마다 `ctx_area_fk100` vs `fk200` — `page.to(100)`/`.to(200)`을 맞춰야 함(`balance.py:931` vs `:996`) |
| 7 | **Rate limit 티어 없음** | 도메인당 전역 19/s·2/s. TR별 세분화 없음. `EGW00201` 시 **상한 없는 재시도 루프** |
| 8 | **캐시는 opt-in** | `kis.cache`는 자동 아님. 정적 데이터만 수동 캐시(`info.py:362,391`, `trading_hours.py:175,212`) |
| 9 | **`kis.stock()`이 API 2회+ 호출** | scope 생성 시 `info()` → 시장 판별 루프가 시장별 시세 TR 순차 호출(`info.py:294-330`). 신규 상품군(선물옵션 등)은 `MARKET_TYPE`/`MARKET_TYPE_MAP`(`api/stock/market.py`, `info.py:250-262`)에 시장 코드 추가 필요 — **숨은 비용** |
| 10 | **WS 티켓 GC** | 구독 티켓을 변수에 안 잡으면 즉시 해지될 수 있음(`websocket.py:287-298,334-337`) |
| 11 | **네이밍 관례 문서 부재** | `CLAUDE.md`가 참조하는 `docs/guidelines/CODING_STANDARDS.md`, `GIT_WORKFLOW.md`, `DOCUMENTATION_RULES.md`가 **실제로 존재하지 않음**(직접 확인). 관례는 기존 코드에서 역추출해야 함 |
| 12 | **hashkey 미구현** | KIS의 선택적 hashkey 헤더는 이 라이브러리가 쓰지 않음 — 신규 주문 TR에도 불필요 |

### 공식 샘플에서의 동일 작업 비용 (비교)

| 방식 | 비용 |
|---|---|
| 1회성 호출 | `ka._url_fetch("/uapi/...", "TRID", "", {...})` + `isOK()` + `DataFrame` — **4~6줄** |
| 컨벤션 준수 기여 | `examples_llm/<seg>/<name>/<name>.py`(80~230줄) + `chk_<name>.py`(100~150줄) + `examples_user/<seg>_functions.py`에 **동일 코드 재복사** + `_examples.py` 호출 1건 → **4개 지점, 200~400줄** |

> **비교 요약**: 1회성 호출은 두 저장소가 비슷합니다(vmkis 5줄 vs 공식 5줄). 차이는 **타입드 통합** 지점에서 벌어집니다 — vmkis Level 1은 30~60줄로 타입 안전한 결과를 얻지만, Level 2 정식 통합은 250~800줄로 공식 샘플의 정식 기여(200~400줄)보다 오히려 비쌉니다. 다만 vmkis Level 2의 산출물은 국내/해외 통합 인터페이스 + 테스트 + IDE 자동완성을 포함합니다.

---

## 11. 문서-코드 드리프트 (수정 필요 항목)

분석 중 발견한 **기존 문서의 부정확한 서술**입니다. 별도 수정 작업을 권장합니다.

| # | 문서 | 서술 | 실제 |
|---|---|---|---|
| 1 | `docs/architecture/ARCHITECTURE.md` 계층 다이어그램 | `API → Client → Response Transform → Utility` 하향 단방향 | **역방향 의존 7건 실재** (§4.3, 판정은 §5) |
| 2 | `ARCHITECTURE.md` Rate Limiting | "실전 초당 19개, 모의 **초당 1개**" | `__env__.py:19` — 모의 **2/s** |
| 3 | `ARCHITECTURE.md` 모듈 구조 | `src/vmkis/types.py`를 "공개 타입 정의"로 표기 | 실제로는 **고급 사용자용 100개 export** (공개 표면은 `public_types.py` 8개) |
| 4 | `ARCHITECTURE.md` 확장성 | 4단계 요약 | 실제 Level 2는 6단계 250~800 LOC (§10) |
| 5 | `docs/reports/ARCHITECTURE_QUALITY_KR.md` | `pykis/api/stock/order.py` 등 인용 | **존재하지 않는 경로** — 업스트림 python-kis 문서 잔재. 복잡도/커버리지 수치 신뢰 불가 |
| 6 | `CLAUDE.md` 문서 체계 | `docs/guidelines/CODING_STANDARDS.md`, `GIT_WORKFLOW.md`, `DOCUMENTATION_RULES.md` | **3개 모두 부재** (`docs/guidelines/`에는 다른 10개 파일만 존재) |
| 7 | `ARCHITECTURE.md` 확장성 | WebSocket 이벤트 추가 4단계 | `WEBSOCKET_RESPONSES_MAP` 등록 누락 시 **이벤트가 조용히 drop**되는 필수 단계 미기재 |

**검증된 문서 주장**: 공개 API 축소(154 → 12+8), 완벽한 재연결 복구(구독·암호키 재수립 확인), Thread-safe 구현, 국내/해외 통합 인터페이스 — 모두 코드로 확인됩니다.

---

## 12. 아키텍처 개선 권장안

수백 개 미커버 엔드포인트에 대응하려면 **Level 2 비용(250~800 LOC)을 낮추는 것**이 핵심입니다. 우선순위 순:

### P0 — 즉시, 저비용

1. **Level 1을 공식 문서화** (문서 1편)
   `fetch(api=..., response_type=...)`는 이미 완성도 높은 **typed escape hatch**인데 사용자 문서 어디에도 없습니다. "미지원 TR 호출 가이드" 하나로 "선물옵션 지원해주세요" 류 이슈의 상당수를 흡수할 수 있습니다. 내부 선례: `api/stock/info.py:311-320`.

2. **문서-코드 드리프트 수정** (§11의 7건)

### P1 — 구조 개선, 중비용

1. **선언적 엔드포인트 스펙 + 범용 실행기**

   ```python
   @dataclass(frozen=True)
   class KisEndpoint:
       path: str
       tr_real: str
       tr_virtual: str | None = None
       method: Literal["GET", "POST"] = "GET"
       domain_override: Literal["real"] | None = None
       page_size: Literal[100, 200] | None = None
   ```

   `kis.call(FOREIGN_PRICE, params={...}, response_type=T)`가 산재한 환경 분기 — **REST TR ID 9곳**(`balance.py:937` 등), **웹소켓 TR ID 2곳**, **파라미터 값 2곳**, **`domain="real"` 강제 10곳**(실측) — 과 `continuous` 처리를 일원화. 이미 `DOMESTIC_ORDER_API_CODES`(`order.py:894`), `FOREIGN_ORDER_API_CODES`(`:1123`)가 이 방향의 반쪽입니다.

#### 📘 입문자용 해설 — "선언적 스펙 + 범용 실행기"란 무엇인가

**(1) 용어 두 개**

- **명령적(imperative)** = *"어떻게 할지"*를 매번 코드로 적는 방식
- **선언적(declarative)** = *"무엇인지"*만 데이터로 적어두고, 실행은 공통 코드에 맡기는 방식

```python
# 명령적                          # 선언적
물을_받는다(550)                   신라면 = 레시피(물=550, 시간=4.5)
불을_켠다()                        끓이기(신라면)   # ← 실행 방법은 '끓이기'가 안다
끓을_때까지_기다린다()              끓이기(진라면)
면을_넣는다()
```

레시피는 **데이터**, `끓이기`가 **범용 실행기(generic executor)** 입니다. 라면이 100종이어도 끓이는 코드는 하나뿐입니다. 파이썬에서 이미 익숙한 예로는 `argparse`가 있습니다 — `parser.add_argument("--verbose", type=bool)`로 **선언만** 하면 실제 파싱은 argparse가 담당합니다.

**(2) 지금 이 프로젝트가 명령적인 지점**

KIS는 같은 기능이라도 실전/모의의 TR ID가 다릅니다(잔고: 실전 `TTTC8434R` / 모의 `VTTC8434R`). 그래서 이런 줄이 흩어져 있습니다 (실측):

| 분기 종류 | 흩어진 곳 | 예시 |
|---|---|---|
| REST TR ID 분기 | **9곳** | `api="VTTC8434R" if self.virtual else "TTTC8434R"` (`balance.py:937`) |
| 웹소켓 TR ID 분기 | **2곳** | `id="H0STCNI9" if self.kis.virtual else "H0STCNI0"` (`order_execution.py:524`) |
| 파라미터 **값** 분기 | **2곳** | `"PDNO": "" if self.virtual else "%"` (`daily_order.py:756`) |
| `domain="real"` 강제 | **10곳** | 시세 TR은 모의 서버에 없어 매번 명시 |

문제는 줄 수가 아니라 **실수할 기회**입니다. 신규 엔드포인트 작성자가 이 규칙들을 매번 기억해야 하고, `domain="real"`을 빠뜨리면 **모의 계정에서만 터지는 버그**가 됩니다(§10 함정 #1). 지원 TR 목록을 알려면 코드를 grep해야 합니다.

**(3) 이미 절반은 하고 있습니다**

`api/account/order.py:894`의 주문 계열은 이미 표(데이터)로 분리되어 있습니다:

```python
DOMESTIC_ORDER_API_CODES: dict[tuple[bool, ORDER_TYPE], str] = {
    # (실전투자여부, 주문종류): API코드
    (True,  "buy"):  "TTTC0802U",
    (True,  "sell"): "TTTC0801U",
    (False, "buy"):  "VTTC0802U",
    (False, "sell"): "VTTC0801U",
}
```

`FOREIGN_ORDER_API_CODES`(`:1123`)는 (실전여부, 시장, 매수/매도) 3중 키로 6개국을 담습니다. **이것이 바로 선언적 스펙**이며, 제안은 이 방식을 주문 밖으로 넓히자는 것입니다.

**(4) 스펙 코드 읽는 법 — `@dataclass` 문법**

| 문법 | 뜻 |
|---|---|
| `@dataclass` | `__init__`/`__repr__`/`__eq__`를 자동 생성하는 데코레이터 |
| `frozen=True` | **읽기 전용**. `spec.path = ...` 시 에러 — 스펙은 상수여야 하므로 |
| `tr_virtual: str \| None = None` | 기본값 `None` → **모의투자 미지원 TR**은 생략만 하면 됨 |
| `Literal["GET", "POST"]` | 두 값만 허용. 오타를 타입 검사기가 잡음 |

선언 예시:

```python
DOMESTIC_BALANCE = KisEndpoint(              # 실전/모의 둘 다 존재
    path="/uapi/domestic-stock/v1/trading/inquire-balance",
    tr_real="TTTC8434R", tr_virtual="VTTC8434R", page_size=100,
)

DOMESTIC_QUOTE = KisEndpoint(                # 모의 서버에 없음 → 실전 강제
    path="/uapi/domestic-stock/v1/quotations/inquire-price",
    tr_real="FHKST01010100", domain_override="real",
)

ORDER_PROFIT = KisEndpoint(                  # 모의 미지원 (tr_virtual 생략)
    path="/uapi/domestic-stock/v1/trading/inquire-period-trade-profit",
    tr_real="TTTC8715R", domain_override="real",
)
```

**(5) 범용 실행기 — 규칙을 한 곳에 모으는 함수**

```python
class VmKis:
    def call(self, ep: KisEndpoint, *, params=None, body=None,
             response_type=KisDynamicDict, page=None, **kw):
        # 규칙 ①: 모의 계좌인데 모의 TR이 없으면 → 실전 도메인으로
        if self.virtual and ep.tr_virtual is None:
            tr_id, domain = ep.tr_real, "real"
        elif self.virtual:
            tr_id, domain = ep.tr_virtual, "virtual"
        else:
            tr_id, domain = ep.tr_real, "real"

        # 규칙 ②: 실전 강제 지정이 있으면 덮어씀
        if ep.domain_override:
            domain = ep.domain_override

        # 규칙 ③: 페이징 커서 길이 자동 적용
        form = [page.to(ep.page_size)] if page and ep.page_size else None

        return self.fetch(ep.path, api=tr_id, method=ep.method,
                          params=params, body=body, domain=domain, form=form,
                          response_type=response_type,
                          continuous=bool(page and not page.is_first), **kw)
```

**(6) Before / After**

```python
# ───── 지금 (명령적) ─────
def domestic_balance(self, account, page=None):
    page = (page or KisPage.first()).to(100)                      # 커서 길이를 손으로
    return self.fetch(
        "/uapi/domestic-stock/v1/trading/inquire-balance",
        api="VTTC8434R" if self.virtual else "TTTC8434R",         # 분기를 손으로
        params={...}, form=[account, page],
        continuous=not page.is_first,                             # 연속조회를 손으로
        response_type=KisDomesticBalance(account_number=account),
    )

# ───── 개선 후 (선언적) ─────
def domestic_balance(self, account, page=None):
    return self.call(
        DOMESTIC_BALANCE,                                          # 스펙만 지정
        params={...}, form=[account], page=page,
        response_type=KisDomesticBalance(account_number=account),
    )
```

**(7) 얻는 것**

| 항목 | 설명 |
|---|---|
| 규칙의 단일화 | 모의 분기·실전 강제·커서 길이가 `call()` **한 곳**에만 존재 |
| 버그 예방 | `domain="real"` 누락 같은 실수가 구조적으로 불가능 |
| 자기 문서화 | `endpoints.py` 하나로 지원 TR 전체가 보임 (지금은 grep 필요) |
| 테스트 용이 | 스펙은 데이터라 네트워크 없이 검증 — `assert DOMESTIC_QUOTE.domain_override == "real"` |
| **자동 생성 가능** | **§13과 직결.** 생성기가 "함수 로직"을 짜기는 어렵지만 `KisEndpoint(...)` **데이터를 찍어내기는 쉽습니다.** 공식 샘플에서 추출한 274개를 이 형태로 생성하면 됩니다 |

**(8) 단점 — 공정하게**

- 간접 계층이 하나 늘어 코드를 읽을 때 스펙 정의부로 한 번 더 이동해야 합니다.
- **불규칙한 엔드포인트를 억지로 밀어 넣으면 역효과**입니다. `daily_order.py:756`의 `"PDNO": "" if self.virtual else "%"`처럼 **파라미터 값 자체가 환경별로 다른** 경우는 스펙으로 표현하기 어려우니 함수 안에 두는 편이 낫습니다.
- 스펙 필드를 잘못 설계하면 전면 수정이 필요하므로, **이미 표로 정리된 주문 계열부터 이관**해 필드 목록을 검증하는 것이 안전합니다.

> **한 줄 요약**: *"어떻게 호출할지"를 함수마다 반복하는 대신, "이 API는 이런 것"을 데이터로 한 번 적고, 그 데이터를 읽어 실행하는 함수를 하나만 만드는 것.*

1. **페이지네이션 제네릭 헬퍼**
   `balance.py`, `daily_order.py`, `order_profit.py`, `pending_order.py`가 **동일 while 루프를 각자 구현**. `kis.fetch_pages(...)` 하나로 API당 ~30 LOC 절감.

2. **WebSocket 자기등록 데코레이터**
   중앙 맵(`api/websocket/__init__.py:13`) 대신 `@realtime_response("H0STANC0")` 클래스 데코레이터 + `__keyless__` 클래스 속성으로 `client/websocket.py:513`의 하드코딩 튜플 제거.
   → **부수 효과: `client → api` 역방향 의존(§4.3-a) 해소** 및 서드파티 플러그인 확장 가능.

3. **Protocol/Mixin 중복 축소 — Tier 문서화**
   신규 엔드포인트에 국내/해외 통합이 필요할 때만 Protocol을 요구하고, 단일 시장 TR은 "impl 클래스 + 모듈 함수"(Level 1 산출물)를 그대로 1급으로 승격. `adapter/websocket/price.py`의 4중 overload(331줄 중 ~280줄)는 **이벤트명 → 함수 레지스트리 dict**로 대체 가능(런타임은 이미 문자열 분기 `:221-244`).

### P2 — 대규모, 고비용

1. **KIS 스펙 → 응답 클래스 codegen**
   KIS 포털의 필드 테이블(항목명/한글명/타입/길이)은 `KisDecimal["stck_prpr"]` 매핑으로 기계 변환 가능합니다. `scripts/generate_api_reference.py`처럼 `scripts/`에 생성기를 두고 산출물을 `api/generated/`에 커밋(사람은 파생 속성·`__pre_init__`만 추가하는 부분 클래스 방식).
   **스펙 소스**: 이 개발 환경에 연결된 `kis-code-assistant` MCP(`search_domestic_stock_api`, `search_domestic_futureoption_api` 등)와 `../open-trading-api/examples_llm/`의 334개 함수 + `COLUMN_MAPPING`이 그대로 기계 판독 가능한 스펙 소스입니다. **공식 샘플을 경쟁자가 아니라 codegen 입력으로 쓰는 것이 가장 현실적인 커버리지 확대 경로입니다.**
   → 이 방안의 타당성은 **§13에서 실측 검증**했습니다(파싱률 98.9%, 벤더링은 라이선스 부재로 기각).

2. **버그 수정 2건**
   - `kis.py:560-599` `while True`에 재시도 상한/백오프 추가
   - `KisNotFoundError` 이름 충돌 해소 (`responses/exceptions.py:13` → `KisResultNotFoundError` 등으로 개명 + deprecation alias)

---

## 13. 검토: 공식 샘플 함수를 하부 레이어로 흡수할 수 있는가

> **검토 요청**: "open-trading-api의 함수 구조를 하부 구조(레이어)로 가져와서 클래스로 모듈화하여 사용하기 쉽게 만들 가능성이 있을까?"

### 13.0 결론 먼저

**가능합니다. 단, 전략 A(런타임 재사용/벤더링)는 기각하고 전략 B(코드 생성)를 채택해야 합니다.**

근거 두 가지가 결정적입니다.

1. 공식 저장소에는 **라이선스 파일이 없어** 코드 벤더링·재배포가 법적으로 불가합니다 (직접 확인: `open-trading-api/`에 LICENSE/COPYING 부재, upstream `koreainvestment/open-trading-api`의 GitHub 라이선스 필드도 `null`).
2. 실측 결과 `examples_llm/`은 REST API 기준 **274개 중 271개(98.9%)가 AST로 기계 파싱**되는 사실상의 기계 판독 스펙입니다. 사실(URL·TR ID·파라미터명·필드명)만 추출해 vmkis 네이티브 코드를 생성하는 데 아무 장애가 없습니다.

### 13.1 전략 A — 런타임 재사용 평가

#### A-1. 그대로 import되는가? → **안 됩니다**

모든 엔드포인트 모듈이 첫 줄에서 `sys.path.extend(['../..', '.'])` 후 `import kis_auth as ka`를 실행합니다(`examples_llm/domestic_stock/volume_rank/volume_rank.py:10-11`). 그런데 `kis_auth.py`는 **import 시점에**:

- `~/KIS/config/KIS{YYYYMMDD}` 토큰 파일을 **생성**하고 (`kis_auth.py:39-45`)
- `~/KIS/config/kis_devlp.yaml`을 로드하며, 파일이 없으면 **import 자체가 `FileNotFoundError`로 실패**합니다 (`kis_auth.py:49-50`).

추가로 `sys.path.extend`가 호스트 앱의 sys.path를 오염시키고, `chk_*.py`는 `from volume_rank import volume_rank`처럼 **평면 최상위 import**를 쓰는데 세그먼트 간 중복 모듈명이 20개 이상입니다(`inquire_balance`, `inquire_price`, `asking_price`가 domestic_stock/domestic_futureoption/overseas_stock에 동명 존재). 패키지화 없이는 이름 충돌로 동시 사용이 불가능합니다.

#### A-2. 가짜 `kis_auth` shim은 가능한가? → **절반만**

`_url_fetch`/`getTREnv`/`smart_sleep`/`data_fetch` 표면을 흉내 내 `VmKis.fetch()`로 위임하는 shim은 스케치 가능합니다:

```python
# 개념 스케치 (shim 모듈을 sys.modules["kis_auth"]에 선주입)
class _FakeKa:
    def __init__(self, kis: VmKis):
        self._kis = kis

    def _url_fetch(self, api_url, ptr_id, tr_cont, params,
                   appendHeaders=None, postFlag=False, hashFlag=True):
        raw = self._kis.fetch(
            api_url,
            method="POST" if postFlag else "GET",
            params=None if postFlag else params,
            body=params if postFlag else None,
            api=ptr_id, continuous=bool(tr_cont),
            response_type=KisDynamicDict,
        )
        return _APIRespAdapter(raw)   # isOK()/getBody().outputN/getHeader().tr_cont 재현

    def smart_sleep(self):
        pass                          # vmkis 자체 rate limiter가 대체
```

그러나 shim이 **못 메우는 것**이 많습니다.

| 못 메우는 것 | 이유 |
|---|---|
| **`_isPaper` 전역 + TR ID 자동 치환** | `_url_fetch`가 모의 모드에서 `T/J/C` 접두 TR을 `V`로 치환. vmkis는 실전/모의를 **요청 단위**(`domain=`)로 선택하므로 프로세스 전역 플래그와 근본 충돌. **멀티 계좌·실전+모의 동시 세션 표현 불가** |
| **DataFrame 반환** | 모든 함수가 `pd.DataFrame` 반환. vmkis는 pandas 의존성이 아예 없고(`pyproject.toml`), 타입드 응답 객체가 라이브러리의 핵심 가치. shim을 씌워도 결과물은 "문자열투성이 DataFrame"이라 **vmkis의 존재 이유를 스스로 부정** |
| **재귀 페이지네이션** | 각 함수가 내부에서 자기 재귀로 전 페이지를 **끝까지** 긁음(`volume_rank.py:126-133`). 페이지 단위 제어·지연 평가 불가, `print("Call Next")` 같은 stdout 부작용 동반 |
| **웹소켓 `open_map`/`data_fetch`** | 실시간 60개가 `kis_auth`의 전역 레지스트리에 결합 → vmkis의 `api/websocket`/`adapter/websocket` 계층과 **이중 구현** |

덧붙여 공식 rate limiter는 **고장 상태**입니다: `changeTREnv`에서 `global _isPaper`만 선언하고 `_smartSleep`은 선언하지 않아(`kis_auth.py:141-151`) 지역변수 대입으로 끝나고 실제로는 항상 초기값 0.1초 고정입니다. **"공식 코드를 쓰면 검증된 인프라를 얻는다"는 기대 자체가 성립하지 않습니다.**

#### A-3. 벤더링 비용

`examples_llm/` 파이썬 파일 671개, 본체만 **41,670 LOC**, chk 포함 **80,355 LOC**. 상류가 "별도 공지 없이 지속 업데이트"(README 명시)되므로 매 갱신마다 80K LOC 3-way 머지가 필요합니다.

#### A-4. 라이선스 — **게이팅 팩터**

| | 라이선스 |
|---|---|
| vm-stock-kis | **MIT** (`LICENCE:1`, `pyproject.toml`의 `license = "MIT"`) |
| open-trading-api (공식) | **없음.** LICENSE/COPYING 파일 부재, upstream GitHub 라이선스 필드 `null` |

README에는 *"고객님의 개발 부담을 줄이고자 **참고용으로 제공**되고 있습니다"*, *"샘플 코드를 활용하여 제작한 고객님의 프로그램으로 인한 손해에 대해서는 당사에서 책임지지 않습니다"* 라는 유의사항만 있고 **복제·수정·재배포 허가 문구는 없습니다.** 라이선스 없는 코드는 기본적으로 **저작권 전부 유보(all rights reserved)**이므로, 소스 파일을 MIT 저장소에 벤더링·재배포하는 것은 허용된다고 볼 근거가 없습니다. **이것 하나만으로 전략 A는 성립하지 않습니다.**

#### A-5. 전략 A 판정: **기각**

라이선스(치명), 전역 상태 충돌, DataFrame 반환, pandas 의존성 유입, 80K LOC 머지 부담. shim은 기술적으로 절반쯤 가능하지만 **만들 가치가 없습니다.**

### 13.2 전략 B — 코드 생성 평가

#### B-1. 파싱 실험 결과 (실제 수행)

AST 기반 파서를 작성해 `examples_llm/` 전체 334개 폴더에 실행했습니다. 산출물은 `parse_llm.py`(7.7KB)와 `ir.json`(549KB, 334 엔트리)로 실재합니다.

| 항목 | 수치 |
|---|---|
| 전체 API 폴더 | 334 |
| REST (모듈 레벨 `API_URL` 보유) | 274 |
| 웹소켓 구독형 (`ka.data_fetch` 사용, URL 없음) | 60 |
| **REST 중 완전 파싱 성공** (URL+tr_id+params+output 형태+COLUMN_MAPPING) | **271 / 274 (98.9%)** |
| 불규칙 사례 | `auth/auth_token`, `auth/auth_ws_token`(vmkis 자체 구현 있어 불필요), `overseas_stock/news_title`(`output` 대신 `outblock1` — 속성명 하나 추가로 해결) |
| tr_id 분기(실전/모의/매수/매도) | 25개 (`order_cash` → TTTC0011U/0012U/VTTC0011U/0012U) |
| 페이지네이션 (tr_cont 재귀) | 181개 |
| FK/NK 커서 파라미터 | 43개 — **변형 4종**: `CTX_AREA_FK100`(15), `FK200`(25), `FK`(2, `CTCA0903R` 등), `FK50`(1) |
| POST (`postFlag=True`) | 18개 |
| output 형태 분포 | `output` 149, `output1+output2` 86, `output1` 22, `output1~3` 6, `output2` 6, 기타 |
| COLUMN_MAPPING 총 응답 필드 | **7,979개** (유니크 2,801개) |

즉 **실질 파싱 성공률은 사실상 100%**(필요한 272개 중 271개 즉시 + `news_title` 1줄 수정)입니다. `examples_llm/`은 *"Generated by KIS API Generator"* 헤더가 말해주듯 **애초에 기계 생성물**이라 구조가 극도로 균질합니다. — **가설 증명 완료.**

#### B-2. 스펙이 안 주는 것: **필드 타입**

`COLUMN_MAPPING`은 필드명 → 한글 라벨만 줍니다. `NUMERIC_COLUMNS`는 334개 중 **114개 파일에서만 비어있지 않아** 보조 자료로만 쓸 수 있습니다. 이 환경의 `kis-code-assistant` MCP도 실호출해 확인한 결과 **api_name/카테고리와 GitHub 소스 URL만 반환**하고 타입 정보는 없습니다.

결국 타입은 **KIS 명명 규칙 휴리스틱 + NUMERIC_COLUMNS + 인간 리뷰**로 채웁니다. 유니크 필드명 2,801개의 접미사 분포를 실측해 만든 매핑 테이블:

| 접미사 (실측 유니크 수) | KisType |
|---|---|
| `_amt`(364) `_pbmn`(89) `_pric`(27) `_unpr`(25) `_prc`(24) `_prpr`(23) `avls`(3) | `KisDecimal` |
| `_rate`(111) `_rt`(31) `_ctrt`(19) `_per`/`_pbr`/`_eps`/`_bps` | `KisDecimal` |
| `_qty`(134) `_vol`(69) `_cnt`(21) `_stcn`(11) | `KisInt` (해외는 소수 수량 가능 → `KisDecimal`) |
| `_dt`(91) `_date`(39) | `KisDate` |
| `_hour`(11) `_time`(10) `_tm`(3) | `KisTime` |
| `_yn`(82) | `KisBool` |
| `_cd`(133) `_code`(38) `_iscd`(12) `_dvsn`(5) `_sign`(22) `_name`(82) `_isnm`(9) `_no`(9) | `KisString` |
| **미매칭 1,297 (46.3%)** | 기본 `KisString` + NUMERIC_COLUMNS 있으면 `KisDecimal` 승격 + 리뷰 |

**핵심 안전장치**: 미확정 필드를 `KisString`으로 두면 **절대 런타임 파싱 에러가 나지 않습니다.** 타입 승격은 점진적으로 하면 되므로 휴리스틱 커버리지 54%는 출발점으로 충분합니다.

#### B-3. 생성 레이어 설계

디렉터리 `src/vmkis/endpoints/<segment>/<api_name>.py`, 모든 파일 첫 줄에 `# AUTO-GENERATED from examples_llm@<upstream SHA> — DO NOT EDIT`.

**거래량순위 실제 생성 예시**:

```python
# src/vmkis/endpoints/domestic_stock/volume_rank.py  (AUTO-GENERATED)
from decimal import Decimal
from typing import TYPE_CHECKING

from ...responses.dynamic import KisDynamic, KisList
from ...responses.response import KisAPIResponse
from ...responses.types import KisDecimal, KisInt, KisString

if TYPE_CHECKING:
    from ...kis import VmKis


class KisVolumeRankItem(KisDynamic):
    name: str = KisString["hts_kor_isnm"]            # HTS 한글 종목명
    symbol: str = KisString["mksc_shrn_iscd"]        # 단축 종목코드
    rank: int = KisInt["data_rank"]                  # 데이터 순위
    price: Decimal = KisDecimal["stck_prpr"]         # 주식 현재가
    change: Decimal = KisDecimal["prdy_vrss"]        # 전일 대비
    change_rate: Decimal = KisDecimal["prdy_ctrt"]   # 전일 대비율
    volume: int = KisInt["acml_vol"]                 # 누적 거래량
    # ... COLUMN_MAPPING 19개 필드 전부, 한글 라벨은 주석으로


class KisVolumeRank(KisAPIResponse):
    __path__ = None
    items: list[KisVolumeRankItem] = KisList(KisVolumeRankItem)["output"]


def volume_rank(
    self: "VmKis", *,
    market: str = "J", belong: str = "0", target: str = "111111111",
    exclude: str = "0000000000", min_price: str = "", max_price: str = "",
    min_volume: str = "", input_iscd: str = "0000", div_cls: str = "0",
) -> KisVolumeRank:
    """거래량순위[v1_국내주식-047] (FHPST01710000)"""
    return self.fetch(
        "/uapi/domestic-stock/v1/quotations/volume-rank",
        api="FHPST01710000",
        params={
            "FID_COND_MRKT_DIV_CODE": market, "FID_COND_SCR_DIV_CODE": "20171",
            "FID_INPUT_ISCD": input_iscd, "FID_DIV_CLS_CODE": div_cls,
            "FID_BLNG_CLS_CODE": belong, "FID_TRGT_CLS_CODE": target,
            "FID_TRGT_EXLS_CLS_CODE": exclude, "FID_INPUT_PRICE_1": min_price,
            "FID_INPUT_PRICE_2": max_price, "FID_VOL_CNT": min_volume,
            "FID_INPUT_DATE_1": "",
        },
        response_type=KisVolumeRank, domain="real",
    )
```

원본의 고정값 파라미터(`fid_cond_scr_div_code="20171"` — 다른 값이면 원본이 `ValueError`를 던지는 것을 파서가 감지)는 시그니처에서 제거하고 상수로 굽습니다.

**평문 `CTX_AREA_FK` 페이지네이션**(부록 A.5에서 실증한 `KisPage` 미지원 케이스)은 생성기가 루프 기반 연속조회를 내보냅니다:

```python
def chk_holiday(self: "VmKis", *, base_date: str) -> KisHolidays:
    result, fk, nk, cont = None, "", "", False
    while True:
        page = self.fetch(
            "/uapi/domestic-stock/v1/quotations/chk-holiday",
            api="CTCA0903R", continuous=cont,
            params={"BASS_DT": base_date, "CTX_AREA_FK": fk, "CTX_AREA_NK": nk},
            response_type=KisHolidaysPage,
        )
        result = result.merge_(page) if result else page
        if page.tr_cont_ not in ("F", "M"):
            return result
        fk, nk, cont = page.ctx_area_fk, page.ctx_area_nk, True
```

별도로 `KisPage.__pre_init__`에 `ctx_area_fk`/`ctx_area_fk50` 분기를 추가하면(**4줄**) 기존 페이지네이션 프레임워크에도 합류시킬 수 있습니다.

**재생성 가능성**: 생성 파일은 절대 손대지 않고, 인간 추가분은 `src/vmkis/endpoints/_overrides/<segment>/<api_name>.py`에 서브클래스/래퍼로 둡니다. 레지스트리가 override 존재 시 그것을 우선 노출합니다.

#### B-4. 클래스 파사드 — Protocol/Mixin 세금 없이

기존 Level 2 비용(250~800 LOC)의 절반이 Protocol·overload·docstring 중복인데, 이는 **손으로 쓰기 때문에** 세금입니다. 생성 코드에서는 서브카테고리별 **네임스페이스 클래스를 통째로 생성**합니다.

```python
# src/vmkis/endpoints/domestic_stock/__init__.py  (AUTO-GENERATED)
class KisDomesticStockRanking:
    __slots__ = ("_kis",)

    def __init__(self, kis: "VmKis"):
        self._kis = kis

    def volume(self, **kwargs) -> KisVolumeRank:
        """거래량순위 (FHPST01710000)"""
        return volume_rank(self._kis, **kwargs)   # 실제로는 전체 시그니처를 그대로 생성

    def fluctuation(self, ...) -> KisFluctuationRank: ...


class KisDomesticStock:
    @cached_property
    def ranking(self) -> KisDomesticStockRanking: ...
    @cached_property
    def finance(self) -> KisDomesticStockFinance: ...
```

`VmKis`에는 생성된 진입점 하나만 추가합니다 — `kis.domestic.ranking.volume()`, `kis.overseas.quote.price(...)`.

`__getattr__` 매직 없이 **전부 실제 typed 메서드**이므로 `.pyi` 스텁 없이 IDE 자동완성·pyright가 그대로 작동합니다(생성기가 verbose한 코드를 뱉는 건 공짜입니다). Scope 통합(`kis.stock("005930").ranking.volume()`)은 2단계 — 파서가 `fid_input_iscd`/`pdno`/`cano`류 파라미터를 "scope 바인딩 가능"으로 표시해 두었으므로, 해당 인자를 자동 주입하는 변형을 추가 생성하면 됩니다.

#### B-5. 기존 74개 수기 엔드포인트와 공존

- **저수준 `endpoints/`는 겹치더라도 전부 생성** (겹침 20 TR ID 포함) — 수기 구현의 회귀 테스트 교차검증 자료로 유용합니다.
- **파사드 네임스페이스에서는 제외맵**(`OVERLAP = {"FHKST01010100": "kis.stock(...).quote", ...}`)에 있는 TR ID의 메서드를 생성하지 않고 docstring에 기존 경로를 안내합니다. → **같은 API에 공식 이름이 두 개 생기는 일 방지. 수기 구현이 항상 승리.**
- 장기적으로 수기 74개 중 단순 조회 계열은 생성판으로 역이관 가능(선택).

#### B-6. 견적

| 항목 | 규모 |
|---|---|
| 생성기 | **~1,500 LOC** (AST 파서 400 — **이미 프로토타입 완성**, 타이핑 휴리스틱 200, emitter 700, CLI+CI 200) |
| 생성물 | REST 272개 × 평균 80~120 LOC ≈ **25~30K LOC** (전부 기계 관리) |
| 인간 리뷰 | 타입 스팟체크 + read-only 자동 스모크 호출 기준 **총 40~60시간**, 세그먼트별 분산 |
| 롤아웃 순서 | domestic_stock 시세·순위·재무 → etfetn(6) → elw(24) → overseas_stock → bond(18) → futureoption → **주문·정정취소(POST 18개)는 맨 마지막, 모의투자 수동 검증 필수** |
| CI | ① `regen` 잡 — 재생성 후 `git diff --exit-code`로 생성물 드리프트 차단 ② 주간 잡 — upstream SHA 갱신 후 IR 재추출·diff → 신규/변경 API 리포트 |

웹소켓 60개는 이 생성기 범위 밖(3단계, 별도 emitter로 vmkis websocket 계층에 접합)입니다.

#### B-7. 전략 B 판정: **채택**

파싱률 98.9% 실증, 타입 갭은 안전한 기본값(`KisString`)+휴리스틱으로 관리 가능, vmkis의 `fetch()`/응답 디스크립터가 **이미 이상적인 타깃 런타임**입니다.

### 13.3 최종 권고: **B 단독 채택** (A는 코드가 아닌 "동작 참조"로만)

하이브리드라 해봐야 A의 역할은 "생성물 검증 시 공식 함수를 로컬에서 돌려 응답을 비교"하는 **개발자 로컬 절차** 정도이며, 저장소에는 공식 코드가 한 줄도 들어가지 않아야 합니다.

> **법적 주의**: 사실(URL, TR ID, 파라미터명, 필드명↔한글 라벨)은 추출해도 되지만, 원본 docstring의 **설명 문단을 verbatim 복사하는 것은 금지**합니다. 생성기는 라벨과 메타데이터로부터 **자체 docstring을 조립**해야 합니다.

**중단 조건 (이러면 접습니다)**

- KIS가 `examples_llm/` 구조를 대폭 개편해 파싱률이 급락하는 경우 (단 IR JSON은 남으므로 스냅샷 기준 유지보수는 가능)
- KIS가 스펙 사실 추출까지 명시적으로 금지하는 약관을 내는 경우
- 파일럿 스모크 테스트에서 타입 변환 실패율이 필드의 10%를 넘는 경우 (휴리스틱 재설계 신호)

**주요 리스크와 완화**

| 리스크 | 완화 |
|---|---|
| ① 타입 오판 | 미확정=`KisString`, lenient 변환 |
| ② 상류 무통보 변경 | SHA 고정 + 주간 diff |
| ③ API 표면이 갑자기 300개 늘며 생기는 문서/디프리케이션 부담 | 세그먼트별 점진 공개, `@experimental` 표기 |
| ④ 주문 계열 오생성 시 **금전 사고** | 주문은 최종 단계 + 수동 리뷰 게이트 |

**단계별 계획**

1. **파일럿 (1주)** — 생성기 v0 + 8개 엔드포인트. 이 8개가 전체 패턴 공간을 커버합니다:
   `volume_rank`(단일 output 대표) · `fluctuation`·`market_cap`(순위 계열 반복성) · `chk_holiday`(평문 FK/NK 페이지네이션 갭) · `inquire_daily_ccld`(**4-way tr_id 분기 + FK100 + output1/2 복합 — 최난도**) · `finance_balance_sheet`·`finance_income_statement`(NUMERIC_COLUMNS 활용) · `news_title`(`outblock1` 불규칙 케이스)
2. **세그먼트 확대 (2~4주)** — domestic_stock 잔여 → etfetn/elw → overseas_stock → bond/futureoption. 각 단계에서 read-only 스모크 + IR diff CI 가동
3. **파사드·Scope 통합** — 네임스페이스 공개, scope 바인딩 변형 생성, 수기 74개 제외맵 정리
4. **(선택) 웹소켓 60개** — 별도 emitter로 vmkis websocket 계층에 생성 접합

---

## 14. 결론

| 축 | 승자 | 격차 |
|---|---|---|
| **커버리지 (폭)** | open-trading-api | 377 vs 74 TR ID — **약 9배** |
| **타입 안전성** | vm-stock-kis | 압도적 (`Decimal`/`datetime` vs 전부 `str`) |
| **오류 처리** | vm-stock-kis | 예외 위계 12종 vs 빈 DataFrame |
| **동시성/멀티환경** | vm-stock-kis | 실전+모의 동시 vs 프로세스당 1환경 |
| **실시간 견고성** | vm-stock-kis | 구독복원·참조카운팅·한도강제 vs 3회 재시도·`unsubscribe` 미동작 |
| **테스트** | vm-stock-kis | 957 vs 0 |
| **패키징/배포** | vm-stock-kis | pip 설치형 vs `sys.path` 해킹 |
| **문서 추적성** | open-trading-api | KIS 문서 ID 1:1 매핑 |
| **LLM 코드 생성 소스** | open-trading-api | `llms.txt` + 원자적 2파일 구조 |
| **계층 아키텍처 순수성** | 무승부 (역설) | vmkis는 8계층이나 역방향 7건, 공식은 2계층이라 위반 자체가 불가 |

**전략적 제언**

1. vm-stock-kis는 **주식 현물 특화 고품질 라이브러리**라는 현재 포지션이 정당합니다. 공식 샘플과 폭으로 경쟁하는 것은 비현실적입니다(377 TR ID × Level 2 비용 400 LOC ≈ 15만 LOC).
2. 대신 **Level 0/1 escape hatch를 1급 기능으로 문서화**하면, "vmkis로 시작하고 미커버 TR은 `fetch()`로 뚫는다"는 실용적 사용 모델이 성립합니다. 이것이 가장 비용 대비 효과가 큰 조치입니다(P0-1).
3. 폭을 늘리려면 **손으로 쓰지 말고 `../open-trading-api/examples_llm/`을 codegen 입력으로 삼아야** 합니다(§13). 실측 파싱률 98.9%로 타당성이 증명되었고, `fetch()`와 `KisType` 디스크립터가 이미 이상적인 타깃 런타임입니다. **단 공식 코드를 저장소에 복사하는 것은 라이선스 부재로 불가**하므로, 추출 대상은 사실(URL·TR ID·파라미터명·필드명)뿐이며 docstring 설명문 복사는 금지입니다.
4. 계층 아키텍처를 문서 주장대로 만들려면 **`client → api` 역참조(WebSocket 레지스트리)부터 끊는 것**이 가장 효과적입니다(P1-5). 나머지 역방향 의존은 도메인상 불가피하거나(응답 객체가 주문 기능을 가짐) 비용 대비 효과가 낮습니다.

---

## 부록 A. `fetch()`로 주식 현물 기능 추가하기 — 실전 예제

vm-stock-kis가 아직 감싸지 않은 국내주식 현물 API는 `VmKis.fetch()`(`src/vmkis/kis.py:601`)로 직접 호출할 수 있습니다. 이 부록은 **raw 호출 → 타입 응답 → 리스트 → 연속조회 → 수동 페이징 → 실시간 → scope 통합** 순서로, 지금 바로 붙여넣어 쓸 수 있는 예제를 제공합니다. 모든 TR ID·파라미터·응답 필드명은 KIS 공식 샘플 코드에서 추출한 것입니다.

### A.0 공통 준비

```python
from datetime import date
from decimal import Decimal

from vmkis import VmKis, KisAuth

# 내부 모듈 import (공개 API는 아니지만 안정적으로 사용 가능)
from vmkis.responses.response import KisAPIResponse, KisResponse
from vmkis.responses.dynamic import KisDynamic, KisList
from vmkis.responses.types import KisString, KisInt, KisDecimal, KisBool, KisDate, KisAny

kis = VmKis("vmkis_auth.json", keep_token=True)
```

**핵심 주의 — `domain="real"`**: `fetch(domain=None)`은 `kis.virtual`이 참이면 모의 도메인으로 갑니다(`kis.py:535-536`). 이 부록의 시세·순위·재무·휴장일 TR은 **모의투자 서버에 없으므로** 모든 예제에서 `domain="real"`을 명시합니다. 실전 전용 클라이언트에서도 명시해서 손해볼 것이 없습니다.

`fetch()`의 편의 파라미터 두 개만 기억하면 됩니다.

- `api="FHPST01710000"` → 요청 헤더 `tr_id`로 들어감 (`kis.py:623`)
- `continuous=True` → 요청 헤더 `tr_cont="N"` (연속조회 2페이지 이후, `kis.py:629`)

rate limit은 `fetch()` 내부의 rate limiter와 `EGW00201`(초당 호출 초과) 자동 재시도가 처리하므로 루프에 별도 sleep을 넣을 필요가 없습니다.

### A.1 Level 0 — raw 호출: 거래량 순위 (`FHPST01710000`)

가장 빠른 방법입니다. `response_type`을 생략하면 `KisDynamicDict`가 반환되는데, 이 타입은 **`rt_cd` 검사를 하지 않으므로**(`responses/types.py:26-55`) 직접 확인해야 합니다.

```python
res = kis.fetch(
    "/uapi/domestic-stock/v1/quotations/volume-rank",
    api="FHPST01710000",
    domain="real",
    params={
        "FID_COND_MRKT_DIV_CODE": "J",      # J: KRX
        "FID_COND_SCR_DIV_CODE": "20171",   # 고정값
        "FID_INPUT_ISCD": "0000",           # 0000: 전체
        "FID_DIV_CLS_CODE": "0",            # 0: 전체
        "FID_BLNG_CLS_CODE": "0",           # 0: 평균거래량
        "FID_TRGT_CLS_CODE": "111111111",
        "FID_TRGT_EXLS_CLS_CODE": "0000000000",
        "FID_INPUT_PRICE_1": "",            # 공란: 전체 가격
        "FID_INPUT_PRICE_2": "",
        "FID_VOL_CNT": "",                  # 공란: 전체 거래량
        "FID_INPUT_DATE_1": "",
    },
)

assert int(res.rt_cd) == 0, f"API 오류: {res.msg_cd} {res.msg1}"   # 수동 확인 필수!

for row in res.output:                       # list[KisDynamicDict]
    print(row.data_rank, row.hts_kor_isnm, row.stck_prpr, row.acml_vol)
```

`KisDynamicDict.__getattr__`가 응답 JSON 키를 그대로 속성으로 노출하고, `output` 같은 리스트는 원소를 다시 `KisDynamicDict`로 감싸 반환합니다. 필드명은 KIS 문서(또는 공식 샘플의 `COLUMN_MAPPING`) 그대로입니다: `mksc_shrn_iscd`(종목코드), `prdy_ctrt`(등락률), `vol_inrt`(거래량증가율), `acml_tr_pbmn`(누적거래대금) 등.

### A.2 Level 1 — 타입 지정 단건 응답: 시간외 단일가 현재가 (`FHPST02300000`)

`KisAPIResponse`를 상속하면 (1) `rt_cd != 0`일 때 `KisAPIError`가 자동 발생하고(`responses/response.py:82-86`), (2) `__path__ = "output"`이 기본이라 필드 선언이 `output` 내부를 바로 가리킵니다(`response.py:99-102`).

```python
class KisOvertimePrice(KisAPIResponse):
    """국내주식 시간외 단일가 현재가 [국내주식-076]"""

    price: Decimal = KisDecimal["ovtm_untp_prpr"]
    """시간외 단일가 현재가"""
    change: Decimal = KisDecimal["ovtm_untp_prdy_vrss"]
    """전일 대비"""
    sign: str = KisString["ovtm_untp_prdy_vrss_sign"]
    """전일 대비 부호"""
    rate: Decimal = KisDecimal["ovtm_untp_prdy_ctrt"]
    """전일 대비율"""
    volume: int = KisInt["ovtm_untp_vol"]
    """시간외 단일가 거래량"""
    amount: Decimal = KisDecimal["ovtm_untp_tr_pbmn"]
    """시간외 단일가 거래대금"""

    # 시간외 세션 전에는 빈 문자열("")로 내려올 수 있는 필드 → 반드시 `| None`
    open: Decimal | None = KisDecimal["ovtm_untp_oprc"]
    high: Decimal | None = KisDecimal["ovtm_untp_hgpr"]
    low: Decimal | None = KisDecimal["ovtm_untp_lwpr"]
    expected_price: Decimal | None = KisDecimal["ovtm_untp_antc_cnpr"]
    """예상 체결가"""
    bid: Decimal | None = KisDecimal["bidp"]
    ask: Decimal | None = KisDecimal["askp"]


def overtime_price(kis: VmKis, symbol: str) -> KisOvertimePrice:
    return kis.fetch(
        "/uapi/domestic-stock/v1/quotations/inquire-overtime-price",
        api="FHPST02300000",
        domain="real",
        params={"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": symbol},
        response_type=KisOvertimePrice,
    )


quote = overtime_price(kis, "005930")
print(quote.price, quote.rate)
```

필드 규칙 (`responses/dynamic.py:271-340`에서 검증한 동작):

| 상황 | 결과 | 대응 |
|---|---|---|
| 응답에 있으나 **미선언** 필드 | 조용히 무시 | `quote.raw()`로 원본 확인 |
| **선언했는데 키 자체가 없음** | `KeyError` | `KisString["fld", None]` 기본값 또는 `__ignore_missing__ = True` |
| 키는 있으나 **값이 빈 문자열** | `KisNoneValueError` | 힌트가 `X \| None`이면 `None`, 아니면 `ValueError` |

### A.3 Level 1 — 타입 지정 리스트 응답: 등락률 순위 (`FHPST01700000`)

리스트 응답은 라이브러리 내부 패턴(`api/stock/daily_chart.py:84-94`)을 그대로 따릅니다: **바깥 클래스는 `KisResponse` 상속**(`__path__`가 없는 쪽)하고 `KisList(Item)["output"]`으로 리스트 키를 지정, **아이템 클래스는 평범한 `KisDynamic`** 상속.

```python
class KisFluctuationRankItem(KisDynamic):
    """등락률 순위 개별 종목"""

    rank: int = KisInt["data_rank"]
    symbol: str = KisString["stck_shrn_iscd"]
    name: str = KisString["hts_kor_isnm"]
    price: Decimal = KisDecimal["stck_prpr"]
    change: Decimal = KisDecimal["prdy_vrss"]
    sign: str = KisString["prdy_vrss_sign"]
    rate: Decimal = KisDecimal["prdy_ctrt"]
    volume: int = KisInt["acml_vol"]
    consecutive_up_days: int | None = KisInt["cnnt_ascn_dynu"]
    """연속 상승 일수"""
    period_rate: Decimal | None = KisDecimal["prd_rsfl_rate"]
    """기간 등락 비율"""


class KisFluctuationRank(KisResponse):        # KisAPIResponse 아님! (__path__ 없음)
    """등락률 순위 [v1_국내주식-088]"""

    items: list[KisFluctuationRankItem] = KisList(KisFluctuationRankItem)["output"]


def fluctuation_rank(kis: VmKis, count: int = 30, ascending: bool = False) -> KisFluctuationRank:
    return kis.fetch(
        "/uapi/domestic-stock/v1/ranking/fluctuation",
        api="FHPST01700000",
        domain="real",
        params={   # 공식 샘플의 키 표기(소문자) 그대로 사용
            "fid_cond_mrkt_div_code": "J",
            "fid_cond_scr_div_code": "20170",
            "fid_input_iscd": "0000",
            "fid_rank_sort_cls_code": "0001" if ascending else "0000",
            "fid_input_cnt_1": str(count),
            "fid_prc_cls_code": "0",
            "fid_input_price_1": "", "fid_input_price_2": "",
            "fid_vol_cnt": "",
            "fid_trgt_cls_code": "0", "fid_trgt_exls_cls_code": "0",
            "fid_div_cls_code": "0",
            "fid_rsfl_rate1": "", "fid_rsfl_rate2": "",
        },
        response_type=KisFluctuationRank,
    )


for item in fluctuation_rank(kis).items:
    print(item.rank, item.name, f"{item.rate}%")
```

**왜 `KisResponse`인가**: `KisList(...)["output"]`의 `"output"`은 최상위 JSON 기준 경로입니다. `KisAPIResponse`를 상속하면 `__path__ = "output"` 때문에 파싱 스코프가 이미 `output` 내부로 들어가 있어 키를 찾지 못합니다. 라이브러리도 같은 이유로 `KisDomesticBalance`에서 `__path__ = None`을 재정의합니다(`api/account/balance.py:579`).

> `fid_rank_sort_cls_code="0001"`(하락률순)은 KIS 문서 기준이며 공식 샘플에는 값 목록이 없으므로 사용 전 실호출로 한 번 확인하세요.

### A.4 연속조회(tr_cont)가 있는 경우: 대차대조표 (`FHKST66430100`)

이 API는 바디 커서 없이 **응답 헤더 `tr_cont`만으로** 연속조회합니다. 다음 페이지 요청은 동일 파라미터에 `continuous=True`(→ 요청 헤더 `tr_cont="N"`)만 추가하면 됩니다. 원본 `requests.Response`는 `KisResponse.__response__`로 접근합니다(`responses/response.py:71`).

```python
class KisBalanceSheetItem(KisDynamic):
    """대차대조표 (단위: 억원)"""

    period: str = KisString["stac_yymm"]              # 결산 년월
    current_assets: Decimal = KisDecimal["cras"]      # 유동자산
    fixed_assets: Decimal = KisDecimal["fxas"]        # 고정자산
    total_assets: Decimal = KisDecimal["total_aset"]  # 자산총계
    current_liabilities: Decimal = KisDecimal["flow_lblt"]
    fixed_liabilities: Decimal = KisDecimal["fix_lblt"]
    total_liabilities: Decimal = KisDecimal["total_lblt"]
    capital: Decimal = KisDecimal["cpfn"]             # 자본금
    total_equity: Decimal = KisDecimal["total_cptl"]  # 자본총계


class KisBalanceSheet(KisResponse):
    items: list[KisBalanceSheetItem] = KisList(KisBalanceSheetItem)["output"]


def balance_sheet(kis: VmKis, symbol: str, quarterly: bool = False) -> KisBalanceSheet:
    """국내주식 대차대조표 [v1_국내주식-078] (연속조회 지원)"""
    first, cont = None, False

    while True:
        result = kis.fetch(
            "/uapi/domestic-stock/v1/finance/balance-sheet",
            api="FHKST66430100",
            domain="real",
            params={   # 공식 샘플의 대소문자 혼용 표기 그대로
                "FID_DIV_CLS_CODE": "1" if quarterly else "0",  # 0: 년, 1: 분기
                "fid_cond_mrkt_div_code": "J",
                "fid_input_iscd": symbol,
            },
            continuous=cont,                 # 2페이지부터 tr_cont="N" 헤더
            response_type=KisBalanceSheet,
        )

        if first is None:
            first = result
        else:
            first.items.extend(result.items)

        # 응답 헤더 tr_cont: F/M = 다음 페이지 있음, D/E = 마지막 (client/page.py:16-22)
        tr_cont = (result.__response__.headers.get("tr_cont") or "").strip()
        if tr_cont not in ("F", "M"):
            return first
        cont = True
```

참고로 `ctx_area_fk100/200` 커서를 쓰는 표준 페이징 API라면 손으로 짤 필요 없이 `KisPaginationAPIResponse` + `KisPage`를 쓰면 됩니다 — 그 패턴은 `api/account/balance.py:931-967`(`domestic_balance`)이 교과서입니다.

### A.5 `KisPage`가 안 통하는 페이징: 국내휴장일 (`CTCA0903R`)

**함정 실증**: `KisPage.__pre_init__`(`client/page.py:47-58`)은 응답에서 `ctx_area_fk100` 또는 `ctx_area_fk200` 키만 찾고, 없으면 `ValueError("페이지 커서를 파싱할 수 없었습니다")`를 던집니다. 그런데 휴장일조회의 커서 키는 접미사 없는 **`ctx_area_fk` / `ctx_area_nk`** 입니다. 따라서 `KisPaginationAPIResponse`를 상속하면 `__pre_init__`의 `KisPage` 변환(`responses/response.py:148-160`)에서 무조건 실패합니다. `KisPage.build`(`page.py:88-97`)도 `ctx_area_fk{size}` 형태로만 폼을 만들기 때문에 요청 쪽도 못 씁니다. **커서를 수동으로 돌려야 합니다.**

```python
class KisHoliday(KisDynamic):
    date: date = KisDate["bass_dt"]
    weekday_code: str = KisString["wday_dvsn_cd"]     # 01:일 ~ 07:토
    business_day: bool = KisBool["bzdy_yn"]           # 영업일 여부
    trading_day: bool = KisBool["tr_day_yn"]          # 거래일 여부
    market_open: bool = KisBool["opnd_yn"]            # 개장일 여부
    settlement_day: bool = KisBool["sttl_day_yn"]     # 결제일 여부


class KisHolidays(KisResponse):                       # Pagination 응답 상속 금지!
    days: list[KisHoliday] = KisList(KisHoliday)["output"]
    # 커서를 일반 필드로 직접 선언 (기본값 ""로 키 부재도 방어)
    next_search: str = KisString["ctx_area_fk", ""]
    next_key: str = KisString["ctx_area_nk", ""]


def market_holidays(kis: VmKis, start: date) -> list[KisHoliday]:
    """국내휴장일조회 [국내주식-040] — 기준일 이후 영업일 정보"""
    days: list[KisHoliday] = []
    search, key, cont = "", "", False

    while True:
        result = kis.fetch(
            "/uapi/domestic-stock/v1/quotations/chk-holiday",
            api="CTCA0903R",
            domain="real",
            params={
                "BASS_DT": start.strftime("%Y%m%d"),
                "CTX_AREA_FK": search,        # 접미사 없는 커서 → KisPage 사용 불가
                "CTX_AREA_NK": key,
            },
            continuous=cont,
            response_type=KisHolidays,
        )
        days.extend(result.days)

        tr_cont = (result.__response__.headers.get("tr_cont") or "").strip()
        if tr_cont not in ("F", "M"):         # F/M = 다음 페이지 존재
            return days

        search, key, cont = result.next_search, result.next_key, True


for d in market_holidays(kis, date(2026, 8, 27))[:5]:
    print(d.date, "개장" if d.market_open else "휴장")
```

같은 요령으로 **공매도 일별추이**(`FHPST04830000`, `/uapi/domestic-stock/v1/quotations/daily-short-sale`, `output2` 리스트: `stck_bsop_date`, `ssts_cntg_qty` 공매도 체결수량, `ssts_vol_rlim` 공매도 거래량비중, `ssts_tr_pbmn` 공매도 거래대금)나 **투자자별 매매동향**(`FHKST01010900`, `output` 리스트: `prsn_ntby_qty`/`frgn_ntby_qty`/`orgn_ntby_qty`)도 A.3 패턴으로 붙일 수 있습니다.

### A.6 실시간 신규 TR: 실시간 예상체결 (`H0STANC0`)

REST와 달리 웹소켓은 **응답 클래스를 등록하지 않으면 데이터가 버려집니다.** `client/websocket.py:546-548`에서 수신 TR ID를 `WEBSOCKET_RESPONSES_MAP`에서 찾지 못하면 `"RTC No response type for %s"` 경고만 남기고 리턴하기 때문입니다. 따라서 **(1) 파싱 클래스 정의, (2) 맵 등록, (3) 구독** 세 단계가 모두 필요합니다.

```python
from vmkis.responses.websocket import KisWebsocketResponse
from vmkis.api.websocket import WEBSOCKET_RESPONSES_MAP


class KisDomesticRealtimeExpectedPrice(KisWebsocketResponse):
    """국내주식 실시간 예상체결 (KRX) [H0STANC0]"""

    # 수신 문자열을 "^"로 쪼갠 뒤 인덱스 순서대로 매핑. 관심 없는 컬럼은 None.
    # 공식 샘플(exp_ccnl_krx.py) 기준 총 45개 컬럼 — 길이가 정확히 일치해야 함!
    __fields__ = [
        KisString["symbol"],    # 0  MKSC_SHRN_ISCD 단축 종목코드
        KisString["time"],      # 1  STCK_CNTG_HOUR 체결 시간 (HHMMSS)
        KisDecimal["price"],    # 2  STCK_PRPR 예상 체결가
        None,                   # 3  PRDY_VRSS_SIGN 전일 대비 부호
        KisDecimal["change"],   # 4  PRDY_VRSS 전일 대비
        KisDecimal["rate"],     # 5  PRDY_CTRT 전일 대비율
        *([None] * 6),          # 6-11 (가중평균가, 시/고/저, 호가)
        KisInt["volume"],       # 12 CNTG_VOL 예상 체결량
        KisInt["acml_volume"],  # 13 ACML_VOL 누적 거래량
        *([None] * 31),         # 14-44 나머지 무시
    ]

    symbol: str
    time: str
    price: Decimal
    change: Decimal
    rate: Decimal
    volume: int
    acml_volume: int


# 등록 — 이 한 줄이 없으면 수신 메시지가 조용히 버려집니다.
# client/websocket.py:19가 같은 dict 객체를 import하므로 "항목 추가"는 반영되지만,
# dict 자체를 재할당(= {...})하면 반영되지 않습니다.
WEBSOCKET_RESPONSES_MAP["H0STANC0"] = KisDomesticRealtimeExpectedPrice


def on_expected_price(sender, e):
    r = e.response      # KisDomesticRealtimeExpectedPrice
    print(f"[{r.time}] {r.symbol} 예상체결가={r.price} ({r.rate}%) 예상체결량={r.volume}")


# 구독 (kis.websocket → KisWebsocketClient.on, client/websocket.py:300)
ticket = kis.websocket.on("H0STANC0", "005930", on_expected_price)
# ticket이 참조 카운트를 쥐고 있으므로 반드시 변수에 보관하세요.
# (referenced_subscribe: 카운터가 0이 되면 자동 구독 해제 — client/websocket.py:287-296)
```

주의사항:

- `__fields__` 길이는 실제 수신 컬럼 수와 **정확히** 일치해야 합니다. `KisWebsocketResponse.parse`(`responses/websocket.py:83-84`)가 `len(items) % len(fields) != 0`이면 `ValueError("Invalid data length")`를 던집니다. 45개는 공식 샘플의 컬럼 목록 기준이며, 실계좌 첫 수신 시 로그로 한 번 검증하길 권합니다(KIS가 컬럼을 추가하는 경우가 있습니다 — 예: `H0STCNT0`은 46개).
- 빈 값(`""`)이 올 수 있는 필드는 REST와 동일하게 타입 힌트를 `| None`으로 선언해야 합니다.
- 시간외 단일가 실시간체결 `H0STOUP0`도 컬럼 구성만 다를 뿐 완전히 같은 방식으로 추가합니다.

### A.7 `kis.stock()` 객체에 메서드로 붙이기

`kis.stock("005930")`은 `KisStockScope` 인스턴스를 반환합니다(`scope/stock.py:85-115`). 이 클래스는 `__slots__` 없는 평범한 클래스라서 **클래스 레벨 몽키패치가 실제로 동작합니다** (scope에는 `self.kis`, `self.symbol`이 있으므로 앞서 만든 함수를 그대로 위임하면 됩니다).

```python
from vmkis.scope.stock import KisStockScope


def _overtime_price(self) -> KisOvertimePrice:
    """시간외 단일가 현재가 (A.2의 함수 재사용)"""
    return overtime_price(self.kis, self.symbol)


KisStockScope.overtime_price = _overtime_price     # 라이브러리 수정 없이 주입

samsung = kis.stock("005930")
print(samsung.overtime_price().price)               # 동작 확인됨
```

**제약과 대안**

- **정적 타입 검사는 통과하지 못합니다.** `kis.stock()`의 반환 타입 힌트는 `KisStock` Protocol이라 mypy/pyright는 `overtime_price`를 모릅니다. IDE 지원이 필요하면 몽키패치 대신 **모듈 함수 스타일**(`overtime_price(kis, "005930")`)을 권장합니다.
- **`KisStockScope`를 상속하는 방식은 소용없습니다.** `kis.stock()`이 `KisStockScope`를 직접 생성하기 때문에(`scope/stock.py:110`) 사용자 서브클래스가 반환될 일이 없습니다. 굳이 원하면 `MyStock(kis=kis, market=s.market, symbol=s.symbol, account=kis.primary)`처럼 기존 scope의 값으로 직접 생성해야 합니다.

### A.8 체크리스트 — 새 TR을 붙이기 전에

1. **도메인**: 시세·순위·재무·휴장일 TR은 모의서버 미지원 → `domain="real"` 명시. 주문·잔고형 TR을 모의에서 쓸 때는 `api="VTTC8434R" if kis.virtual else "TTTC8434R"` 분기(`api/account/balance.py:938` 패턴).
2. **rt_cd 검사**: `KisResponse` 계열은 자동(`KisAPIError`), `KisDynamicDict`(raw)는 반드시 수동 확인.
3. **`__path__`**: 단건 `output` 응답 → `KisAPIResponse` 그대로. `KisList[...]`로 최상위 키를 직접 지정할 때 → `KisResponse` 상속(또는 `__path__ = None`).
4. **빈값 nullable**: 장 시작 전/데이터 없음 구간에 `""`로 오는 필드는 `Decimal | None` 힌트 필수.
5. **필드 누락**: 선언 필드가 응답에 없으면 `KeyError` → 기본값 `KisString["fld", None]` 또는 `__ignore_missing__ = True`(`responses/dynamic.py:271`). 반대로 미선언 필드를 로그로 보려면 `__verbose_missing__ = True`.
6. **페이징 종류 판별**: 커서 키가 `ctx_area_fk100/200`이면 `KisPaginationAPIResponse` + `KisPage`(balance.py 패턴), 접미사 없는 `CTX_AREA_FK/NK`이거나 헤더 `tr_cont`만 쓰면 A.4/A.5의 수동 루프.
7. **rate limit**: `fetch()`에 내장 리미터 + `EGW00201` 자동 재시도가 있으므로 루프에 sleep 불필요. 다만 순위류 API 폴링 주기는 스스로 제한할 것.
8. **웹소켓**: `WEBSOCKET_RESPONSES_MAP` 등록 필수(미등록 = 조용히 드롭), dict 재할당 금지(항목 추가만), `__fields__` 길이 = 실제 컬럼 수, 최대 40 구독 제한, 이벤트 티켓 보관.
9. **캐시/토큰**: 토큰은 `keep_token=True`로 재사용. `fetch()`에는 응답 캐시가 없으므로 휴장일 같은 정적 데이터는 사용자 레벨에서 캐싱.

---

## 부록 B. 분석 근거 파일

**vm-stock-kis**

- `src/vmkis/kis.py` — `VmKis` 파사드, `request()`/`fetch()` 게이트웨이, 메서드 주입 지점
- `src/vmkis/responses/dynamic.py` + `types.py` + `response.py` — 동적 변환 엔진 3종 세트
- `src/vmkis/client/websocket.py` — 실시간 엔진, `client → api` 역참조 지점(:19)
- `src/vmkis/scope/stock.py` + `adapter/product/quote.py` — Scope 조립 루트와 Mixin 바인딩
- `src/vmkis/api/stock/quote.py` — 엔드포인트 구현 표준 패턴(761줄)
- `src/vmkis/api/websocket/__init__.py` — `WEBSOCKET_RESPONSES_MAP` 등록 지점
- `src/vmkis/__env__.py` — 도메인·한도·Rate Limit 상수

**open-trading-api**

- `examples_user/kis_auth.py` — 인증·REST·WS가 전부 담긴 유일 인프라(799줄)
- `examples_llm/domestic_stock/inquire_price/inquire_price.py` — 단건 조회 정본
- `examples_llm/domestic_stock/inquire_balance/inquire_balance.py` — 연속조회 재귀 정본
- `examples_user/domestic_stock/domestic_stock_functions.py` — 최대 통합본(13,463줄/131함수)
- `docs/convention.md` — 공식 코딩 컨벤션(112줄)
- `llms.txt` — LLM 내비게이션 인덱스

## 부록 C. 분석 방법

- **software-architect 서브에이전트 7인 병렬** (model: fable 5)
  1. vm-stock-kis 계층 구조 코드 검증 (AST 기반 import 그래프 분석 포함)
  2. open-trading-api 구조·패턴·커버리지 분석
  3. 미지원 API 추가 플레이북 (기존 엔드포인트 end-to-end 추적)
  4. 의존성 방향 판정 (§5) — 지연 import 계수, 부분 로드 실측, ADP/SDP/DIP 적용
  5. 사용자 관점 편의성 비교 (§8) — 양측 실제 코드 대조
  6. `fetch()` 확장 예제 (부록 A) — 공식 샘플에서 TR/파라미터/필드 추출 후 검증
  7. 하부 레이어 흡수 타당성 (§13) — AST 파서 실작성·실행(334폴더), 라이선스 조사
- 위 결과 중 보고서의 **load-bearing 주장 10건**(역방향 의존 4건, `WEBSOCKET_RESPONSES_MAP` drop 동작, `KisNotFoundError` 중복, Rate Limit 상수, `fetch()` 시그니처, guidelines 문서 부재)은 **메인 세션에서 직접 재검증**했습니다.
