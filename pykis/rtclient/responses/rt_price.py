
from datetime import datetime, time
from typing import Literal

from ..messaging import KisRTResponse

# MKSC_SHRN_ISCD	유가증권 단축 종목코드	String	Y	9	
# STCK_CNTG_HOUR	주식 체결 시간	String	Y	6	
# STCK_PRPR	주식 현재가	Number	Y	4	
# PRDY_VRSS_SIGN	전일 대비 부호	String	Y	1	1 : 상한
# 2 : 상승
# 3 : 보합
# 4 : 하한
# 5 : 하락
# PRDY_VRSS	전일 대비	Number	Y	4	
# PRDY_CTRT	전일 대비율	Number	Y	8	
# WGHN_AVRG_STCK_PRC	가중 평균 주식 가격	Number	Y	8	
# STCK_OPRC	주식 시가	Number	Y	4	
# STCK_HGPR	주식 최고가	Number	Y	4	
# STCK_LWPR	주식 최저가	Number	Y	4	
# ASKP1	매도호가1	Number	Y	4	
# BIDP1	매수호가1	Number	Y	4	
# CNTG_VOL	체결 거래량	Number	Y	8	
# ACML_VOL	누적 거래량	Number	Y	8	
# ACML_TR_PBMN	누적 거래 대금	Number	Y	8	
# SELN_CNTG_CSNU	매도 체결 건수	Number	Y	4	
# SHNU_CNTG_CSNU	매수 체결 건수	Number	Y	4	
# NTBY_CNTG_CSNU	순매수 체결 건수	Number	Y	4	
# CTTR	체결강도	Number	Y	8	
# SELN_CNTG_SMTN	총 매도 수량	Number	Y	8	
# SHNU_CNTG_SMTN	총 매수 수량	Number	Y	8	
# CCLD_DVSN	체결구분	String	Y	1	
# SHNU_RATE	매수비율	Number	Y	8	
# PRDY_VOL_VRSS_ACML_VOL_RATE	전일 거래량 대비 등락율	Number	Y	8	
# OPRC_HOUR	시가 시간	String	Y	6	
# OPRC_VRSS_PRPR_SIGN	시가대비구분	String	Y	1	1 : 상한
# 2 : 상승
# 3 : 보합
# 4 : 하한
# 5 : 하락
# OPRC_VRSS_PRPR	시가대비	Number	Y	4	
# HGPR_HOUR	최고가 시간	String	Y	6	
# HGPR_VRSS_PRPR_SIGN	고가대비구분	String	Y	1	1 : 상한
# 2 : 상승
# 3 : 보합
# 4 : 하한
# 5 : 하락
# HGPR_VRSS_PRPR	고가대비	Number	Y	4	
# LWPR_HOUR	최저가 시간	String	Y	6	
# LWPR_VRSS_PRPR_SIGN	저가대비구분	String	Y	1	1 : 상한
# 2 : 상승
# 3 : 보합
# 4 : 하한
# 5 : 하락
# LWPR_VRSS_PRPR	저가대비	Number	Y	4	
# BSOP_DATE	영업 일자	String	Y	8	
# NEW_MKOP_CLS_CODE	신 장운영 구분 코드	String	Y	2	(1) 첫 번째 비트
# 1 : 장개시전
# 2 : 장중
# 3 : 장종료후
# 4 : 시간외단일가
# 7 : 일반Buy-in
# 8 : 당일Buy-in

# (2) 두 번째 비트
# 0 : 보통
# 1 : 종가
# 2 : 대량
# 3 : 바스켓
# 7 : 정리매매
# 8 : Buy-in
# TRHT_YN	거래정지 여부	String	Y	1	Y : 정지
# N : 정상거래
# ASKP_RSQN1	매도호가 잔량1	Number	Y	8	
# BIDP_RSQN1	매수호가 잔량1	Number	Y	8	
# TOTAL_ASKP_RSQN	총 매도호가 잔량	Number	Y	8	
# TOTAL_BIDP_RSQN	총 매수호가 잔량	Number	Y	8	
# VOL_TNRT	거래량 회전율	Number	Y	8	
# PRDY_SMNS_HOUR_ACML_VOL	전일 동시간 누적 거래량	Number	Y	8	
# PRDY_SMNS_HOUR_ACML_VOL_RATE	전일 동시간 누적 거래량 비율	Number	Y	8	
# HOUR_CLS_CODE	시간 구분 코드	String	Y	1	0 : 장중
# A : 장후예상
# B : 장전예상
# C : 9시이후의 예상가
# D : 시간외 단일가 예상
# MRKT_TRTM_CLS_CODE	임의종료구분코드	String	Y	1	
# VI_STND_PRC	정적VI발동기준가	Number	Y	4	

VRSS_SIGNS = {
    '1': '상한',
    '2': '상승',
    '3': '보합',
    '4': '하한',
    '5': '하락',
}

NEW_MKOP_CLS_CODES_1 = {
    '1': '장개시전',
    '2': '장중',
    '3': '장종료후',
    '4': '시간외단일가',
    '7': '일반Buy-in',
    '8': '당일Buy-in',
}

NEW_MKOP_CLS_CODES_2 = {
    '0': '보통',
    '1': '종가',
    '2': '대량',
    '3': '바스켓',
    '7': '정리매매',
    '8': 'Buy-in',
}

HOUR_CLS_CODES = {
    '0': '장중',
    'A': '장후예상',
    'B': '장전예상',
    'C': '9시이후의 예상가',
    'D': '시간외 단일가 예상',
}

class KisRTPrice(KisRTResponse):
    '''주식 체결가'''
    mksc_shrn_iscd: str
    '''유가증권 단축 종목코드'''
    stck_cntg_hour: time
    '''주식 체결 시간'''
    stck_prpr: int
    '''주식 현재가'''
    prdy_vrss_sign: Literal['1', '2', '3', '4', '5']
    '''전일 대비 부호'''
    prdy_vrss: float
    '''전일 대비'''
    prdy_ctrt: float
    '''전일 대비율'''
    wghn_avrg_stck_prc: float
    '''가중 평균 주식 가격'''
    stck_oprc: int
    '''주식 시가'''
    stck_hgpr: int
    '''주식 최고가'''
    stck_lwpr: int
    '''주식 최저가'''
    askp1: int
    '''매도호가1'''
    bidp1: int
    '''매수호가1'''
    cntg_vol: int
    '''체결 거래량'''
    acml_vol: int
    '''누적 거래량'''
    acml_tr_pbmn: int
    '''누적 거래 대금'''
    seln_cntg_csnu: int
    '''매도 체결 건수'''
    shnu_cntg_csnu: int
    '''매수 체결 건수'''
    ntby_cntg_csnu: int
    '''순매수 체결 건수'''
    cttr: float
    '''체결강도'''
    seln_cntg_smt: int
    '''총 매도 수량'''
    shnu_cntg_smt: int
    '''총 매수 수량'''
    cccd_dvsn: str
    '''체결구분'''
    shnu_rate: float
    '''매수비율'''
    prdy_vol_vrss_acml_vol_rate: float
    '''전일 거래량 대비 등락율'''
    oprc_hour: time
    '''시가 시간'''
    oprc_vrss_prpr_sign: Literal['1', '2', '3', '4', '5']
    '''시가대비구분'''
    oprc_vrss_prpr: int
    '''시가대비'''
    hgpr_hour: time
    '''최고가 시간'''
    hgpr_vrss_prpr_sign: Literal['1', '2', '3', '4', '5']
    '''고가대비구분'''
    hgpr_vrss_prpr: float
    '''고가대비'''
    lwpr_hour: time
    '''최저가 시간'''
    lwpr_vrss_prpr_sign: Literal['1', '2', '3', '4', '5']
    '''저가대비구분'''
    lwpr_vrss_prpr: float
    '''저가대비'''
    bsop_date: datetime
    '''영업 일자'''
    new_mkop_cls_code: str
    '''신 장운영 구분 코드'''
    trht_yn: bool
    '''거래정지 여부'''
    askp_rsqn1: int
    '''매도호가 잔량1'''
    bidp_rsqn1: int
    '''매수호가 잔량1'''
    total_askp_rsqn: int
    '''총 매도호가 잔량'''
    total_bidp_rsqn: int
    '''총 매수호가 잔량'''
    vol_tnrt: float
    '''거래량 회전율'''
    prdy_smns_hour_acml_vol: int
    '''전일 동시간 누적 거래량'''
    prdy_smns_hour_acml_vol_rate: float
    '''전일 동시간 누적 거래량 비율'''
    hour_cls_code: Literal['0', 'A', 'B', 'C', 'D']
    '''시간 구분 코드'''
    mrkt_trtm_cls_code: str
    '''임의종료구분코드'''
    vi_stnd_prc: int
    '''정적VI발동기준가'''

    @property
    def prdy_vrss_sign_name(self) -> str | None:
        return VRSS_SIGNS.get(self.prdy_vrss_sign, None)

    @property
    def oprc_vrss_prpr_sign_name(self) -> str | None:
        return VRSS_SIGNS.get(self.oprc_vrss_prpr_sign, None)

    @property
    def hgpr_vrss_prpr_sign_name(self) -> str | None:
        return VRSS_SIGNS.get(self.hgpr_vrss_prpr_sign, None)
    
    @property
    def lwpr_vrss_prpr_sign_name(self) -> str | None:
        return VRSS_SIGNS.get(self.lwpr_vrss_prpr_sign, None)

    @property
    def new_mkop_cls_code_1_name(self) -> str | None:
        if len(self.new_mkop_cls_code) < 1: return None
        return NEW_MKOP_CLS_CODES_1.get(self.new_mkop_cls_code[0], None)

    @property
    def new_mkop_cls_code_2_name(self) -> str | None:
        if len(self.new_mkop_cls_code) < 2: return None
        return NEW_MKOP_CLS_CODES_2.get(self.new_mkop_cls_code[1], None)
    
    def __init__(self, data: str, parse: bool = True):
        super().__init__(data, parse)
