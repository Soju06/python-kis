from datetime import timedelta

import pytest

from vmkis.utils.timex import parse_timex, timex


@pytest.mark.parametrize(
    "expr,expected",
    [
        (
            ("1", "h"),
            timedelta(hours=1),
        ),  # tuple with strings (should fail int conversion normally; using int tuple below)
    ],
)
def test_parse_timex_with_tuple_strings_raises_value_error(expr, expected):
    # parse_timex expects tuple[int, str]; feeding wrong types should raise TypeError/ValueError
    with pytest.raises((TypeError, ValueError)):
        parse_timex(expr)


def test_parse_timex_with_tuple_valid():
    assert parse_timex((2, "h")) == timedelta(hours=2)
    assert parse_timex((10, "d")) == timedelta(days=10)
    assert parse_timex((1, "M")) == timedelta(days=30)


def test_parse_timex_with_string_valid():
    assert parse_timex("1h") == timedelta(hours=1)
    assert parse_timex("10d") == timedelta(days=10)
    assert parse_timex("3w") == timedelta(weeks=3)


def test_parse_timex_invalid_no_leading_digits():
    with pytest.raises(ValueError, match=r"Invalid time expression: h"):
        parse_timex("h")


def test_parse_timex_invalid_suffix_from_tuple_and_from_string():
    # The error message shows "None" because suffix is looked up in TIMEX_SUFFIX dictionary
    with pytest.raises(ValueError, match=r"Invalid timex expression suffix: None"):
        parse_timex((1, "q"))

    with pytest.raises(ValueError, match=r"Invalid timex expression suffix: None"):
        # "10" becomes value=1, suffix="0" due to implementation slicing behavior
        parse_timex("10")


def test_timex_empty_and_no_matches_errors():
    with pytest.raises(ValueError, match="Empty timex expression"):
        timex("")

    with pytest.raises(ValueError, match=r"Invalid timex expression: abc"):
        timex("abc")


def test_timex_combined_expressions_and_values():
    assert timex("1w2d") == timedelta(days=9)
    assert timex("1d4h") == timedelta(days=1, hours=4)
    assert timex("1h") == timedelta(hours=1)
    # multiple same units
    assert timex("2h30m") == timedelta(hours=2, minutes=30)


def test_timex_pattern_edge_cases():
    # Leading zeros and multi-digit numbers
    assert timex("01d") == timedelta(days=1)
    assert timex("100s") == timedelta(seconds=100)
