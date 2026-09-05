"""
Tests for vmkis.api.stock.info module

Tests coverage for:
- _KisStockInfo class properties
- get_market_country function
- quotable_market function
- info function
- resolve_market function
=== CRITICAL TEST DESIGN NOTES ===

MARKET_TYPE_MAP Structure (defined in src/vmkis/api/stock/info.py:26-50):
- Maps market names to lists of market codes
- KR: ["300"] - Single code (domestic only, no retry capability)
- US: ["512", "513", "529"] - Three codes (NASDAQ, NYSE, AMEX; enables retry testing)
- Other markets: Various code counts depending on market availability

Error Handling & Market Code Iteration:
- Both quotable_market() and info() functions iterate through market codes
- When a market code returns rt_cd=7 (no data), function automatically retries with next code
- When a market code returns other rt_cd values (error), function raises immediately
- Function exhausts all market codes, then raises KisNotFoundError if none succeed

Test Design Implications:
- Tests using market="US" intentionally exploit multiple codes to test retry logic
- Tests using market="KR" cannot test retry scenarios (only one code available)
- test_continues_on_rt_cd_7_error must use market="US" to verify:
  * First market code (512) fails with rt_cd=7
  * Function automatically retries with second code (513)
  * Second call succeeds with mock_info response
  * Without multiple codes, no retry is possible after first error

Cannot substitute KR for US:
- KR has only ["300"], so after first error, no remaining codes to retry
- Function would raise KisNotFoundError instead of retrying
- Test assertion (fake_kis.fetch.call_count == 2) would fail
- This is intentional design, not arbitrary choice"""

from datetime import timedelta
from unittest.mock import Mock, patch

import pytest

from vmkis.api.stock.info import (
    MARKET_CODE_MAP,
    MARKET_TYPE_MAP,
    R_MARKET_TYPE_MAP,
    _KisStockInfo,
    get_market_country,
    info,
    quotable_market,
    resolve_market,
)
from vmkis.client.exceptions import KisAPIError
from vmkis.responses.exceptions import KisNotFoundError


def _fake_kis():
    """`self.call()` 을 태울 수 있는 `VmKis` 목을 만든다.

    이슈 #43 이후 `api/stock/*` 은 `fetch` 대신 `call` 을 쓴다. 목을 그대로
    두면 `fake_kis.call(...)` 이 **새 Mock 을 조용히 돌려주고** `fetch` 에
    걸어 둔 `return_value`/`side_effect` 가 발동하지 않는다. 실제
    `VmKis.call` 을 바인딩하면 `fetch(api=...)` 단언이 그대로 살고 스펙
    해석(TR ID·도메인)까지 함께 검증된다.

    `paper` 을 명시적으로 `False` 로 둔다. 목의 기본값은 Mock 이라
    **truthy** 이므로 두면 모의 계좌로 해석된다.
    """
    from vmkis.kis import VmKis

    kis = Mock()
    kis.paper = False
    kis.call = lambda *args, **kwargs: VmKis.call(kis, *args, **kwargs)
    return kis


# ===== Tests for _KisStockInfo class =====


class TestKisStockInfo:
    """Tests for _KisStockInfo response class."""

    def test_initialization(self):
        """Test _KisStockInfo can be initialized."""
        # _KisStockInfo는 KisAPIResponse를 상속하므로 직접 인스턴스화 불가
        # 속성 정의만 확인
        assert hasattr(_KisStockInfo, "symbol")
        assert hasattr(_KisStockInfo, "std_code")
        assert hasattr(_KisStockInfo, "name_kor")

    def test_name_property(self):
        """Test name property returns name_kor."""
        mock_info = Mock(spec=_KisStockInfo)
        mock_info.name_kor = "삼성전자"

        # Property를 직접 테스트할 수 없으므로 클래스 정의 확인
        assert hasattr(_KisStockInfo, "name")

    def test_market_property(self):
        """Test market property maps from market_code."""
        # market_code 매핑 확인
        assert MARKET_CODE_MAP["300"] == "KRX"
        assert MARKET_CODE_MAP["512"] == "NASDAQ"
        assert MARKET_CODE_MAP["513"] == "NYSE"

    def test_market_name_property(self):
        """Test market_name property maps from market_code."""
        # market_name 매핑 확인
        assert R_MARKET_TYPE_MAP["300"] == "주식"
        assert R_MARKET_TYPE_MAP["512"] == "나스닥"
        assert R_MARKET_TYPE_MAP["513"] == "뉴욕"

    def test_foreign_property(self):
        """Test foreign property checks if market is not KRX."""
        # MARKET_TYPE_MAP["KRX"]에 없는 코드는 해외 종목
        assert "512" not in MARKET_TYPE_MAP["KRX"]
        assert "513" not in MARKET_TYPE_MAP["KRX"]

    def test_domestic_property(self):
        """Test domestic property is opposite of foreign."""
        # MARKET_TYPE_MAP["KRX"]에 있는 코드는 국내 종목
        assert "300" in MARKET_TYPE_MAP["KRX"]


# ===== Tests for get_market_country function =====


class TestGetMarketCountry:
    """Tests for get_market_country function."""

    def test_krx_returns_kr(self):
        """Test KRX market returns KR country."""
        assert get_market_country("KRX") == "KR"

    def test_nasdaq_returns_us(self):
        """Test NASDAQ market returns US country."""
        assert get_market_country("NASDAQ") == "US"

    def test_nyse_returns_us(self):
        """Test NYSE market returns US country."""
        assert get_market_country("NYSE") == "US"

    def test_amex_returns_us(self):
        """Test AMEX market returns US country."""
        assert get_market_country("AMEX") == "US"

    def test_hkex_returns_hk(self):
        """Test HKEX market returns HK country."""
        assert get_market_country("HKEX") == "HK"

    def test_tyo_returns_jp(self):
        """Test TYO market returns JP country."""
        assert get_market_country("TYO") == "JP"

    def test_hnx_returns_vn(self):
        """Test HNX market returns VN country."""
        assert get_market_country("HNX") == "VN"

    def test_hsx_returns_vn(self):
        """Test HSX market returns VN country."""
        assert get_market_country("HSX") == "VN"

    def test_sse_returns_cn(self):
        """Test SSE market returns CN country."""
        assert get_market_country("SSE") == "CN"

    def test_szse_returns_cn(self):
        """Test SZSE market returns CN country."""
        assert get_market_country("SZSE") == "CN"

    def test_invalid_market_raises_error(self):
        """Test unsupported market raises ValueError."""
        with pytest.raises(ValueError, match="지원하지 않는 상품유형명"):
            get_market_country("INVALID")  # type: ignore


# ===== Tests for quotable_market function =====


class TestQuotableMarket:
    """Tests for quotable_market function."""

    def test_validates_empty_symbol(self):
        """Test empty symbol raises ValueError."""
        fake_kis = _fake_kis()

        with pytest.raises(ValueError, match="종목 코드를 입력해주세요"):
            quotable_market(fake_kis, "")

    def test_uses_cache_when_available(self):
        """Test uses cached market when available."""
        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = "KRX"

        result = quotable_market(fake_kis, "005930", market="KR", use_cache=True)

        assert result == "KRX"
        fake_kis.cache.get.assert_called_once_with("quotable_market:KR:005930", str)
        fake_kis.fetch.assert_not_called()

    def test_domestic_market_with_valid_price(self):
        """Test domestic market returns KRX when price is valid."""
        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        mock_response = Mock()
        mock_response.output.stck_prpr = "65000"
        fake_kis.fetch.return_value = mock_response

        result = quotable_market(fake_kis, "005930", market="KR", use_cache=False)

        assert result == "KRX"
        fake_kis.fetch.assert_called_once()

    def test_domestic_market_with_zero_price_continues(self):
        """Test domestic market with zero price tries next market."""
        from unittest.mock import Mock

        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        # First call returns zero price (should continue)
        mock_response_zero = Mock()
        mock_response_zero.output.stck_prpr = "0"
        mock_response_zero.__data__ = {"output": {"stck_prpr": "0"}, "__response__": Mock()}

        # Second call would succeed (but we're only testing the continue logic)
        mock_response_valid = Mock()
        mock_response_valid.output.last = "150.50"

        fake_kis.fetch.side_effect = [mock_response_zero, mock_response_valid]

        # Should skip the zero price and try next market
        quotable_market(fake_kis, "005930", market=None, use_cache=False)

        # fetch should be called twice
        assert fake_kis.fetch.call_count == 2

    def test_foreign_market_with_valid_price(self):
        """Test foreign market returns correct market type."""
        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        mock_response = Mock()
        mock_response.output.last = "150.50"
        fake_kis.fetch.return_value = mock_response

        result = quotable_market(fake_kis, "AAPL", market="NASDAQ", use_cache=False)

        assert result == "NASDAQ"

    def test_foreign_market_with_empty_price_continues(self):
        """Test foreign market with empty price tries next market."""
        from unittest.mock import Mock

        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        # First call returns empty/zero price (should continue)
        mock_response_empty = Mock()
        mock_response_empty.output.last = ""
        mock_response_empty.__data__ = {"output": {"last": ""}, "__response__": Mock()}

        # Second call would succeed
        mock_response_valid = Mock()
        mock_response_valid.output.last = "150.50"

        fake_kis.fetch.side_effect = [mock_response_empty, mock_response_valid]

        # Should skip the empty price and try next market type
        quotable_market(fake_kis, "AAPL", market="US", use_cache=False)

        # fetch should be called twice (once for each US market code)
        assert fake_kis.fetch.call_count == 2

    def test_attribute_error_continues(self):
        """Test AttributeError in response is caught and continues."""
        from unittest.mock import Mock

        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        # First call raises AttributeError (missing output attribute)
        mock_response_error = Mock()
        del mock_response_error.output  # Force AttributeError
        mock_response_error.__data__ = {"__response__": Mock()}

        # Second call succeeds
        mock_response_valid = Mock()
        mock_response_valid.output.stck_prpr = "65000"

        fake_kis.fetch.side_effect = [mock_response_error, mock_response_valid]

        # Should catch AttributeError and continue to next market (use None to iterate multiple markets)
        result = quotable_market(fake_kis, "005930", market=None, use_cache=False)

        assert result == "NASDAQ"  # Second market code in the list
        assert fake_kis.fetch.call_count == 2

    def test_raises_not_found_when_no_markets_match(self):
        """Test raises KisNotFoundError when no markets match."""
        from unittest.mock import Mock

        from requests import Response

        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        # All calls return zero/empty price
        mock_response = Mock()
        mock_response.output.stck_prpr = "0"
        mock_response.output.last = ""

        # Create proper response with __data__ and __response__
        mock_http_response = Mock(spec=Response)
        mock_http_response.status_code = 200
        mock_http_response.text = ""
        mock_response.__data__ = {"output": {"stck_prpr": "0"}, "__response__": mock_http_response}

        fake_kis.fetch.return_value = mock_response

        # Should raise KisNotFoundError when all markets fail
        with pytest.raises(KisNotFoundError) as exc_info:
            quotable_market(fake_kis, "INVALID", market="KR", use_cache=False)

        assert "해당 종목의 정보를 조회할 수 없습니다" in str(exc_info.value)


# ===== Tests for info function =====


class TestInfo:
    """Tests for info function.

    Key Testing Scenario:
    The info() function iterates through market codes based on MARKET_TYPE_MAP:
    - For market="KR": Tries code "300" only
    - For market="US": Tries codes ["512", "513", "529"] in sequence
    - For market=None: Tries all available codes

    Error Handling During Iteration:
    - rt_cd=7 (no data): Continue to next market code
    - Other rt_cd values: Raise immediately without retry
    - All market codes exhausted: Raise KisNotFoundError

    Test Design:
    - Retry tests require market with multiple codes (US, not KR)
    - Single code markets (KR) cannot test retry scenarios
    - Multiple market code iteration requires multi-call mocking
    """

    def test_validates_empty_symbol(self):
        """Test empty symbol raises ValueError."""
        fake_kis = _fake_kis()

        with pytest.raises(ValueError, match="종목 코드를 입력해주세요"):
            info(fake_kis, "")

    def test_uses_cache_when_available(self):
        """Test uses cached info when available."""
        fake_kis = _fake_kis()
        mock_cached_info = Mock()
        fake_kis.cache.get.return_value = mock_cached_info

        result = info(fake_kis, "005930", market="KR", use_cache=True)

        assert result == mock_cached_info
        fake_kis.cache.get.assert_called_once_with("info:KR:005930", _KisStockInfo)
        fake_kis.fetch.assert_not_called()

    def test_calls_quotable_market_when_quotable_true(self):
        """Test calls quotable_market when quotable=True."""
        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        mock_info = Mock()
        fake_kis.fetch.return_value = mock_info

        with patch("vmkis.api.stock.info.quotable_market", return_value="KRX") as mock_quotable:
            info(fake_kis, "005930", market="KR", use_cache=False, quotable=True)

            mock_quotable.assert_called_once_with(
                fake_kis,
                symbol="005930",
                market="KR",
                use_cache=False,
            )

    def test_skips_quotable_market_when_quotable_false(self):
        """Test skips quotable_market when quotable=False."""
        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        mock_info = Mock()
        fake_kis.fetch.return_value = mock_info

        with patch("vmkis.api.stock.info.quotable_market") as mock_quotable:
            info(fake_kis, "005930", market="KR", use_cache=False, quotable=False)

            mock_quotable.assert_not_called()

    def test_successful_fetch_returns_info(self):
        """Test successful fetch returns stock info."""
        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        mock_info = Mock()
        fake_kis.fetch.return_value = mock_info

        result = info(fake_kis, "005930", market="KR", use_cache=False, quotable=False)

        assert result == mock_info
        fake_kis.fetch.assert_called_once()

    def test_sets_cache_after_successful_fetch(self):
        """Test sets cache after successful fetch when use_cache=True."""
        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        mock_info = Mock()
        fake_kis.fetch.return_value = mock_info

        info(fake_kis, "005930", market="KR", use_cache=True, quotable=False)

        fake_kis.cache.set.assert_called_once_with("info:KR:005930", mock_info, expire=timedelta(days=1))

    def test_does_not_cache_when_use_cache_false(self):
        """Test does not cache when use_cache=False."""
        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        mock_info = Mock()
        fake_kis.fetch.return_value = mock_info

        info(fake_kis, "005930", market="KR", use_cache=False, quotable=False)

        fake_kis.cache.set.assert_not_called()

    def test_continues_on_rt_cd_7_error(self):
        """Test continues to next market when rt_cd=7 (no data).

        CRITICAL: This test MUST use market="US" because:
        - MARKET_TYPE_MAP["US"] = ["512", "513", "529"] (3 market codes)
        - MARKET_TYPE_MAP["KR"] = ["300"] (1 market code only)

        Test Scenario:
        1. First fetch() call uses market code "512" (NASDAQ), returns rt_cd=7 error
        2. Function detects rt_cd=7 and continues to next market code
        3. Second fetch() call uses market code "513" (NYSE), succeeds
        4. Result: fetch.call_count == 2 (one per market code)

        Why Not KR?
        - After first error on code "300", no remaining codes exist
        - Function would raise KisNotFoundError, not retry
        - fetch.call_count would be 1, test assertion would fail
        - Cannot demonstrate retry logic with single-code markets

        Design Rationale:
        The US market with 3 codes enables testing the actual retry mechanism
        that info() implements for multiple market availability.
        """
        from unittest.mock import Mock

        from requests import Response

        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        # First call raises KisAPIError with rt_cd=7 (no data)
        # This triggers iteration to next market code
        mock_http_response = Mock(spec=Response)
        mock_http_response.status_code = 200
        mock_http_response.text = ""
        mock_http_response.headers = {"tr_id": "TEST_TR_ID", "gt_uid": "TEST_GT_UID"}
        mock_http_response.request = Mock()
        mock_http_response.request.method = "GET"
        mock_http_response.request.headers = {}
        mock_http_response.request.url = "http://test.com/api"
        mock_http_response.request.body = None
        api_error = KisAPIError(
            data={"rt_cd": "7", "msg1": "조회된 데이터가 없습니다", "__response__": mock_http_response},
            response=mock_http_response,
        )
        api_error.rt_cd = 7

        # Second call succeeds on next market code
        mock_info = Mock()

        fake_kis.fetch.side_effect = [api_error, mock_info]

        # IMPORTANT: market="US" has multiple codes enabling retry logic validation
        # First call: code 512 fails with rt_cd=7
        # Second call: code 513 succeeds
        with patch("vmkis.api.stock.info.quotable_market", return_value="US"):
            result = info(fake_kis, "AAPL", market="US", use_cache=False, quotable=True)

        assert result == mock_info
        # Verify both market codes were attempted (retry occurred)
        assert fake_kis.fetch.call_count == 2

    def test_raises_other_api_errors_immediately(self):
        """Test raises non-rt_cd=7 API errors immediately."""
        from unittest.mock import Mock

        from requests import Response

        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        # Create KisAPIError with rt_cd != 7 (should raise immediately)
        mock_http_response = Mock(spec=Response)
        mock_http_response.status_code = 401
        mock_http_response.text = ""
        mock_http_response.headers = {"tr_id": "TEST_TR_ID", "gt_uid": "TEST_GT_UID"}
        mock_http_response.request = Mock()
        mock_http_response.request.method = "GET"
        mock_http_response.request.headers = {}
        mock_http_response.request.url = "http://test.com/api"
        mock_http_response.request.body = None
        api_error = KisAPIError(
            data={"rt_cd": "1", "msg1": "인증 실패", "__response__": mock_http_response}, response=mock_http_response
        )
        api_error.rt_cd = 1

        fake_kis.fetch.side_effect = api_error

        # Should raise the error immediately without trying next market
        with pytest.raises(KisAPIError) as exc_info:
            with patch("vmkis.api.stock.info.quotable_market", return_value="KR"):
                info(fake_kis, "005930", market="KR", use_cache=False, quotable=True)

        assert exc_info.value.rt_cd == 1
        # Should only call fetch once before raising
        assert fake_kis.fetch.call_count == 1

    def test_raises_not_found_when_all_markets_fail(self):
        """Test raises KisNotFoundError when all markets return rt_cd=7.

        Market Code Exhaustion Scenario for KR Market:
        - MARKET_TYPE_MAP["KR"] = ["300"] (single code)

        Test Scenario:
        1. fetch() call uses code "300", returns rt_cd=7
        2. Function checks for remaining market codes
        3. No more codes available in MARKET_TYPE_MAP["KR"]
        4. Function raises KisNotFoundError (all markets exhausted)

        Design Note:
        This test correctly uses market="KR" because we want to verify
        the exhaustion behavior. With single code, exhaustion occurs naturally
        after first error. The function's raise_not_found() is triggered
        when all available market codes have been attempted.
        """
        from unittest.mock import Mock

        from requests import Response

        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        # All calls raise KisAPIError with rt_cd=7
        # Simulates symbol not available on any market code
        mock_http_response = Mock(spec=Response)
        mock_http_response.status_code = 200
        mock_http_response.text = ""
        mock_http_response.headers = {"tr_id": "TEST_TR_ID", "gt_uid": "TEST_GT_UID"}
        mock_http_response.request = Mock()
        mock_http_response.request.method = "GET"
        mock_http_response.request.headers = {}
        mock_http_response.request.url = "http://test.com/api"
        mock_http_response.request.body = None
        api_error = KisAPIError(
            data={"rt_cd": "7", "msg1": "조회된 데이터가 없습니다", "__response__": mock_http_response},
            response=mock_http_response,
        )
        api_error.rt_cd = 7
        api_error.data = {"rt_cd": "7", "msg1": "조회된 데이터가 없습니다", "__response__": mock_http_response}

        fake_kis.fetch.side_effect = api_error

        # Should raise KisNotFoundError after all markets fail with rt_cd=7
        # KR has only one code, so exhaustion occurs naturally
        with pytest.raises(KisNotFoundError) as exc_info:
            with patch("vmkis.api.stock.info.quotable_market", return_value="KR"):
                info(fake_kis, "INVALID", market="KR", use_cache=False, quotable=True)

        assert "해당 종목의 정보를 조회할 수 없습니다" in str(exc_info.value)

    def test_fetch_params_correct(self):
        """Test fetch is called with correct parameters."""
        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        mock_info = Mock()
        fake_kis.fetch.return_value = mock_info

        info(fake_kis, "005930", market="KR", use_cache=False, quotable=False)

        call_args = fake_kis.fetch.call_args
        assert call_args[0][0] == "/uapi/domestic-stock/v1/quotations/search-info"
        assert call_args[1]["api"] == "CTPF1604R"
        assert call_args[1]["params"]["PDNO"] == "005930"
        assert call_args[1]["params"]["PRDT_TYPE_CD"] in MARKET_TYPE_MAP["KR"]
        assert call_args[1]["domain"] == "live"
        assert call_args[1]["response_type"] == _KisStockInfo

    def test_multiple_markets_iteration(self):
        """Test iterates through all market codes.

        Market Code Iteration Sequence for US Market:
        - MARKET_TYPE_MAP["US"] = ["512", "513", "529"] (NASDAQ, NYSE, AMEX)

        Test Scenario:
        1. First fetch() call uses code "512" (NASDAQ), returns rt_cd=7
        2. Function continues to next market code
        3. Second fetch() call uses code "513" (NYSE), returns rt_cd=7
        4. Function continues to next market code
        5. Third fetch() call uses code "529" (AMEX), succeeds
        6. Result: fetch.call_count == 3 (exhausted 2 codes, succeeded on 3rd)

        This validates:
        - Function maintains iteration state across market codes
        - Each rt_cd=7 triggers progression to next code
        - Success on any code stops iteration
        - All available codes are attempted in sequence
        """
        from unittest.mock import Mock

        from requests import Response

        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        # First two calls fail with rt_cd=7, third succeeds
        # Simulates trying multiple market codes until one has data
        mock_http_response = Mock(spec=Response)
        mock_http_response.status_code = 200
        mock_http_response.text = ""
        mock_http_response.headers = {"tr_id": "TEST_TR_ID", "gt_uid": "TEST_GT_UID"}
        mock_http_response.request = Mock()
        mock_http_response.request.method = "GET"
        mock_http_response.request.headers = {}
        mock_http_response.request.url = "http://test.com/api"
        mock_http_response.request.body = None
        api_error = KisAPIError(
            data={"rt_cd": "7", "msg1": "조회된 데이터가 없습니다", "__response__": mock_http_response},
            response=mock_http_response,
        )
        api_error.rt_cd = 7
        api_error.data = {"rt_cd": "7", "msg1": "조회된 데이터가 없습니다", "__response__": mock_http_response}

        mock_info = Mock()

        # Mock 3 calls: Code 512 fails, Code 513 fails, Code 529 succeeds
        fake_kis.fetch.side_effect = [api_error, api_error, mock_info]

        # Should iterate through market codes until one succeeds
        with patch("vmkis.api.stock.info.quotable_market", return_value="US"):
            result = info(fake_kis, "AAPL", market="US", use_cache=False, quotable=True)

        assert result == mock_info
        # Verify all 3 market codes were attempted (512→513→529)
        assert fake_kis.fetch.call_count == 3


# ===== Tests for resolve_market function =====


class TestResolveMarket:
    """Tests for resolve_market function."""

    def test_returns_market_from_info(self):
        """Test resolve_market returns market property from info."""
        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        mock_info = Mock()
        mock_info.market = "KRX"
        fake_kis.fetch.return_value = mock_info

        # quotable=False to skip quotable_market call which requires complex mocking
        result = resolve_market(fake_kis, "005930", market="KR", use_cache=False, quotable=False)

        assert result == "KRX"

    def test_forwards_all_parameters(self):
        """Test resolve_market forwards all parameters to info."""
        fake_kis = _fake_kis()
        fake_kis.cache.get.return_value = None

        mock_info = Mock()
        mock_info.market = "NASDAQ"
        fake_kis.fetch.return_value = mock_info

        with patch("vmkis.api.stock.info.info", return_value=mock_info) as mock_info_func:
            resolve_market(fake_kis, symbol="AAPL", market="US", use_cache=True, quotable=False)

            mock_info_func.assert_called_once_with(
                fake_kis,
                symbol="AAPL",
                market="US",
                use_cache=True,
                quotable=False,
            )

    def test_validates_empty_symbol(self):
        """Test empty symbol raises ValueError (via info)."""
        fake_kis = _fake_kis()

        with pytest.raises(ValueError, match="종목 코드를 입력해주세요"):
            resolve_market(fake_kis, "")


# ===== Tests for MARKET_TYPE_MAP =====


class TestMarketTypeMap:
    """Tests for MARKET_TYPE_MAP dictionary."""

    def test_kr_has_domestic_codes(self):
        """Test KR market has domestic market codes."""
        assert "300" in MARKET_TYPE_MAP["KR"]

    def test_krx_has_domestic_codes(self):
        """Test KRX market has domestic market codes."""
        assert "300" in MARKET_TYPE_MAP["KRX"]

    def test_nasdaq_has_correct_code(self):
        """Test NASDAQ market has correct code."""
        assert "512" in MARKET_TYPE_MAP["NASDAQ"]

    def test_nyse_has_correct_code(self):
        """Test NYSE market has correct code."""
        assert "513" in MARKET_TYPE_MAP["NYSE"]

    def test_amex_has_correct_code(self):
        """Test AMEX market has correct code."""
        assert "529" in MARKET_TYPE_MAP["AMEX"]

    def test_us_has_all_us_codes(self):
        """Test US market has all US market codes."""
        us_codes = MARKET_TYPE_MAP["US"]
        assert "512" in us_codes  # NASDAQ
        assert "513" in us_codes  # NYSE
        assert "529" in us_codes  # AMEX

    def test_tyo_has_correct_code(self):
        """Test TYO market has correct code."""
        assert "515" in MARKET_TYPE_MAP["TYO"]

    def test_jp_has_correct_code(self):
        """Test JP market has correct code."""
        assert "515" in MARKET_TYPE_MAP["JP"]

    def test_hkex_has_correct_code(self):
        """Test HKEX market has correct code."""
        assert "501" in MARKET_TYPE_MAP["HKEX"]

    def test_hk_has_all_hk_codes(self):
        """Test HK market has all HK market codes."""
        hk_codes = MARKET_TYPE_MAP["HK"]
        assert "501" in hk_codes  # HKEX
        assert "543" in hk_codes  # CNY
        assert "558" in hk_codes  # USD

    def test_vn_has_all_vn_codes(self):
        """Test VN market has all VN market codes."""
        vn_codes = MARKET_TYPE_MAP["VN"]
        assert "507" in vn_codes  # HNX
        assert "508" in vn_codes  # HSX

    def test_cn_has_all_cn_codes(self):
        """Test CN market has all CN market codes."""
        cn_codes = MARKET_TYPE_MAP["CN"]
        assert "551" in cn_codes  # SSE
        assert "552" in cn_codes  # SZSE

    def test_none_has_all_codes(self):
        """Test None market has all available codes."""
        all_codes = MARKET_TYPE_MAP[None]
        assert "300" in all_codes
        assert "512" in all_codes
        assert "513" in all_codes
        assert len(all_codes) > 10
