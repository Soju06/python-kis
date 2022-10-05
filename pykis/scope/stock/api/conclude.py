from ._import import *

def conclude(
    self: 'KisStockScope',
) -> 'KisStockConcludes':
    '''주식체결정보를 조회합니다.'''
    return self.client.request(
        'get',
        '/uapi/domestic-stock/v1/quotations/inquire-price',
        headers={
            'tr_id': 'FHKST01010300'
        },
        params={
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': self.code
        },
        response=KisStockConcludes
    )
