from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Iterable, Iterator, Literal, get_args
from sqlalchemy import Column, Integer, String, Date, Boolean, Float, and_

from .base import KisMarketBase, KisMarketItemBase
from .db import Base

if TYPE_CHECKING:
    from .client import KisMarketClient

# typedef struct
# {
#     char    idx_div[1]; /* 시장구분값 ex) 00002(대형주)일 경우 맨 앞자리 0              */
#     char    idx_code[4];  /* 업종코드 ex) 00002(대형주)일 경우 맨 앞자리를 제외한 0002  */
#     char    idx_name[40]; /* 업종명                                                    */
# } IDX_CODE;
@dataclass
class KisSectorItem(KisMarketItemBase):
    CONTROL = [
        ('idx_full_code', 5),
        ('idx_name', 40),
    ]

    idx_full_code: str
    '''업종 코드'''
    idx_name: str
    '''업종 이름'''

    @property
    def idx_div(self) -> str:
        '''시장 구분값'''
        return self.idx_full_code[0]

    @property
    def idx_code(self) -> str:
        '''업종 코드'''
        return self.idx_full_code[1:]

    def __init__(self, data: str | None = None):
        if data:
            super().__init__(data)


class _KisSectorItem(Base):
    '''업종 종목'''
    __tablename__ = 'sector'
    idx_full_code = Column(String, primary_key=True)
    '''업종 코드'''
    idx_name = Column(String, nullable=False)
    '''업종 이름'''


class KisSector(KisMarketBase[KisSectorItem, _KisSectorItem]):
    ''''''

    def __init__(self, client: 'KisMarketClient'):
        super().__init__(client, 'sector', '업종', 'https://new.real.download.dws.co.kr/common/master/idxcode.mst.zip')
    
    def search(self, name: str, limit: int = 50) -> Iterable[KisSectorItem]:
        '''업종을 검색합니다.'''
        return self._search(_KisSectorItem.idx_name, name, limit)
        
    def __getitem__(self, code: str) -> KisSectorItem | None:
        '''종목을 가져옵니다.'''
        _, db_type = get_args(self.__orig_bases__[0])  # type: ignore
        return self._get(db_type.idx_full_code, code)
    
    def all(self) -> Iterator[KisSectorItem]:
        return super().all()  # type: ignore