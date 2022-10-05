from ._import import *

def elw_price(
    self: 'KisStockScope'
) -> 'KisELWPrice':
    '''ELW 가격을 가져옵니다.

    Args:
        code (str): 종목코드
    '''
    if not self.elw:
        raise ValueError('ELW가 아닙니다.')

    return self.client.request(
        'get',
        '/uapi/domestic-stock/v1/quotations/inquire-elw-price',
        headers={
            'tr_id': 'FHKEW15010000'
        },
        params={
            'FID_COND_MRKT_DIV_CODE': 'W',
            'FID_INPUT_ISCD': self.code,
        },
        response=KisELWPrice
    )
