"""Module exposing the `cast` and `infer_type` functions for single literals.
"""

from infermary.literals import types as tp, helpers as hp
from infermary.exceptions import CastError, FatalCastError


def cast(literal, type_):
    """Return the value object for the given string literal and type.
    """
    try:
        lit = hp.check_and_prepare_literal(literal)
        caster = tp.lookup_caster(type_)
        return caster(lit)
    except TypeError:
        raise CastError(
            f"The input '{literal}' cannot be cast to a value of type "
            f"'{type_}'."
        )


def infer_type(literal, inferred_types):
    """Return the inferred type of the given string literal for the given list
    of allowed types.
    """
    for type_ in inferred_types:
        try:
            cast(literal, type_)
            return type_
        except CastError:
            continue
    raise FatalCastError(
        f"The input '{literal}' could not be cast to any registered type. "
        "This probably means the list of types is incomplete."
    )
