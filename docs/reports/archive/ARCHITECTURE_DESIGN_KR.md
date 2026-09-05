# ARCHITECTURE_DESIGN_KR.md - 설계 패턴 및 아키텍처

**작성일**: 2025년 12월 20일
**대상**: 개발자, 아키텍트
**주제**: 계층화 아키텍처, 설계 패턴, 모듈 구조

---

## 2.1 계층화 아키텍처

```text
┌─────────────────────────────────────────────────────────┐
│  Application Layer (사용자 코드)                         │
│  kis = PyKis("secret.json")                           │
│  stock = kis.stock("005930")                          │
│  quote = stock.quote()                                │
├─────────────────────────────────────────────────────────┤
│  Scope Layer (API 진입점)                              │
│  ├─ KisAccount (계좌 관련)                            │
│  ├─ KisStock (주식 관련)                              │
│  └─ KisStockScope (국내/해외 주식)                     │
├─────────────────────────────────────────────────────────┤
│  Adapter Layer (기능 확장 - Mixin)                    │
│  ├─ KisQuotableAccount (시세 조회)                   │
│  ├─ KisOrderableAccount (주문 가능)                  │
│  └─ KisWebsocketQuotableProduct (실시간 시세)       │
├─────────────────────────────────────────────────────────┤
│  API Layer (REST/WebSocket)                          │
│  ├─ api.account (계좌 API)                           │
│  ├─ api.stock (주식 API)                             │
│  └─ api.websocket (실시간 WebSocket)                │
├─────────────────────────────────────────────────────────┤
│  Client Layer (통신)                                  │
│  ├─ KisAuth (인증 관리)                              │
│  ├─ KisWebsocketClient (WebSocket 통신)             │
│  └─ Rate Limiting (API 호출 제한)                   │
├─────────────────────────────────────────────────────────┤
│  Response Layer (응답 변환)                          │
│  ├─ KisDynamic (동적 타입 변환)                      │
│  ├─ KisObject (객체 자동 변환)                       │
│  └─ Type Hint 생성                                  │
├─────────────────────────────────────────────────────────┤
│  Utility Layer                                       │
│  ├─ Rate Limit (API 호출 제한)                      │
│  ├─ Thread Safety (스레드 안전성)                   │
│  └─ Exception Handling (예외 처리)                  │
└─────────────────────────────────────────────────────────┘
```

**아키텍처 평가**: 🟢 **4.5/5.0 - 우수**

- ✅ 명확한 계층 분리
- ✅ 단일 책임 원칙 준수
- ✅ 의존성 역전 원칙 (Protocol 사용)
- ⚠️ 일부 계층 간 결합도 높음

---

## 2.2 핵심 설계 패턴

### 2.2.1 Protocol 기반 설계 (Structural Subtyping)

```python
# pykis/client/object.py
class KisObjectProtocol(Protocol):
    """모든 API 객체가 준수해야 하는 프로토콜"""
    @property
    def kis(self) -> PyKis:
        """PyKis 인스턴스 참조"""
        ...
```

**장점**:

- ✅ 덕 타이핑 지원
- ✅ 타입 안전성 보장
- ✅ IDE 자동완성 완벽 지원
- ✅ 런타임 타입 체크 가능

**평가**: 🟢 **5.0/5.0 - 매우 우수**

### 2.2.2 Mixin 패턴 (수평적 기능 확장)

```python
# pykis/adapter/account/order.py
class KisOrderableAccount:
    """계좌에 주문 기능 추가"""
    def buy(self, ...): pass
    def sell(self, ...): pass
```

**장점**:

- ✅ 기능 단위로 모듈화
- ✅ 코드 재사용성 높음
- ✅ 다중 상속으로 기능 조합 가능

**평가**: 🟢 **4.0/5.0 - 양호**

### 2.2.3 동적 타입 시스템

```python
# pykis/responses/dynamic.py
class KisDynamic:
    """API 응답을 동적으로 타입이 지정된 객체로 변환"""
```

**평가**: 🟢 **4.5/5.0 - 우수**

### 2.2.4 이벤트 기반 아키텍처 (WebSocket)

```python
# pykis/event/handler.py
class KisEventHandler:
    """이벤트 핸들러 (Pub-Sub 패턴)"""
```

**평가**: 🟢 **4.5/5.0 - 우수**

---

## 2.3 모듈 구조 분석

### 2.3.1 pykis/**init**.py 분석

**현재 상태**:

```python
__all__ = [
    # 총 154개 항목 export
    "PyKis",              # ✅ 필요
    "KisAuth",            # ✅ 필요
    "KisObjectProtocol",  # ❌ 내부 구현
    # ... 150개 이상 내부 구현 노출
]
```

**문제점**:

- 🔴 150개 이상의 클래스가 패키지 루트에 노출
- 🔴 내부 구현(Protocol, Adapter)까지 공개 API로 노출
- 🔴 사용자가 어떤 것을 import해야 할지 혼란
- 🔴 IDE 자동완성 목록이 지나치게 길어짐

**평가**: 🔴 **2.0/5.0 - 개선 필요**

### 2.3.2 pykis/types.py 분석

**현재 상태**:

```python
# pykis/types.py
__all__ = [
    # __init__.py와 동일한 154개 항목 재정의
]
```

**문제점**:

- 🔴 `__init__.py`와 완전히 중복
- 🔴 유지보수 이중 부담
- 🔴 공개 API 경로가 불명확

**평가**: 🔴 **1.5/5.0 - 심각한 개선 필요**

---

## 2.4 설계 철학 및 원칙

### 핵심 원칙

```text
✓ 80/20 법칙 (20%의 메서드로 80%의 작업)
✓ 객체 지향 설계 (메서드 체이닝)
✓ 관례 우선 설정 (기본값 제공)
✓ Pythonic 코드 스타일
✓ 타입 안전성 우선순위
```

---

## 다음 단계

➡️ [코드 품질 분석 보기](ARCHITECTURE_QUALITY_KR.md)
