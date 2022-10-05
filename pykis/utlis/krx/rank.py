
from typing import Literal
from .base import KRXBase

FLUC_TP_CODES = {
    '1': '상승',
    '2': '하락',
    '4': '상한가',
    '5': '하한가',
}

MARKET_ID_NAMES = {
    'STK': '코스피',
    'KSQ': '코스닥',
    'KNX': '코넥스',
}

class KRXRank(KRXBase):
    isu_cd: str
    '''종목 코드'''
    isu_cd_full: str
    '''종목 전체 코드'''
    isu_abbrv: str
    '''종목명'''
    acc_trdvol: int
    '''거래량 합계'''
    fluc_rt: float
    '''등락율'''
    mkt_id: Literal['STK', 'KSQ', 'KNX']
    '''시장 구분 코드'''
    mkt_nm: Literal['KOSPI', 'KOSDAQ', 'KONEX']
    '''시장구분'''
    cmpprevdd_prc: int
    '''대비'''
    acc_trdval: int
    '''거래대금 합계'''
    fluc_tp_cd: Literal['1', '2', '4', '5']
    '''등락 부호'''

    @property
    def fluc_tp(self) -> Literal['상승', '하락', '상한가', '하한가']:
        '''등락 부호'''
        return FLUC_TP_CODES[self.fluc_tp_cd]  # type: ignore

    @property
    def market(self) -> Literal['코스피', '코스닥', '코넥스']:
        '''시장구분'''
        return MARKET_ID_NAMES[self.mkt_id]  # type: ignore
