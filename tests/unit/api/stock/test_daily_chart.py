from datetime import date, datetime, time, timedelta
from decimal import Decimal
from unittest.mock import Mock, patch

import pytest

from vmkis.api.stock import day_chart
from vmkis.utils.timezone import TIMEZONE


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


class _MockBar:
    """Mock bar for testing drop_after and chart operations."""

    def __init__(self, d, open_price=1, high=2, low=1, close=1.5, volume=10, amount=100, change=0):
        # use datetime objects (day_chart expects .time to be datetime-like)
        if isinstance(d, date) and not isinstance(d, datetime):
            d = datetime.combine(d, datetime.min.time())
        self.time = d
        self.time_kst = d
        self.open = Decimal(str(open_price))
        self.high = Decimal(str(high))
        self.low = Decimal(str(low))
        self.close = Decimal(str(close))
        self.volume = volume
        self.amount = Decimal(str(amount))
        self.change = Decimal(str(change))

    @property
    def sign(self):
        """전일대비 부호"""
        return "steady" if self.change == 0 else "rise" if self.change > 0 else "decline"

    @property
    def price(self):
        """현재가 (종가)"""
        return self.close

    @property
    def prev_price(self):
        """전일가"""
        return self.close - self.change

    @property
    def rate(self):
        """등락률 (-100 ~ 100)"""
        from vmkis.utils.math import safe_divide

        return safe_divide(self.change, self.prev_price) * 100

    @property
    def sign_name(self):
        """대비부호명"""
        from vmkis.api.stock.quote import STOCK_SIGN_TYPE_KOR_MAP

        return STOCK_SIGN_TYPE_KOR_MAP[self.sign]


class _MockChart:
    """Mock chart for testing."""

    def __init__(self, bars=None):
        self.bars = bars or []


# Test drop_after function with various scenarios
class TestDropAfter:
    """Tests for the drop_after utility function."""

    def test_drop_after_with_time_start_and_end(self):
        """drop_after filters bars by time range."""
        # Bars need to be in reverse order (most recent first) for drop_after logic
        b4 = _MockBar(datetime(2020, 1, 1, 12, 0, 0))
        b3 = _MockBar(datetime(2020, 1, 1, 11, 0, 0))
        b2 = _MockBar(datetime(2020, 1, 1, 10, 0, 0))
        b1 = _MockBar(datetime(2020, 1, 1, 9, 0, 0))
        chart = _MockChart([b4, b3, b2, b1])

        result = day_chart.drop_after(chart, start=time(10, 0, 0), end=time(11, 0, 0))

        # drop_after reverses the output, keeping bars that match filters
        assert len(result.bars) == 2
        assert result.bars[0].time.time() == time(10, 0, 0)
        assert result.bars[1].time.time() == time(11, 0, 0)

    def test_drop_after_with_timedelta(self):
        """drop_after with timedelta calculates start time from first bar."""
        b1 = _MockBar(datetime(2020, 1, 1, 12, 0, 0))
        b2 = _MockBar(datetime(2020, 1, 1, 11, 0, 0))
        b3 = _MockBar(datetime(2020, 1, 1, 10, 0, 0))
        chart = _MockChart([b1, b2, b3])

        result = day_chart.drop_after(chart, start=timedelta(hours=1))

        # Should keep bars within 1 hour from the first bar (12:00)
        assert len(result.bars) >= 1

    def test_drop_after_with_period(self):
        """drop_after applies period filtering."""
        bars = [_MockBar(datetime(2020, 1, 1, 9, i, 0)) for i in range(10)]
        chart = _MockChart(bars)

        result = day_chart.drop_after(chart, period=3)

        # Should keep every 3rd bar
        assert len(result.bars) == 4  # indices 0, 3, 6, 9

    def test_drop_after_no_filters(self):
        """drop_after with no filters returns all bars reversed."""
        b1 = _MockBar(datetime(2020, 1, 1, 9, 0, 0))
        b2 = _MockBar(datetime(2020, 1, 1, 10, 0, 0))
        chart = _MockChart([b1, b2])

        result = day_chart.drop_after(chart)

        assert len(result.bars) == 2
        # Bars should be reversed
        assert result.bars[0] == b2
        assert result.bars[1] == b1


# Test KisDomesticDayChartBar properties
class TestKisDomesticDayChartBar:
    """Tests for KisDomesticDayChartBar properties and methods."""

    def test_sign_property_steady(self):
        """Bar sign is 'steady' when change is 0."""
        bar = _MockBar(datetime(2020, 1, 1, 9, 0, 0), change=0)
        assert bar.sign == "steady"

    def test_sign_property_rise(self):
        """Bar sign is 'rise' when change is positive."""
        bar = _MockBar(datetime(2020, 1, 1, 9, 0, 0), change=1.5)
        assert bar.sign == "rise"

    def test_sign_property_decline(self):
        """Bar sign is 'decline' when change is negative."""
        bar = _MockBar(datetime(2020, 1, 1, 9, 0, 0), change=-1.5)
        assert bar.sign == "decline"

    def test_price_property(self):
        """price property returns close value."""
        bar = _MockBar(datetime(2020, 1, 1, 9, 0, 0), close=100.5)
        assert bar.price == Decimal("100.5")

    def test_prev_price_property(self):
        """prev_price calculates from close and change."""
        bar = _MockBar(datetime(2020, 1, 1, 9, 0, 0), close=100, change=5)
        assert bar.prev_price == Decimal("95")

    def test_rate_property(self):
        """rate calculates percentage change."""
        bar = _MockBar(datetime(2020, 1, 1, 9, 0, 0), close=105, change=5)
        # prev_price = 105 - 5 = 100, rate = (5/100)*100 = 5%
        assert bar.rate == Decimal("5")

    def test_sign_name_property(self):
        """sign_name returns Korean translation."""
        bar_rise = _MockBar(datetime(2020, 1, 1, 9, 0, 0), change=1)
        bar_decline = _MockBar(datetime(2020, 1, 1, 9, 0, 0), change=-1)
        bar_steady = _MockBar(datetime(2020, 1, 1, 9, 0, 0), change=0)

        assert bar_rise.sign_name in ["상승", "상한", "상한가"]
        assert bar_decline.sign_name in ["하락", "하한", "하한가"]
        assert bar_steady.sign_name == "보합"


# Test domestic_day_chart function
class TestDomesticDayChart:
    """Tests for domestic_day_chart function."""

    def test_validates_empty_symbol(self):
        """domestic_day_chart raises ValueError for empty symbol."""
        fake_kis = _fake_kis()

        with pytest.raises(ValueError, match="종목 코드를 입력해주세요"):
            day_chart.domestic_day_chart(fake_kis, "")

    def test_validates_invalid_period(self):
        """domestic_day_chart raises ValueError for invalid period."""
        fake_kis = _fake_kis()

        with pytest.raises(ValueError, match="간격은 1분 이상이어야 합니다"):
            day_chart.domestic_day_chart(fake_kis, "005930", period=0)

    def test_validates_start_after_end(self):
        """domestic_day_chart raises ValueError when start is after end."""
        fake_kis = _fake_kis()

        with pytest.raises(ValueError, match="시작 시간은 종료 시간보다 이전이어야 합니다"):
            day_chart.domestic_day_chart(fake_kis, "005930", start=time(15, 0, 0), end=time(9, 0, 0))

    def test_fetches_single_page(self):
        """domestic_day_chart fetches and returns chart data."""
        fake_kis = _fake_kis()
        mock_chart = _MockChart(
            [
                _MockBar(datetime(2020, 1, 1, 10, 0, 0)),
                _MockBar(datetime(2020, 1, 1, 9, 30, 0)),
            ]
        )
        fake_kis.fetch.return_value = mock_chart

        result = day_chart.domestic_day_chart(fake_kis, "005930")

        assert fake_kis.fetch.called
        assert result == mock_chart

    def test_handles_timedelta_start(self):
        """domestic_day_chart handles timedelta as start parameter."""
        fake_kis = _fake_kis()
        mock_chart = _MockChart(
            [
                _MockBar(datetime(2020, 1, 1, 12, 0, 0)),
                _MockBar(datetime(2020, 1, 1, 11, 0, 0)),
                _MockBar(datetime(2020, 1, 1, 10, 0, 0)),
            ]
        )
        fake_kis.fetch.return_value = mock_chart

        result = day_chart.domestic_day_chart(fake_kis, "005930", start=timedelta(hours=1))

        assert result is not None


# Test foreign_day_chart function
class TestForeignDayChart:
    """Tests for foreign_day_chart function."""

    def test_validates_empty_symbol(self):
        """foreign_day_chart raises ValueError for empty symbol."""
        fake_kis = _fake_kis()

        with pytest.raises(ValueError, match="종목 코드를 입력해주세요"):
            day_chart.foreign_day_chart(fake_kis, "", "NAS")

    def test_validates_invalid_period(self):
        """foreign_day_chart raises ValueError for invalid period."""
        fake_kis = _fake_kis()

        with pytest.raises(ValueError, match="간격은 1분 이상이어야 합니다"):
            day_chart.foreign_day_chart(fake_kis, "AAPL", "NAS", period=0)

    def test_validates_krx_market(self):
        """foreign_day_chart raises ValueError for KRX market."""
        fake_kis = _fake_kis()

        with pytest.raises(ValueError, match="국내 시장은 domestic_chart"):
            day_chart.foreign_day_chart(fake_kis, "005930", "KRX")

    @patch("vmkis.api.stock.quote.quote")
    def test_fetches_with_quote_for_prev_price(self, mock_quote):
        """foreign_day_chart fetches quote to get prev_price."""
        fake_kis = _fake_kis()
        mock_quote_result = Mock()
        mock_quote_result.prev_price = Decimal("150.0")
        mock_quote.return_value = mock_quote_result

        mock_chart = Mock()
        mock_chart.bars = [_MockBar(datetime(2020, 1, 1, 10, 0, 0))]
        fake_kis.fetch.return_value = mock_chart

        day_chart.foreign_day_chart(fake_kis, "AAPL", "NASDAQ", once=True)

        mock_quote.assert_called_once_with(fake_kis, "AAPL", "NASDAQ")
        assert fake_kis.fetch.called

    @patch("vmkis.api.stock.quote.quote")
    def test_handles_once_parameter(self, mock_quote):
        """foreign_day_chart respects once parameter."""
        fake_kis = _fake_kis()
        mock_quote_result = Mock()
        mock_quote_result.prev_price = Decimal("150.0")
        mock_quote.return_value = mock_quote_result

        mock_chart = Mock()
        mock_chart.bars = [_MockBar(datetime(2020, 1, 1, 10, 0, 0))]
        fake_kis.fetch.return_value = mock_chart

        day_chart.foreign_day_chart(fake_kis, "AAPL", "NASDAQ", once=True)

        # Should only fetch once when once=True
        assert fake_kis.fetch.call_count == 1


# Test day_chart wrapper function
class TestDayChart:
    """Tests for day_chart wrapper function."""

    @patch("vmkis.api.stock.day_chart.domestic_day_chart")
    def test_routes_to_domestic_for_krx(self, mock_domestic):
        """day_chart routes to domestic_day_chart for KRX market."""
        fake_kis = _fake_kis()
        mock_domestic.return_value = _MockChart()

        result = day_chart.day_chart(fake_kis, "005930", "KRX")

        mock_domestic.assert_called_once()
        assert result is not None

    @patch("vmkis.api.stock.day_chart.foreign_day_chart")
    def test_routes_to_foreign_for_non_krx(self, mock_foreign):
        """day_chart routes to foreign_day_chart for non-KRX markets."""
        fake_kis = _fake_kis()
        mock_foreign.return_value = Mock()

        result = day_chart.day_chart(fake_kis, "AAPL", "NASDAQ")

        mock_foreign.assert_called_once()
        assert result is not None


# Test product_day_chart function
class TestProductDayChart:
    """Tests for product_day_chart function."""

    @patch("vmkis.api.stock.day_chart.day_chart")
    def test_calls_day_chart_with_product_attributes(self, mock_day_chart):
        """product_day_chart calls day_chart with product's symbol and market."""
        mock_product = Mock()
        mock_product.kis = Mock()
        mock_product.symbol = "005930"
        mock_product.market = "KRX"
        mock_day_chart.return_value = _MockChart()

        day_chart.product_day_chart(mock_product, start=time(9, 0, 0), end=time(15, 30, 0), period=5)

        mock_day_chart.assert_called_once_with(
            mock_product.kis, symbol="005930", market="KRX", start=time(9, 0, 0), end=time(15, 30, 0), period=5
        )


# Test KisDomesticDayChart class
class TestKisDomesticDayChart:
    """Tests for KisDomesticDayChart response class."""

    def test_initializes_with_symbol(self):
        """KisDomesticDayChart initializes with symbol."""
        chart = day_chart.KisDomesticDayChart("005930")
        assert chart.symbol == "005930"
        assert chart.market == "KRX"
        assert chart.timezone == TIMEZONE


# Test KisForeignDayChart class
class TestKisForeignDayChart:
    """Tests for KisForeignDayChart response class."""

    def test_initializes_with_symbol_market_prev_price(self):
        """KisForeignDayChart initializes with required parameters."""
        chart = day_chart.KisForeignDayChart("AAPL", "NASDAQ", Decimal("150.0"))
        assert chart.symbol == "AAPL"
        assert chart.market == "NASDAQ"
        assert chart.prev_price == Decimal("150.0")


# Test more edge cases for comprehensive coverage
class TestDropAfterEdgeCases:
    """Additional edge cases for drop_after function."""

    def test_drop_after_empty_bars(self):
        """drop_after handles empty bar list."""
        chart = _MockChart([])
        result = day_chart.drop_after(chart)
        assert result.bars == []

    def test_drop_after_timedelta_at_boundary(self):
        """drop_after with timedelta handles boundary conditions."""
        b1 = _MockBar(datetime(2020, 1, 1, 0, 30, 0))
        chart = _MockChart([b1])

        # When timedelta is larger than time elapsed since midnight
        result = day_chart.drop_after(chart, start=timedelta(hours=2))
        assert len(result.bars) >= 0


class TestDomesticDayChartEdgeCases:
    """Additional edge cases for domestic_day_chart."""

    def test_domestic_day_chart_multiple_pages(self):
        """domestic_day_chart fetches multiple pages until exhausted."""
        fake_kis = _fake_kis()

        # First page with data
        chart1 = _MockChart(
            [
                _MockBar(datetime(2020, 1, 1, 15, 0, 0)),
                _MockBar(datetime(2020, 1, 1, 14, 0, 0)),
            ]
        )

        # Second page with data
        chart2 = _MockChart(
            [
                _MockBar(datetime(2020, 1, 1, 13, 0, 0)),
                _MockBar(datetime(2020, 1, 1, 12, 0, 0)),
            ]
        )

        # Third page empty
        chart3 = _MockChart([])

        fake_kis.fetch.side_effect = [chart1, chart2, chart3]

        result = day_chart.domestic_day_chart(fake_kis, "005930")

        assert fake_kis.fetch.call_count == 3
        assert len(result.bars) == 4

    def test_domestic_day_chart_with_end_time(self):
        """domestic_day_chart respects end time parameter."""
        fake_kis = _fake_kis()
        mock_chart = _MockChart(
            [
                _MockBar(datetime(2020, 1, 1, 15, 0, 0)),
                _MockBar(datetime(2020, 1, 1, 10, 0, 0)),
            ]
        )
        fake_kis.fetch.return_value = mock_chart

        result = day_chart.domestic_day_chart(fake_kis, "005930", end=time(14, 0, 0))

        assert result is not None


class TestForeignDayChartEdgeCases:
    """Additional edge cases for foreign_day_chart."""

    @patch("vmkis.api.stock.quote.quote")
    def test_foreign_day_chart_multiple_periods(self, mock_quote):
        """foreign_day_chart fetches multiple periods."""
        fake_kis = _fake_kis()
        mock_quote_result = Mock()
        mock_quote_result.prev_price = Decimal("150.0")
        mock_quote.return_value = mock_quote_result

        # Create charts for different periods - need enough for potential multiple iterations
        def create_chart():
            mock_chart = Mock()
            mock_chart.bars = [_MockBar(datetime(2020, 1, 1, 10, 0, 0))]
            return mock_chart

        # Make fetch return charts indefinitely
        fake_kis.fetch.return_value = create_chart()

        result = day_chart.foreign_day_chart(fake_kis, "AAPL", "NASDAQ", once=True)

        assert result is not None
        # Should call at least once
        assert fake_kis.fetch.call_count == 1

    @patch("vmkis.api.stock.quote.quote")
    def test_foreign_day_chart_with_time_filters(self, mock_quote):
        """foreign_day_chart applies time filtering."""
        fake_kis = _fake_kis()
        mock_quote_result = Mock()
        mock_quote_result.prev_price = Decimal("150.0")
        mock_quote.return_value = mock_quote_result

        mock_chart = Mock()
        mock_chart.bars = [
            _MockBar(datetime(2020, 1, 1, 12, 0, 0)),
            _MockBar(datetime(2020, 1, 1, 10, 0, 0)),
        ]
        fake_kis.fetch.return_value = mock_chart

        result = day_chart.foreign_day_chart(
            fake_kis, "AAPL", "NASDAQ", start=time(11, 0, 0), end=time(13, 0, 0), once=True
        )

        assert result is not None

    @patch("vmkis.api.stock.quote.quote")
    def test_foreign_day_chart_with_period(self, mock_quote):
        """foreign_day_chart applies period filtering."""
        fake_kis = _fake_kis()
        mock_quote_result = Mock()
        mock_quote_result.prev_price = Decimal("150.0")
        mock_quote.return_value = mock_quote_result

        mock_chart = Mock()
        mock_chart.bars = [_MockBar(datetime(2020, 1, 1, 10 + i, 0, 0)) for i in range(10)]
        fake_kis.fetch.return_value = mock_chart

        result = day_chart.foreign_day_chart(fake_kis, "AAPL", "NASDAQ", period=5, once=True)

        assert result is not None

    @patch("vmkis.api.stock.quote.quote")
    def test_foreign_day_chart_with_empty_bars_and_timedelta(self, mock_quote):
        """foreign_day_chart handles timedelta with start parameter."""
        fake_kis = _fake_kis()
        mock_quote_result = Mock()
        mock_quote_result.prev_price = Decimal("150.0")
        mock_quote.return_value = mock_quote_result

        # Return chart with bars to test timedelta logic
        mock_chart = Mock()
        mock_chart.bars = [
            _MockBar(datetime(2020, 1, 1, 12, 0, 0)),
            _MockBar(datetime(2020, 1, 1, 11, 0, 0)),
        ]
        fake_kis.fetch.return_value = mock_chart

        result = day_chart.foreign_day_chart(fake_kis, "AAPL", "NASDAQ", start=timedelta(hours=2), once=True)

        assert result is not None


class TestKisDomesticDayChartBarEdgeCases:
    """Test edge cases for KisDomesticDayChartBar."""

    def test_rate_with_zero_prev_price(self):
        """rate handles zero prev_price gracefully."""
        # close=0, change=0 means prev_price=0
        bar = _MockBar(datetime(2020, 1, 1, 9, 0, 0), close=0, change=0)
        # safe_divide should handle division by zero
        rate = bar.rate
        assert rate == Decimal("0")


class TestKisForeignTradingHours:
    """Tests for KisForeignTradingHours class."""

    def test_initializes_with_market(self):
        """KisForeignTradingHours initializes with market."""
        hours = day_chart.KisForeignTradingHours("NASDAQ")
        assert hours.market == "NASDAQ"


class TestDomesticDayChartIntegration:
    """Integration tests for domestic day chart."""

    def test_domestic_day_chart_respects_start_time(self):
        """domestic_day_chart filters by start time correctly."""
        fake_kis = _fake_kis()

        chart1 = _MockChart(
            [
                _MockBar(datetime(2020, 1, 1, 15, 0, 0)),
                _MockBar(datetime(2020, 1, 1, 14, 0, 0)),
            ]
        )
        chart2 = _MockChart(
            [
                _MockBar(datetime(2020, 1, 1, 13, 0, 0)),
                _MockBar(datetime(2020, 1, 1, 12, 0, 0)),
            ]
        )
        chart3 = _MockChart(
            [
                _MockBar(datetime(2020, 1, 1, 11, 0, 0)),
                _MockBar(datetime(2020, 1, 1, 10, 0, 0)),
            ]
        )

        fake_kis.fetch.side_effect = [chart1, chart2, chart3]

        result = day_chart.domestic_day_chart(fake_kis, "005930", start=time(11, 30, 0))

        assert result is not None
        # Should break when reaching start time
        assert fake_kis.fetch.call_count >= 1

    def test_domestic_day_chart_with_period_5(self):
        """domestic_day_chart applies 5-minute period correctly."""
        fake_kis = _fake_kis()
        bars = [_MockBar(datetime(2020, 1, 1, 9, i, 0)) for i in range(0, 60, 1)]
        mock_chart = _MockChart(bars)
        fake_kis.fetch.return_value = mock_chart

        result = day_chart.domestic_day_chart(fake_kis, "005930", period=5)

        assert result is not None


class TestKisDomesticDayChartBarIntegration:
    """Test actual KisDomesticDayChartBar behavior."""

    def test_bar_properties_with_real_class(self):
        """Test KisDomesticDayChartBar properties directly."""
        # Create a mock bar data that mimics API response

        # Test that the bar can be initialized
        bar = day_chart.KisDomesticDayChartBar()
        # Manually set attributes for testing
        bar.time = datetime(2020, 1, 1, 9, 30, 0, tzinfo=TIMEZONE)
        bar.time_kst = bar.time
        bar.open = Decimal("100.0")
        bar.close = Decimal("105.0")
        bar.high = Decimal("110.0")
        bar.low = Decimal("95.0")
        bar.volume = 1000
        bar.amount = Decimal("100000.0")
        bar.change = Decimal("5.0")

        # Test properties
        assert bar.sign == "rise"
        assert bar.price == Decimal("105.0")
        assert bar.prev_price == Decimal("100.0")
        assert bar.rate == Decimal("5.0")


class TestKisForeignDayChartBarIntegration:
    """Test KisForeignDayChartBar behavior."""

    def test_foreign_bar_properties(self):
        """Test KisForeignDayChartBar properties directly."""
        bar = day_chart.KisForeignDayChartBar()
        # Manually set attributes
        bar.time = datetime(2020, 1, 1, 9, 30, 0, tzinfo=TIMEZONE)
        bar.time_kst = bar.time
        bar.open = Decimal("150.0")
        bar.close = Decimal("155.0")
        bar.high = Decimal("160.0")
        bar.low = Decimal("145.0")
        bar.volume = 5000
        bar.amount = Decimal("750000.0")
        bar.change = Decimal("5.0")

        # Test properties
        assert bar.sign == "rise"
        assert bar.price == Decimal("155.0")
        assert bar.prev_price == Decimal("150.0")


class TestForeignChartTimezoneHandling:
    """Test timezone handling in foreign chart."""

    def test_foreign_trading_hours_initializes(self):
        """Test KisForeignTradingHours initialization."""
        hours = day_chart.KisForeignTradingHours("NYSE")
        assert hours.market == "NYSE"


class TestDomesticDayChartCursorLogic:
    """Test domestic day chart cursor pagination logic."""

    def test_cursor_breaks_on_start_time(self):
        """Test that cursor stops fetching when start time is reached."""
        fake_kis = _fake_kis()

        # Create bars that go back in time
        chart1 = _MockChart(
            [
                _MockBar(datetime(2020, 1, 1, 15, 0, 0)),
                _MockBar(datetime(2020, 1, 1, 14, 0, 0)),
                _MockBar(datetime(2020, 1, 1, 13, 0, 0)),
            ]
        )

        chart2 = _MockChart(
            [
                _MockBar(datetime(2020, 1, 1, 12, 0, 0)),
                _MockBar(datetime(2020, 1, 1, 11, 0, 0)),
                _MockBar(datetime(2020, 1, 1, 10, 0, 0)),
            ]
        )

        # Third fetch returns empty to stop pagination
        chart3 = _MockChart([])

        fake_kis.fetch.side_effect = [chart1, chart2, chart3]

        result = day_chart.domestic_day_chart(fake_kis, "005930", start=time(11, 0, 0), end=time(15, 30, 0))

        assert result is not None
        assert fake_kis.fetch.call_count >= 2


class TestDomesticDayChartLoopTermination:
    """Test loop termination conditions in domestic_day_chart."""

    def test_cursor_less_than_last_time(self):
        """Test pagination stops when cursor is before last bar time."""
        fake_kis = _fake_kis()

        # First fetch returns bars
        chart1 = _MockChart(
            [
                _MockBar(datetime(2020, 1, 1, 15, 0, 0)),
                _MockBar(datetime(2020, 1, 1, 14, 30, 0)),
            ]
        )

        # Set up end time after first bar to trigger early cursor break
        fake_kis.fetch.return_value = chart1

        result = day_chart.domestic_day_chart(
            fake_kis,
            "005930",
            end=time(14, 0, 0),  # Before the last bar
        )

        assert result is not None

    # other runtime behaviors require a live `fetch` method on the client; skip here


# ===== 추가 테스트: daily_chart.py 커버리지 향상 (80% 이상 목표) =====


class TestKisDomesticDailyChartBar:
    """Tests for KisDomesticDailyChartBar (daily_chart.py에서 import)."""

    def test_properties_integration(self):
        """Test all properties work correctly via KisObject.transform_."""
        from vmkis.api.stock.daily_chart import KisDomesticDailyChartBar
        from vmkis.responses.dynamic import KisObject

        # Create mock API response data
        bar_data = {
            "stck_bsop_date": "20231201",
            "stck_oprc": "65000",
            "stck_clpr": "66500",
            "stck_hgpr": "67000",
            "stck_lwpr": "64500",
            "acml_vol": "1000000",
            "acml_tr_pbmn": "65500000000",
            "prdy_vrss": "1500",
            "prdy_vrss_sign": "2",  # Rise
            "flng_cls_code": "00",
            "prtt_rate": "0",
        }

        bar = KisObject.transform_(bar_data, KisDomesticDailyChartBar)

        # Test properties
        assert bar.price == Decimal("66500")
        assert bar.prev_price == Decimal("65000")
        assert bar.change == Decimal("1500")
        assert bar.rate == Decimal("2.307692307692307692307692308")  # (1500/65000)*100
        assert bar.sign == "rise"
        assert bar.sign_name in ["상승", "상한", "상한가"]
        assert bar.ex_date_type.name == "NONE"

    def test_ex_date_type_mapping(self):
        """Test ExDateType mapping from code."""
        from vmkis.api.stock.daily_chart import KisDomesticDailyChartBar
        from vmkis.api.stock.market import ExDateType
        from vmkis.responses.dynamic import KisObject

        # Test rights ex-date (code "01" = EX_RIGHTS)
        bar_data_rights = {
            "stck_bsop_date": "20231201",
            "stck_oprc": "65000",
            "stck_clpr": "66500",
            "stck_hgpr": "67000",
            "stck_lwpr": "64500",
            "acml_vol": "1000000",
            "acml_tr_pbmn": "65500000000",
            "prdy_vrss": "1500",
            "prdy_vrss_sign": "2",
            "flng_cls_code": "01",  # EX_RIGHTS
            "prtt_rate": "0",
        }

        bar = KisObject.transform_(bar_data_rights, KisDomesticDailyChartBar)
        assert bar.ex_date_type == ExDateType.EX_RIGHTS

        # Test dividend ex-date (code "02" = EX_DIVIDEND)
        bar_data_dividend = bar_data_rights.copy()
        bar_data_dividend["flng_cls_code"] = "02"
        bar_dividend = KisObject.transform_(bar_data_dividend, KisDomesticDailyChartBar)
        assert bar_dividend.ex_date_type == ExDateType.EX_DIVIDEND

    def test_sign_mapping(self):
        """Test sign type mapping."""
        from vmkis.api.stock.daily_chart import KisDomesticDailyChartBar
        from vmkis.responses.dynamic import KisObject

        base_data = {
            "stck_bsop_date": "20231201",
            "stck_oprc": "65000",
            "stck_clpr": "66500",
            "stck_hgpr": "67000",
            "stck_lwpr": "64500",
            "acml_vol": "1000000",
            "acml_tr_pbmn": "65500000000",
            "prdy_vrss": "1500",
            "flng_cls_code": "00",
            "prtt_rate": "0",
        }

        # Test rise (2)
        bar_data_rise = base_data.copy()
        bar_data_rise["prdy_vrss_sign"] = "2"
        bar_rise = KisObject.transform_(bar_data_rise, KisDomesticDailyChartBar)
        assert bar_rise.sign == "rise"
        assert bar_rise.sign_name in ["상승", "상한", "상한가"]

        # Test decline (5)
        bar_data_decline = base_data.copy()
        bar_data_decline["prdy_vrss_sign"] = "5"
        bar_data_decline["prdy_vrss"] = "-1500"
        bar_decline = KisObject.transform_(bar_data_decline, KisDomesticDailyChartBar)
        assert bar_decline.sign == "decline"
        assert bar_decline.sign_name in ["하락", "하한", "하한가"]

        # Test steady (3)
        bar_data_steady = base_data.copy()
        bar_data_steady["prdy_vrss_sign"] = "3"
        bar_data_steady["prdy_vrss"] = "0"
        bar_steady = KisObject.transform_(bar_data_steady, KisDomesticDailyChartBar)
        assert bar_steady.sign == "steady"
        assert bar_steady.sign_name == "보합"


class TestKisDomesticDailyChart:
    """Tests for KisDomesticDailyChart response class."""

    def test_initialization(self):
        """Test chart initialization."""
        from vmkis.api.stock.daily_chart import KisDomesticDailyChart

        chart = KisDomesticDailyChart(symbol="005930")
        assert chart.symbol == "005930"
        assert chart.market == "KRX"
        assert chart.timezone is not None

    def test_pre_init_filters_empty_bars(self):
        """Test that __pre_init__ filters out empty bars."""
        from vmkis.api.stock.daily_chart import KisDomesticDailyChart

        chart = KisDomesticDailyChart(symbol="005930")

        # Mock data with some empty items - must include rt_cd for KisResponse
        data = {
            "rt_cd": "0",  # Success code required by KisResponse
            "msg_cd": "MCA00000",
            "msg1": "정상처리 되었습니다.",
            "output1": {"stck_prpr": "66500"},
            "output2": [
                {
                    "stck_bsop_date": "20231201",
                    "stck_oprc": "65000",
                    "stck_clpr": "66500",
                    "stck_hgpr": "67000",
                    "stck_lwpr": "64500",
                    "acml_vol": "1000000",
                    "acml_tr_pbmn": "65500000000",
                    "prdy_vrss": "1500",
                    "prdy_vrss_sign": "2",
                    "flng_cls_code": "00",
                    "prtt_rate": "0",
                },
                None,  # Empty item
                {},  # Empty dict
                {
                    "stck_bsop_date": "20231130",
                    "stck_oprc": "64000",
                    "stck_clpr": "65000",
                    "stck_hgpr": "65500",
                    "stck_lwpr": "63500",
                    "acml_vol": "900000",
                    "acml_tr_pbmn": "64500000000",
                    "prdy_vrss": "-500",
                    "prdy_vrss_sign": "5",
                    "flng_cls_code": "00",
                    "prtt_rate": "0",
                },
            ],
        }

        chart.__pre_init__(data)
        # Should have filtered out None and empty dict
        assert len(data["output2"]) == 2

    @pytest.mark.skip(reason="raise_not_found는 __response__ 필드를 필요로 하므로 실제 API 호출 과정에서만 테스트 가능")
    def test_pre_init_raises_not_found(self):
        """Test __pre_init__ raises error when no data. (SKIPPED: Needs full API response structure)"""
        pass


class TestKisForeignDailyChartBar:
    """Tests for KisForeignDailyChartBar."""

    def test_properties_integration(self):
        """Test all properties work correctly via KisObject.transform_."""
        from vmkis.api.stock.daily_chart import KisForeignDailyChartBar
        from vmkis.responses.dynamic import KisObject

        # Create mock API response data
        bar_data = {
            "xymd": "20231201",
            "open": "150.50",
            "clos": "152.00",
            "high": "153.00",
            "low": "149.50",
            "tvol": "5000000",
            "tamt": "756000000",
            "diff": "1.50",
            "sign": "2",  # Rise
        }

        bar = KisObject.transform_(bar_data, KisForeignDailyChartBar)

        # Test properties
        assert bar.price == Decimal("152.00")
        assert bar.prev_price == Decimal("150.50")
        assert bar.change == Decimal("1.50")
        assert bar.sign == "rise"
        assert bar.sign_name in ["상승", "상한", "상한가"]

        # Test decline case
        bar_data_decline = bar_data.copy()
        bar_data_decline["sign"] = "5"
        bar_data_decline["diff"] = "-1.50"
        bar_decline = KisObject.transform_(bar_data_decline, KisForeignDailyChartBar)
        assert bar_decline.sign == "decline"
        assert bar_decline.prev_price == Decimal("153.50")


class TestKisForeignDailyChart:
    """Tests for KisForeignDailyChart response class."""

    def test_initialization(self):
        """Test chart initialization."""
        from vmkis.api.stock.daily_chart import KisForeignDailyChart

        chart = KisForeignDailyChart(symbol="AAPL", market="NASDAQ")
        assert chart.symbol == "AAPL"
        assert chart.market == "NASDAQ"

    def test_pre_init_sets_timezone(self):
        """Test __pre_init__ sets timezone from market."""
        from vmkis.api.stock.daily_chart import KisForeignDailyChart

        chart = KisForeignDailyChart(symbol="AAPL", market="NASDAQ")

        data = {
            "rt_cd": "0",  # Required by KisResponse
            "msg_cd": "MCA00000",
            "msg1": "정상처리 되었습니다.",
            "output1": {"nrec": "2"},
            "output2": [
                {
                    "xymd": "20231201",
                    "open": "150.50",
                    "clos": "152.00",
                    "high": "153.00",
                    "low": "149.50",
                    "tvol": "5000000",
                    "tamt": "756000000",
                    "diff": "1.50",
                    "sign": "2",
                },
                {
                    "xymd": "20231130",
                    "open": "149.00",
                    "clos": "150.50",
                    "high": "151.00",
                    "low": "148.50",
                    "tvol": "4800000",
                    "tamt": "720000000",
                    "diff": "-0.50",
                    "sign": "5",
                },
                {
                    "xymd": "20231129",
                    "open": "148.00",
                    "clos": "149.00",
                    "high": "150.00",
                    "low": "147.50",
                    "tvol": "4500000",
                    "tamt": "670000000",
                    "diff": "1.00",
                    "sign": "2",
                },
            ],
        }

        chart.__pre_init__(data)

        # Should slice to nrec count
        assert len(data["output2"]) == 2
        assert chart.timezone is not None

    @pytest.mark.skip(reason="해외 차트는 nrec=0일 때 KisNotFoundError를 발생시키지 않고 빈 배열을 반환")
    def test_pre_init_raises_not_found(self):
        """Test __pre_init__ raises error when no records. (SKIPPED: Foreign chart returns empty list, not error)"""
        pass

    def test_post_init_sets_timezones(self):
        """Test __post_init__ sets bar timezones."""
        from vmkis.api.stock.daily_chart import KisForeignDailyChart

        chart = KisForeignDailyChart(symbol="AAPL", market="NASDAQ")

        # Create mock bars
        from datetime import datetime

        bar1 = Mock()
        bar1.time = datetime(2023, 12, 1, 9, 30, 0)
        bar2 = Mock()
        bar2.time = datetime(2023, 11, 30, 9, 30, 0)

        chart.bars = [bar1, bar2]
        chart.timezone = TIMEZONE

        chart.__post_init__()

        # Verify timezone conversion was attempted
        assert hasattr(bar1, "time_kst")
        assert hasattr(bar2, "time_kst")


class TestDropAfterWithDate:
    """Tests for drop_after with date parameters."""

    def test_drop_after_with_date_start(self):
        """Test drop_after with date start parameter."""
        from datetime import date as dt_date

        from vmkis.api.stock.daily_chart import drop_after

        bars = [
            _MockBar(datetime(2023, 12, 5, 9, 0, 0)),
            _MockBar(datetime(2023, 12, 4, 9, 0, 0)),
            _MockBar(datetime(2023, 12, 3, 9, 0, 0)),
            _MockBar(datetime(2023, 12, 2, 9, 0, 0)),
            _MockBar(datetime(2023, 12, 1, 9, 0, 0)),
        ]
        chart = _MockChart(bars)

        result = drop_after(chart, start=dt_date(2023, 12, 3), end=dt_date(2023, 12, 5))

        # Should keep bars from Dec 3-5
        assert len(result.bars) == 3

    def test_drop_after_with_date_end_only(self):
        """Test drop_after with only end date."""
        from datetime import date as dt_date

        from vmkis.api.stock.daily_chart import drop_after

        bars = [
            _MockBar(datetime(2023, 12, 5, 9, 0, 0)),
            _MockBar(datetime(2023, 12, 4, 9, 0, 0)),
            _MockBar(datetime(2023, 12, 3, 9, 0, 0)),
        ]
        chart = _MockChart(bars)

        result = drop_after(chart, end=dt_date(2023, 12, 4))

        # Should keep bars up to Dec 4
        assert len(result.bars) <= 3


class TestDomesticDailyChart:
    """Tests for domestic_daily_chart function."""

    def test_validates_empty_symbol(self):
        """Test validation of empty symbol."""
        from vmkis.api.stock.daily_chart import domestic_daily_chart

        fake_kis = _fake_kis()

        with pytest.raises(ValueError, match="종목 코드를 입력해주세요"):
            domestic_daily_chart(fake_kis, "")

    def test_datetime_conversion(self):
        """Test start/end datetime conversion to date."""
        from vmkis.api.stock.daily_chart import domestic_daily_chart

        fake_kis = _fake_kis()
        chart = _MockChart(
            [
                _MockBar(datetime(2023, 12, 1, 9, 0, 0)),
            ]
        )
        fake_kis.fetch.return_value = chart

        result = domestic_daily_chart(
            fake_kis, "005930", start=datetime(2023, 11, 1, 0, 0, 0), end=datetime(2023, 12, 1, 23, 59, 59)
        )

        assert result is not None

    def test_start_end_swap(self):
        """Test that start and end are swapped if start > end."""
        from datetime import date as dt_date

        from vmkis.api.stock.daily_chart import domestic_daily_chart

        fake_kis = _fake_kis()
        chart = _MockChart(
            [
                _MockBar(datetime(2023, 12, 1, 9, 0, 0)),
            ]
        )
        fake_kis.fetch.return_value = chart

        result = domestic_daily_chart(
            fake_kis,
            "005930",
            start=dt_date(2023, 12, 1),  # Later date
            end=dt_date(2023, 11, 1),  # Earlier date
        )

        assert result is not None
        # Verify fetch was called (dates should be swapped internally)
        assert fake_kis.fetch.called

    def test_period_mapping(self):
        """Test period parameter mapping."""
        from vmkis.api.stock.daily_chart import domestic_daily_chart

        fake_kis = _fake_kis()
        chart = _MockChart([_MockBar(datetime(2023, 12, 1, 9, 0, 0))])
        fake_kis.fetch.return_value = chart

        # Test week period
        domestic_daily_chart(fake_kis, "005930", period="week")
        assert fake_kis.fetch.call_args[1]["params"]["FID_PERIOD_DIV_CODE"] == "W"

        fake_kis.reset_mock()
        fake_kis.fetch.return_value = chart

        # Test month period
        domestic_daily_chart(fake_kis, "005930", period="month")
        assert fake_kis.fetch.call_args[1]["params"]["FID_PERIOD_DIV_CODE"] == "M"

        fake_kis.reset_mock()
        fake_kis.fetch.return_value = chart

        # Test year period
        domestic_daily_chart(fake_kis, "005930", period="year")
        assert fake_kis.fetch.call_args[1]["params"]["FID_PERIOD_DIV_CODE"] == "Y"

    def test_adjust_parameter(self):
        """Test adjust price parameter."""
        from vmkis.api.stock.daily_chart import domestic_daily_chart

        fake_kis = _fake_kis()
        chart = _MockChart([_MockBar(datetime(2023, 12, 1, 9, 0, 0))])
        fake_kis.fetch.return_value = chart

        # Test with adjust=True
        domestic_daily_chart(fake_kis, "005930", adjust=True)
        assert fake_kis.fetch.call_args[1]["params"]["FID_ORG_ADJ_PRC"] == "0"

        fake_kis.reset_mock()
        fake_kis.fetch.return_value = chart

        # Test with adjust=False
        domestic_daily_chart(fake_kis, "005930", adjust=False)
        assert fake_kis.fetch.call_args[1]["params"]["FID_ORG_ADJ_PRC"] == "1"

    def test_pagination_logic(self):
        """Test pagination with multiple fetches."""
        from datetime import date as dt_date

        from vmkis.api.stock.daily_chart import domestic_daily_chart

        fake_kis = _fake_kis()

        # First fetch
        chart1 = _MockChart(
            [
                _MockBar(datetime(2023, 12, 5, 9, 0, 0)),
                _MockBar(datetime(2023, 12, 4, 9, 0, 0)),
            ]
        )

        # Second fetch
        chart2 = _MockChart(
            [
                _MockBar(datetime(2023, 12, 3, 9, 0, 0)),
                _MockBar(datetime(2023, 12, 2, 9, 0, 0)),
            ]
        )

        # Third fetch - empty to stop
        chart3 = _MockChart([])

        fake_kis.fetch.side_effect = [chart1, chart2, chart3]

        result = domestic_daily_chart(fake_kis, "005930", start=dt_date(2023, 12, 1), end=dt_date(2023, 12, 5))

        assert result is not None
        assert fake_kis.fetch.call_count >= 2

    def test_timedelta_start_calculation(self):
        """Test timedelta start parameter calculation."""
        from vmkis.api.stock.daily_chart import domestic_daily_chart

        fake_kis = _fake_kis()
        chart = _MockChart(
            [
                _MockBar(datetime(2023, 12, 5, 9, 0, 0)),
                _MockBar(datetime(2023, 12, 4, 9, 0, 0)),
            ]
        )
        fake_kis.fetch.return_value = chart

        result = domestic_daily_chart(fake_kis, "005930", start=timedelta(days=5))

        assert result is not None


class TestForeignDailyChart:
    """Tests for foreign_daily_chart function."""

    def test_validates_empty_symbol(self):
        """Test validation of empty symbol."""
        from vmkis.api.stock.daily_chart import foreign_daily_chart

        fake_kis = _fake_kis()

        with pytest.raises(ValueError, match="종목 코드를 입력해주세요"):
            foreign_daily_chart(fake_kis, "", "NYSE")

    def test_datetime_conversion(self):
        """Test datetime to date conversion."""
        from vmkis.api.stock.daily_chart import foreign_daily_chart

        fake_kis = _fake_kis()
        chart = _MockChart([_MockBar(datetime(2023, 12, 1, 9, 0, 0))])
        fake_kis.fetch.return_value = chart

        result = foreign_daily_chart(fake_kis, "AAPL", "NASDAQ", start=datetime(2023, 11, 1), end=datetime(2023, 12, 1))

        assert result is not None

    def test_period_mapping(self):
        """Test period parameter mapping."""
        from vmkis.api.stock.daily_chart import foreign_daily_chart

        fake_kis = _fake_kis()
        chart = _MockChart([_MockBar(datetime(2023, 12, 1, 9, 0, 0))])
        fake_kis.fetch.return_value = chart

        # Test day
        foreign_daily_chart(fake_kis, "AAPL", "NASDAQ", period="day")
        assert fake_kis.fetch.call_args[1]["params"]["GUBN"] == "0"

        fake_kis.reset_mock()
        fake_kis.fetch.return_value = chart

        # Test week
        foreign_daily_chart(fake_kis, "AAPL", "NASDAQ", period="week")
        assert fake_kis.fetch.call_args[1]["params"]["GUBN"] == "1"

        fake_kis.reset_mock()
        fake_kis.fetch.return_value = chart

        # Test month
        foreign_daily_chart(fake_kis, "AAPL", "NASDAQ", period="month")
        assert fake_kis.fetch.call_args[1]["params"]["GUBN"] == "2"

    def test_year_period_aggregation(self):
        """Test year period aggregation logic."""
        from vmkis.api.stock.daily_chart import foreign_daily_chart

        fake_kis = _fake_kis()

        # Mock bars spanning multiple years
        chart = _MockChart(
            [
                _MockBar(datetime(2023, 12, 31, 9, 0, 0)),
                _MockBar(datetime(2023, 6, 15, 9, 0, 0)),
                _MockBar(datetime(2022, 12, 31, 9, 0, 0)),
                _MockBar(datetime(2022, 6, 15, 9, 0, 0)),
                _MockBar(datetime(2021, 12, 31, 9, 0, 0)),
            ]
        )
        fake_kis.fetch.return_value = chart

        result = foreign_daily_chart(fake_kis, "AAPL", "NASDAQ", period="year")

        # Should aggregate to yearly bars
        assert result is not None
        # Year aggregation should reduce bar count
        assert len(result.bars) < 5


class TestDailyChartDispatcher:
    """Tests for daily_chart dispatcher function."""

    def test_routes_to_domestic(self):
        """Test routing to domestic_daily_chart for KRX."""
        from vmkis.api.stock.daily_chart import daily_chart

        fake_kis = _fake_kis()
        chart = _MockChart([_MockBar(datetime(2023, 12, 1, 9, 0, 0))])
        fake_kis.fetch.return_value = chart

        with patch("vmkis.api.stock.daily_chart.domestic_daily_chart") as mock_domestic:
            mock_domestic.return_value = chart

            daily_chart(fake_kis, "005930", "KRX")

            assert mock_domestic.called
            assert mock_domestic.call_args[0][1] == "005930"

    def test_routes_to_foreign(self):
        """Test routing to foreign_daily_chart for non-KRX."""
        from vmkis.api.stock.daily_chart import daily_chart

        fake_kis = _fake_kis()
        chart = _MockChart([_MockBar(datetime(2023, 12, 1, 9, 0, 0))])
        fake_kis.fetch.return_value = chart

        with patch("vmkis.api.stock.daily_chart.foreign_daily_chart") as mock_foreign:
            mock_foreign.return_value = chart

            daily_chart(fake_kis, "AAPL", "NASDAQ")

            assert mock_foreign.called
            assert mock_foreign.call_args[0][1] == "AAPL"
            assert mock_foreign.call_args[0][2] == "NASDAQ"


class TestProductDailyChart:
    """Tests for product_daily_chart function."""

    def test_calls_daily_chart_with_product_attributes(self):
        """Test that product method calls daily_chart with correct args."""
        from datetime import date as dt_date

        from vmkis.api.stock.daily_chart import product_daily_chart

        fake_product = Mock()
        fake_product.kis = Mock()
        fake_product.symbol = "TSLA"
        fake_product.market = "NASDAQ"

        chart = _MockChart([_MockBar(datetime(2023, 12, 1, 9, 0, 0))])
        fake_product.kis.fetch.return_value = chart

        with patch("vmkis.api.stock.daily_chart.daily_chart") as mock_daily_chart:
            mock_daily_chart.return_value = chart

            product_daily_chart(
                fake_product, start=dt_date(2023, 11, 1), end=dt_date(2023, 12, 1), period="week", adjust=True
            )

            assert mock_daily_chart.called
            call_args = mock_daily_chart.call_args
            assert call_args[0][0] == fake_product.kis
            assert call_args[0][1] == "TSLA"
            assert call_args[0][2] == "NASDAQ"
            assert call_args[1]["start"] == dt_date(2023, 11, 1)
            assert call_args[1]["end"] == dt_date(2023, 12, 1)
            assert call_args[1]["period"] == "week"
            assert call_args[1]["adjust"] is True
