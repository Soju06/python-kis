# Public API Design (v3 Surface)

Layer 2 사용자 대면 API 설계.

## Design Principles

1. **도메인 우선**: 도메인 네임스페이스가 기본 경로, raw는 보조
2. **환경 명시**: `demo` / `real` 환경을 항상 명시적으로 구분
3. **Async-first**: `KisAsyncClient`가 단일 소스, `KisClient`는 sync 브리지 (ADR-001)
4. **탐색 가능**: 설치 직후 직관적으로 탐색 가능한 표면 API

## Public Object Graph

```
KisClient / KisAsyncClient
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
│   └─ iter(...)            # sync bridge
├─ raw                      # Raw API escape hatch (Layer 0)
└─ close() / aclose()
```

## Naming & Path Rules

| Pattern | Example | Note |
|---------|---------|------|
| 국내 기본 경로 | `kis.domestic.stock.quote("005930")` | 도메인 명시 |
| 해외 명시 경로 | `kis.overseas.stock.quote("AAPL", exchange="NASDAQ")` | exchange 필수 |
| 국내 단축 경로 | `kis.stock("005930").quote()` | 국내 기본만 |
| 해외 단축 경로 | — | exchange= 또는 market= 필수 |

## Configuration

```python
from pykis import KisClient, KisAsyncClient, KisConfig

config = KisConfig(
    app_key="...",
    app_secret="...",
    env="demo",           # demo / real 만 허용
    account_id="12345678-01",
)

# async-first
async with KisAsyncClient(config) as kis:
    quote = await kis.domestic.stock.quote("005930")

# sync bridge
with KisClient(config) as kis:
    quote = kis.domestic.stock.quote("005930")
```

Rules:
- `env`는 `demo` / `real`만 허용 (SR-T002)
- 계좌는 config 기본값 또는 `account(account_id=...)` override
- import 시 네트워크/시크릿 로드 금지

## Streaming

```python
# async
async with kis.streams.price.subscribe("005930") as stream:
    async for tick in stream:
        ...

# sync bridge
for tick in kis.streams.price.iter("005930"):
    ...
```

- `Subscription`은 명시적 `close()` / `aclose()` 제공 (ADR-004)
- GC 기반 해지 없음

## Raw API Escape Hatch

```python
raw = kis.raw
resp = raw.call("uuid-of-endpoint", payload={"...": "..."})
```

- Raw 모델은 자동 생성된 정확한 응답 구조 (Layer 0)
- Domain 모델과 네임스페이스 분리

## Layer Mapping

| API Surface | Layer | Description |
|-------------|-------|-------------|
| `kis.domestic.*` / `kis.overseas.*` | L2 (System) | 도메인 객체, Decimal/UTC |
| `kis.streams.*` | L2 (Streaming System) | 정규화된 이벤트 |
| `kis.raw.*` | L0 (Raw) | API 원형 보존 |
| `kis.account().*` | L2 (System) | 계좌 도메인 객체 |

## Traceability

- SR-D001 (Type annotations) → 모든 public API에 type hints
- SR-D002 (Async/Sync) → KisAsyncClient + KisClient (ADR-001)
- SR-D003 (Actionable errors) → SDK-specific exception hierarchy
- SR-T002 (Demo/Real) → KisConfig.env 명시
- SR-M001 (Streaming) → streams.* 인터페이스 (ADR-004)
