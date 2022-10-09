from ...._import import *

class KisStockPeriodPrice(KisDynamic):
# -STCK_BSOP_DATE	주식 영업 일자	String	Y	8	주식 영업 일자
# -STCK_CLPR	주식 종가	String	Y	10	주식 종가
# -STCK_OPRC	주식 시가	String	Y	10	주식 시가
# -STCK_HGPR	주식 최고가	String	Y	10	주식 최고가
# -STCK_LWPR	주식 최저가	String	Y	10	주식 최저가
# -ACML_VOL	누적 거래량	String	Y	18	누적 거래량
# -ACML_TR_PBMN	누적 거래 대금	String	Y	18	누적 거래 대금
# -FLNG_CLS_CODE	락 구분 코드	String	Y	2	00:해당사항없음(락이 발생안한 경우)
# 01:권리락
# 02:배당락
# 03:분배락
# 04:권배락
# 05:중간(분기)배당락
# 06:권리중간배당락
# 07:권리분기배당락
# -PRTT_RATE	분할 비율	String	Y	11	분할 비율
# -MOD_YN	분할변경여부	String	Y	1	Y, N
# -PRDY_VRSS_SIGN	전일 대비 부호	String	Y	1	전일 대비 부호
# -PRDY_VRSS	전일 대비	String	Y	10	전일 대비
# -REVL_ISSU_REAS	재평가사유코드	String	Y	2	재평가사유코드
    stck_bsop_date: datetime
    '''주식 영업 일자'''
    stck_clpr: int
    '''주식 종가'''
    stck_oprc: int
    '''주식 시가'''
    stck_hgpr: int
    '''주식 최고가'''
    stck_lwpr: int
    '''주식 최저가'''
    acml_vol: int
    '''누적 거래량'''
    acml_tr_pbmn: int
    '''누적 거래 대금'''
    flng_cls_code: str
    '''락 구분 코드'''
    prtt_rate: float
    '''분할 비율'''
    mod_yn: bool
    '''분할변경여부'''
    prdy_vrss_sign: str
    '''전일 대비 부호'''
    prdy_vrss: int
    '''전일 대비'''
    revl_issu_reas: str
    '''재평가사유코드'''

    def __init__(self, data: dict):
        super().__init__(data)


class KisStockPeriodPrices(KisDynamicAPIResponse):
# PRDY_VRSS	전일 대비	String	Y	10	전일 대비
# PRDY_VRSS_SIGN	전일 대비 부호	String	Y	1	전일 대비 부호
# PRDY_CTRT	전일 대비율	String	Y	11	전일 대비율
# STCK_PRDY_CLPR	주식 전일 종가	String	Y	10	주식 전일 종가
# ACML_VOL	누적 거래량	String	Y	18	누적 거래량
# ACML_TR_PBMN	누적 거래 대금	String	Y	18	누적 거래 대금
# HTS_KOR_ISNM	HTS 한글 종목명	String	Y	40	HTS 한글 종목명
# STCK_PRPR	주식 현재가	String	Y	10	주식 현재가
# STCK_SHRN_ISCD	주식 단축 종목코드	String	Y	9	주식 단축 종목코드
# PRDY_VOL	전일 거래량	String	Y	18	전일 거래량
# STCK_MXPR	상한가	String	Y	10	상한가
# STCK_LLAM	하한가	String	Y	10	하한가
# STCK_OPRC	시가	String	Y	10	시가
# STCK_HGPR	최고가	String	Y	10	최고가
# STCK_LWPR	최저가	String	Y	10	최저가
# STCK_PRDY_OPRC	주식 전일 시가	String	Y	10	주식 전일 시가
# STCK_PRDY_HGPR	주식 전일 최고가	String	Y	10	주식 전일 최고가
# STCK_PRDY_LWPR	주식 전일 최저가	String	Y	10	주식 전일 최저가
# ASKP	매도호가	String	Y	10	매도호가
# BIDP	매수호가	String	Y	10	매수호가
# PRDY_VRSS_VOL	전일 대비 거래량	String	Y	10	전일 대비 거래량
# VOL_TNRT	거래량 회전율	String	Y	11	거래량 회전율
# STCK_FCAM	주식 액면가	String	Y	11	주식 액면가
# LSTN_STCN	상장 주수	String	Y	18	상장 주수
# CPFN	자본금	String	Y	22	자본금
# HTS_AVLS	시가총액	String	Y	18	HTS 시가총액
# PER	PER	String	Y	11	PER
# EPS	EPS	String	Y	14	EPS
# PBR	PBR	String	Y	11	PBR
# ITEWHOL_LOAN_RMND_RATEM NAME	전체 융자 잔고 비율	String	Y	13	전체 융자 잔고 비율    
    prdy_vrss: int
    '''전일 대비'''
    prdy_vrss_sign: str
    '''전일 대비 부호'''
    prdy_ctrt: float
    '''전일 대비율'''
    stck_prdy_clpr: int
    '''주식 전일 종가'''
    acml_vol: int
    '''누적 거래량'''
    acml_tr_pbmn: int
    '''누적 거래 대금'''
    hts_kor_isnm: str
    '''HTS 한글 종목명'''
    stck_prpr: int
    '''주식 현재가'''
    stck_shrn_iscd: str
    '''주식 단축 종목코드'''
    prdy_vol: int
    '''전일 거래량'''
    stck_mxpr: int
    '''상한가'''
    stck_llam: int
    '''하한가'''
    stck_oprc: int
    '''시가'''
    stck_hgpr: int
    '''최고가'''
    stck_lwpr: int
    '''최저가'''
    stck_prdy_oprc: int
    '''주식 전일 시가'''
    stck_prdy_hgpr: int
    '''주식 전일 최고가'''
    stck_prdy_lwpr: int
    '''주식 전일 최저가'''
    askp: int
    '''매도호가'''
    bidp: int
    '''매수호가'''
    prdy_vrss_vol: int
    '''전일 대비 거래량'''
    vol_tnrt: float
    '''거래량 회전율'''
    stck_fcam: float
    '''주식 액면가'''
    lstn_stcn: int
    '''상장 주수'''
    cpfn: int
    '''자본금'''
    hts_avls: int
    '''시가총액'''
    per: float
    '''PER'''
    eps: float
    '''EPS'''
    pbr: float
    '''PBR'''
    itewhol_loan_rmnd_ratem_name: float
    '''전체 융자 잔고 비율'''
    prices: list[KisStockPeriodPrice]
    '''주식 일별 가격 정보'''

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        self.prices = [KisStockPeriodPrice(price) for price in data['output2']]
