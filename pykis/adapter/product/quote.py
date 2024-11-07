from datetime import date, time, timedelta
from typing import Literal, Protocol, runtime_checkable

from pykis.api.account.order import ORDER_CONDITION
from pykis.api.base.product import KisProductProtocol
from pykis.api.stock.chart import KisChart
from pykis.api.stock.order_book import KisOrderbookResponse
from pykis.api.stock.quote import KisQuoteResponse
from pykis.utils.timex import TIMEX_TYPE, timex

__all__ = [
    "KisQuotableProduct",
    "KisQuotableProductMixin",
]


@runtime_checkable
class KisQuotableProduct(Protocol):
    """한국투자증권 시세조회가능 상품 프로토콜"""

    def daily_chart(
        self,
        start: date | timedelta | None = None,
        end: date | None = None,
        period: Literal["day", "week", "month", "year"] = "day",
        adjust: bool = False,
    ) -> KisChart:
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
        ...

    def day_chart(
        self,
        start: time | timedelta | None = None,
        end: time | None = None,
        period: int = 1,
    ) -> KisChart:
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
        ...

    def orderbook(
        self,
        condition: ORDER_CONDITION | None = None,
    ) -> KisOrderbookResponse:
        """
        한국투자증권 호가 조회

        [국내주식] 기본시세 -> 주식현재가 호가/예상체결[v1_국내주식-011]
        [해외주식] 기본시세 -> 해외주식 현재가 10호가 [해외주식-033]

        Args:
            condition (ORDER_CONDITION, optional): 주문조건. Defaults to None.

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 종목 코드가 올바르지 않은 경우
        """
        ...

    def quote(
        self,
        extended: bool = False,
    ) -> KisQuoteResponse:
        """
        한국투자증권 주식 현재가 조회

        국내주식시세 -> 주식현재가 시세[v1_국내주식-008]
        해외주식현재가 -> 해외주식 현재가상세[v1_해외주식-029]

        Args:
            extended (bool, optional): 주간거래 시세 조회 여부 (나스닥, 뉴욕, 아멕스)

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 종목 코드가 올바르지 않은 경우
        """
        ...

    def chart(
        self: KisProductProtocol,
        expression: TIMEX_TYPE | None = None,
        *,
        start: time | timedelta | date | None = None,
        end: time | date | None = None,
        period: int | Literal["day", "week", "month", "year"] = "day",
        adjust: bool = False,
    ) -> KisChart:
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
            end (time | date, optional): 조회 종료 시간. Defaults to None.
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
        ...


class KisQuotableProductMixin:
    """한국투자증권 시세조회가능 상품 프로토콜"""

    from pykis.api.stock.daily_chart import product_daily_chart as daily_chart  # 일봉 조회
    from pykis.api.stock.day_chart import product_day_chart as day_chart  # 당일 봉 조회
    from pykis.api.stock.order_book import product_orderbook as orderbook  # 호가 조회
    from pykis.api.stock.quote import product_quote as quote  # 시세 조회

    def chart(
        self: KisProductProtocol,
        expression: TIMEX_TYPE | None = None,
        *,
        start: time | timedelta | date | None = None,
        end: time | date | None = None,
        period: int | Literal["day", "week", "month", "year"] = "day",
        adjust: bool = False,
    ) -> KisChart:
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
            end (time | date, optional): 조회 종료 시간. Defaults to None.
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
        if not start and expression:
            start = timex(expression)

            if not isinstance(period, int) and start <= timedelta(days=1):
                period = 1

        if isinstance(period, int):
            if (start and not isinstance(start, (time, timedelta))) or (end and not isinstance(end, time)):
                raise ValueError("분봉 차트는 시간 타입만 지원합니다.")

            # if adjust:
            #     raise ValueError("분봉 차트는 수정주가를 지원하지 않습니다.")

            from pykis.api.stock.day_chart import product_day_chart

            return product_day_chart(
                self,
                start=start,
                end=end,
                period=int(period),
            )
        else:
            if (start and not isinstance(start, (date, timedelta))) or (end and not isinstance(end, date)):
                raise ValueError("기간 차트는 날짜 타입만 지원합니다.")

            from pykis.api.stock.daily_chart import product_daily_chart

            return product_daily_chart(
                self,
                start=start,
                end=end,
                period=period,
                adjust=adjust,
            )
