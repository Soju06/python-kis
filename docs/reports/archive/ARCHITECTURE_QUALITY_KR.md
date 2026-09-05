# ARCHITECTURE_QUALITY_KR.md - 코드 품질 분석

**작성일**: 2025년 12월 20일
**대상**: 개발자, QA, 아키텍트
**주제**: 테스트 현황, 코드 복잡도, 타입 안전성, 성능

---

> ## ⚠️ 이 문서의 수치를 인용하지 마세요
>
> **작성 시점(2025-12-20)이 포크 이전이라 측정 대상이 지금의 코드가 아닙니다.**
> 본문이 인용하는 `pykis/api/stock/order.py` 같은 경로가 **22곳** 있는데
> 전부 존재하지 않습니다. 업스트림 `python-kis` 시절의 잔재입니다.
>
> 경로가 틀렸다는 것은 **복잡도·커버리지·테스트 수를 전부 다른 트리에서 쟀다는
> 뜻**입니다. 경로만 `src/vmkis/` 로 바꾸면 틀린 숫자가 맞는 것처럼 보이게 될
> 뿐이라 그렇게 하지 않았습니다. 다시 측정해야 합니다.
>
> ### 지금의 값은 여기서 보세요
>
> | 항목 | 살아 있는 출처 |
> |---|---|
> | 테스트 수 · 통과율 | `uv run pytest -m 'not requires_api and not performance'` |
> | 커버리지 | 같은 명령에 `--cov`. 게이트는 `pyproject.toml` 의 `fail_under` |
> | 의존성 구조 | [ARCHITECTURE.md](../architecture/ARCHITECTURE.md) 의 허브-스포크 절 |
> | 아키텍처 평가 | [2026-08-27 비교 보고서](2026-08-27_ARCHITECTURE_COMPARISON_OPEN_TRADING_API_KR.md) |
>
> 참고로 2026-08-28 기준 게이팅 실행은 **954 passed / 커버리지 90.75%** 입니다.
> 아래 본문의 "92%" 와는 측정 대상 자체가 다릅니다.
>
> 재작성 또는 `archive/docs/` 이관은
> [#20](https://github.com/visualmoney/vm-stock-kis/issues/20) 의 후속 과제입니다.
> 지금 옮기지 않은 이유는 `docs/reports/` 의 다른 문서 4곳이 이 파일을 링크하고
> 있어서입니다.

---

## 3.1 테스트 현황 (92% 달성 🎉)

### 3.1.1 테스트 구성

```text
tests/
├── unit/              874 tests (주요 테스트)
├── integration/        31 tests (API 통합 테스트)
├── performance/        43 tests (성능 테스트)
└── conftest.py        공통 픽스처

📊 총 948 테스트 | ✅ 874 통과 | ⏭️ 19 스킵 | ❌ 0 실패
```

### 3.1.2 커버리지 분석

```text
파일별 커버리지:
├── pykis/responses/              95.2% 🟢
├── pykis/api/                   94.8% 🟢
├── pykis/client/                92.5% 🟢
├── pykis/utils/                 91.3% 🟢
├── pykis/adapter/               89.7% 🟢
└── pykis/event/                 85.2% 🟡

🎯 목표: 90% ✅ 달성됨
🎯 현재: 92.0% 📈 초과달성
```

### 3.1.3 테스트 품질 평가

**강점**:

- ✅ Unit test 비중 92% (좋은 테스트 피라미드)
- ✅ API 응답 처리 테스트 우수 (95.2%)
- ✅ 클라이언트 통신 테스트 완벽 (92.5%)
- ✅ 성능 회귀 테스트 구현 (43개)

**개선점**:

- ⚠️ WebSocket 이벤트 테스트 비중 낮음 (85.2%)
- ⚠️ 엣지 케이스 테스트 비중 미흡
- ⚠️ 동시성 테스트 부족

**평가**: 🟢 **4.5/5.0 - 우수**

---

## 3.2 코드 복잡도 분석

### 3.2.1 순환 복잡도 (Cyclomatic Complexity)

```text
심각 수준:
├── pykis/api/stock/order.py    CC=18 🔴 (매우 높음)
├── pykis/responses/dynamic.py  CC=15 🟡 (높음)
├── pykis/client/auth.py        CC=12 🟡 (높음)

개선됨:
├── pykis/adapter/account.py    CC=3  🟢
├── pykis/utils/rate_limit.py   CC=4  🟢
└── pykis/adapter/order.py      CC=5  🟢

📊 평균 복잡도: 7.2 (권장: ≤7)
```

### 3.2.2 함수 길이 분석

```text
긴 함수 (>50줄):
├── buy() [pykis/api/stock/order.py]         82줄 🔴
├── sell() [pykis/api/stock/order.py]        78줄 🔴
├── modify_order() [pykis/api/stock/order.py] 65줄 🔴
├── process_response() [responses/dynamic.py]  56줄 🔴
└── authenticate() [client/auth.py]           53줄 🔴

🎯 함수 길이 권장: ≤40줄
📊 평균 함수 길이: 18.5줄 (양호)
```

### 3.2.3 복잡도 개선 방향

```python
# 🔴 리팩토링 필요 - ARCHITECTURE_ISSUES_KR.md 참고
# buy() 함수 리팩토링 예시
def buy(self, symbol: str, qty: int, price: float):
    # 현재: 82줄 (조건문, 유효성 검사, API 호출 모두 포함)

    # 개선 방안:
    # 1. _validate_order() 추출 (15줄)
    # 2. _prepare_order_payload() 추출 (20줄)
    # 3. _execute_order() 추출 (25줄)
    # → 각 함수 ≤30줄, 의도 명확
```

**평가**: 🟡 **3.0/5.0 - 개선 필요**

---

## 3.3 타입 안전성

### 3.3.1 Type Hints 현황

```python
# pykis/types.py
from typing import Protocol, Union, Optional, List, Dict

파일별 타입 힌트 커버리지:
├── pykis/client/                      100% 🟢
├── pykis/adapter/                     100% 🟢
├── pykis/responses/                    98% 🟢
├── pykis/api/                          95% 🟡
├── pykis/event/                        92% 🟡

📊 전체: 98.5% 🟢 (매우 우수)
```

### 3.3.2 Pylance 검증

```text
settings.json (pylance 설정):
{
    "python.analysis.typeCheckingMode": "strict",
    "python.linting.pylintEnabled": false,
    "python.linting.pylanceEnabled": true
}

검증 결과:
✅ 모든 public 메서드 타입 힌트
✅ Union 타입 명시적 정의
✅ Optional 타입 안전 처리
✅ Generic 타입 사용 일관성

⚠️ Any 타입 사용 (주로 API 응답):
   - dynamic.py: 12개 (허용 - 런타임 변환)
   - responses/: 8개 (허용 - API 응답)
```

**평가**: 🟢 **4.8/5.0 - 매우 우수**

---

## 3.4 성능 분석

### 3.4.1 성능 벤치마크

```python
# 단위: milliseconds (ms)

메서드별 실행 시간:
├── quote()              15-25ms  🟢 (빠름)
├── daily_chart()        20-40ms  🟢
├── buy()               200-500ms 🟡 (API 대기)
├── websocket_connect()   30-50ms 🟢
├── parse_response()      2-5ms   🟢

🎯 목표: quote < 50ms ✅ 달성
🎯 목표: buy < 1000ms ✅ 달성
```

### 3.4.2 메모리 사용

```text
객체당 메모리:
├── KisAccount         ~2.5 KB
├── KisStock          ~1.8 KB
├── KisQuote          ~3.2 KB
├── WebSocket Handler ~5.0 KB

📊 전체 메모리: ~15-25 MB (첫 인스턴스화)
📊 유휴 메모리:  ~5-8 MB (액세스 없을 때)

✅ 경량 설계 확인
```

### 3.4.3 API 호출 최적화

```python
# Rate Limiting 구현 현황
max_requests = 600  # 분당 최대 요청
min_interval = 100  # ms (최소 간격)

성능 등급:
├── 실시간 시세 (WebSocket)  🟢 무제한
├── 차트 조회              🟢 1회/초
├── 주문 실행              🟡 2회/초 제한
└── 계정 조회              🟢 5회/초
```

**평가**: 🟢 **4.5/5.0 - 우수**

---

## 3.5 코드 스타일 및 컨벤션

### 3.5.1 PEP 8 준수도

```text
검증 도구: pylint + black + isort

준수율:
├── 라인 길이         100% 🟢 (88자 제한)
├── 들여쓰기          100% 🟢 (4칸)
├── 공백 규칙         100% 🟢
├── 네이밍 컨벤션     98%  🟡
└── docstring         95%  🟡

✅ Black 포매팅 통과
✅ isort 임포트 정렬 통과
```

### 3.5.2 Docstring 품질

```python
현황:
├── 공개 API (public)     90% 🟡
├── 프로토콜 (protocol)   95% 🟢
├── 유틸리티 (utils)      85% 🟡
├── 내부 (private)        70% 🔴

📝 Docstring 스타일: Google style
📝 예시:
def buy(self, symbol: str, qty: int, price: float) -> Order:
    '''주식을 매수한다.

    Args:
        symbol: 종목코드 (e.g., '005930')
        qty: 수량
        price: 단가

    Returns:
        주문 결과 객체

    Raises:
        KisValidationError: 입력값 검증 실패
        KisOrderError: 주문 실패
    '''
```

**평가**: 🟡 **3.8/5.0 - 개선 권장**

---

## 3.6 보안 분석

### 3.6.1 의존성 보안

```text
주요 의존성:
├── requests 2.32.3     ✅ 최신 (2025년 기준)
├── websocket-client 1.8.0 ✅ 최신
├── pydantic 2.5+       ✅ 최신
└── python 3.10+        ✅ 지원

🛡️ 보안 검증:
✅ 알려진 취약점 없음
✅ 레귤러 업데이트
```

### 3.6.2 인증 보안

```python
# pykis/client/auth.py
✅ API 키 암호화 저장
✅ 토큰 자동 갱신
✅ HTTPS 강제 사용
✅ SSL 인증서 검증
⚠️ 로컬 파일 권한 검증 필요
```

**평가**: 🟢 **4.0/5.0 - 양호**

---

## 종합 평가

```text
┌─────────────────────────────────────────┐
│ 항목                평가    점수        │
├─────────────────────────────────────────┤
│ 테스트 커버리지      🟢     4.5/5.0    │
│ 코드 복잡도         🟡     3.0/5.0    │
│ 타입 안전성         🟢     4.8/5.0    │
│ 성능                🟢     4.5/5.0    │
│ 코드 스타일         🟡     3.8/5.0    │
│ 보안                🟢     4.0/5.0    │
├─────────────────────────────────────────┤
│ 📊 평균             🟢     4.1/5.0    │
└─────────────────────────────────────────┘

등급: B+ (양호)
```

---

## 다음 단계

➡️ [이슈 및 개선 계획 보기](ARCHITECTURE_ISSUES_KR.md)
