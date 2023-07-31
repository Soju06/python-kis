from datetime import date, datetime, timedelta
import logging
import os.path as path
import tempfile
from threading import Lock, Thread
import time
from typing import Iterable
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from itertools import chain

from ..client import KisClient
from ..__env__ import MARKET_VERSION
from ..logging import KisLoggable
from .db import Base, KisMarket
from .base import KisMarketBase
from .markets import *
from ..scope.market.api import KisMarketHoliday, KisMarketHolidays


class KisMarketClient(KisLoggable):
    """한국투자증권 종목정보 클라이언트"""

    database_path: str
    """저장 경로"""
    engine: Engine
    """데이터베이스 엔진"""
    markets: dict[str, KisMarketBase]
    """시장"""
    client: KisClient
    """한국투자증권 API 클라이언트"""

    _sessionmaker: sessionmaker
    _rth: int = 0
    _sstd: datetime | None
    _sl: Lock

    def __init__(
        self,
        client: KisClient,
        database_path: str | None = None,
        auto_sync: bool = True,
    ):
        if database_path is None:
            database_path = path.join(tempfile.gettempdir(), f".pykis-cache_market.{MARKET_VERSION}.db")
        self.database_path = database_path
        self.client = client
        self.markets = {}
        self._sstd = None
        self._sl = Lock()
        self._create_database()

        if auto_sync:
            self._st_sync()

    def _create_database(self):
        self.engine = create_engine(
            f"sqlite:///{self.database_path}?check_same_thread=False"
        )  # maybe it will be ok for a while...
        Base.metadata.create_all(self.engine)
        self._sessionmaker = sessionmaker(bind=self.engine, autoflush=False)

    def _logger_ready(self, logger: logging.Logger):
        logger.debug(f"database open: {self.database_path}")

    def _init(self):
        self._sync_all(comp=False, verbose=False)

    @property
    def session(self) -> Session:
        """세션"""
        return self._sessionmaker()

    def sync_at(self, code: str) -> datetime | None:
        """종목 정보를 마지막으로 업데이트한 시간"""
        return self.session.query(KisMarket.sync_at).filter(KisMarket.code == code).scalar()

    def sync_all(self):
        """모든 시장을 동기화합니다."""
        self._sync_all(comp=True, verbose=False)

    def _sync_all(self, comp: bool = False, verbose: bool = False) -> bool:
        with self._sl:
            now = datetime.now()

            if comp:
                self._sstd = now
            else:
                if self._sstd:
                    if now - self._sstd < timedelta(seconds=30):
                        if verbose:
                            self.logger.info("MARKET: too early to sync")

                        return False

                self._sstd = now

        for code in MARKETS:
            self[code].sync()

        return True

    def _get_market(self, sess: Session, code: str) -> KisMarket:
        market = self[code]

        if not market:
            raise KeyError(f"Unknown market: {code}")

        sess.merge(market._market())
        sess.commit()

        return sess.query(KisMarket).filter(KisMarket.code == code).one()

    def _update_sync_at(self, code: str):
        """종목 정보를 업데이트한 시간을 업데이트합니다."""
        with self.session as sess:
            dm = self._get_market(sess, code)
            dm.sync_at = datetime.now()  # type: ignore
            sess.commit()

    def _st_sync(self):
        """자동동기화 스레드"""
        self._rth += 1
        tid = self._rth
        Thread(target=self._at_sync, args=(tid,), daemon=True).start()

    def _at_sync(self, tid: int):
        """자동 동기화"""
        n = False
        time.sleep(31)
        while self._rth == tid:
            try:
                if self._sync_all(comp=False, verbose=n):
                    self.logger.info("MARKET: auto-sync")
            except Exception as e:
                self.logger.error(f"MARKET: auto-sync exception: {e}")
            finally:
                if not n:
                    n = True
                time.sleep((60 * 60 * 24) + 5)

    def __getitem__(self, code: str) -> MARKET_TYPE:
        """시장"""
        if code not in self.markets:
            market = MARKETS[code](self)
            market._emit_logger(self.logger)
            self.markets[code] = market
        else:
            market = self.markets[code]
        return market  # type: ignore

    @property
    def kospi(self) -> KisKospi:
        """코스피"""
        return self["kospi"]  # type: ignore

    @property
    def kosdaq(self) -> KisKosdaq:
        """코스닥"""
        return self["kosdaq"]  # type: ignore

    @property
    def sector(self) -> KisSector:
        """업종"""
        return self["sector"]  # type: ignore

    def stock(self, code: str) -> KisKStockItem | None:
        """코스피/코스닥 종목"""
        return self.kospi[code] or self.kosdaq[code]  # type: ignore

    def search(
        self, keyword: str, origin: list[str] | None = None
    ) -> dict[str, Iterable[MARKET_ITEM_TYPE]]:
        """종목 검색을 수행합니다.

        Args:
            keyword: 검색 키워드
            origin: 검색할 시장 (기본값: 모든 시장)
        """
        result = {}

        for market in self.markets.values():
            if not origin or market.code in origin:
                result[market.code] = market.search(keyword)

        return result

    def stock_search(self, keyword: str) -> dict[str, Iterable[KisKStockItem]]:
        """코스피/코스닥 종목 검색을 수행합니다."""
        return self.search(keyword, ["kospi", "kosdaq"])  # type: ignore

    def stock_search_combined(self, keyword: str) -> Iterable[KisKStockItem]:
        """코스피/코스닥 종목 검색을 수행합니다."""
        return chain(*self.stock_search(keyword).values())

    def search_one(self, keyword: str, origin: list[str] | None = None) -> MARKET_ITEM_TYPE | None:
        """종목 검색을 수행합니다.

        Args:
            keyword: 검색 키워드
            origin: 검색할 시장 (기본값: 모든 시장)
        """
        for market in self.markets.values():
            if not origin or market.code in origin:
                result = market.search_one(keyword)

                if result:
                    return result

        return None

    def stock_search_one(self, keyword: str) -> KisKStockItem | None:
        return self.search_one(keyword, ["kospi", "kosdaq"])  # type: ignore

    from ..scope.market.api import holiday, info

    def today(self, date: date | datetime | str | None = None) -> KisMarketHoliday | None:
        """휴장일 정보를 가져옵니다.

        Args:
            date: 날짜 (기본값: 오늘)
        """
        if date is None:
            date = datetime.today().date()
        return self.holiday(date)[date]
