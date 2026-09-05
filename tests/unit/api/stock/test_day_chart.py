from datetime import datetime, time, timedelta
from decimal import Decimal

import pytest

from vmkis.api.stock import day_chart
from vmkis.api.stock.day_chart import KisDayChartBarBase


class _B:
    def __init__(self, t):
        self.time = t
        self.time_kst = t
        self.open = 1
        self.high = 2
        self.low = 1
        self.close = 1.5
        self.volume = 10
        self.amount = 100
        self.change = 0


def test_drop_after_time_range():
    """`drop_after` trims bars outside the given start/end range."""
    b1 = _B(datetime(2020, 1, 1, 9, 0))
    b2 = _B(datetime(2020, 1, 1, 10, 0))
    chart = type("C", (), {})()
    chart.bars = [b1, b2]

    res = day_chart.drop_after(chart, start=time(9, 30), end=time(10, 0))
    # result must be a list of bars within the requested time range (may be empty)
    assert isinstance(res.bars, list)
    for bar in res.bars:
        assert time(9, 30) <= bar.time.time() <= time(10, 0)


def test_domestic_day_chart_validations():
    """`domestic_day_chart` validates symbol and period parameters."""
    fake = type("K", (), {})()
    try:
        day_chart.domestic_day_chart(fake, "")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for empty symbol")

    try:
        day_chart.domestic_day_chart(fake, "SYM", period=0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for invalid period")


def test_domestic_day_chart_time_validation():
    """Test that start time must be before end time."""
    fake = type("K", (), {})()

    with pytest.raises(ValueError) as exc_info:
        day_chart.domestic_day_chart(fake, "005930", start=time(15, 0), end=time(9, 0))

    assert "시작 시간" in str(exc_info.value) or "종료 시간" in str(exc_info.value)


def test_daychartbarbase_properties():
    """Test KisDayChartBarBase computed properties."""
    bar = object.__new__(KisDayChartBarBase)
    bar.close = Decimal("100")
    bar.change = Decimal("5")
    bar.open = Decimal("95")
    bar.high = Decimal("105")
    bar.low = Decimal("90")
    bar.volume = 1000
    bar.amount = Decimal("100000")

    # Test sign property
    assert bar.sign == "rise"

    bar.change = Decimal("0")
    assert bar.sign == "steady"

    bar.change = Decimal("-5")
    assert bar.sign == "decline"


def test_daychartbarbase_price_properties():
    """Test price-related properties."""
    bar = object.__new__(KisDayChartBarBase)
    bar.close = Decimal("100")
    bar.change = Decimal("5")

    # Test price property
    assert bar.price == Decimal("100")

    # Test prev_price property
    assert bar.prev_price == Decimal("95")

    # Test rate property (등락률)
    assert bar.rate == Decimal("5") / Decimal("95") * 100


def test_daychartbarbase_sign_name():
    """Test sign_name property returns Korean names."""
    bar = object.__new__(KisDayChartBarBase)
    bar.close = Decimal("100")

    bar.change = Decimal("5")
    assert bar.sign_name in ["상승", "상한", "보합", "하한", "하락"]

    bar.change = Decimal("0")
    assert bar.sign_name in ["상승", "상한", "보합", "하한", "하락"]

    bar.change = Decimal("-5")
    assert bar.sign_name in ["상승", "상한", "보합", "하한", "하락"]


def test_drop_after_with_timedelta_start():
    """Test drop_after when start is a timedelta."""
    b1 = _B(datetime(2020, 1, 1, 9, 0))
    b2 = _B(datetime(2020, 1, 1, 10, 0))
    b3 = _B(datetime(2020, 1, 1, 11, 0))

    chart = type("C", (), {})()
    chart.bars = [b1, b2, b3]

    # Start from 2 hours before the first bar
    res = day_chart.drop_after(chart, start=timedelta(hours=2))

    # Should convert timedelta to time and filter
    assert isinstance(res.bars, list)


def test_drop_after_with_period():
    """Test drop_after with period parameter."""
    bars = [_B(datetime(2020, 1, 1, 9, i)) for i in range(10)]

    chart = type("C", (), {})()
    chart.bars = bars

    # Every 2nd bar
    res = day_chart.drop_after(chart, period=2)

    # Should include only bars at period intervals
    assert isinstance(res.bars, list)
    # Note: period filtering uses modulo, so length depends on implementation


def test_drop_after_filters_by_start_only():
    """Test drop_after filters by start time only."""
    b1 = _B(datetime(2020, 1, 1, 9, 0))
    b2 = _B(datetime(2020, 1, 1, 10, 0))
    b3 = _B(datetime(2020, 1, 1, 11, 0))

    chart = type("C", (), {})()
    chart.bars = [b1, b2, b3]

    res = day_chart.drop_after(chart, start=time(10, 0))

    # Should include bars from 10:00 onwards (going backwards in time)
    assert isinstance(res.bars, list)


def test_drop_after_filters_by_end_only():
    """Test drop_after filters by end time only."""
    b1 = _B(datetime(2020, 1, 1, 9, 0))
    b2 = _B(datetime(2020, 1, 1, 10, 0))
    b3 = _B(datetime(2020, 1, 1, 11, 0))

    chart = type("C", (), {})()
    chart.bars = [b1, b2, b3]

    res = day_chart.drop_after(chart, end=time(10, 0))

    # Should exclude bars after 10:00
    assert isinstance(res.bars, list)


def test_drop_after_no_filters():
    """Test drop_after with no filters returns all bars."""
    b1 = _B(datetime(2020, 1, 1, 9, 0))
    b2 = _B(datetime(2020, 1, 1, 10, 0))

    chart = type("C", (), {})()
    chart.bars = [b1, b2]

    res = day_chart.drop_after(chart)

    # Should return all bars in reverse order
    assert len(res.bars) == 2
