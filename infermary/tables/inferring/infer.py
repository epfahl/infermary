"""Library for inferring a table schema.
"""

from infermary.tables.inferring import (
    count as ct,
    vote as vt
)


def _pack_voted_type(column_counter):
    """Package the most frequent type into a dict with the column name.
    """
    return {
        "name": column_counter["name"],
        "type": vt.vote(column_counter["counter"])
    }


def infer(table, inferred_types, max_sample, parallel):
    """Return the inferred schema for the given table of string literals.
    """
    return list(map(
        _pack_voted_type,
        ct.count(table, inferred_types, max_sample, parallel)))
