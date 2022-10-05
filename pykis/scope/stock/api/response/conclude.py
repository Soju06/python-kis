from ...._import import *

class KisStockConclude(KisDynamic):
    '''주식현재가 채결'''
    stck_cntg_hour: time
    '''주식 체결 시간'''
    stck_prpr: int
    '''주식 현재가'''
    prdy_vrss: int
    '''전일 대비'''
    prdy_vrss_sign: Literal[1, 2, 3, 4, 5]
    '''전일 대비 부호'''
    cntg_vol: int
    '''체결 거래량'''
    tday_rltv: float
    '''당일 체결강도'''
    prdy_ctrt: float
    '''전일 대비율'''

    def __init__(self, data: dict):
        super().__init__(data)

class KisStockConcludes(KisDynamicAPIResponse):
    '''주식현재가 체결'''
    concludes: list[KisStockConclude]
    '''체결'''

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        self.concludes = [KisStockConclude(conclude) for conclude in data['output']]
