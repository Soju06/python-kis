"""Unit tests for vmkis.adapter.product.quote"""

from datetime import date, time
from types import SimpleNamespace


def test_daily_chart_day_chart_orderbook_quote_forward():
    """Test that mixin methods forward to the correct API functions."""
    from vmkis.adapter.product.quote import KisQuotableProductMixin

    calls = []

    def fake_daily(self, start=None, end=None, period="day", adjust=False):
        calls.append(("daily", start, end, period, adjust))
        return "daily-result"

    def fake_day(self, start=None, end=None, period=1):
        calls.append(("day", start, end, period))
        return "day-result"

    def fake_orderbook(self, condition=None):
        calls.append(("orderbook", condition))
        return "orderbook-result"

    def fake_quote(self, extended=False):
        calls.append(("quote", extended))
        return "quote-result"

    class TestProduct(KisQuotableProductMixin):
        def __init__(self):
            self.kis = SimpleNamespace()
            self.symbol = "005930"
            self.market = "KRX"

    orig_daily = KisQuotableProductMixin.daily_chart
    orig_day = KisQuotableProductMixin.day_chart
    orig_orderbook = KisQuotableProductMixin.orderbook
    orig_quote = KisQuotableProductMixin.quote

    try:
        KisQuotableProductMixin.daily_chart = fake_daily
        KisQuotableProductMixin.day_chart = fake_day
        KisQuotableProductMixin.orderbook = fake_orderbook
        KisQuotableProductMixin.quote = fake_quote

        prod = TestProduct()

        res_daily = prod.daily_chart(start=date(2023, 1, 1), period="week")
        assert res_daily == "daily-result"
        assert calls[0][0] == "daily"

        res_day = prod.day_chart(start=time(9, 0), period=5)
        assert res_day == "day-result"
        assert calls[1][0] == "day"

        res_book = prod.orderbook(condition="extended")
        assert res_book == "orderbook-result"
        assert calls[2] == ("orderbook", "extended")

        res_quote = prod.quote(extended=True)
        assert res_quote == "quote-result"
        assert calls[3] == ("quote", True)
    finally:
        KisQuotableProductMixin.daily_chart = orig_daily
        KisQuotableProductMixin.day_chart = orig_day
        KisQuotableProductMixin.orderbook = orig_orderbook
        KisQuotableProductMixin.quote = orig_quote


def test_chart_with_expression_converts_to_start():
    """chart method should convert expression to start timedelta."""
    from vmkis.adapter.product.quote import KisQuotableProductMixin

    calls = []

    def fake_daily(self, start=None, end=None, period="day", adjust=False):
        calls.append(("daily", type(start).__name__, period))
        return "daily-result"

    def fake_day(self, start=None, end=None, period=1):
        calls.append(("day", type(start).__name__, period))
        return "day-result"

    class TestProduct(KisQuotableProductMixin):
        def __init__(self):
            self.kis = SimpleNamespace()
            self.symbol = "005930"
            self.market = "KRX"

    import vmkis.api.stock.daily_chart as daily_api
    import vmkis.api.stock.day_chart as day_api

    orig_daily = daily_api.product_daily_chart
    orig_day = day_api.product_day_chart
    daily_api.product_daily_chart = fake_daily
    day_api.product_day_chart = fake_day

    try:
        prod = TestProduct()

        # expression "7d" should convert to timedelta and call daily_chart
        res = prod.chart("7d")
        assert res == "daily-result"
        assert calls[0][1] == "timedelta"

        # expression "30m" with small timedelta should call day_chart
        res2 = prod.chart("30m")
        assert res2 == "day-result"
        assert calls[1][0] == "day"
    finally:
        daily_api.product_daily_chart = orig_daily
        day_api.product_day_chart = orig_day


def test_chart_dispatches_by_period_type():
    """chart should dispatch to day_chart for int period, daily_chart for string period."""
    from vmkis.adapter.product.quote import KisQuotableProductMixin

    calls = []

    def fake_daily(self, start=None, end=None, period="day", adjust=False):
        calls.append(("daily", period))
        return "daily-result"

    def fake_day(self, start=None, end=None, period=1):
        calls.append(("day", period))
        return "day-result"

    class TestProduct(KisQuotableProductMixin):
        def __init__(self):
            self.kis = SimpleNamespace()
            self.symbol = "005930"
            self.market = "KRX"

    import vmkis.api.stock.daily_chart as daily_api
    import vmkis.api.stock.day_chart as day_api

    orig_daily = daily_api.product_daily_chart
    orig_day = day_api.product_day_chart
    daily_api.product_daily_chart = fake_daily
    day_api.product_day_chart = fake_day

    try:
        prod = TestProduct()

        # int period -> day chart
        res1 = prod.chart(start=time(9, 0), period=5)
        assert res1 == "day-result"
        assert calls[0] == ("day", 5)

        # string period -> daily chart
        res2 = prod.chart(start=date(2023, 1, 1), period="month")
        assert res2 == "daily-result"
        assert calls[1] == ("daily", "month")
    finally:
        daily_api.product_daily_chart = orig_daily
        day_api.product_day_chart = orig_day


def test_chart_raises_for_wrong_type_combinations():
    """chart should raise ValueError for mismatched start/period types."""
    from vmkis.adapter.product.quote import KisQuotableProductMixin

    class TestProduct(KisQuotableProductMixin):
        def __init__(self):
            self.kis = SimpleNamespace()
            self.symbol = "005930"
            self.market = "KRX"

    prod = TestProduct()

    # int period with date start -> should raise
    try:
        prod.chart(start=date(2023, 1, 1), period=5)
    except ValueError as e:
        assert "분봉 차트는 시간 타입만 지원" in str(e)
    else:
        raise AssertionError("Expected ValueError for date with int period")

    # string period with time start -> should raise
    try:
        prod.chart(start=time(9, 0), period="day")
    except ValueError as e:
        assert "기간 차트는 날짜 타입만 지원" in str(e)
    else:
        raise AssertionError("Expected ValueError for time with string period")
