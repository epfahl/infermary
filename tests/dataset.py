"""Example datasets for testing"""
TABLE = {
    "data": {
        "header": ["Name", "Value", "Rank", "Date", "Time", "IsTrue", "FuBar"],
        "rows": [
            ["foo", "1.2", "1", "2017-10-13", " 3:14 pm", "TRUE ", "    "],
            ["foo", "   ", "1", "2017-10-13", " 15:14  ", "TRUE ", "null"],
            ["bar", "   ", "1", "2017-10-13", " 3:14 pm", "TRUE ", "NaN "],
            ["bar", "   ", "2", "2017-10-13", " 3:14 pm", "     ", "    "],
            ["baz", "   ", "2", "2017-10-13", "15:14 pm", "FALSE", "    "],
            ["foo", "1.2", "3", "2017-10-13", " 3:14 pm", "FALSE", "    "],
        ],
    },
    "inferred_types": [
        "string",
        "float",
        "integer",
        "date",
        "time",
        "boolean",
        "missing",
    ],
    "default_types": [
        "string",
        "number",
        "number",
        "date",
        "time",
        "boolean",
        "missing",
    ],
}


TABLE_W_SYMBOLS = {
    "data": {
        "header": [
            "CurrencySymbol",
            "CurrencyEmpties",
            "PercentSymbol",
            "PercentEmpties",
        ],
        "rows": [
            ["$", "$", "%", "%"],
            ["$", "$10.00", "%", "4%"],
            ["$", "$0.00", "%", "40%"],
        ],
    },
    "inferred_types": ["string", "string", "string", "string"],
    "default_types": ["string", "currency", "string", "percent"],
}
