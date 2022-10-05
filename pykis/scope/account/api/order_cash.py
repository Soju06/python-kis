from ._import import *

TR_ID_CODES = [
    # real
    'TTTC0802U',
    'TTTC0801U',
    # virtual
    'VTTC0802U',
    'VTTC0801U'
]

def order(
    self: 'KisAccountScope',
    code: str,
    qty: int,
    unpr: int,
    type: Literal['매도', '매수'],
    dvsn: ORD_DVSN_TYPE = '지정가',
) -> 'KisStockOrder':
    '''주식 주문

    Args:
        code (str): 종목코드
        qty (int): 주문 수량
        unpr (int): 주문 단가 (시장가 주문 시 0)
        type (Literal['매도', '매수']): 주문 타입
        dvsn (ORD_DVSN_TYPE, optional): 주문 구분. Defaults to '지정가'.
    '''
    if len(code) != 6:
        raise ValueError('종목코드는 6자리입니다.')
    if len(dvsn) != 2:
        dvsn = R_ORD_DVSNS[dvsn]  # type: ignore

    return self.client.request(
        'post',
        '/uapi/domestic-stock/v1/trading/order-cash',
        headers={
            'tr_id': TR_ID_CODES[(2 if self.key.virtual_account else 0) + (1 if type == '매도' else 0)]
        },
        body=self.account.build_body({
            'PDNO': code,
            'ORD_DVSN': dvsn,
            'ORD_QTY': qty,
            'ORD_UNPR': unpr
        }),
        response=KisStockOrder
    )

def buy(
    self: 'KisAccountScope',
    code: str,
    qty: int,
    unpr: int,
    dvsn: ORD_DVSN_TYPE = '지정가',
) -> 'KisStockOrder':
    '''주식 매수

    Args:
        code (str): 종목코드
        qty (int): 주문 수량
        unpr (int): 주문 단가 (시장가 주문 시 0)
        dvsn (ORD_DVSN_TYPE, optional): 주문 구분. Defaults to '지정가'.
    '''
    return self.order(code, qty, unpr, '매수', dvsn)

def sell(
    self: 'KisAccountScope',
    code: str,
    qty: int,
    unpr: int,
    dvsn: ORD_DVSN_TYPE = '지정가',
) -> 'KisStockOrder':
    '''주식 매도

    Args:
        code (str): 종목코드
        qty (int): 주문 수량
        unpr (int): 주문 단가 (시장가 주문 시 0)
        dvsn (ORD_DVSN_TYPE, optional): 주문 구분. Defaults to '지정가'.
    '''
    return self.order(code, qty, unpr, '매도', dvsn)
