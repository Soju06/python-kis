> **동결 — 2025-12-17 에 쓴 테스트 규칙입니다.** 원래 자리는
> `docs/rules/TEST_RULES_AND_GUIDELINES.md` 였고, `docs/INDEX.md` 는 이것을
> **"옛 테스트 규칙"** 이라고 적으면서도 살아 있는 자리에 두고 있었습니다.
>
> **`docs/` 안에 "옛 것"이 있으면 스윕 대상인지 매번 판단해야 하고, 그 판단은
> 언젠가 틀립니다.** 실제로 `#70`(`real`/`virtual` → `live`/`paper`)이 대상
> 목록을 손으로 적으면서 이 디렉터리를 빠뜨렸습니다.
>
> 그 결과가 이 문서 안에 그대로 남아 있습니다 — `#78` 의 검사기가 **코드펜스만**
> 고쳐서, 3행의 `paper=True` 와 19행의 *"`virtual=True`: 실제 서버 접근 없이"*
> 가 **같은 절 안에서 서로 어긋납니다.** 181행은 아직 포크 이전 패키지명
> (`from pykis import PyKis`)을 씁니다.
>
> 지금 무엇을 볼 것인가 —
> [`docs/guidelines/GUIDELINES_001_TEST_WRITING.md`](../../docs/guidelines/GUIDELINES_001_TEST_WRITING.md)
> 가 정본입니다. 다만 **이 문서에만 있던 성능 테스트 작성 규칙(벤치마크·메모리
> 프로파일링)은 정본에 없습니다.** 그 자리를 채울지는 별도로 정합니다.
>
> 보관 기준은 [`archive/README.md`](../README.md) 를 보세요.
> 근거: [`#106`](https://github.com/visualmoney/vm-stock-kis/issues/106)

# PyKIS 테스트 개발 규칙 및 가이드

## 1. KisAuth 사용 규칙

### 필수 필드

```python
KisAuth(
    id="test_user",                        # 필수: 사용자 ID
    account="50000000-01",                 # 필수: 계좌번호
    appkey="P" + "A" * 35,                 # 필수: 앱 키 (최소 36자)
    secretkey="S" * 180,                   # 필수: 시크릿 키 (180자)
    paper=True,                            # 필수: 모의투자 여부
)
```

### 포인트

- `virtual=True`: 실제 서버 접근 없이 테스트 모드로 실행
- `appkey`와 `secretkey`는 더미 값이어도 되지만 길이 맞춰야 함
- 모든 필드가 필수 - 하나라도 누락되면 TypeError 발생

## 2. KisObject.transform_() 사용 규칙

### 기본 API

```python
result = KisClass.transform_(
    data,                              # dict 타입의 데이터
    response_type=ResponseType.OBJECT  # 응답 타입 지정
)
```

### Custom Mock 클래스 작성 방법

#### Step 1: 클래스 정의

```python
class MockPrice(KisObject):
    __annotations__ = {  # __fields__ 아님! __annotations__ 사용
        'symbol': str,
        'price': int,
        'volume': int,
    }
```

#### Step 2: __transform__ staticmethod 구현

```python
    @staticmethod
    def __transform__(cls, data):
        """
        동적으로 호출되는 변환 메서드
        - dynamic.py 라인 249에서 transform_fn(transform_type, data) 형태로 호출
        - transform_fn은 getattr(transform_type, "__transform__", None)로 가져온 것
        - 따라서 @staticmethod로 작성해야 cls를 명시적으로 받을 수 있음
        """
        obj = cls(cls)  # KisObject.__init__(self, type) 요구
        for key, value in data.items():
            setattr(obj, key, value)
        return obj
```

#### Step 3: 중첩 객체 처리 (필요시)

```python
class MockQuote(KisObject):
    __annotations__ = {
        'symbol': str,
        'prices': list[MockPrice],
    }

    @staticmethod
    def __transform__(cls, data):
        obj = cls(cls)
        for key, value in data.items():
            if key == 'prices' and isinstance(value, list):
                # 중첩된 객체 재귀 변환
                setattr(obj, key, [
                    MockPrice.__transform__(MockPrice, p) if isinstance(p, dict) else p
                    for p in value
                ])
            else:
                setattr(obj, key, value)
        return obj
```

### 주의사항

- __`__fields__`가 아니라 `__annotations__` 사용__: KisObject는 `__annotations__`으로 필드 정의
- __@staticmethod 사용__: 클래스메서드가 아님!
- __cls를 첫 번째 인자로__: dynamic.py에서 `transform_fn(transform_type, data)` 호출되기 때문
- __KisObject.__init__ 호출__: `obj = cls(cls)` 형태로 type 파라미터 전달

## 3. 성능 테스트 작성 규칙

### 벤치마크 패턴

```python
def test_benchmark_operation(self):
    """벤치마크 설명"""
    data = {...}  # 테스트 데이터

    count = 100  # 반복 횟수
    start = time.time()

    for _ in range(count):
        result = MockClass.transform_(data, MockClass)

    elapsed = time.time() - start
    benchmark = BenchmarkResult("테스트명", elapsed, count)

    print(f"\n{benchmark}")

    # 성능 기준 설정 (ops/s)
    assert benchmark.ops_per_second > 100
```

### 메모리 프로파일링 패턴

```python
def test_memory_operation(self):
    """메모리 사용량 테스트"""
    tracemalloc.start()

    snapshot_before = tracemalloc.take_snapshot()

    # 메모리 집약적 작업
    objects = []
    for i in range(1000):
        obj = MockClass.transform_(data, MockClass)
        objects.append(obj)

    snapshot_after = tracemalloc.take_snapshot()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    top_stats = snapshot_after.compare_to(snapshot_before, 'lineno')
    total_diff = sum(stat.size_diff for stat in top_stats) / 1024

    profile = MemoryProfile(
        name='test_name',
        peak_kb=peak / 1024,
        diff_kb=total_diff,
        count=1000
    )

    print(f"\n{profile}")
    assert profile.per_item_kb < 10.0  # 항목당 10KB 미만
```

## 4. 테스트 스킵 규칙

### skip 데코레이터 사용

```python
@pytest.mark.skip(reason="구체적인 스킵 사유")
def test_something(self):
    """테스트"""
    pass
```

### 스킵 사유 기록

- 라이브러리 구조 문제
- 향후 수정 필요한 항목
- 의존 라이브러리 부재

## 5. 테스트 코드 구조 규칙

### 필수 구성 요소

```python
"""
모듈 설명
간단한 개요
"""

import pytest
from pykis import PyKis, KisAuth

@pytest.fixture
def mock_auth():
    """테스트용 인증 정보"""
    return KisAuth(...)

class TestSomething:
    """테스트 클래스 설명"""

    def test_specific_case(self, mock_auth):
        """구체적 테스트 케이스"""
        pass
```

### 명명 규칙

- 모듈: `test_*.py`
- 클래스: `Test*` 또는 `Test*Suite`
- 메서드: `test_*_*` (동작_상황)
- Fixture: `mock_*` 또는 `fixture_*`

## 6. Mock 객체 작성 규칙

### Mock 클래스 패턴

```python
class MockData(KisObject):
    """모의 데이터 설명"""
    __annotations__ = {
        'field1': str,
        'field2': int,
        'field3': float,
    }

    @staticmethod
    def __transform__(cls, data):
        obj = cls(cls)
        for key, value in data.items():
            setattr(obj, key, value)
        return obj
```

### 포인트

- 실제 응답 클래스와 동일한 필드 구조
- __annotations__로 필드 타입 정의
- __transform__ 메서드 반드시 구현

## 7. 성능 기준 설정 규칙

### 보수적 기준 설정

- 너무 엄격하지 않을 것 (CI/CD 환경 고려)
- 부하 테스트는 상대적 비교 중심
- 메모리는 절대값이 아닌 항목당 사용량으로 판단

### 권장 기준

| 작업 | 기준 | 예시 |
|-----|------|------|
| 간단 변환 | ops/sec > 1000 | simple_transform |
| 중첩 변환 | ops/sec > 300 | nested_transform |
| 대량 배치 | 총 시간 < 1초 | batch_transform |
| 메모리 | 항목당 < 10KB | memory_single_object |

## 8. 커밋 메시지 규칙

### 테스트 성공 시

```text
fix: test_xxxx.py - xx 테스트 통과 (n/n passing)

- KisAuth.virtual 필드 추가
- KisObject.transform_() API 수정
- Mock 클래스 __transform__ 메서드 구현

Coverage: ~65%
```

### 부분 성공 시

```text
feat: test_xxxx.py - 성능 테스트 구현 (n/m passed, k skipped)

- 벤치마크 테스트 7/7 통과
- 메모리 프로파일 7/7 통과
- WebSocket 스트레스: 7개 스킵 (pykis 구조 불일치)

다음 단계: PyKis websocket API 확인 후 테스트 수정

Coverage: 61%
```
