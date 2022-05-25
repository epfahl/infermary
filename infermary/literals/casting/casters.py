"""Library of functions that attempt to cast string values to instances of
objects with the indicated type.  All casting functions raise a TypeError if
the cast fails.
"""

from infermary.literals.casting import formats as fmt
from infermary.literals.casting import helpers as hp


def missing_(literal):
    """Cast the literal as None if it matches one of the specified missing
    sentinel values.
    """
    if literal in fmt.MISSING:
        return None
    raise TypeError


def percent_(literal):
    """Cast the literal to a number if the literal has a percent sign.
    """
    return hp.handle_percent(literal, fmt.PERCENT)


def currency_(literal):
    """Cast the literal to a number if the literal has a dollar sign.
    """
    return hp.handle_currency(literal, fmt.CURRENCY)


def datetime_(literal):
    """Cast the literal to a datetime.datetime object if it matches one of the
    specified datetime.datetime string patterns.
    """
    return hp.handle_datetime(literal, fmt.DATETIME)


def date_(literal):
    """Cast the literal to a datetime.date object if it matches one of the
    specified datetime.date string patterns.
    """
    return hp.handle_datetime(literal, fmt.DATE).date()


def time_(literal):
    """Cast the literal to a datetime.time object if it matches one of the
    specified datetime.time string patterns."""
    return hp.handle_datetime(literal, fmt.TIME).time()


def number_(literal):
    """Cast the literal to a float if it is converted successfully by the
    `to_number` function.
    """
    return hp.handle_numeric(literal, hp.to_number)


def integer_(literal):
    """Cast the literal to an integer if it is converted successfully by the
    `to_integer` function.
    """
    return hp.handle_numeric(literal, hp.to_integer)


def float_(literal):
    """Cast the literal to a float if it is converted successfully by the
    `to_float` function.
    """
    return hp.handle_numeric(literal, hp.to_float)


def boolean_(literal):
    """Cast the literal to True (False) if it matches one of the True (False)
    sentinel values.
    """
    if literal in fmt.TRUE:
        return True
    elif literal in fmt.FALSE:
        return False
    raise TypeError


def string_(literal):
    """Cast the literal to a string if it is converted successfully by the `str`
    function.
    """
    return None if literal in fmt.MISSING else literal


def datelike_(literal):
    """Cast the literal to a datetime.date object if it matches the string
    pattern of a datetime.date or datetime.datetime.

    WARNING: This casting is lossy if the input is a datetime.
    """
    return hp.handle_datetime(literal, fmt.DATELIKE).date()
