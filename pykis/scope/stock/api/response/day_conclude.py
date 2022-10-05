from ...._import import *

class KisStockDayConclude(KisDynamic):
    '''당일 시간 채결 정보'''
# -STCK_CNTG_HOUR	주식 체결 시간	String	N	6	
# -STCK_PBPR	주식 현재가	String	N	10	
# -PRDY_VRSS	전일 대비	String	N	10	
# -PRDY_VRSS_SIGN	전일 대비 부호	String	N	1	
# -PRDY_CTRT	전일 대비율	String	N	11	
# -ASKP	매도호가	String	N	10	
# -BIDP	매수호가	String	N	10	
# -TDAY_RLTV	당일 체결강도	String	N	14	
# -ACML_VOL	누적 거래량	String	N	18	
# -CNQN	체결량	String	N	18	
    stck_cntg_hour: time
    '''주식 체결 시간'''
    stck_pbpr: int
    '''주식 현재가'''
    prdy_vrss: int
    '''전일 대비'''
    prdy_vrss_sign: str
    '''전일 대비 부호'''
    prdy_ctrt: float
    '''전일 대비율'''
    askp: int
    '''매도호가'''
    bidp: int
    '''매수호가'''
    tday_rltv: float
    '''당일 체결강도'''
    acml_vol: int
    '''누적 거래량'''
    cnqn: int
    '''체결량'''

    def __init__(self, data: dict):
        super().__init__(data)


class KisStockDayConcludes(KisDynamicAPIResponse):
    '''일봉'''
# -STCK_PRPR	주식 현재가	String	N	10	
# -PRDY_VRSS	전일 대비	String	N	10	
# -PRDY_VRSS_SIGN	전일 대비 부호	String	N	1	
# -PRDY_CTRT	전일 대비율	String	N	11	
# -ACML_VOL	누적 거래량	String	N	18	
# -PRDY_VOL	전일 거래량	String	N	18	
# -HTS_KOR_ISNM	HTS 한글 종목명	String	N	40	
    stck_prpr: int
    '''주식 현재가'''
    prdy_vrss: int
    '''전일 대비'''
    prdy_vrss_sign: str
    '''전일 대비 부호'''
    prdy_ctrt: float
    '''전일 대비율'''
    acml_vol: int
    '''누적 거래량'''
    prdy_vol: int
    '''전일 거래량'''
    hts_kor_isnm: str
    '''HTS 한글 종목명'''
    concludes: list[KisStockDayConclude]
    '''채결 정보'''

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        self.concludes = [KisStockDayConclude(d) for d in data['output2']]
