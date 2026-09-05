# 섹션 3: 공개 타입 모듈 분리 정책 (핵심 전략)

## 3.1 문제 정의

### 3.1.1 __init__.py 과다 노출 현황

__현재 상태__:

```python
# pykis/__init__.py
__all__ = [
    # 총 154개 항목 export
    "PyKis",                      # ✅ 필요
    "KisAuth",                    # ✅ 필요
    "KisObjectProtocol",          # ❌ 내부 구현
    "KisMarketProtocol",          # ❌ 내부 구현
    "KisProductProtocol",         # ❌ 내부 구현
    "KisAccountProductProtocol",  # ❌ 내부 구현
    # ... 150개 이상 내부 구현 노출
]
```

__문제점__:

- 🔴 초보자가 어떤 것을 import해야 할지 혼란
- 🔴 IDE 자동완성 목록이 지나치게 길어짐 (150+개)
- 🔴 공개 API와 내부 구현의 경계 모호
- 🔴 하위 호환성 관리 부담 (모든 154개를 유지해야 함)
- 🔴 마이그레이션 불가능 (항목 이동 시 깨짐)

### 3.1.2 types.py 중복 정의 문제

__현재 상태__:

```python
# pykis/__init__.py
__all__ = [
    "KisObjectProtocol",   # 154개 항목 export
    "KisMarketProtocol",
    # ... (중복)
]

# pykis/types.py
__all__ = [
    "KisObjectProtocol",   # 동일한 154개 항목 재정의
    "KisMarketProtocol",
    # ... (중복)
]
```

__문제점__:

- 🔴 유지보수 이중 부담: 같은 타입을 두 파일에서 관리
- 🔴 불일치 리스크: 한쪽만 갱신되면 import 경로마다 다른 결과
- 🔴 공개 API 경로 불명확: `from pykis import X` vs `from pykis.types import X` 어느 것이 공식?
- 🔴 버전 업그레이드 시 불일치 가능성 높음

---

## 3.2 해결 방안: 3단계 리팩토링

### 3.2.1 Phase 1: 공개 타입 모듈 분리 (즉시 적용, Breaking Change 없음)

__목표__: 사용자가 import할 필요한 타입만 `public_types.py`로 분리

__신규 파일 생성: `pykis/public_types.py`__

```python
"""
사용자를 위한 공개 타입 정의

이 모듈은 사용자가 Type Hint를 작성할 때 필요한
핵심 타입 별칭만 포함합니다. Protocol, Adapter,
내부 구현 타입은 포함하지 않습니다.

예제:
    >>> from pykis import Quote, Balance, Order
    >>>
    >>> def process_quote(quote: Quote) -> None:
    ...     print(f"가격: {quote.price}")

    >>> def on_balance_update(balance: Balance) -> None:
    ...     print(f"잔고: {balance.deposits}")
"""

from typing import TypeAlias

# ============================================================================
# 응답 타입 Import (내부 경로는 underscore로 표시)
# ============================================================================

from pykis.api.stock.quote import KisQuoteResponse as _KisQuoteResponse
from pykis.api.account.balance import KisIntegrationBalance as _KisIntegrationBalance
from pykis.api.account.order import KisOrder as _KisOrder
from pykis.api.stock.chart import KisChart as _KisChart
from pykis.api.stock.order_book import KisOrderbook as _KisOrderbook
from pykis.api.stock.market import KisMarketInfo as _KisMarketInfo
from pykis.api.stock.trading_hours import KisTradingHours as _KisTradingHours

# ============================================================================
# 사용자 친화적인 타입 별칭 (짧은 이름, Docstring 포함)
# ============================================================================

Quote: TypeAlias = _KisQuoteResponse
"""
시세 정보 타입

예제:
    quote = kis.stock("005930").quote()
    print(quote.name)      # "삼성전자"
    print(quote.price)     # 65000
    print(quote.change)    # 500
"""

Balance: TypeAlias = _KisIntegrationBalance
"""
계좌 잔고 타입 (국내/해외 통합)

예제:
    balance = kis.account().balance()
    print(balance.cash)           # 현금
    print(balance.stocks)         # 보유 종목 리스트
    print(balance.deposits)       # 예수금 (원/달러/위안 등)
"""

Order: TypeAlias = _KisOrder
"""
주문 정보 타입

예제:
    order = kis.stock("005930").buy(price=65000, qty=10)
    print(order.order_number)     # 주문번호
    print(order.status)           # 주문 상태
    print(order.qty)              # 주문 수량
"""

Chart: TypeAlias = _KisChart
"""
차트 데이터 타입 (일/주/월 OHLCV)

예제:
    charts = kis.stock("005930").chart("D")  # 일봉
    for bar in charts:
        print(bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume)
"""

Orderbook: TypeAlias = _KisOrderbook
"""
호가 정보 타입 (매수/매도 호가 정보)

예제:
    orderbook = kis.stock("005930").orderbook()
    print(orderbook.ask_prices)    # 매도호가 [최우선, 2차, 3차, ...]
    print(orderbook.bid_prices)    # 매수호가
    print(orderbook.ask_volumes)   # 매도 수량
    print(orderbook.bid_volumes)   # 매수 수량
"""

MarketInfo: TypeAlias = _KisMarketInfo
"""
시장 정보 타입 (종목 상장 정보, 업종 분류 등)

예제:
    info = kis.stock("005930").info()
    print(info.market)             # 상장 시장 (KOSPI)
    print(info.sector)             # 업종
    print(info.listed_date)        # 상장일
"""

TradingHours: TypeAlias = _KisTradingHours
"""
장 시간 정보 타입 (개장/폐장/주말/휴장)

예제:
    hours = kis.stock("005930").trading_hours()
    print(hours.is_open_now)       # 지금 장중인가?
    print(hours.next_open_time)    # 다음 개장 시간
    print(hours.close_time)        # 폐장 시간
"""

# ============================================================================
# 공개 API
# ============================================================================

__all__ = [
    # 주요 응답 타입 (사용자가 자주 사용)
    "Quote",
    "Balance",
    "Order",
    "Chart",
    "Orderbook",

    # 추가 타입
    "MarketInfo",
    "TradingHours",
]
```

### 3.2.2 Phase 2: `__init__.py` 최소화 (하위 호환성 유지)

__목표__: 공개 API를 20개 이하로 축소하되, 기존 코드 계속 동작

__개선된 `pykis/__init__.py`__

```python
"""
Python-KIS: 한국투자증권 API 라이브러리

빠른 시작:
    >>> from pykis import PyKis
    >>> kis = PyKis(id="ID", account="계좌", appkey="KEY", secretkey="SECRET")
    >>> quote = kis.stock("005930").quote()
    >>> print(f"{quote.name}: {quote.price:,}원")

공개 타입 사용:
    >>> from pykis import Quote, Balance, Order
    >>>
    >>> def on_quote(quote: Quote) -> None:
    ...     print(f"새로운 가격: {quote.price}")

고급 사용 (내부 구조 확장):
    - 아키텍처 문서: docs/ARCHITECTURE.md
    - Protocol 정의: pykis.types (v3.0.0에서 제거 예정)
    - 내부 구현: pykis._internal
"""

# ============================================================================
# 핵심 클래스 (공개 API)
# ============================================================================

from pykis.kis import PyKis
from pykis.client.auth import KisAuth

# ============================================================================
# 공개 타입 (Type Hint용) - public_types.py에서 재export
# ============================================================================

from pykis.public_types import (
    Quote,
    Balance,
    Order,
    Chart,
    Orderbook,
    MarketInfo,
    TradingHours,
)

# ============================================================================
# 선택적: 초보자용 도구 (v2.2.0 이상에서 추가)
# ============================================================================

try:
    from pykis.simple import SimpleKIS
    from pykis.helpers import create_client, save_config_interactive
except ImportError:
    # 아직 구현되지 않은 경우 무시
    SimpleKIS = None
    create_client = None
    save_config_interactive = None

# ============================================================================
# 하위 호환성: 기존 import 지원 (Deprecated)
#
# v2.2.0 (현재): __getattr__ 로 DeprecationWarning 발생
# v2.3.0~v2.9.0: 유지 (업데이트 권고)
# v3.0.0: 제거
# ============================================================================

import warnings
from importlib import import_module
from typing import Any

def __getattr__(name: str) -> Any:
    """
    Deprecated 이름에 대한 하위 호환성 제공

    사용자가 deprecated 경로로 import 시:
    - DeprecationWarning 발생
    - pykis.types에서 해당 항목 반환

    예:
        >>> from pykis import KisObjectProtocol  # ⚠️ Deprecated
        DeprecationWarning: 'KisObjectProtocol'은(는) 패키지 루트에서
        import하는 것이 deprecated되었습니다. 대신 'from pykis.types
        import KisObjectProtocol'을 사용하세요. 이 기능은 v3.0.0에서
        제거될 예정입니다.
    """

    # 내부 Protocol들 (Deprecated)
    _deprecated_internals = {
        # Protocol들
        "KisObjectProtocol": "pykis.types",
        "KisMarketProtocol": "pykis.types",
        "KisProductProtocol": "pykis.types",
        "KisAccountProtocol": "pykis.types",
        "KisAccountProductProtocol": "pykis.types",
        "KisWebsocketQuotableProtocol": "pykis.types",

        # Adapter들 (위험)
        "KisQuotableAccount": "pykis.adapter.account.quote",
        "KisOrderableAccount": "pykis.adapter.account.order",

        # 기타
        "TIMEX_TYPE": "pykis.types",
        "COUNTRY_TYPE": "pykis.types",
        # ... 기타 모든 내부 항목
    }

    if name in _deprecated_internals:
        module_name = _deprecated_internals[name]
        warnings.warn(
            f"from pykis import {name}은(는) deprecated되었습니다. "
            f"대신 'from {module_name} import {name}'을 사용하세요. "
            f"이 기능은 v3.0.0에서 제거될 예정입니다.",
            DeprecationWarning,
            stacklevel=2,
        )
        module = import_module(module_name)
        return getattr(module, name)

    raise AttributeError(f"module 'pykis' has no attribute '{name}'")

# ============================================================================
# 공개 API 정의
# ============================================================================

__all__ = [
    # === 핵심 클래스 ===
    "PyKis",           # 진입점
    "KisAuth",         # 인증

    # === 공개 타입 (Type Hint용) ===
    "Quote",           # 시세
    "Balance",         # 잔고
    "Order",           # 주문
    "Chart",           # 차트
    "Orderbook",       # 호가
    "MarketInfo",      # 시장정보
    "TradingHours",    # 장시간

    # === 초보자 도구 ===
    "SimpleKIS",            # 단순 인터페이스
    "create_client",        # 자동 클라이언트 생성
    "save_config_interactive",  # 대화형 설정 저장
]

__version__ = "2.1.7"
```

### 3.2.3 Phase 3: `types.py` 역할 명확화

__목표__: types.py를 고급 사용자 및 개발자 전용으로 재정의

__개선된 `pykis/types.py`__

```python
"""
내부 타입 및 Protocol 정의

⚠️ 주의: 이 모듈은 라이브러리 내부용입니다.
일반 사용자는 아래 문서를 따르세요.

누가 사용해야 하나?:

    1. 일반 사용자
       └─ from pykis import Quote, Balance, Order 사용

    2. Type Hint를 작성하는 개발자
       └─ from pykis import Quote, Balance 사용 (공개 타입)

    3. 고급 사용자 / 기여자 (확장)
       ├─ from pykis.types import KisObjectProtocol  (Protocol)
       ├─ from pykis.adapter.* import * (Adapter)
       └─ docs/ARCHITECTURE.md 문서 읽기

버전 정책:
    - v2.2.0~v2.9.x: 모든 항목 유지 (이 모듈 계속 import 가능)
    - v3.0.0: 이 모듈 제거 (직접 import 불가)

    ⚠️ v3.0.0부터 'from pykis.types import ...'은 작동하지 않습니다.
       고급 사용자는 'from pykis.adapter.* import ...' 등으로 변경해야 합니다.

예제 (고급 사용자):
    >>> from pykis.types import KisObjectProtocol
    >>>
    >>> class MyCustomObject(KisObjectProtocol):
    ...     def __init__(self, kis):
    ...         self.kis = kis
    ...
    ...     def my_method(self):
    ...         return self.kis.fetch(...)
"""

from typing import Protocol, runtime_checkable

# ============================================================================
# Protocol 정의 (구조적 서브타이핑 지원)
# ============================================================================

@runtime_checkable
class KisObjectProtocol(Protocol):
    """모든 API 객체가 준수해야 하는 프로토콜"""

    @property
    def kis(self) -> "PyKis":
        """PyKis 인스턴스 참조"""
        ...

@runtime_checkable
class KisMarketProtocol(Protocol):
    """시장 관련 API 객체의 프로토콜"""

    def quote(self) -> "Quote":
        """시세 조회"""
        ...

@runtime_checkable
class KisProductProtocol(Protocol):
    """상품(종목) 관련 API 객체의 프로토콜"""

    @property
    def symbol(self) -> str:
        """종목 코드"""
        ...

# ============================================================================
# 기존 내용 유지 (하위 호환성)
# ============================================================================

# ... 나머지 기존 Protocol, TypeAlias, 상수 정의들 계속 유지

__all__ = [
    # Protocol들 (고급 사용자용)
    "KisObjectProtocol",
    "KisMarketProtocol",
    "KisProductProtocol",

    # ... 기존 모든 항목 유지 (하위 호환성)
]
```

---

## 3.3 마이그레이션 전략 (3단계, 하위 호환성 100% 유지)

### 3.3.1 1단계: 준비 (Breaking Change 없음) - 즉시 적용

```bash
# 1. public_types.py 생성
# 2. __init__.py 업데이트
#    - 새로운 import 경로 추가
#    - 기존 import 경로는 DeprecationWarning과 함께 유지
# 3. types.py 문서 업데이트 (역할 명확화)
```

__사용자 영향__: ✅ __없음__ (모든 기존 코드 계속 동작)

### 3.3.2 2단계: 전환 기간 (v2.2.0~v2.9.0) - 2-3 릴리스

```python
# 기존 코드 (계속 동작하지만 경고 발생)
>>> from pykis import KisObjectProtocol
DeprecationWarning: from pykis import KisObjectProtocol은(는)
deprecated되었습니다. 대신 'from pykis.types import KisObjectProtocol'을
사용하세요. 이 기능은 v3.0.0에서 제거될 예정입니다.

# 권장 마이그레이션
>>> from pykis.types import KisObjectProtocol      # 고급 사용자
>>> from pykis import Quote, Balance, Order         # 일반 사용자
```

__사용자 영향__: 🟡 __경고 메시지만__ (기능은 그대로)

__업데이트 가이드__:

| 기존 코드 | 신규 코드 | 대상 | 우선순위 |
|----------|----------|------|----------|
| `from pykis import Quote` | `from pykis import Quote` | 모두 | 필수 없음 (이미 작동) |
| `from pykis import KisObjectProtocol` | `from pykis.types import KisObjectProtocol` | 고급 사용자 | 선택 |
| `from pykis import PyKis` | `from pykis import PyKis` | 모두 | 필수 없음 (그대로) |

### 3.3.3 3단계: 정리 (v3.0.0) - Breaking Change

```python
# v3.0.0: Deprecated 경로 완전 제거

# ✅ 동작
from pykis import PyKis, Quote, Balance
from pykis.types import KisObjectProtocol  # 여전히 동작
from pykis.adapter.account.quote import KisQuotableAccount  # 직접 접근

# ❌ 작동 불가 (error 발생)
from pykis import KisObjectProtocol  # AttributeError!
```

__사용자 영향__: 🔴 __Breaking Change__ (업데이트 필수)

---

## 3.4 테스트 전략

### 3.4.1 신규 테스트: `tests/unit/test_public_api_imports.py`

```python
"""공개 API import 경로 테스트"""
import pytest
import warnings


class TestPublicImports:
    """공개 API가 정상적으로 작동하는지 검증"""

    def test_core_classes_import(self):
        """핵심 클래스 import 가능"""
        from pykis import PyKis, KisAuth
        assert PyKis is not None
        assert KisAuth is not None

    def test_public_types_import(self):
        """공개 타입 import 가능"""
        from pykis import Quote, Balance, Order, Chart, Orderbook
        assert Quote is not None
        assert Balance is not None
        assert Order is not None
        assert Chart is not None
        assert Orderbook is not None

    def test_public_types_module_direct_import(self):
        """public_types 모듈에서 직접 import 가능"""
        from pykis.public_types import Quote, Balance, Order
        assert Quote is not None
        assert Balance is not None
        assert Order is not None

    def test_deprecated_imports_warn(self):
        """Deprecated import 시 경고 발생"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # ⚠️ deprecated 경로
            from pykis import KisObjectProtocol

            assert len(w) >= 1
            assert any(issubclass(x.category, DeprecationWarning) for x in w)
            assert any("deprecated" in str(x.message).lower() for x in w)

    def test_types_module_still_works(self):
        """types 모듈에서 직접 import도 가능 (고급 사용자)"""
        from pykis.types import KisObjectProtocol, KisMarketProtocol
        assert KisObjectProtocol is not None
        assert KisMarketProtocol is not None

    def test_backward_compatibility(self):
        """기존 코드 계속 동작"""
        # v2.0.x 스타일 (여전히 동작)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            from pykis import PyKis
            from pykis import KisObjectProtocol  # deprecated

            assert PyKis is not None
            assert KisObjectProtocol is not None


class TestTypeConsistency:
    """같은 타입이 모든 경로에서 동일한지 확인"""

    def test_quote_type_consistency(self):
        """Quote 타입이 모든 경로에서 동일"""
        from pykis import Quote as Q1
        from pykis.public_types import Quote as Q2

        assert Q1 is Q2

    def test_balance_type_consistency(self):
        """Balance 타입이 모든 경로에서 동일"""
        from pykis import Balance as B1
        from pykis.public_types import Balance as B2

        assert B1 is B2


class TestPublicAPISize:
    """공개 API 크기 확인"""

    def test_public_api_exports_minimal(self):
        """공개 API가 20개 이하"""
        from pykis import __all__

        assert len(__all__) <= 20, \
            f"공개 API 항목이 너무 많습니다 (현재: {len(__all__)}개, 목표: 20개 이하)"

    def test_public_api_contains_essentials(self):
        """공개 API에 필수 항목 포함"""
        from pykis import __all__

        essentials = {"PyKis", "KisAuth", "Quote", "Balance", "Order"}
        assert essentials.issubset(set(__all__)), \
            f"필수 항목 누락: {essentials - set(__all__)}"
```

### 3.4.2 기존 테스트 호환성 유지

```python
# tests/unit/test_compatibility.py
"""기존 코드 호환성 확인"""
import warnings


def test_old_style_import_still_works():
    """v2.0.x 스타일 import 계속 동작"""
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")

        # 이 코드는 계속 동작해야 함
        from pykis import (
            PyKis,
            KisAuth,
            Quote,
            Balance,
            Order,
            Chart,
            Orderbook,
        )

        assert PyKis is not None
        assert all([KisAuth, Quote, Balance, Order, Chart, Orderbook])
```

---

## 3.5 롤아웃 계획

### 3.5.1 v2.2.0 (권장)

```bash
# 릴리스 계획
- public_types.py 추가
- __init__.py 리팩토링 (__getattr__ 추가)
- types.py 문서 업데이트
- CHANGELOG에 Migration Guide 기재
- 예시 코드 업데이트
```

### 3.5.2 v2.3.0~v2.9.x (유지보수)

```bash
# 각 릴리스마다
- Deprecation Warning 계속 표시
- CHANGELOG에 마이그레이션 상기
- 예제/문서에서 신규 방식 사용
```

### 3.5.3 v3.0.0 (Breaking Change)

```bash
# Major 버전 업그레이드
- __getattr__ 제거
- 기존 import 경로 제거
- CHANGELOG에 마이그레이션 가이드 상세 기재
```

---

## 3.6 예상 효과

| 항목 | 현재 | 개선 후 | 효과 |
|------|------|---------|------|
| __공개 API 항목__ | 154개 | 15개 | 🟢 89% 감소 |
| __IDE 자동완성__ | 긴 목록 | 간결함 | 🟢 사용성 개선 |
| __코드 maintenance__ | 154개 유지 | 15개 + types.py 유지 | 🟢 부담 80% 감소 |
| __문서화__ | 혼란 | 명확 | 🟢 초보자 이해도 향상 |
| __마이그레이션 가능성__ | 낮음 | 높음 | 🟢 미래 확장성 보장 |

---

__다음: [주요 이슈 및 개선사항](#주요-이슈-및-개선사항)__
