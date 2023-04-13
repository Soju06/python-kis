from ._import import *

TR_ID_CODES = [
    # real
    'JTTT1002U',
    'JTTT1006U',
    # virtual
    'VTTT1002U',
    'VTTT1001U'
]

def order_us(
    self: 'KisAccountScope',
    code: str,
    qty: int,
    unpr: int,
    type: Literal['매도', '매수'],
    dvsn: US_ORD_DVSN_TYPE = '지정가',
    market: US_OVRS_EXCG_CD = 'NASD'
) -> 'KisStockOrder':
    '''주식 주문

    Args:
        code (str): 종목코드
        qty (int): 주문 수량
        unpr (int): 주문 단가 (시장가 주문 시 0)
        type (Literal['매도', '매수']): 주문 타입
        dvsn (US_ORD_DVSN_TYPE, optional): 주문 구분. Defaults to '지정가'.
        market (US_OVRS_EXCG_CD, optional): 시장 구분. Defaults to 'NASD'.
    '''
    if len(code) > 12:
        raise ValueError('종목코드는 12자리 이하입니다.')
    if len(dvsn) != 2:
        dvsn = US_R_ORD_DVSNS[dvsn]  # type: ignore

    return self.client.request(
        'post',
        '/uapi/overseas-stock/v1/trading/order',
        headers={
            'tr_id': TR_ID_CODES[(2 if self.key.virtual_account else 0) + (1 if type == '매도' else 0)]
        },
        body=self.account.build_body({
            'US_OVRS_EXCG_CD': '나스닥',
            'PDNO': code,
            'ORD_DVSN': dvsn,
            'ORD_QTY': qty,
            'OVRS_ORD_UNPR': unpr,
            'OVRS_EXCG_CD': market
        }),
        response=KisStockOrder
    )

def buy_us(
    self: 'KisAccountScope',
    code: str,
    qty: int,
    unpr: int,
    dvsn: US_ORD_DVSN_TYPE = '지정가',
) -> 'KisStockOrder':
    '''주식 매수

    Args:
        code (str): 종목코드
        qty (int): 주문 수량
        unpr (int): 주문 단가 (시장가 주문 시 0)
        dvsn (ORD_DVSN_TYPE, optional): 주문 구분. Defaults to '지정가'.
    '''
    return self.order_us(code, qty, unpr, '매수', dvsn)

def sell_us(
    self: 'KisAccountScope',
    code: str,
    qty: int,
    unpr: int,
    dvsn: US_ORD_DVSN_TYPE = '지정가',
) -> 'KisStockOrder':
    '''주식 매도

    Args:
        code (str): 종목코드
        qty (int): 주문 수량
        unpr (int): 주문 단가 (시장가 주문 시 0)
        dvsn (ORD_DVSN_TYPE, optional): 주문 구분. Defaults to '지정가'.
    '''
    return self.order_us(code, qty, unpr, '매도', dvsn)
