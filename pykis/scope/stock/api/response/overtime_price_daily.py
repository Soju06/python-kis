from ...._import import *

class KisStockPricePeak(KisDynamic):
    '''일봉'''
    stck_bsop_date: datetime
    '''주식 영업 일자'''
    stck_oprc: int
    '''주식 시가'''
    stck_hgpr: int
    '''주식 최고가'''
    stck_lwpr: int
    '''주식 최저가'''
    stck_clpr: int
    '''주식 종가'''
    acml_vol: int
    '''누적 거래량'''
    prdy_vrss_vol_rate: float
    '''전일 대비 거래량 비율'''
    prdy_vrss: int
    '''전일 대비'''
    prdy_vrss_sign: str
    '''전일 대비 부호'''
    prdy_ctr: float
    '''전일 대비율'''
    hts_frgn_ehrt: float
    '''HTS 외국인 소진율'''
    frgn_ntby_qty: int
    '''외국인 순매수 수량'''
    flng_cls_code: str
    '''락 구분 코드'''
    acml_prtt_rate: float
    '''누적 분할 비율'''


class KisStockPriceDaily(KisDynamicAPIResponse):
    '''일봉'''
    prices: list[KisStockPricePeak]

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        self.prices = [KisStockPricePeak(price) for price in data['output']]
