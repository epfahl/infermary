"""Test each type cast against a battery of example literals.

Notes
-----
* Update these tests to use only the public API.
"""

import pytest

from infermary.literals.casting import casters
from tests.examples import EXAMPLES


def _caster_test(func, literal, result):
    assert getattr(casters, func)(literal) == result


@pytest.mark.parametrize("literal, result", EXAMPLES["missing"])
def test_missing(literal, result):
    _caster_test("missing_", literal, result)


@pytest.mark.parametrize("literal, result", EXAMPLES["percent"])
def test_percent(literal, result):
    return _caster_test("percent_", literal, result)


@pytest.mark.parametrize("literal, result", EXAMPLES["currency"])
def test_currency(literal, result):
    return _caster_test("currency_", literal, result)


@pytest.mark.parametrize("literal, result", EXAMPLES["datetime"])
def test_datetime(literal, result):
    return _caster_test("datetime_", literal, result)


@pytest.mark.parametrize("literal, result", EXAMPLES["date"])
def test_date(literal, result):
    return _caster_test("date_", literal, result)


@pytest.mark.parametrize("literal, result", EXAMPLES["datelike"])
def test_datelike(literal, result):
    return _caster_test("datelike_", literal, result)


@pytest.mark.parametrize("literal, result", EXAMPLES["time"])
def test_time(literal, result):
    return _caster_test("time_", literal, result)


@pytest.mark.parametrize("literal, result", EXAMPLES["integer"])
def test_integer(literal, result):
    return _caster_test("integer_", literal, result)


@pytest.mark.parametrize("literal, result", EXAMPLES["float"])
def test_float(literal, result):
    return _caster_test("float_", literal, result)


@pytest.mark.parametrize("literal, result", EXAMPLES["number"])
def test_number(literal, result):
    return _caster_test("number_", literal, result)


@pytest.mark.parametrize("literal, result", EXAMPLES["boolean"])
def test_boolean(literal, result):
    return _caster_test("boolean_", literal, result)


@pytest.mark.parametrize("literal, result", EXAMPLES["string"])
def test_string(literal, result):
    return _caster_test("string_", literal, result)
