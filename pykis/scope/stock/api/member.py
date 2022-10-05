from ._import import *

def member(
    self: 'KisStockScope',
) -> 'KisStockMembers':
    '''주식, ETF, ETN의 회원별 매수/매도 거래량을 가져옵니다.'''
    return self.client.request(
        'get',
        '/uapi/domestic-stock/v1/quotations/inquire-member',
        headers={
            'tr_id': 'FHKST01010600'
        },
        params={
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': self.code,
        },
        response=KisStockMembers
    )
