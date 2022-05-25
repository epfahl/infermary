"""Test table schema inference and casting."""

import datetime

import pytest

from infermary import exceptions as exc
from infermary import table as tb
from tests.dataset import TABLE, TABLE_W_SYMBOLS


INFERRED_TYPES = [
    "missing",
    "integer",
    "float",
    "boolean",
    "date",
    "time",
    "datetime",
    "string",
]


def test_infer_schema_inferred_types():
    for data_table in (TABLE, TABLE_W_SYMBOLS):
        schema = tb.infer_schema(
            data_table["data"], inferred_types=INFERRED_TYPES
        )
        header, types = list(
            zip(*[(col["name"], col["type"]) for col in schema])
        )
        assert list(header) == data_table["data"]["header"]
        assert list(types) == data_table["inferred_types"]


def test_infer_schema_default_types():
    for data_table in (TABLE, TABLE_W_SYMBOLS):
        schema = tb.infer_schema(data_table["data"])
        header, types = list(
            zip(*[(col["name"], col["type"]) for col in schema])
        )
        assert list(header) == data_table["data"]["header"]
        assert list(types) == data_table["default_types"]


def test_infer_schema_parallel():
    schema = tb.infer_schema(
        TABLE["data"], inferred_types=INFERRED_TYPES, parallel=True
    )
    header, types = list(zip(*[(col["name"], col["type"]) for col in schema]))
    assert list(header) == TABLE["data"]["header"]
    assert list(types) == TABLE["inferred_types"]


def test_cast_standard():
    schema = tb.infer_schema(TABLE["data"])
    rows = tb.cast(TABLE["data"], schema)["rows"]
    assert rows[0][4] == datetime.time(15, 14)


def test_cast_symbols():
    schema = tb.infer_schema(TABLE_W_SYMBOLS["data"])
    rows = tb.cast(TABLE_W_SYMBOLS["data"], schema)["rows"]
    assert rows[0][1] is None, "'$' gets cast to None if type is currency"
    assert rows[0][-1] is None, "'%' gets cast to None if type is percent"


def test_cast_parallel():
    schema = tb.infer_schema(TABLE["data"])
    first_row = tb.cast(TABLE["data"], schema, parallel=True)["rows"][0]
    assert first_row[4] == datetime.time(15, 14)


def test_table_error_empty_dict():
    with pytest.raises(exc.TableFormatError):
        tb.infer_schema({})


def test_table_error_empty_list():
    with pytest.raises(exc.TableFormatError):
        tb.infer_schema([])


def test_table_error_len_mismatch():
    with pytest.raises(exc.TableFormatError):
        tb.infer_schema({"header": ["A"], "rows": [[1, 2], [3, 4]]})


def test_infer_schema_with_error_success():
    res = tb.infer_schema_with_error(TABLE["data"])
    assert res["errors"] == []
    assert len(res["result"]) == 7


def test_infer_schema_with_error_fail():
    res = tb.infer_schema_with_error({})
    err = res["errors"][0]
    assert "detail" in err
    assert err["type"] == "TableFormatError"
    assert res["result"] is None
