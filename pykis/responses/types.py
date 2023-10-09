from datetime import date, datetime, time, tzinfo
from decimal import Decimal
from typing import Any, Callable

from pykis.__env__ import TIMEZONE
from pykis.responses.dynamic import KisDynamic, KisType, KisTypeMeta, KisNoneError


class KisDynamicDict(KisDynamic):
    __transform__ = lambda type, _: type()

    def __str__(self) -> str:
        return str(self.__data__)

    def __repr__(self) -> str:
        return repr(self.__data__)

    def __getattr__(self, name: str) -> Any:
        if name in self.__data__:
            return self.__data__[name]

        return super().__getattribute__(name)


class KisAny(KisType[Any], metaclass=KisTypeMeta[Any]):
    __default__ = []

    def __init__(
        self,
        transform_fn: Callable[[Any], Any] = lambda _: KisDynamicDict(),
    ):
        super().__init__()
        setattr(self, "transform", transform_fn)


class KisString(KisType[str], metaclass=KisTypeMeta):
    __default__ = []

    def transform(self, data: Any) -> str:
        if isinstance(data, str):
            return data

        return str(data)


class KisInt(KisType[int], metaclass=KisTypeMeta[int]):
    __default__ = []

    def transform(self, data: Any) -> int:
        if isinstance(data, int):
            return data

        if data == "":
            raise KisNoneError

        return int(data)


class KisFloat(KisType[float], metaclass=KisTypeMeta):
    """
    금액을 표현 할 경우 부동소수점인 float 타입을 사용하면 정확한 값을 표현할 수 없습니다.
    따라서 금액을 표현할 때는 Decimal 타입을 사용하십시오.
    """

    __default__ = []

    def transform(self, data: Any) -> float:
        if isinstance(data, float):
            return data

        if data == "":
            raise KisNoneError

        return float(data)


class KisDecimal(KisType[Decimal], metaclass=KisTypeMeta):
    __default__ = []

    def transform(self, data: Any) -> Decimal:
        if isinstance(data, Decimal):
            return data

        if data == "":
            raise KisNoneError

        return Decimal(data)


class KisBool(KisType[bool], metaclass=KisTypeMeta):
    __default__ = []

    def transform(self, data: Any) -> bool:
        if isinstance(data, bool):
            return data

        if data == "":
            raise KisNoneError

        if isinstance(data, int):
            return data != 0

        if not isinstance(data, str):
            data = str(data)

        data = data.lower()

        return data == "y" or data == "true"


class KisDate(KisType[date], metaclass=KisTypeMeta):
    __default__ = []

    format: str
    """날짜 포맷"""
    timezone: tzinfo | None
    """타임존"""

    def __init__(self, format: str = "%Y%m%d", timezone: tzinfo | None = TIMEZONE):
        super().__init__()
        self.format = format
        self.timezone = timezone

    def transform(self, data: Any) -> date:
        if isinstance(data, date):
            return data

        if data == "":
            raise KisNoneError

        return datetime.strptime(data, self.format).replace(tzinfo=self.timezone).date()


class KisTime(KisType[time], metaclass=KisTypeMeta):
    __default__ = []

    format: str
    """시간 포맷"""
    timezone: tzinfo | None
    """타임존"""

    def __init__(self, format: str = "%H%M%S", timezone: tzinfo | None = TIMEZONE):
        super().__init__()
        self.format = format
        self.timezone = timezone

    def transform(self, data: Any) -> time:
        if isinstance(data, time):
            return data

        if data == "":
            raise KisNoneError

        return datetime.strptime(data, self.format).replace(tzinfo=self.timezone).time()


class KisDatetime(KisType[datetime], metaclass=KisTypeMeta):
    __default__ = []

    format: str
    """날짜/시간 포맷"""
    timezone: tzinfo | None
    """타임존"""

    def __init__(self, format: str = "%Y%m%d%H%M%S", timezone: tzinfo | None = TIMEZONE):
        super().__init__()
        self.format = format
        self.timezone = timezone

    def transform(self, data: Any) -> datetime:
        if isinstance(data, datetime):
            return data

        if data == "":
            raise KisNoneError

        return datetime.strptime(data, self.format).replace(tzinfo=self.timezone)


class KisDict(KisType[dict[str, Any]], metaclass=KisTypeMeta):
    __default__ = []

    def transform(self, data: Any) -> dict[str, Any]:
        if isinstance(data, dict):
            return data

        if data == "":
            raise KisNoneError

        return dict(data)
