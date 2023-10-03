from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING, Literal

from pykis.api.stock.market import MARKET_TIMEZONE_OBJECT_MAP, MARKET_TYPE, MARKET_TYPE_KOR_MAP
from pykis.client.object import KisObjectBase
from pykis.utils.cache import cached
from pykis.utils.timex import TIMEX_TYPE, timex

if TYPE_CHECKING:
    from pykis.api.stock.info import KisStockInfo
    from pykis.scope.stock.info_stock import KisInfoStock
    from pykis.api.stock.quote import KisQuote
    from pykis.api.stock.day_chart import KisDayChart
    from pykis.api.stock.daily_chart import KisDailyChart


class KisProductScopeBase(KisObjectBase):
    """한국투자증권 상품 기본정보"""

    code: str
    """종목코드"""
    market: MARKET_TYPE | None
    """상품유형타입"""

    @property
    def primary_market(self) -> MARKET_TYPE:
        """실제 상품유형타입"""
        if self.market is not None:
            return self.market

        return self.info.market

    @property
    def market_name(self) -> str:
        """실제 상품유형명"""
        return MARKET_TYPE_KOR_MAP[self.primary_market]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self.code}, market={self.market})"

    @property
    @cached
    def info(self) -> "KisStockInfo":
        """
        상품기본정보 조회.

        국내주식시세 -> 상품기본조회[v1_국내주식-029]

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 종목 코드가 올바르지 않은 경우
        """
        from pykis.api.stock.info import info as _info

        return _info(
            self.kis,
            code=self.code,
            market=self.market,
        )

    @property
    def stock(self) -> "KisInfoStock":
        """종목 Scope"""
        from pykis.scope.stock.info_stock import KisInfoStock

        return KisInfoStock(
            kis=self.kis,
            info=self.info,
        )

    def quote(self) -> "KisQuote":
        """
        한국투자증권 주식 현재가 조회

        국내주식시세 -> 주식현재가 시세[v1_국내주식-008]
        해외주식현재가 -> 해외주식 현재가상세[v1_해외주식-029]

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 종목 코드가 올바르지 않은 경우
        """
        from pykis.api.stock.quote import quote as _quote

        return _quote(
            self.kis,
            code=self.code,
            market=self.primary_market,
        )

    @property
    @cached
    def cached_quote(self) -> "KisQuote":
        """
        한국투자증권 주식 현재가 조회

        국내주식시세 -> 주식현재가 시세[v1_국내주식-008]
        해외주식현재가 -> 해외주식 현재가상세[v1_해외주식-029]

        (캐시됨)

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 종목 코드가 올바르지 않은 경우
        """
        return self.quote()

    def day_chart(
        self,
        start: time | timedelta | None = None,
        end: time | None = None,
        period: int = 1,
    ) -> "KisDayChart":
        """
        한국투자증권 당일 봉 차트 조회

        해외 당일 봉 차트 조회는 한국투자증권 API의 한계로 인해 (24 * 60 / 최대 레코드 수)번 호출하여 원하는 영역의 근접 값을 채워넣습니다.
        따라서, 누락된 봉이 존재할 수 있으며, n = (최대 레코드 수), I = {x | x = (i + 1) * (j + 1), 0 <= ceil(24 * 60 / n), 0 <= j < n}의 해상도를 가집니다.

        국내주식시세 -> 주식당일분봉조회[v1_국내주식-022]
        해외주식현재가 -> 해외주식분봉조회[v1_해외주식-030]

        Args:
            start (time | timedelta, optional): 조회 시작 시간. timedelta인 경우 최근 timedelta만큼의 봉을 조회합니다. Defaults to None.
            end (time, optional): 조회 종료 시간. Defaults to None.
            period (int, optional): 조회 간격 (분). Defaults to 1.

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 조회 파라미터가 올바르지 않은 경우
        """
        from pykis.api.stock.day_chart import day_chart as _day_chart

        return _day_chart(
            self.kis,
            code=self.code,
            market=self.primary_market,
            start=start,
            end=end,
            period=period,
        )

    def daily_chart(
        self,
        start: date | timedelta | None = None,
        end: date | None = None,
        period: Literal["day", "week", "month", "year"] = "day",
        adjust: bool = False,
    ) -> "KisDailyChart":
        """
        한국투자증권 기간 차트 조회

        국내주식시세 -> 국내주식기간별시세(일/주/월/년)[v1_국내주식-016]
        해외주식현재가 -> 해외주식 기간별시세[v1_해외주식-010]

        Args:
            start (date, optional): 조회 시작 시간. timedelta인 경우 최근 timedelta만큼의 봉을 조회합니다. Defaults to None.
            end (date, optional): 조회 종료 시간. Defaults to None.
            period (Literal["day", "week", "month", "year"], optional): 조회 기간. Defaults to "day".
            adjust (bool, optional): 수정 주가 여부. Defaults to False.

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 조회 파라미터가 올바르지 않은 경우
        """
        from pykis.api.stock.daily_chart import daily_chart as _daily_chart

        return _daily_chart(
            self.kis,
            code=self.code,
            market=self.primary_market,
            start=start,
            end=end,
            period=period,
            adjust=adjust,
        )

    def chart(
        self,
        expression: TIMEX_TYPE | None = None,
        *,
        start: time | timedelta | date | None = None,
        end: time | date | None = None,
        period: int | Literal["day", "week", "month", "year"] = "day",
        adjust: bool = False,
    ) -> "KisDayChart | KisDailyChart":
        """
        한국투자증권 기간 차트 조회

        `start` 필드가 지정될 경우 `expression` 필드는 무시됩니다.

        분봉조회:
        국내주식시세 -> 주식당일분봉조회[v1_국내주식-022]
        해외주식현재가 -> 해외주식분봉조회[v1_해외주식-030]

        기간조회:
        국내주식시세 -> 국내주식기간별시세(일/주/월/년)[v1_국내주식-016]
        해외주식현재가 -> 해외주식 기간별시세[v1_해외주식-010]

        Args:
            expression (TIMEX_TYPE, optional): 최근 조회 기간 표현식. Defaults to '7d'.
            start (time | timedelta | date, optional): 조회 시작 시간. timedelta인 경우 최근 timedelta만큼의 봉을 조회합니다. Defaults to None.
            end (date, optional): 조회 종료 시간. Defaults to None.
            period (int | Literal["day", "week", "month", "year"], optional): 조회 기간. (타입이 `int`인 경우 분봉 차트의 분틱 값으로 조회합니다.) Defaults to "day".
            adjust (bool, optional): 수정 주가 여부. (분봉조회는 수정주가를 지원하지 않습니다.) Defaults to False.

        Examples:
            >>> stock.chart("7d") # 7일간의 일 차트 조회
            >>> stock.chart(period=5) # 당일 5분봉 차트 조회
            >>> stock.chart(period="week") # 전체 주봉 차트 조회
            >>> stock.chart("30m", period=1) # 당일 최근 30분간 1분봉 차트 조회
            >>> stock.chart("1y", period="month") # 1년간의 월봉 차트 조회
            >>> stock.chart(start=date(2023, 1, 1), end=date(2023, 10, 1)) # 2023년 1월 1일부터 10월 1일까지의 일봉 차트 조회



        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 조회 파라미터가 올바르지 않은 경우
        """
        is_day = isinstance(period, int)

        if not start and expression:
            start = timex(expression)

        if is_day:
            if (start and not isinstance(start, (time, timedelta))) or (
                end and not isinstance(end, time)
            ):
                raise ValueError("분봉 차트는 시간 타입만 지원합니다.")

            if adjust:
                raise ValueError("분봉 차트는 수정주가를 지원하지 않습니다.")

            return self.day_chart(
                start=start,
                end=end,
                period=int(period),
            )
        else:
            if (start and not isinstance(start, (date, timedelta))) or (
                end and not isinstance(end, date)
            ):
                raise ValueError("기간 차트는 날짜 타입만 지원합니다.")

            return self.daily_chart(
                start=start,
                end=end,
                period=period,
                adjust=adjust,
            )
