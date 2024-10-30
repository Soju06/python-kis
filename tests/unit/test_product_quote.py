from datetime import date
from typing import TYPE_CHECKING
from unittest import TestCase

from pykis import PyKis
from pykis.adapter.product.quote import KisQuotableProduct
from pykis.api.stock.chart import KisChart, KisChartBar
from pykis.api.stock.order_book import KisOrderbook, KisOrderbookItem
from pykis.api.stock.quote import KisQuote

if TYPE_CHECKING:
    from ..env import load_pykis
else:
    from env import load_pykis


class ProductQuoteTests(TestCase):
    pykis: PyKis

    def setUp(self) -> None:
        self.pykis = load_pykis("real", use_websocket=False)

    def test_quotable(self):
        self.assertTrue(isinstance(self.pykis.stock("005930"), KisQuotableProduct))

    def test_krx_quote(self):
        self.assertTrue(isinstance(self.pykis.stock("005930").quote(), KisQuote))
        # https://github.com/Soju06/python-kis/issues/48
        # bstp_kor_isnm 필드 누락 대응
        self.assertTrue(isinstance(self.pykis.stock("002170").quote(), KisQuote))

    def test_nasd_quote(self):
        self.assertTrue(isinstance(self.pykis.stock("NVDA").quote(), KisQuote))

    def test_krx_orderbook(self):
        orderbook = self.pykis.stock("005930").orderbook()
        self.assertTrue(isinstance(orderbook, KisOrderbook))

        for ask in orderbook.asks:
            self.assertTrue(isinstance(ask, KisOrderbookItem))

        for bid in orderbook.bids:
            self.assertTrue(isinstance(bid, KisOrderbookItem))

    def test_nasd_orderbook(self):
        orderbook = self.pykis.stock("NVDA").orderbook()
        self.assertTrue(isinstance(orderbook, KisOrderbook))

        for ask in orderbook.asks:
            self.assertTrue(isinstance(ask, KisOrderbookItem))

        for bid in orderbook.bids:
            self.assertTrue(isinstance(bid, KisOrderbookItem))

    def test_krx_day_chart(self):
        chart = self.pykis.stock("005930").day_chart()
        self.assertTrue(isinstance(chart, KisChart))

        for bar in chart.bars:
            self.assertTrue(isinstance(bar, KisChartBar))

    def test_nasd_day_chart(self):
        chart = self.pykis.stock("NVDA").day_chart()
        self.assertTrue(isinstance(chart, KisChart))

        for bar in chart.bars:
            self.assertTrue(isinstance(bar, KisChartBar))

    def test_krx_daily_chart(self):
        stock = self.pykis.stock("005930")
        daily_chart_1m = stock.daily_chart(start=date(2024, 6, 1), end=date(2024, 6, 30), period="day")
        weekly_chart_1m = stock.daily_chart(start=date(2024, 6, 1), end=date(2024, 6, 30), period="week")

        self.assertTrue(isinstance(daily_chart_1m, KisChart))
        self.assertTrue(isinstance(weekly_chart_1m, KisChart))
        self.assertEqual(len(daily_chart_1m.bars), 19)
        self.assertEqual(len(weekly_chart_1m.bars), 4)

        for bar in daily_chart_1m.bars:
            self.assertTrue(isinstance(bar, KisChartBar))

        for bar in weekly_chart_1m.bars:
            self.assertTrue(isinstance(bar, KisChartBar))

    def test_nasd_daily_chart(self):
        stock = self.pykis.stock("NVDA")
        daily_chart_1m = stock.daily_chart(start=date(2024, 6, 1), end=date(2024, 6, 30), period="day")
        weekly_chart_1m = stock.daily_chart(start=date(2024, 6, 1), end=date(2024, 6, 30), period="week")

        self.assertTrue(isinstance(daily_chart_1m, KisChart))
        self.assertTrue(isinstance(weekly_chart_1m, KisChart))
        self.assertEqual(len(daily_chart_1m.bars), 19)
        self.assertEqual(len(weekly_chart_1m.bars), 4)

        for bar in daily_chart_1m.bars:
            self.assertTrue(isinstance(bar, KisChartBar))

        for bar in weekly_chart_1m.bars:
            self.assertTrue(isinstance(bar, KisChartBar))

    def test_krx_chart(self):
        stock = self.pykis.stock("005930")
        yearly_chart = stock.chart("30y", period="year")
        self.assertTrue(isinstance(yearly_chart, KisChart))
        self.assertAlmostEqual(len(yearly_chart.bars), 30, delta=1)

        for bar in yearly_chart.bars:
            self.assertTrue(isinstance(bar, KisChartBar))

    def test_nasd_chart(self):
        stock = self.pykis.stock("NVDA")
        yearly_chart = stock.chart("15y", period="year")
        self.assertTrue(isinstance(yearly_chart, KisChart))
        self.assertAlmostEqual(len(yearly_chart.bars), 15, delta=1)

        for bar in yearly_chart.bars:
            self.assertTrue(isinstance(bar, KisChartBar))
