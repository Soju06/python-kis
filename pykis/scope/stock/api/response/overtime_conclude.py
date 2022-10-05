from ...._import import *

class KisStockOvertimeConclude(KisDynamic):
    '''시간외 채결 정보'''
# -STCK_CNTG_HOUR	주식 체결 시간	String	N	6	
# -STCK_PRPR	주식 현재가	String	N	10	
# -PRDY_VRSS	전일 대비	String	N	10	
# -PRDY_VRSS_SIGN	전일 대비 부호	String	N	1	
# -PRDY_CTRT	전일 대비율	String	N	11	
# -ASKP	매도호가	String	N	10	
# -BIDP	매수호가	String	N	10	
# -ACML_VOL	누적 거래량	String	N	18	
# -CNTG_VOL	체결 거래량	String	N	18	
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
    acml_vol: int
    '''누적 거래량'''
    cntg_vol: int
    '''체결 거래량'''


    def __init__(self, data: dict):
        super().__init__(data)


class KisStockOvertimeConcludes(KisDynamicAPIResponse):
    '''시간외 채결 정보'''
# -OVTM_UNTP_PRPR	시간외 단일가 현재가	String	N	10	
# -OVTM_UNTP_PRDY_VRSS	시간외 단일가 전일 대비	String	N	10	
# -OVTM_UNTP_PRDY_VRSS_SIGN	시간외 단일가 전일 대비 부호	String	N	1	
# -OVTM_UNTP_PRDY_CTRT	시간외 단일가 전일 대비율	String	N	11	
# -OVTM_UNTP_VOL	시간외 단일가 거래량	String	N	18	
# -OVTM_UNTP_TR_PBMN	시간외 단일가 거래 대금	String	N	18	
# -OVTM_UNTP_MXPR	시간외 단일가 상한가	String	N	18	
# -OVTM_UNTP_LLAM	시간외 단일가 하한가	String	N	18	
# -OVTM_UNTP_OPRC	시간외 단일가 시가2	String	N	10	
# -OVTM_UNTP_HGPR	시간외 단일가 최고가	String	N	10	
# -OVTM_UNTP_LWPR	시간외 단일가 최저가	String	N	10	
# -OVTM_UNTP_ANTC_CNPR	시간외 단일가 예상 체결가	String	N	10	
# -OVTM_UNTP_ANTC_CNTG_VRSS	시간외 단일가 예상 체결 대비	String	N	10	
# -OVTM_UNTP_ANTC_CNTG_VRSS_SIGN	시간외 단일가 예상 체결 대비	String	N	1	
# -OVTM_UNTP_ANTC_CNTG_CTRT	시간외 단일가 예상 체결 대비율	String	N	11	
# -OVTM_UNTP_ANTC_VOL	시간외 단일가 예상 거래량	String	N	18	
# -UPLM_SIGN	상한 부호	String	N	1	
# -LSLM_SIGN	하한 부호	String	N	1	
    ovtm_untp_prpr: int
    '''시간외 단일가 현재가'''
    ovtm_untp_prdy_vrss: int
    '''시간외 단일가 전일 대비'''
    ovtm_untp_prdy_vrss_sign: str
    '''시간외 단일가 전일 대비 부호'''
    ovtm_untp_prdy_ctrt: float
    '''시간외 단일가 전일 대비율'''
    ovtm_untp_vol: int
    '''시간외 단일가 거래량'''
    ovtm_untp_tr_pbmn: int
    '''시간외 단일가 거래 대금'''
    ovtm_untp_mxpr: int
    '''시간외 단일가 상한가'''
    ovtm_untp_llam: int
    '''시간외 단일가 하한가'''
    ovtm_untp_oprc: int
    '''시간외 단일가 시가'''
    ovtm_untp_hgpr: int
    '''시간외 단일가 최고가'''
    ovtm_untp_lwpr: int
    '''시간외 단일가 최저가'''
    ovtm_untp_antc_cnpr: int
    '''시간외 단일가 예상 체결가'''
    ovtm_untp_antc_cntg_vrss: int
    '''시간외 단일가 예상 체결 대비'''
    ovtm_untp_antc_cntg_vrss_sign: str
    '''시간외 단일가 예상 체결 대비 부호'''
    ovtm_untp_antc_cntg_ctrt: float
    '''시간외 단일가 예상 체결 대비율'''
    ovtm_untp_antc_vol: int
    '''시간외 단일가 예상 거래량'''
    uplm_sign: str
    '''상한 부호'''
    lslm_sign: str
    '''하한 부호'''
    

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        self.concludes = [KisStockOvertimeConclude(d) for d in data['output2']]
