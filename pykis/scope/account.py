from datetime import date
from typing import TYPE_CHECKING, Protocol

from pykis.api.account.balance import KisBalance
from pykis.api.account.daily_order import KisDailyOrders
from pykis.api.account.order import (
    ORDER_CONDITION,
    ORDER_EXECUTION,
    ORDER_PRICE,
    ORDER_QUANTITY,
    ORDER_TYPE,
    KisOrder,
    KisOrderNumber,
    KisOrderNumberBase,
)
from pykis.api.account.order_profit import KisOrderProfits
from pykis.api.account.orderable_amount import KisOrderableAmountResponse
from pykis.api.account.pending_order import KisPendingOrders
from pykis.api.base.account import KisAccountBase, KisAccountProtocol
from pykis.api.stock.info import COUNTRY_TYPE
from pykis.api.stock.market import MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.scope.base import KisScope, KisScopeBase
from pykis.utils.params import EMPTY, EMPTY_TYPE

if TYPE_CHECKING:
    from pykis.kis import PyKis

__all__ = [
    "KisAccount",
    "KisAccountScope",
]


class KisAccount(KisScope, KisAccountProtocol, Protocol):
    """한국투자증권 계좌 Base Scope"""

    def balance(
        self: "KisAccountProtocol",
        country: COUNTRY_TYPE | None = None,
    ) -> KisBalance:
        """
        한국투자증권 통합주식 잔고 조회

        국내주식주문 -> 주식잔고조회[v1_국내주식-006]
        해외주식주문 -> 해외주식 체결기준현재잔고[v1_해외주식-008] (실전투자, 모의투자)
        해외주식주문 -> 해외주식 잔고[v1_해외주식-006] (모의투자)
        (업데이트 날짜: 2024/03/30)

        Args:
            country (COUNTRY_TYPE, optional): 국가코드

        Raises:
            KisAPIError: API 호출에 실패한 경우
            ValueError: 계좌번호가 잘못된 경우
        """
        raise NotImplementedError

    def daily_orders(
        self: "KisAccountProtocol",
        start: date,
        end: date,
        country: COUNTRY_TYPE | None = None,
    ) -> KisDailyOrders:
        """
        한국투자증권 통합일별 체결내역 조회

        국내주식주문 -> 주식일별주문체결조회[v1_국내주식-005]
        국내주식주문 -> 해외주식 주문체결내역[v1_해외주식-007]

        Args:
            start (date): 조회 시작일
            end (date): 조회 종료일
            country (COUNTRY_TYPE, optional): 국가코드

        Raises:
            KisAPIError: API 호출에 실패한 경우
            ValueError: 계좌번호가 잘못된 경우
        """
        raise NotImplementedError

    def buy(
        self: "KisAccountProtocol",
        market: MARKET_TYPE,
        symbol: str,
        price: ORDER_PRICE | None = None,
        qty: ORDER_QUANTITY | None = None,
        condition: ORDER_CONDITION | None = None,
        execution: ORDER_EXECUTION | None = None,
        include_foreign: bool = False,
    ) -> KisOrder:
        """
        한국투자증권 통합주식 매수 주문

        국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
        해외주식주문 -> 해외주식 주문[v1_해외주식-001]

        Args:
            market (MARKET_TYPE): 시장
            symbol (str): 종목코드
            price (ORDER_PRICE, optional): 주문가격
            qty (ORDER_QUANTITY, optional): 주문수량
            condition (DOMESTIC_ORDER_CONDITION, optional): 주문조건
            execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
            include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부

        Examples:
            >>> buy(전체, code, price=100, condition=None, execution=None) # 전체 지정가 매수
            >>> buy(전체, code, price=None, condition=None, execution=None) # 전체 시장가 매수
            >>> buy('KRX', code, price=100, condition=None, execution=None) # 지정가 매수
            >>> buy('KRX', code, price=None, condition=None, execution=None) # 시장가 매수
            >>> buy('KRX', code, price=100, condition='condition', execution=None) # 조건부지정가 매수
            >>> buy('KRX', code, price=100, condition='best', execution=None) # 최유리지정가 매수
            >>> buy('KRX', code, price=100, condition='priority', execution=None) # 최우선지정가 매수
            >>> buy('KRX', code, price=100, condition='extended', execution=None) # 시간외단일가 매수 (모의투자 미지원)
            >>> buy('KRX', code, price=None, condition='before', execution=None) # 장전시간외 매수 (모의투자 미지원)
            >>> buy('KRX', code, price=None, condition='after', execution=None) # 장후시간외 매수 (모의투자 미지원)
            >>> buy('KRX', code, price=100, condition=None, execution='IOC') # IOC지정가 매수 (모의투자 미지원)
            >>> buy('KRX', code, price=100, condition=None, execution='FOK') # FOK지정가 매수 (모의투자 미지원)
            >>> buy('KRX', code, price=None, condition=None, execution='IOC') # IOC시장가 매수 (모의투자 미지원)
            >>> buy('KRX', code, price=None, condition=None, execution='FOK') # FOK시장가 매수 (모의투자 미지원)
            >>> buy('KRX', code, price=100, condition='best', execution='IOC') # IOC최유리 매수 (모의투자 미지원)
            >>> buy('KRX', code, price=100, condition='best', execution='FOK') # FOK최유리 매수 (모의투자 미지원)
            >>> buy('NASD', code, price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
            >>> buy('NASD', code, price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
            >>> buy('NASD', code, price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
            >>> buy('NASD', code, price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
            >>> buy('NYSE', code, price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
            >>> buy('NYSE', code, price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
            >>> buy('NYSE', code, price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
            >>> buy('NYSE', code, price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
            >>> buy('AMEX', code, price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
            >>> buy('AMEX', code, price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
            >>> buy('AMEX', code, price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
            >>> buy('AMEX', code, price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
            >>> buy('NASD', code, price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수 (모의투자 미지원)
            >>> buy('NYSE', code, price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수 (모의투자 미지원)
            >>> buy('AMEX', code, price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수 (모의투자 미지원)
            >>> buy('NASD', code, price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수 (모의투자 미지원)
            >>> buy('NYSE', code, price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수 (모의투자 미지원)
            >>> buy('AMEX', code, price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수 (모의투자 미지원)

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            KisMarketNotOpenedError: 시장이 열리지 않은 경우
            ValueError: 종목 코드가 올바르지 않은 경우
        """
        raise NotImplementedError

    def sell(
        self: "KisAccountProtocol",
        market: MARKET_TYPE,
        symbol: str,
        price: ORDER_PRICE | None = None,
        qty: ORDER_QUANTITY | None = None,
        condition: ORDER_CONDITION | None = None,
        execution: ORDER_EXECUTION | None = None,
        include_foreign: bool = False,
    ) -> KisOrder:
        """
        한국투자증권 통합주식 매도 주문

        국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
        해외주식주문 -> 해외주식 주문[v1_해외주식-001]

        Args:
            market (MARKET_TYPE): 시장
            symbol (str): 종목코드
            price (ORDER_PRICE, optional): 주문가격
            qty (ORDER_QUANTITY, optional): 주문수량
            condition (DOMESTIC_ORDER_CONDITION, optional): 주문조건
            execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
            include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부

        Examples:
            >>> sell(전체, code, price=100, condition=None, execution=None) # 전체 지정가 매도
            >>> sell(전체, code, price=None, condition=None, execution=None) # 전체 시장가 매도
            >>> sell('KRX', code, price=100, condition=None, execution=None) # 지정가 매도
            >>> sell('KRX', code, price=None, condition=None, execution=None) # 시장가 매도
            >>> sell('KRX', code, price=100, condition='condition', execution=None) # 조건부지정가 매도
            >>> sell('KRX', code, price=100, condition='best', execution=None) # 최유리지정가 매도
            >>> sell('KRX', code, price=100, condition='priority', execution=None) # 최우선지정가 매도
            >>> sell('KRX', code, price=100, condition='extended', execution=None) # 시간외단일가 매도 (모의투자 미지원)
            >>> sell('KRX', code, price=None, condition='before', execution=None) # 장전시간외 매도 (모의투자 미지원)
            >>> sell('KRX', code, price=None, condition='after', execution=None) # 장후시간외 매도
            >>> sell('KRX', code, price=100, condition=None, execution='IOC') # IOC지정가 매도 (모의투자 미지원)
            >>> sell('KRX', code, price=100, condition=None, execution='FOK') # FOK지정가 매도 (모의투자 미지원)
            >>> sell('KRX', code, price=None, condition=None, execution='IOC') # IOC시장가 매도 (모의투자 미지원)
            >>> sell('KRX', code, price=None, condition=None, execution='FOK') # FOK시장가 매도 (모의투자 미지원)
            >>> sell('KRX', code, price=100, condition='best', execution='IOC') # IOC최유리 매도 (모의투자 미지원)
            >>> sell('KRX', code, price=100, condition='best', execution='FOK') # FOK최유리 매도 (모의투자 미지원)
            >>> sell('NASD', code, price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매도 (모의투자 미지원)
            >>> sell('NASD', code, price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매도 (모의투자 미지원)
            >>> sell('NASD', code, price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매도 (모의투자 미지원)
            >>> sell('NASD', code, price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매도 (모의투자 미지원)
            >>> sell('NYSE', code, price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매도 (모의투자 미지원)
            >>> sell('NYSE', code, price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매도 (모의투자 미지원)
            >>> sell('NYSE', code, price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매도 (모의투자 미지원)
            >>> sell('NYSE', code, price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매도 (모의투자 미지원)
            >>> sell('AMEX', code, price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매도 (모의투자 미지원)
            >>> sell('AMEX', code, price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매도 (모의투자 미지원)
            >>> sell('AMEX', code, price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매도 (모의투자 미지원)
            >>> sell('AMEX', code, price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매도 (모의투자 미지원)
            >>> sell('NASD', code, price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매도 (모의투자 미지원)
            >>> sell('NYSE', code, price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매도 (모의투자 미지원)
            >>> sell('AMEX', code, price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매도 (모의투자 미지원)
            >>> sell('NASD', code, price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매도 (모의투자 미지원)
            >>> sell('NYSE', code, price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매도 (모의투자 미지원)
            >>> sell('AMEX', code, price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매도 (모의투자 미지원)

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            KisMarketNotOpenedError: 시장이 열리지 않은 경우
            ValueError: 종목 코드가 올바르지 않은 경우
        """
        raise NotImplementedError

    def order(
        self: "KisAccountProtocol",
        market: MARKET_TYPE,
        symbol: str,
        order: ORDER_TYPE,
        price: ORDER_PRICE | None = None,
        qty: ORDER_QUANTITY | None = None,
        condition: ORDER_CONDITION | None = None,
        execution: ORDER_EXECUTION | None = None,
        include_foreign: bool = False,
    ) -> KisOrder:
        """
        한국투자증권 통합주식 주문

        국내주식주문 -> 주식주문(현금)[v1_국내주식-001]
        해외주식주문 -> 해외주식 주문[v1_해외주식-001]

        Args:
            market (MARKET_TYPE): 시장
            symbol (str): 종목코드
            order (ORDER_TYPE): 주문종류
            price (ORDER_PRICE, optional): 주문가격
            qty (ORDER_QUANTITY, optional): 주문수량
            condition (DOMESTIC_ORDER_CONDITION, optional): 주문조건
            execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
            include_foreign (bool, optional): 전량 주문시 외화 주문가능금액 포함 여부

        Examples:
            >>> order(전체, code, order='buy', price=100, condition=None, execution=None) # 전체 지정가 매수
            >>> order(전체, code, order='buy', price=None, condition=None, execution=None) # 전체 시장가 매수
            >>> order(전체, code, order='sell', price=100, condition=None, execution=None) # 전체 지정가 매도
            >>> order(전체, code, order='sell', price=None, condition=None, execution=None) # 전체 시장가 매도
            >>> order('KRX', code, order='buy', price=100, condition=None, execution=None) # 지정가 매수
            >>> order('KRX', code, order='buy', price=None, condition=None, execution=None) # 시장가 매수
            >>> order('KRX', code, order='buy', price=100, condition='condition', execution=None) # 조건부지정가 매수
            >>> order('KRX', code, order='buy', price=100, condition='best', execution=None) # 최유리지정가 매수
            >>> order('KRX', code, order='buy', price=100, condition='priority', execution=None) # 최우선지정가 매수
            >>> order('KRX', code, order='buy', price=100, condition='extended', execution=None) # 시간외단일가 매수 (모의투자 미지원)
            >>> order('KRX', code, order='buy', price=None, condition='before', execution=None) # 장전시간외 매수 (모의투자 미지원)
            >>> order('KRX', code, order='buy', price=None, condition='after', execution=None) # 장후시간외 매수 (모의투자 미지원)
            >>> order('KRX', code, order='buy', price=100, condition=None, execution='IOC') # IOC지정가 매수 (모의투자 미지원)
            >>> order('KRX', code, order='buy', price=100, condition=None, execution='FOK') # FOK지정가 매수 (모의투자 미지원)
            >>> order('KRX', code, order='buy', price=None, condition=None, execution='IOC') # IOC시장가 매수 (모의투자 미지원)
            >>> order('KRX', code, order='buy', price=None, condition=None, execution='FOK') # FOK시장가 매수 (모의투자 미지원)
            >>> order('KRX', code, order='buy', price=100, condition='best', execution='IOC') # IOC최유리 매수 (모의투자 미지원)
            >>> order('KRX', code, order='buy', price=100, condition='best', execution='FOK') # FOK최유리 매수 (모의투자 미지원)
            >>> order('KRX', code, order='sell', price=100, condition=None, execution=None) # 지정가 매도
            >>> order('KRX', code, order='sell', price=None, condition=None, execution=None) # 시장가 매도
            >>> order('KRX', code, order='sell', price=100, condition='condition', execution=None) # 조건부지정가 매도
            >>> order('KRX', code, order='sell', price=100, condition='best', execution=None) # 최유리지정가 매도
            >>> order('KRX', code, order='sell', price=100, condition='priority', execution=None) # 최우선지정가 매도
            >>> order('KRX', code, order='sell', price=100, condition='extended', execution=None) # 시간외단일가 매도 (모의투자 미지원)
            >>> order('KRX', code, order='sell', price=None, condition='before', execution=None) # 장전시간외 매도 (모의투자 미지원)
            >>> order('KRX', code, order='sell', price=None, condition='after', execution=None) # 장후시간외 매도
            >>> order('KRX', code, order='sell', price=100, condition=None, execution='IOC') # IOC지정가 매도 (모의투자 미지원)
            >>> order('KRX', code, order='sell', price=100, condition=None, execution='FOK') # FOK지정가 매도 (모의투자 미지원)
            >>> order('KRX', code, order='sell', price=None, condition=None, execution='IOC') # IOC시장가 매도 (모의투자 미지원)
            >>> order('KRX', code, order='sell', price=None, condition=None, execution='FOK') # FOK시장가 매도 (모의투자 미지원)
            >>> order('KRX', code, order='sell', price=100, condition='best', execution='IOC') # IOC최유리 매도 (모의투자 미지원)
            >>> order('KRX', code, order='sell', price=100, condition='best', execution='FOK') # FOK최유리 매도 (모의투자 미지원)
            >>> order('NASD', code, order='buy', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
            >>> order('NASD', code, order='buy', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
            >>> order('NASD', code, order='buy', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
            >>> order('NASD', code, order='buy', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
            >>> order('NYSE', code, order='buy', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
            >>> order('NYSE', code, order='buy', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
            >>> order('NYSE', code, order='buy', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
            >>> order('NYSE', code, order='buy', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
            >>> order('AMEX', code, order='buy', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
            >>> order('AMEX', code, order='buy', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
            >>> order('AMEX', code, order='buy', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
            >>> order('AMEX', code, order='buy', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
            >>> order('NASD', code, order='sell', price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매도 (모의투자 미지원)
            >>> order('NASD', code, order='sell', price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매도 (모의투자 미지원)
            >>> order('NASD', code, order='sell', price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매도 (모의투자 미지원)
            >>> order('NASD', code, order='sell', price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매도 (모의투자 미지원)
            >>> order('NYSE', code, order='sell', price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매도 (모의투자 미지원)
            >>> order('NYSE', code, order='sell', price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매도 (모의투자 미지원)
            >>> order('NYSE', code, order='sell', price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매도 (모의투자 미지원)
            >>> order('NYSE', code, order='sell', price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매도 (모의투자 미지원)
            >>> order('AMEX', code, order='sell', price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매도 (모의투자 미지원)
            >>> order('AMEX', code, order='sell', price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매도 (모의투자 미지원)
            >>> order('AMEX', code, order='sell', price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매도 (모의투자 미지원)
            >>> order('AMEX', code, order='sell', price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매도 (모의투자 미지원)
            >>> order('NASD', code, order='buy', price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수 (모의투자 미지원)
            >>> order('NYSE', code, order='buy', price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수 (모의투자 미지원)
            >>> order('AMEX', code, order='buy', price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수 (모의투자 미지원)
            >>> order('NASD', code, order='buy', price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수 (모의투자 미지원)
            >>> order('NYSE', code, order='buy', price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수 (모의투자 미지원)
            >>> order('AMEX', code, order='buy', price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수 (모의투자 미지원)
            >>> order('NASD', code, order='sell', price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매도 (모의투자 미지원)
            >>> order('NYSE', code, order='sell', price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매도 (모의투자 미지원)
            >>> order('AMEX', code, order='sell', price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매도 (모의투자 미지원)
            >>> order('NASD', code, order='sell', price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매도 (모의투자 미지원)
            >>> order('NYSE', code, order='sell', price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매도 (모의투자 미지원)
            >>> order('AMEX', code, order='sell', price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매도 (모의투자 미지원)

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            KisMarketNotOpenedError: 시장이 열리지 않은 경우
            ValueError: 종목 코드가 올바르지 않은 경우
        """
        raise NotImplementedError

    def modify(
        self: "KisAccountProtocol",
        order: KisOrderNumber,
        price: ORDER_PRICE | None | EMPTY_TYPE = EMPTY,
        qty: ORDER_QUANTITY | None = None,
        condition: ORDER_CONDITION | None | EMPTY_TYPE = EMPTY,
        execution: ORDER_EXECUTION | None | EMPTY_TYPE = EMPTY,
    ) -> KisOrder:
        """
        한국투자증권 통합 주식 주문정정 (국내 모의투자 미지원, 해외 주간거래 모의투자 미지원)

        국내주식주문 -> 주식주문(정정취소)[v1_국내주식-003]
        국내주식주문 -> 해외주식 정정취소주문[v1_해외주식-003]
        (업데이트 날짜: 2024/04/02)

        Args:
            account (str | KisAccountNumber): 계좌번호
            order (KisOrderNumber): 주문번호
            price (ORDER_PRICE, optional): 주문가격
            qty (ORDER_QUANTITY, optional): 주문수량
            condition (ORDER_CONDITION, optional): 주문조건
            execution (ORDER_EXECUTION_CONDITION, optional): 체결조건
        """
        raise NotImplementedError

    def cancel(
        self: "KisAccountProtocol",
        order: KisOrderNumber,
    ) -> KisOrder:
        """
        한국투자증권 통합 주식 주문취소 (해외 주간거래 모의투자 미지원)

        국내주식주문 -> 주식주문(정정취소)[v1_국내주식-003]
        국내주식주문 -> 해외주식 정정취소주문[v1_해외주식-003]
        (업데이트 날짜: 2024/04/02)

        Args:
            account (str | KisAccountNumber): 계좌번호
            order (KisOrderNumber): 주문번호
        """
        raise NotImplementedError

    def profits(
        self: "KisAccountProtocol",
        start: date,
        end: date,
        country: COUNTRY_TYPE | None = None,
    ) -> KisOrderProfits:
        """
        한국투자증권 통합 기간 손익 조회

        국내주식주문 -> 기간별매매손익현황조회[v1_국내주식-060] (모의투자 미지원)
        국내주식주문 -> 해외주식 기간손익[v1_해외주식-032] (모의투자 미지원)
        (업데이트 날짜: 2024/04/03)

        Args:
            account (str | KisAccountNumber): 계좌번호
            start (date): 조회 시작일
            end (date): 조회 종료일
            country (COUNTRY_TYPE, optional): 국가

        Raises:
            KisAPIError: API 호출에 실패한 경우
            ValueError: 계좌번호가 잘못된 경우
        """
        raise NotImplementedError

    def orderable_amount(
        self: "KisAccountProtocol",
        market: MARKET_TYPE,
        symbol: str,
        price: ORDER_PRICE | None = None,
        condition: ORDER_CONDITION | None = None,
        execution: ORDER_EXECUTION | None = None,
    ) -> KisOrderableAmountResponse:
        """
        한국투자증권 주문가능금액 조회

        국내주식주문 -> 매수가능조회[v1_국내주식-007]
        해외주식주문 -> 해외주식 매수가능금액조회[v1_해외주식-014]

        Args:
            market (MARKET_TYPE): 시장코드
            symbol (str): 종목코드
            price (int | None, optional): 주문가격. None인 경우 시장가 주문
            condition (ORDER_CONDITION | None, optional): 주문조건
            execution (ORDER_EXECUTION_CONDITION | None, optional): 체결조건

        Examples:
            >>> orderable_amount(전체, code, price=100, condition=None, execution=None) # 전체 지정가 매수
            >>> orderable_amount(전체, code, price=None, condition=None, execution=None) # 전체 시장가 매수
            >>> orderable_amount("KRX", code, price=100, condition='condition', execution=None) # 국내 조건부지정가 매수
            >>> orderable_amount("KRX", code, price=100, condition='best', execution=None) # 국내 최유리지정가 매수
            >>> orderable_amount("KRX", code, price=100, condition='priority', execution=None) # 국내 최우선지정가 매수
            >>> orderable_amount("KRX", code, price=100, condition='extended', execution=None) # 국내 시간외단일가 매수 (모의투자 미지원)
            >>> orderable_amount("KRX", code, price=None, condition='before', execution=None) # 국내 장전시간외 매수
            >>> orderable_amount("KRX", code, price=None, condition='after', execution=None) # 국내 장후시간외 매수
            >>> orderable_amount("KRX", code, price=100, condition=None, execution='IOC') # 국내 IOC지정가 매수 (모의투자 미지원)
            >>> orderable_amount("KRX", code, price=100, condition=None, execution='FOK') # 국내 FOK지정가 매수 (모의투자 미지원)
            >>> orderable_amount("KRX", code, price=None, condition=None, execution='IOC') # 국내 IOC시장가 매수 (모의투자 미지원)
            >>> orderable_amount("KRX", code, price=None, condition=None, execution='FOK') # 국내 FOK시장가 매수 (모의투자 미지원)
            >>> orderable_amount("KRX", code, price=100, condition='best', execution='IOC') # 국내 IOC최유리 매수 (모의투자 미지원)
            >>> orderable_amount("KRX", code, price=100, condition='best', execution='FOK') # 국내 FOK최유리 매수 (모의투자 미지원)
            >>> orderable_amount('NASD', code, price=100, condition='LOO', execution=None) # 나스닥 장개시지정가 매수 (모의투자 미지원)
            >>> orderable_amount('NASD', code, price=100, condition='LOC', execution=None) # 나스닥 장마감지정가 매수 (모의투자 미지원)
            >>> orderable_amount('NASD', code, price=None, condition='MOO', execution=None) # 나스닥 장개시시장가 매수 (모의투자 미지원)
            >>> orderable_amount('NASD', code, price=None, condition='MOC', execution=None) # 나스닥 장마감시장가 매수 (모의투자 미지원)
            >>> orderable_amount('NYSE', code, price=100, condition='LOO', execution=None) # 뉴욕 장개시지정가 매수 (모의투자 미지원)
            >>> orderable_amount('NYSE', code, price=100, condition='LOC', execution=None) # 뉴욕 장마감지정가 매수 (모의투자 미지원)
            >>> orderable_amount('NYSE', code, price=None, condition='MOO', execution=None) # 뉴욕 장개시시장가 매수 (모의투자 미지원)
            >>> orderable_amount('NYSE', code, price=None, condition='MOC', execution=None) # 뉴욕 장마감시장가 매수 (모의투자 미지원)
            >>> orderable_amount('AMEX', code, price=100, condition='LOO', execution=None) # 아멕스 장개시지정가 매수 (모의투자 미지원)
            >>> orderable_amount('AMEX', code, price=100, condition='LOC', execution=None) # 아멕스 장마감지정가 매수 (모의투자 미지원)
            >>> orderable_amount('AMEX', code, price=None, condition='MOO', execution=None) # 아멕스 장개시시장가 매수 (모의투자 미지원)
            >>> orderable_amount('AMEX', code, price=None, condition='MOC', execution=None) # 아멕스 장마감시장가 매수 (모의투자 미지원)
            >>> orderable_amount('NASD', code, price=100, condition='extended', execution=None) # 나스닥 주간거래 지정가 매수
            >>> orderable_amount('NASD', code, price=None, condition='extended', execution=None) # 나스닥 주간거래 시장가 매수
            >>> orderable_amount('NYSE', code, price=100, condition='extended', execution=None) # 뉴욕 주간거래 지정가 매수
            >>> orderable_amount('NYSE', code, price=None, condition='extended', execution=None) # 뉴욕 주간거래 시장가 매수
            >>> orderable_amount('AMEX', code, price=100, condition='extended', execution=None) # 아멕스 주간거래 지정가 매수
            >>> orderable_amount('AMEX', code, price=None, condition='extended', execution=None) # 아멕스 주간거래 시장가 매수

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 주문조건이 잘못된 경우
        """
        raise NotImplementedError

    def pending_orders(
        self: "KisAccountProtocol",
        country: COUNTRY_TYPE | None = None,
    ) -> KisPendingOrders:
        """
        한국투자증권 통합 미체결 조회

        국내주식주문 -> 주식정정취소가능주문조회[v1_국내주식-004] (모의투자 미지원)
        해외주식주문 -> 해외주식 미체결내역[v1_해외주식-005]
        (업데이트 날짜: 2024/04/01)

        Args:
            country (COUNTRY_TYPE, optional): 국가코드

        Raises:
            KisAPIError: API 호출에 실패한 경우
            ValueError: 계좌번호가 잘못된 경우
        """
        raise NotImplementedError


class KisAccountScope(KisScopeBase, KisAccountBase):
    """한국투자증권 계좌 Base Scope"""

    account_number: KisAccountNumber
    """Scope에서 사용할 계좌 정보"""

    def __init__(self, kis: "PyKis", account: KisAccountNumber):
        super().__init__(kis=kis)
        self.account_number = account

    from pykis.api.account.balance import account_balance as balance  # 잔고 조회
    from pykis.api.account.daily_order import (
        account_daily_orders as daily_orders,  # 일별 체결내역 조회
    )
    from pykis.api.account.order import account_buy as buy  # 매수
    from pykis.api.account.order import account_order as order  # 주문
    from pykis.api.account.order import account_sell as sell  # 매도
    from pykis.api.account.order_modify import account_cancel_order as cancel  # 주문 취소
    from pykis.api.account.order_modify import account_modify_order as modify  # 주문 정정
    from pykis.api.account.order_profit import (
        account_order_profits as profits,  # 주문 수익률 조회
    )
    from pykis.api.account.orderable_amount import (
        account_orderable_amount as orderable_amount,  # 주문 가능 금액 조회
    )
    from pykis.api.account.pending_order import (
        account_pending_orders as pending_orders,  # 미체결 조회
    )


def account(
    self: "PyKis",
    account: str | KisAccountNumber | None = None,
    primary: bool = False,
) -> KisAccount:
    """계좌 정보를 반환합니다.

    Args:
        account: 계좌 번호. None이면 기본 계좌 정보를 사용합니다.
        primary: 기본 계좌로 설정할지 여부
    """
    if isinstance(account, str):
        account = KisAccountNumber(account)

    account = account or self.primary

    if primary:
        self.primary_account = account

    return KisAccountScope(
        kis=self,
        account=account,
    )
