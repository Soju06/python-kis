# 2026-08-28 - Issue #43 시세 계열 엔드포인트 스펙 이관

## 사용자 요청

> 이슈 #43 작업 진행해줘

## 분석

이슈 #43 은 **1~3단계 중 계좌 계열까지만** 끝난 상태([PR #48](https://github.com/visualmoney/vm-stock-kis/pull/48)) 로
열려 있습니다. 완료 기준 두 개 중 하나가 미충족입니다.

| 완료 기준 | 상태 |
|---|---|
| REST TR ID 삼항 분기 제거 | ✅ 9곳 → 0곳 |
| `domain="real"` 이 엔드포인트 정의로 이동 | ❌ **10곳 남음** |

### 작업 범위

**A. `domain="real"` 10곳 → 스펙으로**

```text
api/account/order.py:1396        해외 주간거래 주문 (TTTS6036U/TTTS6037U, POST)
api/stock/quote.py:651,701       FHKST01010100 · HHDFS76200200
api/stock/info.py:305,316,386    FHKST01010100 · HHDFS00000300 · CTPF1604R
api/stock/daily_chart.py:288,380 FHKST03010100 · HHDFS76240000
api/stock/day_chart.py:347,463   FHKST03010200 · HHDFS76950200
```

**B. 남은 표 2종 → 스펙으로**

- `DOMESTIC_DAILY_ORDERS_API_CODES` (`daily_order.py:609`)
- `FOREIGN_ORDER_MODIFY_API_CODES` (`order_modify.py:231`)

**C. (판단) 스펙을 `endpoints.py` 한 곳에 모을지** — A·B 를 마친 뒤 결정

### 착수 전 확인한 위험

**시세 테스트는 `fake_kis = Mock()` 를 씁니다.** 프로덕션이 `fetch` → `call` 로 바뀌면
`fake_kis.fetch.side_effect` 가 발동하지 않고 `fake_kis.call(...)` 이 새 `Mock` 을
돌려줍니다. 계좌 계열에서 쓴 해법(목에 실제 `VmKis.call` 바인딩)을 그대로 적용합니다.

영향 테스트: `test_info.py` 48곳 · `test_daily_chart.py` 65곳 (`fetch` 등장 기준)

## 계획

1. A — 시세/주간거래 10곳을 `KisEndpoint` + `call()` 로 이관
2. 테스트 목에 실제 `VmKis.call` 바인딩 (단언의 가치 유지)
3. B — 표 2종 분해. `FOREIGN_ORDER_MODIFY` 는 **키 없음 → 예외** 동작 유지 필수
4. 완료 기준 grep 2종 확인 + 전체 테스트
5. C 판단 및 일지 작성

## 결과

**완료.** 이슈 완료 기준 2개 모두 충족 — `domain="real"` 10곳 → 0곳,
문자열 TR 표 2종 → 0종. 스펙 56개 / 10파일 / 고유 TR 70개.

작업 중 **프로덕션 결함 2건**을 발견해 함께 고쳤습니다 — `fetch()` 에 없는
`page` 인자를 넘겨 첫 호출에서 죽던 공개 API 2개(국내 일별 체결내역·국내
미체결 주문). 가짜 `fetch` 가 `**kwargs` 를 받아 990건이 통과하는 동안
가려져 있었습니다.

C(스펙 위치)는 **모으지 않기를 권고**로 정리했습니다.

상세: [dev_logs/2026-08-28_12_issue43_quote_endpoints.md](../dev_logs/2026-08-28_12_issue43_quote_endpoints.md)
