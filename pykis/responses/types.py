from datetime import date, datetime, time, tzinfo
from decimal import Decimal
from typing import Any, Callable

from pykis.responses.dynamic import KisDynamic, KisNoneValueError, KisType, KisTypeMeta
from pykis.utils.repr import dict_repr
from pykis.utils.timezone import TIMEZONE

__all__ = [
    "KisDynamicDict",
    "KisAny",
    "KisString",
    "KisInt",
    "KisFloat",
    "KisDecimal",
    "KisBool",
    "KisDate",
    "KisTime",
    "KisDatetime",
    "KisDict",
    "KisTimeToDatetime",
]


class KisDynamicDict(KisDynamic):
    __transform__ = lambda type, _: type()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return dict_repr(self.__data__)

    def __getattr__(self, name: str) -> Any:
        if (value := self.__data__.get(name)) is not None:
            if isinstance(value, dict):
                return KisDynamicDict.from_dict(value)
            elif isinstance(value, list):
                return [KisDynamicDict.from_dict(item) if isinstance(item, dict) else item for item in value]
            else:
                return value

        return super().__getattribute__(name)

    def __dict__(self) -> dict[str, Any]:
        return self.__data__

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        instance = cls()
        instance.__data__ = data

        return instance


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
            raise KisNoneValueError

        return int(data)


class KisFloat(KisType[float], metaclass=KisTypeMeta[float]):
    """
    금액을 표현 할 경우 부동소수점인 float 타입을 사용하면 정확한 값을 표현할 수 없습니다.
    따라서 금액을 표현할 때는 Decimal 타입을 사용하십시오.
    """

    __default__ = []

    def transform(self, data: Any) -> float:
        if isinstance(data, float):
            return data

        if data == "":
            raise KisNoneValueError

        return float(data)


class KisDecimal(KisType[Decimal], metaclass=KisTypeMeta[Decimal]):
    __default__ = []

    def transform(self, data: Any) -> Decimal:
        if isinstance(data, Decimal):
            return data

        if data == "":
            raise KisNoneValueError

        return Decimal(data).normalize()


class KisBool(KisType[bool], metaclass=KisTypeMeta[bool]):
    __default__ = []

    def transform(self, data: Any) -> bool:
        if isinstance(data, bool):
            return data

        if data == "":
            raise KisNoneValueError

        if isinstance(data, int):
            return data != 0

        if not isinstance(data, str):
            data = str(data)

        data = data.lower()

        return data == "y" or data == "true"


class KisDate(KisType[date], metaclass=KisTypeMeta[date]):
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
            raise KisNoneValueError

        return datetime.strptime(data, self.format).replace(tzinfo=self.timezone).date()


class KisTime(KisType[time], metaclass=KisTypeMeta[time]):
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
            raise KisNoneValueError

        return datetime.strptime(data, self.format).replace(tzinfo=self.timezone).time()


class KisDatetime(KisType[datetime], metaclass=KisTypeMeta[datetime]):
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
            raise KisNoneValueError

        return datetime.strptime(data, self.format).replace(tzinfo=self.timezone)


class KisDict(KisType[dict[str, Any]], metaclass=KisTypeMeta[dict[str, Any]]):
    __default__ = []

    def transform(self, data: Any) -> dict[str, Any]:
        if isinstance(data, dict):
            return data

        if data == "":
            raise KisNoneValueError

        return dict(data)


class KisTimeToDatetime(KisType[datetime], metaclass=KisTypeMeta[datetime]):
    __default__ = []

    format: str
    """시간 포맷"""
    timezone: tzinfo | None
    """타임존"""

    def __init__(self, format: str = "%H%M%S", timezone: tzinfo | None = TIMEZONE):
        super().__init__()
        self.format = format
        self.timezone = timezone

    def transform(self, data: Any) -> datetime:
        if isinstance(data, datetime):
            return data

        if data == "":
            raise KisNoneValueError

        return datetime.combine(
            datetime.now(self.timezone).date(),
            datetime.strptime(data, self.format).time(),
            tzinfo=self.timezone,
        )
