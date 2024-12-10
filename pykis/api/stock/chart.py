import bisect
from datetime import date, datetime, time, tzinfo
from decimal import Decimal
from typing import (
    TYPE_CHECKING,
    Iterable,
    Iterator,
    Literal,
    Protocol,
    TypeVar,
    overload,
    runtime_checkable,
)

from pykis.api.base.product import KisProductBase, KisProductProtocol
from pykis.api.stock.market import MARKET_TYPE
from pykis.api.stock.quote import STOCK_SIGN_TYPE
from pykis.responses.response import KisResponseProtocol
from pykis.utils.repr import kis_repr

__all__ = [
    "KisChartBar",
    "KisChart",
    "TChart",
]

if TYPE_CHECKING:
    from pandas import DataFrame


@runtime_checkable
class KisChartBar(Protocol):
    """한국투자증권 차트 봉"""

    @property
    def time(self) -> datetime:
        """시간 (현지시간)"""
        ...

    @property
    def time_kst(self) -> datetime:
        """시간 (한국시간)"""
        ...

    @property
    def open(self) -> Decimal:
        """시가"""
        ...

    @property
    def close(self) -> Decimal:
        """종가 (현재가)"""
        ...

    @property
    def high(self) -> Decimal:
        """고가"""
        ...

    @property
    def low(self) -> Decimal:
        """저가"""
        ...

    @property
    def volume(self) -> int:
        """거래량"""
        ...

    @property
    def amount(self) -> Decimal:
        """거래대금"""
        ...

    @property
    def change(self) -> Decimal:
        """전일대비"""
        ...

    @property
    def sign(self) -> STOCK_SIGN_TYPE:
        """전일대비 부호"""
        ...

    @property
    def price(self) -> Decimal:
        """현재가 (종가)"""
        ...

    @property
    def prev_price(self) -> Decimal:
        """전일가"""
        ...

    @property
    def rate(self) -> Decimal:
        """등락률 (-100 ~ 100)"""
        ...

    @property
    def sign_name(self) -> str:
        """대비부호명"""
        ...


@runtime_checkable
class KisChart(KisProductProtocol, Protocol):
    """한국투자증권 차트"""

    @property
    def timezone(self) -> tzinfo:
        """시간대"""
        ...

    @property
    def bars(self) -> list[KisChartBar]:
        """차트 (오름차순)"""
        ...

    def index(self, time: datetime | date | time, /, kst: bool = False) -> int:
        """
        이진탐색으로 시간에 해당하는 봉의 인덱스를 반환합니다.

        Args:
            time: 시간대
            kst: 한국시간대 여부
        """
        ...

    def order_by(
        self,
        key: Literal["time", "open", "high", "low", "close", "volume", "amount", "change"],
        /,
        reverse: bool = False,
    ) -> list[KisChartBar]:
        """
        차트를 주어진 키로 정렬합니다.

        Args:
            key: 정렬 키
            reverse: 내림차순 여부
        """
        ...

    @overload
    def __getitem__(self, index: datetime | date | time | int) -> KisChartBar: ...

    @overload
    def __getitem__(self, index: slice) -> list[KisChartBar]: ...

    def __getitem__(self, index: datetime | date | time | int | slice) -> KisChartBar | list[KisChartBar]: ...

    def __iter__(self) -> Iterable[KisChartBar]: ...

    def __len__(self) -> int: ...

    def __reversed__(self) -> Iterator[KisChartBar]: ...

    def df(self) -> "DataFrame":
        """
        차트를 Pandas DataFrame으로 변환합니다.

        해당 함수는 Pandas가 설치되어 있어야 합니다.
        """
        ...


@runtime_checkable
class KisChartResponse(KisChart, KisResponseProtocol, Protocol):
    """차트 응답"""


@kis_repr(
    "time",
    "open",
    "close",
    "high",
    "low",
    "volume",
    "amount",
    "change",
    lines="single",
)
class KisChartBarRepr:
    """한국투자증권 차트 봉"""


@kis_repr(
    "market",
    "symbol",
    "bars",
    lines="multiple",
    field_lines={
        "bars": "multiple",
    },
)
class KisChartRepr:
    """한국투자증권 차트"""


class KisChartBase(KisChartRepr, KisProductBase):

    symbol: str
    """종목코드"""
    market: MARKET_TYPE
    """상품유형타입"""

    timezone: tzinfo
    """시간대"""
    bars: list[KisChartBar]
    """차트 (오름차순)"""

    def index(self, time: datetime | date | time, /, kst: bool = False) -> int:
        """
        이진탐색으로 시간에 해당하는 봉의 인덱스를 반환합니다.

        Args:
            time: 시간대
            kst: 한국시간대 여부
        """
        index = bisect.bisect_left(
            self.bars,
            time,
            key=(
                (
                    (lambda bar: bar.time_kst)
                    if isinstance(time, datetime)
                    else ((lambda bar: bar.time_kst.date()) if isinstance(time, date) else (lambda bar: bar.time_kst.time()))
                )
                if kst
                else (
                    (lambda bar: bar.time)
                    if isinstance(time, datetime)
                    else ((lambda bar: bar.time.date()) if isinstance(time, date) else (lambda bar: bar.time.time()))
                )
            ),
        )

        if index >= len(self.bars):
            raise ValueError(f"차트에 {time} 시간의 봉이 없습니다.")

        return index

    def order_by(
        self,
        key: Literal["time", "open", "high", "low", "close", "volume", "amount", "change"],
        /,
        reverse: bool = False,
    ) -> list[KisChartBar]:
        """
        차트를 주어진 키로 정렬합니다.

        Args:
            key: 정렬 키
            reverse: 내림차순 여부
        """
        return sorted(self.bars, key=lambda bar: getattr(bar, key), reverse=reverse)

    @overload
    def __getitem__(self, index: datetime | date | time | int) -> KisChartBar: ...

    @overload
    def __getitem__(self, index: slice) -> list[KisChartBar]: ...

    def __getitem__(self, index: datetime | date | time | int | slice) -> KisChartBar | list[KisChartBar]:
        if isinstance(index, int):
            return self.bars[index]
        elif isinstance(index, (datetime, date, time)):
            return self.bars[self.index(index)]
        elif isinstance(index, slice):
            if isinstance(index.start, int) and isinstance(index.stop, int):
                return self.bars[index]

            if isinstance(index.start, datetime) and isinstance(index.stop, datetime):
                return [bar for bar in self.bars if index.start <= bar.time <= index.stop]
            elif isinstance(index.start, date) and isinstance(index.stop, date):
                return [bar for bar in self.bars if index.start <= bar.time.date() <= index.stop]
            elif isinstance(index.start, time) and isinstance(index.stop, time):
                return [bar for bar in self.bars if index.start <= bar.time.time() <= index.stop]

        raise TypeError(f"인덱스 {index}는 지원하지 않습니다.")

    def __iter__(self) -> Iterable[KisChartBar]:
        return iter(self.bars)

    def __len__(self) -> int:
        return len(self.bars)

    def __reversed__(self) -> Iterator[KisChartBar]:
        return reversed(self.bars)

    def df(self) -> "DataFrame":
        """
        차트를 Pandas DataFrame으로 변환합니다.

        해당 함수는 Pandas가 설치되어 있어야 합니다.
        """
        try:
            import pandas as pd  # type: ignore
        except ImportError as e:
            raise ImportError(
                "Pandas가 설치되어 있지 않습니다.\n" "Pandas를 설치하려면 `pip install pandas`를 실행해주세요."
            ) from e

        return pd.DataFrame(
            {
                "time": [bar.time for bar in self.bars],
                "open": [float(bar.open) for bar in self.bars],
                "high": [float(bar.high) for bar in self.bars],
                "low": [float(bar.low) for bar in self.bars],
                "close": [float(bar.close) for bar in self.bars],
                "volume": [bar.volume for bar in self.bars],
            }
        )


TChart = TypeVar("TChart", bound=KisChart)
