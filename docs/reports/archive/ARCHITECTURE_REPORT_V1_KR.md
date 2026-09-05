# Python-KIS 아키텍처 개선 보고서

**작성일**: 2025년 12월 10일
**대상**: 사용자 및 소프트웨어 엔지니어
**목적**: python-kis 라이브러리의 개선 방향 제시 및 실행 계획 수립

---

## 📋 목차

1. [요약](#요약)
2. [현황 분석](#현황-분석)
3. [개선 과제 및 우선순위](#개선-과제-및-우선순위)
4. [핵심 개선 사항 상세](#핵심-개선-사항-상세)
5. [`__init__.py`와 `types.py` 중복 문제 해결](#__init__py와-typespy-중복-문제-해결)
6. [단계별 실행 계획](#단계별-실행-계획)
7. [할 일 목록](#할-일-목록)
8. [결론 및 권장사항](#결론-및-권장사항)

---

## 요약

### 사용자 관점

python-kis는 한국투자증권 REST/WebSocket API를 타입 안전하게 래핑한 강력한 라이브러리입니다. 사용자 경험은 **설치 → 최소 설정 → 5분 내 `kis.stock("...").quote()` 호출**이 가능해야 하며, Protocol이나 Mixin 같은 내부 구조를 이해할 필요가 없어야 합니다.

### 엔지니어 관점

현재 설계는 견고합니다(Protocol 중심 아키텍처, Mixin 어댑터, DI via `KisObjectBase`, 동적 응답 변환, 이벤트 기반 WebSocket). 높은 확장성과 타입 안전성을 제공하지만, 초기 진입 복잡도가 높고 `__init__.py`와 `types.py` 간 중복 export가 존재하여 정리가 필요합니다.

**핵심 문제:**

- 초보자 진입 장벽이 높음 (Protocol/Mixin 이해 필요)
- 공개 API가 과도하게 노출됨 (150개 이상의 export)
- `__init__.py`와 `types.py`에서 타입이 중복 정의됨
- 통합 테스트 부재
- 문서화 부족 (빠른 시작 가이드, 예제 부족)

---

## 현황 분석

### 강점 ✅

1. **뛰어난 아키텍처 설계**
   - Protocol 기반 구조적 서브타이핑
   - Mixin 패턴으로 수평적 기능 확장
   - Lazy Initialization & 의존성 주입
   - 동적 응답 변환 시스템
   - 이벤트 기반 WebSocket 관리

2. **완벽한 타입 안전성**
   - 모든 함수/클래스에 Type Hint 제공
   - IDE 자동완성 100% 지원
   - Runtime 타입 체크 가능

3. **국내/해외 API 통합**
   - 동일한 인터페이스로 양쪽 시장 지원
   - 자동 라우팅 및 변환

4. **안정적인 라이센스**
   - MIT 라이센스 (상용 사용 가능)
   - 모든 의존성이 Permissive 라이센스

### 약점 ⚠️

1. **높은 초기 학습 곡선**

   ```text
   문제점:
   ├── Protocol과 Mixin 이해 필요
   ├── 30개 이상의 Protocol 정의 노출
   ├── 내부 구조(KisObjectBase, __kis_init__)까지 노출
   └── 150개 이상의 클래스가 __all__에 export됨
   ```

2. **타입 정의 중복**

   ```text
   pykis/__init__.py: 150개 이상 export
   pykis/types.py:    동일한 타입 재정의

   결과:
   ├── 유지보수 이중 부담
   ├── IDE에서 혼란 (같은 타입이 여러 곳에서 import 가능)
   └── 공개 API 범위 불명확
   ```

3. **문서화 부족**
   - README에 사용 예제만 존재
   - 아키텍처 설명 문서 없음
   - `examples/` 폴더 부재
   - 초보자용 빠른 시작 가이드 없음

4. **테스트 전략 미흡**

   ```text
   현재 상태:
   ├── 단위 테스트만 존재 (tests/unit/)
   ├── 통합 테스트 없음 (tests/integration/ 부재)
   ├── order.py 커버리지 76% (90% 목표 미달)
   └── fetch 내부 로직, 예외 처리 경로 미검증
   ```

---

## 개선 과제 및 우선순위

### 🔴 최우선 (High Impact, Low Effort)

| 번호 | 과제 | 예상 소요 | 영향도 |
|------|------|-----------|--------|
| 1 | `QUICKSTART.md` 작성 | 2시간 | ⭐⭐⭐⭐⭐ |
| 2 | `examples/01_basic/` 예제 5개 작성 | 4시간 | ⭐⭐⭐⭐⭐ |
| 3 | `pykis/__init__.py` export 정리 | 2시간 | ⭐⭐⭐⭐ |
| 4 | `pykis/public_types.py` 생성 (타입 중복 해소) | 3시간 | ⭐⭐⭐⭐ |
| 5 | `pykis/simple.py` 초보자 Facade 구현 | 4시간 | ⭐⭐⭐⭐ |

### 🟡 중요 (Medium Term)

| 번호 | 과제 | 예상 소요 | 영향도 |
|------|------|-----------|--------|
| 6 | `pykis/helpers.py` 및 `pykis/cli.py` 구현 | 6시간 | ⭐⭐⭐ |
| 7 | `tests/integration/` 구조 생성 및 테스트 작성 | 2일 | ⭐⭐⭐⭐ |
| 8 | `ARCHITECTURE.md` 상세 문서 작성 | 1일 | ⭐⭐⭐ |
| 9 | `CONTRIBUTING.md` 및 코딩 가이드라인 | 1일 | ⭐⭐⭐ |
| 10 | 의존성 라이센스 자동 체크 도구 추가 | 4시간 | ⭐⭐ |

### 🟢 장기 (Long Term)

| 번호 | 과제 | 예상 소요 | 영향도 |
|------|------|-----------|--------|
| 11 | Apache 2.0 라이센스 재검토 (법적 검토 + 기여자 동의) | 1개월 | ⭐⭐ |
| 12 | Jupyter Notebook 튜토리얼 5개 작성 | 2주 | ⭐⭐⭐ |
| 13 | 비디오 튜토리얼 제작 | 1개월 | ⭐⭐ |
| 14 | API 안정성 및 장기 지원 정책 문서화 | 1주 | ⭐⭐ |

---

## 핵심 개선 사항 상세

### 1. 초보자 진입 장벽 낮추기

#### 문제 상황

```python
# 현재: 사용자가 봐야 하는 것들
from pykis import (
    PyKis,
    KisObjectProtocol,        # ❌ 내부 구현
    KisMarketProtocol,         # ❌ 내부 구현
    KisProductProtocol,        # ❌ 내부 구현
    KisAccountProductProtocol, # ❌ 내부 구현
    # ... 150개 이상
)
```

#### 개선안

```python
# 개선 후: 사용자에게 필요한 것만
from pykis import (
    PyKis,      # 진입점
    KisAuth,    # 인증
    Quote,      # 시세 타입 (Type Hint용)
    Balance,    # 잔고 타입
    Order,      # 주문 타입
)

# 초보자용 단순 인터페이스
from pykis.simple import SimpleKIS
from pykis.helpers import create_client
```

#### 실행 방안

**A) `QUICKSTART.md` 작성**

```markdown
# 🚀 5분 빠른 시작

## 1단계: 설치
```bash
pip install python-kis
```

## 2단계: 인증 정보 설정

```python
from pykis import PyKis

kis = PyKis(
    id="YOUR_ID",
    account="00000000-01",
    appkey="YOUR_APPKEY",
    secretkey="YOUR_SECRET"
)
```

## 3단계: 시세 조회

```python
stock = kis.stock("005930")  # 삼성전자
quote = stock.quote()
print(f"{quote.name}: {quote.price:,}원")
```

**완료! Protocol? Mixin? 몰라도 됩니다! 🎉**

```text

**B) `examples/` 폴더 구조**
```

examples/
├── README.md
├── 01_basic/
│   ├── hello_world.py        # 가장 기본
│   ├── get_quote.py          # 시세 조회
│   ├── get_balance.py        # 잔고 조회
│   ├── place_order.py        # 주문하기
│   └── realtime_price.py     # 실시간 시세
├── 02_intermediate/
│   ├── order_management.py   # 주문 관리
│   ├── portfolio_tracking.py # 포트폴리오 추적
│   └── multi_account.py      # 멀티 계좌
└── 03_advanced/
    ├── custom_strategy.py    # 커스텀 전략
    └── custom_adapter.py     # 어댑터 확장

```text

**C) 초보자용 Facade 구현**
```python
# pykis/simple.py
"""초보자를 위한 단순화된 API"""

class SimpleKIS:
    """Protocol, Mixin 없이 간단하게 사용"""

    def __init__(self, id: str, account: str, appkey: str, secretkey: str):
        self._kis = PyKis(id=id, account=account,
                          appkey=appkey, secretkey=secretkey)

    def get_price(self, symbol: str) -> dict:
        """시세 조회 (딕셔너리 반환)"""
        quote = self._kis.stock(symbol).quote()
        return {
            "name": quote.name,
            "price": quote.price,
            "change": quote.change,
            "change_rate": quote.change_rate
        }

    def get_balance(self) -> dict:
        """잔고 조회"""
        balance = self._kis.account().balance()
        return {
            "cash": balance.deposits.get("KRW").amount,
            "stocks": [
                {"symbol": s.symbol, "name": s.name,
                 "qty": s.qty, "price": s.price}
                for s in balance.stocks
            ]
        }
```

### 2. 통합 테스트 추가

#### 현재 문제

```text
tests/
└── unit/              # 단위 테스트만 존재
    ├── api/
    ├── client/
    └── scope/

문제:
├── fetch() 내부 로직 미검증
├── 예외 처리 경로 미검증 (order.py 873-893줄 등)
├── 실제 API 응답 형식 변경 시 감지 불가
└── WebSocket 연결/재연결 시나리오 미검증
```

#### 개선안

```text
tests/
├── unit/              # 단위 테스트 (기존)
└── integration/       # 통합 테스트 (신규)
    ├── conftest.py    # 공통 fixture
    ├── api/
    │   ├── test_order_flow.py        # 주문 전체 플로우
    │   ├── test_balance_fetch.py     # 잔고 조회 전체
    │   └── test_exception_paths.py   # 예외 경로
    └── websocket/
        └── test_reconnection.py      # 재연결 시나리오
```

#### 실행 방안

```python
# tests/integration/conftest.py
import pytest
from unittest.mock import Mock
import responses

@pytest.fixture
def mock_kis_api():
    """API 응답 Mock"""
    with responses.RequestsMock() as rsps:
        # 토큰 발급
        rsps.add(responses.POST,
                 "https://openapi.koreainvestment.com:9443/oauth2/tokenP",
                 json={"access_token": "mock_token"})
        # 시세 조회
        rsps.add(responses.GET,
                 "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/inquire-price",
                 json={"output": {"stck_prpr": "70000"}})
        yield rsps

# tests/integration/api/test_order_flow.py
def test_complete_order_flow(mock_kis_api):
    """전체 주문 플로우 테스트"""
    kis = PyKis(id="test", account="12345678-01",
                appkey="test", secretkey="test")

    # 1. 시세 조회
    quote = kis.stock("005930").quote()
    assert quote.price > 0

    # 2. 매수 가능 금액 조회
    amount = kis.account().orderable_amount("005930")
    assert amount.orderable_qty > 0

    # 3. 주문 실행 (Mock)
    order = kis.stock("005930").buy(price=70000, qty=1)
    assert order.order_number is not None
```

---

## `__init__.py`와 `types.py` 중복 문제 해결

### 현황 분석

#### 문제점

```python
# pykis/__init__.py (현재)
__all__ = [
    "PyKis",
    "KisObjectProtocol",      # types.py와 중복
    "KisMarketProtocol",       # types.py와 중복
    "KisProductProtocol",      # types.py와 중복
    "KisAccountProtocol",      # types.py와 중복
    # ... 150개 이상 중복
]

# pykis/types.py (현재)
__all__ = [
    "KisObjectProtocol",       # __init__.py와 중복
    "KisMarketProtocol",       # __init__.py와 중복
    # ... 동일한 내용 재정의
]
```

**문제:**

1. 유지보수 부담 (같은 타입을 두 곳에서 관리)
2. IDE 혼란 (같은 타입이 여러 경로로 import 가능)
3. 공개 API 범위 불명확 (어떤 것이 공식 API인지 모호)
4. 버전 업그레이드 시 불일치 가능성

### 해결 방안: 3단계 리팩토링

#### Phase 1: 공개 타입 모듈 분리 (즉시 적용 가능)

**새 파일 생성: `pykis/public_types.py`**

```python
"""
사용자를 위한 공개 타입 정의

이 모듈은 사용자가 Type Hint를 작성할 때 필요한
타입 별칭만 포함합니다.

Example:
    >>> from pykis import Quote, Balance, Order
    >>>
    >>> def process_quote(quote: Quote) -> None:
    ...     print(f"가격: {quote.price}")
"""

from typing import TypeAlias

# 응답 타입 import
from pykis.api.stock.quote import KisQuoteResponse as _KisQuoteResponse
from pykis.api.account.balance import KisIntegrationBalance as _KisIntegrationBalance
from pykis.api.account.order import KisOrder as _KisOrder
from pykis.api.stock.chart import KisChart as _KisChart
from pykis.api.stock.order_book import KisOrderbook as _KisOrderbook

# 사용자 친화적인 별칭
Quote: TypeAlias = _KisQuoteResponse
"""시세 정보 타입"""

Balance: TypeAlias = _KisIntegrationBalance
"""계좌 잔고 타입"""

Order: TypeAlias = _KisOrder
"""주문 타입"""

Chart: TypeAlias = _KisChart
"""차트 데이터 타입"""

Orderbook: TypeAlias = _KisOrderbook
"""호가 정보 타입"""

__all__ = [
    "Quote",
    "Balance",
    "Order",
    "Chart",
    "Orderbook",
]
```

#### Phase 2: `__init__.py` 최소화 (하위 호환성 유지)

**개선된 `pykis/__init__.py`**

```python
"""
Python-KIS: 한국투자증권 API 라이브러리

빠른 시작:
    >>> from pykis import PyKis
    >>> kis = PyKis(id="ID", account="계좌", appkey="KEY", secretkey="SECRET")
    >>> quote = kis.stock("005930").quote()
    >>> print(f"{quote.name}: {quote.price:,}원")

고급 사용:
    - 아키텍처 문서: docs/ARCHITECTURE.md
    - Protocol 정의: pykis.types
    - 내부 구현: pykis._internal
"""

# === 핵심 클래스 ===
from pykis.kis import PyKis
from pykis.client.auth import KisAuth

# === 공개 타입 (Type Hint용) ===
from pykis.public_types import (
    Quote,
    Balance,
    Order,
    Chart,
    Orderbook,
)

# === 선택적: 초보자용 도구 ===
try:
    from pykis.simple import SimpleKIS
    from pykis.helpers import create_client
except ImportError:
    # 아직 구현되지 않은 경우 무시
    SimpleKIS = None
    create_client = None

# === 하위 호환성: 기존 import 지원 (Deprecated) ===
import warnings
from importlib import import_module

def __getattr__(name: str):
    """
    Deprecated된 이름에 대한 하위 호환성 제공

    예: from pykis import KisObjectProtocol
    → DeprecationWarning 발생 후 pykis.types.KisObjectProtocol 반환
    """
    # 내부 Protocol들 (Deprecated)
    _deprecated_internals = {
        "KisObjectProtocol": "pykis.types",
        "KisMarketProtocol": "pykis.types",
        "KisProductProtocol": "pykis.types",
        "KisAccountProtocol": "pykis.types",
        # ... 기타 deprecated 항목
    }

    if name in _deprecated_internals:
        module_name = _deprecated_internals[name]
        warnings.warn(
            f"'{name}'은(는) 패키지 루트에서 import하는 것이 deprecated되었습니다. "
            f"대신 'from {module_name} import {name}'을 사용하세요. "
            f"이 기능은 v3.0.0에서 제거될 예정입니다.",
            DeprecationWarning,
            stacklevel=2,
        )
        module = import_module(module_name)
        return getattr(module, name)

    raise AttributeError(f"module 'pykis' has no attribute '{name}'")

# === 공개 API ===
__all__ = [
    # 핵심 클래스
    "PyKis",
    "KisAuth",

    # 공개 타입
    "Quote",
    "Balance",
    "Order",
    "Chart",
    "Orderbook",

    # 초보자 도구 (선택적)
    "SimpleKIS",
    "create_client",
]

__version__ = "2.1.7"
```

#### Phase 3: `types.py` 역할 명확화

**개선된 `pykis/types.py`**

```python
"""
내부 타입 및 Protocol 정의

⚠️ 주의: 이 모듈은 라이브러리 내부용입니다.
일반 사용자는 `from pykis import Quote, Balance` 등을 사용하세요.

고급 사용자 및 기여자를 위한 내용:
    - 모든 Protocol 정의
    - 내부 타입 별칭
    - Mixin 인터페이스

안정성 보장:
    이 모듈의 내용은 minor 버전에서 변경될 수 있습니다.
    공개 API(`pykis/__init__.py`)만 semantic versioning을 보장합니다.

Example (고급):
    >>> from pykis.types import KisObjectProtocol
    >>>
    >>> class MyCustomObject(KisObjectProtocol):
    ...     def __init__(self, kis):
    ...         self.kis = kis
"""

# 기존 내용 유지
from typing import Protocol, runtime_checkable

@runtime_checkable
class KisObjectProtocol(Protocol):
    """내부용 객체 프로토콜"""
    @property
    def kis(self): ...

# ... 나머지 내용

__all__ = [
    # Protocol들
    "KisObjectProtocol",
    "KisMarketProtocol",
    # ... 기존 내용 유지
]
```

### 마이그레이션 전략

#### 1단계: 준비 (Breaking Change 없음)

```bash
# 1. public_types.py 생성
touch pykis/public_types.py

# 2. __init__.py 업데이트 (하위 호환성 유지)
# - 새로운 import 경로 추가
# - 기존 import 경로는 DeprecationWarning과 함께 유지

# 3. types.py 상단에 문서 추가
```

#### 2단계: 전환 기간 (2-3 릴리스)

```python
# 사용자가 deprecated 경로 사용 시
>>> from pykis import KisObjectProtocol
DeprecationWarning: 'KisObjectProtocol'은(는) 패키지 루트에서
import하는 것이 deprecated되었습니다. 대신 'from pykis.types
import KisObjectProtocol'을 사용하세요.

# 권장 사용법 안내
>>> from pykis.types import KisObjectProtocol  # 고급 사용자
>>> from pykis import Quote, Balance, Order     # 일반 사용자
```

#### 3단계: 정리 (v3.0.0)

```python
# __getattr__ 제거
# Deprecated import 경로 완전 삭제
# 공개 API만 유지
```

### 테스트 전략

**새 테스트 파일: `tests/unit/test_public_api_imports.py`**

```python
"""공개 API import 경로 테스트"""
import pytest
import warnings

def test_public_imports_work():
    """공개 API가 정상적으로 import되는지 확인"""
    from pykis import PyKis, KisAuth, Quote, Balance, Order

    assert PyKis is not None
    assert KisAuth is not None
    assert Quote is not None
    assert Balance is not None
    assert Order is not None

def test_deprecated_imports_warn():
    """Deprecated import 시 경고가 발생하는지 확인"""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        from pykis import KisObjectProtocol

        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "deprecated" in str(w[0].message).lower()

def test_types_module_still_works():
    """types 모듈에서 직접 import도 가능한지 확인"""
    from pykis.types import KisObjectProtocol, KisMarketProtocol

    assert KisObjectProtocol is not None
    assert KisMarketProtocol is not None

def test_public_types_module():
    """public_types 모듈이 제대로 동작하는지 확인"""
    from pykis.public_types import Quote, Balance, Order

    assert Quote is not None
    assert Balance is not None
    assert Order is not None
```

---

## 단계별 실행 계획

### Week 1: 즉시 적용 가능한 개선

#### Day 1-2: 문서화 기초

- [ ] `docs/` 폴더 생성
- [ ] `QUICKSTART.md` 작성
- [ ] `README.md` 상단에 "빠른 시작" 링크 추가
- [ ] 이 보고서 (`ARCHITECTURE_REPORT_KR.md`) 검토 및 수정

#### Day 3-4: 예제 코드

- [ ] `examples/01_basic/` 생성
- [ ] 5개 기본 예제 작성:
  - `hello_world.py` - 가장 기본
  - `get_quote.py` - 시세 조회
  - `get_balance.py` - 잔고 조회
  - `place_order.py` - 주문
  - `realtime_price.py` - 실시간 시세
- [ ] 각 예제에 상세한 주석 추가

#### Day 5-7: API 정리

- [ ] `pykis/public_types.py` 생성
- [ ] `pykis/__init__.py` 리팩토링 (하위 호환성 유지)
- [ ] Deprecation 메커니즘 구현
- [ ] `tests/unit/test_public_api_imports.py` 작성
- [ ] 전체 테스트 실행 및 확인

### Week 2: 초보자 도구 및 테스트

#### Day 1-3: 초보자용 인터페이스

- [ ] `pykis/simple.py` 구현
- [ ] `pykis/helpers.py` 구현:
  - `create_client()` - 환경변수/파일에서 자동 로드
  - `save_config_interactive()` - 대화형 설정 생성
- [ ] 관련 단위 테스트 작성

#### Day 4-5: CLI 도구

- [ ] `pykis/cli.py` 구현
- [ ] `pyproject.toml`에 script entry 추가
- [ ] CLI 테스트

#### Day 6-7: 통합 테스트

- [ ] `tests/integration/` 폴더 구조 생성
- [ ] `conftest.py` 작성 (공통 fixture)
- [ ] 3-5개 통합 테스트 작성:
  - 주문 전체 플로우
  - 잔고 조회 플로우
  - 예외 처리 경로
  - WebSocket 재연결

### Week 3-4: 고급 문서화

#### Week 3

- [ ] `ARCHITECTURE.md` 작성:
  - Protocol 설명
  - Mixin 패턴 설명
  - 아키텍처 다이어그램
  - 왜 이렇게 설계했는가?
- [ ] `CONTRIBUTING.md` 작성:
  - 코딩 스타일
  - Commit 가이드라인
  - PR 프로세스
  - 테스트 요구사항

#### Week 4

- [ ] `examples/02_intermediate/` 작성 (3개)
- [ ] `examples/03_advanced/` 작성 (2개)
- [ ] 각 예제에 README 추가
- [ ] API 안정성 정책 문서 작성

### Month 2: 고급 기능 및 자동화

#### Week 1-2: 라이센스 및 법적 검토

- [ ] 의존성 라이센스 자동 체크 스크립트
- [ ] `LICENSES/` 폴더 자동 생성
- [ ] Apache 2.0 전환 검토:
  - 법적 검토
  - 기여자 동의 수집
  - 마이그레이션 계획

#### Week 3-4: CI/CD 개선

- [ ] GitHub Actions 설정:
  - 단위 테스트 자동 실행
  - 커버리지 리포트 자동 생성
  - 통합 테스트 (선택적)
  - 라이센스 체크
- [ ] Pre-commit hooks 설정
- [ ] 커버리지 배지 추가

### Month 3+: 장기 개선

- [ ] Jupyter Notebook 튜토리얼 5개
- [ ] 비디오 튜토리얼 제작
- [ ] 다국어 문서 (영문)
- [ ] 커뮤니티 피드백 수집 및 반영
- [ ] 성능 최적화
- [ ] 추가 시장 지원 (선물/옵션 등)

---

## 할 일 목록

### ✅ 완료

- [x] daily_order.py 커버리지 개선 (78% → 84%)
- [x] pending_order.py 커버리지 개선 (79% → 90%)

### 🔄 진행 중

- [ ] order.py 커버리지 개선 (76% → 90%+)
  - 현재 76%, 목표 90%
  - 주요 누락: domestic_order, foreign_order, 예외 처리 경로

### 📋 대기 중 (우선순위순)

#### 최우선 (이번 주)

1. [ ] `QUICKSTART.md` 작성
2. [ ] `examples/01_basic/` 예제 5개 작성
3. [ ] `pykis/public_types.py` 생성
4. [ ] `pykis/__init__.py` export 정리 (하위 호환성 유지)
5. [ ] 공개 API import 테스트 작성

#### 높은 우선순위 (다음 주)

1. [ ] `pykis/simple.py` 초보자 Facade 구현
2. [ ] `pykis/helpers.py` 헬퍼 함수 구현
3. [ ] `pykis/cli.py` CLI 도구 구현
4. [ ] `tests/integration/` 구조 생성
5. [ ] 통합 테스트 3-5개 작성

#### 중간 우선순위 (2주 이내)

 1. [ ] `ARCHITECTURE.md` 상세 문서
 2. [ ] `CONTRIBUTING.md` 기여 가이드
 3. [ ] 의존성 라이센스 자동 체크
 4. [ ] `LICENSES/` 폴더 자동 생성
 5. [ ] CI/CD 파이프라인 개선

#### 낮은 우선순위 (1개월 이상)

 1. [ ] Apache 2.0 라이센스 재검토 및 전환
 2. [ ] Jupyter Notebook 튜토리얼
 3. [ ] 비디오 튜토리얼 제작
 4. [ ] API 안정성 정책 문서화
 5. [ ] 다국어 문서 (영문) 작성

---

## 결론 및 권장사항

### 핵심 메시지

> **Protocol과 Mixin은 라이브러리 내부 구현의 우아함을 위한 것입니다.**
> **사용자는 이것을 전혀 몰라도 사용할 수 있어야 합니다.**

### 즉시 실행 권장 사항

1. **`QUICKSTART.md` 작성** (2시간)
   - 5분 내 첫 API 호출 성공 목표
   - 최소한의 코드로 동작하는 예제

2. **`pykis/public_types.py` 생성** (3시간)
   - Quote, Balance, Order 등 핵심 타입만 export
   - `__init__.py` 정리하여 공개 API 명확화

3. **`examples/01_basic/` 5개 예제** (4시간)
   - 복사-붙여넣기로 바로 실행 가능한 코드
   - 상세한 주석 포함

4. **`pykis/simple.py` Facade** (4시간)
   - 초보자가 dict로 결과 받을 수 있는 인터페이스
   - Protocol/Mixin 없이 사용 가능

### 단계별 우선순위

```text
Phase 1 (1주): 문서 + 예제 + API 정리
  └─> 즉각적인 UX 개선

Phase 2 (2주): 초보자 도구 + 통합 테스트
  └─> 사용성 및 품질 향상

Phase 3 (1개월): 고급 문서 + 자동화
  └─> 장기 유지보수성 개선

Phase 4 (2개월+): 고급 기능 + 커뮤니티
  └─> 생태계 확장
```

### 성공 지표

**정량적:**

- ⏱️ Time to First Success: 5분 이내
- 📊 커버리지: order.py 90% 이상
- 📈 GitHub Stars: 현재 대비 50% 증가
- 💬 "어떻게 사용하나요?" 질문: 50% 감소

**정성적:**

- ✅ "이해하기 쉬웠다" 피드백
- ✅ "빠르게 시작할 수 있었다" 피드백
- ✅ "문서가 충분했다" 피드백

### 위험 및 완화 방안

| 위험 | 영향 | 완화 방안 |
|------|------|-----------|
| 하위 호환성 깨짐 | 높음 | Deprecation 경고 2 릴리스 유지 |
| 문서 작성 부담 | 중간 | 단계별로 나눠서 진행 |
| 커뮤니티 반발 | 낮음 | 기존 import 경로 유지 (deprecated) |
| 테스트 작성 시간 | 중간 | 핵심 경로부터 우선순위 |

### 최종 권고

1. **지금 당장 시작할 것:**
   - `QUICKSTART.md` 작성
   - `examples/01_basic/` 3개만이라도 작성
   - `pykis/__init__.py` export 50개로 줄이기

2. **다음 주까지:**
   - `pykis/public_types.py` 완성
   - `pykis/simple.py` 구현
   - 기본 통합 테스트 3개 작성

3. **한 달 안에:**
   - 전체 문서화 완료
   - 통합 테스트 커버리지 70% 이상
   - CI/CD 파이프라인 구축

이러한 개선을 통해 **초기 학습 곡선을 50% 이상 낮추고**, **유지보수 비용을 30% 절감**하며, **커뮤니티 기여를 2배 증가**시킬 수 있을 것으로 예상됩니다.

---

**문서 끝**

*작성자: Python-KIS 프로젝트 팀*
*최종 수정: 2025년 12월 10일*
