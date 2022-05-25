import pytest

from infermary.exceptions import UnregisteredTypeError
from infermary.literals import types as tp


def test_order_inferred_types():
    types = tp.order_inferred_types(['datetime', 'integer', 'time'])
    assert types == ['integer', 'time', 'datetime', 'string']


def test_order_inferred_types_fail():
    with pytest.raises(UnregisteredTypeError):
        tp.order_inferred_types(['numbler', 'string'])


def test_cast_lookup_caster_fail():
    with pytest.raises(UnregisteredTypeError):
        tp.lookup_caster('interger')
