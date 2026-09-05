"""성능 벤치마크 테스트

`KisObject.transform_()` 의 성능을 측정합니다.

경과 시간에는 반드시 **`time.perf_counter()`** 를 씁니다. `time.time()` 은
벽시계라 Windows 에서 눈금이 약 15.6ms 이고, 측정 구간이 그보다 빨리 끝나면
경과가 정확히 `0.000s` 로 찍힙니다. 그러면 `ops_per_second` 가 뒤집혀
**기계가 빠를수록 테스트가 실패**했습니다 (이슈 #23).

`perf_counter` 는 단조 증가하며 해상도가 훨씬 높고, 시스템 시계 변경(NTP 동기화,
서머타임)의 영향도 받지 않습니다. 경과 시간 측정에 벽시계를 쓸 이유가 없습니다.
"""

import time

import pytest

from vmkis.responses.dynamic import KisObject


class MockPrice(KisObject):
    """모의 가격 응답"""

    __annotations__ = {
        "symbol": str,
        "price": int,
        "volume": int,
        "timestamp": str,
        "market": str,
    }

    @staticmethod
    def __transform__(cls, data):
        obj = cls(cls)
        for key, value in data.items():
            setattr(obj, key, value)
        return obj


class MockQuote(KisObject):
    """모의 호가 응답"""

    __annotations__ = {
        "symbol": str,
        "name": str,
        "current_price": int,
        "high": int,
        "low": int,
        "volume": int,
        "prices": list[MockPrice],
    }

    @staticmethod
    def __transform__(cls, data):
        obj = cls(cls)
        for key, value in data.items():
            if key == "prices" and isinstance(value, list):
                setattr(obj, key, [MockPrice.__transform__(MockPrice, p) if isinstance(p, dict) else p for p in value])
            else:
                setattr(obj, key, value)
        return obj


class BenchmarkResult:
    """벤치마크 결과"""

    def __init__(self, name: str, elapsed: float, count: int):
        self.name = name
        self.elapsed = elapsed
        self.count = count

    @property
    def ops_per_second(self) -> float:
        """초당 연산 수.

        경과가 0이면 `inf` 를 반환한다. 예전에는 `0.0` 이었는데, 그것은
        "측정 불가능하게 빨랐다"를 "처리량이 0이다"로 뒤집어 보고하는 것이었다.
        그 결과 `assert ops_per_second > 10` 같은 하한 검사가 **기계가 빠를수록
        실패**했다.

        `time.perf_counter()` 로 바꾼 뒤로는 경과가 정확히 0이 나오기 어렵지만,
        의미가 틀린 값을 남겨 둘 이유는 없다.
        """
        if self.elapsed > 0:
            return self.count / self.elapsed
        return float("inf")

    @property
    def avg_time_ms(self) -> float:
        """평균 시간(ms)"""
        if self.count > 0:
            return (self.elapsed / self.count) * 1000
        return 0.0

    def __repr__(self):
        return (
            f"{self.name}: {self.count} ops in {self.elapsed:.3f}s "
            f"({self.ops_per_second:.1f} ops/s, {self.avg_time_ms:.3f}ms/op)"
        )


class TestTransformBenchmark:
    """KisObject.transform_() 벤치마크"""

    def test_benchmark_simple_transform(self):
        """단순 객체 변환 벤치마크"""
        data = {
            "symbol": "005930",
            "price": 70000,
            "volume": 1000000,
            "timestamp": "20240101090000",
            "market": "KRX",
        }

        count = 1000
        start = time.perf_counter()

        for _ in range(count):
            result = MockPrice.transform_(data, MockPrice)
            assert result.symbol == "005930"

        elapsed = time.perf_counter() - start
        benchmark = BenchmarkResult("단순 변환", elapsed, count)

        print(f"\n{benchmark}")

        # 기준: 1000회 변환 < 0.5초(2000+ ops/s)
        assert benchmark.ops_per_second > 2000

    def test_benchmark_nested_transform(self):
        """중첩 객체 변환 벤치마크"""
        data = {
            "symbol": "005930",
            "name": "삼성전자",
            "current_price": 70000,
            "high": 71000,
            "low": 69000,
            "volume": 5000000,
            "prices": [
                {
                    "symbol": "005930",
                    "price": 70000 + i * 100,
                    "volume": 100000 - i * 1000,
                    "timestamp": f"2024010109{i:02d}00",
                    "market": "KRX",
                }
                for i in range(10)
            ],
        }

        count = 100
        start = time.perf_counter()

        for _ in range(count):
            result = MockQuote.transform_(data, MockQuote)
            assert len(result.prices) == 10

        elapsed = time.perf_counter() - start
        benchmark = BenchmarkResult("중첩 변환(10개 아이템)", elapsed, count)

        print(f"\n{benchmark}")

        # 기준: 100회 변환 < 0.5초(200+ ops/s)
        assert benchmark.ops_per_second > 200

    def test_benchmark_large_list_transform(self):
        """대용량 리스트 변환 벤치마크"""
        data = {
            "symbol": "005930",
            "name": "삼성전자",
            "current_price": 70000,
            "high": 71000,
            "low": 69000,
            "volume": 5000000,
            "prices": [
                {
                    "symbol": "005930",
                    "price": 70000 + i,
                    "volume": 100000,
                    "timestamp": "20240101090000",
                    "market": "KRX",
                }
                for i in range(100)
            ],
        }

        count = 10
        start = time.perf_counter()

        for _ in range(count):
            result = MockQuote.transform_(data, MockQuote)
            assert len(result.prices) == 100

        elapsed = time.perf_counter() - start
        benchmark = BenchmarkResult("대용량 리스트(100개)", elapsed, count)

        print(f"\n{benchmark}")

        # 기준: 10회 변환 < 1.0초(10+ ops/s)
        assert benchmark.ops_per_second > 10

    def test_benchmark_batch_transform(self):
        """배치 변환 벤치마크"""
        prices = [
            {
                "symbol": f"{1000 + i:06d}",
                "price": 50000 + i * 100,
                "volume": 100000 + i * 1000,
                "timestamp": "20240101090000",
                "market": "KRX",
            }
            for i in range(100)
        ]

        start = time.perf_counter()

        results = [MockPrice.transform_(price, MockPrice) for price in prices]

        elapsed = time.perf_counter() - start
        benchmark = BenchmarkResult("배치 변환(100개)", elapsed, len(prices))

        print(f"\n{benchmark}")

        assert len(results) == 100
        # 예전에는 `if elapsed > 0: ... else: assert True` 였다. time.time() 의
        # 해상도 때문에 elapsed 가 0으로 찍히는 것을 우회하려던 것인데,
        # `assert True` 는 아무것도 검사하지 않는다. perf_counter 로 바꾼 뒤로는
        # 우회가 필요 없다.
        assert benchmark.ops_per_second > 100

    def test_benchmark_deep_nesting(self):
        """깊은 중첩 벤치마크"""

        class Level3(KisObject):
            __annotations__ = {"value": int, "name": str}

            @staticmethod
            def __transform__(cls, data):
                obj = cls(cls)
                for key, value in data.items():
                    setattr(obj, key, value)
                return obj

        class Level2(KisObject):
            __annotations__ = {"items": list[Level3], "count": int}

            @staticmethod
            def __transform__(cls, data):
                obj = cls(cls)
                for key, value in data.items():
                    if key == "items" and isinstance(value, list):
                        setattr(
                            obj, key, [Level3.__transform__(Level3, i) if isinstance(i, dict) else i for i in value]
                        )
                    else:
                        setattr(obj, key, value)
                return obj

        class Level1(KisObject):
            __annotations__ = {"data": Level2, "id": str}

            @staticmethod
            def __transform__(cls, data):
                obj = cls(cls)
                for key, value in data.items():
                    if key == "data" and isinstance(value, dict):
                        setattr(obj, key, Level2.__transform__(Level2, value))
                    else:
                        setattr(obj, key, value)
                return obj

        data = {"id": "root", "data": {"count": 5, "items": [{"value": i, "name": f"item_{i}"} for i in range(5)]}}

        count = 100
        start = time.perf_counter()

        for _ in range(count):
            result = Level1.transform_(data, Level1)
            assert result.data.count == 5

        elapsed = time.perf_counter() - start
        benchmark = BenchmarkResult("깊은 중첩 (3레벨, 5개)", elapsed, count)

        print(f"\n{benchmark}")

        # 기준: 100회 < 0.3초(300+ ops/s)
        assert benchmark.ops_per_second > 300

    def test_benchmark_optional_fields(self):
        """선택 필드 벤치마크"""

        class OptionalData(KisObject):
            __annotations__ = {
                "required": str,
                "optional1": int | None,
                "optional2": str | None,
                "optional3": float | None,
            }

            @staticmethod
            def __transform__(cls, data):
                obj = cls(cls)
                for key, value in data.items():
                    setattr(obj, key, value)
                return obj

        # 일부 필드만 있는 데이터
        data = {
            "required": "test",
            "optional1": 42,
            # optional2, optional3 없음
        }

        count = 1000
        start = time.perf_counter()

        for _ in range(count):
            result = OptionalData.transform_(data, OptionalData)
            assert result.required == "test"

        elapsed = time.perf_counter() - start
        benchmark = BenchmarkResult("선택 필드", elapsed, count)

        print(f"\n{benchmark}")

        # 기준: 1000회 < 0.5초(2000+ ops/s)
        assert benchmark.ops_per_second > 2000

    def test_benchmark_comparison(self):
        """다양한 시나리오 비교 벤치마크"""
        scenarios = []

        # 1. 단순
        simple_data = {
            "symbol": "005930",
            "price": 70000,
            "volume": 1000000,
            "timestamp": "20240101090000",
            "market": "KRX",
        }

        count = 500
        start = time.perf_counter()
        for _ in range(count):
            MockPrice.transform_(simple_data, MockPrice)
        scenarios.append(BenchmarkResult("단순 (5필드)", time.perf_counter() - start, count))

        # 2. 중첩 (10개)
        nested_data = {
            "symbol": "005930",
            "name": "삼성전자",
            "current_price": 70000,
            "high": 71000,
            "low": 69000,
            "volume": 5000000,
            "prices": [
                {
                    "symbol": "005930",
                    "price": 70000 + i,
                    "volume": 100000,
                    "timestamp": "20240101090000",
                    "market": "KRX",
                }
                for i in range(10)
            ],
        }

        count = 100
        start = time.perf_counter()
        for _ in range(count):
            MockQuote.transform_(nested_data, MockQuote)
        scenarios.append(BenchmarkResult("중첩 (10개)", time.perf_counter() - start, count))

        # 3. 대용량(100개)
        large_data = {
            "symbol": "005930",
            "name": "삼성전자",
            "current_price": 70000,
            "high": 71000,
            "low": 69000,
            "volume": 5000000,
            "prices": [
                {
                    "symbol": "005930",
                    "price": 70000 + i,
                    "volume": 100000,
                    "timestamp": "20240101090000",
                    "market": "KRX",
                }
                for i in range(100)
            ],
        }

        count = 10
        start = time.perf_counter()
        for _ in range(count):
            MockQuote.transform_(large_data, MockQuote)
        scenarios.append(BenchmarkResult("대용량(100개)", time.perf_counter() - start, count))

        # 결과 출력
        print("\n=== 벤치마크 비교 ===")
        for scenario in scenarios:
            print(scenario)

        # 모든 시나리오가 기준을 충족
        assert all(s.ops_per_second > 10 for s in scenarios)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
