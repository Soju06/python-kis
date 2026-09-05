# 2026-08-28 - Issue #44 페이지네이션 헬퍼

## 사용자 요청

> #44 진행해줘

## 분석

[#43](https://github.com/visualmoney/vm-stock-kis/issues/43) 이 닫히면서 선행
조건이 해소됐습니다. `call(ep, page=...)` 이 커서 길이와 `continuous` 를 이미
처리하므로 헬퍼가 더 얇아집니다.

### 이슈가 "먼저 정하라"고 한 것

**`daily_chart.py` / `day_chart.py` 를 먼저 확인하세요 — `api/account/` 의
4개와 누적 구조가 다를 수 있습니다.**

확인 결과 **다릅니다.** 11개 루프가 한 종류가 아니라 두 계열이었습니다.

| 계열 | 곳 | 성격 |
|---|---|---|
| **KIS 커서 연속조회** | 8 | `KisPage` · `continuous` · `is_last` · `next_page`. 골격 동일 |
| **날짜/시간 커서 반복** | 3 | `KisPage` 를 **아예 쓰지 않음.** 봉 시각에서 다음 커서를 도출 |

차트 계열은 종료 조건이 이질적입니다 — `not result.bars` · `cursor < last` ·
`start` 가 `timedelta` 일 때 재계산 · 해외 당일차트는 시각별 dedup.
`for i in range(FOREIGN_MAX_PERIODS)` 는 `NMIN` 을 늘리는 완전히 다른 기제입니다.

**따라서 헬퍼는 8곳만 덮습니다.**

### 설계 선택

| 방식 | 판정 |
|---|---|
| `merge` 콜백 주입 | **채택.** 응답 클래스 무변경 — 이슈의 "제외" 항목을 지킴 |
| 응답 클래스에 `__merge__` | 기각. 응답 8종 수정. #45 가 경고한 타입 경험 훼손 우려 |
| 누적 필드명을 문자열로 | 기각. 타입 검사 안 됨 |

## 계획

1. `order_profit.py` 의 남은 `fetch` 2곳에 스펙 부여 (#43 잔여)
2. `VmKis.fetch_pages()` 구현 — 상한 포함
3. 8개 루프 이관
4. 헬퍼 자체 테스트 + **되돌려 확인**

## 결과

**완료.** `api/account/` 순 −104줄, `kis.py` +88줄.

`response_type` 이 팩토리여야 하는 이유를 발견해 타입 가드로 막았습니다 —
인스턴스를 넘기면 **모든 페이지가 같은 객체에 파싱되어 결과가 불어납니다.**

상세: [dev_logs/2026-08-28_14_issue44_fetch_pages.md](../dev_logs/2026-08-28_14_issue44_fetch_pages.md)
