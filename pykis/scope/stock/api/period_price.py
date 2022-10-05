from ._import import *

def period_price(
    self: 'KisStockScope',
    start_date: datetime,
    end_date: datetime,
    period: Literal['일', '주', '월', '년'] = '일',
    org_adj: bool = True,
) -> 'KisStockPeriodPrices':
    '''주식기간봉을 조회합니다.

    Args:
        start_date: 시작일
        end_date: 종료일
        org_adj: 수정주가 반영 여부. 기본값은 True.
    '''
    if not self.stock:
        raise ValueError('주식이 아닙니다.')

    return self.client.request(
        'get',
        '/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice',
        headers={
            'tr_id': 'FHKST03010100'
        },
        params={
            'FID_COND_MRKT_DIV_CODE': 'J',
            'FID_INPUT_ISCD': self.code,
            'FID_INPUT_DATE_1': start_date.strftime('%Y%m%d'),
            'FID_INPUT_DATE_2': end_date.strftime('%Y%m%d'),
            'FID_PERIOD_DIV_CODE': 'D' if period == '일' else 'W' if period == '주' else 'M' if period == '월' else 'Y',
            'FID_ORG_ADJ_PRC': '0' if org_adj else '1',
        },
        response=KisStockPeriodPrices
    )
