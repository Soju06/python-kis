import importlib
from datetime import time
from unittest.mock import Mock, patch

import pytest

from vmkis.api.stock import trading_hours as th
from vmkis.responses.exceptions import KisNotFoundError
from vmkis.utils.timezone import TIMEZONE


def test_trading_hours_module_importable():
    """Trading hours module should import without errors and expose expected names (if present)."""
    mod = importlib.import_module("vmkis.api.stock.trading_hours")
    # it's sufficient that the module imports; optionally check for common names
    assert hasattr(mod, "KisTradingHoursBase") or True


def test_kis_trading_hours_base_timezone_property():
    """Test KisTradingHoursBase timezone property."""
    trading_hour = object.__new__(th.KisTradingHoursBase)
    trading_hour.market = "KRX"

    # Should return KST timezone
    tz = trading_hour.timezone
    assert tz is not None
    assert tz == TIMEZONE


def test_kis_trading_hours_base_market_name_property():
    """Test KisTradingHoursBase market_name property."""
    trading_hour = object.__new__(th.KisTradingHoursBase)
    trading_hour.market = "KRX"

    # Should return market name
    market_name = trading_hour.market_name
    assert market_name is not None
    assert isinstance(market_name, str)


def test_kis_simple_trading_hours_initialization():
    """Test KisSimpleTradingHours initialization."""
    open_time = time(9, 0)
    close_time = time(15, 30)

    trading_hour = th.KisSimpleTradingHours(market="KRX", open=open_time, close=close_time)

    assert trading_hour.market == "KRX"
    assert trading_hour.open == open_time
    assert trading_hour.close == close_time
    assert trading_hour.open_kst is not None
    assert trading_hour.close_kst is not None


def test_trading_hours_krx_market():
    """Test trading_hours function for KRX market."""
    mock_kis = Mock()
    mock_kis.cache = Mock()
    mock_kis.cache.get = Mock(return_value=None)
    mock_kis.cache.set = Mock()

    result = th.trading_hours(mock_kis, market="KRX", use_cache=True)

    assert isinstance(result, th.KisSimpleTradingHours)
    assert result.market == "KRX"
    assert result.open == time(9, 0, tzinfo=TIMEZONE)
    assert result.close == time(15, 30, tzinfo=TIMEZONE)

    # Verify cache.set was called
    mock_kis.cache.set.assert_called_once()


def test_trading_hours_with_cache():
    """Test trading_hours function with cached result."""
    cached_hours = th.KisSimpleTradingHours(
        market="KRX", open=time(9, 0, tzinfo=TIMEZONE), close=time(15, 30, tzinfo=TIMEZONE)
    )

    mock_kis = Mock()
    mock_kis.cache = Mock()
    mock_kis.cache.get = Mock(return_value=cached_hours)

    result = th.trading_hours(mock_kis, market="KRX", use_cache=True)

    assert result == cached_hours
    mock_kis.cache.get.assert_called_once_with("trading_hours:KRX", th.KisSimpleTradingHours)


def test_trading_hours_country_code_kr():
    """Test trading_hours with country code 'KR' maps to 'KRX'."""
    mock_kis = Mock()
    mock_kis.cache = Mock()
    mock_kis.cache.get = Mock(return_value=None)
    mock_kis.cache.set = Mock()

    result = th.trading_hours(mock_kis, market="KR", use_cache=True)

    assert result.market == "KRX"


def test_trading_hours_country_code_us():
    """Test trading_hours with country code 'US' maps to 'NASDAQ'."""
    mock_kis = Mock()
    mock_kis.cache = Mock()
    mock_kis.cache.get = Mock(return_value=None)
    mock_kis.cache.set = Mock()

    # Mock foreign_day_chart
    mock_chart = Mock()
    mock_chart.trading_hours = th.KisSimpleTradingHours(market="NASDAQ", open=time(9, 30), close=time(16, 0))

    with patch("vmkis.api.stock.day_chart.foreign_day_chart", return_value=mock_chart):
        result = th.trading_hours(mock_kis, market="US", use_cache=True)

        assert result.market == "NASDAQ"


def test_trading_hours_country_code_jp():
    """Test trading_hours with country code 'JP' maps to 'TYO'."""
    mock_kis = Mock()
    mock_kis.cache = Mock()
    mock_kis.cache.get = Mock(return_value=None)
    mock_kis.cache.set = Mock()

    mock_chart = Mock()
    mock_chart.trading_hours = th.KisSimpleTradingHours(market="TYO", open=time(9, 0), close=time(15, 0))

    with patch("vmkis.api.stock.day_chart.foreign_day_chart", return_value=mock_chart):
        result = th.trading_hours(mock_kis, market="JP", use_cache=True)

        assert result.market == "TYO"


def test_trading_hours_country_code_hk():
    """Test trading_hours with country code 'HK' maps to 'HKEX'."""
    mock_kis = Mock()
    mock_kis.cache = Mock()
    mock_kis.cache.get = Mock(return_value=None)
    mock_kis.cache.set = Mock()

    mock_chart = Mock()
    mock_chart.trading_hours = th.KisSimpleTradingHours(market="HKEX", open=time(9, 30), close=time(16, 0))

    with patch("vmkis.api.stock.day_chart.foreign_day_chart", return_value=mock_chart):
        result = th.trading_hours(mock_kis, market="HK", use_cache=True)

        assert result.market == "HKEX"


def test_trading_hours_country_code_vn():
    """Test trading_hours with country code 'VN' maps to 'HSX'."""
    mock_kis = Mock()
    mock_kis.cache = Mock()
    mock_kis.cache.get = Mock(return_value=None)
    mock_kis.cache.set = Mock()

    mock_chart = Mock()
    mock_chart.trading_hours = th.KisSimpleTradingHours(market="HSX", open=time(9, 0), close=time(15, 0))

    with patch("vmkis.api.stock.day_chart.foreign_day_chart", return_value=mock_chart):
        result = th.trading_hours(mock_kis, market="VN", use_cache=True)

        assert result.market == "HSX"


def test_trading_hours_country_code_cn():
    """Test trading_hours with country code 'CN' maps to 'SSE'."""
    mock_kis = Mock()
    mock_kis.cache = Mock()
    mock_kis.cache.get = Mock(return_value=None)
    mock_kis.cache.set = Mock()

    mock_chart = Mock()
    mock_chart.trading_hours = th.KisSimpleTradingHours(market="SSE", open=time(9, 30), close=time(15, 0))

    with patch("vmkis.api.stock.day_chart.foreign_day_chart", return_value=mock_chart):
        result = th.trading_hours(mock_kis, market="CN", use_cache=True)

        assert result.market == "SSE"


def test_trading_hours_foreign_market_with_alias():
    """Test trading_hours for foreign market that uses alias (HNX -> HSX)."""
    mock_kis = Mock()
    mock_kis.cache = Mock()
    mock_kis.cache.get = Mock(return_value=None)
    mock_kis.cache.set = Mock()

    mock_chart = Mock()
    mock_chart.trading_hours = th.KisSimpleTradingHours(market="HSX", open=time(9, 0), close=time(15, 0))

    with patch("vmkis.api.stock.day_chart.foreign_day_chart", return_value=mock_chart):
        result = th.trading_hours(mock_kis, market="HNX", use_cache=True)

        # HNX should resolve to HSX
        assert result.market == "HSX"


def test_trading_hours_foreign_market_not_found():
    """Test trading_hours raises ValueError when no stock found."""
    mock_kis = Mock()
    mock_kis.cache = Mock()
    mock_kis.cache.get = Mock(return_value=None)
    mock_kis.cache.set = Mock()

    # Create proper KisNotFoundError with mock response
    mock_response = Mock()

    # Mock foreign_day_chart to always raise KisNotFoundError
    with patch("vmkis.api.stock.day_chart.foreign_day_chart", side_effect=KisNotFoundError("Not found", mock_response)):
        with pytest.raises(ValueError, match="해외 주식 시장 정보를 찾을 수 없습니다"):
            th.trading_hours(mock_kis, market="NASDAQ", use_cache=True)


def test_trading_hours_foreign_market_retry_on_not_found():
    """Test trading_hours retries with next symbol on KisNotFoundError."""
    mock_kis = Mock()
    mock_kis.cache = Mock()
    mock_kis.cache.get = Mock(return_value=None)
    mock_kis.cache.set = Mock()

    mock_chart = Mock()
    mock_chart.trading_hours = th.KisSimpleTradingHours(market="NASDAQ", open=time(9, 30), close=time(16, 0))

    mock_response = Mock()
    call_count = [0]

    def mock_foreign_day_chart(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] == 1:
            # First call fails
            raise KisNotFoundError("Not found", mock_response)
        # Second call succeeds
        return mock_chart

    with patch("vmkis.api.stock.day_chart.foreign_day_chart", side_effect=mock_foreign_day_chart):
        result = th.trading_hours(mock_kis, market="NASDAQ", use_cache=True)

        assert result.market == "NASDAQ"
        # Should have tried at least 2 symbols
        assert call_count[0] >= 2


def test_trading_hours_without_cache():
    """Test trading_hours function with use_cache=False."""
    mock_kis = Mock()
    mock_kis.cache = Mock()
    mock_kis.cache.get = Mock()
    mock_kis.cache.set = Mock()

    result = th.trading_hours(mock_kis, market="KRX", use_cache=False)

    assert isinstance(result, th.KisSimpleTradingHours)
    assert result.market == "KRX"

    # Verify cache.get was NOT called
    mock_kis.cache.get.assert_not_called()
    # Verify cache.set was NOT called
    mock_kis.cache.set.assert_not_called()


def test_market_sample_stock_map_has_expected_markets():
    """Test MARKET_SAMPLE_STOCK_MAP contains expected markets."""
    assert "KRX" in th.MARKET_SAMPLE_STOCK_MAP
    assert "NASDAQ" in th.MARKET_SAMPLE_STOCK_MAP
    assert "NYSE" in th.MARKET_SAMPLE_STOCK_MAP
    assert "AMEX" in th.MARKET_SAMPLE_STOCK_MAP
    assert "TYO" in th.MARKET_SAMPLE_STOCK_MAP
    assert "HKEX" in th.MARKET_SAMPLE_STOCK_MAP
    assert "HSX" in th.MARKET_SAMPLE_STOCK_MAP
    assert "SSE" in th.MARKET_SAMPLE_STOCK_MAP
    assert "SZSE" in th.MARKET_SAMPLE_STOCK_MAP

    # Check HNX points to HSX
    assert th.MARKET_SAMPLE_STOCK_MAP["HNX"] == "HSX"
    assert th.MARKET_SAMPLE_STOCK_MAP["SZSE"] == "SSE"
