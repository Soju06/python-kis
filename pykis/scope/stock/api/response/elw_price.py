from ...._import import *

class KisELWPrice(KisDynamicAPIResponse):
# -ELW_SHRN_ISCD	ELW 단축 종목코드	String	Y	9	
# -HTS_KOR_ISNM	HTS 한글 종목명	String	Y	40	
# -ELW_PRPR	ELW 현재가	String	Y	10	
# -PRDY_VRSS	전일 대비	String	Y	10	
# -PRDY_VRSS_SIGN	전일 대비 부호	String	Y	1	
# -PRDY_CTRT	전일 대비율	String	Y	10	
# -ACML_VOL	누적 거래량	String	Y	18	
# -PRDY_VRSS_VOL_RATE	전일 대비 거래량 비율	String	Y	12	
# -UNAS_SHRN_ISCD	기초자산 단축 종목코드	String	Y	9	
# -UNAS_ISNM	기초자산 종목명	String	Y	40	
# -UNAS_PRPR	기초자산 현재가	String	Y	13	
# -UNAS_PRDY_VRSS	기초자산 전일 대비	String	Y	13	
# -UNAS_PRDY_VRSS_SIGN	기초자산 전일 대비 부호	String	Y	1	
# -UNAS_PRDY_CTRT	기초자산 전일 대비율	String	Y	10	
# -BIDP	매수호가	String	Y	10	
# -ASKP	매도호가	String	Y	10	
# -ACML_TR_PBMN	누적 거래 대금	String	Y	18	
# -VOL_TNRT	거래량 회전율	String	Y	10	
# -ELW_OPRC	ELW 시가2	String	Y	10	
# -ELW_HGPR	ELW 최고가	String	Y	10	
# -ELW_LWPR	ELW 최저가	String	Y	10	
# -STCK_PRDY_CLPR	주식 전일 종가	String	Y	10	
# -HTS_THPR	HTS 이론가	String	Y	13	
# -DPRT	괴리율	String	Y	10	
# -ATM_CLS_NAME	ATM 구분 명	String	Y	10	
# -HTS_INTS_VLTL	HTS 내재 변동성	String	Y	15	
# -ACPR	행사가	String	Y	13	
# -PVT_SCND_DMRS_PRC	피벗 2차 디저항 가격	String	Y	10	
# -PVT_FRST_DMRS_PRC	피벗 1차 디저항 가격	String	Y	10	
# -PVT_PONT_VAL	피벗 포인트 값	String	Y	10	
# -PVT_FRST_DMSP_PRC	피벗 1차 디지지 가격	String	Y	10	
# -PVT_SCND_DMSP_PRC	피벗 2차 디지지 가격	String	Y	10	
# -DMSP_VAL	디지지 값	String	Y	10	
# -DMRS_VAL	디저항 값	String	Y	10	
# -ELW_SDPR	ELW 기준가	String	Y	10	
# -APPRCH_RATE	접근도	String	Y	13	
# -TICK_CONV_PRC	틱환산가	String	Y	11	
# -INVT_EPMD_CNTT	투자 유의 내용	String	Y	200	
    elw_shrn_iscd: str
    '''ELW 단축 종목코드'''
    hts_kor_isnm: str
    '''HTS 한글 종목명'''
    elw_prpr: int
    '''ELW 현재가'''
    prdy_vrss: int
    '''전일 대비'''
    prdy_vrss_sign: str
    '''전일 대비 부호'''
    prdy_ctrct: float
    '''전일 대비율'''
    acml_vol: int
    '''누적 거래량'''
    prdy_vrss_vol_rate: float
    '''전일 대비 거래량 비율'''
    unas_shrn_iscd: str
    '''기초자산 단축 종목코드'''
    unas_isnm: str
    '''기초자산 종목명'''
    unas_prpr: float
    '''기초자산 현재가'''
    unas_prdy_vrss: float
    '''기초자산 전일 대비'''
    unas_prdy_vrss_sign: str
    '''기초자산 전일 대비 부호'''
    unas_prdy_ctrt: float
    '''기초자산 전일 대비율'''
    bidp: int
    '''매수호가'''
    askp: int
    '''매도호가'''
    acml_tr_pbmn: int
    '''누적 거래 대금'''
    vol_tnrt: float
    '''거래량 회전율'''
    elw_oprc: int
    '''ELW 시가2'''
    elw_hgpr: int
    '''ELW 최고가'''
    elw_lwpr: int
    '''ELW 최저가'''
    stck_prdy_clpr: int
    '''주식 전일 종가'''
    hts_thpr: float
    '''HTS 이론가'''
    dprt: float
    '''괴리율'''
    atm_cls_name: str
    '''ATM 구분 명'''
    hts_ints_vltl: float
    '''HTS 내재 변동성'''
    acpr: float
    '''행사가'''
    pvt_scnd_dmrs_prc: int
    '''피벗 2차 디저항 가격'''
    pvt_frst_dmrs_prc: int
    '''피벗 1차 디저항 가격'''
    pvt_pont_val: int
    '''피벗 포인트 값'''
    pvt_frst_dmsp_prc: int
    '''피벗 1차 디지지 가격'''
    pvt_scnd_dmsp_prc: int
    '''피벗 2차 디지지 가격'''
    dmsp_val: int
    '''디지지 값'''
    dmrs_val: int
    '''디저항 값'''
    elw_sdpr: int
    '''ELW 기준가'''
    apprch_rate: float
    '''접근도'''
    tick_conv_prc: float
    '''틱환산가'''
    invt_epmd_cntt: str
    '''투자 유의 내용'''
