
from datetime import datetime
from typing import Generic, Iterable, Iterator, Literal, TypeVar, get_args

from .db import Base
from .base import KisMarketItemBase, KisMarketBase

SCRT_GRP_CLS_CODES = {
    'ST': '주권',
    'MF': '증권투자회사',
    'RT': '부동산투자회사',
    'SC': '선박투자회사',
    'IF': '사회간접자본투융자회사',
    'DR': '주식예탁증서',
    'EW': 'ELW',
    'EF': 'ETF',
    'SW': '신주인수권증권',
    'SR': '신주인수권증서',
    'BC': '수익증권',
    'FE': '해외ETF',
    'FS': '외국주권',
}

AVLS_SCAL_CLS_CODES = {
    '0': '제외',
    '1': '대',
    '2': '중',
    '3': '소',
}

ETP_PROD_CLS_CODES = {
    '0': '해당없음',
    '1': '투자회사형',
    '2': '수익증권형',
    '3': 'ETN',
    '4': '손실제한ETN',
}

SHORT_OVER_CLS_CODES = {
    '0': '해당없음',
    '1': '지정예고',
    '2': '지정',
    '3': '지정연장(해제연기)',
}

MRKT_ALRM_CLS_CODES = {
    '00': '해당없음',
    '01': '투자주의',
    '02': '투자경고',
    '03': '투자위험',
}

FLNG_CLS_CODES = {
    '00': '해당사항없음',
    '01': '권리락',
    '02': '배당락',
    '03': '분배락',
    '04': '권배락',
    '05': '중간배당락',
    '06': '권리중간배당락',
    '99': '기타',
}

FCAM_MOD_CLS_CODES = {
    '00': '해당없음',
    '01': '액면분할',
    '02': '액면병합',
    '99': '기타',
}

ICIC_CLS_CODES = {
    '00': '해당없음',
    '01': '유상증자',
    '02': '무상증자',
    '03': '유무상증자',
    '99': '기타',
}

PRST_CLS_CODES = {
    '0': '해당없음(보통주)',
    '1': '구형우선주',
    '2': '신형우선주',
}

class KisKStockItem(KisMarketItemBase):
    '''국내 주식 정보'''
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
    low_current_yn: bool
    '''저유동성종목 여부'''
    krx_issu_yn: bool
    '''KRX 종목 여부'''
    etp_prod_cls_code: Literal['0', '1', '2', '3']
    '''ETP 상품구분코드'''
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
    def scrt_grp_cls_name(self) -> str | None:
        return SCRT_GRP_CLS_CODES.get(self.scrt_grp_cls_code, None)

    @property
    def avls_scal_cls_name(self) -> str | None:
        return AVLS_SCAL_CLS_CODES.get(self.avls_scal_cls_code, None)

    @property
    def etp_prod_cls_name(self) -> str | None:
        return ETP_PROD_CLS_CODES.get(self.etp_prod_cls_code, None)

    @property
    def short_over_cls_name(self) -> str | None:
        return SHORT_OVER_CLS_CODES.get(self.short_over_cls_code, None)

    @property
    def mrkt_alrm_cls_name(self) -> str | None:
        return MRKT_ALRM_CLS_CODES.get(self.mrkt_alrm_cls_code, None)

    @property
    def flng_cls_name(self) -> str | None:
        return FLNG_CLS_CODES.get(self.flng_cls_code, None)

    @property
    def fcam_mod_cls_name(self) -> str | None:
        return FCAM_MOD_CLS_CODES.get(self.fcam_mod_cls_code, None)

    @property
    def icic_cls_name(self) -> str | None:
        return ICIC_CLS_CODES.get(self.icic_cls_code, None)

    @property
    def prst_cls_name(self) -> str | None:
        return PRST_CLS_CODES.get(self.prst_cls_code, None)

    def __init__(self, data: str):
        super().__init__(data)

TITME = TypeVar('TITME', bound=KisKStockItem)
TDBITTEM = TypeVar('TDBITTEM', bound=Base)

class KisKStockMarket(Generic[TITME, TDBITTEM], KisMarketBase[TITME, TDBITTEM]):
    def search(self, name: str, limit: int = 50) -> Iterable[TITME]:
        '''종목을 검색합니다.'''
        _, db_type = get_args(self.__orig_bases__[0])  # type: ignore
        return self._search(db_type.hts_kor_isnm, name, limit)  # type: ignore

    def items(self, offset: int = 0, limit: int = 100) -> Iterable[TITME]:
        '''종목을 가져옵니다.'''
        return super().items(offset, limit)

    def all(self) -> Iterator[TITME]:
        '''모든 종목을 가져옵니다.'''
        return super().all()  # type: ignore
    
    def __getitem__(self, code: str) -> TITME | None:
        '''종목을 가져옵니다.'''
        _, db_type = get_args(self.__orig_bases__[0])  # type: ignore
        return self._get(db_type.mksc_shrn_iscd, code)
