"""Module exposing public API to casting and schema inference of literal
tabular data.
"""

from infermary import error_catcher as ec
from infermary.literals import types as tp
from infermary.tables import table as tb

MAX_SAMPLE = 1000


def cast(table, schema, parallel=False):
    """Return a table of value objects given a table of literal values and a
    schema.  If `parallel` is True, the casting computation is performed in
    parallel.

    The input table and schema have the forms

    Examples
    --------
    >>> table = {"header": ["A", "B"], "rows": [["1", "foo"], ["2", "bar"]]}
    >>> schema = [
        {"name": "A", "type": "integer"},
        {"name": "B", "type": "string"}
    ]
    >>> cast(table, schema)
    {"header": ["A", "B"], "rows": [[1, "foo"], [2, "bar"]]}
    """
    return tb.cast(table, schema, parallel)


def infer_schema(
    table, inferred_types=None, max_sample=MAX_SAMPLE, parallel=False
):
    """Return the inferred schema for the given table of string literals and
    list of inferred types.   If inferred types are not provided, a default
    list is used. The parameters `max_sample` is the maximum sample size of
    non-empty literals used for type inference. If `parallel` is True, the
    inference computation is performed in parallel.

    The input table has the form

    Examples
    --------
    >>> table = {"header": ["A", "B"], "rows": [["1", "foo"], ["2", "bar"]]}
    >>> infer_schema(table)
    [
        {"name": "A", "type": "integer"},
        {"name": "B", "type": "string"}
    ]
    """
    ordered_inferred_types = tp.order_inferred_types(inferred_types)
    return tb.infer_schema(table, ordered_inferred_types, max_sample, parallel)


cast_with_error = ec.error_catcher(cast)
infer_schema_with_error = ec.error_catcher(infer_schema)
