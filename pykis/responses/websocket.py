from types import NoneType
from typing import Any, Iterable, Protocol, TypeVar, get_args, runtime_checkable

from pykis import logging
from pykis.responses.dynamic import KisNoneValueError, KisType, empty
from pykis.responses.types import KisAny

__all__ = [
    "TWebsocketResponse",
    "KisWebsocketResponse",
]


@runtime_checkable
class KisWebsocketResponseProtocol(Protocol):
    """한국투자증권 실시간 응답 클래스"""

    @property
    def __data__(self) -> list[str]:
        """원본 데이터"""
        ...

    def raw(self) -> list[str]:
        """원본 응답 데이터를 반환합니다."""
        ...


class KisWebsocketResponse:
    """한국투자증권 실시간 응답 클래스"""

    __fields__: list[KisType | type[KisType] | Any | None] = []
    """파싱할 필드 목록"""

    __data__: list[str]
    """원본 데이터"""

    def __pre_init__(self, data: list[str]) -> None:
        pass

    def __post_init__(self) -> None:
        pass

    def raw(self) -> list[str]:
        """원본 응답 데이터를 반환합니다."""
        return self.__data__

    @classmethod
    def parse(
        cls,
        data: str,
        /,
        count: int | None = None,
        split: str = "^",
        *,
        response_type: "type[TWebsocketResponse]",
    ) -> "Iterable[TWebsocketResponse]":
        """
        데이터를 파싱합니다.

        Args:
            data (str): 데이터
            count (int | None): 데이터 갯수
            split (str): 데이터 구분자
            response_type (Callable[..., TWebsocketResponse]): 응답 클래스
        """
        items = data.split(split)
        fields = getattr(response_type, "__fields__", None)

        if not fields:
            response = response_type()

            if (pre_init := getattr(response, "__pre_init__", None)) is not None:
                pre_init(items)

            setattr(response, "__data__", items)

            if (post_init := getattr(response, "__post_init__", None)) is not None:
                post_init()

            yield response
            return

        if len(items) % len(fields) != 0:
            raise ValueError(f"Invalid data length: {len(items)}")

        # 필드 갯수 검증
        if count is not None:
            if len(items) // len(fields) != count:
                raise ValueError(f"Invalid data count: {len(items) / len(fields)}")
        else:
            count = len(items) // len(fields)

        # 각 아이템의 필드를 묶음 [A, A, B, B] -> [(A, A), (B, B)]
        try:
            for values in zip(*[iter(items)] * len(fields)):
                values: list[str]
                response = response_type()

                if (pre_init := getattr(response, "__pre_init__", None)) is not None:
                    pre_init(values)

                setattr(response, "__data__", values)

                annotation = response_type.__annotations__

                for i, (field, value) in enumerate(zip(fields, values)):
                    if field is None:
                        continue

                    if isinstance(field, type):
                        field = field.default_type()

                    if field.field is None:
                        logging.logger.warning(f"{response_type.__name__}[{i}] 필드의 이름이 지정되지 않았습니다.")
                        continue

                    try:
                        if isinstance(field, KisAny) and field.absolute:
                            value = field.transform(values)
                        else:
                            value = field.transform(value)

                        setattr(response, field.field, value)
                    except KisNoneValueError:
                        nullable = NoneType in get_args(anno) if (anno := annotation.get(field.field)) else False

                        default_value = None if field.default is empty else field.default

                        if callable(default_value):
                            default_value = default_value()

                        if default_value is None and not nullable:
                            raise ValueError(f"{response_type.__name__}.{field.field} 필드가 None일 수 없습니다.")

                        setattr(response, field.field, default_value)

                    except Exception as e:
                        raise ValueError(
                            f"{response_type.__name__}.{field.field} 필드를 변환하는 중 오류가 발생했습니다.\n→ {type(e).__name__}: {e}"
                        ) from e

                if (post_init := getattr(response, "__post_init__", None)) is not None:
                    post_init()

                yield response
        except Exception as e:
            raise ValueError(f"데이터 파싱 중 오류가 발생했습니다.\n→ {type(e).__name__}: {e}") from e


TWebsocketResponse = TypeVar("TWebsocketResponse", bound=KisWebsocketResponseProtocol)
