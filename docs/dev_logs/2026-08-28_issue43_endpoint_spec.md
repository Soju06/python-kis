# 2026-08-28 - Issue #43 선언적 엔드포인트 스펙 개발 일지

**대상 이슈**: [#43](https://github.com/visualmoney/vm-stock-kis/issues/43)
**범위**: 1~3단계 중 **계좌 계열까지**. 시세 계열(`api/stock/*`)은 남았습니다.

---

## 요약

```text
975 passed, 7 skipped (게이팅)
TOTAL 90.81%
REST TR ID 삼항 분기: 9곳 -> 0곳
```

---

## 1단계 — `KisEndpoint` + `VmKis.call()`

기존 코드를 건드리지 않고 추가만 했습니다(동작 변화 0).

`KisEndpoint.resolve(virtual)` 가 규칙 셋을 한 곳에 모읍니다.

```text
실전 계좌 + 모의 있음 : ('TTTC8434R', 'real')
모의 계좌 + 모의 있음 : ('VTTC8434R', 'virtual')
모의 계좌 + 모의 없음 : ('FHKST01010100', 'real')   <- 실전으로 라우팅
override             : ('V', 'real')
```

세 번째가 핵심입니다. **`tr_virtual` 을 생략하는 것만으로 "모의 미지원 TR"이
표현되고, 도메인 라우팅이 자동**입니다. 예전에는 `domain="real"` 을 손으로
붙였고 빠뜨리면 모의 계정에서만 터졌습니다.

`frozen=True` 로 두어 실행 중 변경을 막았습니다(`FrozenInstanceError` 확인).

---

## 2단계 — 주문 계열 이관으로 필드 설계 검증

이슈가 "이미 표로 정리된 주문 계열부터 이관해 필드 목록을 검증"하라고 한
이유가 여기서 드러났습니다.

### 표는 `KisEndpoint` 보다 차원이 많았습니다

```python
DOMESTIC_ORDER_API_CODES: dict[tuple[bool, ORDER_TYPE], str]
FOREIGN_ORDER_API_CODES:  dict[tuple[bool, MARKET_TYPE, ORDER_TYPE], str]
```

`KisEndpoint` 는 `tr_real`/`tr_virtual` 두 필드뿐입니다. **해법은 차원을
나누는 것이었습니다** — 실전/모의 차원만 스펙 안으로 넣고 나머지는 dict 키로
남깁니다.

```python
DOMESTIC_ORDER_ENDPOINTS: dict[ORDER_TYPE, KisEndpoint]
FOREIGN_ORDER_ENDPOINTS:  dict[tuple[MARKET_TYPE, ORDER_TYPE], KisEndpoint]
```

**설계가 통했습니다.** 18개 (시장, 매수/매도) 조합이 전부 실전/모의 쌍을
완비하고 있어 손실 없이 분해됐습니다.

### 표를 손으로 옮기지 않았습니다

18개 항목을 전사하면 오타가 납니다. **기존 표를 런타임에 읽어 새 리터럴을
생성**했고, 생성 과정에서 쌍이 불완전한 조합이 없음을 함께 검증했습니다.
원본의 시장 설명 주석(`# 미국 매수 주문`)도 정규식으로 뽑아 보존했습니다.

---

## 3단계 — 계좌 계열 이관

| 파일 | 스펙 | 이관 |
|---|---|---|
| `order.py` | `DOMESTIC_ORDER_ENDPOINTS`(2) · `FOREIGN_ORDER_ENDPOINTS`(18) | 2곳 |
| `balance.py` | `_DOMESTIC_BALANCE` · `_FOREIGN_BALANCE` · `_FOREIGN_PRESENT_BALANCE` | 3곳 |
| `daily_order.py` | `_FOREIGN_DAILY_ORDERS` | 1곳 |
| `order_modify.py` | `_DOMESTIC_ORDER_MODIFY` | 2곳 |
| `orderable_amount.py` | `_DOMESTIC_ORDERABLE_AMOUNT` · `_FOREIGN_ORDERABLE_AMOUNT` | 2곳 |
| `pending_order.py` | `_FOREIGN_PENDING_ORDERS` | 1곳 |

### Before / After — 페이징이 특히 줄었습니다

```python
# 이전
page = (page or KisPage.first()).to(100)          # 커서 길이를 손으로
result = self.fetch(
    "/uapi/domestic-stock/v1/trading/inquire-balance",
    api="VTTC8434R" if self.virtual else "TTTC8434R",   # 분기를 손으로
    params={...},
    form=[account, page],
    continuous=not page.is_first,                       # 연속조회를 손으로
    response_type=...,
)

# 이후
page = page or KisPage.first()
result = self.call(
    _DOMESTIC_BALANCE,
    params={...},
    form=[account],
    page=page,
    response_type=...,
)
```

---

## 테스트 — 단언의 가치를 지켰습니다

목이 `fetch` 를 잡고 있어서 `call()` 로 바꾸니 전부 깨졌습니다. 두 선택지가
있었습니다.

1. 단언을 `call(스펙)` 으로 바꾸기 → **"국내 매수는 TTTC0802U 로 나간다"는
   검증이 사라집니다**
2. 목에 **실제 `VmKis.call` 을 바인딩** → `fetch(api=...)` 단언이 그대로 살고,
   덤으로 스펙 해석까지 검증됩니다

2번을 택했습니다.

```python
def call(self, *args, **kwargs):
    from vmkis.kis import VmKis
    return VmKis.call(self, *args, **kwargs)
```

`call()` 이 `self.virtual` 과 `self.fetch` 만 쓰므로 목에 그대로 붙습니다.
**테스트가 이전보다 더 많이 검증하게 됐습니다.**

표 검증 테스트는 스펙 기준으로 다시 썼고, **네트워크 없이 규칙을 확인**하는
단언을 더했습니다.

```python
assert buy.resolve(virtual=False) == ("TTTC0802U", "real")
assert buy.resolve(virtual=True) == ("VTTC0802U", "virtual")
```

---

## 밟은 함정

- **중복 인자**: 스펙이 `method="POST"` 를 들고 있는데 호출부에도 남아
  `TypeError: got multiple values for keyword argument 'method'`.
  중첩 괄호 때문에 정규식 탐지가 실패해, **괄호 깊이를 세는 방식**으로 다시 찾았습니다.
- **import 누락**: 스펙만 넣고 `KisEndpoint` import 를 빠뜨려 `F821`.
  ruff 가 잡았습니다.

---

## 남은 것 — 시세 계열

`api/stock/*` 의 `domain="real"` **10곳**이 남았습니다.

```text
api/account/order.py:1   api/stock/daily_chart.py:2   api/stock/day_chart.py:2
api/stock/info.py:3      api/stock/quote.py:2
```

전부 고정 TR ID 에 `domain="real"` 을 손으로 붙인 형태라, `tr_virtual` 을
생략한 `KisEndpoint` 로 옮기면 **`domain` 인자 자체가 사라집니다.** 이관은
단순하지만 시세/차트 경로는 테스트가 많아 별도로 진행하는 편이 안전합니다.

`info.py` 의 3곳은 시장 판별 루프 안에 있고, `quote.py` 와 **같은 TR
(`FHKST01010100`, `HHDFS00000300`)** 을 씁니다. 스펙을 공유하면 중복이 더 줍니다.

## 다음 할 일

- [ ] 시세 계열 이관 → `domain="real"` 10곳 제거
- [ ] `DOMESTIC_DAILY_ORDERS_API_CODES`, `FOREIGN_ORDER_MODIFY_API_CODES` —
      아직 표로 남은 두 개. 주문 계열과 같은 방식으로 분해 가능
- [ ] [#44](https://github.com/visualmoney/vm-stock-kis/issues/44) 페이징 헬퍼.
      `call(page=...)` 이 커서와 `continuous` 를 처리하므로 이제 더 얇게 만들 수 있다
- [ ] (검토) 스펙을 `endpoints.py` 한 곳에 모을지. 지금은 각 모듈에 co-locate 했다.
      한곳에 모으면 "지원 TR 전체가 한눈에" 보이지만 정의와 사용이 멀어진다
