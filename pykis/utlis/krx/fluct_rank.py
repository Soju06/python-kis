from datetime import datetime
from typing import Literal

from .rank import KRXRank

# KOSPI = mktId: STK
# KOSDAQ = mktId: KSQ
# KONEX = mktId: KNX

class KRXFluctRank(KRXRank):
    '''등락율 순위'''
    acc_trdval: int
    '''거래대금 합계'''
    acc_trdvol: int
    '''거래량 합계'''
    bas_prc: int
    '''시작일 기준가'''
    clsprc: int
    '''종료일 종가'''
    cmpprevdd_prc: int
    '''대비'''
    dyavg_trdval: int
    '''거래대금 일평균'''
    dyavg_trdvol: int
    '''거래량 일평균'''
    fluc_rt: float
    '''등락율'''
    fluc_tp_cd: Literal['1', '2']
    '''등락 부호'''
    isu_abbrv: str
    '''종목명'''
    isu_cd: str
    '''종목 코드'''
    isu_cd_full: str
    '''종목 전체 코드'''
    mkt_id: Literal['STK', 'KSQ', 'KNX']
    '''시장 구분 코드'''
    mkt_nm: Literal['KOSPI', 'KOSDAQ', 'KONEX']
    '''시장구분'''
    rank: int
    '''순위'''
    secugrp_id: str
    '''종목 그룹 코드'''

    @staticmethod
    def fetch(
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        table: Literal['상승', '하락', '거래상위'] = '상승',
        market: Literal['전체', '주식', '코스피', '코스닥', '코넥스'] = '주식',
        proc: bool = True,
        sort: Literal['자동', '등락율', '거래량', '거래대금'] = '자동',
        reverse: bool = False,
    ) -> list['KRXFluctRank']:
        '''등락율 순위 조회 (20분 지연)

        Args:
            start_date (datetime, optional): 시작일. Defaults to None.
            end_date (datetime, optional): 종료일. Defaults to None.
            table (Literal['상승', '하락', '거래상위'], optional): 테이블. Defaults to '상승'.
            market (Literal['전체', '주식', '코스피', '코스닥', '코넥스'], optional): 전체, 주식, 코스피, 코스닥, 코넥스. Defaults to '주식'.
            proc (bool, optional): 수정주가 적용. Defaults to True.
            sort (Literal['자동', '등락율', '거래량', '거래대금'], optional): 정렬. 상승 또는 하락 테이블인 경우 '등락율', 거래상위 테이블인 경우 '거래량' Defaults to '자동'.
            reverse (bool, optional): 기준에 반대 차순. Defaults to False.

        Returns:
            list['KRXFluctRank']: 등락율 순위
        '''
        acc = table == '거래상위'
        tp = table == '상승'

        if sort == '자동':
            sort = '거래량' if acc else '등락율'

        if end_date is None:
            end_date = KRXFluctRank._last_date()

        if start_date is None:
            start_date = end_date

        data = {
            'strtDd': start_date.strftime('%Y%m%d'),
            'endDd': end_date.strftime('%Y%m%d'),
            'itmTpCd2': '1' if tp or acc else '2',
            'mktId': 'ALL' if market == '전체' or market == '주식' else 'STK' if market == '코스피' else 'KSQ' if market == '코스닥' else 'KNX',
        }

        if proc:
            data['stkprcTpCd'] = 'Y'

        if market == '전체':
            data['itmTpCd1'] = 'Y'

        if acc:
            data['itmTpCd3'] = '1'

        items: list[KRXFluctRank] = KRXRank._fetch(
            'dbms/MDC/EASY/ranking/MDCEASY01601' if acc else 'dbms/MDC/EASY/ranking/MDCEASY01501',
            KRXFluctRank,
            **data
        )  # type: ignore

        if sort == '등락율':
            items.sort(key=lambda item: item.fluc_rt, reverse=(tp or acc) and not reverse)
        elif sort == '거래량':
            items.sort(key=lambda item: item.acc_trdvol, reverse=not reverse)
        elif sort == '거래대금':
            items.sort(key=lambda item: item.acc_trdval, reverse=not reverse)

        return items
