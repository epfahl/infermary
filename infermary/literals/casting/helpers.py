"""Library of helper functions for literal casting.
"""

from datetime import datetime
from math import fabs
import re


NUMBER_WITH_COMMAS_PATTERN = re.compile(r"^-?(?!0)\d{1,3}(,\d{3})+(\.\d+)?$")

MULTIPLIERS = {
    'k': 1e3,
    'm': 1e6,
    'b': 1e9,
    't': 1e12,
}


def _strip_numeric_commas(literal):
    """If the literal matches the pattern of a number with commas, return the
    string with the commas removed; otherwise, return the literal.

    Examples
    --------
    >>> _strip_numeric_commas("1,234")
    "1234"
    >>> _strip_numeric_commas("1234")
    "1234"
    >>> _strip_numeric_commas("1,234.5")
    "1234.5"
    >>> _strip_numeric_commas("12,34.5")
    "12,34.5"
    """
    if NUMBER_WITH_COMMAS_PATTERN.match(literal) is None:
        return literal
    return literal.replace(",", "")


def _has_nonnumeric_leading_zero(literal):
    """Return True if the literal has a leading zero that is inconsistent with
    a numeric pattern.

    Examples
    --------
    >>> has_nonnumeric_leading_zero("0")
    False
    >>> has_nonnumeric_leading_zero("01")
    True
    >>> has_nonnumeric_leading_zero("0.1")
    False
    >>> has_nonnumeric_leading_zero("01.1")
    True
    """
    whole_part = literal.split(".")[0]
    return len(whole_part) > 1 and whole_part.startswith("0")


def to_number(literal):
    """Return a floating point number if the literal matches the pattern of a
    number and float conversion is successful.

    Examples
    --------
    >>> to_number("1.0")
    1.0
    >>> to_number("1,234.5")
    1234.5
    >>> to_number("1e-1")
    0.1
    >>> to_number("-1.1e1")
    -11.0
    >>> to_number("1,23,4.5")  # Error
    """
    if not _has_nonnumeric_leading_zero(literal):
        return float(_strip_numeric_commas(literal))
    raise TypeError


def to_float(literal):
    """Return a floating point number if float conversion is successful and
    1) the string has exactly one decimal point.
    or (inclusive)
    2) the string as exactly one "e" (or "E") and the cast float is in (0, 1).

    Examples
    --------
    >>> to_float("1.0")
    1.0
    >>> to_float(".0")
    0.0
    >>> to_float("1e-1")
    0.1
    >>> to_float("1.e-1")
    0.1
    >>> to_float("1")   # Error
    >>> to_float("1e0")   # Error
    >>> to_float("1e-0")  # Error
    """
    value = to_number(literal)
    has_one_dot = (literal.count(".") == 1)
    exp_in_01 = (
        (literal.lower().count("e") == 1) and
        (0 < fabs(value) < 1))
    if has_one_dot or exp_in_01:
        return value
    raise TypeError


def to_integer(literal):
    """Return an integer if float conversion is successful and
    1) the string has no decimal point
    and
    2) the float conversion numerically equals the integer conversion

    Examples
    --------
    >>> to_integer("1")
    1
    >>> to_integer("1e1")
    10
    >>> to_integer("1e-0")
    1
    >>> to_integer("1.0")  # Error
    >>> to_integer("0.0")  # Error
    >>> to_integer("1.e-0")  # Error
    """
    float_value = to_number(literal)
    int_value = int(float_value)
    has_no_dot = (literal.count(".") == 0)
    if has_no_dot and (float_value == int_value):
        return int_value
    raise TypeError


def handle_numeric(literal, conv_func):
    """Attempt to convert the given string literal to a value using the given
    conversion function.
    """
    try:
        return conv_func(literal)
    except ValueError:
        raise TypeError


def handle_percent(literal, regexes):
    """Attempt to convert the given string literal to a number, which has a
    percent sign.
    """
    for regex in regexes:
        percent = regex.search(literal)
        if percent:
            negative, value = percent.groups()
            if value == '':  # Accounts for literals of '%'
                continue
            value = to_number(value) / 100
            return value * -1 if negative else value
    raise TypeError


def handle_currency(literal, regexes):
    """Attempt to convert the given string literal to a number, which has a
    dollar sign.
    """
    for regex in regexes:
        currency = regex.search(literal)
        if currency:
            parens, negative, value, character = currency.groups()
            if value == '':  # Accounts for literals of '$'
                continue
            if character:
                multiplier = MULTIPLIERS.get(character.lower(), 1)
            else:
                multiplier = 1
            value = to_number(value) * multiplier
            return value * -1 if negative or parens else value
    raise TypeError


def handle_datetime(literal, patterns):
    """Attempt to return a datetime object for the given string literal and
    list of datetime formats.
    """
    for pattern in patterns:
        try:
            return datetime.strptime(literal, pattern)
        except ValueError:
            continue
    raise TypeError
