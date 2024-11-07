from decimal import Decimal
from typing import TYPE_CHECKING, Any, Iterable, Protocol, runtime_checkable

from pykis.api.account.order import ORDER_CONDITION
from pykis.api.base.product import KisProductBase, KisProductProtocol
from pykis.api.stock.market import (
    DAYTIME_MARKET_SHORT_TYPE_MAP,
    MARKET_SHORT_TYPE_MAP,
    MARKET_TYPE,
)
from pykis.responses.dynamic import KisTransform
from pykis.responses.response import (
    KisAPIResponse,
    KisResponseProtocol,
    raise_not_found,
)
from pykis.responses.types import KisInt
from pykis.utils.repr import kis_repr
from pykis.utils.typing import Checkable

if TYPE_CHECKING:
    from pykis.kis import PyKis

__all__ = [
    "KisOrderbook",
    "KisOrderbookItem",
    "KisOrderbookResponse",
    "orderbook",
]


@runtime_checkable
class KisOrderbookItem(Protocol):
    """한국투자증권 호가 항목"""

    @property
    def price(self) -> Decimal:
        """호가가격"""
        ...

    @property
    def volume(self) -> int:
        """호가잔량"""
        ...


@runtime_checkable
class KisOrderbook(KisProductProtocol, Protocol):
    """한국투자증권 호가"""

    @property
    def decimal_places(self) -> int:
        """소수점 자리수"""
        ...

    @property
    def asks(self) -> list[KisOrderbookItem]:
        """매도호가"""
        ...

    @property
    def bids(self) -> list[KisOrderbookItem]:
        """매수호가"""
        ...

    @property
    def count(self) -> int: ...

    @property
    def ask_price(self) -> KisOrderbookItem:
        """매도 1호가"""
        ...

    @property
    def bid_price(self) -> KisOrderbookItem:
        """매수 1호가"""
        ...

    @property
    def ask_volume(self) -> int:
        """매도 1호가 잔량"""
        ...

    @property
    def bid_volume(self) -> int:
        """매수 1호가 잔량"""
        ...


@kis_repr(
    "price",
    "volume",
    lines="single",
)
class KisOrderbookItemRepr:
    """한국투자증권 호가 항목"""


class KisOrderbookItemBase(KisOrderbookItemRepr):
    """한국투자증권 호가 항목"""

    price: Decimal
    """호가가격"""
    volume: int
    """호가잔량"""

    def __init__(self, price: Decimal, volume: int):
        super().__init__()
        self.price = price
        self.volume = volume

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, KisOrderbookItemBase):
            return False
        return self.price == o.price and self.volume == o.volume

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __iter__(self) -> Iterable[Decimal | int]:
        yield self.price
        yield self.volume


class KisOrderbookResponse(KisOrderbook, KisResponseProtocol, Protocol):
    """한국투자증권 호가 응답"""


@kis_repr(
    "market",
    "symbol",
    "asks",
    "bids",
    lines="multiple",
    field_lines={
        "asks": "multiple",
        "bids": "multiple",
    },
)
class KisOrderbookRepr:
    """한국투자증권 호가"""


class KisOrderbookBase(KisOrderbookRepr, KisProductBase):
    """한국투자증권 호가"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    decimal_places: int
    """소수점 자리수"""

    asks: list[KisOrderbookItem]
    """매도호가"""
    bids: list[KisOrderbookItem]
    """매수호가"""

    @property
    def count(self) -> int:
        return min(len(self.asks), len(self.bids))

    @property
    def ask_price(self) -> KisOrderbookItem:
        """매도 1호가"""
        return self.asks[0]

    @property
    def bid_price(self) -> KisOrderbookItem:
        """매수 1호가"""
        return self.bids[0]

    @property
    def ask_volume(self) -> int:
        """매도 1호가 잔량"""
        return self.ask_price.volume

    @property
    def bid_volume(self) -> int:
        """매수 1호가 잔량"""
        return self.bid_price.volume


class KisDomesticOrderbookItem(KisOrderbookItemBase):
    """한국투자증권 국내 호가"""


if TYPE_CHECKING:
    Checkable[KisOrderbookItem](KisDomesticOrderbookItem)


class KisDomesticOrderbook(KisAPIResponse, KisOrderbookBase):
    """한국투자증권 국내 호가"""

    __path__ = "output1"

    symbol: str  # __init__ 에서 초기화
    """종목코드"""
    market: MARKET_TYPE = "KRX"
    """상품유형타입"""

    decimal_places: int = 1
    """소수점 자리수"""

    asks: list[KisOrderbookItem] = KisTransform(
        lambda x: [
            KisDomesticOrderbookItem(
                price=Decimal(x[f"askp{i}"]),
                volume=int(x[f"askp_rsqn{i}"]),
            )
            for i in range(1, 11)
        ]
    )()  # type: ignore
    """매도호가"""
    bids: list[KisOrderbookItem] = KisTransform(
        lambda x: [
            KisDomesticOrderbookItem(
                price=Decimal(x[f"bidp{i}"]),
                volume=int(x[f"bidp_rsqn{i}"]),
            )
            for i in range(1, 11)
        ]
    )()  # type: ignore
    """매수호가"""

    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol

    def __pre_init__(self, data: dict[str, Any]):
        if "askp1" not in data["output1"]:
            raise_not_found(
                data,
                "해당 종목의 호가를 조회할 수 없습니다.",
                symbol=self.symbol,
                market=self.market,
            )

        super().__pre_init__(data)


class KisForeignOrderbookItem(KisOrderbookItemBase):
    """한국투자증권 해외 호가"""


if TYPE_CHECKING:
    Checkable[KisOrderbookItem](KisForeignOrderbookItem)


class KisForeignOrderbook(KisAPIResponse, KisOrderbookBase):
    """한국투자증권 해외 호가"""

    __path__ = "output1"

    symbol: str  # __init__ 에서 초기화
    """종목코드"""
    market: MARKET_TYPE  # __init__ 에서 초기화
    """상품유형타입"""

    decimal_places: int = KisInt["zdiv"]
    """소수점 자리수"""

    asks: list[KisOrderbookItem]  # __pre_init__ 에서 초기화
    """매도호가"""
    bids: list[KisOrderbookItem]  # __pre_init__ 에서 초기화
    """매수호가"""

    def __init__(self, symbol: str, market: MARKET_TYPE):
        super().__init__()
        self.symbol = symbol
        self.market = market

    def __pre_init__(self, data: dict[str, Any]):
        super().__pre_init__(data)

        if not data["output1"]["rsym"]:
            raise_not_found(
                data,
                "해당 종목의 호가를 조회할 수 없습니다.",
                symbol=self.symbol,
                market=self.market,
            )

        output2 = data["output2"]
        count = 10 if self.market in ["NASDAQ", "NYSE"] else 1  # 미국외 시장은 1호가만 제공

        self.asks = [
            KisForeignOrderbookItem(
                price=Decimal(output2[f"pask{i}"]),
                volume=int(output2[f"vask{i}"]),
            )
            for i in range(1, 1 + count)
        ]
        self.bids = [
            KisForeignOrderbookItem(
                price=Decimal(output2[f"pbid{i}"]),
                volume=int(output2[f"vbid{i}"]),
            )
            for i in range(1, 1 + count)
        ]


def domestic_orderbook(
    self: "PyKis",
    symbol: str,
) -> KisDomesticOrderbook:
    """
    한국투자증권 국내 주식 호가 조회

    [국내주식] 기본시세 -> 주식현재가 호가/예상체결[v1_국내주식-011]
    (업데이트 날짜: 2024/05/03)

    Args:
        symbol (str): 종목코드

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    if not symbol:
        raise ValueError("종목코드를 입력해주세요.")

    return self.fetch(
        "/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn",
        api="FHKST01010200",
        params={
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
        },
        response_type=KisDomesticOrderbook(symbol),
    )


def foreign_orderbook(
    self: "PyKis",
    market: MARKET_TYPE,
    symbol: str,
    condition: ORDER_CONDITION | None = None,
) -> KisForeignOrderbook:
    """
    한국투자증권 해외 주식 호가 조회

    [해외주식] 기본시세 -> 해외주식 현재가 10호가 [해외주식-033]
    (업데이트 날짜: 2024/05/27)

    Args:
        market (MARKET_TYPE): 상품유형타입
        symbol (str): 종목코드
        condition (ORDER_CONDITION, optional): 주문조건. Defaults to None.

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    if not symbol:
        raise ValueError("종목코드를 입력해주세요.")

    return self.fetch(
        "/uapi/overseas-price/v1/quotations/inquire-asking-price",
        api="HHDFS76200100",
        params={
            "EXCD": (DAYTIME_MARKET_SHORT_TYPE_MAP[market] if condition == "extended" else MARKET_SHORT_TYPE_MAP[market]),
            "SYMB": symbol,
        },
        response_type=KisForeignOrderbook(
            symbol=symbol,
            market=market,
        ),
    )


def orderbook(
    self: "PyKis",
    market: MARKET_TYPE,
    symbol: str,
    condition: ORDER_CONDITION | None = None,
) -> KisOrderbookResponse:
    """
    한국투자증권 호가 조회

    [국내주식] 기본시세 -> 주식현재가 호가/예상체결[v1_국내주식-011]
    [해외주식] 기본시세 -> 해외주식 현재가 10호가 [해외주식-033]

    Args:
        market (MARKET_TYPE): 상품유형타입
        symbol (str): 종목코드
        condition (ORDER_CONDITION, optional): 주문조건. Defaults to None.

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    if market == "KRX":
        return domestic_orderbook(
            self,
            symbol=symbol,
        )
    else:
        return foreign_orderbook(
            self,
            market=market,
            symbol=symbol,
            condition=condition,
        )


def product_orderbook(
    self: "KisProductProtocol",
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
    return orderbook(
        self.kis,
        market=self.market,
        symbol=self.symbol,
        condition=condition,
    )
