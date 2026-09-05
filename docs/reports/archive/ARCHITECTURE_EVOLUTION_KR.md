# ARCHITECTURE_EVOLUTION_KR.md - v3.0.0 진화 및 공개 API 정리

**작성일**: 2025년 12월 20일
**대상**: 마이그레이션 담당자, 기여자, 고급 사용자
**주제**: v3.0.0 Breaking Changes, 공개 API 정리, 마이그레이션 가이드

---

## 6.1 v3.0.0 주요 변경점

### 6.1.1 공개 API 정리 (154개 → 20개)

**변경 개요**:

```text
현재 (v2.1.x)          v3.0.0 (변경 후)
────────────────────────────────────────────
154개 export        →   20개 export
혼란스러운 네비게이션  →   명확한 진입점
내부/공개 구분 모호  →   엄격한 구분
```

---

## 6.2 v3.0.0 공개 API 최종 목록

### 6.2.1 필수 핵심 클래스 (5개)

```python
# pykis/__init__.py v3.0.0

# 1. 메인 진입점
from .kis import PyKis
"PyKis"                    # 주 클래스

# 2. 인증
from .client.auth import KisAuth
"KisAuth"                  # 인증 관리

# 3. Scope (진입점)
from .client.account import KisAccount
from .adapter.stock import KisStock
from .adapter.derivatives import KisFutures, KisOptions
"KisAccount"
"KisStock"
"KisFutures"
"KisOptions"

# 5개 진입점
__all__ = [
    "PyKis",
    "KisAuth",
    "KisAccount",
    "KisStock",
    "KisFutures",
    "KisOptions",
    # ... (총 20개)
]
```

### 6.2.2 응답 타입 클래스 (10개)

```python
# pykis/__init__.py v3.0.0

from .responses.types import (
    # 주문 관련
    Order,              # 주문 정보
    OrderModify,        # 주문 수정

    # 시세 관련
    Quote,              # 현재가
    Chart,              # 캔들

    # 계좌 관련
    Balance,            # 잔고
    BalanceSummary,     # 잔고 요약
    Position,           # 보유 종목

    # 기타
    MarketInfo,         # 시장 정보
    WebsocketData,      # WebSocket 데이터
    Exception,          # 예외
]

__all__ = [
    # ... 핵심 5개
    # 응답 타입 10개
    "Order",
    "OrderModify",
    "Quote",
    "Chart",
    "Balance",
    "BalanceSummary",
    "Position",
    "MarketInfo",
    "WebsocketData",
    "KisException",

    # ... (총 20개)
]
```

### 6.2.3 예외 클래스 (5개)

```python
# pykis/__init__.py v3.0.0

from .exceptions import (
    KisException,           # 기본 예외
    KisValidationError,     # 입력값 오류
    KisOrderError,          # 주문 오류
    KisAuthError,           # 인증 오류
    KisNetworkError,        # 네트워크 오류
)

__all__ = [
    # ... 15개
    "KisException",
    "KisValidationError",
    "KisOrderError",
    "KisAuthError",
    "KisNetworkError",
    # (총 20개)
]
```

---

## 6.3 비공개 API (내부용, pykis.types 권장)

### 6.3.1 내부 Protocol & Adapter

```python
# 더 이상 pykis.__init__에서 export 안 함
# 필요 시 pykis.types 또는 해당 모듈에서 직접 import

# 비공개 처리
- KisObjectProtocol          # pykis.client.object
- KisQuotableAccount         # pykis.adapter.account.quote
- KisOrderableAccount        # pykis.adapter.account.order
- KisWebsocketQuotableProduct  # pykis.adapter.product.websocket
- ... (130개 이상)
```

### 6.3.2 내부 유틸리티

```python
# 비공개 처리 (pykis._internal에서만 사용)
- KisDynamic                 # 응답 변환 (내부 구현)
- KisAdapter                 # Adapter 베이스 (내부)
- RateLimiter               # API 제한 (내부)
- WebsocketClient           # WebSocket (내부)
```

---

## 6.4 마이그레이션 가이드

### 6.4.1 v2.1.x → v3.0.0 마이그레이션

#### 시나리오 1: 간단한 주식 시세 조회

**Before (v2.1.x)**:

```python
from pykis import PyKis, KisStock, KisQuotableProduct

kis = PyKis("config.json")
stock = kis.stock("005930")
quote = stock.quote()
print(quote.price)
```

**After (v3.0.0) - 동일함**:

```python
from pykis import PyKis

kis = PyKis("config.json")
stock = kis.stock("005930")
quote = stock.quote()
print(quote.price)  # 사용 코드는 변화 없음
```

**변경 사항**:

- ✅ `KisStock` import 제거 가능 (내부적으로 처리)
- ✅ `KisQuotableProduct` import 제거 (이제 비공개)
- ✅ 실제 코드는 수정 불필요

#### 시나리오 2: 주문 실행

**Before (v2.1.x)**:

```python
from pykis import (
    PyKis,
    KisAccount,
    KisOrderableAccount,
    Order,
)

kis = PyKis("config.json")
account = kis.account(1234567890)
order = account.buy("005930", 10, 70000)
```

**After (v3.0.0)**:

```python
from pykis import PyKis, Order

kis = PyKis("config.json")
account = kis.account(1234567890)
order = account.buy("005930", 10, 70000)
```

**변경 사항**:

- ✅ `KisAccount`, `KisOrderableAccount` 제거 가능
- ✅ `Order` 타입 import 여전히 가능
- ✅ 실제 호출 코드는 변화 없음

#### 시나리오 3: WebSocket 실시간 시세

**Before (v2.1.x)**:

```python
from pykis import (
    PyKis,
    KisStockScope,
    KisWebsocketQuotableProduct,
)

kis = PyKis("config.json")
domestic = kis.domestic

@domestic.on_quote
def on_quote(quote):
    print(quote)
```

**After (v3.0.0) - 동일함**:

```python
from pykis import PyKis

kis = PyKis("config.json")
domestic = kis.domestic

@domestic.on_quote
def on_quote(quote):
    print(quote)
```

**변경 사항**:

- ✅ Decorator 사용 방식은 유지
- ✅ 내부 Adapter 클래스는 비공개화되나 동작은 동일

---

## 6.5 Breaking Changes 목록

### 6.5.1 직접 영향을 미치는 변경

```text
순번    변경 사항                              영향도   대응
────────────────────────────────────────────────────────────
1     공개 API 154 → 20개                    중간    auto-import 호환성 유지
2     KisObjectProtocol 비공개화            낮음    내부 구현 용도만
3     KisDynamic 비공개화                   낮음    API 응답만 사용
4     내부 Adapter 클래스 비공개화          낮음    Scope로만 접근
────────────────────────────────────────────────────────────
```

### 6.5.2 간접 영향 (주의 필요)

```text
변경 사항                               v2.1.x 코드   v3.0.0 결과
────────────────────────────────────────────────────────────────
pykis/types.py 정리                    import types  호환성 유지
Dynamic 응답 처리 최적화               quote.price   동일하게 동작
주문 메서드 리팩토링                   buy()         시그니처 동일
────────────────────────────────────────────────────────────────
```

---

## 6.6 공개 API 정책

### 6.6.1 공개 API 판별 기준

```python
# v3.0.0부터 적용되는 정책

"공개 API" = "pykis/__init__.py의 __all__에 명시된 항목"

✅ 공개 API로 간주:
   - 최상위 클래스 (PyKis, KisAuth, Order)
   - 주요 응답 타입 (Quote, Balance, Chart)
   - 공개 예외 (KisException, KisOrderError)
   - 문서화된 메인 메서드

❌ 내부 구현 (비공개):
   - Protocol (KisObjectProtocol, ...)
   - Adapter/Mixin (KisQuotableAccount, ...)
   - 동적 변환 (KisDynamic, ...)
   - 유틸리티 (RateLimiter, ...)

☑️ 내부 구현 접근 방법 (필요 시):
   from pykis._internal import ...
   from pykis.types import ...
```

### 6.6.2 버전 지정 정책

```text
공개 API 변경:
├─ 신규 추가        → Minor 버전 (v3.1.0)
├─ Deprecation 추가  → Minor 버전 (v3.1.0)
├─ Deprecation 제거  → Major 버전 (v4.0.0)
└─ 삭제              → Major 버전 (v4.0.0)

내부 구현 변경:
├─ 모두 Patch 버전 (v3.0.1)에서 허용
└─ 공개 API 호출 결과는 동일 유지
```

---

## 6.7 마이그레이션 타임라인

### 6.7.1 단계별 계획

```text
v2.1.7 (현재)
├─ 기능: v3.0.0 준비 경고 추가
└─ 상태: 모든 기존 코드 동작함

v2.2.0 (호환성 레이어)
├─ 기능: Deprecation 경고 추가
├─ 기능: pykis._legacy 모듈 제공
└─ 상태: v2.1.x 코드 여전히 작동하나 경고 표시

v3.0.0 (Breaking Change)
├─ 변경: 공개 API 20개로 축소
├─ 변경: 내부 구현 비공개화
└─ 상태: v2.1.x 코드는 import 오류 발생

v3.1.0 (안정화)
├─ 기능: 신규 공개 API 추가 (필요시)
└─ 상태: v3.0.0으로 마이그레이션 완료
```

### 6.7.2 지원 기간

```text
버전         출시        종료 지원    보안 패치
──────────────────────────────────────────────
v2.1.x      2025-06    2026-03    ✅ 있음
v2.2.x      2025-12    2026-06    ✅ 있음
v3.0.x      2026-01    2027-01    ✅ 있음
v3.1.x      2026-02    2027-06    ✅ 있음
v4.0.0      2027-01    (미정)     ✅ 있음
```

---

## 6.8 공개 API 구체 목록

### 6.8.1 최종 **all** 정의

```python
# pykis/__init__.py v3.0.0

__all__ = [
    # 메인 클래스 (1개)
    "PyKis",

    # 인증 (1개)
    "KisAuth",

    # Scope 클래스 (4개)
    "KisAccount",
    "KisStock",
    "KisFutures",
    "KisOptions",

    # 응답 타입 (10개)
    "Order",
    "OrderModify",
    "Quote",
    "Chart",
    "Balance",
    "BalanceSummary",
    "Position",
    "MarketInfo",
    "WebsocketData",
    "OrderBook",

    # 예외 (4개)
    "KisException",
    "KisValidationError",
    "KisOrderError",
    "KisAuthError",

    # 총 20개
]
```

### 6.8.2 pykis.types 유지

```python
# pykis/types.py v3.0.0

# 하위 호환성을 위해 유지
# 그러나 pykis/__init__.py와 구분된 방식

from .responses.types import *  # 응답 타입만
from .exceptions import *       # 예외 타입만

# 내부 구현은 별도:
from .client.object import KisObjectProtocol  # 내부 구현 (타입 체킹용)
```

---

## 6.9 예제 코드

### 6.9.1 v3.0.0 권장 사용법

```python
# ✅ v3.0.0에서 권장하는 import 방식

# 간단한 사용
from pykis import PyKis

# 타입 체킹이 필요한 경우
from pykis import PyKis, Quote, Order, Balance

# 예외 처리
from pykis import (
    PyKis,
    KisException,
    KisOrderError,
    KisValidationError,
)

# 실제 사용
kis = PyKis("config.json")
stock = kis.stock("005930")
quote: Quote = stock.quote()

try:
    order: Order = kis.account(acc_no).buy("005930", 10, 70000)
except KisOrderError as e:
    print(f"주문 실패: {e}")
```

### 6.9.2 비권장 (내부 구현 직접 접근)

```python
# ❌ v3.0.0에서 비권장 (작동하지 않음)

from pykis import (
    KisObjectProtocol,      # ❌ 비공개
    KisDynamic,             # ❌ 비공개
    KisOrderableAccount,    # ❌ 비공개
)

# 대신 필요시:
from pykis._internal import KisDynamic  # 내부용 (권장 안 함)
from pykis.types import KisObjectProtocol  # 타입 체킹만
```

---

## 6.10 FAQ (마이그레이션 관련)

### Q1: 내 v2.1.x 코드가 v3.0.0에서 동작할까요?

**A**: 대부분 동작합니다.

- ✅ `PyKis.stock()` → 동일
- ✅ `account.buy()` → 동일
- ✅ `@domestic.on_quote` → 동일
- ❌ 내부 클래스를 직접 import한 경우만 수정 필요

### Q2: 어떤 코드를 수정해야 할까요?

**A**: 다음과 같은 import만 확인하세요:

```python
# ❌ 수정 필요
from pykis import (
    KisObjectProtocol,
    KisDynamic,
    # ... 154개 중 처음 5개 제외
)

# ✅ 그냥 두어도 됨
from pykis import PyKis, Order, Quote
```

### Q3: 내부 구현에 접근해야 하면요?

**A**: `pykis._internal`에서 import하세요:

```python
# v3.0.0
from pykis._internal import KisDynamic
from pykis.types import KisObjectProtocol

# (권장하지 않음 - 파기될 수 있음)
```

### Q4: 마이그레이션 비용은?

**A**: 매우 낮습니다:

- 일반적인 사용: 0줄 수정
- 내부 클래스 사용: 1-2줄 수정 (경로 변경)

---

## 결론

v3.0.0은 **공개 API 정리를 통해 접근성을 개선**하는 메이저 업데이트입니다.

```text
Before (v2.1.x)         After (v3.0.0)
154개 항목 혼란   →     20개 항목 명확
사용자 어려움     →     쉬운 학습곡선
유지보수 부담     →     명확한 구조
```

**마이그레이션은 간단합니다** - 대부분의 코드는 변화가 없습니다.

---

## 참고 문서

- [ARCHITECTURE_ROADMAP_KR.md](ARCHITECTURE_ROADMAP_KR.md) - v3.0.0 일정
- [ARCHITECTURE_ISSUES_KR.md](ARCHITECTURE_ISSUES_KR.md) - 기술적 변경사항
- [README.md](../../README.md) - 프로젝트 개요
