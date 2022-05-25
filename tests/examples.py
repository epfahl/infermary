"""Input/Output examples for type casting, including expected failures.
"""

from datetime import datetime

import pytest


_DATETIME = datetime(2017, 10, 13, 15, 14, 13)
_DATETIME_ROUNDED = _DATETIME.replace(second=0)
_DATE = _DATETIME.date()
_TIME = _DATETIME.time()
_TIME_ROUNDED = _DATETIME_ROUNDED.time()


def xfail(value):
    return pytest.param(value, None, marks=pytest.mark.xfail)


EXAMPLES = {
    "missing": [
        ("", None),
        ("NaN", None),
        ("nan", None),
        ("null", None),
        ("None", None),
        ("NULL", None),
        xfail("a"),
        xfail("1"),
    ],
    "percent": [
        ("0.0%", 0),
        ("0%", 0),
        ("1.098%", 0.01098),
        ("398,980.0%", 3989.8),
        ("3%", 0.03),
        ("-3%", -0.03),
        ("-33.3098%", -0.333098),
        xfail("1%%"),
        xfail("%3"),
        xfail("a"),
        xfail("1"),
        xfail("%"),
    ],
    "currency": [
        ("$0.00", 0),
        ("$0", 0),
        ("$100,099.93", 100099.93),
        ("-$0.98", -0.98),
        ("($398.98)", -398.98),
        ("$198K", 198000),
        ("$1b", 1000000000),
        ("$19,000M", 19000000000),
        xfail("$$1"),
        xfail("1$"),
        xfail("$1e"),
        xfail("a"),
        xfail("1"),
        xfail("$"),
    ],
    "datetime": [
        ("2017-10-13 15:14:13", _DATETIME),
        ("2017-10-13T15:14:13", _DATETIME),
        ("2017-10-13T15:14:13Z", _DATETIME),
        ("2017-10-13 15:14", _DATETIME_ROUNDED),
        xfail("2017-13-10 15:14:13"),
        xfail("2017-10-13"),
        xfail("15:14:13"),
        xfail("a"),
        xfail("1"),
    ],
    "date": [
        ("2017-10-13", _DATE),
        ("10/13/2017", _DATE),
        ("10/13/17", _DATE),
        xfail("2017-10-13 15:14:13"),
        xfail("13/10/2017"),
        xfail("a"),
        xfail("1"),
    ],
    "datelike": [
        ("2017-10-13", _DATE),
        ("10/13/2017", _DATE),
        ("2017-10-13 15:14:13", _DATE),
    ],
    "time": [
        ("15:14:13", _TIME),
        ("15:14", _TIME_ROUNDED),
        ("3:14:13 PM", _TIME),
        ("3:14pm", _TIME_ROUNDED),
        xfail("15:14:13 pm"),
        xfail("2017-10-13 15:14:13"),
        xfail("a"),
        xfail("1"),
    ],
    "integer": [
        ("1", 1),
        ("2017", 2017),
        ("1e1", 10),
        ("1e-0", 1),
        ("-1", -1),
        ("1,234,567", 1234567),
        xfail("1,23,4"),
        xfail("01,234"),
        xfail("01"),
        xfail("1.0"),
        xfail("0.0"),
        xfail("a"),
        xfail("1.23"),
        xfail("1.e-0"),
    ],
    "float": [
        ("1.23", 1.23),
        ("0.1", 0.1),
        ("1e-1", 0.1),
        ("-1.23e1", -12.3),
        ("1,234,567.89", 1234567.89),
        xfail("12,34.56"),
        xfail("01.2"),
        xfail("1"),
        xfail("1e0"),
        xfail("1e-0"),
        xfail("a"),
        xfail("1.23"),
    ],
    "number": [
        ("0", 0.0),
        ("1", 1.0),
        ("0.1", 0.1),
        ("1e1", 10.0),
        ("1e-1", 0.1),
        ("-1.23e1", -12.3),
        ("1,234,567.89", 1234567.89),
        xfail("12,34.56"),
        xfail("01.2"),
        xfail(""),
        xfail("a"),
    ],
    "boolean": [
        ("True", True),
        ("true", True),
        ("TRUE", True),
        ("False", False),
        ("false", False),
        ("FALSE", False),
        xfail("A"),
        xfail("T"),
        xfail("1"),
        xfail("0"),
    ],
    "string": [
        ("foo", "foo"),
        ("", None),
        ("NaN", None),
        ("nan", None),
        ("null", None),
        ("None", None),
        ("NULL", None),
    ],
}
