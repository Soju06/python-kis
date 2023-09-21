from datetime import timedelta
import logging

from .account import KisAccount
from .client import KisKey, KisClient
from .logging import KisLoggable
from .market import KisMarketClient, KisKStockItem
from .rtclient import KisRTClient
from .scope import KisAccountScope, KisStockScope


class PyKis(KisLoggable):
    """한국투자증권 API"""

    key: KisKey
    """한국투자증권 API Key"""
    client: KisClient
    """한국투자증권 API 클라이언트"""
    market: KisMarketClient
    """종목 정보 클라이언트"""

    _rtclient: KisRTClient | None
    _init: bool = False

    def __init__(
        self,
        appkey: str | KisKey,
        appsecret: str | None = None,
        virtual_account: bool = False,
        market_database_path: str | None = None,
        market_auto_sync_interval: timedelta = timedelta(days=1),
        market_auto_sync: bool = True,
        realtime: bool = True,
        logger: logging.Logger | None = None,
        late_init: bool = False,
    ):
        """한국투자증권 API를 생성합니다.

        Args:
            appkey: 앱 키 또는 앱 키 객체
            appsecret: 앱 시크릿. 앱 키 객체를 사용할 경우 생략 가능.
            virtual_account: 가상계좌 여부. 앱 키 객체를 사용할 경우 생략 가능.
            market_database_path: 종목 정보 데이터베이스 경로. 생략 시 임시 경로에 저장됩니다.
            market_auto_sync_interval: 종목 정보 자동 동기화 주기. 기본값은 1일입니다.
            market_auto_sync: 종목 정보 자동 동기화 여부. 기본값은 True입니다.
            realtime: 실시간 API 사용 여부. 생략 시 사용됩니다.
            logger: 로거. 생략 시 기본 로거가 사용됩니다.
            late_init: 지연 초기화 여부. 기본값은 False입니다.
        """
        if isinstance(appkey, KisKey):
            self.key = appkey
        else:
            if not appsecret:
                raise ValueError("AppSecret이 없습니다.")

            self.key = KisKey(appkey, appsecret, virtual_account)

        self.client = KisClient(self.key)
        self.market = KisMarketClient(
            client=self.client,
            database_path=market_database_path,
            auto_sync=market_auto_sync,
            auto_sync_interval=market_auto_sync_interval,
        )
        self._emit_logger(logger)

        if realtime:
            self._rtclient = KisRTClient(self.client, logger=self.logger)
        else:
            self._rtclient = None

        if not late_init:
            self.init()

    @property
    def rtclient(self) -> KisRTClient:
        """실시간 API 클라이언트"""
        if self._rtclient is None:
            raise ValueError("실시간 API 사용이 설정되지 않았습니다.")
        return self._rtclient

    def init(self):
        """API를 초기화합니다."""
        if self._init:
            return

        self.market._init()

        if self._rtclient:
            self._rtclient.wait_connected()

        self._init = True

    def stock(self, stock: KisKStockItem | str) -> KisStockScope:
        """코스피/코스닥 종목 스코프를 생성합니다.

        Args:
            code: 종목 코드
        """
        if isinstance(stock, str):
            st = self.market.stock(stock)
            if st is None:
                raise ValueError(f"코스피/코스닥 종목 {stock}이 존재하지 않습니다.")
            stock = st

        scope = KisStockScope(self, stock)
        scope._emit_logger(self.logger)

        return scope

    def stock_search(self, name: str) -> KisStockScope | None:
        """코스피/코스닥 종목을 검색합니다.

        Args:
            name: 종목 이름
        """
        stock = self.market.stock_search_one(name)
        if stock is None:
            return None
        return self.stock(stock)

    def account(self, account: KisAccount | str) -> KisAccountScope:
        """계좌 스코프를 생성합니다.

        Args:
            account: 계좌 또는 계좌 번호
        """
        if isinstance(account, str):
            account = KisAccount(account)

        scope = KisAccountScope(self, account)
        scope._emit_logger(self.logger)
        return scope
