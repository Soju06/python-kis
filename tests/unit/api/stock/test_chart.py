import sys
from datetime import datetime
from decimal import Decimal

from vmkis.api.stock import chart


class _Bar:
    def __init__(self, ts, open_, high, low, close, volume, amount, change):
        self.time = ts
        self.time_kst = ts
        self.open = Decimal(open_)
        self.high = Decimal(high)
        self.low = Decimal(low)
        self.close = Decimal(close)
        self.volume = int(volume)
        self.amount = Decimal(amount)
        self.change = Decimal(change)


def _make_chart(bars):
    # Create a simple object that uses KisChartBase behavior by instantiating a subclass
    class Dummy(chart.KisChartBase):
        pass

    d = Dummy()
    d.symbol = "SYM"
    d.market = "KRX"
    d.timezone = None
    d.bars = bars
    return d


def test_index_and_getitem_order_by_len_iter():
    """Indexing, ordering, __getitem__, iteration and length behave as expected."""
    now = datetime(2020, 1, 1, 9, 0, 0)
    bars = [
        _Bar(now, "1", "2", "1", "1.5", 10, "100", "0"),
        _Bar(now.replace(hour=10), "2", "3", "2", "2.5", 5, "200", "0"),
    ]
    c = _make_chart(bars)

    # index by datetime
    idx0 = c.index(now)
    assert idx0 == 0

    # __getitem__ by int
    assert c[0] is bars[0]

    # __getitem__ by datetime
    assert c[now] is bars[0]

    # order_by volume ascending
    ordered = c.order_by("volume")
    assert ordered[0].volume == 5

    # iteration and len
    assert list(iter(c)) == bars
    assert len(c) == 2


def test_slice_getitem_by_range():
    """Slicing by datetime ranges returns the matching bars list."""
    b1 = _Bar(datetime(2020, 1, 1, 9), "1", "2", "1", "1.5", 10, "100", "0")
    b2 = _Bar(datetime(2020, 1, 1, 10), "2", "3", "2", "2.5", 5, "200", "0")
    c = _make_chart([b1, b2])

    # slice by datetimes
    res = c[datetime(2020, 1, 1, 9) : datetime(2020, 1, 1, 10)]
    assert b1 in res


def test_index_out_of_range_raises():
    """Indexing a non-existing time raises ValueError."""
    b1 = _Bar(datetime(2020, 1, 1, 9), "1", "2", "1", "1.5", 10, "100", "0")
    c = _make_chart([b1])
    # search for a time after the last bar should raise
    try:
        c.index(datetime(2030, 1, 1))
    except ValueError as e:
        assert "차트에" in str(e)
    else:
        raise AssertionError("Expected ValueError for missing bar")


def test_df_importerror_and_success(monkeypatch):
    """`df()` raises ImportError when pandas missing, and returns DataFrame when available."""
    b1 = _Bar(datetime(2020, 1, 1, 9), "1", "2", "1", "1.5", 10, "100", "0")
    c = _make_chart([b1])

    # Ensure pandas not present
    if "pandas" in sys.modules:
        monkeypatch.setitem(sys.modules, "_pandas_backup", sys.modules.pop("pandas"))

    try:
        try:
            c.df()
        except ImportError:
            pass
        else:
            raise AssertionError("Expected ImportError when pandas not installed")

        # Provide a fake pandas
        class FakePD:
            @staticmethod
            def DataFrame(obj):
                return {k: v for k, v in obj.items()}

        monkeypatch.setitem(sys.modules, "pandas", FakePD())
        df = c.df()
        assert "time" in df and "open" in df
    finally:
        # restore pandas if it was present
        if "_pandas_backup" in sys.modules:
            monkeypatch.setitem(sys.modules, "pandas", sys.modules.pop("_pandas_backup"))
