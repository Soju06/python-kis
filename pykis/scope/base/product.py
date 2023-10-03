from datetime import date, time
from typing import TYPE_CHECKING, Literal

from pykis.api.stock.market import MARKET_TYPE, MARKET_TYPE_KOR_MAP
from pykis.client.object import KisObjectBase
from pykis.utils.cache import cached

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
        """시장 종류"""
        return MARKET_TYPE_KOR_MAP[self.market]

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
        start: time | None = None,
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
            start (time, optional): 조회 시작 시간. Defaults to None.
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
        start: date | None = None,
        end: date | None = None,
        period: Literal["day", "week", "month", "year"] = "day",
        adjust: bool = False,
    ) -> "KisDailyChart":
        """
        한국투자증권 기간 차트 조회

        국내주식시세 -> 국내주식기간별시세(일/주/월/년)[v1_국내주식-016]
        해외주식현재가 -> 해외주식 기간별시세[v1_해외주식-010]

        Args:
            start (date, optional): 조회 시작 시간. Defaults to None.
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
        start: time | date | None = None,
        end: time | date | None = None,
        period: Literal["1", "5", "10", "30", "60", "day", "week", "month", "year"] = "day",
        adjust: bool = False,
    ) -> "KisDayChart | KisDailyChart":
        """
        한국투자증권 기간 차트 조회

        분봉조회의 경우 `start`, `end` 파라미터가 `time` 타입이어야 하며,
        기간조회의 경우 `start`, `end` 파라미터가 `date` 타입이어야 합니다.

        분봉조회:
        국내주식시세 -> 주식당일분봉조회[v1_국내주식-022]
        해외주식현재가 -> 해외주식분봉조회[v1_해외주식-030]

        기간조회:
        국내주식시세 -> 국내주식기간별시세(일/주/월/년)[v1_국내주식-016]
        해외주식현재가 -> 해외주식 기간별시세[v1_해외주식-010]

        Args:
            start (date, optional): 조회 시작 시간. Defaults to None.
            end (date, optional): 조회 종료 시간. Defaults to None.
            period (Literal["day", "week", "month", "year"], optional): 조회 기간. Defaults to "day".
            adjust (bool, optional): 수정 주가 여부. (분봉조회는 수정주가를 지원하지 않습니다.) Defaults to False.

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 조회 파라미터가 올바르지 않은 경우
        """
        if period in ("1", "5", "10", "30", "60", "hour"):
            if (start and not isinstance(start, time)) or (end and not isinstance(end, time)):
                raise ValueError("분봉 차트는 시간 타입만 지원합니다.")

            if adjust:
                raise ValueError("분봉 차트는 수정주가를 지원하지 않습니다.")

            return self.day_chart(
                start=start,
                end=end,
                period=int(period),
            )
        else:
            if (start and not isinstance(start, date)) or (end and not isinstance(end, date)):
                raise ValueError("기간 차트는 날짜 타입만 지원합니다.")

            return self.daily_chart(
                start=start,
                end=end,
                period=period,
                adjust=adjust,
            )
