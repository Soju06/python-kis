# 미지원 API 호출하기 — `fetch()` 가이드

이 라이브러리는 KIS OpenAPI 중 **주식 현물만** 구현합니다. 선물옵션·채권·ELW·
순위분석·조건검색 등은 전용 메서드가 없습니다.

**그래도 호출할 수 있습니다.** `VmKis.fetch()` 가 정식 escape hatch입니다.
라이브러리를 고치거나 포크할 필요가 없습니다.

전량 OpenAPI codegen 이관은 **하지 않습니다** (`#100` **B**). 새 TR 은 수요가
있을 때 이슈 한 건 = TR 하나(`TR: <id>`), 또는 아래에서 `fetch()` 로 붙입니다.
`scripts/codegen/pilot/` 은 휠 밖입니다.

> 이 문서는 "vmkis로 시작하고, 없는 TR은 `fetch()` 로 뚫는다"는 사용 모델을
> 전제합니다. 대부분의 경우 [Level 0](#level-0--그냥-호출하기-5줄) 이나
> [Level 1](#level-1--타입-붙이기-3060줄) 로 충분합니다.

## 목차

1. [Level 0 — 그냥 호출하기 (5줄)](#level-0--그냥-호출하기-5줄)
2. [Level 1 — 타입 붙이기 (30~60줄)](#level-1--타입-붙이기-3060줄)
3. [Level 2 — 라이브러리에 통합](#level-2--라이브러리에-통합)
4. [Level 3 — 실시간(WebSocket) TR 추가](#level-3--실시간websocket-tr-추가)
5. [함정 체크리스트](#함정-체크리스트)

---

## Level 0 — 그냥 호출하기 (5줄)

```python
from vmkis import VmKis

kis = VmKis("vmkis_auth.json", keep_token=True)

res = kis.fetch(
    "/uapi/overseas-price/v1/quotations/price",
    api="HHDFS00000300",                              # TR ID → headers["tr_id"]
    params={"AUTH": "", "EXCD": "NAS", "SYMB": "AAPL"},
    domain="live",                                    # 시세 TR은 모의 서버에 없음
)

print(res.rt_cd, res.msg1)   # ⚠️ 자동 예외 없음 — 직접 확인해야 합니다
print(res.output.last)       # 현재가 (문자열 그대로)
raw: dict = res.raw()        # 순수 dict
```

### 공짜로 따라오는 것

`requests` 로 직접 호출하는 것과 달리, 아래가 전부 적용됩니다.

- appkey / 토큰 주입과 **자동 갱신**
- 실전 / 모의 **도메인 라우팅**
- **Rate Limiting** (실전 19/s, 모의 2/s)
- `EGW00201`(유량 초과) **지수 백오프 재시도**, `EGW00123`(토큰 만료) **재발급**
- HTTP 오류 → `KisHTTPError`

### 주의 세 가지

1. **업무 오류가 예외로 바뀌지 않습니다.**
   기본 `response_type` 인 `KisDynamicDict` 는 `rt_cd` 검사를 건너뜁니다.
   `res.rt_cd` 를 직접 확인하세요. 이게 싫으면 Level 1로 가세요.
2. **값이 전부 문자열입니다.** `Decimal(res.output.last)` 처럼 직접 캐스팅해야 합니다.
3. **페이지네이션을 직접 관리해야 합니다.** `continuous=True` 와 커서를 손으로 다뤄야 합니다.

### 더 낮은 층

`kis.request(...)` 는 `requests.Response` 를 그대로 돌려줍니다. 응답 파싱까지
직접 하고 싶을 때만 쓰세요.

> 라이브러리 내부도 같은 패턴을 씁니다. `src/vmkis/api/stock/info.py` 가
> `HHDFS00000300` 을 `response_type` 없이 호출합니다.

---

## Level 1 — 타입 붙이기 (30~60줄)

응답 클래스를 하나 정의하면 `Decimal` 변환, `rt_cd` → 예외, nullable 처리가
전부 자동이 됩니다. **라이브러리를 수정하지 않습니다. 사용자 코드입니다.**

```python
from decimal import Decimal

from vmkis import VmKis
from vmkis.responses.response import KisAPIResponse     # __path__="output" 포함
from vmkis.responses.types import KisDecimal, KisInt, KisString


class ForeignPrice(KisAPIResponse):
    """해외주식 현재체결가 (HHDFS00000300)"""

    __ignore_missing__ = True          # KIS가 필드를 추가/누락해도 안전

    symbol: str = KisString["rsym"]
    price: Decimal = KisDecimal["last"]
    prev_price: Decimal = KisDecimal["base"]
    change: Decimal = KisDecimal["diff"]
    rate: Decimal = KisDecimal["rate"]
    volume: int = KisInt["tvol"]
    orderable: str | None = KisString["ordy", None]     # 기본값 지정


def foreign_price(kis: VmKis, exchange: str, symbol: str) -> ForeignPrice:
    return kis.fetch(
        "/uapi/overseas-price/v1/quotations/price",
        api="HHDFS00000300",
        params={"AUTH": "", "EXCD": exchange, "SYMB": symbol},
        response_type=ForeignPrice,
        domain="live",
    )


p = foreign_price(VmKis("vmkis_auth.json"), "NAS", "AAPL")
print(p.price, p.rate)      # Decimal, Decimal
```

### 베이스 클래스 고르기

| 클래스 | 쓸 때 |
|---|---|
| `KisResponse` | `rt_cd` 검사만 필요. 응답 루트를 직접 다룸 |
| `KisAPIResponse` | **대부분 이것.** `__path__ = "output"` 이 기본 |
| `KisPaginationAPIResponse` | 연속조회. `page_status` / `next_page` 자동 |

### 필드 디스크립터

`vmkis.responses.types` 에 있습니다.

`KisString` · `KisInt` · `KisDecimal` · `KisBool` · `KisDate` · `KisTime` ·
`KisDatetime` · `KisDict` · `KisAny(fn)`

> **금액에 `KisFloat` 를 쓰지 마세요.** 부동소수점 오차가 그대로 돈 계산에
> 들어갑니다. `KisDecimal` 을 쓰세요.

문법:

```python
KisDecimal["field"]                  # 필수 필드
KisString["field", None]             # 없으면 None
KisString()("field", absolute=True)  # __path__ 를 무시하고 응답 루트에서 찾기
```

리스트 응답은 `KisList` 를 씁니다.

```python
from vmkis.responses.dynamic import KisList

class RankItem(KisAPIResponse):
    symbol: str = KisString["mksc_shrn_iscd"]
    name: str = KisString["hts_kor_isnm"]

class RankResponse(KisAPIResponse):
    __path__ = None                                   # output2가 루트 바로 아래
    items: list[RankItem] = KisList(RankItem)["output"]
```

### 클래스 옵션

- `__path__` — 응답에서 필드를 찾을 시작 경로. `None` 이면 루트
- `__ignore_missing__` — 필드가 없어도 `KeyError` 를 내지 않음

### 생성자 인자가 필요하면

`response_type` 에 **클래스 대신 인스턴스**를 넘깁니다.

```python
kis.fetch(..., response_type=MyResponse(symbol="005930"))
```

---

## Level 2 — 라이브러리에 통합

`kis.stock("005930").my_feature()` 처럼 1급 시민으로 만들려면 **250~800 LOC** 가
듭니다. 절반 이상이 Protocol / overload / docstring 중복입니다.

절차는 [ARCHITECTURE.md 의 확장성 절](../architecture/ARCHITECTURE.md#새로운-rest-api-추가--6단계-250800-loc)에
있습니다.

> **Protocol 을 반드시 써야 하는 것은 아닙니다.** 단일 시장 TR 이고 공개
> 타입으로 내보내지 않는다면 impl 클래스 + 모듈 함수만으로 1급 시민이 됩니다.
> 판정표는 [언제 Protocol 이 필요한가](../architecture/ARCHITECTURE.md#언제-protocol-이-필요한가--판정-기준)
> 에 있습니다 — 이 기준이 없던 동안 필요 없는 곳에도 Protocol 을 쓰게
> 되어 있었습니다.

**대부분의 경우 Level 1로 충분하고, 여기까지 올 필요가 없습니다.** 라이브러리에
넣어야 하는 경우는 (1) 여러 사람이 쓰는 사내 표준이 되거나, (2) 이 저장소에
기여할 때입니다.

### 중간 지점 — 기존 scope 객체에 메서드만 붙이기

```python
def my_feature(self):
    return self.kis.fetch(..., response_type=MyResponse)

# kis.stock(...) 이 돌려주는 클래스에 직접 붙입니다
from vmkis.scope.stock import KisStock
KisStock.my_feature = my_feature
```

공식 확장점은 아니지만 Level 2의 보일러플레이트 없이 호출 편의를 얻습니다.

---

## Level 3 — 실시간(WebSocket) TR 추가

1. **응답 클래스 정의** — `KisWebsocketResponse` 를 상속하고 `__fields__` 를
   `^` 분리 **순서 그대로** 나열합니다. 미사용 필드는 `None`.

2. **⚠️ 레지스트리에 등록** — 이게 이 절의 전부입니다.

   ```python
   from vmkis.responses.websocket import register_websocket_response

   @register_websocket_response("H0STANC0")
   class MyRealtimeResponse(KisWebsocketResponse, ...):
       ...
   ```

   > **이 한 줄이 없으면 구독 메시지는 정상 전송되고 서버도 데이터를 보내지만,
   > 수신 이벤트가 조용히 버려집니다.** 경고 로그만 남습니다. 실시간 TR 추가에서
   > 가장 자주 빠뜨리는 단계입니다.
   >
   > 암호화되는 TR 이면 `encrypted=True` 를 함께 줍니다.
   >
   > 데코레이터는 **클래스 정의 시점에** 등록합니다. 따라서 그 모듈이 한 번은
   > import 되어야 합니다. 사용자 코드에서는 클래스를 정의한 모듈을 import 하면
   > 됩니다.

   기존 dict 에 직접 넣는 방식도 여전히 동작합니다.

   ```python
   from vmkis.responses.websocket import WEBSOCKET_RESPONSES_MAP

   WEBSOCKET_RESPONSES_MAP["H0STANC0"] = MyRealtimeResponse
   ```

   > 같은 dict 객체를 참조하므로 **항목 추가**는 반영됩니다. 다만
   > `WEBSOCKET_RESPONSES_MAP = {...}` 처럼 **재할당하면 반영되지 않습니다.**

3. **구독** — `kis.websocket.on(...)` 으로 붙입니다.

   ```python
   ticket = kis.websocket.on(id="H0STANC0", key="005930", callback=handler)
   # ⚠️ ticket 을 변수에 보관하세요. GC되면 구독이 해지됩니다.
   ```

---

## 함정 체크리스트

새 TR을 붙이기 전에 훑어보세요.

| # | 함정 | 대응 |
|---|---|---|
| 1 | **도메인 라우팅 기본값** | `domain=None` 이면 `kis.paper` 를 따라갑니다. **시세 TR은 모의 서버에 없으므로** `domain="live"` 를 명시하세요. 빠뜨리면 모의 계정에서만 터집니다 |
| 2 | **모의 미지원 TR** | 기간손익 등 일부는 모의 변형이 없습니다. 반대로 잔고·주문류는 `"VT..." if paper else "TT..."` 분기가 필요합니다 |
| 3 | **빈 값** | KIS는 값이 없으면 `""` 를 보냅니다. `KisInt`/`KisDecimal`/`KisDate` 는 이때 예외를 냅니다. 어노테이션을 `\| None` 로 두면 `None` 이 됩니다 |
| 4 | **필드 자체 누락** | `KeyError`. `KisString["field", None]` 또는 `__ignore_missing__ = True` 로 대응합니다. 실제로 일부 종목에서 종목명 필드가 빠져 옵니다 |
| 5 | **`KisDynamicDict` 는 `rt_cd` 를 검사하지 않음** | Level 0에서 업무 오류가 조용히 통과합니다 |
| 6 | **페이지 커서 접미사** | `ctx_area_fk100` / `fk200` / `fk50` / 접미사 없음 네 가지가 있습니다. `KisPage` 가 넷 다 파싱하지만, 요청 폼을 직접 만든다면 API마다 다르다는 점을 기억하세요 |
| 7 | **Rate limit 은 도메인 전역** | TR별 세분화가 없습니다. 실전 19/s, 모의 2/s 공유입니다 |
| 8 | **캐시는 자동이 아님** | `kis.cache` 는 opt-in 입니다. 정적 데이터만 수동으로 캐시하세요 |
| 9 | **`kis.stock()` 이 API를 2회 이상 호출** | scope 생성 시 종목 정보를 조회해 시장을 판별합니다. 신규 상품군(선물옵션 등)은 시장 코드 등록이 따로 필요합니다 — **숨은 비용** |
| 10 | **WebSocket 티켓 GC** | 구독 티켓을 변수에 잡지 않으면 즉시 해지될 수 있습니다 |
| 11 | **hashkey 미사용** | KIS의 선택적 hashkey 헤더는 이 라이브러리가 쓰지 않습니다. 신규 주문 TR에도 불필요합니다 |

---

## 그래서 어디까지 해야 하나

| 상황 | 권장 |
|---|---|
| 한 번 조회해 보고 싶다 | **Level 0** |
| 내 코드에서 계속 쓴다 | **Level 1** — 타입과 예외를 얻습니다 |
| 팀 표준으로 만든다 | Level 1 + 중간 지점(메서드 부착) |
| 이 저장소에 기여한다 | **Level 2** |
| 실시간 TR 이 필요하다 | **Level 3** — 레지스트리 등록을 잊지 마세요 |

Level 0/1 로 해결되지 않는 것을 발견하면
[이슈](https://github.com/visualmoney/vm-stock-kis/issues)로 알려주세요.
어떤 TR이 실제로 필요한지가 Level 2 우선순위를 정하는 근거가 됩니다.
