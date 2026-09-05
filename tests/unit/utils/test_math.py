from decimal import Decimal

import pytest

from vmkis.utils.math import safe_divide


@pytest.mark.parametrize(
    "a,b,expected,expected_type",
    [
        # ints -> result is float (Python true division)
        (6, 3, 2.0, float),
        (7, 2, 3.5, float),
        # floats -> float
        (5.0, 2.0, 2.5, float),
        # Decimal -> Decimal
        (Decimal("5"), Decimal("2"), Decimal("2.5"), Decimal),
        # division by zero returns zero of the input type
        (5, 0, 0, int),
        (5.0, 0.0, 0.0, float),
        (Decimal("5"), Decimal("0"), Decimal("0"), Decimal),
        # mixed types: int / float -> float
        (5, 2.0, 2.5, float),
        # mixed zero: int a, float b==0.0 (falsy) -> returns type(a)() == int 0
        (5, 0.0, 0, int),
    ],
)
def test_safe_divide_various_types(a, b, expected, expected_type):
    result = safe_divide(a, b)

    # check value equality (Decimal supports ==)
    assert result == expected

    # check return type (Decimal should be Decimal, floats/ints as expected)
    assert isinstance(result, expected_type)


def test_safe_divide_no_zero_division_error_for_nonzero():
    # ensure no ZeroDivisionError for normal divisors
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(Decimal("10"), Decimal("4")) == Decimal("2.5")
