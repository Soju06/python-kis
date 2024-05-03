from decimal import Decimal
from typing import TYPE_CHECKING, Any

from pykis.api.base.product import KisProductBase
from pykis.api.stock.market import CURRENCY_TYPE, MARKET_TYPE
from pykis.responses.dynamic import KisDynamic, KisTransform
from pykis.responses.response import KisAPIResponse, raise_not_found
from pykis.utils.repr import kis_repr

if TYPE_CHECKING:
    from pykis.kis import PyKis


@kis_repr(
    "price",
    "volume",
    lines="single",
)
class KisAskingPriceItem:
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
        if not isinstance(o, KisAskingPriceItem):
            return False
        return self.price == o.price and self.volume == o.volume

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __iter__(self):
        yield self.price
        yield self.volume


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
class KisAskingPrice(KisDynamic, KisProductBase):
    """한국투자증권 호가"""

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    decimal_places: int
    """소수점 자리수"""
    currency: CURRENCY_TYPE
    """통화코드"""

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

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(symbol={self.symbol!r}, market={self.market!r})"


class KisDomesticAskingPrice(KisAPIResponse, KisAskingPrice):
    """한국투자증권 국내 호가"""

    __path__ = "output1"

    symbol: str
    """종목코드"""
    market: MARKET_TYPE = "KRX"
    """상품유형타입"""

    decimal_places: int = 1
    """소수점 자리수"""
    currency: CURRENCY_TYPE = "KRW"
    """통화코드"""

    ask: list[KisAskingPriceItem] = KisTransform(
        lambda x: [
            KisAskingPriceItem(
                price=Decimal(x[f"askp{i + 1}"]),
                volume=x[f"askp_rsqn{i + 1}"],
            )
            for i in range(10)
        ]
    )()
    """매도호가"""
    bid: list[KisAskingPriceItem] = KisTransform(
        lambda x: [
            KisAskingPriceItem(
                price=Decimal(x[f"bidp{i + 1}"]),
                volume=x[f"bidp_rsqn{i + 1}"],
            )
            for i in range(10)
        ]
    )()
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
