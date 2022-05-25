"""Test type casting against a battery of examples.
"""

import pytest

from infermary import literal as lt
from infermary.literals.helpers import check_and_prepare_literal
from infermary.exceptions import CastError, InvalidLiteralError
from tests.examples import EXAMPLES


def repackage_examples():
    """Given a dict of the form {<type>: <list of in/out examples>}, return a
    list of the form [(<input value>, <result value>, <result type>)] for the
    first example from each type.
    """
    return [
        (type_examples[0] + (result_type,))
        for result_type, type_examples in EXAMPLES.items()
    ]


@pytest.mark.parametrize(
    "literal, result_value, result_type", repackage_examples()
)
def test_literal(literal, result_value, result_type):
    assert lt.cast(literal, result_type) == result_value
    assert lt.infer_type(literal, inferred_types=[result_type]) == result_type


def test_check_and_prepare_literal_pass():
    assert check_and_prepare_literal("  1 ") == "1"


def test_check_and_prepare_literal_fail():
    with pytest.raises(InvalidLiteralError):
        check_and_prepare_literal(1)


def test_cast_type_fail():
    with pytest.raises(CastError):
        lt.cast("1", "float")


def test_cast_with_error_success():
    res = lt.cast_with_error("1", "integer")
    assert res["errors"] == []
    assert res["result"] == 1


def test_cast_with_error_fail():
    res = lt.cast_with_error("1", "float")
    err = res["errors"][0]
    assert "detail" in err
    assert err["type"] == "CastError"
    assert res["result"] is None
