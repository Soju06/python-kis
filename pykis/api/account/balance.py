from decimal import Decimal
from typing import TYPE_CHECKING

from pykis.api.base.account import KisAccountBase
from pykis.api.base.account_product import KisAccountProductBase
from pykis.api.stock.info import COUNTRY_TYPE, market_to_country, resolve_market
from pykis.api.stock.market import CURRENCY_TYPE, MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.client.page import KisPage
from pykis.responses.dynamic import KisDynamic, KisList, KisObject, KisTransform
from pykis.responses.response import KisAPIResponse, KisPaginationAPIResponse
from pykis.responses.types import KisAny, KisDecimal, KisString
from pykis.utils.cache import cached

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisBalanceStock(KisDynamic, KisAccountProductBase):
    """한국투자증권 보유종목"""

    balance: "KisBalance"
    """계좌잔고 (post initialization)"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    @property
    def name(self) -> str:
        """종목명"""
        return self.info.name

    @property
    def purchase_price(self) -> Decimal:
        """매입평균가"""
        return self.purchase_amount / self.quantity

    current_price: Decimal
    """현재가"""

    @property
    def price(self) -> Decimal:
        """현재가"""
        return self.current_price

    quantity: Decimal
    """수량"""

    orderable: Decimal
    """매도가능수량"""

    @property
    def qty(self) -> Decimal:
        """수량"""
        return self.quantity

    purchase_amount: Decimal
    """매입금액"""

    @property
    def current_amount(self) -> Decimal:
        """평가금액"""
        return self.current_price * self.quantity

    @property
    def amount(self) -> Decimal:
        """평가금액"""
        return self.current_amount

    @property
    def profit(self) -> Decimal:
        """손익금액"""
        return self.current_amount - self.purchase_amount

    @property
    def profit_rate(self) -> Decimal:
        """손익률 (-100 ~ 100)"""
        return self.profit / self.purchase_amount * 100

    @property
    def rate(self) -> Decimal:
        """수익률 (-100 ~ 100)"""
        return self.profit_rate

    currency: CURRENCY_TYPE
    """통화코드"""
    exchange_rate: Decimal
    """환율"""

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(account_number={self.account_number!r}, code={self.symbol!r}, market={self.market!r}, quantity={self.quantity}, purchase_price={self.purchase_price}, current_price={self.current_price}, profit={self.profit}, profit_rate={self.profit_rate})"

    def __repr__(self) -> str:
        return str(self)


class KisDeposit(KisDynamic, KisAccountBase):
    """한국투자증권 통화별 예수금"""

    account_number: KisAccountNumber
    """계좌번호"""

    currency: CURRENCY_TYPE
    """통화코드"""
    amount: Decimal
    """예수금"""
    withdrawable_amount: Decimal
    """출금가능금액"""

    @property
    def withdrawable(self) -> Decimal:
        """출금가능금액"""
        return self.withdrawable_amount

    exchange_rate: Decimal
    """환율"""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(account_number={self.account_number!r}, currency={self.currency!r}, amount={self.amount}, withdrawable_amount={self.withdrawable_amount}, exchange_rate={self.exchange_rate})"

    def __str__(self) -> str:
        return str(self)


class KisBalance(KisDynamic, KisAccountBase):
    """한국투자증권 계좌 잔고"""

    country: COUNTRY_TYPE | None
    """국가코드 (스코프 지정시)"""

    stocks: list[KisBalanceStock]
    """보유종목"""
    deposits: dict[CURRENCY_TYPE, KisDeposit]
    """통화별 예수금"""

    def __kis_post_init__(self):
        self._kis_spread(self.stocks)
        self._kis_spread(self.deposits)

    @property
    def amount(self) -> Decimal:
        """총자산금액 (원화, 보유종목 + 예수금)"""
        sum = self.current_amount

        for deposit in self.deposits.values():
            sum += deposit.amount * deposit.exchange_rate

        return sum

    @property
    def total(self) -> Decimal:
        """총평가금액 (원화, 보유종목 + 예수금)"""
        return self.amount

    @property
    def purchase_amount(self) -> Decimal:
        """총매입금액 (원화)"""
        sum = Decimal(0)

        for stock in self.stocks:
            if (deposit := self.deposits.get(stock.currency)) is not None:
                sum += stock.purchase_amount * deposit.exchange_rate

        return sum

    @property
    def current_amount(self) -> Decimal:
        """총평가금액 (원화)"""
        sum = Decimal(0)

        for stock in self.stocks:
            if (deposit := self.deposits.get(stock.currency)) is not None:
                sum += stock.current_amount * deposit.exchange_rate

        return sum

    @property
    def profit(self) -> Decimal:
        """총손익금액 (원화)"""
        return self.current_amount - self.purchase_amount

    @property
    def profit_rate(self) -> Decimal:
        """총손익률 (-100 ~ 100)"""
        return self.profit / self.purchase_amount * 100

    @property
    def withdrawable_amount(self) -> Decimal:
        """총출금가능금액 (원화)"""
        return Decimal(
            sum(deposit.withdrawable_amount * deposit.exchange_rate for deposit in self.deposits.values())
        ).quantize(Decimal("1"))

    @property
    def withdrawable(self) -> Decimal:
        """총출금가능금액 (원화)"""
        return self.withdrawable_amount

    def __iter__(self):
        return iter(self.stocks)

    def __len__(self):
        return len(self.stocks)

    def __getitem__(self, key: int | str) -> KisBalanceStock:
        """
        보유종목을 인덱스 또는 종목코드로 조회합니다.

        Args:
            key (int | str): 인덱스 또는 종목코드
        """
        if isinstance(key, int):
            return self.stocks[key]
        elif isinstance(key, str):
            for stock in self.stocks:
                if stock.symbol == key:
                    return stock
            raise KeyError(key)
        else:
            raise TypeError(key)

    def stock(self, symbol: str) -> KisBalanceStock | None:
        """보유종목을 종목코드로 조회합니다."""
        for stock in self.stocks:
            if stock.symbol == symbol:
                return stock

        return None

    def deposit(self, currency: CURRENCY_TYPE) -> KisDeposit | None:
        """통화별 예수금을 조회합니다."""
        return self.deposits.get(currency)

    def __repr__(self) -> str:
        nl = "\n    "
        nll = "\n        "
        return f"{self.__class__.__name__}({nl}account_number={self.account_number!r},{nl}deposits={{{nll}{(nll.join(f'{k}: {v!r}' for k, v in self.deposits.items()))}{nl}}}{nl}stocks=[{nll}{f',{nll}'.join(map(repr, self.stocks))}{nl}],{nl}withdrawable_amount={self.withdrawable_amount},{nl}purchase_amount={self.purchase_amount},{nl}current_amount={self.current_amount},{nl}profit={self.profit},{nl}profit_rate={self.profit_rate}\n)"


class KisDomesticBalanceStock(KisBalanceStock):
    """한국투자증권 국내종목 잔고"""

    symbol: str = KisString["pdno"]
    """종목코드"""
    market: MARKET_TYPE = "KRX"
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    name: str = KisString["prdt_name"]
    """종목명"""

    current_price: Decimal = KisDecimal["prpr"]
    """현재가"""

    quantity: Decimal = KisDecimal["hldg_qty"]
    """수량"""
    orderable: Decimal = KisDecimal["ord_psbl_qty"]
    """매도가능수량"""

    purchase_amount: Decimal = KisDecimal["pchs_amt"]
    """매입금액"""

    currency: CURRENCY_TYPE = "KRW"
    """통화코드"""
    exchange_rate: Decimal = Decimal(1)
    """환율"""


class KisDomesticDeposit(KisDeposit):
    """한국투자증권 국내종목 예수금"""

    account_number: KisAccountNumber
    """계좌번호"""

    currency: CURRENCY_TYPE = "KRW"
    """통화코드"""
    amount: Decimal = KisDecimal["dnca_tot_amt"]
    """예수금"""
    withdrawable_amount: Decimal = KisDecimal["dnca_tot_amt"]
    """출금가능금액"""

    exchange_rate: Decimal = Decimal(1)
    """환율"""


class KisDomesticBalance(KisPaginationAPIResponse, KisBalance):
    """한국투자증권 국내종목 잔고"""

    __path__ = None

    country: COUNTRY_TYPE | None = "KR"
    """국가코드 (스코프 지정시)"""

    stocks: list[KisDomesticBalanceStock] = KisList(KisDomesticBalanceStock)["output1"]
    """보유종목"""
    deposits: dict[CURRENCY_TYPE, KisDomesticDeposit] = KisAny(
        lambda x: {
            "KRW": KisObject.transform_(
                x[0],
                KisDomesticDeposit,
                ignore_missing=True,
            )
        }
    )["output2"]
    """통화별 예수금"""

    def __init__(self, account_number: KisAccountNumber):
        super().__init__()
        self.account_number = account_number

    def __post_init__(self) -> None:
        super().__post_init__()

        for stock in self.stocks:
            stock.balance = self
            stock.account_number = self.account_number

        for deposit in self.deposits.values():
            deposit.account_number = self.account_number


class KisOverseasPresentBalanceStock(KisBalanceStock):
    """한국투자증권 해외종목 잔고"""

    symbol: str = KisString["pdno"]
    """종목코드"""
    market: MARKET_TYPE = KisString["ovrs_excg_cd"]
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    name: str = KisString["prdt_name"]
    """종목명"""

    current_price: Decimal = KisDecimal["ovrs_now_pric1"]
    """현재가"""

    quantity: Decimal = KisDecimal["cblc_qty13"]
    """수량"""
    orderable: Decimal = KisDecimal["ord_psbl_qty1"]
    """매도가능수량"""

    purchase_amount: Decimal = KisDecimal["frcr_pchs_amt"]
    """매입금액"""

    currency: CURRENCY_TYPE = KisString["buy_crcy_cd"]
    """통화코드"""
    exchange_rate: Decimal = KisDecimal["bass_exrt"]
    """환율"""


class KisOverseasPresentDeposit(KisDeposit):
    """한국투자증권 국내종목 예수금"""

    account_number: KisAccountNumber
    """계좌번호"""

    currency: CURRENCY_TYPE = KisString["crcy_cd"]
    """통화코드"""
    amount: Decimal = KisDecimal["frcr_dncl_amt_2"]
    """예수금"""
    withdrawable_amount: Decimal = KisDecimal["frcr_drwg_psbl_amt_1"]
    """출금가능금액"""

    exchange_rate: Decimal = KisDecimal["frst_bltn_exrt"]
    """환율"""


class KisOverseasPresentBalance(KisAPIResponse, KisBalance):
    """한국투자증권 해외종목 잔고"""

    __path__ = None

    country: COUNTRY_TYPE | None
    """국가코드 (스코프 지정시)"""

    stocks: list[KisBalanceStock] = KisList(KisOverseasPresentBalanceStock)["output1"]
    """보유종목"""
    deposits: dict[CURRENCY_TYPE, KisDeposit] = KisAny(
        lambda x: {
            i["crcy_cd"]: KisObject.transform_(
                i,
                KisOverseasPresentDeposit,
                ignore_missing=True,
            )
            for i in x
        }
    )["output2"]
    """통화별 예수금"""

    def __init__(self, account_number: KisAccountNumber, country: COUNTRY_TYPE | None = None):
        super().__init__()
        self.account_number = account_number
        self.country = country

    def __post_init__(self) -> None:
        super().__post_init__()

        for stock in self.stocks:
            stock.balance = self
            stock.account_number = self.account_number

        for deposit in self.deposits.values():
            deposit.account_number = self.account_number


class KisOverseasBalanceStock(KisBalanceStock):
    """한국투자증권 해외종목 잔고"""

    symbol: str = KisString["ovrs_pdno"]
    """종목코드"""
    market: MARKET_TYPE = KisString["ovrs_excg_cd"]
    """상품유형타입"""
    account_number: KisAccountNumber = KisTransform(
        lambda x: KisAccountNumber(f"{x['cano']}-{x['acnt_prdt_cd']}")
    )()
    """계좌번호"""

    name: str = KisString["ovrs_item_name"]
    """종목명"""

    current_price: Decimal = KisDecimal["now_pric2"]
    """현재가"""

    quantity: Decimal = KisDecimal["ovrs_cblc_qty"]
    """수량"""
    orderable: Decimal = KisDecimal["ord_psbl_qty"]
    """매도가능수량"""

    purchase_amount: Decimal = KisDecimal["frcr_pchs_amt1"]
    """매입금액"""

    currency: CURRENCY_TYPE = KisString["tr_crcy_cd"]
    """통화코드"""

    @property
    @cached
    def exchange_rate(self) -> Decimal:
        """환율 (캐시됨)"""
        return self.balance.deposits[self.currency].exchange_rate


class KisOverseasBalance(KisPaginationAPIResponse, KisBalance):
    """한국투자증권 해외종목 잔고"""

    __path__ = None

    country: COUNTRY_TYPE | None
    """국가코드 (스코프 지정시)"""

    stocks: list[KisBalanceStock] = KisList(KisOverseasBalanceStock)["output1"]
    """보유종목"""
    deposits: dict[CURRENCY_TYPE, KisDeposit]
    """통화별 예수금"""

    def __init__(self, account_number: KisAccountNumber, country: COUNTRY_TYPE | None = None):
        super().__init__()
        self.account_number = account_number
        self.country = country
        self.deposits = {}

    def __post_init__(self) -> None:
        super().__post_init__()

        for stock in self.stocks:
            stock.balance = self


class KisIntegrationBalance(KisBalance):
    """한국투자증권 통합잔고"""

    country: COUNTRY_TYPE | None = None
    """국가코드 (스코프 지정시)"""

    stocks: list[KisBalanceStock]
    """보유종목"""
    deposits: dict[CURRENCY_TYPE, KisDeposit]
    """통화별 예수금"""

    _balances: list[KisBalance]
    """내부구현 잔고"""

    def __init__(self, account_number: KisAccountNumber, *balances: KisBalance):
        super().__init__()
        self.account_number = account_number
        self._balances = list(balances)
        self.stocks = []
        self.deposits = {}

        for balance in self._balances:
            self.stocks.extend(balance.stocks)

            for stock in balance.stocks:
                stock.balance = self

            for currency, deposit in balance.deposits.items():
                self.deposits[currency] = deposit


def domestic_balance(
    self: "PyKis",
    account: str | KisAccountNumber,
    page: KisPage | None = None,
    continuous: bool = True,
) -> KisDomesticBalance:
    """
    한국투자증권 국내 주식 잔고 조회

    국내주식주문 -> 주식잔고조회[v1_국내주식-006]
    (업데이트 날짜: 2024/03/29)

    Args:
        account (str | KisAccountNumber): 계좌번호
        page (KisPage, optional): 페이지 정보
        continuous (bool, optional): 연속조회 여부

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    page = (page or KisPage.first()).to(100)
    first = None

    while True:
        result = self.fetch(
            "/uapi/domestic-stock/v1/trading/inquire-balance",
            api="VTTC8434R" if self.virtual else "TTTC8434R",
            params={
                "AFHR_FLPR_YN": "N",
                "OFL_YN": "",
                "INQR_DVSN": "02",
                "UNPR_DVSN": "01",
                "FUND_STTL_ICLD_YN": "Y",
                "FNCG_AMT_AUTO_RDPT_YN": "N",
                "PRCS_DVSN": "00",
            },
            form=[
                account,
                page,
            ],
            continuous=not page.is_first,
            response_type=KisDomesticBalance(
                account_number=account,
            ),
        )

        if first is None:
            first = result
        else:
            first.stocks.extend(result.stocks)

        if not continuous or result.is_last:
            break

        page = result.next_page

    return first


def _internal_overseas_balance(
    self: "PyKis",
    account: str | KisAccountNumber,
    market: str | None = None,
    page: KisPage | None = None,
    continuous: bool = True,
) -> KisOverseasBalance:
    """
    한국투자증권 해외 주식 잔고 조회

    해외주식주문 -> 해외주식 잔고[v1_해외주식-006]
    (업데이트 날짜: 2024/03/30)

    Args:
        account (str | KisAccountNumber): 계좌번호
        market (str, optional): 시장코드
        page (KisPage, optional): 페이지 정보
        continuous (bool, optional): 연속조회 여부

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    page = (page or KisPage.first()).to(200)
    first = None

    while True:
        result = self.fetch(
            "/uapi/overseas-stock/v1/trading/inquire-balance",
            api="VTTS3012R" if self.virtual else "TTTS3012R",
            params={
                "OVRS_EXCG_CD": market if market else "",
                "TR_CRCY_CD": "",
            },
            form=[
                account,
                page,
            ],
            continuous=not page.is_first,
            response_type=KisOverseasBalance(
                account_number=account,
            ),
        )

        if first is None:
            first = result
        else:
            first.stocks.extend(result.stocks)

        if not continuous or result.is_last:
            break

        page = result.next_page

    return first


OVERSEAS_COUNTRY_MARKET_MAP: dict[tuple[bool | None, COUNTRY_TYPE | None], list[str | None]] = {
    # 실전투자여부, 국가코드 -> 조회시장코드
    (None, None): [None],
    (True, "US"): ["NASD"],
    (False, "US"): ["NASD", "NYSE", "AMEX"],
    (None, "HK"): ["SEHK"],
    (None, "CN"): ["SHAA", "SZAA"],
    (None, "JP"): ["TKSE"],
    (None, "VN"): ["VNSE", "HASE"],
}


def _overseas_balance(
    self: "PyKis",
    account: str | KisAccountNumber,
    country: COUNTRY_TYPE | None = None,
) -> KisOverseasBalance:
    """
    한국투자증권 해외 주식 잔고 조회

    해외주식주문 -> 해외주식 잔고[v1_해외주식-006]
    (업데이트 날짜: 2024/03/30)

    Args:
        account (str | KisAccountNumber): 계좌번호
        country (COUNTRY_TYPE, optional): 국가코드

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    markets = OVERSEAS_COUNTRY_MARKET_MAP.get(
        (not self.virtual, country), OVERSEAS_COUNTRY_MARKET_MAP[(None, country)]
    )

    first = None

    for market in markets:
        result = _internal_overseas_balance(self, account, market)

        if first is None:
            first = result
        else:
            first.stocks.extend(result.stocks)

    if first is None:
        raise ValueError("Invalid country code")

    return first


OVERSEAS_COUNTRY_MAP = {
    None: "000",
    "US": "840",
    "HK": "344",
    "CN": "156",
    "JP": "392",
    "VN": "704",
}


def overseas_balance(
    self: "PyKis",
    account: str | KisAccountNumber,
    country: COUNTRY_TYPE | None = None,
) -> KisOverseasPresentBalance:
    """
    한국투자증권 해외 주식 잔고 조회

    해외주식주문 -> 해외주식 체결기준현재잔고[v1_해외주식-008] (실전투자, 모의투자)
    해외주식주문 -> 해외주식 잔고[v1_해외주식-006] (모의투자)
    (업데이트 날짜: 2024/03/30)

    Args:
        account (str | KisAccountNumber): 계좌번호
        country (COUNTRY_TYPE, optional): 국가코드

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    result = self.fetch(
        "/uapi/overseas-stock/v1/trading/inquire-present-balance",
        api="VTRP6504R" if self.virtual else "CTRP6504R",
        params={
            "WCRC_FRCR_DVSN_CD": "02",
            "NATN_CD": OVERSEAS_COUNTRY_MAP[country],
            "TR_MKET_CD": "00",
            "INQR_DVSN_CD": "00",
        },
        form=[account],
        response_type=KisOverseasPresentBalance(
            account_number=account,
            country=country,
        ),
    )

    if self.virtual:
        result.stocks = _overseas_balance(
            self,
            account=account,
            country=country,
        ).stocks

        for stock in result.stocks:
            stock.balance = result

    return result


def balance(
    self: "PyKis",
    account: str | KisAccountNumber,
    country: COUNTRY_TYPE | None = None,
) -> KisBalance:
    """
    한국투자증권 통합주식 잔고 조회

    국내주식주문 -> 주식잔고조회[v1_국내주식-006]
    해외주식주문 -> 해외주식 체결기준현재잔고[v1_해외주식-008] (실전투자, 모의투자)
    해외주식주문 -> 해외주식 잔고[v1_해외주식-006] (모의투자)
    (업데이트 날짜: 2024/03/30)

    Args:
        account (str | KisAccountNumber): 계좌번호
        country (COUNTRY_TYPE, optional): 국가코드

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    if country is None:
        return KisIntegrationBalance(
            account,
            domestic_balance(self, account),
            overseas_balance(self, account),
        )
    elif country == "KR":
        return domestic_balance(self, account)
    else:
        return overseas_balance(self, account, country)


def orderable_quantity(
    self: "PyKis",
    account: str | KisAccountNumber,
    symbol: str,
    country: COUNTRY_TYPE | None = None,
) -> Decimal | None:
    """
    한국투자증권 매도가능수량 조회

    국내주식시세 -> 상품기본조회[v1_국내주식-029]
    국내주식주문 -> 주식잔고조회[v1_국내주식-006]
    해외주식주문 -> 해외주식 체결기준현재잔고[v1_해외주식-008] (실전투자, 모의투자)
    해외주식주문 -> 해외주식 잔고[v1_해외주식-006] (모의투자)
    (업데이트 날짜: 2024/03/30)

    Args:
        account (str | KisAccountNumber): 계좌번호
        symbol (str): 종목코드
        country (COUNTRY_TYPE, optional): 국가코드

    Returns:
        Decimal: 매도가능수량

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    if not country:
        country = market_to_country(resolve_market(self, symbol=symbol))

    stock = balance(
        self,
        account=account,
        country=country,
    ).stock(symbol)

    if stock:
        return stock.orderable

    return None
