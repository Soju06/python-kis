from decimal import Decimal
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

from pykis.api.base.product import KisProductBase, KisProductProtocol
from pykis.api.stock.market import MARKET_TYPE
from pykis.responses.dynamic import KisTransform
from pykis.responses.response import (
    KisAPIResponse,
    KisResponseProtocol,
    raise_not_found,
)
from pykis.utils.repr import kis_repr
from pykis.utils.typing import Checkable

if TYPE_CHECKING:
    from pykis.kis import PyKis

__all__ = [
    "KisAskingPrice",
    "KisAskingPriceItem",
    "KisAskingPriceResponse",
    "asking_price",
]


@runtime_checkable
class KisAskingPriceItem(Protocol):
    """한국투자증권 호가 항목"""

    @property
    def price(self) -> Decimal:
        """호가가격"""
        raise NotImplementedError

    @property
    def volume(self) -> int:
        """호가잔량"""
        raise NotImplementedError


@runtime_checkable
class KisAskingPrice(KisProductProtocol, Protocol):
    """한국투자증권 호가"""

    @property
    def decimal_places(self) -> int:
        """소수점 자리수"""
        raise NotImplementedError

    @property
    def ask(self) -> list[KisAskingPriceItem]:
        """매도호가"""
        raise NotImplementedError

    @property
    def bid(self) -> list[KisAskingPriceItem]:
        """매수호가"""
        raise NotImplementedError

    @property
    def count(self) -> int:
        return min(len(self.ask), len(self.bid))

    @property
    def ask_price(self) -> KisAskingPriceItem:
        """매도 1호가"""
        return self.ask[0]

    @property
    def bid_price(self) -> KisAskingPriceItem:
        """매수 1호가"""
        return self.bid[0]

    @property
    def ask_volume(self) -> int:
        """매도 1호가 잔량"""
        return self.ask_price.volume

    @property
    def bid_volume(self) -> int:
        """매수 1호가 잔량"""
        return self.bid_price.volume


@kis_repr(
    "price",
    "volume",
    lines="single",
)
class KisAskingPriceItemRepr:
    """한국투자증권 호가 항목"""


class _KisAskingPriceItem(KisAskingPriceItemRepr):
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
        if not isinstance(o, _KisAskingPriceItem):
            return False
        return self.price == o.price and self.volume == o.volume

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __iter__(self):
        yield self.price
        yield self.volume


if TYPE_CHECKING:
    Checkable[KisAskingPriceItem](_KisAskingPriceItem)


class KisAskingPriceResponse(KisAskingPrice, KisResponseProtocol, Protocol):
    """한국투자증권 호가 응답"""


@kis_repr(
    "market",
    "symbol",
    "ask",
    "bid",
    lines="multiple",
    field_lines={
        "ask": "multiple",
        "bid": "multiple",
    },
)
class KisAskingPriceRepr:
    """한국투자증권 호가"""


class KisAskingPriceBase(KisAskingPriceRepr, KisProductBase):
    """한국투자증권 호가"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    decimal_places: int
    """소수점 자리수"""

    ask: list[KisAskingPriceItem]
    """매도호가"""
    bid: list[KisAskingPriceItem]
    """매수호가"""

    @property
    def count(self) -> int:
        return min(len(self.ask), len(self.bid))

    @property
    def ask_price(self) -> KisAskingPriceItem:
        """매도 1호가"""
        return self.ask[0]

    @property
    def bid_price(self) -> KisAskingPriceItem:
        """매수 1호가"""
        return self.bid[0]

    @property
    def ask_volume(self) -> int:
        """매도 1호가 잔량"""
        return self.ask_price.volume

    @property
    def bid_volume(self) -> int:
        """매수 1호가 잔량"""
        return self.bid_price.volume


class KisDomesticAskingPrice(KisAPIResponse, KisAskingPriceBase):
    """한국투자증권 국내 호가"""

    __path__ = "output1"

    symbol: str  ## __init__ 에서 초기화
    """종목코드"""
    market: MARKET_TYPE = "KRX"
    """상품유형타입"""

    decimal_places: int = 1
    """소수점 자리수"""

    ask: list[KisAskingPriceItem] = KisTransform(
        lambda x: [
            _KisAskingPriceItem(
                price=Decimal(x[f"askp{i + 1}"]),
                volume=int(x[f"askp_rsqn{i + 1}"]),
            )
            for i in range(10)
        ]
    )()  # type: ignore
    """매도호가"""
    bid: list[KisAskingPriceItem] = KisTransform(
        lambda x: [
            _KisAskingPriceItem(
                price=Decimal(x[f"bidp{i + 1}"]),
                volume=int(x[f"bidp_rsqn{i + 1}"]),
            )
            for i in range(10)
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
                code=self.symbol,
                market=self.market,
            )

        super().__pre_init__(data)


def domestic_asking_price(
    self: "PyKis",
    symbol: str,
) -> KisDomesticAskingPrice:
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
        response_type=KisDomesticAskingPrice(symbol),
    )


def asking_price(
    self: "PyKis",
    market: MARKET_TYPE,
    symbol: str,
) -> KisAskingPriceResponse:
    """
    한국투자증권 호가 조회 (해외주식 미지원)

    [국내주식] 기본시세 -> 주식현재가 호가/예상체결[v1_국내주식-011]

    Args:
        market (MARKET_TYPE): 상품유형타입
        symbol (str): 종목코드

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    if market == "KRX":
        return domestic_asking_price(self, symbol=symbol)

    raise ValueError(f"해외주식 호가는 지원하지 않습니다. ({market})")


def product_asking_price(
    self: "KisProductProtocol",
) -> KisAskingPriceResponse:
    """
    한국투자증권 호가 조회 (해외주식 미지원)

    [국내주식] 기본시세 -> 주식현재가 호가/예상체결[v1_국내주식-011]

    Raises:
        KisAPIError: API 호출에 실패한 경우
        KisNotFoundError: 조회 결과가 없는 경우
        ValueError: 종목 코드가 올바르지 않은 경우
    """
    return asking_price(
        self.kis,
        market=self.market,
        symbol=self.symbol,
    )
