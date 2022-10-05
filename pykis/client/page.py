
from typing import Literal


KisPageStatus = Literal['begin', 'end']

def to_page_status(status: str) -> KisPageStatus:
    if status == 'F' or status == 'M':
        return 'begin'
    elif status == 'D' or status == 'E':
        return 'end'
    else:
        raise ValueError(f'Invalid page status: {status}')

class KisPage:
    '''한국투자증권 페이징 정보'''
    search: str
    '''CTX_AREA_FK100	연속조회검색조건100'''
    key: str
    '''CTX_AREA_NK100	연속조회키100'''

    def __init__(self, data: dict):
        self.search = data['ctx_area_fk100']
        self.key = data['ctx_area_nk100']
    
    @property
    def empty(self) -> bool:
        '''페이징 정보가 비어있는지 확인합니다.'''
        return self.search == '' and self.key == ''

    @staticmethod
    def first() -> 'KisPage':
        '''첫 페이지'''
        return KisPage({'ctx_area_fk100': '', 'ctx_area_nk100': ''})

    def build_body(self, body: dict) -> dict:
        '''페이징 정보를 추가합니다.'''
        body['CTX_AREA_FK100'] = self.search
        body['CTX_AREA_NK100'] = self.key

        return body