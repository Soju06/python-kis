from decimal import Decimal
from typing import TYPE_CHECKING

from pykis.api.base.account import KisAccountBase
from pykis.api.base.account_product import KisAccountProductBase
from pykis.api.stock.info import COUNTRY_TYPE, MARKET_TYPE_MAP
from pykis.api.stock.market import CURRENCY_TYPE, MARKET_TYPE
from pykis.client.account import KisAccountNumber
from pykis.client.page import KisPage
from pykis.responses.dynamic import KisDynamic, KisList, KisObject
from pykis.responses.response import KisAPIResponse, KisPaginationAPIResponse
from pykis.responses.types import KisAny, KisDecimal, KisInt, KisString

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisBalanceStock(KisDynamic, KisAccountProductBase):
    """한국투자증권 보유종목"""

    balance: "KisBalance"
    """계좌잔고 (post initialization)"""

    code: str
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
    def name_kor(self) -> str:
        """종목명"""
        return self.info.name_kor

    @property
    def full_name_kor(self) -> str:
        """종목전체명"""
        return self.info.full_name_kor

    @property
    def name_eng(self) -> str:
        """종목영문명"""
        return self.info.name_eng

    @property
    def full_name_eng(self) -> str:
        """종목영문전체명"""
        return self.info.full_name_eng

    @property
    def overseas(self) -> bool:
        """해외종목 여부"""
        return self.market not in MARKET_TYPE_MAP["KRX"]

    @property
    def domestic(self) -> bool:
        """국내종목 여부"""
        return not self.overseas

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
        return f"{self.__class__.__name__}(account_number={self.account_number!r}, code={self.code!r}, market={self.market!r}, quantity={self.quantity}, current_price={self.current_price}, purchase_amount={self.purchase_amount})"

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


class KisBalance(KisDynamic, KisAccountBase):
    """한국투자증권 계좌 잔고"""

    country: COUNTRY_TYPE | None
    """국가코드 (스코프 지정시)"""

    stocks: list[KisBalanceStock]
    """보유종목"""
    deposits: dict[CURRENCY_TYPE, KisDeposit]
    """통화별 예수금"""

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
                if stock.code == key:
                    return stock
            raise KeyError(key)
        else:
            raise TypeError(key)


class KisDomesticBalanceStock(KisBalanceStock):
    """한국투자증권 국내종목 잔고"""

    code: str = KisString["pdno"]
    """종목코드"""
    market: MARKET_TYPE = "KRX"
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    name: str = KisString["prdt_name"]
    """종목명"""
    name_kor: str = KisString["prdt_name"]
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


class KisOverseasBalanceStock(KisBalanceStock):
    """한국투자증권 해외종목 잔고"""

    code: str = KisString["pdno"]
    """종목코드"""
    market: MARKET_TYPE = KisString["ovrs_excg_cd"]
    """상품유형타입"""
    account_number: KisAccountNumber
    """계좌번호"""

    name: str = KisString["prdt_name"]
    """종목명"""
    name_kor: str = KisString["prdt_name"]
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


class KisOverseasDeposit(KisDeposit):
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


class KisOverseasBalance(KisAPIResponse, KisBalance):
    """한국투자증권 해외종목 잔고"""

    __path__ = None

    country: COUNTRY_TYPE | None
    """국가코드 (스코프 지정시)"""

    stocks: list[KisOverseasBalanceStock] = KisList(KisOverseasBalanceStock)["output1"]
    """보유종목"""
    deposits: dict[CURRENCY_TYPE, KisDeposit] = KisAny(
        lambda x: {
            i["crcy_cd"]: KisObject.transform_(
                i,
                KisOverseasDeposit,
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
) -> KisOverseasBalance:
    """
    한국투자증권 해외 주식 잔고 조회 (모의투자 미지원)

    해외주식주문 -> 해외주식 체결기준현재잔고[v1_해외주식-008]
    (업데이트 날짜: 2024/03/29)

    Args:
        account (str | KisAccountNumber): 계좌번호
        country (COUNTRY_TYPE, optional): 국가코드

    Raises:
        KisAPIError: API 호출에 실패한 경우
        ValueError: 계좌번호가 잘못된 경우
    """
    if self.virtual:
        raise ValueError("모의투자에서는 해외 주식 잔고 조회를 지원하지 않습니다.")

    if not isinstance(account, KisAccountNumber):
        account = KisAccountNumber(account)

    return self.fetch(
        "/uapi/overseas-stock/v1/trading/inquire-present-balance",
        api="CTRP6504R",
        params={
            "WCRC_FRCR_DVSN_CD": "02",
            "NATN_CD": OVERSEAS_COUNTRY_MAP[country],
            "TR_MKET_CD": "00",
            "INQR_DVSN_CD": "00",
        },
        form=[account],
        response_type=KisOverseasBalance(
            account_number=account,
            country=country,
        ),
    )
