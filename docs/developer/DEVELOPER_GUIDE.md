# VM-Stock-KIS - 개발자 문서

## 목차

1. [개발 환경 설정](#개발-환경-설정)
2. [개발 환경 구성](#개발-환경-구성)
3. [핵심 모듈 상세 가이드](#핵심-모듈-상세-가이드)
4. [새로운 API 추가 방법](#새로운-api-추가-방법)
5. [테스트 작성 가이드](#테스트-작성-가이드)
6. [코드 스타일 가이드](#코드-스타일-가이드)
7. [디버깅 및 로깅](#디버깅-및-로깅)
8. [성능 최적화](#성능-최적화)

---

## 개발 환경 설정

### 필수 요구사항

- Python 3.10 이상
- uv (의존성 관리)
- Git

### 초기 설정

```bash
# 저장소 클론
git clone https://github.com/visualmoney/vm-stock-kis.git
cd vm-stock-kis

# 가상 환경 생성 및 활성화
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# 의존성 설치
uv sync --group dev

# 개발 모드로 설치
pip install -e .
```

### IDE 설정

#### VS Code

```json
{
  "python.linting.pylintEnabled": true,
  "python.linting.enabled": true,
  "python.formatting.provider": "autopep8",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

---

## 개발 환경 구성

### 프로젝트 구조 이해

```text
src/vmkis/
├── kis.py              # VmKis 메인 클래스 (800+ 줄)
├── types.py            # 공개 타입 정의
├── logging.py          # 로깅 시스템
│
├── api/                # REST/WebSocket API 구현
│   ├── auth/           # 토큰 관리
│   ├── stock/          # 주식 관련 API
│   └── websocket/      # 실시간 데이터
│
├── scope/              # API 진입점
│   ├── account.py      # 계좌 Scope (KisAccount)
│   ├── stock.py        # 주식 Scope (KisStock)
│   └── base.py         # Scope 베이스
│
├── adapter/            # 기능 추가 (Mixin)
│   ├── product/        # 상품 기능
│   ├── account_product/# 계좌-상품 기능
│   └── websocket/      # 실시간 기능
│
├── client/             # 통신 계층
│   ├── websocket.py    # WebSocket 클라이언트 (450+ 줄)
│   ├── auth.py         # 인증 정보
│   ├── account.py      # 계좌번호
│   ├── appkey.py       # 앱키
│   ├── exceptions.py   # 예외 처리
│   └── object.py       # 객체 베이스
│
├── responses/          # 응답 변환
│   ├── dynamic.py      # 동적 타입 시스템 (500+ 줄)
│   ├── types.py        # 타입 구현체
│   ├── response.py     # 응답 베이스
│   └── exceptions.py   # 응답 예외
│
├── event/              # 이벤트 시스템
│   ├── handler.py      # 이벤트 핸들러 (300+ 줄)
│   ├── subscription.py # 구독 관리
│   └── filters/        # 필터링
│
└── utils/              # 유틸리티
    ├── rate_limit.py   # Rate Limiting
    ├── thread_safe.py  # Thread 안전성
    ├── repr.py         # 커스텀 repr
    ├── workspace.py    # 경로 관리
    └── ...
```

### 주요 코드 라인 수

| 모듈 | 라인 수 | 설명 |
|------|--------|------|
| kis.py | 800+ | 메인 클래스, API 호출 관리 |
| dynamic.py | 500+ | 동적 타입 시스템 핵심 |
| websocket.py | 450+ | WebSocket 통신 |
| handler.py | 300+ | 이벤트 시스템 |
| repr.py | 250+ | 객체 표현 |

---

## 핵심 모듈 상세 가이드

### 1. VmKis 클래스 (kis.py)

#### 초기화 패턴

```python
# 패턴 1: 파일 기반
kis = VmKis("secret.json")

# 패턴 2: KisAuth 객체
from vmkis import KisAuth
auth = KisAuth(id="...", appkey="...", secretkey="...", account="...")
kis = VmKis(auth)

# 패턴 3: 직접 입력
kis = VmKis(
    id="soju06",
    account="00000000-01",
    appkey="...",
    secretkey="..."
)

# 패턴 4: 모의투자
kis = VmKis(
    "real_secret.json",
    "paper_secret.json",
    keep_token=True
)
```

#### 핵심 메서드

```python
# Scope 진입점
account = kis.account()      # KisAccount
stock = kis.stock("000660")  # KisStock

# 저수준 API
response = kis.request(
    path="/uapi/domestic-stock/v1/quotations/inquire-price",
    method="GET",
    params={"fid_cond_mrkt_div_code": "J"}
)

# API 래퍼
result = kis.api(
    "usdh1",
    params={...},
    response_type=KisQuote
)

# WebSocket
websocket = kis.websocket
```

#### Rate Limiting 메커니즘

```python
# 내부 동작
@property
def rate_limiter(self) -> RateLimiter:
    return self._rate_limiters.get(domain)

# 요청 전
rate_limiter.wait()  # 제한에 따라 대기

# 요청 후
if success:
    rate_limiter.on_success()
else:
    rate_limiter.on_error()
```

### 2. 동적 타입 시스템 (responses/dynamic.py)

#### KisType 기반 클래스

```python
from vmkis.responses.dynamic import KisType, KisTypeMeta

class KisInt(KisType[int], metaclass=KisTypeMeta[int]):
    """정수 타입"""
    @classmethod
    def transform_(cls, value):
        return int(value) if value is not None else None

class KisDecimal(KisType[Decimal], metaclass=KisTypeMeta[Decimal]):
    """소수점 숫자"""
    @classmethod
    def transform_(cls, value):
        if value is None:
            return None
        return Decimal(value).quantize(Decimal('0.01'))
```

#### KisObject 사용법

```python
from vmkis.responses.dynamic import KisObject, KisTransform
from vmkis.responses.response import KisResponse

@dataclass
class MyResponse(KisResponse):
    symbol: str = KisString()
    price: Decimal = KisDecimal()
    volume: int = KisInt()

# 변환
data = {"symbol": "000660", "price": "70000", "volume": "1000"}
result = KisObject.transform_(data, MyResponse)
# result.symbol == "000660"
# result.price == Decimal("70000.00")
# result.volume == 1000
```

#### 커스텀 타입 정의

```python
class KisCustomType(KisType[CustomClass]):
    @classmethod
    def transform_(cls, value):
        if isinstance(value, CustomClass):
            return value
        return CustomClass(value)
```

### 3. WebSocket 클라이언트 (client/websocket.py)

#### 아키텍처

```python
class KisWebsocketClient:
    # 상태
    _connected: bool
    _subscriptions: set[KisWebsocketTR]
    _message_handlers: dict[str, Callable]

    # 메서드
    async def connect()      # WebSocket 연결
    async def disconnect()   # WebSocket 해제
    async def subscribe()    # 구독 요청
    async def unsubscribe()  # 구독 해제
```

#### 재연결 메커니즘

```text
연결 시도
    ↓
연결 성공 ──N──→ 대기 후 재시도
    ↓Y
구독 복구 (저장된 구독 다시 요청)
    ↓
메시지 수신 루프
    ↓
연결 끊김 감지
    ↓
자동 재연결 시도
```

#### 사용 예

```python
# 자동으로 관리 (Scope를 통해)
ticket = stock.on("price", callback)

# 또는 직접 사용
from vmkis.client.messaging import KisWebsocketTR

websocket = kis.websocket
tr = KisWebsocketTR("H0STCNT0", "000660")
websocket.subscribe(tr, callback)
```

### 4. Event 시스템 (event/handler.py)

#### 이벤트 핸들러

```python
from vmkis.event.handler import KisEventHandler

# 핸들러 생성
handler = KisEventHandler()

# 이벤트 등록
def on_event(sender, e):
    print(f"Event: {e}")

ticket = handler.subscribe(on_event)

# 이벤트 발생
handler.invoke(sender, event_args)

# 구독 해제
ticket.unsubscribe()
```

#### 이벤트 필터

```python
from vmkis.event.filters.product import KisProductEventFilter

# 특정 상품만 필터링
filter = KisProductEventFilter("000660")
handler.subscribe(callback, filter=filter)
```

### 5. Scope 패턴 (scope/account.py, scope/stock.py)

#### 계좌 Scope

```python
@dataclass
class KisAccount(
    KisAccountScope,
    KisAccountQuotableProductMixin,
    KisRealtimeAccountProductable,
    ...
):
    """계좌 객체"""

    account_number: KisAccountNumber

    # Mixin에서 상속한 메서드
    def balance(self):       # 잔고 조회
    def pending_orders(self):# 미체결 주문
    def on(event, callback): # 실시간 이벤트
```

#### 주식 Scope

```python
@dataclass
class KisStock(
    KisStockScope,
    KisQuotableProductMixin,
    KisWebsocketQuotableProductMixin,
    ...
):
    """주식 객체"""

    symbol: str
    market: MARKET_TYPE

    # Mixin에서 상속한 메서드
    def quote(self):         # 시세 조회
    def chart(self):         # 차트 조회
    def on(event, callback):  # 실시간. stock.on("price", ...)
```

---

## 새로운 API 추가 방법

### 단계별 가이드

#### Step 1: API Response 타입 정의

```python
# src/vmkis/responses/my_response.py
from dataclasses import dataclass
from vmkis.responses.response import KisResponse
from vmkis.responses.types import KisString, KisInt, KisDecimal

@dataclass
class KisMyData(KisResponse):
    """내 API 응답"""

    symbol: str = KisString()
    price: Decimal = KisDecimal()
    volume: int = KisInt()
```

#### Step 2: API 함수 구현

```python
# src/vmkis/api/my_api.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vmkis.kis import VmKis

def get_my_data(
    kis: "VmKis",
    symbol: str,
    domain: Literal["live", "paper"] = "live"
) -> KisMyData:
    """내 데이터 조회

    Args:
        kis: VmKis 인스턴스
        symbol: 종목코드
        domain: 도메인 ("live" 또는 "paper")

    Returns:
        KisMyData: 조회 결과

    Raises:
        KisAPIError: API 에러
    """
    return kis.api(
        "my_api_tr_id",
        method="GET",
        params={
            "fid_input_iscd": symbol,
        },
        response_type=KisMyData,
        domain=domain,
    )
```

#### Step 3: Adapter Mixin 작성

```python
# src/vmkis/adapter/my_adapter.py
from typing import Protocol

class KisMyApiCapable(Protocol):
    """내 API를 사용할 수 있는 객체"""
    @property
    def kis(self) -> "VmKis":
        ...

class KisMyApiMixin(KisMyApiCapable):
    """내 API 기능 추가"""

    def get_my_data(self) -> KisMyData:
        """내 데이터 조회"""
        from vmkis.api.my_api import get_my_data
        return get_my_data(self.kis, self.symbol)
```

#### Step 4: Scope에 Mixin 추가

```python
# src/vmkis/scope/stock.py
from vmkis.adapter.my_adapter import KisMyApiMixin

@dataclass
class KisStock(
    KisStockScope,
    KisMyApiMixin,  # 추가
    ...
):
    pass
```

#### Step 5: 공개 API 노출

```python
# src/vmkis/__init__.py
from vmkis.responses.my_response import KisMyData

__all__ = [
    ...,
    "KisMyData",
]
```

### 최소 예제: 시세 조회 추가

```python
# 1. Response 타입
@dataclass
class KisSimpleQuote(KisResponse):
    symbol: str = KisString()
    price: Decimal = KisDecimal()

# 2. API 함수
def get_simple_quote(kis: "VmKis", symbol: str) -> KisSimpleQuote:
    return kis.api(
        "simple_quote_tr",
        params={"symbol": symbol},
        response_type=KisSimpleQuote
    )

# 3. Mixin
class KisSimpleQuotableMixin:
    def simple_quote(self) -> KisSimpleQuote:
        return get_simple_quote(self.kis, self.symbol)

# 4. Scope에 추가
class KisStock(KisStockScope, KisSimpleQuotableMixin, ...):
    pass

# 5. 사용
stock = kis.stock("000660")
quote = stock.simple_quote()
```

---

## 테스트 작성 가이드

### 테스트 구조

```text
tests/
├── __init__.py
├── conftest.py           # pytest 설정
├── test_kis.py           # VmKis 테스트
├── test_scope.py         # Scope 테스트
├── test_api/             # API 테스트
│   ├── test_stock_quote.py
│   ├── test_account_balance.py
│   └── ...
├── test_responses/       # Response 변환 테스트
│   ├── test_dynamic.py
│   └── test_types.py
└── fixtures/             # 테스트 데이터
    ├── responses.json
    └── auth.json
```

### 단위 테스트 작성

```python
# tests/test_kis.py
import pytest
from vmkis import VmKis, KisAuth
from vmkis.client.exceptions import KisAPIError

@pytest.fixture
def kis():
    """테스트 VmKis 인스턴스"""
    auth = KisAuth(
        id="test_user",
        account="00000000-01",
        appkey="test_app_key" * 3,  # 36자
        secretkey="test_secret_key" * 6,  # 180자
    )
    return VmKis(auth)

def test_kis_initialization(kis):
    """VmKis 초기화 테스트"""
    assert kis is not None
    assert kis.primary_account == "00000000-01"

def test_kis_stock_creation(kis):
    """주식 객체 생성 테스트"""
    stock = kis.stock("000660")
    assert stock.symbol == "000660"
    assert stock.kis == kis

def test_kis_account_creation(kis):
    """계좌 객체 생성 테스트"""
    account = kis.account()
    assert account.account_number == kis.primary_account
    assert account.kis == kis
```

### Mock을 이용한 테스트

```python
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

@pytest.fixture
def mock_kis(kis):
    """Mock된 VmKis"""
    kis.request = Mock()
    return kis

def test_quote_with_mock(mock_kis):
    """시세 조회 Mock 테스트"""
    # `vmkis.Quote` 는 Protocol 이라 인스턴스를 만들 수 없습니다.
    # 반환값 대역은 필요한 속성만 가진 값 객체로 세웁니다.
    mock_kis.request.return_value = SimpleNamespace(
        symbol="000660",
        price=Decimal("70000"),
    )

    stock = mock_kis.stock("000660")
    # quote = stock.quote()  # 실제 구현 테스트
    # assert quote.price == Decimal("70000")

    # `Mock()` 을 그대로 반환값으로 쓰면 어떤 속성 접근이든 조용히 Mock 을
    # 돌려주므로, 검증하는 줄이 사실상 아무것도 검사하지 않게 됩니다.
```

### 통합 테스트

```python
# tests/test_integration.py
import pytest
from vmkis import VmKis

@pytest.mark.integration
def test_real_api_call(kis):
    """실제 API 호출 테스트 (개발 환경에서만)"""
    # 주의: 실제 계정으로 테스트 가능
    stock = kis.stock("000660")

    # quote = stock.quote()
    # assert quote is not None
    # assert quote.symbol == "000660"
```

### 테스트 실행

```bash
# 모든 테스트
pytest

# 특정 파일만
pytest tests/test_kis.py

# Coverage 포함
pytest --cov=vmkis --cov-report=html

# 특정 마커
pytest -m unit
pytest -m integration

# 상세 출력
pytest -vv
```

---

## 코드 스타일 가이드

### 명명 규칙

```python
# 클래스: PascalCase로 Kis 접두사
class KisAccount:
    pass

# 함수/메서드: snake_case
def get_balance():
    pass

# 상수: UPPER_SNAKE_CASE
API_REQUEST_LIMIT = 20

# 비공개 속성: 언더스코어 접두사
_private_attribute = None

# 프로토콜: 접미사 Protocol
class KisObjectProtocol(Protocol):
    pass
```

### 타입 힌팅

```python
from typing import Optional, Literal, Union

# 필수
def quote(self) -> KisQuote:
    pass

# 선택사항
def balance(self, account: Optional[str] = None) -> KisBalance:
    pass

# 리터럴
def api(self, domain: Literal["live", "paper"] = "live"):
    pass

# Union (가능하면 | 사용)
def request(self) -> dict | KisResponse:
    pass
```

### Docstring

```python
def quote(self, extended: bool = False) -> KisQuote:
    """주식 시세를 조회합니다.

    Args:
        extended (bool, optional): 주간거래 포함 여부. 기본값 False.

    Returns:
        KisQuote: 주식 시세 정보

    Raises:
        KisAPIError: API 호출 실패 시
        KisMarketNotOpenedError: 시장 미개장 시

    Examples:
        >>> stock = kis.stock("000660")
        >>> quote = stock.quote()
        >>> print(quote.price)
        70000

    Note:
        실시간 시세는 stock.on("price", ...) 를 사용하세요.
    """
    pass
```

### 일반 코드 스타일

```python
# 라인 길이: 88자 (Black 기본값)
# 들여쓰기: 4 스페이스
# 문자열: 큰따옴표 선호
# 임포트: isort로 정렬

# 임포트 순서
import sys                      # 표준 라이브러리
from pathlib import Path

from requests import Response   # 서드파티
from typing_extensions import Protocol

from vmkis.kis import VmKis     # 로컬 모듈
```

---

## 디버깅 및 로깅

### 로깅 설정

```python
from vmkis import logging

# 로그 레벨 설정
logging.setLevel("DEBUG")  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# 로그 확인
logger = logging.logger
logger.debug("디버그 메시지")
logger.info("정보 메시지")
logger.warning("경고 메시지")
logger.error("에러 메시지")
```

### 환경 변수

`.env` 를 읽는 python-dotenv 는 **런타임 의존성이 아닙니다**(#72). 저장소에서
개발 중이라면 `[dependency-groups] test` 에 있으므로 `uv sync --group dev` 로
이미 들어와 있고, 그 밖의 환경에서는 `pip install python-dotenv` 가 필요합니다.

```python
# .env 파일
DEBUG=true
KIS_ID=your_id
KIS_APPKEY=your_appkey
KIS_SECRETKEY=your_secretkey

# 코드에서 사용
from dotenv import load_dotenv
import os

load_dotenv()
kis_id = os.getenv("KIS_ID")
```

### API 요청 디버깅

```python
# 상세 에러 정보 활성화
from vmkis.__env__ import TRACE_DETAIL_ERROR

# kis.py의 verbose 파라미터 활용
response = kis.api(..., verbose=True)
```

### WebSocket 디버깅

```python
# WebSocket 메시지 추적
import logging
logging.getLogger("websocket").setLevel(logging.DEBUG)

# 또는
logging.setLevel("DEBUG")
```

---

## 성능 최적화

### 1. HTTP 연결 풀링

```python
# VmKis는 자동으로 requests.Session을 재사용
# 여러 요청: 같은 KisAccessToken 재사용
kis = VmKis(...)
for symbol in symbols:
    stock = kis.stock(symbol)
    quote = stock.quote()  # 같은 세션 재사용
```

### 2. Rate Limiting

```python
# 자동으로 관리됨
# 하지만 대량 요청 시 최적화 가능

from vmkis.utils.rate_limit import RateLimiter

# 순차 요청 (자동 rate limit)
for symbol in symbols:
    quote = kis.stock(symbol).quote()  # 자동으로 대기

# 병렬 처리 (권장하지 않음 - rate limit 위반)
# asyncio나 threading 사용 시 rate limit 고려
```

### 3. 메모리 최적화

```python
# 이벤트 구독은 GC에 의해 자동 정리
ticket = stock.on("price", callback)
del ticket  # 자동으로 구독 해제

# 또는 명시적 해제
ticket.unsubscribe()
```

### 4. 배치 처리

```python
# 여러 종목 조회
symbols = ["000660", "005930", "035420"]

# 최적: 순차 처리 (rate limit 자동)
for symbol in symbols:
    quote = kis.stock(symbol).quote()

# WebSocket: 최대 40개 동시 구독
tickets = []
for symbol in symbols[:40]:
    ticket = kis.stock(symbol).on("price", callback)
    tickets.append(ticket)
```

---

## 개발 팁

### 1. 새로운 기능 테스트

```bash
# 모드 가상 테스트 환경
kis = VmKis("secret.json", "paper_secret.json")

# 모의투자로 테스트 후 실전 전환
```

### 2. 디버깅 팁

```python
# 응답 원본 확인
response = kis.api(...)
print(response.__response__)  # 원본 HTTP 응답

# 동적 속성 확인
response._kis_property  # 동적 속성 확인
```

### 3. 타입 체킹

```bash
# mypy를 이용한 타입 체크
pip install mypy
mypy vmkis --strict

# 또는 Pylance (VS Code)
```

---

이 문서는 VM-Stock-KIS 개발자를 위한 완벽한 가이드입니다.
더 많은 정보는 소스코드의 docstring을 참조하세요.
