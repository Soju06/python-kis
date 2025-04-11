from decimal import Decimal
from typing import overload


@overload
def safe_divide(a: int, b: int) -> float: ...


@overload
def safe_divide(a: float, b: float) -> float: ...


@overload
def safe_divide(a: Decimal, b: Decimal) -> Decimal: ...


def safe_divide(a: int | float | Decimal, b: int | float | Decimal) -> int | float | Decimal:
    return a / b if b else type(a)()
