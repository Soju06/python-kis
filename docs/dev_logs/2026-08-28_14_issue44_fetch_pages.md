# 2026-08-28 - Issue #44 페이지네이션 헬퍼 개발 일지

**대상 이슈**: [#44](https://github.com/visualmoney/vm-stock-kis/issues/44)
**선행**: [#43](https://github.com/visualmoney/vm-stock-kis/issues/43) 완료 —
`call(ep, page=...)` 이 커서 길이와 `continuous` 를 이미 처리합니다

---

## 요약

```text
994 passed, 22 skipped / TOTAL 91.39%  (게이트 90)
페이징 루프  8곳 -> 0곳 (차트 3곳은 대상 아님, 아래 §1)
api/account/  순 -104줄   kis.py  +88줄
```

---

## 1. 이슈의 전제가 절반만 맞았습니다

이슈는 루프 **11곳**을 한 종류로 보고 *"다른 것은 어느 필드에 누적하는가
한 줄뿐"* 이라고 적었습니다. 그리고 스스로 이렇게 경고했습니다.

> `daily_chart.py` / `day_chart.py` 를 먼저 확인하세요 — `api/account/` 의
> 4개와 누적 구조가 다를 수 있습니다. **다르면 헬퍼 시그니처가 달라집니다.**

**확인 결과 다릅니다.** 두 계열입니다.

| 계열 | 곳 | 무엇으로 페이징하나 | 종료 조건 |
|---|---|---|---|
| **KIS 커서 연속조회** | **8** | `KisPage` + `tr_cont` 헤더 | `is_last` 하나 |
| **날짜/시간 커서 반복** | 3 | **`KisPage` 를 아예 안 씀.** 봉 시각에서 도출 | 이질적 4종 |

차트 계열의 종료 조건은 이렇습니다.

```python
if not result.bars: break
last = result.bars[-1].time.date()
if cursor and cursor < last: break
if isinstance(start, timedelta): start = (chart.bars[0].time - start).date()
if start and last <= start: break
cursor = last - period_delta        # 다음 커서를 직접 계산
```

해외 당일차트는 아예 `for i in range(FOREIGN_MAX_PERIODS)` 로 `NMIN` 을
늘려 가며 **시각별 dedup** 을 합니다. 같은 추상화가 아닙니다.

**억지로 한 헬퍼에 밀어 넣으면 역효과입니다.** 8곳만 덮었습니다.

> 이슈 본문의 "11개 루프 이관"과 완료 기준
> `git grep -c 'while True' -- 'src/vmkis/api/*'` **= 0** 은 이 발견에 따라
> 충족되지 않습니다. 차트 3곳은 그대로입니다.

---

## 2. 설계 — `merge` 콜백

이슈가 제시한 세 안 중 하나를 골라야 했습니다.

| 방식 | 판정 |
|---|---|
| **`merge` 콜백 주입** | **채택** |
| 응답 클래스에 `__merge__` | 기각 |
| 누적 필드명을 문자열로 | 기각 |

`merge` 를 고른 이유:

- 이슈의 **"제외" 항목**이 *"응답 클래스의 필드 구조 변경"* 을 배제했습니다.
  콜백은 응답 8종을 건드리지 않습니다
- `__merge__` 는 호출부가 한 줄 짧아지는 대신 **누적 규칙이 루프에서 멀어집니다.**
  [#45](https://github.com/visualmoney/vm-stock-kis/issues/45) 가 경고한 것과
  같은 종류의 타협입니다
- 문자열 필드명은 타입 검사를 잃습니다. 타입 힌트는 이 라이브러리의 핵심 강점입니다

### Before / After

```python
# 이전 — 8곳에 같은 모양이 복사돼 있었다
page = page or KisPage.first()
first = None

while True:
    result = self.call(_DOMESTIC_BALANCE, params={...}, form=[account], page=page,
                       response_type=KisDomesticBalance(account_number=account))
    if first is None:
        first = result
    else:
        first.stocks.extend(result.stocks)      # <- 여기만 달랐다
    if not continuous or result.is_last:
        break
    page = result.next_page

return first

# 이후
return self.fetch_pages(
    _DOMESTIC_BALANCE,
    params={...},
    form=[account],
    response_type=lambda: KisDomesticBalance(account_number=account),
    page=page,
    continuous=continuous,
    merge=lambda first, more: first.stocks.extend(more.stocks),
)
```

| 파일 | 순 변화 |
|---|---|
| `balance.py` | −28 |
| `daily_order.py` | −28 |
| `order_profit.py` | −20 |
| `pending_order.py` | −28 |

---

## 3. 밟은 함정 — `response_type` 은 팩토리여야 합니다

호출부를 보면 응답 객체를 **루프 안에서** 만들고 있었습니다.

```python
while True:
    result = self.call(..., response_type=KisDomesticBalance(account_number=account))
```

헬퍼로 옮기면서 인자를 밖으로 뺄 때 **왜 안에 있었는지** 확인해야 했습니다.
`responses/dynamic.py:257` 이 답입니다.

```python
object = transform_type if isinstance(transform_type, KisDynamic) else transform_type()
```

**인스턴스를 넘기면 그 인스턴스에 그대로 파싱합니다.** 하나를 돌려 쓰면 모든
페이지가 같은 객체가 되고, `first is result` 가 되어
`merge(first, result)` 가 **자기 자신을 이어붙입니다.** 결과가 조용히
불어납니다.

그래서 `fetch_pages` 는 **팩토리만** 받고, 인스턴스를 주면 즉시 `TypeError`
로 막습니다. 메시지에 올바른 사용법을 넣었습니다.

```text
response_type 에는 인스턴스가 아니라 팩토리를 주세요.
인스턴스를 주면 모든 페이지가 같은 객체에 파싱되어 결과가 불어납니다.
예: response_type=lambda: KisDomesticBalance(account_number=account)
```

---

## 4. 무한 루프 상한

이슈가 요구한 항목입니다. 서버가 `is_last` 를 끝내 주지 않거나 커서가
진행하지 않으면 루프가 끝나지 않습니다. **조용히 도는 것보다 명시적으로
실패하는 편이 낫습니다.**

`MAX_PAGES = 100` 을 기본값으로 두고 넘기면 예외를 냅니다.

> `KisInternalError` 를 쓰지 않았습니다. 그 예외의 베이스 `KisException` 이
> 생성자에서 `Response` 를 요구하는데 이 지점에는 건넬 응답이 없습니다.
> (`KisInternalError` 는 저장소 어디에서도 쓰인 적이 없습니다.)
> `RuntimeError` 를 씁니다.

---

## 5. 테스트 — 페이징 루프를 처음으로 직접 검증합니다

이슈가 지적한 그대로였습니다. **8곳을 복사해 두고 그 루프를 검증하는 테스트가
하나도 없었습니다.** 한 곳으로 모았으니 한 번만 검증합니다.

`tests/unit/client/test_fetch_pages.py` 9건 — 단일 페이지 · 다중 페이지 누적 ·
`continuous=False` · 상한 · 첫 페이지의 `continuous` 헤더 · 스펙 해석 ·
커서 길이 · 인스턴스 거부.

### 되돌려 확인했습니다

통과만 보면 아무것도 검사하지 않는 상태를 못 잡습니다.

| 변이 | 결과 |
|---|---|
| `continuous`/`is_last` 를 무시해 첫 페이지만 반환 | **4 failed** |
| `is_last` 를 무시 (무한 루프) | **5 failed** |
| 첫 페이지에도 `continuous=True` 전송 | **1 failed** |
| `merge` 호출 생략 (누적 안 함) | **1 failed** |

기존 목 4곳에도 실제 `VmKis.fetch_pages` 를 바인딩했습니다(#43 에서 `call`
에 했던 것과 같은 방식). `fetch(api=...)` 단언이 그대로 살고 페이징 루프까지
함께 검증됩니다.

> `test_balance.py` 의 `monkeypatch.setattr(bal, "KisPage", ...)` 는 이제
> **발동하지 않습니다** — 첫 페이지를 `fetch_pages` 가 만들기 때문입니다.
> 남기면 오해를 부르므로 지우고 이유를 적었습니다.

---

## 6. #43 잔여 2곳도 함께 정리

`order_profit.py` 는 `domain="real"` 이 없어 #43 의 대상 목록에 없었지만
`fetch` 를 직접 쓰고 있었습니다. 페이징 이관을 하려면 스펙이 필요하므로
같이 만들었습니다.

```python
_DOMESTIC_ORDER_PROFITS  TTTC8715R  page_size=100
_FOREIGN_ORDER_PROFITS   TTTS3039R  page_size=200
```

커서 길이는 기존 호출부의 `.to(100)` / `.to(200)` 에서 그대로 옮겼습니다.

---

## 변경 파일

- `src/vmkis/kis.py` — `fetch_pages()` · `TPagination` · `MAX_PAGES`
- `src/vmkis/api/account/balance.py` · `daily_order.py` · `pending_order.py` — 각 2곳 이관
- `src/vmkis/api/account/order_profit.py` — 스펙 2종 + 2곳 이관
- `tests/unit/client/test_fetch_pages.py` — **신설**
- `tests/unit/api/account/test_balance.py` · `test_daily_order.py` · `test_order_profit.py` — 목에 실제 `fetch_pages` 바인딩

## 테스트 결과

```text
994 passed, 22 skipped
TOTAL 91.39%  (게이트 90)
ruff check / format  통과
```

## 다음 할 일

- [ ] 차트 계열 3곳은 **별건입니다.** 필요하다면 "날짜 커서 반복"이라는
      다른 추상화로 따로 다뤄야 합니다. 지금 묶으면 역효과입니다
- [ ] `tests/unit/utils/test_rate_limit_accuracy.py::test_rate_limiter_thread_safety`
      가 커버리지 실행에서 간헐 실패합니다. 타이밍 의존으로 보이며 이슈 등록
      여부는 미정입니다
