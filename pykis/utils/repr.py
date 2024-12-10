from functools import wraps
from io import StringIO
from typing import Any, Iterable, Literal, Protocol, TypeVar

__all__ = [
    "SINGLE_LINE_MAX_LENGTH",
    "REPR_LINE_MODE",
    "TObject",
    "kis_repr",
    "custom_repr",
    "remove_custom_repr",
    "dict_repr",
    "list_repr",
    "tuple_repr",
    "set_repr",
    "object_repr",
]

SINGLE_LINE_MAX_LENGTH = 100


class UnboundedType:
    def __eq__(self, other):
        return isinstance(other, UnboundedType)

    def __repr__(self):
        return "Unbounded"


UNBOUNDED = UnboundedType()

REPR_LINE_MODE = Literal["single", "multiple"]

TObject = TypeVar("TObject")


def kis_repr(
    *fields: str,
    lines: REPR_LINE_MODE | None = None,
    field_lines: dict[str, REPR_LINE_MODE] | None = None,
    indent: str = "    ",
    max_depth: int = 7,
):
    def decorator(cls: type[TObject]) -> type[TObject]:
        @wraps(cls.__repr__)
        def __repr__(self, _depth: int = 0) -> str:
            return object_repr(
                self,
                fields=fields or None,
                lines=lines,
                field_lines=field_lines,
                indent=indent,
                max_depth=max_depth,
                _depth=_depth,
            )

        __repr__.__doc__ = f"Return a string representation of {cls.__name__} object."
        __repr__.__annotations__ = {"self": cls}
        __repr__.__module__ = cls.__module__
        __repr__.__qualname__ = f"{cls.__qualname__}.__repr__"
        __repr__.__name__ = "__repr__"
        __repr__.__is_kis_repr__ = True  # type: ignore

        cls.__repr__ = __repr__
        return cls

    return decorator


def _append_with_indent(sb: StringIO, value: str, indent: str):
    lines = value.splitlines()
    for i in range(len(lines)):
        if i > 0:
            sb.write("\n")

        sb.write(indent)
        sb.write(lines[i])


class ReprFunction(Protocol):
    def __call__(self, obj: Any, max_depth: int = 7, depth: int = 0) -> str: ...


custom_reprs: dict[type, ReprFunction] = {}


def custom_repr(cls: type, fn: ReprFunction):
    custom_reprs[cls] = fn


def remove_custom_repr(cls: type):
    custom_reprs.pop(cls, None)


def _repr(
    obj: object,
    lines: REPR_LINE_MODE | None = None,
    indent: str = "    ",
    max_depth: int = 7,
    _depth: int = 0,
) -> str:
    if _depth >= max_depth:
        return "..."

    if isinstance(obj, dict):
        return dict_repr(
            obj,
            lines=lines,
            indent=indent,
            max_depth=max_depth,
            _depth=_depth,
        )
    elif isinstance(obj, list):
        return list_repr(
            obj,
            lines=lines,
            indent=indent,
            max_depth=max_depth,
            _depth=_depth,
        )
    elif isinstance(obj, tuple):
        return tuple_repr(
            obj,
            lines=lines,
            indent=indent,
            max_depth=max_depth,
            _depth=_depth,
        )
    elif isinstance(obj, (set, frozenset)):
        return set_repr(
            obj,
            lines=lines,
            indent=indent,
            max_depth=max_depth,
            _depth=_depth,
        )
    elif (repr_fn := getattr(obj, "__repr__", None)) and getattr(repr_fn, "__is_kis_repr__", False):
        return repr_fn(_depth=_depth)
    else:
        for cls, fn in custom_reprs.items():
            if isinstance(obj, cls):
                return fn(
                    obj,
                    depth=_depth,
                    max_depth=max_depth,
                )

        return repr(obj)


def dict_repr(
    dct: dict,
    lines: REPR_LINE_MODE | None = None,
    indent: str = "    ",
    ellipsis: int | None = None,
    max_depth: int = 7,
    _depth: int = 0,
) -> str:
    if _depth >= max_depth:
        return "{:...}"

    values = []
    length = len(dct)
    has_ellipsis = length > (ellipsis or length)

    for i, (k, v) in enumerate(dct.items()):
        if i >= (ellipsis or length):
            break

        values.append(
            (
                k,
                _repr(
                    v,
                    indent=indent,
                    max_depth=max_depth,
                    _depth=_depth + 1,
                ),
            )
        )

    if lines is None:
        lines = (
            "single"
            if (
                len(values) <= 5  # 5 or less
                and not has_ellipsis  # "..." is not included
                and sum(len(k) + len(v) + 4 for k, v in values) - 1 <= SINGLE_LINE_MAX_LENGTH  # ": , "
                and not any("\n" in v for _, v in values)  # single line
            )
            else "multiple"
        )

    sb = StringIO()

    if lines == "single":
        sb.write("{")
        for i, (k, v) in enumerate(values):
            if i > 0:
                sb.write(", ")

            sb.write(f"{k!r}: {v}")

        # logic compatible
        if has_ellipsis:
            sb.write(", ...")

        sb.write("}")
    else:
        sb.write("{\n")

        for i, (k, v) in enumerate(values):
            if i > 0:
                sb.write(",\n")

            _append_with_indent(sb, f"{k!r}: {v}", indent)

        sb.write("\n")

        if has_ellipsis:
            sb.write(indent)
            sb.write("...\n")

        sb.write("}")

    sb.flush()

    return sb.getvalue()


def list_repr(
    lst: Iterable,
    lines: REPR_LINE_MODE | None = None,
    indent: str = "    ",
    ellipsis: int | None = None,
    max_depth: int = 7,
    _depth: int = 0,
) -> str:
    return _iterable_repr(
        lst,
        "[]",
        lines=lines,
        indent=indent,
        ellipsis=ellipsis,
        max_depth=max_depth,
        _depth=_depth,
    )


def tuple_repr(
    tpl: tuple,
    lines: REPR_LINE_MODE | None = None,
    indent: str = "    ",
    ellipsis: int | None = None,
    max_depth: int = 7,
    _depth: int = 0,
) -> str:
    return _iterable_repr(
        tpl,
        "()",
        lines=lines,
        indent=indent,
        ellipsis=ellipsis,
        max_depth=max_depth,
        _depth=_depth,
    )


def set_repr(
    st: set | frozenset,
    lines: REPR_LINE_MODE | None = None,
    indent: str = "    ",
    ellipsis: int | None = None,
    max_depth: int = 7,
    _depth: int = 0,
) -> str:
    return _iterable_repr(
        st,
        "{}",
        lines=lines,
        indent=indent,
        ellipsis=ellipsis,
        max_depth=max_depth,
        _depth=_depth,
    )


def _iterable_repr(
    lst: Iterable,
    tie: str = "[]",
    lines: REPR_LINE_MODE | None = None,
    indent: str = "    ",
    ellipsis: int | None = None,
    max_depth: int = 7,
    _depth: int = 0,
) -> str:
    if len(tie) == 0 or len(tie) % 2 != 0:
        raise ValueError("tie must be even length")

    open_tie = tie[: len(tie) // 2]
    close_tie = tie[len(tie) // 2 :]

    if _depth >= max_depth:
        return f"{open_tie}...{close_tie}"

    if not isinstance(lst, (list, tuple, set, frozenset)):
        lst = list(lst)

    if not lst:
        return f"{open_tie}{close_tie}"

    values = []
    length = len(lst)
    has_ellipsis = length > (ellipsis or length)

    for i, value in enumerate(lst):
        if i >= (ellipsis or length):
            break

        values.append(
            _repr(
                value,
                indent=indent,
                max_depth=max_depth,
                _depth=_depth + 1,
            )
        )

    if lines is None:
        lines = (
            "single"
            if (
                len(values) <= 5  # 5 or less
                and not has_ellipsis  # "..." is not included
                and sum(len(v) + 2 for v in values) - 1 <= SINGLE_LINE_MAX_LENGTH  # ", "
                and not any("\n" in v for v in values)  # single line
            )
            else "multiple"
        )

    sb = StringIO()

    if lines == "single":
        sb.write(open_tie)
        for i, v in enumerate(values):
            if i > 0:
                sb.write(", ")
            sb.write(v)

        # logic compatible
        if has_ellipsis:
            sb.write(", ...")

        sb.write(close_tie)
    else:
        sb.write(open_tie)
        sb.write("\n")

        for i in range(len(values)):
            if i > 0:
                sb.write(",\n")

            _append_with_indent(sb, values[i], indent)

        sb.write("\n")

        if has_ellipsis:
            sb.write(indent)
            sb.write("...\n")

        sb.write(close_tie)

    sb.flush()

    return sb.getvalue()


def object_repr(
    obj: object,
    fields: list[str] | tuple[str, ...] | None = None,
    lines: REPR_LINE_MODE | None = None,
    field_lines: dict[str, REPR_LINE_MODE] | None = None,
    indent: str = "    ",
    max_depth: int = 7,
    _depth: int = 0,
) -> str:
    if _depth >= max_depth:
        return f"{obj.__class__.__name__}(...)"

    if fields is None:
        fields = [f for f in dir(obj) if not f.startswith("_")]

    values = []

    for field in fields:
        try:
            value = getattr(obj, field)
        except AttributeError:
            value = UNBOUNDED

        values.append(
            (
                field,
                (
                    value
                    if value is UNBOUNDED
                    else _repr(
                        value,
                        lines=field_lines.get(field) if field_lines else None,
                        indent=indent,
                        max_depth=max_depth,
                        _depth=_depth + 1,
                    )
                ),
            )
        )

    sb = StringIO()

    if lines is None:
        lines = (
            "single"
            if (
                len(values) <= 5  # 5 or less
                and sum(len(k) + len(v) + 2 for k, v in values) - 1 <= SINGLE_LINE_MAX_LENGTH  # "=,"
                and not any("\n" in v for _, v in values)  # single line
            )
            else "multiple"
        )

    if lines == "single":
        sb.write(f"{obj.__class__.__name__}(")
        for i, (k, v) in enumerate(values):
            if i > 0:
                sb.write(", ")

            sb.write(f"{k}={v}")

        sb.write(")")
    else:
        sb.write(f"{obj.__class__.__name__}(\n")

        for i, (k, v) in enumerate(values):
            if i > 0:
                sb.write(",\n")

            _append_with_indent(sb, f"{k}={v}", indent)

        sb.write("\n)")

    sb.flush()

    return sb.getvalue()


#####################################
## PyKis Custom Repr Functions
#####################################

from datetime import date, datetime, time
from decimal import Decimal
from zoneinfo import ZoneInfo


def decimal_repr(obj: Decimal, max_depth: int = 7, depth: int = 0) -> str:
    return format(obj.normalize(), "f")


def datetime_repr(obj: datetime, max_depth: int = 7, depth: int = 0) -> str:
    return repr(obj.isoformat())


def date_repr(obj: date, max_depth: int = 7, depth: int = 0) -> str:
    return repr(obj.isoformat())


def time_repr(obj: time, max_depth: int = 7, depth: int = 0) -> str:
    return repr(obj.isoformat())


def zoneinfo_repr(obj: ZoneInfo, max_depth: int = 7, depth: int = 0) -> str:
    return f"{ZoneInfo.__name__}({obj.key!r})"


custom_repr(Decimal, decimal_repr)
custom_repr(datetime, datetime_repr)
custom_repr(date, date_repr)
custom_repr(time, time_repr)
custom_repr(ZoneInfo, zoneinfo_repr)
