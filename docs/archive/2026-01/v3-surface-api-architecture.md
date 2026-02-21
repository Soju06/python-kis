# v3 Surface API Architecture (Draft)

작성일: 2026-01-12

## 목표 (SDK 사용자 관점)

- 설치 직후 **직관적으로 탐색 가능한 표면 API** 제공
- `demo` / `real` 환경을 **항상 명시적으로** 구분
- **async-first**, sync는 얇은 브리지
- 도메인 모델(편의/표준화)과 Raw 모델(정확/저수준)을 **명확히 분리**

---

## 1) Public Object Graph

```
Kis / KisAsync
├─ config
├─ domestic
│   ├─ stock
│   │   ├─ quote(symbol)
│   │   ├─ orderbook(symbol)
│   │   └─ candle(symbol, interval, from, to)
│   └─ market
├─ overseas
│   ├─ stock
│   └─ market
├─ account(account_id=None)
│   ├─ orders.buy(...)
│   ├─ orders.sell(...)
│   ├─ positions.list(...)
│   └─ balances.get(...)
├─ streams
│   ├─ price.subscribe(symbol)
│   ├─ order.subscribe(...)
│   └─ iter(...)  # sync bridge
├─ raw  # Raw API escape hatch
└─ close()/aclose()
```

핵심 원칙:
- `KisAsync`가 **단일 소스**이며, `Kis`는 얇은 sync 브리지
- 계층은 **도메인 우선 → raw는 보조**
- `domestic` / `overseas`는 상위 namespace로 분리

---

## 2) 네이밍/경로 규칙

- 기본 경로: `kis.domestic.stock.quote("005930")`
- 해외는 명시적: `kis.overseas.stock.quote("AAPL", exchange="NASDAQ")`
- 단축 경로는 **국내 기본**만 제공
  - `kis.stock("005930").quote()`
  - 해외는 `exchange=` 또는 `market=`가 필수

---

## 3) Config & Environment

```python
from pykis import Kis, KisAsync, KisConfig

config = KisConfig(
    app_key="...",
    app_secret="...",
    env="demo",  # 반드시 demo/real 중 하나
    account_id="12345678-01",
)

kis = Kis(config)  # sync wrapper
```

규칙:
- `env`는 `demo` / `real`만 허용
- 계좌는 `KisConfig` 기본값 또는 `account(account_id=...)`로 override
- import 시 네트워크/시크릿 로드 금지

---

## 4) Sync / Async 전략

```python
# async-first
async with KisAsync(config) as kis:
    quote = await kis.domestic.stock.quote("005930")

# sync bridge
with Kis(config) as kis:
    quote = kis.domestic.stock.quote("005930")
```

- Async API가 모든 기능의 원본
- Sync는 내부에서 안전한 브리지 호출만 수행

---

## 5) Streams / Subscription 모델

```python
async with kis.streams.price.subscribe("005930") as stream:
    async for tick in stream:
        ...

for tick in kis.streams.price.iter("005930"):
    ...
```

- `Subscription`은 명시적 `close()/aclose()` 제공
- GC 기반 해지 없음

---

## 6) Raw API Escape Hatch

```python
raw = kis.raw
resp = raw.call("uuid-of-endpoint", payload={"...": "..."})
```

- Raw 모델은 자동 생성된 **정확한 응답 구조**
- Domain 모델과 혼용하지 않도록 네임스페이스 분리

---

## 7) Concept Usage (End-to-End)

```python
from decimal import Decimal
from pykis import Kis, KisConfig

config = KisConfig(
    app_key="...",
    app_secret="...",
    env="demo",
    account_id="12345678-01",
)

with Kis(config) as kis:
    quote = kis.domestic.stock.quote("005930")

    order = kis.account().orders.buy(
        symbol="005930",
        qty=1,
        price=Decimal("70000"),
        exchange="KRX",
    )
```

설계 요약:
- **도메인 네임스페이스가 기본 경로**
- **raw는 탈출구로만 사용**
- **demo/real의 명시성**을 최우선 원칙으로 둔다
