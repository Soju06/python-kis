from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Iterator, Literal
from sqlalchemy import Column, Integer, String, Date, Boolean, Float

from .db import Base
from .kstock import KisKStockMarket, KisKStockItem

if TYPE_CHECKING:
    from .client import KisMarketClient

APNT_CLS_CODES = {
    '0': '미분류',
    '1': '건설기계',
    '2': '조선운송',
    '3': '철강소재',
    '4': '에너지화학',
    '5': '정보통신',
    '6': '금융',
    '7': '필수소비재',
    '8': '자유소비재',
}

# typedef struct
# {
#     char    mksc_shrn_iscd[9];        /* 단축코드                                     */
#     char    stnd_iscd[12];             /* 표준코드                                     */
#     char    hts_kor_isnm[N];           /* 한글종목명                                   */
#     char    scrt_grp_cls_code[2];               /* 증권그룹구분코드                             */
#                                                 /* ST:주권 MF:증권투자회사 RT:부동산투자회사    */
#                                                 /* SC:선박투자회사 IF:사회간접자본투융자회사    */
#                                                 /* DR:주식예탁증서 EW:ELW EF:ETF                */
#                                                 /* SW:신주인수권증권 SR:신주인수권증서          */
#                                                 /* BC:수익증권 FE:해외ETF FS:외국주권           */
# 	char    avls_scal_cls_code[1];              /* 시가총액 규모 구분 코드 유가                 */
# 												/* (0:제외 1:대 2:중 3:소)                      */
#     char    bstp_larg_div_code[4];              /* 지수 업종 대분류 코드                        */
#     char    bstp_medm_div_code[4];              /* 지수 업종 중분류 코드                        */
#     char    bstp_smal_div_code[4];              /* 지수 업종 소분류 코드                        */
#     char    mnin_cls_code_yn[1];                /* 제조업 구분 코드 (Y/N)                       */
#     char    low_current_yn[1];               	/* 저유동성종목 여부 							*/
#     char    sprn_strr_nmix_issu_yn[1];          /* 지배 구조 지수 종목 여부 (Y/N)               */
#     char    kospi200_apnt_cls_code[1];          /* KOSPI200 섹터업종(20110401 변경됨) 			*/
#                                                 /* 0:미분류 1:건설기계 2:조선운송 3:철강소재 	*/
# 												/* 4:에너지화학 5:정보통신 6:금융 7:필수소비재 	*/
# 												/* 8: 자유소비재                                */
#     char    kospi100_issu_yn[1];                /* KOSPI100여부                                 */
#     char    kospi50_issu_yn[1];                 /* KOSPI50 종목 여부                            */
#     char    krx_issu_yn[1];                     /* KRX 종목 여부                                */
#     char    etp_prod_cls_code[1];            	/* ETP 상품구분코드								*/
# 												/* 0:해당없음 1:투자회사형 2:수익증권형			*/
# 												/* 3:ETN 4:손실제한ETN							*/
#     char    elw_pblc_yn[1];                     /* ELW 발행여부 (Y/N)                           */
#     char    krx100_issu_yn[1];                  /* KRX100 종목 여부 (Y/N)                       */
#     char    krx_car_yn[1];                      /* KRX 자동차 여부                              */
#     char    krx_smcn_yn[1];                     /* KRX 반도체 여부                              */
#     char    krx_bio_yn[1];                      /* KRX 바이오 여부                              */
#     char    krx_bank_yn[1];                     /* KRX 은행 여부                                */
#     char    etpr_undt_objt_co_yn[1];            /* 기업인수목적회사여부 						*/
#     char    krx_enrg_chms_yn[1];                /* KRX 에너지 화학 여부                         */
#     char    krx_stel_yn[1];                     /* KRX 철강 여부                                */
#     char    short_over_cls_code[1];             /* 단기과열종목구분코드 0:해당없음              */
#                                                 /* 1:지정예고 2:지정 3:지정연장(해제연기)       */
#     char    krx_medi_cmnc_yn[1];                /* KRX 미디어 통신 여부                         */
#     char    krx_cnst_yn[1];                     /* KRX 건설 여부                                */
#     char    krx_fnnc_svc_yn[1];                 /* 삭제됨(20151218)								*/
#     char    krx_scrt_yn [1];                    /* KRX 증권 구분                                */
#     char    krx_ship_yn [1];                    /* KRX 선박 구분                                */
#     char    krx_insu_yn[1];                     /* KRX섹터지수 보험여부                         */
#     char    krx_trnp_yn[1];                     /* KRX섹터지수 운송여부                         */
# 	char	sri_nmix_yn[1];                     /* SRI 지수여부 (Y,N)                           */
# 	char    stck_sdpr[9];                       /* 주식 기준가                                  */
#     char    frml_mrkt_deal_qty_unit[5];         /* 정규 시장 매매 수량 단위                     */
#     char    ovtm_mrkt_deal_qty_unit[5];         /* 시간외 시장 매매 수량 단위                   */
#     char    trht_yn[1];                         /* 거래정지 여부                                */
#     char    sltr_yn[1];                         /* 정리매매 여부                                */
#     char    mang_issu_yn[1];                    /* 관리 종목 여부                               */
#     char    mrkt_alrm_cls_code[2];              /* 시장 경고 구분 코드 (00:해당없음 01:투자주의 */
#                                                 /* 02:투자경고 03:투자위험                      */
# 	char    mrkt_alrm_risk_adnt_yn[1];          /* 시장 경고위험 예고 여부                      */
#     char    insn_pbnt_yn[1];                    /* 불성실 공시 여부                             */
#     char    byps_lstn_yn[1];                    /* 우회 상장 여부                               */
#     char    flng_cls_code[2];                   /* 락구분 코드 (00:해당사항없음 01:권리락       */
#                                                 /* 02:배당락 03:분배락 04:권배락 05:중간배당락  */
#                                                 /* 06:권리중간배당락 99:기타                    */
#                                                 /* S?W,SR,EW는 미해당(SPACE)                     */
#     char    fcam_mod_cls_code[2];               /* 액면가 변경 구분 코드 (00:해당없음           */
#                                                 /* 01:액면분할 02:액면병합 99:기타              */
#     char    icic_cls_code[2];                   /* 증자 구분 코드 (00:해당없음 01:유상증자      */
#                                                 /* 02:무상증자 03:유무상증자 99:기타)           */
#     char    marg_rate[3];                       /* 증거금 비율                                  */
#     char    crdt_able[1];                       /* 신용주문 가능 여부                           */
#     char    crdt_days[3];                       /* 신용기간                                     */
#     char    prdy_vol[12];                       /* 전일 거래량                                  */
#     char    stck_fcam[12];                      /* 주식 액면가                                  */
#     char    stck_lstn_date[8];                  /* 주식 상장 일자                               */
#     char    lstn_stcn[15];                      /* 상장 주수(천)                                */
#     char    cpfn[21];                           /* 자본금                                       */
#     char    stac_month[2];                      /* 결산 월                                      */
#     char    po_prc[7];                          /* 공모 가격                                    */
#     char    prst_cls_code[1];                   /* 우선주 구분 코드 (0:해당없음(보통주)         */
#                                                 /* 1:구형우선주 2:신형우선주                    */
#     char    ssts_hot_yn[1];                     /* 공매도과열종목여부  							*/
#     char    stange_runup_yn[1];                 /* 이상급등종목여부 							*/
#     char    krx300_issu_yn[1];                  /* KRX300 종목 여부 (Y/N)                       */
#     char    kospi_issu_yn[1];                   /* KOSPI여부                                    */
# 	char	sale_account[9];					/* 매출액                                       */
# 	char    bsop_prfi[9];						/* 영업이익                                     */
# 	char	op_prfi[9];							/* 경상이익                                     */
# 	char	thtr_ntin[5];						/* 당기순이익                                   */
# 	char	roe[9];								/* ROE(자기자본이익률)                          */
# 	char	base_date[8];						/* 기준년월                                     */
# 	char	prdy_avls_scal[9];					/* 전일기준 시가총액 (억)                       */

# 	char	grp_code[3];						/* 그룹사 코드                                  */
#     char    co_crdt_limt_over_yn[1];            /* 회사신용한도초과여부                         */
#     char    secu_lend_able_yn[1];               /* 담보대출가능여부                             */
#     char    stln_able_yn[1];                    /* 대주가능여부                                 */
# }   ST_KSP_CODE;

@dataclass
class KisKospiItem(KisKStockItem):
    CONTROL = [
        ('mksc_shrn_iscd', 9),
        ('stnd_iscd', 12),
        ('hts_kor_isnm', (9+12, -227)),
        ('_index', -1),
        ('_reverse', True),
        ('scrt_grp_cls_code', 2),
        ('avls_scal_cls_code', 1),
        ('bstp_larg_div_code', 4),
        ('bstp_medm_div_code', 4),
        ('bstp_smal_div_code', 4),
        ('mnin_cls_code_yn', 1),
        ('low_current_yn', 1),
        ('sprn_strr_nmix_issu_yn', 1),
        ('kospi200_apnt_cls_code', 1),
        ('kospi100_issu_yn', 1),
        ('kospi50_issu_yn', 1),
        ('krx_issu_yn', 1),
        ('etp_prod_cls_code', 1),
        ('elw_pblc_yn', 1),
        ('krx100_issu_yn', 1),
        ('krx_car_yn', 1),
        ('krx_smcn_yn', 1),
        ('krx_bio_yn', 1),
        ('krx_bank_yn', 1),
        ('etpr_undt_objt_co_yn', 1),
        ('krx_enrg_chms_yn', 1),
        ('krx_stel_yn', 1),
        ('short_over_cls_code', 1),
        ('krx_medi_cmnc_yn', 1),
        ('krx_cnst_yn', 1),
        ('_dummy', 1),
        ('krx_scrt_yn', 1),
        ('krx_ship_yn', 1),
        ('krx_insu_yn', 1),
        ('krx_trnp_yn', 1),
        ('sri_nmix_yn', 1),
        ('stck_sdpr', 9),
        ('frml_mrkt_deal_qty_unit', 5),
        ('ovtm_mrkt_deal_qty_unit', 5),
        ('trht_yn', 1),
        ('sltr_yn', 1),
        ('mang_issu_yn', 1),
        ('mrkt_alrm_cls_code', 2),
        ('mrkt_alrm_risk_adnt_yn', 1),
        ('insn_pbnt_yn', 1),
        ('byps_lstn_yn', 1),
        ('flng_cls_code', 2),
        ('fcam_mod_cls_code', 2),
        ('icic_cls_code', 2),
        ('marg_rate', 3),
        ('crdt_able', 1),
        ('crdt_days', 3),
        ('prdy_vol', 12),
        ('stck_fcam', 12),
        ('stck_lstn_date', 8),
        ('lstn_stcn', 15),
        ('cpfn', 21),
        ('stac_month', 2),
        ('po_prc', 7),
        ('prst_cls_code', 1),
        ('ssts_hot_yn', 1),
        ('stange_runup_yn', 1),
        ('krx300_issu_yn', 1),
        ('kospi_issu_yn', 1),
        ('sale_account', 9),
        ('bsop_prfi', 9),
        ('op_prfi', 9),
        ('thtr_ntin', 5),
        ('roe', 9),
        ('base_date', 8),
        ('prdy_avls_scal', 9),
        ('grp_code', 3),
        ('co_crdt_limt_over_yn', 1),
        ('secu_lend_able_yn', 1),
        ('stln_able_yn', 1),
    ]

    mksc_shrn_iscd: str
    '''단축코드'''
    stnd_iscd: str
    '''표준코드'''
    hts_kor_isnm: str
    '''한글종목명'''
    scrt_grp_cls_code: Literal['ST', 'MF', 'RT', 'SC', 'IF', 'DR', 'EW', 'EF', 'SW', 'SR', 'BC', 'FE', 'FS']
    '''증권그룹구분코드'''
    avls_scal_cls_code: Literal['0', '1', '2', '3']
    '''시가총액 규모 구분 코드 유가'''
    bstp_larg_div_code: str
    '''지수 업종 대분류 코드'''
    bstp_medm_div_code: str
    '''지수 업종 중분류 코드'''
    bstp_smal_div_code: str
    '''지수 업종 소분류 코드'''
    mnin_cls_code_yn: bool
    '''제조업 구분 코드'''
    low_current_yn: bool
    '''저유동성종목 여부'''
    sprn_strr_nmix_issu_yn: bool
    '''지배 구조 지수 종목 여부'''
    kospi200_apnt_cls_code: Literal['0', '1', '2', '3', '4', '5', '6', '7', '8']
    '''KOSPI200 섹터업종'''
    kospi100_issu_yn: bool
    '''KOSPI100여부'''
    kospi50_issu_yn: bool
    '''KOSPI50 종목 여부'''
    krx_issu_yn: bool
    '''KRX 종목 여부'''
    etp_prod_cls_code: Literal['0', '1', '2', '3']
    '''ETP 상품구분코드'''
    elw_pblc_yn: bool
    '''ELW 발행여부'''
    krx100_issu_yn: bool
    '''KRX100 종목 여부'''
    krx_car_yn: bool
    '''KRX 자동차 여부'''
    krx_smcn_yn: bool
    '''KRX 반도체 여부'''
    krx_bio_yn: bool
    '''KRX 바이오 여부'''
    krx_bank_yn: bool
    '''KRX 은행 여부'''
    etpr_undt_objt_co_yn: bool
    '''기업인수목적회사여부'''
    krx_enrg_chms_yn: bool
    '''KRX 에너지 화학 여부'''
    krx_stel_yn: bool
    '''KRX 철강 여부'''
    short_over_cls_code: Literal['0', '1', '2', '3']
    '''단기과열종목구분코드'''
    krx_medi_cmnc_yn: bool
    '''KRX 미디어 통신 여부'''
    krx_cnst_yn: bool
    '''KRX 건설 여부'''
    krx_scrt_yn: bool
    '''KRX 증권 구분'''
    krx_ship_yn: bool
    '''KRX 선박 구분'''
    krx_insu_yn: bool
    '''KRX섹터지수 보험여부'''
    krx_trnp_yn: bool
    '''KRX섹터지수 운송여부'''
    sri_nmix_yn: bool
    '''SRI 지수여부'''
    stck_sdpr: int
    '''주식 기준가'''
    frml_mrkt_deal_qty_unit: int
    '''정규 시장 매매 수량 단위'''
    ovtm_mrkt_deal_qty_unit: int
    '''시간외 시장 매매 수량'''
    trht_yn: bool
    '''거래정지 여부'''
    sltr_yn: bool
    '''정리매매 여부'''
    mang_issu_yn: bool
    '''관리 종목 여부'''
    mrkt_alrm_cls_code: Literal['00', '01', '02', '03']
    '''시장 경고 구분 코드'''
    mrkt_alrm_risk_adnt_yn: bool
    '''시장 경고위험 예고 여부'''
    insn_pbnt_yn: bool
    '''불성실 공시 여부'''
    byps_lstn_yn: bool
    '''우회 상장 여부'''
    flng_cls_code: Literal['00', '01', '02', '03', '04', '05', '06', '99']
    '''락구분 코드'''
    fcam_mod_cls_code: Literal['00', '01', '02', '99']
    '''액면가 변경 구분 코드'''
    icic_cls_code: Literal['00', '01', '02', '03', '99']
    '''증자 구분 코드'''
    marg_rate: int
    '''증거금 비율'''
    crdt_able: bool
    '''신용주문 가능 여부'''
    crdt_days: int
    '''신용기간'''
    prdy_vol: int
    '''전일 거래량'''
    stck_fcam: int
    '''주식 액면가'''
    stck_lstn_date: datetime
    '''주식 상장 일자'''
    lstn_stcn: int
    '''상장 주수(천)'''
    cpfn: int
    '''자본금'''
    stac_month: int
    '''결산 월'''
    po_prc: int
    '''공모 가격'''
    prst_cls_code: Literal['0', '1', '2']
    '''우선주 구분 코드'''
    ssts_hot_yn: bool
    '''공매도과열종목여부'''
    stange_runup_yn: bool
    '''이상급등종목여부'''
    krx300_issu_yn: bool
    '''KRX300 종목 여부'''
    kospi_issu_yn: bool
    '''KOSPI여부'''
    sale_account: int
    '''매출액'''
    bsop_prfi: int
    '''영업이익'''
    op_prfi: int
    '''경상이익'''
    thtr_ntin: int
    '''당기순이익'''
    roe: float
    '''ROE(자기자본이익률)'''
    base_date: datetime
    '''기준년월'''
    prdy_avls_scal: int
    '''전일기준 시가총액 (억)'''
    grp_code: str
    '''그룹사 코드'''
    co_crdt_limt_over_yn: bool
    '''회사신용한도초과여부'''
    secu_lend_able_yn: bool
    '''담보대출가능여부'''
    stln_able_yn: bool
    '''대주가능여부'''

    @property
    def kospi200_apnt_cls_name(self) -> str | None:
        return APNT_CLS_CODES.get(self.kospi200_apnt_cls_code, None)

    def __init__(self, data: str | None = None):
        if data:
            super().__init__(data)


class _KisKospiItem(Base):
    '''KOSPI 종목 정보'''
    __tablename__ = 'kospi'
    mksc_shrn_iscd = Column(String, primary_key=True)
    stnd_iscd = Column(String)
    hts_kor_isnm = Column(String)
    scrt_grp_cls_code = Column(String)
    avls_scal_cls_code = Column(String)
    bstp_larg_div_code = Column(String)
    bstp_medm_div_code = Column(String)
    bstp_smal_div_code = Column(String)
    mnin_cls_code_yn = Column(Boolean)
    low_current_yn = Column(Boolean)
    sprn_strr_nmix_issu_yn = Column(Boolean)
    kospi200_apnt_cls_code = Column(String)
    kospi100_issu_yn = Column(Boolean)
    kospi50_issu_yn = Column(Boolean)
    krx_issu_yn = Column(Boolean)
    etp_prod_cls_code = Column(String)
    elw_pblc_yn = Column(Boolean)
    krx100_issu_yn = Column(Boolean)
    krx_car_yn = Column(Boolean)
    krx_smcn_yn = Column(Boolean)
    krx_bio_yn = Column(Boolean)
    krx_bank_yn = Column(Boolean)
    etpr_undt_objt_co_yn = Column(Boolean)
    krx_enrg_chms_yn = Column(Boolean)
    krx_stel_yn = Column(Boolean)
    short_over_cls_code = Column(String)
    krx_medi_cmnc_yn = Column(Boolean)
    krx_cnst_yn = Column(Boolean)
    krx_scrt_yn = Column(Boolean)
    krx_ship_yn = Column(Boolean)
    krx_insu_yn = Column(Boolean)
    krx_trnp_yn = Column(Boolean)
    sri_nmix_yn = Column(Boolean)
    stck_sdpr = Column(Integer)
    frml_mrkt_deal_qty_unit = Column(Integer)
    ovtm_mrkt_deal_qty_unit = Column(Integer)
    trht_yn = Column(Boolean)
    sltr_yn = Column(Boolean)
    mang_issu_yn = Column(Boolean)
    mrkt_alrm_cls_code = Column(String)
    mrkt_alrm_risk_adnt_yn = Column(Boolean)
    insn_pbnt_yn = Column(Boolean)
    byps_lstn_yn = Column(Boolean)
    flng_cls_code = Column(String)
    fcam_mod_cls_code = Column(String)
    icic_cls_code = Column(String)
    marg_rate = Column(Integer)
    crdt_able = Column(Boolean)
    crdt_days = Column(Integer)
    prdy_vol = Column(Integer)
    stck_fcam = Column(Integer)
    stck_lstn_date = Column(Date)
    lstn_stcn = Column(Integer)
    cpfn = Column(Integer)
    stac_month = Column(Integer)
    po_prc = Column(Integer)
    prst_cls_code = Column(String)
    ssts_hot_yn = Column(Boolean)
    stange_runup_yn = Column(Boolean)
    krx300_issu_yn = Column(Boolean)
    kospi_issu_yn = Column(Boolean)
    sale_account = Column(Integer)
    bsop_prfi = Column(Integer)
    op_prfi = Column(Integer)
    thtr_ntin = Column(Integer)
    roe = Column(Float)
    base_date = Column(Date)
    prdy_avls_scal = Column(Integer)
    grp_code = Column(String)
    co_crdt_limt_over_yn = Column(Boolean)
    secu_lend_able_yn = Column(Boolean)
    stln_able_yn = Column(Boolean)


class KisKospi(KisKStockMarket[KisKospiItem, _KisKospiItem]):
    '''코스피 시장'''

    def __init__(self, client: 'KisMarketClient'):
        super().__init__(client, 'kospi', '코스피', 'https://new.real.download.dws.co.kr/common/master/kospi_code.mst.zip')
    