from ._import import *

def overtime_conclude(
    self: 'KisStockScope',
) -> 'KisStockOvertimeConcludes':
    '''주식시간외채결정보를 조회합니다.'''
    if not self.stock:
        raise ValueError('주식이 아닙니다.')

    return self.client.request(
        'get',
        '/uapi/domestic-stock/v1/quotations/inquire-time-overtimeconclusion',
        headers={
            'tr_id': 'FHPST02310000'
        },
        params={
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': self.code,
            'FID_HOUR_CLS_CODE': '1'
        },
        response=KisStockOvertimeConcludes
    )
