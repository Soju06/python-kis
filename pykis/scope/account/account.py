
from ..base import KisScopeBase
from .._import import *


class KisAccountScope(KisScopeBase):
    '''주식 계좌'''
    account: 'KisAccount'
    '''주식 계좌'''

    def __init__(self, kis: 'PyKis', account: 'KisAccount'):
        super().__init__(kis)
        self.account = account

    from .api import \
        order, buy, sell, \
        overseas_order, overseas_buy, overseas_sell, \
        order_revise, cancel, revise, \
        overseas_order_revise, overseas_cancel, overseas_revise, \
        revisable_order, revisable_orders, revisable_order_all, \
        overseas_revisable_order, overseas_revisable_orders, overseas_revisable_order_all, \
        daily_orders, daily_order_all, \
        balances as balance, balance_all, \
        amount, profit
