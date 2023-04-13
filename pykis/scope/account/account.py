
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
        order_us, buy_us, sell_us, \
        order_revise, cancel, revise, \
        order_revise_us, cancel_us, revise_us, \
        revisable_orders, revisable_order_all, \
        daily_orders, daily_order_all, \
        balances as balance, balance_all, \
        amount, profit
