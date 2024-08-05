from decimal import Decimal
from typing import TYPE_CHECKING
from unittest import TestCase

from pykis import PyKis
from pykis.api.account.balance import KisBalance, KisBalanceStock, KisDeposit
from pykis.scope.account import KisAccount

if TYPE_CHECKING:
    from ..env import load_pykis
else:
    from env import load_pykis


class AccountBalanceTests(TestCase):
    pykis: PyKis
    virtual_pykis: PyKis

    def setUp(self) -> None:
        self.pykis = load_pykis("real", use_websocket=False)
        self.virtual_pykis = load_pykis("virtual", use_websocket=False)

    def test_account_scope(self):
        account = self.pykis.account()

        self.assertTrue(isinstance(account, KisAccount))

    def test_virtual_account_scope(self):
        account = self.virtual_pykis.account()

        self.assertTrue(isinstance(account, KisAccount))

    def test_balance(self):
        account = self.pykis.account()
        balance = account.balance()

        self.assertTrue(isinstance(balance, KisBalance))
        self.assertTrue(isinstance(balance.deposits["KRW"], KisDeposit))

        if (usd_deposit := balance.deposits["USD"]) is not None:
            self.assertTrue(isinstance(usd_deposit, KisDeposit))
            self.assertGreater(usd_deposit.exchange_rate, Decimal(800))

    def test_virtual_balance(self):
        balance = self.virtual_pykis.account().balance()

        self.assertTrue(isinstance(balance, KisBalance))
        self.assertIsNotNone(balance.deposits["KRW"])
        self.assertIsNotNone(balance.deposits["USD"])
        self.assertIsNotNone(isinstance(balance.deposits["KRW"], KisDeposit))
        self.assertIsNotNone(isinstance(balance.deposits["USD"], KisDeposit))
        self.assertGreater(balance.deposits["USD"].exchange_rate, Decimal(800))

    def test_balance_stock(self):
        balance = self.pykis.account().balance()

        if not balance.stocks:
            self.skipTest("No stocks in account")

        for stock in balance.stocks:
            self.assertTrue(isinstance(stock, KisBalanceStock))

    def test_virtual_balance_stock(self):
        balance = self.virtual_pykis.account().balance()

        if not balance.stocks:
            self.skipTest("No stocks in account")

        for stock in balance.stocks:
            self.assertTrue(isinstance(stock, KisBalanceStock))
