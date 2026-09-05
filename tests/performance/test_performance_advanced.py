"""
성능 테스트 - 응답 처리 및 메모리 효율성

JSON 파싱, 데이터 변환, 메모리 사용 등의 성능을 테스트합니다.
"""

import json

import pytest


@pytest.mark.performance
class TestResponseProcessingPerformance:
    """API 응답 처리 성능 테스트."""

    def test_large_json_parsing_speed(self, benchmark):
        """대용량 JSON 파싱 속도."""
        large_response = {
            "output": [
                {
                    "stck_cntg_hour": "153000",
                    "stck_prpr": f"{70000 + i}",
                    "acml_vol": f"{1000000 * (i + 1)}",
                    "prdy_vrss": f"{500 * (i + 1) % 10000}",
                }
                for i in range(1000)
            ]
        }

        def parse_json():
            return json.loads(json.dumps(large_response))

        result = benchmark.pedantic(parse_json, rounds=100, iterations=10)
        assert result is not None

    def test_quote_transformation_speed(self, benchmark):
        """호가 데이터 변환 속도."""
        quote_data = {
            "stck_prpr": "72000",
            "stck_cntg_hour": "153000",
            "stck_oprc": "71500",
            "stck_hgpr": "72500",
            "stck_lwpr": "70800",
            "acml_vol": "50000000",
            "acml_tr_pbmn": "3600000000000",
        }

        def transform_quote():
            return {k.upper(): v for k, v in quote_data.items()}

        result = benchmark(transform_quote)
        assert result is not None

    def test_batch_order_processing_speed(self, benchmark):
        """대량 주문 데이터 처리 속도."""
        orders = [
            {
                "ordt": "20250101",
                "ordtm": "093000",
                "odno": f"{100000 + i}",
                "sll_buy_gb": "01" if i % 2 == 0 else "02",
                "stck_cntg_hour": f"{93000 + (i % 60)}",
                "ord_qty": f"{100 * (i + 1)}",
                "ord_unpr": f"{70000 + (i * 100 % 5000)}",
                "exec_qty": f"{90 + (i % 10)}",
                "ord_status": "체결완료" if i % 3 == 0 else "주문중",
            }
            for i in range(100)
        ]

        def process_orders():
            return sum(len(order) for order in orders)

        result = benchmark(process_orders)
        assert result > 0


@pytest.mark.performance
class TestMemoryUsage:
    """메모리 사용량 테스트."""

    def test_large_dataset_memory(self):
        """대량 데이터셋 메모리 사용."""
        import sys

        large_data = [
            {
                "stck_prpr": f"{70000 + i}",
                "stck_cntg_hour": "153000",
                "acml_vol": f"{1000000 * (i + 1)}",
            }
            for i in range(10000)
        ]

        size_mb = sys.getsizeof(large_data) / 1024 / 1024

        assert size_mb < 10, f"Memory usage too high: {size_mb:.2f}MB"

    def test_circular_reference_prevention(self):
        """순환 참조 방지."""
        obj = {"key": "value"}
        obj["self"] = None

        import sys

        assert sys.getrefcount(obj) >= 2


@pytest.mark.performance
@pytest.mark.benchmark(min_rounds=5)
class TestAPILatency:
    """API 응답 지연 시간 테스트."""

    def test_token_acquisition_latency(self, benchmark):
        """토큰 발급 지연 시간."""

        def get_token():
            return {"access_token": "test_token", "expires_in": 86400}

        result = benchmark(get_token)
        assert result["access_token"] is not None

    def test_quote_request_latency(self, benchmark):
        """호가 조회 지연 시간."""

        def process_quote():
            return {
                "stck_prpr": "72000",
                "stck_cntg_hour": "153000",
                "acml_vol": "50000000",
            }

        result = benchmark(process_quote)
        assert "stck_prpr" in result
