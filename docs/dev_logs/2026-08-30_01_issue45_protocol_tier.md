# 2026-08-30 - #45 Protocol Tier 기준 문서화 + overload 유지 결정 개발 일지

## 작업 내용

(A) Protocol 판정 기준을 `ARCHITECTURE.md` 에 넣고, (B) `@overload` →
레지스트리 교체를 **측정 후 기각**했습니다. `src/` 는 한 줄도 바꾸지 않았습니다.

## 무엇에 걸렸는가

### 1. (B) 를 먼저 판정해야 (A) 를 쓸 수 있었습니다

이슈는 "(A) 가 먼저"라고 적었지만 순서가 반대였습니다. (A) 는 "Protocol 이
언제 필요한가"인데, (B) 가 통과하면 `adapter/*` Protocol 의 형태 자체가
달라집니다. **(B) 를 모르는 채로 (A) 를 쓰면 다시 써야 합니다.**

### 2. 추측하지 않고 pyright 로 쟀습니다

이슈가 남긴 질문이 이것이었습니다.

> 타입 검사기가 dict 분기의 반환 타입을 좁힐 수 있는가?
> 못 하면 (B)는 하지 않는 편이 낫습니다.

**pyright 는 VS Code 의 Pylance 엔진**이므로 "IDE 자동완성이 얼마나
나빠지는가"의 직접적인 답이기도 합니다. 클릭해 보는 것보다 재현 가능합니다.

세 가지 최소 예제에 `reveal_type` 을 찍었습니다.

```text
a_overload.py:20 - Type of "c.on("price")" is "Ticket[Price]"
a_overload.py:21 - Type of "c.on("orderbook")" is "Ticket[Orderbook]"
b_registry.py:27 - Type of "r.on("price")" is "Ticket[Price] | Ticket[Orderbook]"
b_registry.py:28 - Type of "r.on("orderbook")" is "Ticket[Price] | Ticket[Orderbook]"
c_hybrid.py:28 - Type of "h.on("price")" is "Ticket[Price]"
c_hybrid.py:29 - Type of "h.on("orderbook")" is "Ticket[Orderbook]"
```

파이썬 타입 시스템에 **키에 따라 반환 타입이 달라지는 매핑**을 표현할 방법이
없습니다. (B) 를 그대로 하면 사용자가 매번 `isinstance` 로 좁혀야 합니다.

### 3. 세 번째 변형이 이슈에 없었습니다 — 그런데 그것도 답이 아닙니다

이슈는 (B)를 "overload 를 레지스트리로 **대체**"로 적었는데, 사실 두 가지가
섞여 있습니다.

1. `@overload` 스텁 — **타입 표면**
2. 런타임 `if/elif` 분기 — **디스패치**

2번만 dict 로 바꾸고 1번을 남기는 절충안(`c_hybrid`)이 가능하고, 위에서 보듯
**좁힘도 지켜집니다.** 그래서 줄 수를 실측했습니다.

```text
adapter/websocket/price.py   331줄
  @overload 스텁              170줄  (51%)   ← 유지해야 함
  실제 구현부                 118줄  (36%)   ← 이 중 분기는 ~24줄
  그 밖(import 등)             43줄
```

**비용의 절반이 overload 스텁입니다.** 절충안은 331줄에서 ~20줄을 줄이면서
간접 참조를 늘립니다. 남는 장사가 아닙니다.

즉 (B)는 어느 형태로도 **줄이려던 것을 줄이지 못합니다.** 기각했습니다.

### 4. "구현 개수"로 Protocol 필요성을 셀 수 없습니다

(A) 를 쓰려고 Protocol 53개가 왜 있는지 세려 했는데, 처음 만든 스크립트가
**전부 0** 을 냈습니다.

```text
0  KisQuote      —
0  KisBalance    —
```

**Protocol 은 구조적입니다.** `KisDomesticQuote` 는 `KisQuote` 를 상속하지
않습니다 — 모양만 맞추면 됩니다. 상속 그래프로 세는 접근 자체가 틀렸습니다.
모듈별 구체 클래스를 세는 쪽으로 바꿨습니다.

### 5. 이슈가 제시한 기준 하나로는 53개가 설명되지 않습니다

이슈는 **"국내/해외 통합이 있을 때만 Protocol"** 을 제안했습니다. 재 보니
그것만으로는 안 됩니다.

```text
—  api/stock/info.py           국내=0 해외=0   KisStockInfo (구현: _KisStockInfo 하나)
—  api/stock/trading_hours.py  국내=0 해외=0   KisTradingHours
—  api/base/product.py         국내=0 해외=0   KisProductProtocol
```

`KisStockInfo` 는 구현이 **하나**인데 Protocol 입니다. 이유는 구체 클래스가
`_KisStockInfo` 로 **비공개**이고 Protocol 만 `vmkis.types` 로 공개되기
때문입니다. `KisProductProtocol` 은 믹스인이 `self` 에 무엇이 있는지 선언하는
용도입니다.

역할이 셋이었습니다.

| | 역할 | 기준 |
|---|---|---|
| T1 | 시장 통합 | 호출자가 국내·아시아·미국을 **하나의 이름**으로 받는가 |
| T2 | 공개 반환 타입 | `public_types`/`types` 로 내보내며 구체 클래스를 감추는가 |
| T3 | 믹스인 self 타입 | 믹스인이 `self` 에 무엇이 있다고 가정하는지 선언 |

`scope/` 의 `KisAccount`·`KisStock` 은 넷째 역할처럼 보이지만 **T1 어댑터
Protocol 들의 교집합**이므로 T2 입니다.

### 6. 전수 확인 결과 — 고칠 것이 없었습니다

이슈의 작업 항목에 "불필요하게 Protocol 을 쓴 사례가 있는지 전수 확인"이
있었습니다. **53개 전부 T1/T2/T3 에 들어갑니다.**

기대했던 "지울 것"이 안 나왔지만 그것도 결과입니다. 이 절은 **기존 코드를
고치기 위한 것이 아니라 다음 사람이 판정을 다시 발명하지 않게 하려는 것**
이라고 문서에 적었습니다.

## 결정

| | 결정 | 근거 |
|---|---|---|
| (A) Tier 기준 | **문서화함** | `ARCHITECTURE.md` "언제 Protocol 이 필요한가" |
| (B) overload → 레지스트리 | **기각** | pyright 로 좁힘 소실 확인. 절충안도 ~20/331줄만 절감 |
| 보일러플레이트 축소 | **#21 codegen 이 남은 선택지** | 손으로 덜 쓰는 길이 막혔으므로 생성하는 쪽 |

## 변경 파일

- `docs/architecture/ARCHITECTURE.md` — 판정표 T1/T2/T3, 흔한 오해 3가지,
  전수 확인 결과, overload 유지 근거(측정치 포함). 기존 두 곳에 상호 참조
- `docs/user/EXTENDING_API.md` — Level 2 에 "Protocol 을 반드시 쓸 필요는 없다" 포인터

**`src/` 변경 없음.** 이슈의 "동작 변경 금지" 항목대로입니다.

## 재현

pyright 는 이 저장소의 의존성이 **아닙니다**. `uvx pyright <파일>` 로 그때만
받아 썼습니다. 숫자는 위에 적어 뒀으니 **다시 재기 전에 이 일지를 먼저 보세요.**

측정 스크립트는 `@overload` 데코레이터가 붙은 `ast.FunctionDef` 의
`end_lineno - lineno` 를 합산하는 것이 전부입니다.
