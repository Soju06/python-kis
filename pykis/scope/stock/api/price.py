from ._import import *

def price(
    self: 'KisStockScope',
) -> 'KisStockPrice':
    '''주식현재가를 조회합니다.'''
    return self.client.request(
        'get',
        '/uapi/domestic-stock/v1/quotations/inquire-price',
        headers={
            'tr_id': 'FHKST01010100'
        },
        params={
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': self.code,
        },
        response=KisStockPrice
    )
