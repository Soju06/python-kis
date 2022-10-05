from ._import import *

def day_conclude(
    self: 'KisStockScope',
    time: time,
) -> 'KisStockDayConcludes':
    '''주식일별체결정보를 조회합니다. (주식 전용)

    Args:
        time: 시간
    '''
    if not self.stock:
        raise ValueError('주식이 아닙니다.')

    return self.client.request(
        'get',
        '/uapi/domestic-stock/v1/quotations/inquire-time-itemconclusion',
        headers={
            'tr_id': 'FHPST01060000'
        },
        params={
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': self.code,
            'FID_INPUT_HOUR_1': time.strftime('%H%M%S'),
        },
        response=KisStockDayConcludes
    )
