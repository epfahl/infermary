"""Module exposing public API to casting and type inference of single string
literals.
"""

from infermary.literals import types as tp, literal as lt
from infermary import error_catcher as ec


def cast(literal, type_):
    """Return the value object for the given string literal and type.  A
    TypeError is raised if the literal cannot be cast against the given type.

    Examples
    --------
    >>> cast("", "missing")
    None
    >>> cast("1", "integer")
    1
    >>> cast("foo", "string")
    "foo"
    >>> cast(1, "integer")  # raises TypeError
    >>> cast("1", "datetime")  # raises TypeError
    """
    return lt.cast(literal, type_)


def infer_type(literal, inferred_types=None):
    """Return the inferred type of the given string literal for the given list
    of types.  If inferred types are not provided, a default list is used.

    Examples
    --------
    >>> infer_type("")
    "missing"
    >>> infer_type("1")
    "integer"
    >>> infer_type("foo")
    "string"
    """
    ordered_inferred_types = tp.order_inferred_types(inferred_types)
    return lt.infer_type(literal, ordered_inferred_types)


cast_with_error = ec.error_catcher(cast)
infer_type_with_error = ec.error_catcher(infer_type)
