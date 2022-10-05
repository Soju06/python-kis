from ._import import *

def asking_price(
    self: 'KisStockScope',
) -> 'KisStockAskingPrices':
    '''주식, ETF, ETN의 호가 정보를 가져옵니다.'''
    return self.client.request(
        'get',
        '/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn',
        headers={
            'tr_id': 'FHKST01010200'
        },
        params={
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': self.code,
        },
        response=KisStockAskingPrices
    )
