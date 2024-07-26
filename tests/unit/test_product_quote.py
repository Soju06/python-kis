from datetime import date
from unittest import TestCase

from pykis import PyKis
from pykis.adapter.product.quote import KisQuotableProduct
from pykis.api.stock.chart import KisChart
from pykis.api.stock.order_book import KisOrderBook
from pykis.api.stock.quote import KisQuote
from tests.env import load_pykis


class ProductQuoteTests(TestCase):
    pykis: PyKis

    def setUp(self) -> None:
        self.pykis = load_pykis("real", use_websocket=False)

    def test_quotable(self):
        self.assertTrue(isinstance(self.pykis.stock("005930"), KisQuotableProduct))

    def test_krx_quote(self):
        self.assertTrue(isinstance(self.pykis.stock("005930").quote(), KisQuote))

    def test_nasd_quote(self):
        self.assertTrue(isinstance(self.pykis.stock("NVDA").quote(), KisQuote))

    def test_krx_orderbook(self):
        self.assertTrue(isinstance(self.pykis.stock("005930").orderbook(), KisOrderBook))

    def test_nasd_orderbook(self):
        self.assertTrue(isinstance(self.pykis.stock("NVDA").orderbook(), KisOrderBook))

    def test_krx_day_chart(self):
        self.assertTrue(isinstance(self.pykis.stock("005930").day_chart(), KisChart))

    def test_nasd_day_chart(self):
        self.assertTrue(isinstance(self.pykis.stock("NVDA").day_chart(), KisChart))

    def test_krx_daily_chart(self):
        stock = self.pykis.stock("005930")
        daily_chart_1m = stock.daily_chart(start=date(2024, 6, 1), end=date(2024, 6, 30), period="day")
        weekly_chart_1m = stock.daily_chart(start=date(2024, 6, 1), end=date(2024, 6, 30), period="week")

        self.assertTrue(isinstance(daily_chart_1m, KisChart))
        self.assertTrue(isinstance(weekly_chart_1m, KisChart))
        self.assertEqual(len(daily_chart_1m.bars), 19)
        self.assertEqual(len(weekly_chart_1m.bars), 4)

    def test_nasd_daily_chart(self):
        stock = self.pykis.stock("NVDA")
        daily_chart_1m = stock.daily_chart(start=date(2024, 6, 1), end=date(2024, 6, 30), period="day")
        weekly_chart_1m = stock.daily_chart(start=date(2024, 6, 1), end=date(2024, 6, 30), period="week")

        self.assertTrue(isinstance(daily_chart_1m, KisChart))
        self.assertTrue(isinstance(weekly_chart_1m, KisChart))
        self.assertEqual(len(daily_chart_1m.bars), 19)
        self.assertEqual(len(weekly_chart_1m.bars), 4)

    def test_krx_chart(self):
        stock = self.pykis.stock("005930")
        yearly_chart = stock.chart("30y", period="year")
        self.assertTrue(isinstance(yearly_chart, KisChart))
        self.assertAlmostEqual(len(yearly_chart.bars), 30, delta=1)

    def test_nasd_chart(self):
        stock = self.pykis.stock("NVDA")
        yearly_chart = stock.chart("15y", period="year")
        self.assertTrue(isinstance(yearly_chart, KisChart))
        self.assertAlmostEqual(len(yearly_chart.bars), 15, delta=1)
