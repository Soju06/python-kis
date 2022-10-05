from ._import import *

def investor(
    self: 'KisStockScope',
) -> 'KisStockInvestors':
    '''주식 투자자별 매매동향 조회'''
    return self.client.request(
        'get',
        '/uapi/domestic-stock/v1/quotations/inquire-investor',
        headers={
            'tr_id': 'FHKST01010900'
        },
        params={
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': self.code
        },
        response=KisStockInvestors
    )
