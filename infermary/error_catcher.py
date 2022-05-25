"""Error handling wrapper.
"""

from decorator import decorator


def _expand_error(exc):
    """Return a payload that holds the error message and the exception type.
    """
    return {
        "detail": exc.args[0],
        "type": type(exc).__name__
    }


@decorator
def error_catcher(func, *args):
    """Decorator to catch exceptions and return a payload with `error` and
    `result` fields.
    """
    try:
        return {"errors": [], "result": func(*args)}
    except Exception as exc:    # pylint: disable=broad-except
        return {
            "errors": [_expand_error(exc)],
            "result": None
        }
