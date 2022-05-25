"""Helper functions for casting and schema inference of literal tabular data.
"""

from infermary.exceptions import TableFormatError


def validate_table(table):
    """Return the table data if validation passes; otherwise, raise an
    exception.

    Notes
    -----
    * This is a rough, first pass at structural validation.  The error message
      does not indicate the nature of the problem.
    """
    try:
        header = table["header"]
        rows = table["rows"]
        assert isinstance(header, list)
        assert isinstance(rows, list)
        assert len(rows[0]) == len(header)
    except Exception:
        raise TableFormatError(
            "The input does not match the accepted table format. The input "
            "object must be a dictionary with a `header` field that is a "
            "list of the column names, and a `rows` field that is a list of "
            "row data.  The length of each row must match the header length."
        )
    return table
