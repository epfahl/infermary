`Infermary` is a Python library for type inference and casting of tabular data.


## Installation

First, clone the repo. Then install dependencies:

```
pip install -r requirements.txt
```


## Type Inference and Supported Types

Type inference in `infermary` is accomplished by attempting to cast a given string literal to an instance of an object with a certain type.  If the cast is successful, the corresponding type is returned.  If the attempt fails, a `CastError` is raised.  `infermary` loops over an ordered list of types until a successful cast is found.

Below is the list of supported types in the order that `infermary` attempts casting.  Each type is accompanied by examples of strings for which the corresponding type is inferred.

```
 missing -- "", "null", "NaN"
 integer -- "0", "123", "1e2"
   float -- "0.1", "1.23", "1e-1"
  number -- [union of integer and float]
 boolean -- "True", "FALSE", "true"
datetime -- "2017-10-13 15:14:13", "2017-10-13T15:14:13"
    date -- "2017-10-13", "10/13/17"
    time -- "15:14:13", "3:14 pm"
  string -- "foo", "bar"
```

Since the input is a string, `infermary` will always default to inferring a `string` type if no other type casts are successful.

It is important to note that `infermary` has an explicit `missing` type that is inferred for a string equal to one of the associated sentinel values.

## Table Schema Inference

A table schema is a record of the types for each table column.  Below is a sample of tabular data in the format required by `infermary`:

```
{
    "header": ["Name", "Height", "Age"],
    "rows": [
        ["Name", "Height", "Age"],
        ["Foo", "5.7", "15"],
        ["Bar", "2.1", "1"],
        ["Baz", "", "49"]
    ]
}
```

If one is distinguishing between integer and float numeric values, this table has the expected schema:

```
[
    {"name": "Name", "type": "string"},
    {"name": "Height", "type": "float"},
    {"name": "Age", "type": "integer"}
]
```

Notice that one of the cells is empty.  To infer the schema of the table, it is necessary to count the occurrence of each type in a given column and make a statistical determination of the most likely type.  Currently, `infermary` chooses the column type based on a *majority vote that excludes the counts of `missing` entries.*


## Usage

### Literals

To infer the type of a string literal, set the list of inferred types and call `literal.infer_type`:

```python
>>> from infermary import literal
>>> inferred_types = ["missing", "integer", "float", "boolean", "date", "time", "datetime", "string"]
>>> literal.infer_type("2017-10-13", inferred_types=inferred_types)
"date"
```

To cast to a value object against a given type, call `literal.cast`:

```python
>>> from infermary import literal
>>> literal.cast("2017-10-13", "date")
datetime.date(2017, 10, 13)
>>> literal.cast("123", "date")  # raises CastError
```

### Tables

Table schema inference is accomplished with the `infer_schema` function:

```python
>>> from infermary import table
>>> inferred_types = ["missing", "integer", "float", "boolean", "date", "time", "datetime", "string"]
>>> header = ["Name", "Value", "Rank", "Date", "Time", "IsTrue", "FuBar"]
>>> rows = [
    ["foo", "1.2", "1", "2017-10-13", " 3:14 pm", "TRUE ", "    "],
    ["foo", "1.2", "1", "2017-10-13", " 15:14  ", "true ", "null"],
    ["bar", "   ", "1", "2017-10-13", " 3:14 pm", "TRUE ", "NaN "],
    ["bar", "   ", "2", "2017-10-13", " 3:14 pm", "     ", "    "],
    ["baz", "1.2", "2", "2017-10-13", "15:14 pm", "FALSE", "    "],
    ["foo", "1.2", "3", "2017-10-13", " 3:14 pm", "False", "    "]
]
>>> tbl = {"header": header, "rows": rows}
>>> table.infer_schema(tbl, inferred_types=inferred_types)
[
    {"name": "Name", "type": "string"},
    {"name": "Value", "type": "float"},
    {"name": "Rank", "type": "integer"},
    {"name": "Date", "type": "date"},
    {"name": "Time", "type": "time"},
    {"name": "IsTrue", "type": "boolean"},
    {"name": "FuBar", "type": "missing"}
]
```

To make things interesting, this table has extra spaces around string values, cells with empty strings, cells with explicit `null` sentinel values, and one incorrectly formatting time.

Casting of a table of literals against a schema is accomplished with `table.cast` function.  Using the sample data above and the schema returned from `table.infer_schema` (named `schema` below), we find

```python
>>> from infermary import table
>>> table.cast(tbl, schema)
{
    "header": ["Name", "Value", "Rank", "Date", "Time", "IsTrue", "FuBar"],
    "rows": [
        ["foo", 1.2, 1, datetime.date(2017, 10, 13), datetime.time(15, 14), True, None],
        ... additional rows ommitted ...
    ]
}
```

### Default and Custom Type Lists

In the above inference examples, the list of inferred types was explicitly specified.  Note that order of the provided type list is irrelevant; the system will order the types according to the ordered master type list.  If no types are provided, `infermary` will use the default:

```
["missing", "number", "boolean", "date", "time", "datetime", "string"]
```

## Error Reporting

The public API of `infermary` exposes variants of `literal.cast`, `literal.infer_type`, `table.cast`, and `table.infer_schema` that return a dict holding both the result and error reports.  These variants are called by appending `_with_error` to the function name.  The returned payload has the form.     

```
{
    "errors": [...error objects...],
    "result": ...function result if no errors; else None...
}
```

If there are errors, each error object has structure

```
{
    "detail": ...error message...,
    "type": ...error type...
}
```

Below is a listing of custom error types in `infermary`, short descriptions of when each error is likely to be encountered, and an example message for each type.

```
CastError
    when: An attempt to cast against the wrong type.
    message: "The input '123' cannot be cast to a value of type 'float'."

InvalidLiteralError
    when: The literal is not a string.
    message: "The input 123 must be a string, not a value of type 'int'."

UnregisteredTypeError
    when: The type is unknown to *infermary*.
    message: "Type 'foobar' is not registered."


TableFormatError
    when: The tabular data is incorrectly formatted.
    message: "The input does not match the accepted table format. The input
     object must be a dictionary with a `header` field that is a
     list of the column names, and a `rows` field that is a list
     of row data."

FatalCastError:
    when: Almost never, but perhaps while refactoring or debugging.
    message: "The input '123' could not be cast to any registered type.
     This probably means the list of types is incomplete."
```
