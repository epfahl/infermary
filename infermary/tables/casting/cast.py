"""Library for casting table literals."""

from functools import partial
from itertools import starmap

from infermary.exceptions import CastError
from infermary.literals import literal as lt
from infermary.tables import parallel as pl


CHUNKSIZE = 1000


def _cast_literal(literal, type_):
    """Cast the given literal against the given type.  This function will
    always return a value: the value object if casting succeeds, and None if
    casting fails.
    """
    try:
        return lt.cast(literal, type_)
    except CastError:
        return None


def _cast_literals(literals, type_, parallel, chunksize=CHUNKSIZE):
    """Cast each element of the iterable of literals against the given type.
    """
    mapper = pl.map_par(pl.Pool, chunksize=chunksize) if parallel else map
    return mapper(partial(_cast_literal, type_=type_), literals)


def _cast_columns(columns, types, parallel):
    """Return a list of cast columns for the given list of column types.
    """
    mapper = (
        pl.map_par(pl.NDPool, map_method="starmap") if parallel else starmap
    )
    return mapper(
        partial(_cast_literals, parallel=parallel), zip(columns, types)
    )


def cast(table, schema, parallel):
    """Return a table of value objects given a table of literal values and a
    schema.
    """
    types = [col["type"] for col in schema]
    columns = zip(*table["rows"])
    cast_columns = _cast_columns(columns, types, parallel)
    cast_rows = list(map(list, zip(*cast_columns)))
    return {"header": table["header"], "rows": cast_rows}
