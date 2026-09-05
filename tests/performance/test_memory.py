"""
메모리 프로파일 테스트
KisObject의 메모리 사용량을 추적합니다
"""

import tracemalloc

from vmkis.responses.dynamic import KisObject


class MockData(KisObject):
    """모의 데이터"""

    __annotations__ = {
        "id": str,
        "value": int,
        "name": str,
        "data": str,
    }

    @staticmethod
    def __transform__(cls, data):
        obj = cls(cls)
        for key, value in data.items():
            setattr(obj, key, value)
        return obj


class MockNested(KisObject):
    """중첩 데이터"""

    __annotations__ = {
        "id": str,
        "items": list[MockData],
    }

    @staticmethod
    def __transform__(cls, data):
        obj = cls(cls)
        for key, value in data.items():
            if key == "items" and isinstance(value, list):
                setattr(obj, key, [MockData.__transform__(MockData, i) if isinstance(i, dict) else i for i in value])
            else:
                setattr(obj, key, value)
        return obj


class MemoryProfile:
    """메모리 프로파일 결과"""

    def __init__(self, name: str, peak_kb: float, diff_kb: float, count: int):
        self.name = name
        self.peak_kb = peak_kb
        self.diff_kb = diff_kb
        self.count = count

    @property
    def per_item_kb(self) -> float:
        """항목당 메모리 사용량 (KB)"""
        if self.count > 0:
            return self.diff_kb / self.count
        return 0.0

    def __repr__(self):
        return f"{self.name}: {self.diff_kb:.1f}KB total, {self.per_item_kb:.3f}KB/item (peak: {self.peak_kb:.1f}KB)"


class TestMemoryUsage:
    """메모리 사용량 테스트"""

    def test_memory_single_object(self):
        """단일 객체 메모리 사용량"""
        tracemalloc.start()

        snapshot_before = tracemalloc.take_snapshot()

        # 1000개 객체 생성
        objects = []
        for i in range(1000):
            data = {
                "id": f"test_{i}",
                "value": i,
                "name": f"name_{i}",
                "data": "x" * 100,
            }
            obj = MockData.transform_(data, MockData)
            objects.append(obj)

        snapshot_after = tracemalloc.take_snapshot()

        # 메모리 사용량 계산
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        top_stats = snapshot_after.compare_to(snapshot_before, "lineno")
        total_diff = sum(stat.size_diff for stat in top_stats) / 1024  # KB

        profile = MemoryProfile(name="single_object", peak_kb=peak / 1024, diff_kb=total_diff, count=1000)

        print(f"\n{profile}")

        # 객체당 메모리가 합리적인지 확인 (예: 10KB 미만)
        assert profile.per_item_kb < 10.0, f"Too much memory per item: {profile.per_item_kb:.3f}KB"

    def test_memory_nested_objects(self):
        """중첩 객체 메모리 사용량"""
        tracemalloc.start()

        snapshot_before = tracemalloc.take_snapshot()

        # 100개 중첩 객체 (각 10개 아이템)
        objects = []
        for i in range(100):
            items = [
                {
                    "id": f"item_{i}_{j}",
                    "value": j,
                    "name": f"name_{j}",
                    "data": "x" * 50,
                }
                for j in range(10)
            ]

            data = {
                "id": f"nested_{i}",
                "items": items,
            }
            obj = MockNested.transform_(data, MockNested)
            objects.append(obj)

        snapshot_after = tracemalloc.take_snapshot()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        top_stats = snapshot_after.compare_to(snapshot_before, "lineno")
        total_diff = sum(stat.size_diff for stat in top_stats) / 1024

        profile = MemoryProfile(name="nested_objects", peak_kb=peak / 1024, diff_kb=total_diff, count=100)

        print(f"\n{profile}")
        assert profile.per_item_kb < 50.0

    def test_memory_large_batch(self):
        """대량 배치 메모리 사용량"""
        tracemalloc.start()

        snapshot_before = tracemalloc.take_snapshot()

        # 10000개 객체
        objects = []
        for i in range(10000):
            data = {
                "id": f"batch_{i}",
                "value": i % 1000,
                "name": f"item_{i}",
                "data": "x" * 50,
            }
            obj = MockData.transform_(data, MockData)
            objects.append(obj)

        snapshot_after = tracemalloc.take_snapshot()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        top_stats = snapshot_after.compare_to(snapshot_before, "lineno")
        total_diff = sum(stat.size_diff for stat in top_stats) / 1024

        profile = MemoryProfile(name="large_batch", peak_kb=peak / 1024, diff_kb=total_diff, count=10000)

        print(f"\n{profile}")
        assert profile.diff_kb < 50000  # 50MB 미만

    def test_memory_reuse(self):
        """객체 재사용 메모리 사용량"""
        tracemalloc.start()

        data = {
            "id": "test",
            "value": 100,
            "name": "name",
            "data": "x" * 100,
        }

        snapshot_before = tracemalloc.take_snapshot()

        # 같은 데이터로 1000번 변환
        for _ in range(1000):
            MockData.transform_(data, MockData)

        snapshot_after = tracemalloc.take_snapshot()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        top_stats = snapshot_after.compare_to(snapshot_before, "lineno")
        total_diff = sum(stat.size_diff for stat in top_stats) / 1024

        profile = MemoryProfile(name="reuse", peak_kb=peak / 1024, diff_kb=total_diff, count=1000)

        print(f"\n{profile}")
        # 재사용시 메모리가 많이 증가하지 않아야 함
        assert profile.per_item_kb < 5.0

    def test_memory_cleanup(self):
        """메모리 정리 테스트"""
        import gc

        tracemalloc.start()

        # 많은 객체 생성
        objects = []
        for i in range(1000):
            data = {
                "id": f"cleanup_{i}",
                "value": i,
                "name": f"name_{i}",
                "data": "x" * 100,
            }
            obj = MockData.transform_(data, MockData)
            objects.append(obj)

        tracemalloc.take_snapshot()
        before_mem = tracemalloc.get_traced_memory()[0]

        # 객체 제거
        objects.clear()
        gc.collect()

        tracemalloc.take_snapshot()
        after_mem = tracemalloc.get_traced_memory()[0]
        tracemalloc.stop()

        # 메모리가 해제되었는지 확인
        diff_kb = (after_mem - before_mem) / 1024
        print(f"\nMemory diff after cleanup: {diff_kb:.1f}KB")

        # 정리 후 메모리 증가가 거의 없어야 함
        assert diff_kb < 100  # 100KB 미만

    def test_memory_deep_nesting(self):
        """깊은 중첩 메모리 사용량"""
        tracemalloc.start()

        snapshot_before = tracemalloc.take_snapshot()

        # 50개 객체, 각 50개 아이템
        objects = []
        for i in range(50):
            items = [
                {
                    "id": f"deep_{i}_{j}",
                    "value": j,
                    "name": f"name_{j}",
                    "data": "x" * 100,
                }
                for j in range(50)
            ]

            data = {
                "id": f"parent_{i}",
                "items": items,
            }
            obj = MockNested.transform_(data, MockNested)
            objects.append(obj)

        snapshot_after = tracemalloc.take_snapshot()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        top_stats = snapshot_after.compare_to(snapshot_before, "lineno")
        total_diff = sum(stat.size_diff for stat in top_stats) / 1024

        profile = MemoryProfile(name="deep_nesting", peak_kb=peak / 1024, diff_kb=total_diff, count=50)

        print(f"\n{profile}")
        assert profile.per_item_kb < 200.0

    def test_memory_allocation_pattern(self):
        """메모리 할당 패턴 분석"""
        tracemalloc.start()

        # 여러 크기의 객체 생성
        objects = []

        # 작은 객체 (100개)
        for i in range(100):
            data = {"id": f"s_{i}", "value": i, "name": "small", "data": "x" * 10}
            objects.append(MockData.transform_(data, MockData))

        small_mem = tracemalloc.get_traced_memory()[0]

        # 중간 객체 (100개)
        for i in range(100):
            data = {"id": f"m_{i}", "value": i, "name": "medium", "data": "x" * 100}
            objects.append(MockData.transform_(data, MockData))

        medium_mem = tracemalloc.get_traced_memory()[0]

        # 큰 객체 (100개)
        for i in range(100):
            data = {"id": f"l_{i}", "value": i, "name": "large", "data": "x" * 1000}
            objects.append(MockData.transform_(data, MockData))

        large_mem = tracemalloc.get_traced_memory()[0]

        tracemalloc.stop()

        # 메모리 증가 패턴 확인
        small_diff = small_mem / 1024
        medium_diff = (medium_mem - small_mem) / 1024
        large_diff = (large_mem - medium_mem) / 1024

        print(f"\nSmall objects: {small_diff:.1f}KB")
        print(f"Medium objects: {medium_diff:.1f}KB")
        print(f"Large objects: {large_diff:.1f}KB")

        # 큰 객체가 더 많은 메모리를 사용해야 함
        assert large_diff > medium_diff > small_diff
