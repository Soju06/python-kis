from ...._import import *

class KisStockInvestor(KisDynamic):
    stck_bsop_date: datetime
    '''주식 영업 일자'''
    stck_clpr: int
    '''주식 종가'''
    prdy_vrss: int
    '''전일 대비'''
    prdy_vrss_sign: int
    '''전일 대비 부호'''
    prsn_ntby_qty: int
    '''개인 순매수 수량'''
    frgn_ntby_qty: int
    '''외국인 순매수 수량'''
    orgn_ntby_qty: int
    '''기관계 순매수 수량'''
    prsn_ntby_tr_pbmn: int
    '''개인 순매수 거래 대금'''
    frgn_ntby_tr_pbmn: int
    '''외국인 순매수 거래 대금'''
    orgn_ntby_tr_pbmn: int
    '''기관계 순매수 거래 대금'''
    prsn_shnu_vol: int
    '''개인 매수2 거래량'''
    frgn_shnu_vol: int
    '''외국인 매수2 거래량'''
    orgn_shnu_vol: int
    '''기관계 매수2 거래량'''
    prsn_shnu_tr_pbmn: int
    '''개인 매수2 거래 대금'''
    frgn_shnu_tr_pbmn: int
    '''외국인 매수2 거래 대금'''
    orgn_shnu_tr_pbmn: int
    '''기관계 매수2 거래 대금'''
    prsn_seln_vol: int
    '''개인 매도 거래량'''
    frgn_seln_vol: int
    '''외국인 매도 거래량'''
    orgn_seln_vol: int
    '''기관계 매도 거래량'''
    prsn_seln_tr_pbmn: int
    '''개인 매도 거래 대금'''
    frgn_seln_tr_pbmn: int
    '''외국인 매도 거래 대금'''
    orgn_seln_tr_pbmn: int
    '''기관계 매도 거래 대금'''

class KisStockInvestors(KisDynamicAPIResponse):
    investors: list[KisStockInvestor]

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        self.investors = [KisStockInvestor(investor) for investor in data['output']]