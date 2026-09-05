# 2026-08-28 - Issue #43 시세 계열 엔드포인트 스펙 이관 개발 일지

**대상 이슈**: [#43](https://github.com/visualmoney/vm-stock-kis/issues/43)
**범위**: 남은 A·B 전부. 이슈의 완료 기준 두 개가 모두 충족됐습니다.
**앞선 일지**: [2026-08-28_issue43_endpoint_spec.md](./2026-08-28_issue43_endpoint_spec.md) (계좌 계열)

---

## 요약

```text
985 passed, 22 skipped / TOTAL 90.69%  (게이트 90)
domain="real" (api/):      10곳 -> 0곳
문자열 TR 표 (*_API_CODES): 2종 -> 0종
스펙 총계:                  56개 / 10파일 / 고유 TR 70개
```

**작업 중 프로덕션 결함 2건을 발견해 함께 고쳤습니다** (아래 §3).

---

## 1. A — `domain="real"` 10곳을 스펙으로

전부 **고정 TR ID + 손으로 붙인 도메인** 형태였습니다. `tr_virtual` 을
생략하면 `resolve()` 가 모의 계좌에서도 실전을 돌려주므로 `domain` 인자
자체가 사라집니다.

| 파일 | 신설 스펙 | 이관 |
|---|---|---|
| `api/stock/quote.py` | `DOMESTIC_QUOTE` · `FOREIGN_QUOTE` | 2곳 |
| `api/stock/info.py` | `FOREIGN_PRICE` · `PRODUCT_INFO` | 3곳 |
| `api/stock/daily_chart.py` | `DOMESTIC_DAILY_CHART` · `FOREIGN_DAILY_CHART` | 2곳 |
| `api/stock/day_chart.py` | `DOMESTIC_DAY_CHART` · `FOREIGN_DAY_CHART` | 2곳 |
| `api/account/order.py` | `FOREIGN_DAYTIME_ORDER_ENDPOINTS` | 1곳 |

`info.py` 의 국내 시세 확인은 `quote.py` 와 **같은 TR**(`FHKST01010100`)이라
스펙을 재정의하지 않고 import 해서 씁니다. 테스트가 `is` 동일성으로 이를
고정합니다.

> 이슈 코멘트는 `info.py` 3곳이 `quote.py` 와 TR 두 개(`FHKST01010100`,
> `HHDFS00000300`)를 공유한다고 적었지만, **`HHDFS00000300` 은 `info.py`
> 에서만 씁니다.** `quote.py` 의 해외 시세는 `HHDFS76200200`(price-detail)
> 로 다른 엔드포인트입니다. 공유되는 것은 국내 TR 하나뿐입니다.

---

## 2. 시세 테스트는 TR ID 를 검증한 적이 없었습니다

TODO_LIST 가 경고한 것은 "목이 `call` 을 조용히 삼킨다"였는데, 실제로는
**그보다 앞선 문제**가 있었습니다.

`DOMESTIC_QUOTE.tr_real` 을 `"WRONG_TR_ID"` 로 바꾸고 돌렸습니다.

```text
165 passed
```

**아무것도 잡지 못했습니다.** 시세 테스트는 `params` 만 단언하고 `api=` 는
보지 않았습니다. 이관 이전부터 있던 구멍입니다.

두 가지를 했습니다.

1. **목에 실제 `VmKis.call` 바인딩** (`_fake_kis()` 팩토리, 58곳)
   — 목의 `virtual` 기본값이 Mock 이라 **truthy** 입니다. 그대로 두면 모의
   계좌로 해석되므로 `False` 를 명시합니다
2. **`tests/unit/api/stock/test_endpoints.py` 신설** — 스펙은 데이터라
   네트워크 없이 TR ID·경로·도메인 라우팅을 직접 검증합니다

되돌려 확인했습니다.

```text
tr_real 오염       -> 2 failed   (예전에는 0 failed)
tr_virtual 잘못 채움 -> 라우팅 단언이 실패
```

---

## 3. 밟은 함정 — 이번에 새로 드러난 것

### (a) `fetch()` 에 없는 `page` 인자를 넘기는 곳이 2곳 있었습니다

```text
api/account/daily_order.py:644    국내 일별 체결내역 조회
api/account/pending_order.py:711  국내 미체결 주문 조회
```

`VmKis.fetch()` 의 파라미터에 `page` 는 없습니다. **첫 호출에서
`TypeError: fetch() got an unexpected keyword argument 'page'` 로 죽습니다.**
`git log -L` 로 보면 PR #48 이 아니라 **업스트림에서부터 있던 결함**입니다.

**테스트가 왜 못 잡았나.** 가짜 `fetch` 가 `**kwargs` 를 받습니다.

```python
def fetch(self, *args, **kwargs):      # 무엇이든 받는다
    return SimpleNamespace(is_last=True, orders=["A"], next_page=None)
```

목은 시그니처를 검사하지 않습니다. 990건이 통과하는 동안 두 공개 API 가
호출 즉시 죽는 상태였습니다.

**대응**: `tests/unit/api/test_call_contract.py` 가 소스를 AST 로 읽어
`self.fetch(...)` / `self.call(...)` 호출부의 키워드가 실제 시그니처에
있는지 검사합니다. 목을 거치지 않으므로 이 종류의 결함을 구조적으로 막습니다.
결함을 되살려 실패를 확인했습니다.

```text
AssertionError: vmkis/api/account/pending_order.py:719 — fetch() 가 받지 않는 인자 ['page']
```

### (b) `method="POST"` 일괄 삭제가 무관한 호출까지 건드렸습니다

스펙이 `method` 를 들고 있으므로 호출부의 `method="POST"` 를 지워야 하는데
(지난 세션의 **중복 인자** 함정), 문자열 치환이 `fetch` 를 그대로 쓰는
주간거래 정정/취소 2곳까지 지웠습니다. **`ruff` 도 테스트도 잡지 못합니다 —
문법은 유효하고 POST 가 GET 으로 조용히 바뀔 뿐입니다.**

호출 범위를 괄호 깊이로 잘라 `method` 인자 유무를 전수 출력해서 찾았습니다.
정규식으로는 중첩 괄호 때문에 못 봅니다 — 지난 세션과 같은 교훈입니다.

두 곳은 `_FOREIGN_DAYTIME_ORDER_MODIFY` 스펙으로 함께 이관했습니다.

### (c) `git checkout <file>` 로 되돌리다 이관 작업을 날렸습니다

변이 테스트(스펙을 일부러 오염) 후 원복에 `git checkout` 을 썼는데,
**커밋 전이라 HEAD 로 돌아가 이관 자체가 사라졌습니다.** `quote.py` 는
백업이 있어 복구했지만 `daily_chart.py` 는 재작업했습니다.

> 커밋하지 않은 상태에서 변이 테스트를 할 때는 `cp` 백업으로 원복하거나,
> **먼저 커밋하고 변이시키세요.**

---

## 4. B — 남은 표 2종 분해

손으로 옮기지 않고 **기존 표를 런타임에 읽어 새 리터럴을 생성**했습니다.
생성 전에 쌍 완비를 검증했습니다.

```text
FOREIGN_ORDER_MODIFY   조합 14개 -> 쌍 완비 14/14
DOMESTIC_DAILY_ORDERS  조합  2개 -> 쌍 완비  2/2
```

| 이전 | 이후 |
|---|---|
| `DOMESTIC_DAILY_ORDERS_API_CODES: dict[tuple[bool, bool], str]` | `DOMESTIC_DAILY_ORDERS_ENDPOINTS: dict[bool, KisEndpoint]` |
| `FOREIGN_ORDER_MODIFY_API_CODES: dict[tuple[bool, MARKET_TYPE, Literal[...]], str]` | `FOREIGN_ORDER_MODIFY_ENDPOINTS: dict[tuple[MARKET_TYPE, Literal[...]], KisEndpoint]` |

`FOREIGN_ORDER_MODIFY` 는 **희소 표**입니다(상하이·베트남에 정정 주문 없음).
`.get()` 으로 조회하고 `None` 이면 예외를 내는 동작을 그대로 유지했습니다 —
키가 없다는 것 자체가 "그 시장은 지원하지 않는다"는 뜻입니다.

원본의 시장 설명 주석(`# 미국 정정 주문`)도 정규식으로 뽑아 보존했습니다.

### 커서 길이는 추측하지 않았습니다

`page_size` 는 요청의 `CTX_AREA_FK{n}` 필드명을 정합니다. 틀리면 연속조회가
엉뚱한 필드를 찾습니다. KIS 공식 예제를 조회해 확인했습니다.

| 엔드포인트 | 문서상 필드 | `page_size` |
|---|---|---|
| `inquire-daily-ccld` | `CTX_AREA_FK100` | 100 |
| `inquire-psbl-rvsecncl` | `CTX_AREA_FK100` | 100 |

> **범위 밖으로 남긴 것**: 업스트림 예제는 일별 체결내역에 `TTTC0081R` /
> `CTSC9215R` 를 쓰는데 이 저장소는 `TTTC8001R` / `CTSC9115R` 입니다.
> TR ID 변경은 동작 변화이므로 이 이슈에서 다루지 않았습니다. 별도 확인이
> 필요합니다.

---

## 5. C 판단 — 스펙을 `endpoints.py` 한 곳에 모을 것인가

**모으지 않기를 권합니다.** A·B 를 마치고 전체가 보이는 상태에서 판단했습니다.

```text
api/account/order.py         22        api/stock/daily_chart.py   2
api/account/order_modify.py  16        api/stock/day_chart.py     2
api/account/balance.py        3        api/stock/info.py          2
api/account/daily_order.py    3        api/stock/quote.py         2
api/account/orderable_amount.py 2      api/account/pending_order.py 2
                                       합계 56 스펙 / 10 파일 / 고유 TR 70개
```

56개 중 **38개가 주문 계열 두 파일의 dict 표**이고, 키가 `MARKET_TYPE` ·
`ORDER_TYPE` 같은 인접 정의에 묶여 있습니다. 한곳으로 옮기면 `endpoints.py`
가 `api/` 의 타입들을 거꾸로 import 하는 허브가 됩니다 — 이 저장소가 이슈
[#17](https://github.com/visualmoney/vm-stock-kis/issues/17)·[#18](https://github.com/visualmoney/vm-stock-kis/issues/18)
에서 없앤 바로 그 형태입니다.

**이점으로 들었던 "지원 TR 전체가 한눈에"는 이동 없이도 얻습니다.** 위 표는
AST 로 즉시 생성한 것입니다. 파일 배치를 바꾸는 대신 목록을 생성하면
두 성질을 모두 지킵니다.

---

## 변경 파일

- `src/vmkis/api/stock/quote.py` · `info.py` · `daily_chart.py` · `day_chart.py` — 시세 스펙 8개
- `src/vmkis/api/account/order.py` — 주간거래 주문 스펙
- `src/vmkis/api/account/order_modify.py` — 표 분해 + 주간거래 정정취소 스펙
- `src/vmkis/api/account/daily_order.py` — 표 분해 + `fetch(page=)` 결함 수정
- `src/vmkis/api/account/pending_order.py` — `fetch(page=)` 결함 수정
- `src/vmkis/client/endpoint.py` — 사라진 표를 가리키던 문서 갱신
- `tests/unit/api/stock/test_endpoints.py` — **신설**. 스펙 검증
- `tests/unit/api/test_call_contract.py` — **신설**. 호출부 시그니처 정적 검사
- `tests/unit/api/stock/test_info.py` · `test_daily_chart.py` — 목에 실제 `call` 바인딩
- `tests/unit/api/account/test_daily_order.py` — 동상 + 표 검증을 스펙 기준으로

## 테스트 결과

```text
985 passed, 22 skipped
TOTAL 90.69%  (게이트 90)
ruff check / format  통과
```

## 다음 할 일

- [ ] [#44](https://github.com/visualmoney/vm-stock-kis/issues/44) 페이징 헬퍼 —
      선행 조건이던 #43 이 끝났습니다. `call(page=...)` 이 커서 길이와
      `continuous` 를 처리하므로 헬퍼가 얇아집니다
- [ ] 일별 체결내역 TR ID 가 업스트림(`TTTC0081R`/`CTSC9215R`)과 다른 건 확인
- [ ] [#21](https://github.com/visualmoney/vm-stock-kis/issues/21) codegen —
      스펙이 전부 데이터가 됐으므로 착수 판단이 가능해졌습니다
