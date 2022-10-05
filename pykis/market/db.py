from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class KisMarket(Base):
    '''시장'''
    __tablename__ = 'market'
    code = Column(String, primary_key=True)
    '''시장 코드'''
    name = Column(String, nullable=False)
    '''시장 이름'''
    sync_at = Column(DateTime, nullable=True)
    '''동기화된 시간'''
