import re
from datetime import timedelta

__all__ = [
    "TIMEX_TYPE",
    "parse_timex",
    "timex",
]

TIMEX_TYPE = str

TIMEX_SUFFIX = {
    "y": timedelta(days=365),
    "M": timedelta(days=30),
    "w": timedelta(days=7),
    "d": timedelta(days=1),
    "h": timedelta(hours=1),
    "m": timedelta(minutes=1),
    "s": timedelta(seconds=1),
}

TIMEX_PATTERN = re.compile(r"(\d+)([a-zA-Z]+)")


def parse_timex(expression: str | tuple[int, str]) -> timedelta:
    """
    Parse time expression

    Args:
        expression (str): time expression

    Examples:
        >>> parse_timex("1h")
        timedelta(hours=1)
        >>> parse_timex("10d")
        timedelta(days=10)

    Raises:
        ValueError: invalid time expression

    """
    if isinstance(expression, tuple):
        value, suffix = expression
    else:
        i = 0

        for i, c in enumerate(expression):
            if not c.isdigit():
                break

        if not i:
            raise ValueError(f"Invalid time expression: {expression}")

        value, suffix = int(expression[:i]), expression[i:]

    suffix = TIMEX_SUFFIX.get(suffix, None)

    if suffix is None:
        raise ValueError(f"Invalid timex expression suffix: {suffix}")

    return suffix * value


def timex(expression: str) -> timedelta:
    """
    Parse time expression

    Args:
        expression (str): time expression

    Examples:
        >>> timex("1h")
        timedelta(hours=1)
        >>> timex("1d")
        timedelta(days=1)
        >>> timex("1w2d")
        timedelta(days=9)
        >>> timex("1d4h")
        timedelta(days=1, hours=4)

    Raises:
        ValueError: invalid time expression
    """
    if not expression:
        raise ValueError("Empty timex expression")

    matches = TIMEX_PATTERN.findall(expression)
    value = timedelta()

    if not matches:
        raise ValueError(f"Invalid timex expression: {expression}")

    for match in matches:
        value += parse_timex((int(match[0]), match[1]))

    return value
