from types import EllipsisType, NoneType
from typing import (
    Any,
    Callable,
    Generic,
    Protocol,
    TypeVar,
    get_args,
    runtime_checkable,
)

from pykis import logging

__all__ = [
    "KisType",
    "TType",
    "KisDynamicScopedPath",
    "KisDynamic",
    "TDynamic",
    "KisTransform",
    "TListItem",
    "KisList",
    "KisObject",
    "KisNoneValueError",
]

T = TypeVar("T")

empty = object()


class KisTypeMeta(type, Generic[T]):
    def __getitem__(self, args: str | None | tuple[str | None, T | None | object]) -> T:
        return self()[args]


class KisType(Generic[T]):
    """한국투자증권 Open API 응답 타입"""

    __default__: list | None = None
    __default_type__: "KisType[Any] | None" = None

    field: str | None
    """응답 필드"""
    scope: str | None
    """응답 범위"""
    default: T | Callable[[], T] | None | object
    """기본값"""
    absolute: bool
    """
    절대 경로 여부

    절대 경로일 경우, 응답 데이터의 최상위를 기준으로 데이터를 가져옵니다.
    """

    def __init__(self):
        self.field = None
        self.scope = None
        self.default = empty
        self.absolute = False

    def __call__(
        self,
        field: str | None | EllipsisType = ...,
        default: T | Callable[[], T] | None | object | EllipsisType = ...,
        scope: str | None | EllipsisType = ...,
        absolute: bool | EllipsisType = ...,
    ) -> T:
        if not isinstance(field, EllipsisType):
            self.field = field

        if not isinstance(default, EllipsisType):
            self.default = default

        if not isinstance(scope, EllipsisType):
            self.scope = scope

        if not isinstance(absolute, EllipsisType):
            self.absolute = absolute

        return self  # type: ignore

    def __getitem__(self, args: str | None | tuple[str | None, T | Callable[[], T] | None | object]) -> T:
        if isinstance(args, tuple):
            return self(field=args[0] if args[0] else None, default=args[1])

        return self(field=args if args else None)

    def transform(self, data: Any) -> T:
        """응답 데이터를 변환합니다."""
        raise NotImplementedError

    @classmethod
    def default_type(cls) -> "KisType[Any]":
        if cls.__default__ is None:
            raise ValueError(f"{cls.__name__}은 기본 필드를 가지고 있지 않습니다.")

        if cls.__default_type__ is None:
            cls.__default_type__ = cls(*cls.__default__)

        return cls.__default_type__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(field={self.field!r}, scope={self.scope!r}, absolute={self.absolute!r})"


TType = TypeVar("TType", bound=KisType[Any])


class KisDynamicScopedPath:
    """응답 데이터 위치 표현"""

    path: list[str]
    """응답 데이터 위치"""

    def __init__(self, path: str | list[str]):
        self.path = path.split(".") if isinstance(path, str) else path

    def __call__(self, data: dict[str, Any]) -> dict[str, Any]:
        for key in self.path:
            data = data[key]

        return data

    def __repr__(self) -> str:
        return f"KisDynamicScope({self.path})"

    @classmethod
    def get_scope(cls, object: "KisDynamic | type[KisDynamic]") -> "KisDynamicScopedPath | None":
        """응답 데이터 위치 표현을 반환합니다."""
        if (scope := getattr(object, "__path__", None)) is None:
            return None

        if isinstance(scope, str):
            scope = KisDynamicScopedPath(scope)

            if isinstance(object, type):
                setattr(object, "__path__", scope)

        return scope


@runtime_checkable
class KisDynamicProtocol(Protocol):
    @property
    def __data__(self) -> dict[str, Any]:
        """원본 응답 데이터"""
        ...

    def raw(self) -> dict[str, Any] | None:
        """원본 응답 데이터의 복사본을 반환합니다."""
        ...


class KisDynamic:
    __verbose_missing__: bool = False
    """정의된 필드가 아닌 데이터가 있을 경우 경고 여부"""
    __ignore_missing__: bool = False
    """데이터에 정의된 필드가 없을 경우 예외 무시 여부"""
    __transform__: Callable[[type["KisDynamic"], dict[str, Any]], "KisDynamic"] | None = None
    """응답 데이터 변환 함수"""
    __path__: KisDynamicScopedPath | str | None = None
    """응답 데이터 위치 지정"""

    __data__: dict[str, Any] = None  # type: ignore
    """원본 응답 데이터"""

    def __pre_init__(self, data: dict[str, Any]) -> None:
        pass

    def __post_init__(self) -> None:
        pass

    def raw(self) -> dict[str, Any] | None:
        """원본 응답 데이터의 복사본을 반환합니다."""
        if self.__data__ is None:
            return None

        data = self.__data__.copy()
        data.pop("__response__", None)

        return data


TDynamic = TypeVar("TDynamic", bound=KisDynamic)


class KisTransformMeta(type, Generic[T]):
    def __getitem__(self, transform_fn: Callable[[dict[str, Any]], T]) -> T:
        return self(transform_fn)


class KisTransform(Generic[T], KisType[T], metaclass=KisTransformMeta):
    """응답 데이터 필드 값이 아닌 응답 데이터 전체를 변환합니다."""

    def __init__(self, transform_fn: Callable[[dict[str, Any]], T]):
        super().__init__()
        setattr(self, "transform", transform_fn)


TListItem = TypeVar("TListItem", bound=KisType[Any] | type[KisDynamic])


class KisList(Generic[TListItem], KisType[list[Any]], metaclass=KisTypeMeta[list[Any]]):
    type: TListItem
    """리스트 타입"""

    def __init__(self, type: TListItem):
        super().__init__()
        self.type = type

    def transform(self, data: Any) -> list[Any]:
        if not isinstance(data, list):
            raise TypeError(f"list 형을 기대하였지만, {type(data).__name__} 형이 입력되었습니다.")

        if isinstance(self.type, KisType):
            return [self.type.transform(item) for item in data]
        else:
            return [KisObject.transform_(item, self.type) for item in data]


class KisObject(Generic[TDynamic], KisType[TDynamic], metaclass=KisTypeMeta):
    type_: type[TDynamic] | Callable[[], TDynamic]

    def __init__(self, type: type[TDynamic] | Callable[[], TDynamic]):
        super().__init__()
        self.type_ = type

    def transform(self, data: Any) -> TDynamic:
        return self.transform_(data, self.type_)

    @classmethod
    def transform_(
        cls,
        data: Any,
        transform_type: TDynamic | type[TDynamic] | Callable[[], TDynamic],
        ignore_missing: bool = False,
        ignore_missing_fields: set[str] | None = None,
        ignore_path: bool = False,
        pre_init: bool = True,
        post_init: bool = True,
        scope: str | None = None,
    ) -> TDynamic:
        if not isinstance(data, dict):
            raise TypeError(f"dict 형을 기대하였지만, {type(data).__name__} 형이 입력되었습니다.")

        if isinstance(transform_type, type):
            if (transform_fn := getattr(transform_type, "__transform__", None)) is not None:
                object = transform_fn(transform_type, data)
                setattr(object, "__data__", data)

                if post_init and hasattr(object, "__post_init__"):
                    object.__post_init__()

                return object

        object = transform_type if isinstance(transform_type, KisDynamic) else transform_type()
        object_type = type(object)

        if pre_init and hasattr(object, "__pre_init__"):
            object.__pre_init__(data)

        parsing_data = data

        if not ignore_path:
            scoped_path = KisDynamicScopedPath.get_scope(object_type)

            if scoped_path is not None:
                parsing_data = scoped_path(data)

        ignore_missing = ignore_missing or getattr(object_type, "__ignore_missing__", False)
        annotations = {
            key: value
            for obj in object_type.__mro__
            if (annotations := getattr(obj, "__annotations__", None)) is not None
            for key, value in annotations.items()
        }
        missing = set(parsing_data.keys())
        missing.discard("__response__")

        for key, type_, anno in (
            (field, type_, annotations.get(field, None))
            for field in dir(object_type)
            if (not field.startswith("_") or field.endswith("_"))
            and (
                isinstance(type_ := getattr(object_type, field, None), KisType)
                or (isinstance(type_, type) and issubclass(type_, KisType))
            )
        ):
            if isinstance(type_, type):
                if (getattr(type_, "__default__", None)) is None:
                    raise ValueError(
                        f"{object_type.__name__}의 {key} 필드에 {type_.__name__}은 간접적으로 타입을 지정할 수 없습니다."
                    )

                type_ = type_.default_type()

            if scope is not None and type_.scope != scope:
                continue

            field = None if isinstance(type_, KisTransform) else type_.field or key
            nullable = NoneType in get_args(anno) if anno else None
            target_data = data if type_.absolute else parsing_data

            if field is not None and target_data is parsing_data:
                missing.discard(field)

            if field is None:
                value = target_data
            elif field not in target_data:
                if type_.default is empty:
                    if ignore_missing:
                        continue

                    raise KeyError(f"{object_type.__name__}.{key} 필드의 {field}값이 존재하지 않습니다. ({type_!r})")

                if callable(type_.default):
                    value = type_.default()
                else:
                    value = type_.default
            else:
                value = target_data[field]

            result = empty

            if value is not None:
                try:
                    result = type_.transform(value)
                except KisNoneValueError:
                    pass
                except Exception as e:
                    raise ValueError(
                        f"{object_type.__name__}.{key} 필드를 변환하는 중 오류가 발생했습니다.\n→ {type(e).__name__}: {e}"
                    ) from e

            if result is empty:
                if nullable:
                    result = None
                else:
                    raise ValueError(f"{object_type.__name__}.{key} 필드의 값이 빈 값입니다.")

            setattr(object, key, result)

        if missing and getattr(object_type, "__verbose_missing__", False):
            if ignore_missing_fields is not None:
                missing -= ignore_missing_fields

            if missing:
                logging.logger.warning(f"{object_type.__name__}에 정의되지 않은 필드가 있습니다: {', '.join(missing)}")

        setattr(object, "__data__", data)

        if post_init and hasattr(object, "__post_init__"):
            object.__post_init__()

        return object  # type: ignore


class KisNoneValueError(Exception):
    """빈 값이 입력되었을 때 발생하는 예외"""

    pass
