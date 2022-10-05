from datetime import datetime
from typing import Literal

from .rank import KRXRank

class KRXLimitRank(KRXRank):
    '''상한/하한 순위'''
    isu_cd: str
    '''종목 코드'''
    isu_cd_full: str
    '''종목 전체 코드'''
    mkt_id: Literal['STK', 'KSQ', 'KNX']
    '''시장 구분 코드'''
    isu_abbrv: str
    '''종목명'''
    mkt_nm: Literal['KOSPI', 'KOSDAQ', 'KONEX']
    '''시장구분'''
    fluc_tp_cd: Literal['4', '5']
    '''등락 부호'''
    cmpprevdd_prc: int
    '''전일대비'''
    fluc_rt: float
    '''등락률'''
    tdd_opnprc: int
    '''시가'''
    tdd_clsprc: int
    '''종가'''
    tdd_hgprc: int
    '''고가'''
    tdd_lwprc: int
    '''저가'''
    acc_trdvol: int
    '''거래량'''
    acc_trdval: int
    '''거래대금'''

    @staticmethod
    def fetch(
        date: datetime | None = None,
        table: Literal['상한가', '하한가'] = '상한가',
        market: Literal['전체', '코스피', '코스닥', '코넥스'] = '전체',
        sort: Literal['거래량', '거래대금'] = '거래량',
        reverse: bool = False,
    ) -> list['KRXLimitRank']:
        '''상한/하한 종목을 가져옵니다. (20분 지연)
        
        Args:
            date (datetime, optional): 날짜. Defaults to None.
            table (Literal['상한가', '하한가'], optional): 상한/하한. Defaults to '상한가'.
            market (Literal['전체', '코스피', '코스닥', '코넥스'], optional): 시장. Defaults to '전체'.
            sort (Literal['거래량', '거래대금'], optional): 정렬 기준. Defaults to '거래량'.
            reverse (bool, optional): 기준에 반대 차순. Defaults to False.
        '''
        if date is None:
            date = KRXLimitRank._last_date()

        data = {
            'trdDd': date.strftime('%Y%m%d'),
            'flucTpCd': '4' if table == '상한가' else '5',
            'mktId': 'ALL' if market == '전체' else 'STK' if market == '코스피' else 'KSQ' if market == '코스닥' else 'KNX',
        }

        items: list[KRXLimitRank] = KRXRank._fetch(
            'dbms/MDC/EASY/ranking/MDCEASY01801',
            KRXLimitRank,
            **data
        )  # type: ignore

        if sort == '거래량':
            items.sort(key=lambda item: item.acc_trdvol, reverse=not reverse)
        elif sort == '거래대금':
            items.sort(key=lambda item: item.acc_trdval, reverse=not reverse)

        return items
