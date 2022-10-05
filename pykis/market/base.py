from abc import abstractmethod
from datetime import datetime, timedelta
import io
import logging
from threading import Lock
import zipfile
import requests
from typing import TYPE_CHECKING, Generic, Iterable, TypeVar, get_args
from sqlalchemy.orm import Session
from sqlalchemy import Column, and_

from ..logging import KisLoggable
from .db import Base, KisMarket

if TYPE_CHECKING:
    from .client import KisMarketClient

class KisMarketItemBase:
    '''시장 종목'''
    
    def __init__(self, data: str):
        items = self.__class__.__dict__['CONTROL'].copy()
        data_len = len(data)
        index = 0
        reverse = False

        while items:
            key, value = items[0]
            del items[0]
            
            if key == '_reverse':
                items.reverse()
                reverse = not reverse
                continue
            elif key == '_index':
                if value < 0:
                    value = data_len - (abs(value) - 1)
                index = value
                continue
            elif key[:2] == '__':
                continue
            elif isinstance(value, tuple):
                value = list(value)

                for i, v in enumerate(value):
                    if v < 0:
                        value[i] = data_len - abs(v)

                v = data[value[0]:value[1]]
            elif reverse:
                v = data[index - value:index]
                index -= value
            else:
                v = data[index:index + value]
                index += value

            if key == '_dummy':
                continue
            
            type = self.__annotations__[key]
            setattr(self, key, self.__convert(type, v.strip()))

    def __convert(self, type, value):
        try:
            if type != str:
                if type == bool:
                    return value == 'Y' if value else None
                elif type == datetime:
                    return datetime.strptime(value, '%Y%m%d')
                elif type.__name__ == 'Literal':
                    return value

                return type(value)
        except:
            return None
        return value

TITME = TypeVar('TITME', bound=KisMarketItemBase)
TDBITTEM = TypeVar('TDBITTEM', bound=Base)

class KisMarketBase(Generic[TITME, TDBITTEM], KisLoggable):
    '''시장'''
    client: 'KisMarketClient'
    '''클라이언트'''
    code: str
    '''시장 코드'''
    name: str
    '''시장 이름'''
    mst: str
    '''종목 데이터 주소'''
    encoding: str = 'cp949'
    '''인코딩'''
    
    _lock: Lock
    
    def __init__(self, client: 'KisMarketClient', code: str, name: str, mst: str):
        self.client = client
        self.code = code
        self.name = name
        self.mst = mst
        self._lock = Lock()

    def sync(self, cache: bool = True):
        '''종목 정보를 동기화합니다.'''
        with self._lock:
            if cache:
                sync_at = self.client.sync_at(self.code)

                if sync_at and datetime.now() - sync_at < timedelta(days=1):
                    self.client.logger.info(f'MARKET: up to date {self.code}')
                    return

            self._sync()

    def _sync(self):
        self.logger.info(f'MARKET: sync %s, download %s', self.code, self.mst)
        with zipfile.ZipFile(io.BytesIO(requests.get(self.mst).content)) as archive:
            data = archive.read(archive.filelist[0])
        self._update(data.decode(self.encoding))
    
    def _update(self, data: str):
        lines = data.splitlines()
        self.logger.info('MARKET: parseing %s data... %s lines', self.code, len(lines))
        type, db_type = get_args(self.__orig_bases__[0])  # type: ignore

        with self.client.session as sess:
            for line in lines:
                if not line: continue
                item = db_type()
                state = item._sa_instance_state
                item.__dict__ = type(line).__dict__
                item._sa_instance_state = state
                sess.merge(item)
                
            self.client._update_sync_at(self.code)
            sess.commit()

            if self.logger.level == logging.DEBUG:
                self.logger.info(f'MARKET: up to date {self.code}, {sess.query(db_type).count()} items')
    
    def _sf_acc(self):
        with self._lock: pass

    def _market(self) -> KisMarket:
        return KisMarket(
            code=self.code,
            name=self.name
        )
    
    @property
    def _session(self) -> Session:
        return self.client.session
    
    def _search(self, column: Column, name: str, limit: int = 50) -> Iterable:
        self._sf_acc()
        type, db_type = get_args(self.__orig_bases__[0])  # type: ignore

        with self._session as sess:
            keywords = name.split()
            for item in sess.query(db_type) \
                .filter(and_(*[column.like(f'%{keyword}%') for keyword in keywords])) \
                .limit(limit).all():
                data = type()
                del item.__dict__['_sa_instance_state']
                data.__dict__ = item.__dict__
                yield data
            
    def _get(self, column: Column, data: str) -> TITME | None:
        self._sf_acc()
        type, db_type = get_args(self.__orig_bases__[0])  # type: ignore

        with self._session as sess:
            item = sess.query(db_type).filter(column == data).first()

            if item:
                data = type()
                del item.__dict__['_sa_instance_state']
                data.__dict__ = item.__dict__
                return data  # type: ignore

            return None

    def items(self, offset: int = 0, limit: int = 100) -> Iterable:
        '''종목 정보를 반환합니다.'''
        self._sf_acc()
        type, db_type = get_args(self.__orig_bases__[0])  # type: ignore

        with self._session as sess:
            for item in sess.query(db_type).offset(offset).limit(limit).all():
                data = type()
                del item.__dict__['_sa_instance_state']
                data.__dict__ = item.__dict__
                yield data

    def all(self):
        self._sf_acc()
        return self.items(limit=999999)
    
    @abstractmethod
    def search(self, name: str, limit: int = 50) -> Iterable:
        '''종목 이름으로 검색합니다.'''
        raise NotImplementedError()
    
    def search_one(self, name: str) -> TITME | None:
        for i in self.search(name, 1):
            return i
        
        return None
    