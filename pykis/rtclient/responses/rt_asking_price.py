
from datetime import time
from typing import Literal

from .rt_price import VRSS_SIGNS
from ..messaging import KisRTResponse

# MKSC_SHRN_ISCD	유가증권 단축 종목코드	String	Y	9	
# BSOP_HOUR	영업 시간	String	Y	6	
# HOUR_CLS_CODE	시간 구분 코드	String	Y	1	
# ASKP1	매도호가1	Number	Y	4	
# ASKP2	매도호가2	Number	Y	4	
# ASKP3	매도호가3	Number	Y	4	
# ASKP4	매도호가4	Number	Y	4	
# ASKP5	매도호가5	Number	Y	4	
# ASKP6	매도호가6	Number	Y	4	
# ASKP7	매도호가7	Number	Y	4	
# ASKP8	매도호가8	Number	Y	4	
# ASKP9	매도호가9	Number	Y	4	
# ASKP10	매도호가10	Number	Y	4	
# BIDP1	매수호가1	Number	Y	4	
# BIDP2	매수호가2	Number	Y	4	
# BIDP3	매수호가3	Number	Y	4	
# BIDP4	매수호가4	Number	Y	4	
# BIDP5	매수호가5	Number	Y	4	
# BIDP6	매수호가6	Number	Y	4	
# BIDP7	매수호가7	Number	Y	4	
# BIDP8	매수호가8	Number	Y	4	
# BIDP9	매수호가9	Number	Y	4	
# BIDP10	매수호가10	Number	Y	4	
# ASKP_RSQN1	매도호가 잔량1	Number	Y	8	
# ASKP_RSQN2	매도호가 잔량2	Number	Y	8	
# ASKP_RSQN3	매도호가 잔량3	Number	Y	8	
# ASKP_RSQN4	매도호가 잔량4	Number	Y	8	
# ASKP_RSQN5	매도호가 잔량5	Number	Y	8	
# ASKP_RSQN6	매도호가 잔량6	Number	Y	8	
# ASKP_RSQN7	매도호가 잔량7	Number	Y	8	
# ASKP_RSQN8	매도호가 잔량8	Number	Y	8	
# ASKP_RSQN9	매도호가 잔량9	Number	Y	8	
# ASKP_RSQN10	매도호가 잔량10	Number	Y	8	
# BIDP_RSQN1	매수호가 잔량1	Number	Y	8	
# BIDP_RSQN2	매수호가 잔량2	Number	Y	8	
# BIDP_RSQN3	매수호가 잔량3	Number	Y	8	
# BIDP_RSQN4	매수호가 잔량4	Number	Y	8	
# BIDP_RSQN5	매수호가 잔량5	Number	Y	8	
# BIDP_RSQN6	매수호가 잔량6	Number	Y	8	
# BIDP_RSQN7	매수호가 잔량7	Number	Y	8	
# BIDP_RSQN8	매수호가 잔량8	Number	Y	8	
# BIDP_RSQN9	매수호가 잔량9	Number	Y	8	
# BIDP_RSQN10	매수호가 잔량10	Number	Y	8	
# TOTAL_ASKP_RSQN	총 매도호가 잔량	Number	Y	8	
# TOTAL_BIDP_RSQN	총 매수호가 잔량	Number	Y	8	
# OVTM_TOTAL_ASKP_RSQN	시간외 총 매도호가 잔량	Number	Y	8	
# OVTM_TOTAL_BIDP_RSQN	시간외 총 매수호가 잔량	Number	Y	8	
# ANTC_CNPR	예상 체결가	Number	Y	4	
# ANTC_CNQN	예상 체결량	Number	Y	8	
# ANTC_VOL	예상 거래량	Number	Y	8	
# ANTC_CNTG_VRSS	예상 체결 대비	Number	Y	4	
# ANTC_CNTG_VRSS_SIGN	예상 체결 대비 부호	String	Y	1	1 : 상한
# 2 : 상승
# 3 : 보합
# 4 : 하한
# 5 : 하락
# ANTC_CNTG_PRDY_CTRT	예상 체결 전일 대비율	Number	Y	8	
# ACML_VOL	누적 거래량	Number	Y	8	
# TOTAL_ASKP_RSQN_ICDC	총 매도호가 잔량 증감	Number	Y	4	
# TOTAL_BIDP_RSQN_ICDC	총 매수호가 잔량 증감	Number	Y	4	
# OVTM_TOTAL_ASKP_ICDC	시간외 총 매도호가 증감	Number	Y	4	
# OVTM_TOTAL_BIDP_ICDC	시간외 총 매수호가 증감	Number	Y	4	
# STCK_DEAL_CLS_CODE	주식 매매 구분 코드	String	Y	2	

class KisRTAskingPrice(KisRTResponse):
    '''실시간 호가 정보'''
    mksc_shrn_iscd: str
    '''유가증권 단축 종목코드'''
    bsop_hour: time
    '''영업 시간'''
    hour_cls_code: str
    '''시간 구분 코드'''
    askp1: int
    '''매도호가1'''
    askp2: int
    '''매도호가2'''
    askp3: int
    '''매도호가3'''
    askp4: int
    '''매도호가4'''
    askp5: int
    '''매도호가5'''
    askp6: int
    '''매도호가6'''
    askp7: int
    '''매도호가7'''
    askp8: int
    '''매도호가8'''
    askp9: int
    '''매도호가9'''
    askp10: int
    '''매도호가10'''
    bidp1: int
    '''매수호가1'''
    bidp2: int
    '''매수호가2'''
    bidp3: int
    '''매수호가3'''
    bidp4: int
    '''매수호가4'''
    bidp5: int
    '''매수호가5'''
    bidp6: int
    '''매수호가6'''
    bidp7: int
    '''매수호가7'''
    bidp8: int
    '''매수호가8'''
    bidp9: int
    '''매수호가9'''
    bidp10: int
    '''매수호가10'''
    askp_rsqn1: int
    '''매도호가 잔량1'''
    askp_rsqn2: int
    '''매도호가 잔량2'''
    askp_rsqn3: int
    '''매도호가 잔량3'''
    askp_rsqn4: int
    '''매도호가 잔량4'''
    askp_rsqn5: int
    '''매도호가 잔량5'''
    askp_rsqn6: int
    '''매도호가 잔량6'''
    askp_rsqn7: int
    '''매도호가 잔량7'''
    askp_rsqn8: int
    '''매도호가 잔량8'''
    askp_rsqn9: int
    '''매도호가 잔량9'''
    askp_rsqn10: int
    '''매도호가 잔량10'''
    bidp_rsqn1: int
    '''매수호가 잔량1'''
    bidp_rsqn2: int
    '''매수호가 잔량2'''
    bidp_rsqn3: int
    '''매수호가 잔량3'''
    bidp_rsqn4: int
    '''매수호가 잔량4'''
    bidp_rsqn5: int
    '''매수호가 잔량5'''
    bidp_rsqn6: int
    '''매수호가 잔량6'''
    bidp_rsqn7: int
    '''매수호가 잔량7'''
    bidp_rsqn8: int
    '''매수호가 잔량8'''
    bidp_rsqn9: int
    '''매수호가 잔량9'''
    bidp_rsqn10: int
    '''매수호가 잔량10'''
    total_askp_rsqn: int
    '''총 매도호가 잔량'''
    total_bidp_rsqn: int
    '''총 매수호가 잔량'''
    ovtm_total_askp_rsqn: int
    '''시간외 총 매도호가 잔량'''
    ovtm_total_bidp_rsqn: int
    '''시간외 총 매수호가 잔량'''
    antc_cnpr: int
    '''예상 체결가'''
    antc_cnqn: int
    '''예상 체결량'''
    antc_vol: int
    '''예상 거래량'''
    antc_cntg_vrss: int
    '''예상 체결 대비'''
    antc_cntg_vrss_sign: Literal['1', '2', '3', '4', '5']
    '''예상 체결 대비 부호'''
    antc_cntg_prdy_ctrt: float
    '''예상 체결 전일 대비율'''
    acml_vol: int
    '''누적 거래량'''
    total_askp_rsqn_icdc: int
    '''총 매도호가 잔량 증감'''
    total_bidp_rsqn_icdc: int
    '''총 매수호가 잔량 증감'''
    ovtm_total_askp_icdc: int
    '''시간외 총 매도호가 증감'''
    ovtm_total_bidp_icdc: int
    '''시간외 총 매수호가 증감'''
    stck_deal_cls_code: str
    '''주식 매매 구분 코드'''
    
    @property
    def antc_cntg_vrss_name(self) -> str | None:
        return VRSS_SIGNS.get(self.antc_cntg_vrss_sign, None)
    
    def __init__(self, data: str, parse: bool = True):
        super().__init__(data, parse)
