"""Module exposing the `cast` and `infer_schema` functions for casting and
schema inference of literal tabular data.

Notes
-----
* Tabular data is assumed to have the form
  {
      "header": [column header names],
      "rows": [[row values], ...]
  }
"""

from infermary.tables import helpers as hp
from infermary.tables.casting import cast as caster
from infermary.tables.inferring import infer as inferrer


def infer_schema(table, inferred_types, max_sample, parallel):
    """Return the inferred schema for the given table of string literals.
    """
    return inferrer.infer(
        hp.validate_table(table), inferred_types, max_sample, parallel
    )


def cast(table, schema, parallel):
    """Return a table of value objects given a table of literal values and a
    schema.
    """
    return caster.cast(hp.validate_table(table), schema, parallel)
