# 테스트 코드 작성 가이드라인

**작성일**: 2025-12-17
**목적**: vm-stock-kis 프로젝트의 테스트 코드 작성 표준화
**적용 범위**: 모든 단위 테스트, 통합 테스트

---

## 1. 기본 규칙

### 1.1 테스트 파일 구조

```text
tests/
├── unit/
│   ├── api/
│   │   ├── account/
│   │   │   └── test_order.py
│   │   ├── stock/
│   │   │   └── test_info.py
│   │   └── websocket/
│   ├── client/
│   │   └── test_*.py
│   ├── event/
│   │   └── test_*.py
│   ├── responses/
│   │   └── test_*.py
│   ├── scope/
│   │   └── test_*.py
│   └── utils/
│       └── test_*.py
├── integration/
│   ├── api/
│   │   └── test_flow_*.py
│   └── websocket/
│       └── test_*.py
└── conftest.py (공통 fixture)
```

### 1.2 테스트 명명 규칙

```python
# ✅ 좋은 예

def test_quotable_market_returns_krx_for_domestic_stock():
    """테스트: 국내 주식은 KRX 마켓을 반환"""
    ...

def test_info_continues_on_rt_cd_7_error():
    """테스트: rt_cd=7 에러 시 다음 마켓 코드로 재시도"""
    ...

def test_raises_not_found_when_all_markets_exhausted():
    """테스트: 모든 마켓 코드 소진 시 KisNotFoundError 발생"""
    ...

# ❌ 나쁜 예

def test_func():
    """함수 테스트"""
    ...

def test_1():
    """무언가 테스트"""
    ...
```

### 1.3 테스트 클래스 명명

```python
# ✅ 좋은 예

class TestQuotableMarket:
    """quotable_market() 함수 테스트"""

    def test_validates_empty_symbol(self):
        """테스트: 빈 심볼은 ValueError 발생"""
        ...

class TestInfo:
    """info() 함수 테스트"""

    def test_continues_on_rt_cd_7_error(self):
        """테스트: rt_cd=7은 재시도"""
        ...

# ❌ 나쁜 예

class Test:
    """테스트"""
    ...

class TestFunctions:
    """함수들 테스트"""
    ...
```

---

## 2. Mock 작성 패턴

### 2.1 Response Mock 기본 구조

```python
from unittest.mock import Mock
from requests import Response

# ✅ 완전한 Response Mock

mock_http_response = Mock(spec=Response)
mock_http_response.status_code = 200
mock_http_response.text = ""
mock_http_response.headers = {"tr_id": "TEST_TR_ID", "gt_uid": "TEST_GT_UID"}
mock_http_response.request = Mock()
mock_http_response.request.method = "GET"
mock_http_response.request.headers = {}
mock_http_response.request.url = "http://test.com/api"
mock_http_response.request.body = None

# ❌ 불완전한 Mock (테스트 실패 원인)

mock_http_response = Mock()
# status_code, headers, request 누락 → KisAPIError 초기화 실패
```

### 2.2 KisObject 응답 Mock

```python
# ✅ API 응답 데이터 Mock (transform_() 사용)

mock_response = Mock()
mock_response.__data__ = {
    "output": {
        "basDt": "20250101",
        "clpr": 65000,
        "exdy_type": "1"
    },
    "__response__": Mock()  # 순환 참조
}

# 자동 변환
result = KisDomesticDailyChartBar.transform_(mock_response.__data__)
```

### 2.3 KisAPIError Mock

```python
# ✅ KisAPIError 생성 패턴

from vmkis.client.exceptions import KisAPIError

api_error = KisAPIError(
    data={
        "rt_cd": "7",
        "msg1": "조회된 데이터가 없습니다",
        "__response__": mock_http_response
    },
    response=mock_http_response
)
api_error.rt_cd = 7  # rt_cd 속성 명시
api_error.data = {"rt_cd": "7", ...}  # data 속성도 설정
```

---

## 3. 테스트 작성 패턴

### 3.1 단위 테스트 구조 (AAA 패턴)

```python
def test_feature_behavior():
    """테스트: 기능의 행동을 검증"""
    # Arrange: 테스트 환경 준비
    fake_kis = Mock()
    fake_kis.cache.get.return_value = None

    mock_response = Mock()
    mock_response.output.stck_prpr = "65000"
    fake_kis.fetch.return_value = mock_response

    # Act: 기능 실행
    result = quotable_market(fake_kis, "005930", market="KR", use_cache=False)

    # Assert: 결과 검증
    assert result == "KRX"
    fake_kis.fetch.assert_called_once()
```

### 3.2 에러 처리 테스트

```python
def test_raises_exception_on_invalid_input():
    """테스트: 잘못된 입력에 예외 발생"""
    fake_kis = Mock()

    # Act & Assert
    with pytest.raises(ValueError, match="종목 코드를 입력해주세요"):
        quotable_market(fake_kis, "")
```

### 3.3 마켓 코드 반복 테스트

```python
def test_continues_on_rt_cd_7_error():
    """테스트: rt_cd=7 에러 시 다음 마켓 코드로 재시도"""
    fake_kis = Mock()
    fake_kis.cache.get.return_value = None

    # Arrange: rt_cd=7 에러 후 성공
    api_error = KisAPIError(
        data={"rt_cd": "7", "msg1": "조회된 데이터가 없습니다", "__response__": mock_http_response},
        response=mock_http_response
    )
    api_error.rt_cd = 7

    mock_info = Mock()
    fake_kis.fetch.side_effect = [api_error, mock_info]

    # Act: US 마켓 사용 (3개 코드로 재시도 가능)
    with patch('vmkis.api.stock.info.quotable_market', return_value="US"):
        result = info(fake_kis, "AAPL", market="US", use_cache=False, quotable=True)

    # Assert: 2개 마켓 코드 시도 확인
    assert result == mock_info
    assert fake_kis.fetch.call_count == 2
```

---

## 4. 마켓 코드 선택 가이드

### 4.1 MARKET_TYPE_MAP 이해

```python
MARKET_TYPE_MAP = {
    "KR": ["300"],                    # ✅ 국내 (1개)
    "KRX": ["300"],                   # ✅ 국내 (1개)
    "NASDAQ": ["512"],                # ✅ 나스닥 (1개)
    "NYSE": ["513"],                  # ✅ 뉴욕 (1개)
    "AMEX": ["529"],                  # ✅ 아멕스 (1개)
    "US": ["512", "513", "529"],      # ⭐ 미국 (3개 - 재시도 가능)
    "TYO": ["515"],                   # ✅ 도쿄 (1개)
    "JP": ["515"],                    # ✅ 일본 (1개)
    "HKEX": ["501"],                  # ✅ 홍콩 (1개)
    "HK": ["501", "543", "558"],      # ⭐ 홍콩 (3개 - 재시도 가능)
    "HNX": ["507"],                   # ✅ 하노이 (1개)
    "HSX": ["508"],                   # ✅ 호치민 (1개)
    "VN": ["507", "508"],             # ⭐ 베트남 (2개 - 재시도 가능)
    "SSE": ["551"],                   # ✅ 상하이 (1개)
    "SZSE": ["552"],                  # ✅ 선전 (1개)
    "CN": ["551", "552"],             # ⭐ 중국 (2개 - 재시도 가능)
    None: [모든 코드],                 # ⭐ 전체 (재시도 많음)
}
```

### 4.2 마켓 선택 기준

```python
# ✅ 재시도 로직 테스트 시: US, HK, VN, CN, None 사용

def test_continues_on_rt_cd_7_error():
    """재시도 테스트는 다중 코드 마켓 필수"""
    with patch('vmkis.api.stock.info.quotable_market', return_value="US"):  # ✅ 3개 코드
        ...

    # ❌ 불가능한 조합
    with patch('vmkis.api.stock.info.quotable_market', return_value="KR"):  # ❌ 1개 코드만
        ...

# ✅ 마켓 소진 테스트 시: KR, KRX, NASDAQ 등 단일 코드 마켓 사용

def test_raises_not_found_when_all_markets_exhausted():
    """모든 마켓 소진 시 테스트는 단일 코드 마켓 적합"""
    with patch('vmkis.api.stock.info.quotable_market', return_value="KR"):  # ✅ 1개 코드
        ...
```

---

## 5. 스킵된 테스트 처리

### 5.1 스킵 제거 체크리스트

테스트를 스킵 해제할 때 다음을 확인하세요:

- [ ] 스킵 사유가 여전히 유효한가?
- [ ] `KisObject.transform_()` 패턴으로 해결 가능한가?
- [ ] Mock 구조가 완전한가? (Response, request, headers 포함)
- [ ] 적절한 마켓 코드 선택이 되었는가?
- [ ] 에러 처리 경로를 모두 커버했는가?
- [ ] 테스트가 실제로 pass하는가?

### 5.2 스킵 vs 제거

```python
# ❌ 스킵 유지 (불필요한 경우)
@pytest.mark.skip(reason="구현 불가")
def test_something():
    ...

# ✅ 스킵 제거 + 구현
def test_something():
    """구현된 테스트"""
    fake_kis = Mock()
    result = quotable_market(fake_kis, "005930", market="KR", use_cache=False)
    assert result == "KRX"
```

---

## 6. 커버리지 목표

### 6.1 모듈별 목표

| 모듈 | 현재 | 목표 | 상태 |
|------|------|------|------|
| `api.stock` | 98% | 99%+ | 🟢 우수 |
| `api.account` | 94% | 95%+ | 🟢 우수 |
| `client.websocket` | 94% | 95%+ | 🟢 우수 |
| `event.handler` | 89% | 92%+ | 🟡 개선 중 |
| `adapter.websocket` | 85% | 90%+ | 🟡 개선 중 |
| `responses.dynamic` | 98% | 99%+ | 🟢 우수 |

### 6.2 커버리지 측정

```bash
# 전체 커버리지 측정
uv run pytest --cov --cov-report=html --cov-report=term-missing

# 특정 모듈 커버리지 측정
uv run pytest tests/unit/api/stock/ --cov=vmkis.api.stock --cov-report=term-missing
```

---

## 7. 주의사항

### 7.1 흔한 실수

```python
# ❌ Response Mock 불완전
mock_response = Mock()
# status_code, headers, request 누락

# ✅ Response Mock 완전
mock_response = Mock(spec=Response)
mock_response.status_code = 200
mock_response.text = ""
mock_response.headers = {"tr_id": "X", "gt_uid": "Y"}
mock_response.request = Mock()
mock_response.request.method = "GET"
mock_response.request.headers = {}
mock_response.request.url = "http://test.com"
mock_response.request.body = None
```

```python
# ❌ 마켓 코드 잘못 선택
with patch('vmkis.api.stock.info.quotable_market', return_value="KR"):
    # 1개 코드만 있어서 재시도 테스트 불가능
    ...

# ✅ 올바른 마켓 코드
with patch('vmkis.api.stock.info.quotable_market', return_value="US"):
    # 3개 코드로 재시도 가능
    ...
```

```python
# ❌ rt_cd 속성 누락
api_error = KisAPIError(data={...}, response=mock_response)
# api_error.rt_cd 설정 안 됨

# ✅ rt_cd 속성 설정
api_error = KisAPIError(data={...}, response=mock_response)
api_error.rt_cd = 7
```

### 7.2 테스트 격리

```python
# ✅ 각 테스트는 독립적이어야 함

def test_something_1():
    fake_kis = Mock()  # 각 테스트마다 새로운 Mock
    ...

def test_something_2():
    fake_kis = Mock()  # 이전 테스트와 격리됨
    ...
```

---

## 8. 검토 체크리스트

코드 리뷰 시 확인하세요:

- [ ] 테스트 명칭이 명확한가?
- [ ] 주석/Docstring이 목적을 설명하는가?
- [ ] Mock이 완전한가? (spec, 모든 속성)
- [ ] AAA 패턴을 따르는가?
- [ ] 예외 처리가 정확한가?
- [ ] 마켓 코드 선택이 적절한가?
- [ ] 테스트가 실제로 pass하는가?
- [ ] 커버리지가 증가했는가?

---

**다음 문서**: GUIDELINES_003_DOCUMENTATION.md (문서화 가이드라인)
