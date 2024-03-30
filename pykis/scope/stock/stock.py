from decimal import Decimal
from typing import TYPE_CHECKING

from pykis.api.account.order import ORDER_CONDITION, ORDER_EXECUTION_CONDITION
from pykis.api.stock.market import MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.scope.base.product import KisProductScope

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisStock(KisProductScope):
    """한국투자증권 주식 Scope"""

    account_number: KisAccountNumber | None

    def __init__(
        self,
        kis: "PyKis",
        code: str,
        market: MARKET_TYPE,
        account: KisAccountNumber | None = None,
    ):
        super().__init__(kis=kis, market=market)
        self.code = code
        self.account_number = account

    @property
    def account(self) -> KisAccountNumber:
        """
        계좌 정보를 반환합니다. 스코프에 계좌 정보가 없는 경우 기본 계좌 정보를 반환합니다.

        Raises:
            ValueError: 스코프에 계좌 정보가 없으며, 기본 계좌 정보가 없을 경우
        """
        if self.account_number is None:
            return self.kis.primary

        return self.account_number

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self.code!r}, market={self.market!r}, account={self.account_number!r})"

    def orderable_amount(
        self,
        price: Decimal | None = None,
        condition: ORDER_CONDITION | None = None,
        execution: ORDER_EXECUTION_CONDITION | None = None,
    ):
        """
        한국투자증권 주문가능금액 조회

        국내주식주문 -> 매수가능조회[v1_국내주식-007]
        해외주식주문 -> 해외주식 매수가능금액조회[v1_해외주식-014]

        Args:
            price (int | None, optional): 주문가격. None인 경우 시장가 주문
            condition (ORDER_CONDITION | None, optional): 주문조건
            execution (ORDER_EXECUTION_CONDITION | None, optional): 채결조건

        Examples:
            >>> stock.orderable_amount(price=100, condition=None, execution=None) # 전체 지정가 매수
            >>> stock.orderable_amount(price=None, condition=None, execution=None) # 전체 시장가 매수
            >>> stock.orderable_amount(price=100, condition='condition', execution=None) # 국내 조건부지정가 매수
            >>> stock.orderable_amount(price=100, condition='best', execution=None) # 국내 최유리지정가 매수
            >>> stock.orderable_amount(price=100, condition='priority', execution=None) # 국내 최우선지정가 매수
            >>> stock.orderable_amount(price=100, condition='extended', execution=None) # 국내 시간외단일가 매수
            >>> stock.orderable_amount(price=None, condition='before', execution=None) # 국내 장전시간외 매수
            >>> stock.orderable_amount(price=None, condition='after', execution=None) # 국내 장후시간외 매수
            >>> stock.orderable_amount(price=100, condition=None, execution='IOC') # 국내 IOC지정가 매수
            >>> stock.orderable_amount(price=100, condition=None, execution='FOK') # 국내 FOK지정가 매수
            >>> stock.orderable_amount(price=None, condition=None, execution='IOC') # 국내 IOC시장가 매수
            >>> stock.orderable_amount(price=None, condition=None, execution='FOK') # 국내 FOK시장가 매수
            >>> stock.orderable_amount(price=100, condition='best', execution='IOC') # 국내 IOC최유리 매수
            >>> stock.orderable_amount(price=100, condition='best', execution='FOK') # 국내 FOK최유리 매수
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

        Raises:
            KisAPIError: API 호출에 실패한 경우
            KisNotFoundError: 조회 결과가 없는 경우
            ValueError: 주문조건이 잘못된 경우
        """
        from pykis.api.account.orderable_amount import orderable_amount

        return orderable_amount(
            self.kis,
            account=self.account,
            market=self.market,
            code=self.code,
            price=price,
            condition=condition,
            execution=execution,
        )
