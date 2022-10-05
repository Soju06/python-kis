from ...._import import *

class KisStockPrice(KisDynamicAPIResponse):
    '''주식현재가'''
    iscd_stat_cls_code: str
    '''종목 상태 구분 코드'''
    marg_rate: float
    '''증거금 비율'''
    rprs_mrkt_kor_name: str
    '''대표시장 한글명'''
    new_hgpr_lwpr_cls_code: str
    '''신 고가 저가 구분 코드'''
    bstp_kor_isnm: str
    '''업종 한글 종목명'''
    temp_stop_yn: bool
    '''임시 정지 여부'''
    oprc_rang_cont_yn: bool
    '''시가 범위 연장 여부'''
    clpr_rang_cont_yn: bool
    '''종가 범위 연장 여부'''
    crdt_able_yn: bool
    '''신용 가능 여부'''
    grmn_rate_cls_code: str
    '''보증금 비율 구분 코드'''
    elw_pblc_yn: bool
    '''ELW 발행 여부'''
    stck_prpr: int
    '''주식 현재가'''
    prdy_vrss: int
    '''전일 대비'''
    prdy_vrss_sign: int
    '''전일 대비 부호'''
    prdy_ctrt: float
    '''전일 대비율'''
    acml_tr_pbmn: int
    '''누적 거래 대금'''
    acml_vol: int
    '''누적 거래량'''
    prdy_vrss_vol_rate: float
    '''전일 대비 거래량 비율'''
    stck_oprc: int
    '''주식 시가'''
    stck_hgpr: int
    '''주식 최고가'''
    stck_lwpr: int
    '''주식 최저가'''
    stck_mxpr: int
    '''주식 상한가'''
    stck_llam: int
    '''주식 하한가'''
    stck_sdpr: int
    '''주식 기준가'''
    wghn_avrg_stck_prc: float
    '''가중 평균 주식 가격'''
    hts_frgn_ehrt: float
    '''HTS 외국인 소진율'''
    frgn_ntby_qty: int
    '''외국인 순매수 수량'''
    pgtr_ntby_qty: int
    '''프로그램매매 순매수 수량'''
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
    dmrs_val: int
    '''디저항 값'''
    dmsp_val: int
    '''디지지 값'''
    cpfn: int
    '''자본금'''
    rstc_wdth_prc: int
    '''제한 폭 가격'''
    stck_fcam: float
    '''주식 액면가'''
    stck_sspr: int
    '''주식 대용가'''
    aspr_unit: int
    '''호가단위'''
    hts_deal_qty_unit_val: int
    '''HTS 매매 수량 단위 값'''
    lstn_stcn: int
    '''상장 주수'''
    hts_avls: int
    '''HTS 시가총액'''
    per: float
    '''PER'''
    pbr: float
    '''PBR'''
    stac_month: int
    '''결산 월'''
    vol_tnrt: float
    '''거래량 회전율'''
    eps: float
    '''EPS'''
    bps: float
    '''BPS'''
    d250_hgpr: int
    '''250일 최고가'''
    d250_hgpr_date: datetime
    '''250일 최고가 일자'''
    d250_hgpr_vrss_prpr_rate: float
    '''250일 최고가 대비 현재가 비율'''
    d250_lwpr: int
    '''250일 최저가'''
    d250_lwpr_date: datetime
    '''250일 최저가 일자'''
    d250_lwpr_vrss_prpr_rate: float
    '''250일 최저가 대비 현재가 비율'''
    stck_dryy_hgpr: int
    '''주식 연중 최고가'''
    dryy_hgpr_vrss_prpr_rate: float
    '''연중 최고가 대비 현재가 비율'''
    dryy_hgpr_date: datetime
    '''연중 최고가 일자'''
    stck_dryy_lwpr: int
    '''주식 연중 최저가'''
    dryy_lwpr_vrss_prpr_rate: float
    '''연중 최저가 대비 현재가 비율'''
    dryy_lwpr_date: datetime
    '''연중 최저가 일자'''
    w52_hgpr: int
    '''52주일 최고가'''
    w52_hgpr_vrss_prpr_ctr: float
    '''52주일 최고가 대비 현재가 대비'''
    w52_hgpr_date: datetime
    '''52주일 최고가 일자'''
    w52_lwpr: int
    '''52주일 최저가'''
    w52_lwpr_vrss_prpr_ctr: float
    '''52주일 최저가 대비 현재가 대비'''
    w52_lwpr_date: datetime
    '''52주일 최저가 일자'''
    whol_loan_rmnd_rate: float
    '''전체 융자 잔고 비율'''
    ssts_yn: bool
    '''공매도가능여부'''
    stck_shrn_iscd: str
    '''주식 단축 종목코드'''
    fcam_cnnm: str
    '''액면가 통화명'''
    cpfn_cnnm: str
    '''자본금 통화명'''
    apprch_rate: float
    '''접근도'''
    frgn_hldn_qty: int
    '''외국인 보유 수량'''
    vi_cls_code: str
    '''VI적용구분코드'''
    ovtm_vi_cls_code: str
    '''시간외단일가VI적용구분코드'''
    last_ssts_cntg_qty: int
    '''최종 공매도 체결 수량'''
    invt_caful_yn: bool
    '''투자유의여부'''
    mrkt_warn_cls_code: str
    '''시장경고코드'''
    short_over_yn: bool
    '''단기과열여부'''
