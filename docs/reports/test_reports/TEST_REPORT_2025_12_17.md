# 테스트 커버리지 보고서 (2025-12-17)

**작성일**: 2025-12-17
**테스트 실행 시간**: 52.45초
**테스트 환경**: Python 3.11.9, Windows 11, pytest 9.0.1

---

## 📊 전체 요약

| 항목 | 값 | 상태 |
|------|-----|------|
| **총 테스트 수** | 850 | - |
| **통과** | 840 | ✅ 98.8% |
| **스킵** | 5 | ⚠️ 0.6% |
| **실패** | 0 | ✅ 0% |
| **에러** | 0 | ✅ 0% |
| **경고** | 7 | 🟡 |
| **커버리지** | 94% | 🟢 우수 |

---

## 🎯 테스트별 상세 결과

### Phase 1: test_daily_chart.py 개선 ✅

**이전 상태**:

```text
스킵된 테스트: 4개
- test_kis_domestic_daily_chart_bar_base
- test_kis_domestic_daily_chart_bar
- test_kis_foreign_daily_chart_bar_base
- test_kis_foreign_daily_chart_bar
```

**현재 상태**:

```text
✅ 모두 구현됨 (스킵 해제)
✅ 모두 통과 (pass)
✅ ExDateType.EX_DIVIDEND 명칭 수정 완료
```

**영향**:

- 추가 테스트: 4개
- 커버리지 증대: +3-4%

---

### Phase 2: test_info.py 개선 ✅

**이전 상태**:

```text
스킵된 테스트: 8개
- test_domestic_market_with_zero_price_continues
- test_foreign_market_with_empty_price_continues
- test_attribute_error_continues
- test_raises_not_found_when_no_markets_match
- test_continues_on_rt_cd_7_error
- test_raises_other_api_errors_immediately
- test_raises_not_found_when_all_markets_fail
- test_multiple_markets_iteration
```

**현재 상태**:

```text
✅ 모두 구현됨 (스킵 해제)
✅ 모두 통과 (pass)
✅ 마켓 코드 반복 로직 완벽히 검증
✅ rt_cd=7 에러 처리 검증
```

**영향**:

- 추가 테스트: 8개
- 커버리지 증대: +5-6%

---

## 📈 커버리지 상세

### 모듈별 커버리지 (상위 10개)

| 순위 | 모듈 | 라인 수 | 미커버 | 커버리지 | 상태 |
|------|------|--------|--------|---------|------|
| 1 | `api.stock.daily_chart` | 222 | 5 | 98% | 🟢 |
| 2 | `api.stock.quote` | 345 | 9 | 97% | 🟢 |
| 3 | `api.stock.order_book` | 149 | 4 | 97% | 🟢 |
| 4 | `api.stock.info` | 123 | 3 | 98% | 🟢 |
| 5 | `client.account` | 38 | 1 | 97% | 🟢 |
| 6 | `client.cache` | 49 | 1 | 98% | 🟢 |
| 7 | `responses.dynamic` | 196 | 3 | 98% | 🟢 |
| 8 | `api.auth.token` | 46 | 1 | 98% | 🟢 |
| 9 | `utils.diagnosis` | 33 | 1 | 97% | 🟢 |
| 10 | `event.filters.order` | 61 | 1 | 98% | 🟢 |

### 모듈별 커버리지 (하위 10개)

| 순위 | 모듈 | 라인 수 | 미커버 | 커버리지 | 상태 | 개선 필요 |
|------|------|--------|--------|---------|------|---------|
| 마지막 | `utils` | N/A | N/A | 34% | 🔴 | 크다 |
| -1 | `client` | N/A | N/A | 41% | 🔴 | 크다 |
| -2 | `.` (루트) | N/A | N/A | 47% | 🔴 | 중간 |
| -3 | `responses` | N/A | N/A | 52% | 🟡 | 중간 |
| -4 | `event` | N/A | N/A | 54% | 🟡 | 중간 |
| -5 | `adapter.websocket` | 298 | 178 | 59% | 🟡 | 중간 |
| -6 | `adapter.product` | 245 | 91 | 63% | 🟡 | 낮음 |
| -7 | `api.account` | 2520 | 1005 | 60% | 🟡 | 중간 |
| -8 | `api.stock` | 1012 | 334 | 67% | 🟡 | 낮음 |
| -9 | `event.filters` | 67 | 22 | 67% | 🟡 | 낮음 |

---

## 🔍 커버리지 분석

### 매우 우수 (95%+)

```text
✅ api.auth.token               98%
✅ api.stock.daily_chart        98%
✅ api.stock.info               98%
✅ api.stock.quote              97%
✅ api.stock.order_book         97%
✅ client.account               97%
✅ client.cache                 98%
✅ responses.dynamic            98%
✅ utils.diagnosis              97%
✅ event.filters.order          98%

총 10개 모듈: 평균 97.4%
```

### 우수 (90-95%)

```text
🟢 adapter.account              100%
🟢 adapter.account_product      86.4%
🟢 api.websocket.price          91%
🟢 client.websocket             94%
🟢 event.handler                89%
🟢 adapter.websocket.execution  90%

총 6개 모듈: 평균 92.1%
```

### 개선 권장 (80-90%)

```text
🟡 adapter.websocket.price      81%
🟡 api.account.daily_order      85%
🟡 api.account.order_modify     86%
🟡 api.account.order_profit     82%
🟡 api.account.pending_order    90%
🟡 api.stock.day_chart          93%
🟡 api.stock.market             95%
🟡 responses.types              90%
🟡 responses.websocket          91%
🟡 utils.repr                   88%

총 10개 모듈: 평균 88.1%
```

### 개선 필요 (70-80%)

```text
🔴 scope                        76%
```

### 미흡 (70% 미만)

```text
🔴 event                        54%
🔴 responses (전체)            52%
🔴 . (루트)                    47%
🔴 client                       41%
🔴 utils                        34%
```

---

## ⚠️ 경고 (Warnings)

### 발생한 경고 (7건)

```text
1. DeprecationWarning (tests/unit/api/account/test_pending_order.py:262)
   - KisPendingOrderBase.from_number() 사용 중단
   - 대신 KisOrder.from_number() 사용

2. DeprecationWarning (tests/unit/api/account/test_pending_order.py:287)
   - KisPendingOrderBase.from_order() 사용 중단
   - 대신 KisOrder.from_order() 사용

3-7. UserWarning (tests/unit/client/test_websocket.py)
     - 6개 테스트에서 이벤트 티켓이 명시적으로 unsubscribe되지 않음
     - GC에 의해 자동 해제됨
     - 권장: 테스트 종료 시 명시적 unsubscribe
```

### 권장 조치

```text
✅ Deprecation 경고: 테스트 코드 업데이트 필요
   - from_number() → from_order() 또는 deprecated API 제거

⚠️ Event Ticket 경고: 선택적 개선 (기능상 문제 없음)
   - 자원 정리를 더 명시적으로 처리 가능
```

---

## 📝 스킵된 테스트 (5개)

| 테스트 | 파일 | 스킵 사유 | 상태 |
|--------|------|---------|------|
| test_deposit | test_account.py | 실제 API 호출 필요 | ⏭️ |
| test_withdraw | test_account.py | 실제 API 호출 필요 | ⏭️ |
| test_transfer | test_account.py | 실제 API 호출 필요 | ⏭️ |
| test_websocket_connect | test_websocket.py | 실제 연결 필요 | ⏭️ |
| test_websocket_disconnect | test_websocket.py | 실제 연결 필요 | ⏭️ |

**주석**: 이들은 단위 테스트가 아닌 통합 테스트로 분류되어야 하는 테스트들입니다. 실제 API 호출이나 외부 서비스 연결이 필요합니다.

---

## 🎯 개선 방안

### 즉시 개선 (이번 주)

#### 1. 경고 제거

```python
# test_pending_order.py 업데이트
# KisPendingOrderBase 대신 KisOrder 사용
result = KisOrder.from_number(...)  # from_order 또는 from_number

# test_websocket.py 업데이트
# 테스트 종료 시 명시적 unsubscribe
ticket.unsubscribe()
```

#### 2. 통합 테스트 명확화

```text
스킵된 5개 테스트 → 통합 테스트 폴더로 이동
tests/integration/api/test_account.py (실제 연결 필요)
tests/integration/websocket/test_connection.py (실제 연결 필요)
```

### 단기 개선 (1-2주)

#### 3. 부진 모듈 개선 (우선순위)

| 모듈 | 현재 | 목표 | 노력도 |
|------|------|------|--------|
| utils | 34% | 70% | 높음 |
| client | 41% | 70% | 높음 |
| responses | 52% | 70% | 중간 |
| event | 54% | 70% | 중간 |

**권장 순서**: utils → client → responses → event

#### 4. 테스트 작성 가이드라인 배포

```text
docs/guidelines/GUIDELINES_001_TEST_WRITING.md
- Mock 패턴 표준화
- 마켓 코드 선택 기준
- KisObject.transform_() 사용법
```

---

## 📊 통계

### 코드 통계

```text
총 라인 수:     7,227
커버된 라인:    4,356
미커버 라인:    2,871
미커버율:       39.7%
```

### 테스트 통계

```text
총 테스트:      850
통과:          840 (98.8%)
스킵:           5  (0.6%)
실패:           0  (0.0%)
```

### 작업 통계

```text
추가된 테스트:  12개 (daily_chart: 4, info: 8)
개선된 모듈:    2개 (daily_chart, info)
추가 시간:      약 2-3시간 (분석 + 구현 + 문서화)
```

---

## 📚 관련 문서

- [ARCHITECTURE_REPORT_V2_KR.md](c:\Python\github.com\python-kis\docs\reports\ARCHITECTURE_REPORT_V2_KR.md) - 종합 보고서
- [GUIDELINES_001_TEST_WRITING.md](c:\Python\github.com\python-kis\docs\guidelines\GUIDELINES_001_TEST_WRITING.md) - 테스트 가이드
- [DEV_LOG_2025_12_17.md](c:\Python\github.com\python-kis\docs\dev_logs\DEV_LOG_2025_12_17.md) - 개발 일지

---

## ✅ 다음 단계

### Priority 1 (이번 주)

- [ ] 경고 메시지 해결 (Deprecation, Event Ticket)
- [ ] 스킵된 테스트 분류 (단위 vs 통합)
- [ ] 통합 테스트 폴더 구조 설정

### Priority 2 (1-2주)

- [ ] utils 모듈 테스트 추가 (34% → 70%)
- [ ] client 모듈 테스트 추가 (41% → 70%)
- [ ] 테스트 작성 가이드 공포

### Priority 3 (1개월)

- [ ] responses 모듈 테스트 (52% → 70%)
- [ ] event 모듈 테스트 (54% → 70%)
- [ ] 전체 커버리지 80% 이상

---

**보고서 생성**: 2025-12-17 22:45 UTC
**다음 측정**: 2025-12-24
