from ...._import import *

class KisStockAskingPrice:
    '''주식, ETF, ETN의 호가 정보'''
    items: list[int]
    '''호가'''

    def __init__(self, data: dict, prefix: str):
        self.items = [int(data[f'{prefix}{i}']) for i in range(1, 11)]
        
    def __getitem__(self, key: int):
        return self.items[key]

    def __iter__(self):
        return iter(self.items)

class KisStockAskingPrices(KisDynamicAPIResponse):
    aspr_acpt_hour: time
    '''호가 접수 시간'''
    askp: KisStockAskingPrice
    '''매도호가'''
    bidp: KisStockAskingPrice
    '''매수호가'''
    askp_rsqn: KisStockAskingPrice
    '''매도호가 잔량'''
    bidp_rsqn: KisStockAskingPrice
    '''매수호가 잔량'''
    askp_rsqn_icdc: KisStockAskingPrice
    '''매도호가 잔량 증감'''
    bidp_rsqn_icdc: KisStockAskingPrice
    '''매수호가 잔량 증감'''
    total_askp_rsqn: int
    '''총 매도호가 잔량'''
    total_bidp_rsqn: int
    '''총 매수호가 잔량'''
    total_askp_rsqn_icdc: int
    '''총 매도호가 잔량 증감'''
    total_bidp_rsqn_icdc: int
    '''총 매수호가 잔량 증감'''
    ovtm_total_askp_icdc: int
    '''시간외 총 매도호가 증감'''
    ovtm_total_bidp_icdc: int
    '''시간외 총 매수호가 증감'''
    ovtm_total_askp_rsqn: int
    '''시간외 총 매도호가 잔량'''
    ovtm_total_bidp_rsqn: int
    '''시간외 총 매수호가 잔량'''
    ntby_aspr_rsqn: int
    '''순매수 호가 잔량'''
    new_mkop_cls_code: str
    '''신 장운영 구분 코드'''
    antc_mkop_cls_code: str
    '''예상 장운영 구분 코드'''
    stck_prpr: int
    '''주식 현재가'''
    stck_oprc: int
    '''주식 시가'''
    stck_hgpr: int
    '''주식 최고가'''
    stck_lwpr: int
    '''주식 최저가'''
    stck_sdpr: int
    '''주식 기준가'''
    antc_cnpr: int
    '''예상 체결가'''
    antc_cntg_vrss_sign: str
    '''예상 체결 대비 부호'''
    antc_cntg_vrss: str
    '''예상 체결 대비'''
    antc_cntg_prdy_ctrct: str
    '''예상 체결 전일 대비율'''
    antc_vol: int
    '''예상 거래량'''
    stck_shrn_iscd: str
    '''주식 단축 종목코드'''
    vi_cls_code: str
    '''VI적용구분코드'''

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        data = data['output1']
        self.askp = KisStockAskingPrice(data, 'askp')
        self.bidp = KisStockAskingPrice(data, 'bidp')
        self.askp_rsqn = KisStockAskingPrice(data, 'askp_rsqn')
        self.bidp_rsqn = KisStockAskingPrice(data, 'bidp_rsqn')
        self.askp_rsqn_icdc = KisStockAskingPrice(data, 'askp_rsqn_icdc')
        self.bidp_rsqn_icdc = KisStockAskingPrice(data, 'bidp_rsqn_icdc')