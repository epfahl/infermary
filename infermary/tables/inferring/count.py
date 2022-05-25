"""Library for counting column types.
"""

from collections import Counter
from functools import partial

from infermary.literals import literal as lt
from infermary.tables import parallel as pl


CHUNKSIZE = 10


def _sample_nonempty(literals, max_sample):
    """Filter for literals that have at least one non-whitespace character,
    then select the first `max_sample` elements.
    """
    return list(filter(lambda l: l.strip(), literals))[:max_sample]


def _count_types(
    literals, inferred_types, max_sample, parallel, chunksize=CHUNKSIZE
):
    """Return a type Counter given a list of literals.
    """
    mapper = pl.map_par(pl.Pool, chunksize=chunksize) if parallel else map
    return Counter(
        mapper(
            partial(lt.infer_type, inferred_types=inferred_types),
            _sample_nonempty(literals, max_sample),
        )
    )


def _count_column_types(columns, inferred_types, max_sample, parallel):
    """Return a list of type Counters for the given list of table columns.
    """
    mapper = pl.map_par(pl.NDPool) if parallel else map
    return mapper(
        partial(
            _count_types,
            inferred_types=inferred_types,
            max_sample=max_sample,
            parallel=parallel,
        ),
        columns,
    )


def _pack_counters(names, counters):
    """Return a list of dicts that contain the type counters for each name.

    [{"name": name, "counter": counter} ...]
    """
    return [
        {"name": name, "counter": counter}
        for name, counter in zip(names, counters)
    ]


def count(table, inferred_types, max_sample, parallel):
    """Return type counters for each header given a table object.

    Examples
    --------
    >>> table = {"header": ["A", "B"], "rows": [["1", "foo"], ["2", "bar"]]}
    >>> collect_type_counts(table)
    [
        {
            "name": "A",
            "counts": Counter({"integer": 2})
        },
        {
            "name": "B",
            "counts": Counter({"string": 2})
        }
    ]
    """
    counters = _count_column_types(
        zip(*table["rows"]), inferred_types, max_sample, parallel
    )
    return _pack_counters(table["header"], counters)
