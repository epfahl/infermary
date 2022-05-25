"""Module holding type inference order and type-to-caster mapping.
"""

from collections import OrderedDict

from infermary.exceptions import UnregisteredTypeError
from infermary.literals.casting import casters

# Master ordered mapping between type names and caster functions.
ORDERED_TYPE_TO_CASTER = OrderedDict([
    ("missing", casters.missing_),
    ("integer", casters.integer_),
    ("float", casters.float_),
    ("number", casters.number_),
    ("boolean", casters.boolean_),
    ("date", casters.date_),
    ("time", casters.time_),
    ("datetime", casters.datetime_),
    ("datelike", casters.datelike_),
    ("percent", casters.percent_),
    ("currency", casters.currency_),
    ("string", casters.string_)
])

# Default ordered list of inferred types.
DEFAULT_ORDERED_INFERRED_TYPES = [
    "missing",
    "number",
    "boolean",
    "date",
    "time",
    "datetime",
    "percent",
    "currency",
    "string"
]


def order_inferred_types(types):
    """Return a list of the given types in the order found in the master
    list.  The given types must be a subset of the master list.  If the input
    is null, return the ordered default list.
    """
    if types is None:
        return DEFAULT_ORDERED_INFERRED_TYPES
    types_set = set(types)
    diff = types_set - set(ORDERED_TYPE_TO_CASTER)
    if diff:
        raise UnregisteredTypeError(
            f"The following types are not registered: {diff}."
        )
    res = list(filter(lambda t: t in types_set, ORDERED_TYPE_TO_CASTER))
    if "string" not in res:
        res.append("string")
    return res


def lookup_caster(type_):
    """Return the cast function for the given type.
    """
    try:
        return ORDERED_TYPE_TO_CASTER[type_]
    except KeyError:
        raise UnregisteredTypeError(f"Type '{type_}' is not registered.")
