from datetime import date, time, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING, Literal

from pykis.api.stock.market import MARKET_TYPE, MARKET_TYPE_KOR_MAP
from pykis.client.account import KisAccountNumber
from pykis.client.object import KisObjectBase
from pykis.utils.cache import cached
from pykis.utils.timex import TIMEX_TYPE, timex

if TYPE_CHECKING:
    from pykis.api.account.order import (
        ORDER_CONDITION,
        ORDER_EXECUTION_CONDITION,
        ORDER_PRICE,
        ORDER_TYPE,
        KisOrder,
    )
    from pykis.api.account.orderable_amount import KisOrderableAmount
    from pykis.api.stock.daily_chart import KisDailyChart
    from pykis.api.stock.day_chart import KisDayChart
    from pykis.api.stock.info import KisStockInfo
    from pykis.api.stock.quote import KisQuote
    from pykis.scope.account.account import KisAccountScope
    from pykis.scope.stock.info_stock import KisInfoStock


class KisProductBase(KisObjectBase):
    """한국투자증권 상품 기본정보"""

    code: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    @property
    def name(self) -> str:
        """상품명"""
        return self.info.name

    @property
    def market_name(self) -> str:
        """실제 상품유형명"""
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

    def quote(self, extended: bool = False) -> "KisQuote":
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
        from pykis.api.stock.quote import quote

        return quote(
            self.kis,
            code=self.code,
            market=self.market,
            extended=extended,
        )

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
        from pykis.api.stock.day_chart import day_chart

        return day_chart(
            self.kis,
            code=self.code,
            market=self.market,
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
        from pykis.api.stock.daily_chart import daily_chart

        return daily_chart(
            self.kis,
            code=self.code,
            market=self.market,
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
            if (start and not isinstance(start, (time, timedelta))) or (end and not isinstance(end, time)):
                raise ValueError("분봉 차트는 시간 타입만 지원합니다.")

            if adjust:
                raise ValueError("분봉 차트는 수정주가를 지원하지 않습니다.")

            return self.day_chart(
                start=start,
                end=end,
                period=int(period),
            )
        else:
            if (start and not isinstance(start, (date, timedelta))) or (end and not isinstance(end, date)):
                raise ValueError("기간 차트는 날짜 타입만 지원합니다.")

            return self.daily_chart(
                start=start,
                end=end,
                period=period,
                adjust=adjust,
            )

    def orderable_amount(
        self,
        price: "ORDER_PRICE | None" = None,
        condition: "ORDER_CONDITION | None" = None,
        execution: "ORDER_EXECUTION_CONDITION | None" = None,
        account: "str | KisAccountNumber | KisAccountScope | None" = None,
    ) -> "KisOrderableAmount":
        """
        한국투자증권 주문가능금액 조회

        국내주식주문 -> 매수가능조회[v1_국내주식-007]
        해외주식주문 -> 해외주식 매수가능금액조회[v1_해외주식-014]

        Args:
            price (ORDER_PRICE | None, optional): 주문가격. None인 경우 시장가 주문
            condition (ORDER_CONDITION | None, optional): 주문조건
            execution (ORDER_EXECUTION_CONDITION | None, optional): 채결조건
            account (str | KisAccountNumber | KisAccountScope | None, optional): 계좌번호. None인 경우 기본 계좌 사용

        Examples:
            >>> stock.orderable_amount(price=100, condition=None, execution=None) # 전체 지정가 매수
            >>> stock.orderable_amount(price=None, condition=None, execution=None) # 전체 시장가 매수
            >>> stock.orderable_amount(price=100, condition='condition', execution=None) # 국내 조건부지정가 매수
            >>> stock.orderable_amount(price=100, condition='best', execution=None) # 국내 최유리지정가 매수
            >>> stock.orderable_amount(price=100, condition='priority', execution=None) # 국내 최우선지정가 매수
            >>> stock.orderable_amount(price=100, condition='extended', execution=None) # 국내 시간외단일가 매수
            >>> stock.orderable_amount(price=None, condition='before', execution=None) # 국내 장전시간외 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=None, condition='after', execution=None) # 국내 장후시간외 매수
            >>> stock.orderable_amount(price=100, condition=None, execution='IOC') # 국내 IOC지정가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=100, condition=None, execution='FOK') # 국내 FOK지정가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=None, condition=None, execution='IOC') # 국내 IOC시장가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=None, condition=None, execution='FOK') # 국내 FOK시장가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=100, condition='best', execution='IOC') # 국내 IOC최유리 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=100, condition='best', execution='FOK') # 국내 FOK최유리 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
            >>> stock.orderable_amount(price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수
            >>> stock.orderable_amount(price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수
            >>> stock.orderable_amount(price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수
            >>> stock.orderable_amount(price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수
            >>> stock.orderable_amount(price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수
            >>> stock.orderable_amount(price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 주문조건이 잘못된 경우
        """
        from pykis.api.account.orderable_amount import orderable_amount

        return orderable_amount(
            self.kis,
            account=(
                account.account if isinstance(account, KisAccountScope) else (account or self.kis.primary)
            ),
            market=self.market,
            code=self.code,
            price=price,
            condition=condition,
            execution=execution,
        )

    def order(
        self,
        order: "ORDER_TYPE",
        price: "ORDER_PRICE | None" = None,
        qty: Decimal | None = None,
        condition: "ORDER_CONDITION | None" = None,
        execution: "ORDER_EXECUTION_CONDITION | None" = None,
        include_foreign: bool = False,
        account: str | KisAccountNumber | None = None,
    ) -> "KisOrder":
        """
        한국투자증권 통합주식 주문

        국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
        해외주식주문 -> 해외주식 주문[v1_해외주식-001]

        Args:
            order (ORDER_TYPE): 주문종류
            price (ORDER_PRICE, optional): 주문가격
            qty (Decimal, optional): 주문수량
            condition (DOMESTIC_ORDER_CONDITION, optional): 주문조건
            execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
            include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부
            account (str | KisAccountNumber | None, optional): 계좌번호. None인 경우 기본 계좌 사용

        Examples:
            >>> order('buy', price=100, condition=None, execution=None) # 전체 지정가 매수
            >>> order('buy', price=None, condition=None, execution=None) # 전체 시장가 매수
            >>> order('sell', price=100, condition=None, execution=None) # 전체 지정가 매도
            >>> order('sell', price=None, condition=None, execution=None) # 전체 시장가 매도
            >>> order('buy', price=100, condition=None, execution=None) # 지정가 매수
            >>> order('buy', price=None, condition=None, execution=None) # 시장가 매수
            >>> order('buy', price=100, condition='condition', execution=None) # 조건부지정가 매수
            >>> order('buy', price=100, condition='best', execution=None) # 최유리지정가 매수
            >>> order('buy', price=100, condition='priority', execution=None) # 최우선지정가 매수
            >>> order('buy', price=100, condition='extended', execution=None) # 시간외단일가 매수 (모의투자 미지원)
            >>> order('buy', price=None, condition='before', execution=None) # 장전시간외 매수 (모의투자 미지원)
            >>> order('buy', price=None, condition='after', execution=None) # 장후시간외 매수 (모의투자 미지원)
            >>> order('buy', price=100, condition=None, execution='IOC') # IOC지정가 매수 (모의투자 미지원)
            >>> order('buy', price=100, condition=None, execution='FOK') # FOK지정가 매수 (모의투자 미지원)
            >>> order('buy', price=None, condition=None, execution='IOC') # IOC시장가 매수 (모의투자 미지원)
            >>> order('buy', price=None, condition=None, execution='FOK') # FOK시장가 매수 (모의투자 미지원)
            >>> order('buy', price=100, condition='best', execution='IOC') # IOC최유리 매수 (모의투자 미지원)
            >>> order('buy', price=100, condition='best', execution='FOK') # FOK최유리 매수 (모의투자 미지원)
            >>> order('sell', price=100, condition=None, execution=None) # 지정가 매도
            >>> order('sell', price=None, condition=None, execution=None) # 시장가 매도
            >>> order('sell', price=100, condition='condition', execution=None) # 조건부지정가 매도
            >>> order('sell', price=100, condition='best', execution=None) # 최유리지정가 매도
            >>> order('sell', price=100, condition='priority', execution=None) # 최우선지정가 매도
            >>> order('sell', price=100, condition='extended', execution=None) # 시간외단일가 매도 (모의투자 미지원)
            >>> order('sell', price=None, condition='before', execution=None) # 장전시간외 매도 (모의투자 미지원)
            >>> order('sell', price=None, condition='after', execution=None) # 장후시간외 매도
            >>> order('sell', price=100, condition=None, execution='IOC') # IOC지정가 매도 (모의투자 미지원)
            >>> order('sell', price=100, condition=None, execution='FOK') # FOK지정가 매도 (모의투자 미지원)
            >>> order('sell', price=None, condition=None, execution='IOC') # IOC시장가 매도 (모의투자 미지원)
            >>> order('sell', price=None, condition=None, execution='FOK') # FOK시장가 매도 (모의투자 미지원)
            >>> order('sell', price=100, condition='best', execution='IOC') # IOC최유리 매도 (모의투자 미지원)
            >>> order('sell', price=100, condition='best', execution='FOK') # FOK최유리 매도 (모의투자 미지원)
            >>> order('buy', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
            >>> order('buy', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
            >>> order('buy', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
            >>> order('buy', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
            >>> order('buy', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
            >>> order('buy', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
            >>> order('buy', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
            >>> order('buy', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
            >>> order('buy', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
            >>> order('buy', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
            >>> order('buy', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
            >>> order('buy', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
            >>> order('sell', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매도 (모의투자 미지원)
            >>> order('sell', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매도 (모의투자 미지원)
            >>> order('sell', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매도 (모의투자 미지원)
            >>> order('sell', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매도 (모의투자 미지원)
            >>> order('sell', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매도 (모의투자 미지원)
            >>> order('sell', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매도 (모의투자 미지원)
            >>> order('sell', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매도 (모의투자 미지원)
            >>> order('sell', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매도 (모의투자 미지원)
            >>> order('sell', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매도 (모의투자 미지원)
            >>> order('sell', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매도 (모의투자 미지원)
            >>> order('sell', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매도 (모의투자 미지원)
            >>> order('sell', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매도 (모의투자 미지원)
            >>> order('buy', price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수 (모의투자 미지원)
            >>> order('buy', price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수 (모의투자 미지원)
            >>> order('buy', price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수 (모의투자 미지원)
            >>> order('buy', price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수 (모의투자 미지원)
            >>> order('buy', price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수 (모의투자 미지원)
            >>> order('buy', price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수 (모의투자 미지원)
            >>> order('sell', price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매도 (모의투자 미지원)
            >>> order('sell', price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매도 (모의투자 미지원)
            >>> order('sell', price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매도 (모의투자 미지원)
            >>> order('sell', price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매도 (모의투자 미지원)
            >>> order('sell', price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매도 (모의투자 미지원)
            >>> order('sell', price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매도 (모의투자 미지원)

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            KisMarketNotOpenedError: 시장이 열리지 않은 경우
            ValueError: 종목 코드가 올바르지 않은 경우
        """
        from pykis.api.account.order import order as _order
        from pykis.scope.account.account import KisAccountScope

        return _order(
            self.kis,
            account=(
                account.account if isinstance(account, KisAccountScope) else (account or self.kis.primary)
            ),
            market=self.market,
            code=self.code,
            order=order,
            price=price,
            qty=qty,
            condition=condition,
            execution=execution,
            include_foreign=include_foreign,
        )

    def buy(
        self,
        price: "ORDER_PRICE | None" = None,
        qty: Decimal | None = None,
        condition: "ORDER_CONDITION | None" = None,
        execution: "ORDER_EXECUTION_CONDITION | None" = None,
        include_foreign: bool = False,
        account: str | KisAccountNumber | None = None,
    ) -> "KisOrder":
        """
        한국투자증권 통합주식 매수 주문

        국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
        해외주식주문 -> 해외주식 주문[v1_해외주식-001]

        Args:
            price (ORDER_PRICE, optional): 주문가격
            qty (Decimal, optional): 주문수량
            condition (ORDER_CONDITION, optional): 주문조건
            execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
            include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부
            account (str | KisAccountNumber | None, optional): 계좌번호. None인 경우 기본 계좌 사용

        Examples:
            >>> order(price=100, condition=None, execution=None) # 전체 지정가 매수
            >>> order(price=None, condition=None, execution=None) # 전체 시장가 매수
            >>> order(price=100, condition=None, execution=None) # 지정가 매수
            >>> order(price=None, condition=None, execution=None) # 시장가 매수
            >>> order(price=100, condition='condition', execution=None) # 조건부지정가 매수
            >>> order(price=100, condition='best', execution=None) # 최유리지정가 매수
            >>> order(price=100, condition='priority', execution=None) # 최우선지정가 매수
            >>> order(price=100, condition='extended', execution=None) # 시간외단일가 매수 (모의투자 미지원)
            >>> order(price=None, condition='before', execution=None) # 장전시간외 매수 (모의투자 미지원)
            >>> order(price=None, condition='after', execution=None) # 장후시간외 매수 (모의투자 미지원)
            >>> order(price=100, condition=None, execution='IOC') # IOC지정가 매수 (모의투자 미지원)
            >>> order(price=100, condition=None, execution='FOK') # FOK지정가 매수 (모의투자 미지원)
            >>> order(price=None, condition=None, execution='IOC') # IOC시장가 매수 (모의투자 미지원)
            >>> order(price=None, condition=None, execution='FOK') # FOK시장가 매수 (모의투자 미지원)
            >>> order(price=100, condition='best', execution='IOC') # IOC최유리 매수 (모의투자 미지원)
            >>> order(price=100, condition='best', execution='FOK') # FOK최유리 매수 (모의투자 미지원)
            >>> order(price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
            >>> order(price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
            >>> order(price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
            >>> order(price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
            >>> order(price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
            >>> order(price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
            >>> order(price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
            >>> order(price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
            >>> order(price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
            >>> order(price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
            >>> order(price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
            >>> order(price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
            >>> order(price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수 (모의투자 미지원)
            >>> order(price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수 (모의투자 미지원)
            >>> order(price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수 (모의투자 미지원)
            >>> order(price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수 (모의투자 미지원)
            >>> order(price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수 (모의투자 미지원)
            >>> order(price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수 (모의투자 미지원)

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            KisMarketNotOpenedError: 시장이 열리지 않은 경우
            ValueError: 종목 코드가 올바르지 않은 경우
        """
        return self.order(
            "buy",
            price=price,
            qty=qty,
            condition=condition,
            execution=execution,
            include_foreign=include_foreign,
            account=account,
        )

    def sell(
        self,
        price: "ORDER_PRICE | None" = None,
        qty: Decimal | None = None,
        condition: "ORDER_CONDITION | None" = None,
        execution: "ORDER_EXECUTION_CONDITION | None" = None,
        account: str | KisAccountNumber | None = None,
    ) -> "KisOrder":
        """
        한국투자증권 통합주식 매도 주문

        국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
        해외주식주문 -> 해외주식 주문[v1_해외주식-001]

        Args:
            order (ORDER_TYPE): 주문종류
            price (ORDER_PRICE, optional): 주문가격
            qty (Decimal, optional): 주문수량
            condition (DOMESTIC_ORDER_CONDITION, optional): 주문조건
            execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
            account (str | KisAccountNumber | None, optional): 계좌번호. None인 경우 기본 계좌 사용

        Examples:
            >>> order(price=100, condition=None, execution=None) # 전체 지정가 매도
            >>> order(price=None, condition=None, execution=None) # 전체 시장가 매도
            >>> order(price=100, condition=None, execution=None) # 지정가 매도
            >>> order(price=None, condition=None, execution=None) # 시장가 매도
            >>> order(price=100, condition='condition', execution=None) # 조건부지정가 매도
            >>> order(price=100, condition='best', execution=None) # 최유리지정가 매도
            >>> order(price=100, condition='priority', execution=None) # 최우선지정가 매도
            >>> order(price=100, condition='extended', execution=None) # 시간외단일가 매도 (모의투자 미지원)
            >>> order(price=None, condition='before', execution=None) # 장전시간외 매도 (모의투자 미지원)
            >>> order(price=None, condition='after', execution=None) # 장후시간외 매도
            >>> order(price=100, condition=None, execution='IOC') # IOC지정가 매도 (모의투자 미지원)
            >>> order(price=100, condition=None, execution='FOK') # FOK지정가 매도 (모의투자 미지원)
            >>> order(price=None, condition=None, execution='IOC') # IOC시장가 매도 (모의투자 미지원)
            >>> order(price=None, condition=None, execution='FOK') # FOK시장가 매도 (모의투자 미지원)
            >>> order(price=100, condition='best', execution='IOC') # IOC최유리 매도 (모의투자 미지원)
            >>> order(price=100, condition='best', execution='FOK') # FOK최유리 매도 (모의투자 미지원)
            >>> order(price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매도 (모의투자 미지원)
            >>> order(price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매도 (모의투자 미지원)
            >>> order(price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매도 (모의투자 미지원)
            >>> order(price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매도 (모의투자 미지원)
            >>> order(price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매도 (모의투자 미지원)
            >>> order(price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매도 (모의투자 미지원)
            >>> order(price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매도 (모의투자 미지원)
            >>> order(price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매도 (모의투자 미지원)
            >>> order(price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매도 (모의투자 미지원)
            >>> order(price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매도 (모의투자 미지원)
            >>> order(price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매도 (모의투자 미지원)
            >>> order(price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매도 (모의투자 미지원)
            >>> order(price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매도 (모의투자 미지원)
            >>> order(price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매도 (모의투자 미지원)
            >>> order(price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매도 (모의투자 미지원)
            >>> order(price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매도 (모의투자 미지원)
            >>> order(price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매도 (모의투자 미지원)
            >>> order(price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매도 (모의투자 미지원)

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            KisMarketNotOpenedError: 시장이 열리지 않은 경우
            ValueError: 종목 코드가 올바르지 않은 경우
        """
        return self.order(
            "sell",
            price=price,
            qty=qty,
            condition=condition,
            execution=execution,
            account=account,
        )
