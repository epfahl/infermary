"""Module that holds allowed string formats for relevant types.
"""

import re


MISSING = ["", "NaN", "nan", "null", "None", "NULL"]

PERCENT = [re.compile(r"([-]?)(\d{0,2}(?:,?\d{1,3})*(?:(?:\.\d+)?))%")]

CURRENCY = [
    re.compile(
        r"([(]?)([-]?)[$](\d{0,2}(?:,?\d{1,3})*(?:(?:\.\d+)?))([KkBbMmTt])?"
    )
]

DATE = ["%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"]

TIME = ["%H:%M:%S", "%H:%M", "%I:%M:%S %p", "%I:%M %p", "%I:%M%p"]

DATETIME = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M:%S.%fZ",
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S.%fZ",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%d+%H:%M:%S",
    "%Y-%m-%d+%H:%M",
    "%m/%d/%Y %H:%M:%S",
    "%m/%d/%y %H:%M:%S",
    "%m/%d/%Y %I:%M:%S %p",
    "%m/%d/%y %I:%M:%S %p",
]

TRUE = ["True", "TRUE", "true"]

FALSE = ["False", "FALSE", "false"]

DATELIKE = DATE + DATETIME
