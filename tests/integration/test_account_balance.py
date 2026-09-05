from decimal import Decimal
from unittest import TestCase

import pytest
from requests.exceptions import SSLError
from tests.env import load_vmkis

from vmkis import VmKis
from vmkis.api.account.balance import KisBalance, KisDeposit
from vmkis.client.exceptions import KisAPIError, KisHTTPError
from vmkis.scope.account import KisAccount

pytestmark = pytest.mark.requires_api


class AccountBalanceTests(TestCase):
    vmkis: VmKis
    paper_vmkis: VmKis

    @classmethod
    def setUpClass(cls) -> None:
        """클래스 레벨에서 한 번만 실행 - 토큰 발급 횟수 제한 방지"""
        cls.vmkis = load_vmkis("live", use_websocket=False)
        cls.paper_vmkis = load_vmkis("paper", use_websocket=False)

    def test_account_scope(self):
        account = self.vmkis.account()

        self.assertTrue(isinstance(account, KisAccount))

    def test_virtual_account_scope(self):
        account = self.paper_vmkis.account()

        self.assertTrue(isinstance(account, KisAccount))

    def test_balance(self):
        try:
            account = self.vmkis.account()
            balance = account.balance()

            self.assertTrue(isinstance(balance, KisBalance))
            self.assertTrue(isinstance(balance.deposits["KRW"], KisDeposit))

            if (usd_deposit := balance.deposits.get("USD")) is not None:
                self.assertTrue(isinstance(usd_deposit, KisDeposit))
                self.assertGreater(usd_deposit.exchange_rate, Decimal(800))
        except (KisHTTPError, KisAPIError, SSLError) as e:
            self.skipTest(f"API call failed: {e}")

    def test_virtual_balance(self):
        try:
            balance = self.paper_vmkis.account().balance()

            self.assertTrue(isinstance(balance, KisBalance))
            self.assertIsNotNone(balance.deposits["KRW"])
            self.assertIsNotNone(balance.deposits["USD"])
            self.assertTrue(isinstance(balance.deposits["KRW"], KisDeposit))
            self.assertTrue(isinstance(balance.deposits["USD"], KisDeposit))
            self.assertGreater(balance.deposits["USD"].exchange_rate, Decimal(800))
        except (KisHTTPError, KisAPIError, SSLError) as e:
            self.skipTest(f"Virtual API call failed: {e}")

    def test_balance_stock(self):
        try:
            balance = self.vmkis.account().balance()

            if not balance.stocks:
                self.skipTest("No stocks in account")

            for stock in balance.stocks:
                # isinstance() 체크 시 Protocol의 모든 속성에 접근하여 API 호출이 발생하므로
                # 필수 속성이 있는지만 확인
                self.assertTrue(hasattr(stock, "symbol"))
                self.assertTrue(hasattr(stock, "quantity"))
        except (KisHTTPError, KisAPIError, SSLError) as e:
            self.skipTest(f"Balance API call failed: {e}")

    def test_virtual_balance_stock(self):
        try:
            balance = self.paper_vmkis.account().balance()

            if not balance.stocks:
                self.skipTest("No stocks in account")

            for stock in balance.stocks:
                # isinstance() 체크 시 Protocol의 모든 속성에 접근하여 API 호출이 발생하므로
                # 필수 속성이 있는지만 확인
                self.assertTrue(hasattr(stock, "symbol"))
                self.assertTrue(hasattr(stock, "quantity"))
        except (KisHTTPError, KisAPIError, SSLError) as e:
            self.skipTest(f"Virtual balance API call failed: {e}")
