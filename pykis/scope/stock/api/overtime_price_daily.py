from ._import import *

def overtime_price_daily(
    self: 'KisStockScope',
    period: Literal['일', '주', '월'] = '일',
    org_adj: bool = False,
) -> 'KisStockPriceDaily':
    '''주식시간외일자별가격을 조회합니다.

    Args:
        period: 기간. 기본값은 day.
        org_adj: 수정주가 반영 여부. 기본값은 False.
    '''

    return self.client.request(
        'get',
        '/uapi/domestic-stock/v1/quotations/inquire-daily-overtimeprice',
        headers={
            'tr_id': 'FHPST02320000'
        },
        params={
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': self.code,
            'FID_PERIOD_DIV_CODE': 'D' if period == '일' else 'W' if period == '주' else 'M',
            'FID_ORG_ADJ_PRC': '0' if org_adj else '1',
        },
        response=KisStockPriceDaily
    )
